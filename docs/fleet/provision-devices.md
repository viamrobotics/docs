---
linkTitle: "Provision devices"
title: "Provision devices"
weight: 20
layout: "docs"
type: "docs"
description: "Set up automated provisioning so machines configure themselves when they first come online."
---

Set up zero-touch provisioning so machines you ship or deploy automatically configure themselves on first boot. You install `viam-agent` on the device during manufacturing, define a configuration in a defaults file, and when someone powers on the device and provides network credentials, the machine downloads and applies its configuration from a fragment.

## When to use provisioning

Use provisioning when you are manufacturing or deploying multiple devices that need to come online with a predefined configuration without manual setup per device. Provisioning is designed for:

- Shipping devices to customers who will connect them to their own networks
- Deploying devices in facilities where IT staff will connect them
- Setting up field devices that need WiFi or Bluetooth onboarding

If you are setting up a small number of machines manually, you can skip provisioning and configure each machine directly in the Viam app.

## How provisioning works

1. During manufacturing, you flash an OS image with `viam-agent` pre-installed and a defaults file (`viam-defaults.json`) that specifies a fragment and provisioning options.
2. On first boot, `viam-agent` checks for network connectivity. If no known network is available, it enters provisioning mode.
3. In provisioning mode, `viam-agent` creates a WiFi hotspot (or advertises a Bluetooth service) so the end user can provide network credentials.
4. The end user connects to the hotspot or Bluetooth and provides WiFi credentials through a mobile app or captive portal.
5. `viam-agent` connects to the provided network, registers the machine with Viam (using the fragment from the defaults file), and downloads `viam-server` and the configured software.
6. The machine is now online and running.

## Prerequisites

- A [fragment](/fleet/reuse-configuration/) with the configuration your machines should use. Note the fragment ID.
- A device with a supported Linux OS. See the [platform requirements](/foundation/) for supported platforms.

## 1. Create the defaults file

Create a file called `viam-defaults.json` that defines the provisioning behavior. At minimum, specify a `fragment_id`.

```json
{
  "network_configuration": {
    "manufacturer": "your-company",
    "model": "your-product",
    "fragment_id": "your-fragment-id",
    "hotspot_prefix": "your-product-setup",
    "hotspot_password": "viamsetup"
  }
}
```

### Defaults file fields

All fields are optional except where noted.

| Field                                     | Type    | Default             | Description                                                                                                                                                         |
| ----------------------------------------- | ------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `manufacturer`                            | string  | `"viam"`            | Displayed on the captive portal or mobile app during setup.                                                                                                         |
| `model`                                   | string  | `"custom"`          | Displayed on the captive portal or mobile app during setup.                                                                                                         |
| `fragment_id`                             | string  | —                   | The fragment to apply to machines provisioned with this defaults file. Required when using the mobile app for provisioning.                                         |
| `hotspot_interface`                       | string  | First 802.11 device | The network interface to use for the provisioning hotspot.                                                                                                          |
| `hotspot_prefix`                          | string  | `"viam-setup"`      | Prepended to the device hostname to create the hotspot SSID: `{prefix}-{hostname}`.                                                                                 |
| `hotspot_password`                        | string  | `"viamsetup"`       | Password for the WiFi hotspot or Bluetooth connection. When using the mobile app, must be `"viamsetup"`.                                                            |
| `disable_captive_portal_redirect`         | boolean | `false`             | When `true`, only `*.setup` domains redirect to the portal, preventing mobile devices from auto-opening it. Set to `true` when using a mobile app for provisioning. |
| `disable_bt_provisioning`                 | boolean | `false`             | When `true`, disables Bluetooth provisioning. The machine will not advertise Bluetooth services.                                                                    |
| `disable_wifi_provisioning`               | boolean | `false`             | When `true`, disables WiFi hotspot provisioning.                                                                                                                    |
| `bluetooth_trust_all`                     | boolean | `false`             | When `true`, accepts all Bluetooth pairing requests without requiring an unlock from a mobile app. Only needed for Bluetooth tethering.                             |
| `turn_on_hotspot_if_wifi_has_no_internet` | boolean | `false`             | When `true`, the device re-enters provisioning mode if the connected WiFi network has no internet access.                                                           |
| `offline_before_starting_hotspot_minutes` | integer | `2`                 | Minutes to wait for a known network before entering provisioning mode. Increase for environments where the WiFi router boots slowly.                                |
| `user_idle_minutes`                       | integer | `5`                 | Minutes before considering a provisioning user idle and resuming normal connection attempts.                                                                        |
| `retry_connection_timeout_minutes`        | integer | `10`                | Minutes before exiting provisioning mode to try other connection methods. Provisioning mode restarts if connectivity does not improve.                              |
| `wifi_power_save`                         | boolean | —                   | When set, explicitly enables or disables WiFi power save for all connections managed by NetworkManager. If not set, the system default applies.                     |
| `device_reboot_after_offline_minutes`     | integer | `0`                 | When set to a positive number, reboots the device after this many minutes offline in hotspot mode. `0` disables.                                                    |

## 2. Run the preinstall script

Download and run the preinstall script to install `viam-agent` and the defaults file onto your device or OS image.

{{< tabs >}}
{{% tab name="wget" %}}

```sh {class="command-line" data-prompt="$"}
wget https://storage.googleapis.com/packages.viam.com/apps/viam-agent/preinstall.sh
chmod 755 preinstall.sh
```

{{% /tab %}}
{{% tab name="curl" %}}

```sh {class="command-line" data-prompt="$"}
curl -O https://storage.googleapis.com/packages.viam.com/apps/viam-agent/preinstall.sh
chmod 755 preinstall.sh
```

{{% /tab %}}
{{< /tabs >}}

Run the script from the same directory that contains your `viam-defaults.json` file:

```sh {class="command-line" data-prompt="$"}
sudo ./preinstall.sh
```

The script picks up `viam-defaults.json` from the current directory and copies it along with `viam-agent` to the appropriate locations on the device. For Raspberry Pi, it modifies the first-run script to start `viam-agent` on boot.

To install onto an external rootfs (for example, a mounted SD card image):

```sh {class="command-line" data-prompt="$"}
sudo ./preinstall.sh /path/to/rootfs
```

## 3. Boot the device

Power on the device. `viam-agent` starts automatically and:

1. Checks for a known WiFi network.
2. If none is found after `offline_before_starting_hotspot_minutes` (default: 2 minutes), creates a WiFi hotspot named `{hotspot_prefix}-{hostname}`.
3. Waits for a user to connect and provide network credentials.

The end user completes setup by following the [end-user device setup](/fleet/end-user-setup/) instructions.

## 4. Verify provisioning

After the end user provides network credentials:

1. The machine connects to the provided network.
2. `viam-agent` registers the machine with Viam and applies the fragment.
3. `viam-server` is downloaded and started.
4. The machine appears in the Viam app fleet dashboard as **Live**.

Check the fleet dashboard at [app.viam.com/fleet/machines](https://app.viam.com/fleet/machines) to confirm the machine is online.

## Provision additional networks

To configure fallback WiFi networks that the device can connect to without going through provisioning mode, add an `additional_networks` section to the defaults file:

```json
{
  "network_configuration": {
    "fragment_id": "your-fragment-id",
    "hotspot_prefix": "your-product-setup"
  },
  "additional_networks": {
    "office-wifi": {
      "type": "wifi",
      "ssid": "OfficeNetwork",
      "psk": "office-password",
      "priority": 30
    },
    "factory-wifi": {
      "type": "wifi",
      "ssid": "FactoryNetwork",
      "psk": "factory-password",
      "priority": 20
    }
  }
}
```

Networks with higher `priority` values are preferred. See [system settings](/fleet/system-settings/) for the full network configuration reference.

## Limitations

- The preinstall script cannot be run twice on the same device. To re-provision, delete `/etc/viam.json` and reboot.
- Provisioning requires `viam-agent`, which runs on Linux systems with NetworkManager. It is not available for microcontrollers.
- When using the Viam mobile app for provisioning, the `hotspot_password` must be `"viamsetup"`.

## Related pages

- [End-user device setup](/fleet/end-user-setup/) for the end-user side of the provisioning flow
- [Reuse configuration](/fleet/reuse-configuration/) for creating the fragment your provisioned machines will use
- [System settings](/fleet/system-settings/) for configuring additional networks and agent behavior
- [Build apps](/build-apps/) for building custom provisioning apps using the Flutter or TypeScript SDK's provisioning client
