---
title: "viam-micro-server Development Setup"
linkTitle: "viam-micro-server dev setup"
weight: 5
no_list: true
type: docs
images: ["/installation/thumbnails/esp32-espressif.png"]
imageAlt: "E S P 32 - espressif"
description: "Set up the Espressif ESP32 for development with `viam-micro-server`."
# SMEs: Nicolas M., Gautham V., Andrew M.
aliases:
  - /installation/prepare/microcontrollers/development-setup/
  - /get-started/installation/prepare/microcontrollers/development-setup/
  - /get-started/installation/microcontrollers/development-setup/
  - /get-started/installation/viam-micro-server-dev/
  - /installation/viam-micro-server-dev/
---

`viam-micro-server` is the lightweight version of [`viam-server`](/get-started/#viam-server) which can run on resource-limited embedded systems (ESP32) that cannot run the fully-featured `viam-server`.

This page provides instructions for you to customize `viam-micro-server` and create modules.

{{< alert title="Looking to install viam-micro-server?" color="note" >}}
If you only want to install and use `viam-micro-server`, see [Install `viam-micro-server`](/installation/#install-viam-micro-server) instead.
{{< /alert >}}

Follow these steps to install and build `viam-micro-server` on your ESP32 for development:

1. Install the [required software](#software-requirements)
2. [Set up your development environment](#set-up-your-development-environment) with Viam's Canon CLI utility _(recommended)_ or manually
3. [Install `viam-micro-server`](#install-viam-micro-server)

## Software requirements

`viam-micro-server` is written in Rust.
To be able to develop `viam-micro-server` on macOS and Linux systems, you must install the following software on your development machine:

1. Install dependencies:

   {{< tabs >}}
   {{% tab name="Linux" %}}

```sh { class="command-line" data-prompt="$"}
sudo apt-get install git libssl-dev dfu-util libusb-1.0-0 libudev-dev
```

    {{% /tab %}}
    {{% tab name="macOS" %}}

If you haven't already, install Homebrew:

```sh { class="command-line" data-prompt="$"}
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then, install `dfu-util`:

```sh { class="command-line" data-prompt="$"}
brew install dfu-util
```

    {{% /tab %}}
    {{% /tabs %}}

2. Install `Rust` and `cargo`

   ```sh { class="command-line" data-prompt="$"}
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

   Once completed open a new tab on your terminal or run `. "$HOME/.cargo/env"`.

   See the [Rust Installation guide](https://www.rust-lang.org/tools/install) for more information and other installation methods.

3. Install `cargo-generate` with `cargo`

   Run the following command to install `cargo-generate`:

   ```sh { class="command-line" data-prompt="$"}
   cargo install cargo-generate
   ```

4. Install `espflash`

   Run the following command to install `espflash`:

   ```sh { class="command-line" data-prompt="$"}
   cargo install espflash
   ```

## Set up your development environment

{{< tabs >}}
{{% tab name="Canon CLI (recommended)" %}}

[Canon](https://github.com/viamrobotics/canon) is a CLI utility for managing a Docker-based canonical environment.

1. [Install Docker Engine](https://docs.docker.com/engine/install/). Canon requires a working installation of Docker Engine.
2. If you are running Docker Engine on Linux, make sure that you go through the [post installation steps](https://docs.docker.com/engine/install/linux-postinstall/) to run Docker automatically on startup.

{{< tabs >}}
{{% tab name="Direct Go Install (Linux)" %}}

3. Run `go version` to confirm your system has [Go 1.19](https://golangtutorial.dev/news/go-1.19-version-released/#major-changes-in-go-119-version) or later installed.
4. Install canon:

   ```sh { class="command-line" data-prompt="$"}
   go install github.com/viamrobotics/canon@latest
   ```

5. [Add the go binary folder to your `PATH`](https://go.dev/doc/gopath_code) by running:

   ```sh { class="command-line" data-prompt="$"}
   export PATH=$PATH:$(go env GOPATH)/bin
   ```

{{% /tab %}}
{{% tab name="With Homebrew (Linux/MacOS)" %}}

3. Install canon:

   ```sh { class="command-line" data-prompt="$"}
   brew install viamrobotics/brews/canon
   ```

{{% /tab %}}
{{% /tabs %}}

{{% /tab %}}
{{% tab name="Manual" %}}

To set up the Docker development environment for ESP manually, complete the following instructions:

{{< alert title="Tip" color="tip" >}}
You only need to follow these steps if you are not using Canon to build `viam-micro-server`.

If you have completed your set up with Canon, skip this section and continue to [install `viam-micro-server`](#install-viam-micro-server).

{{< /alert >}}

1. Install additional build dependencies:

{{% tabs %}}
{{% tab name="Linux" %}}

```sh { class="command-line" data-prompt="$"}
sudo apt-get install git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
```

{{% /tab %}}
{{% tab name="macOS" %}}

```sh { class="command-line" data-prompt="$"}
brew install cmake ninja dfu-util
```

{{% /tab %}}
{{% /tabs %}}

2.  Install and activate the ESP-IDF

    Clone Viam's fork of the ESP-IDF, the development framework for Espressif SoCs (System-on-Chips) supported on Windows, Linux and macOS:

    ```sh { class="command-line" data-prompt="$"}
    mkdir -p ~/esp
    cd ~/esp
    git clone --depth 1 -b v4.4.4 --single-branch --recurse-submodules --shallow-submodules https://github.com/viamrobotics/esp-idf
    ```

3.  Then, install the required tools for ESP-IDF:

    ```sh { class="command-line" data-prompt="$"}
    cd ~/esp/esp-idf
    ./install.sh esp32
    ```

4.  To activate ESP-IDF, run the following command to source (`.`) the activation script `export.sh`:

        ```sh { class="command-line" data-prompt="$"}
        . $HOME/esp/esp-idf/export.sh
        ```

        {{< alert title="Tip" color="tip" >}}

    To avoid conflicts with other toolchains, adding this command to your `.bashrc` or `.zshrc` is not recommended.
    Instead, save this command to run in any future terminal session where you need to activate the ESP-IDF development framework.
    {{< /alert >}}

5.  Install the following tools with `cargo`:

    ```sh { class="command-line" data-prompt="$"}
    cargo install espup
    cargo install cargo-espflash
    cargo install ldproxy
    ```

6.  Download and install the ESP-RS toolchain:

    ```sh { class="command-line" data-prompt="$"}
    espup install -s -f ~/esp/export-rs.sh -v 1.67.0
    ```

7.  Activate the ESP Rust toolchain, run the following command to source (`.`) the activation script `export-rs.sh`:

        ```sh { class="command-line" data-prompt="$"}
        . $HOME/esp/export-rs.sh
        ```

        {{< alert title="Tip" color="tip" >}}

    To avoid conflicts with other toolchains, adding this command to your .bashrc or .zshrc is not recommended.
    Instead, save this command to run in any future terminal session where you need to activate the ESP-IDF development framework.
    {{< /alert >}}

{{% /tab %}}
{{% /tabs %}}

## Install `viam-micro-server`

1. Create a new machine

   Navigate to [the Viam app](https://app.viam.com) and [add a new machine](/cloud/machines/#add-a-new-machine) in your desired location.

   Click on the name of the machine to go to the machine's page.

1. [Start Docker](https://docs.docker.com/config/daemon/start/) on your development machine.
   If you haven't already, complete Docker's [Linux post installation steps](https://docs.docker.com/engine/install/linux-postinstall/) to set up Docker to run whenever your system boots up.

1. Generate a new project from [this template](https://github.com/viamrobotics/micro-rdk/tree/main/templates/project) to create a new micro-RDK project to upload to your ESP32 by running:

   ```sh { class="command-line" data-prompt="$"}
   cargo generate --git https://github.com/viamrobotics/micro-rdk.git
   ```

   Select `templates/project` when prompted.
   Give the project a name of your choice.
   Select `esp32` for **MCU**.
   If you wish to configure an `esp32-camera` or a `fake` camera as a component of your machine, select **true** for **include camera module and traits**.

   You will be prompted to paste your machine's `viam-server` robot JSON configuration into the terminal, which is the same thing as its machine cloud credentials.

   To obtain this:

   - Navigate to your new machine's page on [the Viam app](https://app.viam.com) and select the **CONFIGURE** tab.
   - Select the part status dropdown to the right of your machine's name on the top of the page: {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}
   - Click the copy icon underneath **Machine cloud credentials**.
     `viam-micro-server` needs this JSON, which contains your machine part secret key and cloud app address, to connect to the [Viam app](https://app.viam.com).
   - Paste the machine cloud credentials into your terminal when prompted.

   {{% snippet "secret-share.md" %}}

1. Upload `viam-micro-server` to your ESP32

   Now, flash the project to your ESP32 and it will connect to [the Viam app](https://app.viam.com) from which you can then remotely control it:

   {{< tabs >}}
   {{% tab name="Use Canon" %}}

```sh { class="command-line" data-prompt="$"}
cd <your-path-to/your-project-directory>
canon bash -lc "make build-esp32-bin"
make flash-esp32-bin
```

    {{% /tab %}}
    {{% tab name="Local environment" %}}

Make sure you have run `. ~/dev/esp/export-rs.sh` and `. ~/dev/esp/esp-idf/export.sh` before running the following command:

```sh { class="command-line" data-prompt="$"}
make upload
```

    {{% /tab %}}
    {{% /tabs %}}

    When prompted, select the serial port that your ESP32 is connected to through a data cable.

    If successful, you will retain a serial connection to the board until you press `Ctrl-C`.
    To manage this connection, consider running it within a dedicated terminal session, or under `tmux` or `screen`.
    While the serial connection is live, you can also restart the currently flashed image with `Ctrl-R`.

1. Navigate to your new machine's page on [the Viam app](https://app.viam.com).
   If successful, **Live** should be displayed underneath **Last online**.

## Troubleshooting

If you run into the error `Failed to open serial port` when flashing your ESP32 with Linux, make sure the user is added to the group `dialout` with `sudo gpasswd -a $USER dialout`.

If you get the following error while connecting to your ESP32:

```sh { class="command-line" data-prompt="$"}
`Error: espflash::timeout

  × Error while connecting to device
  ╰─▶ Timeout while running command
```

If successful, the Viam app will show that your machine part's status is **Live**.

Run the following command:

```sh { class="command-line" data-prompt="$"}
espflash flash --erase-parts nvs --partition-table partitions.csv  target/xtensa-esp32-espidf/release/esp32-camera --baud 115200 && sleep 2 && espflash monitor
```

Try the connection command again.
The baud rate on your device may not have been fast enough to connect.
If successful, the Viam app will show that your machine part's status is **Live**.

If you get the error `viam.json not found` try the following to manually add your machine cloud credentials as a file in your project:

1. Navigate to your machine's page on [the Viam app](https://app.viam.com) and select the **CONFIGURE** tab.
1. Select the part status dropdown to the right of your machine's name on the top of the page: {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Restart button on the machine part info dropdown">}}
1. Click the copy icon underneath **Machine cloud credentials**.
   `viam-micro-server` needs this JSON, which contains your machine part secret key and cloud app address, to connect to the [Viam app](https://app.viam.com).
1. Navigate to the directory of the project you just created.
1. Create a new <file>viam.json</file> file and paste the `viam-server` machine cloud credentials in.
1. Save the file.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
