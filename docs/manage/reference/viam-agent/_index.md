---
title: "viam-agent"
linkTitle: "viam-agent"
weight: 20
no_list: true
type: docs
description: "The viam-agent is a self-updating service manager that maintains the lifecycle for Viam's system services, among them viam-server and provisioning."
date: "2025-02-14"
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
- Allows control of deployed software versions.
- Provides various operating system settings.

{{< alert title="Support notice" color="note" >}}
Currently, `viam-agent` is only supported on Linux for amd64 (x86_64) and arm64 (aarch64) CPUs and Windows (native).
{{< /alert >}}

To provision machines using `viam-agent`, see [Provision Machines](/manage/fleet/provision/setup/).

## Installation

{{< table >}}
{{% tablestep number=1 %}}
Add a new machine.
{{% /tablestep %}}
{{% tablestep number=2 %}}
Navigate to the machine's **CONFIGURE** tab.
{{% /tablestep %}}
{{% tablestep number=3 %}}
Click **View setup instructions** on the alert to **Set up your machine part**:

{{<imgproc src="/installation/setup.png" resize="400x" declaredimensions=true alt="Machine setup alert in a newly created machine" class="shadow imgzoom">}}
{{% /tablestep %}}
{{% tablestep number=4 %}}
Follow the instructions to install `viam server` with `viam-agent`.
Your machine must have `curl` available in order to install `viam-agent`.

{{< tabs >}}
{{% tab name="Linux" %}}

You can use `viam-agent` either with

{{< tabs >}}
{{% tab name="environment variables" %}}

The command will be of the following form:

```sh {class="command-line" data-prompt="$" data-output=""}
sudo /bin/sh -c "VIAM_API_KEY_ID=<KEYID> VIAM_API_KEY=<KEY> VIAM_PART_ID=<PARTID>; $(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
```

{{% /tab %}}
{{% tab name="a machine credentials file" %}}

```sh {class="command-line" data-prompt="$"}
sudo /bin/sh -c "$(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
```

The machine credentials file must be at <file>/etc/viam.json</file>.
You can get the machine cloud credentials by clicking the copy icon next to **Machine cloud credentials** in the part status dropdown to the right of your machine's name on the top of the page.

{{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Machine part info dropdown" class="shadow">}}

{{% /tab %}}
{{< /tabs >}}

On Linux, `viam-agent` will install itself as a systemd service named `viam-agent`.
For information on managing the service, see [Manage `viam-agent`](/manage/reference/viam-agent/manage-viam-agent/).

{{% /tab %}}
{{% tab name="Windows" %}}

On Windows, the [`viam-agent` installer](https://storage.googleapis.com/packages.viam.com/apps/viam-agent/viam-agent-windows-installer.exe) installs `viam-agent` as a service.
Your machine credentials file must be at <file>\etc\viam.json</file>.

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{< /table >}}

## Configuration

{{< tabs >}}
{{% tab name="Config Builder" %}}

1. Navigate to your machine's page.
1. Navigate to the **CONFIGURE** tab.
1. Click on **machine settings**.
1. Edit and fill in the attributes as applicable.

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
      "viam_server_env": {
        "CUSTOM_VAR": "value"
      }
    },
    "network_configuration": {
      "manufacturer": "viam",
      "model": "custom",
      "fragment_id": "",
      "hotspot_interface": "wlan0",
      "hotspot_prefix": "viam-setup",
      "hotspot_password": "viamsetup",
      "disable_captive_portal_redirect": false,
      "offline_before_starting_hotspot_minutes": 2,
      "user_idle_minutes": 5,
      "retry_connection_timeout_minutes": 10,
      "turn_on_hotspot_if_wifi_has_no_internet": true,
      "wifi_power_save": null
    },
    "additional_networks": {
      "network1": {
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
      "network2": {
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
      "os_auto_upgrade_type": "all",
      "forward_system_logs": "all,-gdm,-tailscaled"
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

{{< alert title="Tip: Check versions of viam-agent and viam-server" color="tip" >}}

You can find the installed versions of viam-agent and viam-server on your machine's page. Click on the part status dropdown to the right of your machine's name on the top of the page.

{{< /alert >}}

<!-- prettier-ignore -->
| Name       | Type | Required? | Description |
| ---------- | ---- | --------- | ----------- |
| `agent` | string | **Required** | The version of Viam agent specified as either:<ul><li>a version number`"5.6.77"` or `"0.65.1-dev.7"` (indicating the seventh commit to "main" after the previous non-dev release, `0.65.0`)</li><li>a tag such as`"stable"` or `"dev"`.</li><li>a URL such as `"http://example.com/viam-agent-test-aarch64"`, `"file:///home/myuser/viam-agent-test-aarch64"`, or `"file:///C:/Users/viam/Downloads/viam-agent-v0.31.0-windows-x86_64.exe"`</li></ul> Viam agent is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Default: `"stable"`. |
| `viam-server` | string | **Required** | The version of `viam-server` specified as `"5.6.77"`, `"stable"`, `"dev"` or by providing a URL such as `"http://example.com/viam-server-test-aarch64"`, `"file:///home/myuser/viam-server-test-aarch64"`, or `"file:///C:/Users/viam/Downloads/viam-server-v0.72.0-windows-x86_64.exe"`. `viam-server` is semantically versioned and is tested before release. When set to `"stable"`, `viam-server` will automatically upgrade when a new stable version is released. Default: `"stable"`. |

For more information on managing `viam-agent` see [Manage `viam-agent`](/manage/reference/viam-agent/manage-viam-agent/).

### Update or downgrade `viam-server` with `viam-agent`

{{< alert title="Tip" color="tip" >}}
The current version of `viam-server` is displayed in the machine's part status dropdown to the right of your machine’s name on its page.
{{< /alert >}}

{{% hiddencontent %}}
`viam-server` is made from the RDK. Therefore the version of RDK and `viam-server` installed on a machine is always the same.

To check the version of `viam-server` (or the RDK) check the machine part status dropdown.
To update the version of `viam-server` (or the RDK) update the machine settings.
{{% /hiddencontent %}}

1. Navigate to your machine's **CONFIGURE** tab.
2. Click on **machine settings** on the left side of the page.
3. Change the specified `viam-server` version.
4. Save your configuration.

## `advanced_settings`

<!-- prettier-ignore -->
| Name       | Type | Required? | Description |
| ---------- | ---- | --------- | ----------- |
| `debug` | boolean | Optional | Sets the log level to debug for any logging from the Viam agent binary. Default: `false`. |
| `disable_network_configuration` | boolean | Optional | Disables the network and hotspot configuration, as well as the configuration of additional networks. Default: `false`. |
| `disable_system_configuration` | boolean | Optional | Disables the system configuration. Default: `false`. |
| `disable_viam_server` | boolean | Optional | Disable `viam-server` remotely. This option is often used by developers working on Viam agent or when manually running `viam-server`. Default: `false`. |
| `viam_server_env` | object | Optional | A map of environment variable names to values that `viam-agent` passes to `viam-server` and its child processes (including modules). Both keys and values must be strings. See [Environment Variables for viam-server](#environment-variables-for-viam-server). Default: `{}` (empty). |
| `viam_server_start_timeout_minutes` | integer | Optional | Specify a time after which, if `viam-server` hasn't successfully started, Viam agent will kill it and restart. Default: `10`. |
| `wait_for_update_check` | boolean | Optional | If set to `true`, `viam-agent` will wait for a network connection and check for updates before starting `viam-server`. See [Reduce startup time](#reduce-startup-time). Default: `false`. |

### Environment Variables for viam-server

You can configure environment variables for `viam-server` using the `viam_server_env` setting in `advanced_settings`.
Environment variables set through `viam_server_env` are passed to `viam-server` and all child processes it launches, including modules.
`viam-server` also inherits existing environment variables from `viam-agent`, such as `HOME`, `PWD`, `TERM`, `PATH`.

{{< alert title="Important" color="note" >}}
When you change environment variables in `viam_server_env`, `viam-agent` will automatically restart `viam-server` to apply these and any other changes made before saving.
This restart will occur immediately if `viam-server` is in a maintenance window and not currently processing configuration changes.
{{< /alert >}}

Changes to `viam_server_env` are the only changes that automatically trigger a `viam-server` restart. Changing other configuration options requires a manual restart unless you've also changed `viam_server_env`.

#### Example configurations

```json
{
  "agent": {
    "advanced_settings": {
      "viam_server_env": {
        "PION_LOG_TRACE": "all", # Debug logging for WebRTC
        "HTTPS_PROXY": "socks5://proxy.example.com:1080", # SOCKS proxy
        "HTTP_PROXY": "socks5://proxy.example.com:1080",
        "CUSTOM_VAR": "value"
      }
    }
  }
}
```

To remove an environment variable, remove it from the `viam_server_env` object and save your configuration.

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
| `device_reboot_after_offline_minutes` | integer | Optional | If set, `viam-agent` will reboot the device after it has been offline for the specified duration. Default: `0` (disabled). |
| `disable_captive_portal_redirect` | boolean | Optional | By default, ALL DNS lookups using the provisioning hotspot will redirect to the device. This causes most phones/mobile devices to automatically redirect the user to the {{< glossary_tooltip term_id="captive-web-portal" text="captive portal" >}} as a "sign in" screen. When disabled, only domains ending in .setup (ex: viam.setup) will be redirected. This generally avoids displaying the portal to users and is mainly used in conjunction with a mobile provisioning application workflow. Default: `false`. |
| `fragment_id` | string | Optional | The `fragment_id` of the fragment to configure machines with. Required when using the Viam mobile app for provisioning. The Viam mobile app uses the fragment to configure the machine. |
| `hotspot_interface` | string | Optional | The interface to use for hotspot/provisioning/wifi management. Example: `"wlan0"`. Default: first discovered 802.11 device. |
| `hotspot_password` | string | Optional | The Wifi password for the provisioning hotspot. Default: `"viamsetup"`. |
| `hotspot_prefix` | string | Optional | `viam-agent` will prepend this to the hostname of the device and use the resulting string for the provisioning hotspot SSID. Default: `"viam-setup"`. |
| `manufacturer` | string | Optional | Purely informative. May be displayed on captive portal or provisioning app. Default: `"viam"`. |
| `model` | string | Optional | Purely informative. May be displayed on captive portal or provisioning app. Default: `"custom"`. |
| `offline_before_starting_hotspot_minutes` | integer | Optional | Amount of time the device will spend offline, in minutes, before the machine begins broadcasting a wireless hotspot. Default: `2`. |
| `retry_connection_timeout_minutes` | integer | Optional | Provisioning mode will exit after this time (in minutes), to allow other unmanaged (for example wired) or manually configured connections to be tried. Provisioning mode will restart if the connection/online status doesn't change. Default: `10`. |
| `turn_on_hotspot_if_wifi_has_no_internet` | boolean | Optional | When enabled, Wi-Fi connections without Internet access are considered offline. After `offline_before_starting_hotspot_minutes` minutes offline, your device will begin broadcasting a hotspot. This setting must be enabled for your device to attempt connecting to `additional_networks`. Default: `false`. |
| `user_idle_minutes` | integer | Optional | Amount of time before considering a user (using the captive web portal or provisioning app) idle, and resuming normal behavior. Used to avoid interrupting provisioning mode (for example for network tests/retries) when a user might be busy entering details. Default: `5` (5 minutes). |
| `wifi_power_save` | boolean | Optional | If set, will explicitly enable or disable power save for all WiFi connections managed by NetworkManager. If not set, the system default applies. Default: `false`. |

For more detailed instructions on what these settings do, see [Provisioning](/manage/fleet/provision/setup/#configure-defaults).

## `additional_networks`

For an already-online device, you can configure new WiFi or wired networks in the machine's [`viam-agent` configuration](/manage/reference/viam-agent/#configuration).
It's primarily useful for a machine that moves between different networks, so the machine can automatically connect when moved between locations.

<!-- prettier-ignore -->
| Name       | Type | Required? | Description | Available with the Micro-RDK |
| ---------- | ---- | --------- | ----------- | ---------------------------- |
| `interface` | string | Optional | Name of interface, for example: `"wlan0"`, `"eth0"`, `"enp14s0"`. Default: `""`. | |
| `ipv4_address` | string | Optional | IPv4 address in CIDR format, for example: `"192.168.0.1/24"`. Default: `"auto"`. | |
| `ipv4_dns` | string | Optional | Array of IPv4 DNS such as `["192.168.0.254", "8.8.8.8"]`. Default: `[]`. | |
| `ipv4_gateway` | string | Optional | IPv4 gateway. Default: `""`. | |
| `ipv4_route_metric` | integer | Optional | IPv4 route metric. Lower values are preferred. Default: `0` which defaults to `100` for wired networks and `600` for wireless network. | |
| `priority` | integer | Optional | Priority to choose the network with. Values between -999 and 999 with higher values taking precedence. Default: `0`. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `psk` | string | Optional | The network passkey. Default: `""`. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `ssid` | string | Optional | The WiFi network's SSID. Only needed for WiFi networks. Default: `""`. | <p class="center-text"><i class="fas fa-check" title="yes"></i></p> |
| `type` | string | Optional | The type of the network. Required if a network is provided. Options: `"wifi"`, `"wired"`. | |

To add additional networks add them using the JSON editor for your device's config.

{{< alert title="Important" color="note" >}}
Note that if you are adding networks to a machine's configuration, the machine will need to be connected to the internet to retrieve the configuration information containing the network credentials before it can use them.
{{< /alert >}}

During provisioning, `viam-agent` will try to connect to each specified network in order of `priority` from highest to lowest.
If the highest-priority network is not available (or, if `turn_on_hotspot_if_wifi_has_no_internet` is enabled, the machine can connect but internet is not available), `viam-agent` will then attempt to connect to the next-highest network, and so on until all configured networks have been tried.

## `system-configuration`

<!-- prettier-ignore -->
| Name       | Type | Required? | Description |
| ---------- | ---- | --------- | ----------- |
| `forward_system_logs` | string | Optional | Enable forwarding of system logs (journald) to the cloud. A comma-separated list of SYSLOG_IDENTIFIERs to include, optionally prefixed with "-" to exclude. "all" is a special keyword to log everything. Examples: `"kernel,tailscaled,NetworkManager"` or `"all,-gdm,-tailscaled"`. Default: `""` (disabled). |
| `logging_journald_runtime_max_use_megabytes` | integer | Optional |Set the temporary space limit for logs. `-1` to disable. Default: `512` (512 MB). |
| `logging_journald_system_max_use_megabytes` | integer | Optional | Sets the maximum disk space `journald` will use for persistent log storage. `-1` to disable. Default: `512` (512 MB). |
| `os_auto_upgrade_type` | boolean | Optional | Manage OS package updates using Viam by setting this field. Installs the `unattended-upgrades` package, and replace `20auto-upgrades` and `50unattended-upgrades` in <FILE>/etc/apt/apt.conf.d/</FILE>, with an automatically generated Origins-Pattern list that is generated based on that of `50unattended-upgrades`. Custom repos installed on the system at the time the setting is enabled will be included. Options: `"all"` (automatic upgrades are performed for all packages), `"security"` (automatic upgrades for only packages containing `"security"` in their codename (for example `bookworm-security`)), `"disable"` (disable automatic upgrades), `""` (do not change system settings). Default: `""`. |

For more detailed instructions, see [Configure machine settings](https://docs.viam.com/manage/fleet/system-settings/).

## Agent logs

These log messages include `viam-server` stops and starts, the status of `viam-agent`, and any errors or warnings encountered during operation.

{{< tabs >}}
{{% tab name="App UI" %}}

`viam-agent` writes log messages to Viam.

`viam-agent` only sends messages when your machine is online and connected to the internet.
If your machine is offline, log messages are queued and are sent to Viam once your machine reconnects to the internet.

Navigate to the **LOGS** tab of your machine's page.

Select from the **Levels** dropdown menu to filter the logs by severity level:

{{<imgproc src="/build/program/sdks/log-level-info.png" resize="600x" declaredimensions=true alt="Filtering by log level of info in the logs tab." class="shadow imgzoom">}}

{{% /tab %}}
{{% tab name="Command line on Linux" %}}

```sh {class="command-line" data-prompt="$"}
sudo journalctl --unit=viam-agent
```

{{% /tab %}}
{{% tab name="Event Viewer on Windows" %}}

Open the Windows Event Viewer (`eventvwr` from the command line).

You will find the `viam-agent` logs under **Windows Logs > Application** on the **Details** tab

{{<imgproc src="/manage/windows-logs.png" resize="1000x" class="imgzoom" style="width:600px" declaredimensions=true alt="Windows Event Viewer showing logs">}}

{{% /tab %}}
{{< /tabs >}}

## Core options

<!-- prettier-ignore -->
| Option | Description |
| ------ | ----------- |
| `-c`, `--config` | Path to machine credentials file. Default: `/etc/viam.json`. |
| `--defaults` | Path to manufacturer defaults file. Default: `/etc/viam-defaults.json` |
| `-d`, `--debug` | Enable debug logging (on agent only). Can also be set with environment variable `VIAM_AGENT_DEBUG`. |
| `-w`, `--wait` | Update versions before starting. Can also be set with environment variable `VIAM_AGENT_WAIT_FOR_UPDATE`. |
| `-h`, `--help` | Show help message. |
| `--install` | Install systemd service. |
| `--dev-mode` | Allow running as non-root and non-service. Can also be set with environment variable `VIAM_AGENT_DEVMODE`. |
