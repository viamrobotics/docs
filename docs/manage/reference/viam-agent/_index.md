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

The [`viam-agent`](https://github.com/viamrobotics/agent) is a self-updating service manager that maintains the lifecycle for itself and the following system services:

- `viam-server`: the core of the machine
- [`agent-provisioning`](#agent-provisioning): device provisioning which can set up machine configs and manage WiFi networks. For more information see [Provisioning](/manage/fleet/provision/setup/).
- [`agent-syscfg`](#agent-syscfg): provides various operating system and system configuration tweaks

Among other things, `viam-agent`:

- Installs, runs, and monitors `viam-server`
  You can also use a custom build of `viam-server`, if needed.
- Provides automatic updates for `viam-server` and the agent itself.
- Allows control of deployed software versions through the Viam app.

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
    "viam-agent": {
      "release_channel": "stable",
      "pin_version": "",
      "pin_url": ""
    },
    "viam-server": {
      "release_channel": "stable",
      "pin_version": "",
      "pin_url": "",
      "disable_subsystem": false,
      "attributes": {
        "fast_start": false
      }
    },
    "agent-provisioning": {
      "disable_subsystem": false,
      "networks": []
    },
    "agent-syscfg": {
      "disable_subsystem": false
    }
  }
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "agent": {
    "viam-agent": {
      "pin_version": "1.2.3"
    },
    "viam-server": {
      "attributes": {
        "fast_start": true
      }
    },
    "agent-provisioning": {
      "attributes": {
        "hotspot_password": "acme123",
        "networks": [
          {
            "type": "wifi",
            "ssid": "fallbackNetOne",
            "psk": "myFirstPassword",
            "priority": 30
          },
          {
            "type": "wifi",
            "ssid": "fallbackNetTwo",
            "psk": "mySecondPassword",
            "priority": 10
          }
        ]
      }
    },
    "agent-syscfg": {
      "attributes": {
        "logging": {
          "disable": false,
          "system_max_use": "128M",
          "runtime_max_use": "96M"
        },
        "upgrades": {
          "type": "all"
        }
      }
    }
  }
}
```

{{% /tab %}}
{{< /tabs >}}

### `viam-agent`

<!-- prettier-ignore -->
| Option | Type | Required? | Description |
| ------ | ---- | --------- | ----------- |
| `release_channel` | string | Optional | `viam-agent` is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Options: `"stable"` (default). |
| `pin_version` | string | Optional | Use a specific version for `viam-agent` (as provided by the release channel). If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `pin_url` | string | Optional | Ignore normal version selection and directly download from the specified URL. If set, no automatic upgrades will be performed until the setting is updated to a new URL (or removed to revert to the release channel). Typically this is only used for testing/troubleshooting. If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |

### `viam-server`

<!-- prettier-ignore -->
| Option | Type | Required? | Description |
| ------ | ---- | --------- | ----------- |
| `release_channel` | string | Optional | `viam-agent` is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Options: `"stable"` (default), `"latest"`. |
| `pin_version` | string | Optional | Use a specific version for `viam-server` (as provided by the release channel). If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `pin_url` | string | Optional | Ignore normal version selection and directly download from the specified URL. If set, no automatic upgrades will be performed until the setting is updated to a new URL (or removed to revert to the release channel). Typically this is only used for testing/troubleshooting. If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `disable_subsystem` | boolean | Optional | When set to `true` it disables the management of `viam-server`. |
| `attributes` | object | Optional | <ul><li>`fast_start`: If set to `true`, `viam-agent` will not wait for a network connection nor check for updates before starting `viam-server`. See [Fast start mode](#fast-start-mode).</li></ul> |

#### Version updates

When a new version of `viam-server` becomes available, `viam-agent` will restart and upgrade `viam-server` immediately.
To limit when `viam-server` can be updated, you can configure a [Maintenance Window](/operate/reference/viam-server/#maintenance-window).
With a configured maintenance window, `viam-agent` will restart and upgrade `viam-server` only when maintenance is allowed and when `viam-server` is not currently processing config changes.

#### Fast start mode

You can use fast start mode to bypass `viam-agent` waiting for a network connection to be established and checking for updates during initial startup.
This will result in `viam-server` executing as quickly as possible.

This is useful if you have a device that often starts when offline or on a slow connection, and if having the latest version immediately after start isn't required.

{{< alert title="Note" color="note" >}}
Period update checks will continue to run afterwards.
The fast start mode only affects the initial startup sequencing.
{{< /alert >}}

You can also start `viam-agent` in fast start mode by setting `VIAM_AGENT_FAST_START=1` in your environment.

### `agent-provisioning`

<!-- prettier-ignore -->
| Option | Type | Required? | Description |
| ------ | ---- | --------- | ----------- |
| `disable_subsystem` | boolean | Optional | When set to `true` it disables `agent-provisioning` management. |
| `attributes` | object | Optional | You can override all attributes from the [`viam-agent` configuration file](/manage/fleet/provision/setup/#configure-agent-provisioning) here. The [`viam-agent` configuration file](/manage/fleet/provision/setup/#configure-agent-provisioning) is generally customized by the manufacturer to provide "out of the box" settings. The attributes configured in the machine config in the Viam app can let you as the machine user override those if you wish. For security purposes, you should change the `hotspot_password`. You can also configure `roaming_mode` and add any additional networks you want to configure. <ul><li>`hotspot_password`: Overwrite the password set for the WiFi hotspot a machine creates during provisioning.</li><li>`networks`: Networks a machine can automatically connect to when roaming mode is enabled. See [Networks](#networks). </li><li>`roaming_mode`: If enabled, lets the machine connect to additional configured networks. See [Networks](#networks). </li><li>`wifi_power_save`: If set, will explicitly enable or disable power save for all WiFi connections managed by NetworkManager. </li></ul> |

#### Networks

For an already-online device, you can configure new WiFi networks in the machine's [`viam-agent` configuration](/manage/reference/viam-agent/#configuration) in the Viam app.
It's primarily useful for a machine that moves between different networks, so the machine can automatically connect when moved between locations.

To add additional networks add them using the JSON editor for your device's config in the Viam app.

{{< alert title="Important" color="note" >}}
You must enable `roaming_mode` in the [`agent-provisioning` configuration](#configuration) to allow the machine to connect to the specified networks.
Note that if you are using the Viam app to add networks to a machine's configuration, the machine will need to be connected to the internet to retrieve the configuration information containing the network credentials before it can use them.
{{< /alert >}}

If `roaming_mode` is enabled, `agent-provisioning` will try to connect to each specified network in order of `priority` from highest to lowest.
If the highest-priority network is not available or the machine can connect but internet is not available, `viam-agent` will then attempt to connect to the next-highest network, and so on until all configured networks have been tried.

<!-- prettier-ignore -->
| Name       | Type   | Description |
| ---------- | ------ | ----------- |
| `type`     | string | The type of the network. Options: `"wifi"`|
| `ssid`     | string | The network's SSID. |
| `psk`      | string | The network pass key. |
| `priority` | int    | Priority to choose the network with. Values between -999 and 999. Default: `0`. |

The following configuration defines the connection information and credentials for two WiFi networks named `fallbackNetOne` and `fallbackNetTwo`:

```json {class="line-numbers linkable-line-numbers"}
...
"agent": {
  "agent-provisioning": {
    ...
    "attributes": {
      ...
      "roaming_mode": true,
      "networks": [
        {
          "type": "wifi",
          "ssid": "fallbackNetOne",
          "psk": "myFirstPassword",
          "priority": 30
        },
        {
          "type": "wifi",
          "ssid": "fallbackNetTwo",
          "psk": "mySecondPassword",
          "priority": 10
        }
      ]
    }
  }
}
```

### `agent-syscfg`

`agent-syscfg` is a plugin for `viam-agent` that allows you to configure logging settings and automated upgrades for packages installed on the operating system.

<!-- prettier-ignore -->
| Option | Type | Required? | Description |
| ------ | ---- | --------- | ----------- |
| `disable_subsystem` | boolean | Optional | When set to `true` it disables `agent-syscfg`. |
| `attributes` | object | Optional | <ul><li>`logging`: parameters for logging<ul><li>`system_max_use`: sets the maximum disk space `journald` will user for persistent log storage. Numeric values are in bytes, with optional single letter suffix for larger units, for example. K, M, or G. Default: `512M`.</li><li>`runtime_max_use`: sets the runtime/temporary limit. Numeric values are in bytes, with optional single letter suffix for larger units, for example. K, M, or G. Default: `512M`.</li><li>`disable`: If `false` (default), Viam enforces the given logging configurations. If `true`: Viam does NOT modify logging configuration, and the operating system defaults are used.</li></ul></li><li>`upgrades`: using `upgrades` installs the `unattended-upgrades` package, and replace `20auto-upgrades` and `50unattended-upgrades` in <FILE>/etc/apt/apt.conf.d/</FILE>, with an automatically generated Origins-Pattern list that is generated based on that of `50unattended-upgrades`. Custom repos installed on the system at the time the setting is enabled will be included.<ul><li>`type`: Configured unattended upgrades for Debian bullseye and bookworm. Options: `""` (no effect), `"disable"` (disables automatic upgrades), `"security"` (only enables updates from sources with "security" in their codename, ex: `bookworm-security`), `"all"` (enable updates from all configured sources).</li></ul></li></ul> |

The following configuration allows all upgrades from configured sources and sets the maximum disk space `journald` will user for persistent log storage to 128MB and the runtime limit to 96MB:

```json {class="line-numbers linkable-line-numbers"}
"agent-syscfg": {
  "release_channel": "stable",
  "attributes": {
    "logging": {
      "disable": false,
      "system_max_use": "128M",
      "runtime_max_use": "96M"
    },
    "upgrades": {
      "type": "all"
    }
  }
}
```

## Version management for `viam-agent` and `viam-server`

By default, `viam-agent` automatically updates both itself and `viam-server` as new updates are released.
You can configure update behavior using the [Viam app](https://app.viam.com/).
To ensure that updates only occur when your machines are ready, configure a [maintenance window](/operate/reference/viam-server/#maintenance-window).

To use a specific version of `viam-agent` and `viam-server`, you can pin the version.

{{< alert title="Important" color="note" >}}
When `viam-agent` updates itself, you must [restart `viam-agent`](/manage/reference/viam-agent/manage-viam-agent/) or reboot in order to use the new version.
When you stop or restart `viam-agent`, the agent will stop or restart `viam-server` as well.

When `viam-server` updates itself, you must restart `viam-server` in order to use the new version.
You can restart `viam-server` from the machine's part status dropdown to the right of your machine’s name on its page in the Viam app.

{{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}

{{< /alert >}}

For more information on managing `viam-agent` see:

{{< cards >}}
{{% card link="/manage/reference/viam-agent/manage-viam-agent/" %}}
{{< /cards >}}

## Agent logs

`viam-agent` writes log messages to the [Viam app](https://app.viam.com/).
You can find these messages on the [**LOGS** tab](/manage/troubleshoot/troubleshoot/#check-logs) of your machine's page.

`viam-agent` only sends messages when your machine is online and connected to the internet.
If your machine is offline, log messages are queued and are sent to the Viam app once your machine reconnects to the internet.

These log messages include when `viam-server` is stopped and started, the status of `viam-agent`, and any errors or warnings encountered during operation.
