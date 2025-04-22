---
linkTitle: "Set up an ESP32"
title: "Set up an ESP32"
weight: 25
layout: "docs"
type: "docs"
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
no_list: false
description: "Install the lightweight version of the software that drives hardware and connects your device to the cloud."
prev: "/operate/get-started/basics/"
next: "/operate/get-started/other-hardware/micro-module/"
aliases:
  - /installation/microcontrollers/
  - /installation/prepare/microcontrollers/
  - /installation/prepare/microcontrollers/
  - /build/micro-rdk/
  - /get-started/installation/microcontrollers/
  - /installation/viam-micro-server-setup/
  - /operate/reference/viam-micro-server/viam-micro-server-troubleshooting/
---

Viam maintains a [lightweight version of `viam-server`](/operate/reference/viam-micro-server/) for microcontrollers.

## Supported microcontrollers

ESP32 microcontrollers must have at least 2 cores, 384kB SRAM, 2MB PSRAM and 8MB flash to work with Viam.
The following microcontrollers have been tested with Viam:

- [ESP32-WROVER Series](https://www.espressif.com/en/products/modules/esp32)

## About ESP32 microcontroller setup

Because microcontrollers do not run operating systems and are instead flashed with firmware, the setup process is different than for regular computers and SBCs.

To use an ESP32 controller with custom hardware, you build a firmware version from the Micro-RDK and modules to support your hardware.

To quickly try out Viam for microcontrollers, you can use the pre-built binary `viam-micro-server` which supports the following components:

- [`gpio`](/operate/reference/components/servo/gpio-micro-rdk/): A servo controlled by GPIO pins.
- [`two_wheeled_base`](/operate/reference/components/base/two_wheeled_base/): A robotic base with differential steering.
- [`free_heap_sensor`](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src): Reports the amount of free heap memory on the microcontroller.
- [`wifi_rssi_sensor`](https://github.com/viamrobotics/micro-rdk/tree/main/examples/modular-drivers/src): Reports the signal strength of the ESP32's WiFi connection.

## Quickstart with pre-built firmware

{{% hiddencontent %}}
Viam provides installers to flash an ESP32 from macOS or Linux running on the x86_64 or ARM64 (AArch64) processor architectures.
{{% /hiddencontent %}}

To get started quickly with the pre-built `viam-micro-server` binary, follow these steps:

1. Create a [Viam app](https://app.viam.com) account.
   The Viam app is the online hub for configuring and managing devices as well as viewing data.

1. Add a new _{{< glossary_tooltip term_id="machine" text="machine" >}}_ using the button in the top right corner of the **LOCATIONS** tab in the app.
   A machine represents your device.

1. From your machine's page in the Viam app, click **View setup instructions** and follow the steps for your operating system.
   The app provides commands to install `viam-micro-server` and connect it to the cloud with your machine's unique credentials.

1. A secure connection is automatically established between your machine and the Viam app.
   When you update your machine's configuration, `viam-micro-server` automatically gets the updates.

   You are ready to [configure](/operate/get-started/supported-hardware/) any of the components listed above on your machine.

## Build and flash custom firmware

If you are using your ESP32 with resources that are not supported by the pre-built binary, you can build your own firmware with the Micro-RDK and your choice of {{< glossary_tooltip term_id="module" text="modules" >}}.

### Set up your development environment

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
   espup install -s -f /dev/null -v 1.85.0
   ```

{{% hiddencontent %}}
Prior versions of the above `espup` instructions created a file called `export-rs.sh` which needed to be sourced before proceeding.
That requirement [no longer applies](https://github.com/esp-rs/esp-idf-hal/issues/319#issuecomment-1785168921) for Micro-RDK development.
The above command redirects `espup`'s production of the setup script to `/dev/null` to avoid cluttering the home directory.
If you would like to instead retain the setup script, replace `/dev/null` in the above command with the location where you would like the script to be written, or remove the `-f /dev/null` entirely and the file will be written to `$HOME/export-esp.sh` by default.
{{% /hiddencontent %}}

### Build your firmware

Create firmware that integrates an existing module with the Micro-RDK:

1. Create a new machine and obtain its credentials:

   Navigate to the [Viam app](https://app.viam.com) and add a new machine.
   Click on the name of the machine to go to the machine's page, then select the **CONFIGURE** tab.

   Then select the part status dropdown to the right of your machine's name on the top of the page and copy the **Machine cloud credentials**:

   {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown" class="shadow" >}}

   The Micro-RDK needs these credentials, which contains your machine part secret key and cloud app address, to connect to the [Viam app](https://app.viam.com).

   {{% snippet "secret-share.md" %}}

1. Generate a new project skeleton from [this template](https://github.com/viamrobotics/micro-rdk/tree/main/templates/project):

   ```sh { class="command-line" data-prompt="$"}
   cargo generate --git https://github.com/viamrobotics/micro-rdk.git
   ```

   Follow the prompts:

   - Select `templates/project` when prompted.
   - Give the project a name of your choice.
   - Select `esp32` for **MCU**.
   - If you wish to configure an `esp32-camera` or a `fake` camera as a component of your machine, select **true** for **Include camera module?**.
   - For **Machine cloud credentials**, paste in the machine cloud credentials you obtained in step 1.

   Hit **Enter** to generate the project.
   The CLI automatically initializes a git repository in the generated directory for version control and in case you want to use cloud build later.

1. Navigate into the generated project:

   ```sh { class="command-line" data-prompt="$"}
   cd <path-to/your-project-directory>
   ```

1. Add any desired modules to the project by including them in the `dependencies` section of the `Cargo.toml` for the generated project.
   For example, to add any of the [example modules](https://github.com/viamrobotics/micro-rdk/blob/main/examples/modular-drivers/README.md#example-modules), add the following line to the `Cargo.toml` file, replacing `v0.5.0` with the version of the Micro-RDK you are using:

   ```toml {class="line-numbers linkable-line-numbers" data-line="3"}
   [dependencies]
   ...
   micro-rdk-modular-driver-example = { git = "https://github.com/viamrobotics/micro-rdk.git", rev = "v0.5.0", package = "micro-rdk-modular-driver-example", features = ["esp32"] }
   ```

1. Compile the project using one of the following commands, depending on whether you want to use [over-the-air (OTA) firmware updates](/operate/reference/viam-micro-server/manage-micro/#over-the-air-updates) or not:

   {{< tabs >}}
   {{% tab name="OTA" %}}

   ```sh { class="command-line" data-prompt="$"}
   make build-esp32-ota
   ```

   {{% /tab %}}
   {{% tab name="No OTA" %}}

   ```sh { class="command-line" data-prompt="$"}
   make build-esp32-bin
   ```

   {{% /tab %}}
   {{< /tabs >}}

   The first build may be fairly time consuming, as ESP-IDF must be cloned and built, and all dependent Rust crates must be fetched and built.
   Subsequent builds will be faster.

### Flash your ESP32

Upload the generated firmware to your ESP32:

1. Use a data cable to connect your ESP32 board to a USB port on your development machine.

1. Run the following command to flash the firmware to your ESP32:

   ```sh { class="command-line" data-prompt="$"}
   make flash-esp32-bin
   ```

   When prompted, select the serial port that your ESP32 is connected to through a data cable.

   If the flash is successful, you will retain a serial connection to the board until you press `Ctrl-C`.
   To manage this connection, consider running it within a dedicated terminal session, or under `tmux` or `screen`.
   While the serial connection is live, you can also restart the currently flashed image with `Ctrl-R`.

1. Navigate to your new machine's page on the [Viam app](https://app.viam.com).
   If successful, the status indicator should turn green and show **Live**.

   {{< alert title="Note" color="tip" >}}

After adding (or removing) a module or changing the version of a module, you must rerun the build and flash steps in order to rebuild the firmware and reflash the device.

The above build and flash steps may be combined by using the `upload` target:

```sh { class="command-line" data-prompt="$"}
make upload
```

{{< /alert >}}

### Configure and test your machine

You can now configure the models you included in your firmware and test them:

1. Navigate to your machine's page in the [Viam app](https://app.viam.com).

1. From the **CONFIGURE** tab, click **JSON** mode.
   Micro-RDK components and services must be configured in JSON.

1. Add your components and services to the machine configuration.
   If you are using one of the example modules, find configuration details in the [example modules README](https://github.com/viamrobotics/micro-rdk/blob/main/examples/modular-drivers/README.md#example-modules).
   For example, if you want to use a free heap sensor, your configuration could look like this:

   ```json
   {
     "components": [
       {
         "name": "my-free-heap-sensor",
         "api": "rdk:component:sensor",
         "model": "free-heap",
         "attributes": {}
       }
     ]
   }
   ```

1. Click **Builder** mode and find the configuration card of the component you want to test.

1. Click to open the **Test** section of the card and use the interface to test the component.

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

You can also try disconnecting and reconnecting the ESP32 to the USB port, then retrying the flash command.

### Error: `viam.json` not found

If you get the error `viam.json not found` try the following to manually add your machine cloud credentials as a file in your project:

1. Navigate to your machine's page on the [Viam app](https://app.viam.com) and select the **CONFIGURE** tab.
1. Select the part status dropdown to the right of your machine's name on the top of the page:

   {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown" class="shadow" >}}

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
