---
title: "viam-agent"
linkTitle: "viam-agent"
weight: 20
no_list: true
type: docs
description: "The viam-agent is a self-updating service manager that maintains the lifecycle for Viam's system services, among them viam-server and provisioning."
date: "2024-08-16"
aliases:
  - /configure/agent/
# updated: ""  # When the content was last entirely checked
# SMEs: James, Ale
---

The [`viam-agent`](https://github.com/viamrobotics/agent) is a self-updating service manager that maintains the lifecycle for itself and `viam-server`.

Among other things, `viam-agent`:

- Installs, runs, and monitors `viam-server` or a custom build of `viam-server`.
- Provides tooling for device provisioning and network management.
- Provides automatic updates for `viam-server` and the agent itself.
- Allows control of deployed software versions through the Viam app.
- Provides various operating system settings.

{{< alert title="Support notice" color="note" >}}
Currently, `viam-agent` is only supported on Linux, for amd64 (x86_64) and arm64 (aarch64) CPUs.
{{< /alert >}}

To provision machines using `viam-agent`, see

{{< cards >}}
{{% card link="/manage/fleet/provision/setup/" %}}
{{< /cards >}}

## Installation

You can install `viam-agent` using either an existing machine's part ID and API key, or using an existing machine credentials configuration file at <file>/etc/viam.json</file>.

{{< alert title="Important" color="note" >}}
Your machine must have `curl` available in order to install `viam-agent`.
{{< /alert >}}

1. The first step is to add a new machine in the [Viam app](https://app.viam.com).
2. Navigate to the **CONFIGURE** tab and find your machine's card.
   An alert will be present directing you to **Set up your machine part**:

<p>
{{<imgproc src="/installation/setup-part.png" resize="800x" declaredimensions=true alt="Machine setup alert in a newly created machine" class="imgzoom aligncenter">}}
</p>

Click **View setup instructions** to open the setup instructions.
Then navigate to the machine part's setup and follow the instructions to install `viam server` with `viam-agent`.

The command will be of the following form:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
sudo /bin/sh -c "VIAM_API_KEY_ID=<KEYID> VIAM_API_KEY=<KEY> VIAM_PART_ID=<PARTID>; $(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
```

{{< alert title="Note" color="note" >}}

As an alternative to specifying the `VIAM_API_KEY_ID`, the `VIAM_API_KEY`, and the `VIAM_PART_ID` when running the command, you can also copy the `viam-server` app JSON configuration from the Viam app into <file>/etc/viam.json</file>.
You can get the machine cloud credentials by clicking the copy icon next to **Machine cloud credentials** in the part status dropdown to the right of your machine's name on the top of the page.
{{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}

Then run the following command to install `viam-agent`:

```sh {class="command-line" data-prompt="$"}
sudo /bin/sh -c "$(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
```

    {{< /alert >}}

`viam-agent` will install itself as a systemd service named `viam-agent`.
For information on managing the service, see [Manage `viam-agent`](/manage/reference/viam-agent/manage-viam-agent/).

## Configuration

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Agent**.

<p>
{{< imgproc src="/configure/agent.png" alt="Configuration of viam-agent" resize="1200x" style="width:600px" class="imgzoom aligncenter">}}
</p>

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON (Default)" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "agent": {
    "version_control": {
      "agent": "stable",
      "viam-server": "0.52.1"
    },
    "advanced_settings": {
      "debug": false,
      "wait_for_update_check": false,
      "viam_server_start_timeout_minutes": 10,
      "disable_viam_server": false,
      "disable_network_configuration": false,
      "disable_system_configuration": false
    },
    "network_configuration": {
      "manufacturer": "viam",
      "model": "custom",
      "fragment_id": "",
      "hotspot_prefix": "viam-setup",
      "hotspot_password": "viamsetup",
      "disable_captive_portal_redirect": false,
      "offline_before_starting_hotspot_minutes": 2,
      "user_idle_minutes": 5,
      "retry_connection_timeout_minutes": 10,
      "turn_on_hotspot_if_wifi_has_no_internet": false,
      "wifi_power_save": null
    },
    "additional_networks": {
      {
        "type": "",
        "interface": "",
        "ssid": "",
        "psk": "",
        "priority": 0,
        "ipv4_address": "",
        "ipv4_gateway": "",
        "ipv4_dns": [],
        "ipv4_route_metric": 0
      }
    },
    "system_configuration": {
      "logging_journald_system_max_use_megabytes": 512,
      "logging_journald_runtime_max_use_megabytes": 512,
      "os_auto_upgrade_type": "security"
    }
  }
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "agent": {
    "version_control": {
      "agent": "stable",
      "viam-server": "0.52.1"
    },
    "advanced_settings": {
      "debug": false,
      "wait_for_update_check": false,
      "viam_server_start_timeout_minutes": 10,
      "disable_viam_server": false,
      "disable_network_configuration": false,
      "disable_system_configuration": false
    },
    "network_configuration": {
      "manufacturer": "viam",
      "model": "custom",
      "fragment_id": "",
      "hotspot_prefix": "viam-setup",
      "hotspot_password": "viamsetup",
      "disable_captive_portal_redirect": false,
      "offline_before_starting_hotspot_minutes": 2,
      "user_idle_minutes": 5,
      "retry_connection_timeout_minutes": 10,
      "turn_on_hotspot_if_wifi_has_no_internet": false,
      "wifi_power_save": null
    },
    "additional_networks": {
      {
        "type": "wifi",
        "interface": "",
        "ssid": "fallbackNetOne",
        "psk": "myFirstPassword",
        "priority": 30,
        "ipv4_address": "",
        "ipv4_gateway": "",
        "ipv4_dns": [],
        "ipv4_route_metric": 0
      },
      {
        "type": "wifi",
        "interface": "",
        "ssid": "fallbackNetTwo",
        "psk": "mySecondPassword",
        "priority": 10,
        "ipv4_address": "",
        "ipv4_gateway": "",
        "ipv4_dns": [],
        "ipv4_route_metric": 0
      }
    },
    "system_configuration": {
      "logging_journald_system_max_use_megabytes": 128,
      "logging_journald_runtime_max_use_megabytes": 96,
      "os_auto_upgrade_type": "all"
    }
  }
}
```

{{% /tab %}}
{{< /tabs >}}

## `version_control`: Version management for `viam-agent` and `viam-server`

By default, when a new version of `viam-server` becomes available, it will automatically download.
When `viam-agent` next restarts, it installs and starts using the new version of `viam-server`.
To ensure that updates only occur when your machines are ready, configure a [maintenance window](/operate/reference/viam-server/#maintenance-window). With a configured maintenance window, `viam-agent` will restart and upgrade `viam-server` only when maintenance is allowed and when `viam-server` is not currently processing config changes.

<!-- prettier-ignore -->
| Name       | Type | Required? | Description |
| ---------- | ---- | --------- | ----------- |
| `agent` | string | true | The version of Viam agent specified as `"5.6.77"`, `"stable"` or by providing a URL such as `"http://example.com/viam-agent-test-aarch64"` or `"file://home/myuser/viam-agent-test-aarch64"`. Viam agent is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Default: `"stable"`. |
| `viam-server` | string | true | The version of `viam-server` specified as `"5.6.77"`, `"stable"` or by providing a URL such as `"http://example.com/viam-agent-test-aarch64"` or `"file://home/myuser/viam-server-test-aarch64"`. `viam-server` is semantically versioned and is tested before release. When set to `"stable"`, `viam-server` will automatically upgrade when a new stable version is released. Default: `"stable"`. |

{{< alert title="Important" color="note" >}}
`viam-agent` does not update itself.
You must [restart `viam-agent`](/manage/reference/viam-agent/manage-viam-agent/) or reboot in order to use the new version.
When you stop or restart `viam-agent`, the agent will stop or restart `viam-server` as well.

When `viam-server` updates itself, you must restart `viam-server` in order to use the new version.
You can restart `viam-server` from the machine's part status dropdown to the right of your machine’s name on its page in the Viam app.

{{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}

{{< /alert >}}

For more information on managing `viam-agent` see:

{{< cards >}}
{{% card link="/manage/reference/viam-agent/manage-viam-agent/" %}}
{{< /cards >}}

## `advanced_settings`

<!-- prettier-ignore -->
| Name       | Type | Required? | Description |
| ---------- | ---- | --------- | ----------- |
| `debug` | boolean | false | Sets the log level to debug for any logging from the Viam agent binary. Default: `false`. |
| `disable_network_configuration` | boolean | false | Disables the network and hotspot configuration, as well as the configuration of additional networks. Default: `false`. |
| `disable_system_configuration` | boolean | false | Disables the system configuration. Default: `false`. |
| `disable_viam_server` | boolean | false | Disable `viam-server` remotely. This option is often used by developers working on Viam agent or when manually running `viam-server`. Default: `false`. |
| `viam_server_start_timeout_minutes` | integer | false | Specify a time after which, if `viam-server` hasn't successfully started, Viam agent will kill it and restart. Default: `10`. |
| `wait_for_update_check` | boolean | false | If set to `true`, `viam-agent` will wait for a network connection and check for updates before starting `viam-server`. See [Reduce startup time](#reduce-startup-time). Default: `false`. |

### Reduce startup time

You can set `wait_for_update_check` to `false` to bypass `viam-agent` waiting for a network connection to be established and checking for updates during initial startup.
This will result in `viam-server` executing as quickly as possible.

This is useful if you have a device that often starts when offline or on a slow connection, and if having the latest version immediately after start isn't required.

{{< alert title="Note" color="note" >}}
Periodic update checks will continue to run afterwards.
This setting only affects the initial startup sequencing.
{{< /alert >}}

You can also start `viam-agent` in fast start mode by setting `VIAM_AGENT_FAST_START=1` in your environment.

## `network_configuration`

<!-- prettier-ignore -->
| Name       | Type | Required? | Description |
| ---------- | ---- | --------- | ----------- |
| `device_reboot_after_offline_minutes` | integer | false | If set, `viam-agent` will reboot the device after it has been offline for the specified duration. Default: `0` (disabled). |
| `disable_captive_portal_redirect` | boolean | false | By default, ALL DNS lookups using the provisioning hotspot will redirect to the device. This causes most phones/mobile devices to automatically redirect the user to the captive portal as a "sign in" screen. When disabled, only domains ending in .setup (ex: viam.setup) will be redirected. This generally avoids displaying the portal to users and is mainly used in conjunction with a mobile provisioning application workflow. Default: `false`. |
| `fragment_id` | string | false | The `fragment_id` of the fragment to configure machines with. Required when using the Viam mobile app for provisioning. The Viam mobile app uses the fragment to configure the machine. |
| `hotspot_interface` | string | false | The interface to use for hotspot/provisioning/wifi management. Default: first discovered 802.11 device. |
| `hotspot_password` | string | false | The Wifi password for the provisioning hotspot. Default: `"viamsetup"`. |
| `hotspot_prefix` | string | false | `viam-agent` will prepend this to the hostname of the device and use the resulting string for the provisioning hotspot SSID. Default: `"viam-setup"`. |
| `manufacturer` | string | false | Purely informative. May be displayed on captive portal or provisioning app. Default: `"viam"`. |
| `model` | string | false | Purely informative. May be displayed on captive portal or provisioning app. Default: `"custom"`. |
| `offline_before_starting_hotspot_minutes` | integer | false | Will only enter provisioning mode (hotspot) after being disconnected longer than this time. Useful on flaky connections, or when part of a system where the device may start quickly, but the WiFi/router may take longer to be available. Default: `2` (2 minutes). |
| `retry_connection_timeout_minutes` | integer | Optional | Provisioning mode will exit after this time, to allow other unmanaged (for example wired) or manually configured connections to be tried. Provisioning mode will restart if the connection/online status doesn't change. Default: `10` (10 minutes). |
| `turn_on_hotspot_if_wifi_has_no_internet` | boolean | false | By default, the device will only attempt to connect to a single WiFi network (the one with the highest priority), provided during initial provisioning/setup using the provisioning mobile app or captive web portal. WiFi connection alone is enough to consider the device as "online" even if the global internet is not reachable. If the primary network configured during provisioning cannot be connected to and `turn_on_hotspot_if_wifi_has_no_internet` is enabled, the device will attempt connections to all configured networks in `networks`, and only consider the device online if the internet is reachable. Default: `false`. |
| `user_idle_minutes` | integer | false | Amount of time before considering a user (using the captive web portal or provisioning app) idle, and resuming normal behavior. Used to avoid interrupting provisioning mode (for example for network tests/retries) when a user might be busy entering details. Default: `5` (5 minutes). |
| `wifi_power_save` | boolean | false | If set, will explicitly enable or disable power save for all WiFi connections managed by NetworkManager. If not set, the system default applies. Default: `false`. |

For more detailed instructions on what these settings do, see [Provisioning](https://docs.viam.com/manage/fleet/provision/setup/#configure-agent-provisioning).

## `additional_networks`

For an already-online device, you can configure new WiFi or wired networks in the machine's [`viam-agent` configuration](/manage/reference/viam-agent/#configuration) in the Viam app.
It's primarily useful for a machine that moves between different networks, so the machine can automatically connect when moved between locations.

<!-- prettier-ignore -->
| Name       | Type | Required? | Description |
| ---------- | ---- | --------- | ----------- |
| `interface` | string | optional | Name of interface, for example: `"wlan0"`, `"eth0"`, `"enp14s0"`. Default: `""`. |
| `ipv4_address` | string | optional | IPv4 address in CIDR format, for example: `"192.168.0.1/24"`. Default: `"auto"`. |
| `ipv4_dns` | string | optional | Array of IPv4 DNS such as `["192.168.0.254", "8.8.8.8"]`. Default: `[]`. |
| `ipv4_gateway` | string | optional | IPv4 gateway. Default: `""`. |
| `ipv4_route_metric` | integer | optional | IPv4 route metric. Lower values are preferred. Default: `0` which defaults to `100` for wired networks and `600` for wireless network. |
| `priority` | integer | optional | Priority to choose the network with. Values between -999 and 999 with higher values taking precedence. Default: `0`. |
| `psk` | string | optional | The network passkey. Default: `""`. |
| `ssid` | string | optional | The WiFi network's SSID. Only needed for WiFi networks. Default: `""`. |
| `type` | string | optional | The type of the network. Required if a network is provided. Options: `"wifi"`, `"wired"`. |

To add additional networks add them using the JSON editor for your device's config in the Viam app.

{{< alert title="Important" color="note" >}}
You must enable `turn_on_hotspot_if_wifi_has_no_internet` in the [`agent-provisioning` configuration](#configuration) to allow the machine to connect to the specified networks.
Note that if you are using the Viam app to add networks to a machine's configuration, the machine will need to be connected to the internet to retrieve the configuration information containing the network credentials before it can use them.
{{< /alert >}}

If `turn_on_hotspot_if_wifi_has_no_internet` is enabled, `agent-provisioning` will try to connect to each specified network in order of `priority` from highest to lowest.
If the highest-priority network is not available or the machine can connect but internet is not available, `viam-agent` will then attempt to connect to the next-highest network, and so on until all configured networks have been tried.

## `system-configuration`

<!-- prettier-ignore -->
| Name       | Type | Required? | Description |
| ---------- | ---- | --------- | ----------- |
| `logging_journald_runtime_max_use_megabytes` | integer | optional |Set the temporary space limit for logs. `-1` to disable. Default: `512` (512 MB). |
| `logging_journald_system_max_use_megabytes` | integer | optional | Sets the maximum disk space `journald` will use for persistent log storage. `-1` to disable. Default: `512` (512 MB). |
| `os_auto_upgrade_type` | boolean | optional | Manage OS package updates using Viam by setting this field. Installs the `unattended-upgrades` package, and replace `20auto-upgrades` and `50unattended-upgrades` in <FILE>/etc/apt/apt.conf.d/</FILE>, with an automatically generated Origins-Pattern list that is generated based on that of `50unattended-upgrades`. Custom repos installed on the system at the time the setting is enabled will be included. Options: `"all"` (automatic upgrades are performed for all packages), `"security"` (automatic upgrades for only packages containing `"security"` in their codename (for example `bookworm-security`)), `"disable"` (disable automatic upgrades), `""` (do not change system settings). Default: `""`. |

For more detailed instructions, see [Configure machine settings](https://docs.viam.com/manage/fleet/system-settings/).

## Agent logs

`viam-agent` writes log messages to the [Viam app](https://app.viam.com/).
You can find these messages on the [**LOGS** tab](/manage/troubleshoot/troubleshoot/#check-logs) of your machine's page.

`viam-agent` only sends messages when your machine is online and connected to the internet.
If your machine is offline, log messages are queued and are sent to the Viam app once your machine reconnects to the internet.

These log messages include when `viam-server` is stopped and started, the status of `viam-agent`, and any errors or warnings encountered during operation.
