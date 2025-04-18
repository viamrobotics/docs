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

   Select `templates/project` when prompted. Give the project a name of your choice.
   Select `esp32` for **MCU**.
   If you wish to configure an `esp32-camera` or a `fake` camera as a component of your machine, select **true** for **include camera module and traits**.

   You will be prompted to paste your machine's `viam-server` robot JSON configuration into the terminal, which is the same thing as its machine cloud credentials.
   Paste in the credentials you obtained in step 1.

1. Navigate into the generated project:

   ```sh { class="command-line" data-prompt="$"}
   cd <path-to/your-project-directory>
   ```

1. If you wish to use version control for this project, this is the best time to initialize a git repository and commit all the generated files, but be sure to exclude the generated `viam.json` file, which includes secrets:

   ```sh { class="command-line" data-prompt="$"}
   git add .
   git restore viam.json
   git commit -m "initial commit"
   ```

1. Add any desired modules to the project by including them in the `dependencies` section of the `Cargo.toml` for the generated project.

1. Compile the project using one of the following commands, depending on whether you want to use over-the-air (OTA) firmware updates or not:

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

   The first build may be fairly time consuming, as ESP-IDF must be cloned and built, and all dependent Rust crates must be fetched and built as well.
   Subsequent builds will be faster.

### Flash your ESP32

Upload the generated firmware to your ESP32:

1. Use a data cable to connect your ESP32 board to a USB port on your development machine.

1. Run the following command to flash the firmware to your ESP32:

   ```sh { class="command-line" data-prompt="$"}
   make flash-esp32-bin
   ```

   When prompted, select the serial port that your ESP32 is connected to through a data cable.

   If successful, you will retain a serial connection to the board until you press `Ctrl-C`.
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
   For example, if you want to use a board, your configuration could look similar to this:

   ```json
   {
     "components": [
       {
         "name": "my-board",
         "model": "esp32",
         "api": "rdk:component:board",
         "attributes": {
           "pins": [15, 34],
           "analogs": [
             {
               "pin": "34",
               "name": "sensor"
             }
           ],
           "digital_interrupts": [
             {
               "pin": 4
             }
           ]
         },
         "depends_on": []
       }
     ]
   }
   ```

1. Click **Builder** mode and find the configuration card of the component you want to test.

1. Click to open the **Test** section of the card and use the interface to test the component.
