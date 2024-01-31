---
title: "The Micro-RDK Development Setup"
linkTitle: "Microcontroller Development Setup"
weight: 50
no_list: true
type: docs
image: "get-started/installation/thumbnails/esp32-espressif.png"
imageAlt: "E S P 32 - espressif"
images: ["/get-started/installation/thumbnails/esp32-espressif.png"]
description: "Set up the Espressif ESP32 for development with the micro-RDK."
# SMEs: Nicolas M., Gautham V., Andrew M.
aliases:
  - "/installation/prepare/microcontrollers/development-setup/"
---

{{% readfile "/static/include/micro-rdk.md" %}}

## Get started

Follow these steps to install and build the micro-rdk on your ESP32 for development:

1. Install the [required software](#software-requirements)
2. [Set up your development environment](#set-up-your-development-environment) manually or with Viam's Canon CLI utility _(recommended)_
3. [Install the Micro-RDK](#install-the-micro-rdk)

{{% readfile "/static/include/micro-rdk-hardware.md" %}}

### Software requirements

The micro-RDK is written in Rust.
To be able to develop the micro-RDK on macOS and Linux systems, you must install the following software on your development machine:

#### Install dependencies

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

#### Install `Rust`

```sh { class="command-line" data-prompt="$"}
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

See the [Rust Installation guide](https://www.rust-lang.org/tools/install) for more information and other installation methods.

#### Install `cargo-generate` with `cargo`

`cargo` installs automatically when downloading Rust with rustup.

Run the following command to install `cargo-generate`:

```sh { class="command-line" data-prompt="$"}
cargo install cargo-generate
```

#### Install `espflash`

Run the following command to install `espflash`

```sh { class="command-line" data-prompt="$"}
cargo install espflash
```

### Set up your development environment

{{< tabs >}}
{{% tab name="Canon CLI (recommended)" %}}

[Canon](https://github.com/viamrobotics/canon) is a CLI utility for managing a Docker-based canonical environment.

Canon requires a working installation of Docker Engine.

[Install Docker Engine](https://docs.docker.com/engine/install/) before proceeding.
If you are running Docker Engine on Linux, make sure that you go through the [post installation steps](https://docs.docker.com/engine/install/linux-postinstall/) to run Docker automatically on startup.

{{< tabs >}}
{{% tab name="Direct Go Install (Linux)" %}}

Make sure your system has [Go 1.19](https://golangtutorial.dev/news/go-1.19-version-released/#major-changes-in-go-119-version) or later installed.
Verify your version of Go with `go version`.

```sh { class="command-line" data-prompt="$"}
go install github.com/viamrobotics/canon@latest
```

Make sure to [add the go binary folder to your `PATH`](https://go.dev/doc/gopath_code) by running:
`export PATH=$PATH:$(go env GOPATH)/bin`.

{{% /tab %}}
{{% tab name="With Homebrew (Linux/MacOS)" %}}

```sh { class="command-line" data-prompt="$"}
brew install viamrobotics/brews/canon
```

{{% /tab %}}
{{% /tabs %}}

{{% /tab %}}
{{% tab name="Manual" %}}

{{< alert title="Tip" color="tip" >}}
You only need to follow these steps if you are not using Canon to build the micro-RDK.

If you have completed your set up with Canon, skip this section and continue to [install the Micro-RDK](#install-the-micro-rdk).

{{< /alert >}}

To set up the Docker development environment for ESP manually, complete the following instructions:

#### Install build dependencies

{{< tabs >}}
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

#### Install and activate the ESP-IDF

Clone Viam's fork of the ESP-IDF, the development framework for Espressif SoCs (System-on-Chips) supported on Windows, Linux and macOS:

```sh { class="command-line" data-prompt="$"}
mkdir -p ~/esp
cd ~/esp
git clone --depth 1 -b v4.4.4 --single-branch --recurse-submodules --shallow-submodules https://github.com/viamrobotics/esp-idf
```

Then, install the required tools for ESP-IDF:

```sh { class="command-line" data-prompt="$"}
cd ~/esp/esp-idf
./install.sh esp32
```

To activate ESP-IDF, run the following command to source (`.`) the activation script `export.sh`:

```sh { class="command-line" data-prompt="$"}
. $HOME/esp/esp-idf/export.sh
```

{{< alert title="Tip" color="tip" >}}
To avoid conflicts with other toolchains, adding this command to your `.bashrc` or `.zshrc` is not recommended.
Instead, save this command to run in any future terminal session where you need to activate the ESP-IDF development framework.
{{< /alert >}}

#### Install the Rust ESP toolchain and activate the ESP-RS virtual environment

First, install the following tools with `cargo`:

```sh { class="command-line" data-prompt="$"}
cargo install espup
```

```sh { class="command-line" data-prompt="$"}
cargo install cargo-espflash v2.0.0-rc.1
```

```sh { class="command-line" data-prompt="$"}
cargo install ldproxy
```

To download and install the esp-rs toolchain, run:

```sh { class="command-line" data-prompt="$"}
espup install -s -f ~/esp/export-rs.sh -v 1.67.0
```

To activate the ESP Rust toolchain, run the following command to source (`.`) the activation script `export-rs.sh`:

```sh { class="command-line" data-prompt="$"}
. $HOME/esp/export-rs.sh
```

{{< alert title="Tip" color="tip" >}}

To avoid conflicts with other toolchains, adding this command to your .bashrc or .zshrc is not recommended.
Instead, save this command to run in any future terminal session where you need to activate the ESP-IDF development framework.

{{< /alert >}}

{{% /tab %}}
{{% /tabs %}}

## Install the micro-RDK

### Create a new machine

Navigate to [the Viam app](https://app.viam.com) and [add a new machine](/fleet/machines/#add-a-new-machine) in your desired location.

Click on the name of the machine to go to the machine's page.
Then, navigate to the **Config** tab.

### Configure your machine with an ESP32

[Client API](/build/program/apis/) usage with the micro-RDK is currently limited to the following supported {{< glossary_tooltip term_id="resource" text="resources" >}}:

- [Base](/build/micro-rdk/base/)
- [Board](/build/micro-rdk/board/)
- [Encoder](/build/micro-rdk/encoder/)
- [Movement Sensor](/build/micro-rdk/movement-sensor/)
- [Motor](/build/micro-rdk/motor/)

See [micro-RDK](/build/micro-rdk/) to get a list of supported models and instructions on how to configure them.
Follow [this guide](/build/micro-rdk/board/esp32/) to configure an `esp32` board on your machine.

### Generate a new project from the micro-RDK template

[Start Docker](https://docs.docker.com/config/daemon/start/) on your development machine.
If you haven't already, complete Docker's [Linux post installation steps](https://docs.docker.com/engine/install/linux-postinstall/) to set up Docker to run whenever your system boots up.

Use [the Micro-RDK template](https://github.com/viamrobotics/micro-rdk-robot-template.git) to create a new Micro-RDK project to upload to your ESP32 by running:

```sh { class="command-line" data-prompt="$"}
cargo generate --git https://github.com/viamrobotics/micro-rdk-robot-template.git
```

You will be prompted to paste your machine's JSON configuration into the terminal.
To obtain this:

- Navigate to [your new machine's](#create-a-new-machine) page on [the Viam app](https://app.viam.com).
- Click on the **Setup** tab.
  Keep your `Mode` and `Architecture` selections at default.
- Click the **Copy viam-server config** button on the right side of the **Setup** tab.
  The micro-RDK needs this JSON file, which contains your machine part secret key and cloud app address, to connect to the [Viam app](https://app.viam.com).
- Paste the `viam-server` config into your terminal when prompted.

{{% snippet "secret-share.md" %}}

### Upload the micro-RDK to your ESP32

Now, upload the project to connect to your ESP32 and remotely control it live on [the Viam app](https://app.viam.com):

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

If successful, you will retain a serial connection to the board until you press `Ctrl-C`.
To manage this connection, consider running it within a dedicated terminal session, or under `tmux` or `screen`.
While the serial connection is live, you can also restart the currently flashed image with `Ctrl-R`.

Navigate to your new machine's page on [the Viam app](https://app.viam.com).
If successful, **Live** should be displayed underneath **Last online**.

### Troubleshooting

If you run into the error `Failed to open serial port` when flashing your ESP32 with Linux, make sure the user is added to the group `dialout` with `sudo gpasswd -a $USER dialout`

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
