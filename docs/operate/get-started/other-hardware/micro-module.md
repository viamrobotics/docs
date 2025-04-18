---
title: "Create or use a Micro-RDK module"
linkTitle: "Micro-RDK modules"
type: "docs"
weight: 29
images: ["/installation/thumbnails/esp32-espressif.png"]
imageAlt: "E S P 32 - espressif"
tags: ["modular resources", "components", "services", "registry"]
description: "Set up an Espressif ESP32 microcontroller for development with the Micro-RDK including writing and using custom modules rather than using the pre-built viam-micro-server."
languages: ["rust"]
viamresources: []
platformarea: ["registry"]
level: "Intermediate"
date: "2024-12-11"
# updated: ""  # When the tutorial was last entirely checked
aliases:
  - /installation/prepare/microcontrollers/development-setup/
  - /get-started/installation/prepare/microcontrollers/development-setup/
  - /get-started/installation/microcontrollers/development-setup/
  - /get-started/installation/viam-micro-server-dev/
  - /installation/viam-micro-server-dev/
---

[The Micro-RDK](https://github.com/viamrobotics/micro-rdk/) is the lightweight version of Viam's full Robot Development Kit (RDK), designed for resource-limited embedded systems (ESP32 microcontrollers) that cannot run the fully-featured `viam-server`.
`viam-micro-server` is the pre-built firmware built from the Micro-RDK and a default set of {{< glossary_tooltip term_id="module" text="modules" >}}, provided for convenience.
If you want to use different modules on your microcontroller, you can build your own firmware with the Micro-RDK and your choice of modules using the instructions on this page.

{{< expand "Why does the Micro-RDK work differently from the full RDK?" >}}
Microcontrollers do not have full operating systems like single-board computers and general-purpose computers.
This means that microcontrollers can only run one "program" at a time, and a microcontroller must be flashed with firmware containing the entire logic to run.

The Micro-RDK is a version of the RDK library written in Rust and designed to run on microcontrollers.
The Micro-RDK includes built-in support for several common hardware components, such as standard DC motors and an ultrasonic sensor.
Viam provides a default firmware build that includes the Micro-RDK as well as two modules: a wifi sensor and a memory heap sensor.
You can use additional modules to support more or other hardware by building custom firmware from the Micro-RDK and one or more Micro-RDK-compatible modules.
{{< /expand >}}

For advanced topics including development of the Micro-RDK itself, see [Viam Micro-RDK Development on GitHub](https://github.com/viamrobotics/micro-rdk/blob/main/DEVELOPMENT.md).

## Create a new module

To create a new module compatible with the Micro-RDK, follow these steps.

1. If you have not previously developed a module for the Micro-RDK, please review the [module template README](https://github.com/viamrobotics/micro-rdk/tree/main/templates/module) and the [example module implementation walkthrough](https://github.com/viamrobotics/micro-rdk/blob/main/examples/modular-drivers/README.md) before continuing.

1. Generate a new module skeleton from [this template](https://github.com/viamrobotics/micro-rdk/tree/main/templates/module):

   ```sh { class="command-line" data-prompt="$"}
   cargo generate --git https://github.com/viamrobotics/micro-rdk.git
   ```

   Select `templates/module` when prompted, give the module a name of your choice, and answer any additional prompts.

1. Change directories into the generated tree:

   ```sh { class="command-line" data-prompt="$"}
   cd <your-path-to/your-module-directory>
   ```

1. If you wish to use version control for the module, this is the best time to initialize a git repository and commit all the generated files.
   There are no secrets in a newly generated module repository:

   ```sh { class="command-line" data-prompt="$"}
   git add .
   git commit -m "initial commit"
   ```

1. Develop the module by defining `structs` which implement the necessary `traits` and adding tests and registration hooks for them, per the walkthrough.

1. To consume the module, follow the [Build custom firmware](#build-custom-firmware) workflow in a different directory, and register your module in the `dependencies` section of the project's `Cargo.toml` file, then build and flash the project.
   The module will now be available for use by adding it to your machine configuration on the [Viam app](https://app.viam.com).

For further details on Micro-RDK development, including credentials management and developer productivity suggestions, please see the [development technical notes page on GitHub](https://github.com/viamrobotics/micro-rdk/blob/main/DEVELOPMENT.md).

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

## Troubleshooting

### Error: `xtensa-esp32-elf-gcc: error: unrecognized command line option '--target=xtensa-esp32-espidf'` when building on macOS

This is caused by an [upstream bug](https://github.com/esp-rs/esp-idf-template/issues/174).
To work around this issue, ensure that `CRATE_CC_NO_DEFAULTS=1` is set in the environment when building.

### Error: `error: externally-managed-environment` when building ESP-IDF on macOS

This is encountered when attempting to build ESP-IDF projects while using Python obtained from Homebrew.
Homebrew's Python infrastructure is not intended for end-user consumption but is instead made available to support Homebrew packages which require a python interpreter.
The preferred workaround for this issue is to obtain a user-facing python installation not from Homebrew, but there are other, less safe, workarounds.
Please see the macOS specific notes in the [development technical notes on GitHub](https://github.com/viamrobotics/micro-rdk/blob/main/DEVELOPMENT.md#fixing-esp-builds-on-macos) for more details.

### Error: Failed to open serial port

If you run into the error `Failed to open serial port` when flashing your ESP32 with Linux, make sure the user is added to the group `dialout` with `sudo gpasswd -a $USER dialout`.

### Error: `espflash::timeout`

If you get the following error while connecting to your ESP32:

```sh { class="command-line" data-prompt="$"}
`Error: espflash::timeout

  × Error while connecting to device
  ╰─▶ Timeout while running command
```

Run the following command, replacing `<YOUR_PROJECT_NAME>` with the name of your project firmware (for example, `esp32-camera`):

```sh { class="command-line" data-prompt="$"}
espflash flash --erase-parts nvs --partition-table partitions.csv  target/xtensa-esp32-espidf/release/<YOUR_PROJECT_NAME> --baud 115200 && sleep 2 && espflash monitor
```

Try the connection command again.
The baud rate on your device may not have been fast enough to connect.
If successful, the Viam app will show that your machine part's status is **Live**.

### Error: `viam.json` not found

If you get the error `viam.json not found` try the following to manually add your machine cloud credentials as a file in your project:

1. Navigate to your machine's page on the [Viam app](https://app.viam.com) and select the **CONFIGURE** tab.
1. Select the part status dropdown to the right of your machine's name on the top of the page: {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown" class="shadow" >}}
1. Click the copy icon underneath **Machine cloud credentials**.
   The Micro-RDK needs this JSON object, which contains your machine part secret key and cloud app address, to connect to the [Viam app](https://app.viam.com).
1. Navigate to the directory of the project you just created.
1. Create a new <file>viam.json</file> file and paste the machine cloud credentials from the Viam app in.
1. Save the file.

### Error: failed to run custom build command for `esp32-explorer (/host)`

This may occur for various reasons such as your machine cloud credentials, WiFi SSID, or password not being populated.
Check that your machine cloud credentials are provided in your project directory as <file>viam.json</file> and ensure that your WiFi credentials are provided.

### Error: invalid value `460800` for `--before <BEFORE>`

Change `"-b"` to `"-B` in the <file>Makefile</file>, as `"-B"` is the Baudrate config.
Run the following commands to flash <file>esp32-server.bin</file> to your ESP32 microcontroller at a high baud rate, wait for 2 seconds, and observe the device's output:

```sh {class="command-line" data-prompt="$"}
espflash write-bin 0x0 target/esp32-server.bin -B 460800  && sleep 2 && espflash monitor
```

You can find additional assistance in the [Troubleshooting section](/manage/troubleshoot/troubleshoot/).

{{< snippet "social.md" >}}
