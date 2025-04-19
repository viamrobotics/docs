---
title: "Manage Micro-RDK"
linkTitle: "Manage Micro-RDK"
weight: 100
no_list: true
type: docs
tags: ["modular resources", "components", "services", "registry"]
description: "Manage your Micro-RDK-based firmware."
date: "2025-04-18"
---

## Micro-RDK CLI

The Viam Micro-RDK installer is a command line tool that you can also use to troubleshoot.
It allows you to:

- View logs locally and debug issues when your device has not connected to the Viam app
- Change wifi credentials on your microcontroller
- Overwrite firmware using a serial cable

{{< tabs >}}
{{% tab name="Download the latest release" %}}

Download the latest release of the installer for your architecture:

- [x86_64-Linux](https://github.com/viamrobotics/micro-rdk/releases/latest/download/micro-rdk-installer-amd64-linux)
- [aarch64-Linux](https://github.com/viamrobotics/micro-rdk/releases/latest/download/micro-rdk-installer-arm64-linux)
- [MacOS](https://github.com/viamrobotics/micro-rdk/releases/latest/download/micro-rdk-installer-macos)
- [Windows](https://github.com/viamrobotics/micro-rdk/releases/latest/download/micro-rdk-installer-windows.exe)

{{% /tab %}}
{{% tab name="Build from source" %}}

You can also build the `micro-rdk-installer` CLI from [source](https://github.com/viamrobotics/micro-rdk/tree/main/micro-rdk-installer):

1. Clone the repository:

   ```bash
   git clone https://github.com/viamrobotics/micro-rdk.git
   ```

1. Change directories into the repository:

   ```bash
   cd micro-rdk/micro-rdk-installer
   ```

1. Build the CLI:

   ```bash
   cargo build
   ```

1. The executable will be at <file>target/debug/micro-rdk-installer</file>.

{{% /tab %}}
{{< /tabs >}}

### Usage

The following commands are available:

<!-- prettier-ignore -->
| Command | Description |
| ------- | ----------- |
| `write-flash` | Flash a pre-compiled binary (`viam-micro-server`) directly to an ESP32 connected to your computer with a data cable. |
| `write-credentials` | Write Wi-Fi and machine credentials to the NVS storage partition of an ESP32 running `viam-micro-server`. |
| `create-nvs-partition` | Generate a binary of a complete NVS data partition that contains Wi-Fi and security credentials for a machine. |
| `monitor` | Monitor an ESP32 currently connected to your computer with a data cable. |
| `help` | Print this list of commands or the help for a specific command. |

#### Command options

| Option         | Description                       |
| -------------- | --------------------------------- |
| `-h`, `--help` | Print help for a specific command |

#### Command examples

The following command examples use the `micro-rdk-installer-macos` executable.
Change the executable to the appropriate one for your architecture.

```bash
# Flash a pre-compiled binary to an ESP32 using app config credentials downloaded from the Viam app setup tab
./micro-rdk-installer-macos write-flash --app-config=~/Downloads/my-microcontroller-main.json

# Monitor an ESP32 currently connected to your computer with a data cable
./micro-rdk-installer-macos monitor

# Get help for a specific command
./micro-rdk-installer-macos create-nvs-partition --help
```

## Over-the-air updates

{{% hiddencontent %}}
Over-the-air updates are available for `viam-server` and the Micro-RDK. For information about `viam-server` see [Deploy software packages to machines](/manage/software/deploy-software/).
The following information covers the Micro-RDK.
{{% /hiddencontent %}}

To remotely update the firmware on your microcontroller without a physical connection to the device, add the OTA (over-the-air) service to your microcontroller's configuration in the [Viam app](https://app.viam.com).
Use **JSON** mode to add the service as in the template below, then configure the URL from which to fetch new firmware, and the version name.

The firmware hosting endpoint must use HTTP/2.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers" data-line="3-10"}
{
  "services": [
    {
      "name": "OTA",
      "api": "rdk:service:generic",
      "model": "rdk:builtin:ota_service",
      "attributes": {
        "url": "<URL where firmware is stored in cloud storage>",
        "version": "<version name>"
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "name": "OTA",
      "api": "rdk:service:generic",
      "model": "rdk:builtin:ota_service",
      "attributes": {
        "url": "https://storage.googleapis.com/jordanna/micro-rdk-server-esp32-ota.bin",
        "version": "myVersion1"
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

Your device checks for configuration updates periodically.
If the device receives a configuration with the OTA service and a modified `version` field in it, the device downloads the new firmware to an inactive partition and restarts.
When the device boots it loads the new firmware.

{{% alert title="Note" color="note" %}}
There is no way to roll back to previous firmware after a bad upgrade without reflashing the device with a physical connection, so test your firmware thoroughly before deploying it to a fleet.
{{% /alert %}}

{{% alert title="Tip" color="tip" %}}
To update the firmware version for a group of microcontrollers at the same time, you can [create a fragment](/manage/software/deploy-software/) with the OTA service configuration and apply it to multiple machines.
Then, whenever you update the `version` field in the fragment, the version will be updated for each machine that has that fragment in its config, triggering a firmware update the next time the devices fetch their configs.
{{% /alert %}}
