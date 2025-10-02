---
linkTitle: "Configure machine settings"
title: "Configure machine operating system settings"
weight: 50
layout: "docs"
type: "docs"
description: "Configure network settings, operating system package updates and logging defaults."
---

The `viam-agent` configuration allows you to configure:

- [settings for package updates for the host operating system](#manage-os-package-updates)
- [networks a machine can connect to](#configure-networks)
- [parameters for operating system logging](#configure-operating-system-logging)

## Manage OS package updates

By default, the configuration in <FILE>/etc/apt/apt.conf.d/</FILE> determines the behavior for updating operating system packages.
To manage OS package updates using Viam, add a `"system_configuration"` object to the `"agent"` object in the machine's JSON configuration, if it doesn't already exist.
Then, add the `"os_auto_upgrade_type"` field in its attributes:

```json
"agent": {
    "system_configuration": {
        "os_auto_upgrade_type": "security"
    }
}
```

When the `os_auto_upgrade_type` is set, `viam-agent` will install the `unattended-upgrades` package and replace `20auto-upgrades` and `50unattended-upgrades` in <FILE>/etc/apt/apt.conf.d/</FILE> with an Origins-Pattern list generated automatically from configured repositories on the system.
Custom repos installed on the system at the time the setting is enabled will be included.

You can set automatic upgrades to the following options:

- `"all"`: automatic upgrades are performed for all packages
- `"security"`: automatic upgrades for only packages containing `"security"` in their codename (for example `bookworm-security`)
- `""`: disable automatic upgrades

For complete reference information, see [viam-agent](/manage/reference/viam-agent/#system-configuration).

## Configure networks

By default, your machine can connect to networks added at the operating system level, for example, directly in NetworkManager.

For an already-online device, you can add new WiFi networks by updating the `"agent"` value in the machine's JSON configuration.
This is primarily useful for a machine that moves between different networks, so the machine can automatically connect when moved between locations.

To add networks, add or update the `additional_networks` field to the `agent` object and set `"turn_on_hotspot_if_wifi_has_no_internet": true`.

{{< alert title="Note" color="note" >}}
If you are adding networks to a machine’s configuration, the machine will need to be connected to the internet to retrieve the configuration information containing the network credentials before it can use them.
{{< /alert >}}

The following configuration defines the connection information and credentials for two WiFi networks named `fallbackNetOne` and `fallbackNetTwo`.
`viam-agent` will try to connect to `fallbackNetOne` first, since its priority is highest.
If the `fallbackNetOne` is not available or the machine can connect but internet is not available, `viam-agent` will then attempt to connect to `fallbackNetTwo`.

```json
"agent": {
    "additional_networks": {
        "network_name_1": {
            "type": "wifi",
            "ssid": "fallbackNetOne",
            "psk": "myFirstPassword",
            "priority": 30
        },
        "network_name_2": {
            "type": "wifi",
            "ssid": "fallbackNetTwo",
            "psk": "mySecondPassword",
            "priority": 10
        }
    }
}
```

Configuring multiple WiFi networks for the Micro-RDK is similar but the only supported attributes are `priority`, `psk`, and `ssid`.

For complete reference information, see [viam-agent](/manage/reference/viam-agent/#network_configuration).

## Configure network settings for tunneling

To tunnel to a machine part you must first explicitly enumerate ports to which you are allowed to tunnel in your machine's JSON config.
The following configuration allows you to tunnel to ports `5900` and `5901`:

```json {class="line-numbers linkable-line-numbers"}
"network": {
  "traffic_tunnel_endpoints": [
    {
      "port": 5900
    },
    {
      "port": 5901,
      "connection_timeout": "5s"
    }
  ]
}
```

Then you can use the [`viam machine part tunnel`](https://docs.viam.com/dev/tools/cli/#machines-alias-robots-and-machine) command:

```sh {class="command-line" data-prompt="$" data-output="2-10"}
viam machine part tunnel --part=123 --destination-port=1111 --local-port 5900
```

## Configure network settings to disable TLS

To configure your machine to disable TLS on the hosted HTTP server, you must specify `"no_tls": true` in your machine's configuration:

```json {class="line-numbers linkable-line-numbers"}
"network": {
  "no_tls": true
}
```

## Configure bind address and port

If you are running `viam-server` on a different port that `8080`, set the `bind_address` in your machine settings:

```json {class="line-numbers linkable-line-numbers"}
"network": {
  "bind_address": "localhost:8081"
}
```

## Configure operating system logging

By default, the maximum disk space `journald` will use for `viam-server` logs is 512MB.

To adjust these settings update the `"agent"` value in the machine's JSON configuration.

For complete reference information, see [viam-agent](/manage/reference/viam-agent/#system-configuration) and the [`journald` docs](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html#SystemMaxUse=).

### Set the maximum disk space

To set the maximum disk space `journald` will use to persist logs, add the `logging_journald_system_max_use_megabytes` field to the `system_configuration` object.
You may need to add the `system_configuration` object to the `agent` object if it doesn't already exist.

The configured values will take precedence over operating system defaults.

```json
"agent": {
    "system_configuration": {
        "os_auto_upgrade_type": "security",
        "logging_journald_system_max_use_megabytes": 512
    }
}
```

### Set the runtime space limit space

To set the temporary space limit for logs, add the `logging_journald_runtime_max_use_megabytes` field to the `system_configuration` object.
You may need to add the `system_configuration` object to the `agent` object if it doesn't already exist.

The configured values will take precedence over operating system defaults.

```json
"agent": {
    "system_configuration": {
        "os_auto_upgrade_type": "security",
        "logging_journald_runtime_max_use_megabytes": 512
    }
}
```

### Forward system logs to the cloud

You can configure `viam-agent` to forward system logs from journald to the cloud for additional diagnostics information.
This allows you to view system logs from your machine alongside Viam's own logs.

To enable system log forwarding, add the `forward_system_logs` field to the `system_configuration` object. This field accepts a comma-separated list of service identifiers to include or exclude from forwarding.

```json
"agent": {
    "system_configuration": {
        "forward_system_logs": "kernel,NetworkManager,tailscaled"
    }
}
```

{{< alert title="Note" color="note" >}}
System log forwarding requires journald to be available on the system. This feature is only supported on Linux systems.
{{< /alert >}}

#### Filtering options

You can control which system logs are forwarded using the following syntax:

- `"all"`: Forward all system logs (in addition to`viam-agent` and `viam-server` logs which are sent directly to the cloud and always visible)
- Comma-separated list of service identifiers: Forward only logs from the specified services
- Prefix a service with `-` to exclude it: For example, `"all,-gdm,-tailscaled"` forwards all logs except those from `gdm` and `tailscaled`

Examples:

```json
// Forward only kernel, NetworkManager, and tailscaled logs
"forward_system_logs": "kernel,NetworkManager,tailscaled"

// Forward all system logs except gdm and tailscaled
"forward_system_logs": "all,-gdm,-tailscaled"

// Disable system log forwarding (default)
"forward_system_logs": ""
```
