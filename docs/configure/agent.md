---
title: "viam-agent"
linkTitle: "viam-agent"
weight: 50
no_list: true
type: docs
description: "The viam-agent is a self-updating service manager that maintains the lifecycle for Viam's system services, among them viam-server and provisioning."
# SMEs: James, Ale
---

The [`viam-agent`](https://github.com/viamrobotics/agent) is a self-updating service manager that maintains the lifecycle for itself and the following system services:

- `viam-server`: the core of the machine
- [`agent-provisioning`](/fleet/provision/): device provisioning subsystem that can set up machine configs and manage WiFi networks.
- [`agent-syscfg`](https://github.com/viamrobotics/agent-syscfg): provides various operating system and system configuration tweaks

Among other things, `viam-agent`:

- Installs, runs, and monitors `viam-server`
  You can also use a custom build of `viam-server`, if needed.
- Provides automatic updates for `viam-server`, the agent itself, and any configured subsystems (such as the `agent-provisioning` subsystem).
- Allows control of deployed software versions through the Viam app.

{{< alert title="Support notice" color="note" >}}
Currently, `viam-agent` is only supported on Linux, for amd64 (x86_64) and arm64 (aarch64) CPUs.
{{< /alert >}}

To provision machines using `viam-agent`, see

{{< cards >}}
{{% card link="/fleet/provision/" %}}
{{< /cards >}}

## Installation

You can install `viam-agent` using either an existing machine's part ID and API key, or using an existing <file>/etc/viam.json</file> configuration file.

{{< alert title="Important" color="note" >}}
Your machine must have `curl` available in order to install `viam-agent`.
{{< /alert >}}

1.  The first step is to [create a new machine in the Viam app](/cloud/machines/#add-a-new-machine).
2.  Then navigate to the machine part's **CONNECT** tab and follow the instructions to install `viam server` with `viam-agent`.

    The command will be of the following form:

    ```sh {class="command-line" data-prompt="$" data-output="1-10"}
    sudo /bin/sh -c "VIAM_API_KEY_ID=<KEYID> VIAM_API_KEY=<KEY> VIAM_PART_ID=<PARTID>; $(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
    ```

    This command will obtain the machine config and store it in <FILE>/etc/viam.json</FILE> using the API key and part ID.

    {{< alert title="Note" color="note" >}}

As an alternative to specifying the `VIAM_API_KEY_ID`, the `VIAM_API_KEY`, and the `VIAM_PART_ID` when running the command, you can also copy the `viam-server` app JSON configuration from the Viam app into <file>/etc/viam.json</file>.
You can get the `viam-server` app JSON configuration by clicking the copy icon next to **Viam server config** in the part status dropdown to the right of your machine's name on the top of the page.
{{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}

Then run the following command to install `viam-agent`:

```sh {class="command-line" data-prompt="$"}
sudo /bin/sh -c "$(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
```

    {{< /alert >}}

`viam-agent` will install itself as a systemd service named `viam-agent`.
For information on managing the service, see [Manage `viam-agent`](/installation/manage-viam-agent/).

## Configuration

{{< tabs >}}
{{% tab name="Default" %}}

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
      "release_channel": "stable",
      "pin_version": "",
      "pin_url": "",
      "disable_subsystem": false,
      "networks": []
    },
    "agent-syscfg": {
      "release_channel": "stable",
      "pin_version": "",
      "pin_url": "",
      "disable_subsystem": false
    }
  }
}
```

{{% /tab %}}
{{% tab name="Example" %}}

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
          "disable": true,
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

Each section primarily controls updates for that subsystem:

### `viam-agent`

<!-- prettier-ignore -->
| Option | Type | Required? | Description |
| ------ | ---- | --------- | ----------- |
| `release_channel` | string | Optional | `viam-agent` is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Options: `"stable"` (default). |
| `pin_version` | string | Optional | Lock the subsystem to a specific version (as provided by the release channel). If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `pin_url` | string | Optional | Ignore normal version selection and directly download from the specified URL. If set, no automatic upgrades will be performed until the setting is updated to a new URL (or removed to revert to the release channel). Typically this is only used for testing/troubleshooting. If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |

### `viam-server`

<!-- prettier-ignore -->
| Option | Type | Required? | Description |
| ------ | ---- | --------- | ----------- |
| `attributes` | object | Optional | <ul><li>`fast_start`: If set to `true`, `viam-agent` will not wait for a network connection nor check for updates before starting `viam-server`. See [Fast start mode](#fast-start-mode).</li></ul> |
| `release_channel` | string | Optional | `viam-agent` is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Options: `"stable"` (default), `"latest"`. |
| `pin_version` | string | Optional | "Lock" the subsystem to a specific version (as provided by the release channel). If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `pin_url` | string | Optional | Ignore normal version selection and directly download from the specified URL. If set, no automatic upgrades will be performed until the setting is updated to a new URL (or removed to revert to the release channel). Typically this is only used for testing/troubleshooting. If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `disable_subsystem` | boolean | Optional | When set to `true` it disables the `viam-server` subsystem. |

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
| `attributes` | object | Optional | <ul><li>`hotspot_password`: Set a password for the WiFi hotspot a machine creates during provisioning.</li><li>`networks`: Networks a machine can automatically connect to when roaming mode is enabled in the [`agent-provision`](/fleet/provision/#configuration) and either no primary network was configured by the end user in the provisioning app or the primary network cannot be connected to. See [#networks].</li><li>`roaming_mode`: If enabled, lets the machine connect to additional configured netowrks. See [Networks](#networks).</li></ul> |
| `release_channel` | string | Optional | `agent-provisioning` is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Options: `"stable"` (default), `"latest"`. |
| `pin_version` | string | Optional | Lock the subsystem to a specific version (as provided by the release channel). If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `pin_url` | string | Optional | Ignore normal version selection and directly download from the specified URL. If set, no automatic upgrades will be performed until the setting is updated to a new URL (or removed to revert to the release channel). Typically this is only used for testing/troubleshooting. If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `disable_subsystem` | boolean | Optional | When set to `true` it disables the `agent-provisioning` subsystem. |

#### Networks

For an already-online device, you can add additional networks to the machine's [`viam-agent` configuration](/configure/agent/#configuration).
It's primarily useful for a machine that might move between different WiFi networks, so the machine can automatically connect when moved between locations.

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

<!-- prettier-ignore -->
| Option | Type | Required? | Description |
| ------ | ---- | --------- | ----------- |
| `attributes` | object | Optional | <ul><li>`logging`: parameters for logging<ul><li>`system_max_use`: sets the maximum disk space journald will user for persistent log storage. Numeric values are in bytes, with optional single letter suffix for larger units, for example. K, M, or G. Default: `512M`.</li><li>`runtime_max_use`: sets the runtime/temporary limit. Numeric values are in bytes, with optional single letter suffix for larger units, for example. K, M, or G. Default: `512M`.</li><li>`disable`: when set to `true`, the defaults for `512M` limits are ignored and the operating system defaults are used.</li></ul></li><li>`upgrades`: Using `upgrades` installs the `unattended-upgrades` package, and replace `20auto-upgrades` and `50unattended-upgrades` in <FILE>/etc/apt/apt.conf.d/</FILE>, with the latter's Origins-Pattern list being generated automatically from configured repositories on the system, so custom repos (at the time the setting is enabled) will be included.<ul><li>`type`: Configured unattended upgrades for Debian bullseye and bookworm. Options: `""` (no effect), `"disable"` (disables automatic upgrades), `"security"` (only enables updates from sources with security in their codename, ex: bookworm-security), `"all"` (enable updates from all configured sources).</li></ul></li></ul> |
| `release_channel` | string | Optional | `agent-syscfg` is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Options: `"stable"` (default), `"latest"`. |
| `pin_version` | string | Optional | "Lock" the subsystem to a specific version (as provided by the release channel). If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `pin_url` | string | Optional | Ignore normal version selection and directly download from the specified URL. If set, no automatic upgrades will be performed until the setting is updated to a new URL (or removed to revert to the release channel). Typically this is only used for testing/troubleshooting. If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `disable_subsystem` | boolean | Optional | When set to `true` it disables the `agent-syscfg` subsystem. |

## Version management for `viam-agent` and `viam-server`

`viam-agent` automatically updates both itself, its subsystems, and `viam-server` as new updates are released.
You can configure update behavior for the Agent and `viam-server` using the [Viam app](https://app.viam.com/).

To use a specific version of `viam-agent` and `viam-server`, you can pin the version.

{{< alert title="Important" color="note" >}}
When `viam-agent` updates itself, you must [restart `viam-agent`](/installation/manage-viam-agent/) or reboot in order to use the new version.
When you stop or restart `viam-agent`, the agent will stop or restart `viam-server` as well.

When `viam-server` updates itself, you must restart `viam-server` in order to use the new version.
You can restart `viam-server` from the machine's part status dropdown to the right of your machine’s name on its page in the Viam app.

{{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}

{{< /alert >}}

For more information on managing `viam-agent` see:

{{< cards >}}
{{% card link="/installation/manage-viam-agent/" %}}
{{< /cards >}}

## Agent logs

`viam-agent` writes log messages to the [Viam app](https://app.viam.com/).
You can find these messages on the [**LOGS** tab](/cloud/machines/#logs) of your machine's page.

`viam-agent` only sends messages when your machine is online and connected to the internet.
If your machine is offline, log messages are queued and are sent to the Viam app once your machine reconnects to the internet.

These log messages include when `viam-server` is stopped and started, the status of agent subsystems, and any errors or warnings encountered during operation.

## Next Steps

To see how to provision machines using `viam-agent`, see:

{{< cards >}}
{{% card link="/fleet/provision/" %}}
{{< /cards >}}
