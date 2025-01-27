---
title: "Create or use a Micro-RDK module"
linkTitle: "Micro-RDK modules"
type: "docs"
weight: 29
images: ["/installation/thumbnails/esp32-espressif.png"]
imageAlt: "E S P 32 - espressif"
tags: ["modular resources", "components", "services", "registry"]
description: "Set up the Espressif ESP32 for development with the Micro-RDK including writing and using custom modules with the Micro-RDK rather than the pre-built viam-micro-server."
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

[The Micro-RDK](https://github.com/viamrobotics/micro-rdk/) is the lightweight version of Viam's full Robot Development Kit (RDK), designed for resource-limited embedded systems (ESP32) that cannot run the fully-featured `viam-server`.
`viam-micro-server` is the pre-built firmware built from the Micro-RDK and a default set of {{< glossary_tooltip term_id="module" text="modules" >}}, provided for convenience.
If you want to use different modules with the Micro-RDK, you can build your own firmware using the instructions on this page.

{{< alert title="Looking to install viam-micro-server?" color="note" >}}
If you only want to install the pre-built `viam-micro-server` firmware with a default set of modules, follow the normal [setup instructions](/operate/get-started/setup/) instead.
{{< /alert >}}

{{< expand "Why does the Micro-RDK work differently from the full RDK?" >}}
Microcontrollers do not have full operating systems like single-board computers and general-purpose computers.
This means that microcontrollers can only run one "program" at a time, and a microcontroller must be flashed with firmware containing the entire logic to run.

The Micro-RDK is a version of the RDK library written in Rust and designed to run on microcontrollers.
The Micro-RDK includes built-in support for several common hardware components, such as standard DC motors and an ultrasonic sensor.
Viam provides a default firmware build that includes the Micro-RDK as well as two modules: a wifi sensor and a memory heap sensor.
You can use additional modules to support more or other hardware by building custom firmware from the Micro-RDK and one or more Micro-RDK-compatible modules.
{{< /expand >}}

The instructions below are for configuring a development environment in order to:

- Develop custom firmware which combines the Micro-RDK with one or more modules.
- Develop modules for the Micro-RDK.

For advanced topics including development of the Micro-RDK itself, see [Viam Micro-RDK Development on GitHub](https://github.com/viamrobotics/micro-rdk/blob/main/DEVELOPMENT.md).

## Required software

The [Micro-RDK](https://github.com/viamrobotics/micro-rdk) (from which `viam-micro-server` is built) is written in Rust.
To be able to develop for the Micro-RDK on macOS and Linux systems, you must install the following software on your development machine:

1. Install dependencies:

   {{< tabs >}}
   {{% tab name="Linux" %}}

   ```sh { class="command-line" data-prompt="$"}
   sudo apt-get install bison ccache cmake curl dfu-util flex git gperf libffi-dev libssl-dev libudev-dev libusb-1.0-0 ninja-build python3 python3-pip python3-venv wget
   ```

   {{% /tab %}}
   {{% tab name="macOS" %}}

   If you haven't already, install Homebrew:

   ```sh { class="command-line" data-prompt="$"}
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

   Then, install dependencies:

   ```sh { class="command-line" data-prompt="$"}
   brew install cmake dfu-util ninja
   ```

   {{% /tab %}}
   {{< /tabs >}}

1. If you do not yet have a Rust environment installed, install it with `rustup`.

   ```sh { class="command-line" data-prompt="$"}
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

   Once completed, start a new shell instance, or run `. "$HOME/.cargo/env"` in the current one.

   See the [Rust Installation guide](https://www.rust-lang.org/tools/install) for more information and other installation methods.

1. Install `espup` and ESP development utilities with `cargo`:

   ```sh { class="command-line" data-prompt="$"}
   cargo install cargo-espflash cargo-generate espflash espup ldproxy
   ```

1. Use `espup` to download and install the ESP Rust toolchain:

   ```sh { class="command-line" data-prompt="$"}
   espup install -s -f /dev/null -v 1.83.0
   ```

{{< alert title="Note" color="tip" >}}
Prior versions of the above `espup` instructions created a file called `export-rs.sh` which needed to be sourced before proceeding.
That requirement [no longer applies](https://github.com/esp-rs/esp-idf-hal/issues/319#issuecomment-1785168921) for Micro-RDK development.
The above command redirects `espup`'s production of the setup script to `/dev/null` to avoid cluttering the home directory.
If you would like to instead retain the setup script, replace `/dev/null` in the above command with the location where you would like the script to be written, or remove the `-f /dev/null` entirely and the file will be written to `$HOME/export-esp.sh` by default.
{{< /alert >}}

## Build custom firmware

To create firmware that integrates an existing module with the Micro-RDK, and flash your microcontroller with it, follow these steps.

1.  Create a new machine and obtain its credentials:

    Navigate to the [Viam app](https://app.viam.com) and add a new machine.
    Click on the name of the machine to go to the machine's page, then select the **CONFIGURE** tab.

    Then select the part status dropdown to the right of your machine's name on the top of the page and copy the **Machine cloud credentials**:

    {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}

    The Micro-RDK needs these credentials, which contains your machine part secret key and cloud app address, to connect to the [Viam app](https://app.viam.com).

{{% snippet "secret-share.md" %}}

2.  Generate a new project skeleton from [this template](https://github.com/viamrobotics/micro-rdk/tree/main/templates/project):

    ```sh { class="command-line" data-prompt="$"}
    cargo generate --git https://github.com/viamrobotics/micro-rdk.git
    ```

    Select `templates/project` when prompted. Give the project a name of your choice.
    Select `esp32` for **MCU**.
    If you wish to configure an `esp32-camera` or a `fake` camera as a component of your machine, select **true** for **include camera module and traits**.

    You will be prompted to paste your machine's `viam-server` robot JSON configuration into the terminal, which is the same thing as its machine cloud credentials.
    Paste in the credentials you obtained in step 1.

3.  Change directories into the generated project:

    ```sh { class="command-line" data-prompt="$"}
    cd <your-path-to/your-project-directory>
    ```

4.  If you wish to use version control for this project, this is the best time to initialize a git repository and commit all the generated files, but be sure to exclude the generated `viam.json` file, which includes secrets:

    ```sh { class="command-line" data-prompt="$"}
    git add .
    git restore viam.json
    git commit -m "initial commit"
    ```

5.  Compile the project:

    ```sh { class="command-line" data-prompt="$"}
    make build-esp32-bin
    ```

    Please note that the first build may be fairly time consuming, as ESP-IDF must be cloned and built, and all dependent Rust crates must be fetched and built as well.
    Subsequent builds will be faster.

6.  Upload the generated firmware to your ESP32:

    Connect the ESP32 board you wish to flash to a USB port on your development machine, and run:

    ```sh { class="command-line" data-prompt="$"}
    make flash-esp32-bin
    ```

    When prompted, select the serial port that your ESP32 is connected to through a data cable.

    If successful, you will retain a serial connection to the board until you press `Ctrl-C`.
    To manage this connection, consider running it within a dedicated terminal session, or under `tmux` or `screen`.
    While the serial connection is live, you can also restart the currently flashed image with `Ctrl-R`.

{{< alert title="Note" color="tip" >}}

The above build and flash steps may be combined by using the `upload` target:

```sh { class="command-line" data-prompt="$"}
make upload
```

{{< /alert >}}

7.  Navigate to your new machine's page on the [Viam app](https://app.viam.com).
    If successful, **Live** should be displayed underneath **Last online**.

8.  You may now add any desired modules to the project by including them in the `dependencies` section of the `Cargo.toml` for the generated project.
    After adding (or removing) a module or changing the version of a module, you must rerun steps 5-6 above in order to rebuild the firmware and reflash the device.

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

To remotely update the firmware on your microcontroller without a physical connection to the device, add the OTA (over-the-air) service to your microcontroller's configuration in the [Viam app](https://app.viam.com).
Use **JSON** mode to add the service as in the template below, then configure the URL from which to fetch new firmware, and the version name.

There are two requirements for hosting firmware:

- The hosting endpoint must use HTTP/2.
- The hosting endpoint must _not_ use redirection.

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
To update the firmware version for a group of microcontrollers at the same time, you can [create a fragment](/manage/software/deploy-packages/) with the OTA service configuration and apply it to multiple machines.
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

Run the following command:

```sh { class="command-line" data-prompt="$"}
espflash flash --erase-parts nvs --partition-table partitions.csv  target/xtensa-esp32-espidf/release/esp32-camera --baud 115200 && sleep 2 && espflash monitor
```

Try the connection command again.
The baud rate on your device may not have been fast enough to connect.
If successful, the Viam app will show that your machine part's status is **Live**.

### Error: `viam.json` not found

If you get the error `viam.json not found` try the following to manually add your machine cloud credentials as a file in your project:

1. Navigate to your machine's page on the [Viam app](https://app.viam.com) and select the **CONFIGURE** tab.
1. Select the part status dropdown to the right of your machine's name on the top of the page: {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}
1. Click the copy icon underneath **Machine cloud credentials**.
   The Micro-RDK needs this JSON object, which contains your machine part secret key and cloud app address, to connect to the [Viam app](https://app.viam.com).
1. Navigate to the directory of the project you just created.
1. Create a new <file>viam.json</file> file and paste the `viam-server` machine cloud credentials in.
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
