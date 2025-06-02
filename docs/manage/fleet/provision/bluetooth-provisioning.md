---
title: "Bluetooth provisioning with viam-agent"
linkTitle: "Bluetooth provisioning"
weight: 70
type: "docs"
description: "Learn how to use Bluetooth Low Energy (BLE) for machine provisioning as an alternative to WiFi hotspot provisioning."
tags: ["fleet management", "viam-server", "viam-agent", "bluetooth", "provisioning"]
images: ["/installation/thumbnails/install.png"]
imageAlt: "Bluetooth provisioning"
languages: []
viamresources: []
platformarea: ["fleet"]
level: "Advanced"
date: "2025-06-02"
prev: "/manage/fleet/provision/end-user-setup/"
# updated: ""  # When the tutorial was last entirely checked
# SMEs: James, Ale
cost: "0"
---

Bluetooth provisioning enables machine setup using Bluetooth Low Energy (BLE) as an alternative to WiFi hotspot provisioning. This method is particularly useful in environments with many WiFi networks, where hotspot provisioning may be less reliable, or when you want to avoid creating an open WiFi hotspot.

## Overview

When Bluetooth provisioning is enabled, `viam-agent` advertises a BLE service that mobile applications can connect to directly. This allows users to provision machines without needing to join a WiFi hotspot, providing a more streamlined setup experience on mobile devices.

### Key Features

- **Direct BLE connection**: Mobile apps connect directly to the machine via Bluetooth
- **Encrypted communication**: All credential exchanges use RSA OAEP encryption
- **Parallel operation**: Can work alongside WiFi hotspot provisioning
- **Mobile-optimized**: Designed for optimal mobile app user experience
- **Automatic adapter selection**: Automatically selects the first available Bluetooth adapter

## How Bluetooth Provisioning Works

1. **Service Advertisement**: When provisioning mode starts, `viam-agent` advertises a BLE service with a name beginning with `viam-setup-`
1. **Mobile App Discovery**: Compatible mobile apps scan for and connect to the advertised BLE service
1. **Secure Handshake**: The machine generates an RSA key pair and shares the public key with the mobile app
1. **Credential Exchange**: The mobile app encrypts and sends WiFi credentials and/or machine credentials
1. **Network Connection**: The machine attempts to connect using the provided credentials
1. **Service Installation**: Once connected, `viam-agent` installs and starts `viam-server`

## Configuration

### Basic Configuration

To enable Bluetooth provisioning, ensure `disable_bt_provisioning` is set to `false` (the default) in your `viam-defaults.json`:

```json {class="line-numbers linkable-line-numbers"}
{
  "network_configuration": {
    "disable_bt_provisioning": false,
    "disable_wifi_provisioning": false
  }
}
```

### Advanced Configuration

For machines with multiple Bluetooth adapters, specify which adapter to use:

```json {class="line-numbers linkable-line-numbers"}
{
  "network_configuration": {
    "disable_bt_provisioning": false,
    "bluetooth_adapter_name": "hci0"
  }
}
```

### Bluetooth-Only Provisioning

To use only Bluetooth provisioning and disable WiFi hotspot provisioning:

```json {class="line-numbers linkable-line-numbers"}
{
  "network_configuration": {
    "disable_bt_provisioning": false,
    "disable_wifi_provisioning": true,
    "fragment_id": "your-fragment-id"
  }
}
```

{{< alert title="Note" color="note" >}}
When using Bluetooth-only provisioning, you must provide a `fragment_id` for mobile app configuration.
{{< /alert >}}

## Security

Bluetooth provisioning implements several security measures:

### Encryption

- **RSA OAEP Encryption**: All credential data is encrypted using RSA OAEP with SHA-256
- **2048-bit Keys**: Uses 2048-bit RSA keys for strong encryption
- **Per-Session Keys**: New key pairs are generated for each provisioning session
- **Public Key Exchange**: Public keys are shared using x509 PKIX encoding

### Communication Protocol

The BLE service uses predefined UUIDs for different characteristics:

- **Service UUID**: Generated from namespace `74a942f4-0f45-43f4-88ca-f87021ae36ea`
- **Write Characteristics**: For receiving encrypted credentials (SSID, PSK, machine credentials)
- **Read Characteristics**: For sharing status, network lists, and public keys
- **Encrypted Payloads**: All sensitive data is encrypted before transmission

## Bluetooth Service Characteristics

The Bluetooth service exposes several characteristics for different functions:

### Write-Only Characteristics

- **SSID**: Receives encrypted WiFi network name
- **PSK**: Receives encrypted WiFi password
- **Robot Part ID**: Receives encrypted machine part identifier
- **Robot Part Secret**: Receives encrypted machine secret
- **App Address**: Receives encrypted cloud app address

### Read-Only Characteristics

- **Status**: Provides machine configuration and connection status
- **Networks**: Lists available WiFi networks with signal strength and security info
- **Public Key**: Shares the RSA public key for encryption
- **Errors**: Reports any provisioning errors

## Mobile App Integration

### Supported Platforms

Bluetooth provisioning is designed for mobile applications using:

- **Flutter SDK**: Full BLE provisioning support
- **TypeScript SDK**: BLE provisioning capabilities
- **Viam Mobile App**: Native Bluetooth provisioning support

### App Development Considerations

When developing mobile apps with Bluetooth provisioning:

1. **BLE Permissions**: Ensure your app requests appropriate Bluetooth permissions
1. **Service Discovery**: Scan for services with the `viam-setup-` prefix
1. **Encryption Handling**: Implement RSA OAEP encryption for credential transmission
1. **Error Handling**: Monitor the errors characteristic for provisioning feedback
1. **Status Monitoring**: Check the status characteristic to track provisioning progress

## Troubleshooting

### Bluetooth Adapter Issues

**Problem**: Bluetooth provisioning not starting

**Solutions**:
1. Check if Bluetooth is available:
   ```sh {class="command-line" data-prompt="$"}
   bluetoothctl list
   ```

1. Verify Bluetooth service status:
   ```sh {class="command-line" data-prompt="$"}
   sudo systemctl status bluetooth
   ```

1. For multiple adapters, specify the correct one:
   ```json
   {
     "network_configuration": {
       "bluetooth_adapter_name": "hci0"
     }
   }
   ```

### Mobile Device Connection Issues

**Problem**: Mobile app cannot discover the machine

**Solutions**:
1. Ensure Bluetooth is enabled on the mobile device
1. Check that the mobile app has Bluetooth permissions
1. Verify the device supports Bluetooth Low Energy (BLE)
1. Try restarting Bluetooth on the mobile device

### Encryption Errors

**Problem**: Credential transmission fails

**Solutions**:
1. Check `viam-agent` logs for encryption errors:
   ```sh {class="command-line" data-prompt="$"}
   sudo journalctl -u viam-agent -f
   ```

1. Ensure the mobile app is using the correct public key
1. Verify RSA OAEP implementation in the mobile app

### Configuration Issues

**Problem**: Bluetooth provisioning not enabled

**Solutions**:
1. Verify `disable_bt_provisioning` is set to `false`
1. Check that `disable_network_configuration` is not set to `true`
1. Ensure the system has a working Bluetooth adapter

## Testing and Development

### CLI Testing Tool

The `viam-agent` repository includes a CLI tool for testing Bluetooth provisioning:

```sh {class="command-line" data-prompt="$"}
# Clone the agent repository
git clone https://github.com/viamrobotics/agent.git
cd agent

# Scan for Bluetooth devices
go run ./cmd/provisioning-client/ --scan

# Test Bluetooth provisioning
go run ./cmd/provisioning-client/ --bluetooth --status

# Set WiFi credentials via Bluetooth
go run ./cmd/provisioning-client/ --bluetooth --ssid="MyNetwork" --psk="MyPassword"

# Set machine credentials via Bluetooth
go run ./cmd/provisioning-client/ --bluetooth --partID="part-id" --secret="secret" --appaddr="https://app.viam.com:443"
```

### Development Environment

For development and testing:

1. **Filter Devices**: Use the `--filter` option to find specific devices:
   ```sh {class="command-line" data-prompt="$"}
   go run ./cmd/provisioning-client/ --scan --filter="viam-setup"
   ```

1. **Monitor Status**: Check provisioning status:
   ```sh {class="command-line" data-prompt="$"}
   go run ./cmd/provisioning-client/ --bluetooth --status
   ```

1. **List Networks**: View available WiFi networks:
   ```sh {class="command-line" data-prompt="$"}
   go run ./cmd/provisioning-client/ --bluetooth --networks
   ```

## Best Practices

### Configuration

- **Enable Both Methods**: Keep both Bluetooth and WiFi provisioning enabled for maximum compatibility
- **Fragment Configuration**: Always provide a `fragment_id` when using mobile apps
- **Adapter Selection**: Specify `bluetooth_adapter_name` for machines with multiple Bluetooth adapters

### Security

- **Key Management**: RSA keys are automatically generated per session - no manual key management required
- **Credential Handling**: All sensitive data is encrypted before transmission
- **Network Security**: Consider the security of the WiFi networks being configured

### User Experience

- **Clear Instructions**: Provide clear setup instructions for end users
- **Fallback Options**: Ensure WiFi hotspot provisioning is available as a fallback
- **Error Reporting**: Monitor the errors characteristic for user feedback

## Limitations

- **BLE Requirement**: Both the machine and mobile device must support Bluetooth Low Energy
- **Mobile Focus**: Optimized for mobile app workflows rather than web browsers
- **Linux Support**: Currently supported on Linux systems with Bluetooth adapters
- **Range Limitation**: Bluetooth has a shorter range than WiFi hotspots

## Next Steps

- [Set up machine provisioning](/manage/fleet/provision/setup/)
- [Configure viam-agent](/manage/reference/viam-agent/)
- [End-user setup guide](/manage/fleet/provision/end-user-setup/)
- [Mobile app development with Flutter SDK](https://flutter.viam.dev/)