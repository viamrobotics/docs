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

To work with Viam's Micro-RDK, ESP32 microcontrollers must have at least:

- 2 cores
- 384kB SRAM
- 2MB PSRAM
- 8MB flash

The following microcontrollers have been tested with Viam:

- [ESP32-WROVER Series](https://www.espressif.com/en/products/modules/esp32)

{{% hiddencontent %}}
The Micro-RDK and `viam-micro-server` do not support 32-bit Linux.
{{% /hiddencontent %}}

## About ESP32 microcontroller setup

Microcontrollers do not run operating systems and are instead flashed with dedicated firmware.
Because of this, the microcontroller setup process is different than for SBCs, laptops, and desktops.

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

1. Create a Viam account on [app.viam.com](https://app.viam.com).
   You can configure and manage devices and data collection in the web UI.

1. Add a new _{{< glossary_tooltip term_id="machine" text="machine" >}}_ using the button in the top right corner of the **LOCATIONS** tab in the app.
   A machine represents your device.

1. On your machine's page, click **View setup instructions** and follow the steps for your operating system.
   The app provides commands to install `viam-micro-server` and connect it to the cloud with your machine's unique credentials.

1. A secure connection is automatically established between your machine and Viam.
   When you update your machine's configuration, `viam-micro-server` automatically gets the updates.

   You are ready to [configure](#configure-and-test-your-machine) any of the components listed above on your machine.

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

   If you haven't already, [install Homebrew](https://brew.sh/).

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

   Add a new machine on [Viam](https://app.viam.com).
   Click on the name of the machine to go to the machine's page, then select the **CONFIGURE** tab.

   Then select the part status dropdown to the right of your machine's name on the top of the page and copy the **Machine cloud credentials**:

   {{<imgproc src="/get-started/micro-credentials.png" resize="450x" declaredimensions=true alt="Machine part info menu accessed by Live status indicator, with machine cloud credentials button highlighted." class="shadow" >}}

   The Micro-RDK needs these credentials, which contain your machine part secret key and cloud app address, to connect to Viam.

1. Generate a new project skeleton from [this template](https://github.com/viamrobotics/micro-rdk/tree/main/templates/project):

   ```sh { class="command-line" data-prompt="$"}
   cargo generate --git https://github.com/viamrobotics/micro-rdk.git
   ```

   Follow the prompts:

   - Which sub-template should be expanded?: `templates/project`.
   - Project name: Your choice.
   - MCU: `esp32`.
   - Include camera module?: If you will use an `esp32-camera` or a `fake` camera as a component of your machine, select `true`.
   - Machine cloud credentials: Paste in the machine cloud credentials you obtained in step 1.
   - Enter Wi-Fi name: The name of the Wi-Fi network for the ESP32 to connect to on boot. Note that you must provide a 2.4 GHz network.
   - Enter the Wi-Fi password: The password for the 2.GHz WiFi network.

   Hit **Enter** to generate the project.
   The CLI automatically initializes a git repository in the generated directory for version control.

1. Navigate into the generated project:

   ```sh { class="command-line" data-prompt="$"}
   cd <path-to/your-project-directory>
   ```

1. Add any desired modules to the project by including them in the `dependencies` section of the `Cargo.toml` for the generated project:

   {{< tabs >}}
   {{% tab name="Local path dependency" %}}

   While developing a module, you'll typically use a local path dependency to reference your module directory, for example:

   ```toml {class="line-numbers linkable-line-numbers" data-line="3"}
   [dependencies]
   ...
   my-module = { path = "../my-module" }
   ```

   {{% /tab %}}
   {{% tab name="Git repository dependency" %}}

   For modules hosted in a Git repository, specify the repository URL and optionally a specific commit (`rev`), branch (`branch`), or tag (`tag`), for example:

   ```toml {class="line-numbers linkable-line-numbers" data-line="3"}
   [dependencies]
   ...
   my-module = { git = "https://github.com/username/my-module.git", tag = "v1.0.0" }
   ```

   To use any of the [example modules](https://github.com/viamrobotics/micro-rdk/blob/main/examples/modular-drivers/README.md#example-modules) provided by Viam, use this line, specifying the Micro-RDK version that matches your development environment:

   ```toml {class="line-numbers linkable-line-numbers" data-line="3"}
   [dependencies]
   ...
   micro-rdk-modular-driver-example = { git = "https://github.com/viamrobotics/micro-rdk.git", rev = "v0.5.0", package = "micro-rdk-modular-driver-example", features = ["esp32"] }
   ```

   {{% /tab %}}
   {{< /tabs >}}

1. Compile the project:

   ```sh { class="command-line" data-prompt="$"}
   make build-esp32-bin
   ```

   The first build can take a few minutes, as ESP-IDF must be cloned and built, and all dependent Rust crates must be fetched and built.
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
   While the serial connection is live, you can also restart the currently flashed image with `Ctrl-R`.

1. Navigate to your new machine's page.
   If successful, the status indicator should turn green and show the **Live** status.

### Configure and test your machine

You can now configure the models you included in your firmware and test them:

1. Navigate to your machine's page.

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

1. If you make changes to your module code, rerun the build and flash steps to update the firmware and test the new version on your ESP32.

## Configure over-the-air updates

You can update the firmware on your microcontroller without a physical connection.

{{% hiddencontent %}}
Over-the-air updates are available for `viam-server` and the Micro-RDK. For information about `viam-server` see [Deploy software packages to machines](/manage/software/deploy-software/).
The following information covers the Micro-RDK.
{{% /hiddencontent %}}

The first time you flash your microcontroller, you must build a full firmware image, and use a data cable to flash it to your microcontroller.
After the initial flash, you can update the firmware remotely by using the over-the-air (OTA) service to pull [cloud-hosted, OTA-ready firmware](#build-and-host-ota-firmware) from a URL.

The firmware hosting endpoint must use HTTP/2.

To configure OTA updates:

1. On your machine's page, go to the **CONFIGURE** tab and select **JSON** mode.

1. Paste in the template below, then configure the URL from which to fetch new firmware, and a version name of your choice.
   The value of the `version` field is not directly used by the OTA service, so you can use any string.

   {{< tabs >}}
   {{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers" data-line="3-11"}
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
        "url": "https://github.com/Jessamy/modulefirmware/releases/download/v0.1.2/modulefirmware-ota.bin",
        "version": "myVersion1"
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

Your device checks for configuration updates periodically.
If the device receives a configuration with a modified `version` field, the device downloads the new firmware to an inactive partition and restarts.
When the device boots it loads the new firmware.

To trigger a remote update of the firmware on your microcontroller after the initial configuration, edit the `version` field and save the config.

{{% alert title="Note" color="note" %}}
There is no way to roll back to previous firmware after a bad upgrade without reflashing the device with a physical connection, so test your firmware thoroughly before deploying it to a fleet.
{{% /alert %}}

### Update multiple microcontrollers at the same time

To update the firmware version for a group of microcontrollers at the same time, you can [create a fragment](/manage/software/deploy-software/) with the OTA service configuration and apply it to multiple machines.
Then, whenever you update the `version` field in the fragment, the version will be updated for each machine that has that fragment in its config, triggering a firmware update the next time the devices fetch their configs.

### Build and host OTA firmware

To use the OTA service, you must host your firmware in the cloud so that it can be accessed at a URL.

GitHub workflows simplify the process of building and hosting your firmware by eliminating the need to build locally and then upload the firmware image to a cloud storage bucket.

{{< tabs >}}
{{% tab name="Use GitHub workflows (recommended)" %}}

To build firmware on GitHub, follow these steps:

1. [Create a firmware project](#build-and-flash-custom-firmware).
   _Do not include Wi-Fi credentials or machine cloud credentials in the project_, since you will be publishing the project to a public GitHub repository.
   The OTA service does not modify the partition containing the machine cloud credentials and WiFi credentials, so OTA updates do not require the credentials.

1. Create a public GitHub repository for your firmware project, and upload the contents of the firmware project directory to the repository.
   The `templates/project` template you used to create your project contains a GitHub workflow file that is used to build your firmware.

1. In the firmware GitHub repository, navigate to **Settings** &rarr; **Actions** &rarr; **General** and enable **Read and write permissions**.

1. Go to the firmware GitHub repository's **Releases** page and create a new release.
   Create a tag starting with `v` followed by a version number, for example `v1.0.0`.
   Click **Publish release** to trigger a build of the firmware.

To deploy the firmware:

1. Wait for the build to complete.

1. In your firmware GitHub repository, navigate to the **Releases** page and find the assets for the release you just created.
   The assets include the full and OTA firmware images.
   Copy the URL of the OTA firmware image.

1. Navigate to your machine's **CONFIGURE** tab and [configure the OTA service](#configure-over-the-air-updates) with the URL of the firmware image you just copied.

{{% /tab %}}
{{% tab name="Build locally and host manually" %}}

If you want to use OTA updates, but don't want to use GitHub Actions, follow these steps:

1. Build the OTA firmware locally with the following command:

   ```sh { class="command-line" data-prompt="$"}
   make build-esp32-ota
   ```

   Note that this is different from the `make build-esp32-bin` command, which builds a full firmware image that you must use the first time you flash your microcontroller.

1. Upload the OTA firmware image to a cloud storage bucket.

1. Configure the URL of the cloud storage bucket in your microcontroller's OTA service configuration.

{{% /tab %}}
{{< /tabs >}}
