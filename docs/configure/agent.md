---
title: "viam-agent"
linkTitle: "viam-agent"
weight: 50
no_list: true
type: docs
description: "The viam-agent is a self-updating service manager that maintains the lifecycle for Viam's system services, among them viam-server and provisioning."
# SMEs: James, Ale
---

The [`viam-agent`](https://github.com/viamrobotics/agent) is a self-updating service manager that maintains the lifecycle for the following system services:

- `viam-agent`: the main agent program itself
- `viam-server`: the core of the machine
- [`agent-provisioning`](/fleet/provision/): device provisioning subsystem that can set up WiFi and machine configs.
- [`agent-syscfg`](https://github.com/viamrobotics/agent-syscfg): provides various operating system and system configuration tweaks

Among other things, `viam-agent`:

- Installs `viam-server` as a static binary, removing the need to perform any library linking or dependency installation during first-time setup.
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
`viam-agent` supports the Linux `x86_64` and `aarch64` architectures only.
Your machine must have `curl` available in order to install `viam-agent`.
{{< /alert >}}

{{< tabs >}}
{{% tab name="Automatic install using a part ID" %}}

Follow the instructions on the machine part's **CONNECT** tab to install with Viam Agent.
The command will be of the following form:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
sudo /bin/sh -c "VIAM_API_KEY_ID=<KEYID> VIAM_API_KEY=<KEY> VIAM_PART_ID=<PARTID>; $(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
```

This command will obtain the machine config and store it in <FILE>/etc/viam.json</FILE> using the API key and part ID.

{{% /tab %}}
{{% tab name="Manual install using a configuration file" %}}

If you want to install `viam-agent` on a machine that you have not yet created in the Viam app, follow these steps:

1. Create a configuration file with the desired configuration for your machine. You can:

   - [create a new machine in the Viam app](/cloud/machines/#add-a-new-machine) and configure it as desired or use an existing deployed machine, then switch to **Builder** mode and copy the configuration shown into a new file on your machine.
   - base your configuration on the [example configuration file](/internals/local-configuration-file/#example-json-configuration-file), and adjust as needed.

1. Place the configuration into a file called <file>viam.json</file> in the <file>/etc/</file> folder on the machine you wish to install `viam-agent` to: <file>/etc/viam.json</file>.

1. Run the following command to install `viam-agent` on your machine:

   ```sh {class="command-line" data-prompt="$"}
   sudo /bin/sh -c "$(curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-agent/install.sh)"
   ```

{{% /tab %}}
{{< /tabs >}}

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
      "pin_url": "",
      "disable_subsystem": false
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
      "release_channel": "stable",
      "pin_version": "1.2.3",
      "pin_url": "http://example/test.binary",
      "disable_subsystem": false
    },
    "viam-server": {
      "attributes": {
        "fast_start": true
      }
    },
    "agent-provisioning": {
      "release_channel": "stable",
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
      ],
      "attributes": {
        "hotspot_password": "acme123"
      }
    },
    "agent-syscfg": {
      "release_channel": "stable"
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
| `release_channel` | string | Optional | `viam-agent` is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Options: `"stable"` (default), `"??"`. |
| `pin_version` | string | Optional | "Lock" the subsystem to a specific version (as provided by the release channel). If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `pin_url` | string | Optional | "Lock" the subsystem to a specific binary. If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). Typically this is only used for testing/troubleshooting. If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `disable_subsystem` | boolean | Optional | When set to `true` it disables `viam-agent` subsystem. |

### `viam-server`

<!-- prettier-ignore -->
| Option | Type | Required? | Description |
| ------ | ---- | --------- | ----------- |
| `attributes` | object | Optional | <ul><li>`fast_start`: If set to `true`, `viam-agent` will not wait a network connection and check for updates before starting `viam-server`. See [Fast start mode](#fast-start-mode).</li></ul> |
| `release_channel` | string | Optional | `viam-agent` is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Options: `"stable"` (default), `"??"`. |
| `pin_version` | string | Optional | "Lock" the subsystem to a specific version (as provided by the release channel). If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `pin_url` | string | Optional | "Lock" the subsystem to a specific binary. If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). Typically this is only used for testing/troubleshooting. If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `disable_subsystem` | boolean | Optional | When set to `true` it disables the `viam-server` subsystem. |

#### Fast start mode

You can use fast start mode to bypass `viam-agent` waiting for a network connection to be established and checking for updates during initial startup.
This will result in `viam-server` executing as quickly as possible.

This is useful if you have a device that often starts when offline or on a slow connection, and if having the latest version immediately after start isn't required.

{{< alert title="Note" color="note" >}}
Period update checks will continue to run afterwards.
The fast start mode only affects the initial startup sequencing.
{{< /alert >}}

You can also start `viam-agent` in fast start mode by setting `VIAM_AGENT_FASTSTART=1` in your environment.

### `agent-provisioning`

<!-- prettier-ignore -->
| Option | Type | Required? | Description |
| ------ | ---- | --------- | ----------- |
| `networks` | array | Optional | Networks a machine can automatically connect to when roaming mode is enabled in the [`agent-provision`](/fleet/provision/#configuration) and either no primary network was configured by the end user in the provisioning app or the primary network cannot be connected to. See [#networks]. |
| `attributes` | object | Optional | <ul><li>`hotspot_password`: Set a password for the WiFi hotspot a machine creates during provisioning.</li></ul> |
| `release_channel` | string | Optional | `viam-agent` is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Options: `"stable"` (default), `"??"`. |
| `pin_version` | string | Optional | "Lock" the subsystem to a specific version (as provided by the release channel). If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `pin_url` | string | Optional | "Lock" the subsystem to a specific binary. If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). Typically this is only used for testing/troubleshooting. If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `disable_subsystem` | boolean | Optional | When set to `true` it disables the `agent-provisioning` subsystem. |

#### Networks

During the provisioning process, a machine connects to a network to install `viam-server`.
If an end user uses an app to provision the machine, they will generally provide network details through that app.

However, if you know the networks provisioned machines will be able to use prior to installing `viam-agent`, add them to the machine's [`viam-agent` configuration](/configure/agent/#configuration) or to the fragment you use for provisioning.
To add additional networks to an already-online device, add them using the JSON editor for your device's config in the Viam app.

{{< alert title="Important" color="note" >}}
You must enable `roaming_mode` in the [`agent-provisioning` configuration](#configuration) to use roaming mode.
Additionally, the end user must either **not** provide a primary network or there must be an issue with the connection to the primary network, for `agent-provisioning` to enter roaming mode.
`agent-provisioning` will enter roaming mode only when `roaming_mode` is enabled and no connection can be established to a primary network.
{{< /alert >}}

If configured, `agent-provisioning` will try to connect to each specified network in order of `priority` from highest to lowest.
If the highest-priority network is not available or the machine can connect but internet is not available, `viam-agent` will then attempt to connect to the next-highest network, and so on until all configured networks have been tried.
If the machine cannot connect to any network that has internet, it will then enter hotspot mode.
For more information see [Provisioning](/fleet/provision/#how-an-end-user-would-use-it).

<!-- prettier-ignore -->
| Name       | Type   | Description |
| ---------- | ------ | ----------- |
| `type`     | string | The type of the network. Options: `"wifi"`|
| `ssid`     | string | The network's SSID. |
| `psk`      | string | The network pass key. |
| `priority` | int    | Priority to choose the network with. Values between -999 and 100. Default: `0`. |

The following configuration defines the connection information and credentials for two WiFi networks named `fallbackNetOne` and `fallbackNetTwo`:

```json {class="line-numbers linkable-line-numbers"}
...
"agent": {
  "agent-provisioning": {
    ...
    "attributes": {
      ...
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
| `release_channel` | string | Optional | `viam-agent` is semantically versioned and is tested before release. Releases happen infrequently. When set to `"stable"`, `viam-agent` will automatically upgrade when a new version is released. Options: `"stable"` (default), `"??"`. |
| `pin_version` | string | Optional | "Lock" the subsystem to a specific version (as provided by the release channel). If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `pin_url` | string | Optional | "Lock" the subsystem to a specific binary. If set, no automatic upgrades will be performed until the setting is updated to a new version (or removed to revert to the release channel). Typically this is only used for testing/troubleshooting. If both `pin_url` and `pin_version` is set, `pin_url` will be used. Default: `""`. |
| `disable_subsystem` | boolean | Optional | When set to `true` it disables the `agent-syscfg` subsystem. |

## Version management for `viam-agent` and `viam-server`

`viam-agent` automatically updates both itself and `viam-server` as new updates are released.
You can configure update behavior for the Agent and `viam-server` using the [Viam app](https://app.viam.com/).

{{< alert title="Important" color="note" >}}
When `viam-agent` updates either itself or `viam-server`, you must [restart these system services](/installation/manage-viam-agent/) in order to use the new version.
When you stop or restart `viam-agent`, the agent will stop or restart `viam-server` as well.
{{< /alert >}}

To use a specific version of `viam-agent` and `viam-server`, you can pin the version.

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

To see how to provision machines using `viam-agent`, see

{{< cards >}}
{{% card link="/fleet/provision/" %}}
{{< /cards >}}
