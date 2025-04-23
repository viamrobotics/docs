---
title: "Manage Micro-RDK"
linkTitle: "Manage Micro-RDK"
weight: 100
no_list: true
type: docs
tags: ["modular resources", "components", "services", "registry"]
description: "Manage your Micro-RDK-based firmware."
date: "2025-04-18"
draft: true
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
