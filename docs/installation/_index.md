---
title: "Installation Guide"
linkTitle: "Installation Guide"
childTitleEndOverwrite: "Try Viam"
weight: 20
no_list: true
type: docs
image: "/installation/thumbnails/install.png"
imageAlt: "Install Viam"
images: ["/installation/thumbnails/install.png"]
description: "To use Viam software with your robot, install and run the viam-server binary on the computer that you want to use to control the robot."
aliases:
    - /installation/prepare/
    - /installation/macos-install/
    - /installation/linux-install/
    - /installation/install/
    - /installation/install/linux-install/
    - /installation/install/macos-install
    - /getting-started/installation/
    - /getting-started/macos-install/
    - /getting-started/linux-install/
---

To use Viam software with your robot, install and run the `viam-server` binary on the computer that you want to use to control the robot.
In most cases, this will be a [single board computer (SBC)](#install-on-a-single-board-computer), like a Raspberry Pi, but you can also install `viam-server` on a [macOS or Linux computer](#install-on-a-macos-or-linux-computer).

For an overview of the Viam software platform, see [Viam in 3 minutes](/viam/).

## Install on a single board computer

### Prepare your board

If you haven't already, you must install a supported operating system on your {{< glossary_tooltip term_id="board" text="board" >}} (SBC).
`viam-server` supports Linux 64-bit operating systems running on the `aarch64` or `x86_64` architectures.
If you are using one of the following boards, you can follow our guide for that board to prepare it for installation:

{{< cards >}}
{{% card link="/installation/prepare/rpi-setup/" class="small" %}}
{{% card link="/installation/prepare/beaglebone-setup/" class="small" %}}
{{% card link="/installation/prepare/sk-tda4vm/" class="small" %}}
{{% card link="/installation/prepare/jetson-nano-setup/" class="small" %}}
{{% card link="/installation/prepare/jetson-agx-orin-setup/" class="small" %}}
{{< /cards >}}

<br>

Viam also provides a lightweight version of `viam-server` which can run on resource-limited embedded systems that cannot run the fully-featured Robot Development Kit (RDK).
If you are using an ESP32 microcontroller, prepare your board using the following guide:

{{< cards >}}
{{% card link="/installation/prepare/microcontrollers" class="small" %}}
{{< /cards >}}

Other SBCs such as the [RockPi S](https://wiki.radxa.com/RockpiS) and [Orange Pi Zero 2](https://orangepi.com/index.php?route=product/product&path=237&product_id=849) can run Viam with an experimental [periph.io](https://periph.io/) based [modular component](https://github.com/viam-labs/periph_board).

### Install `viam-server`

Once you have a compatible operating system on your board, follow along with the video below or walk through the steps outlined beneath it to install `viam-server` on your board:

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/gmIW9JoWStA">}}

#### Installation steps

1. Go to the [Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots/#add-a-new-robot).
   If this is your first time using the Viam app, you must create an account first.

1. On the **Setup** tab, select `Linux` for **Mode** and select the appropriate **Architecture** for your board.
   On most Linux operating systems, you can run `uname -m` to confirm your board's architecture.

1. Follow the steps shown on the **Setup** tab to install `viam-server` on your board.

1. Once `viam-server` is installed and running on your board, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your robot has successfully connected.

By default, `viam-server` will start automatically when your system boots, but you can [change this behavior](/installation/manage/) if desired.

## Install on a macOS or Linux computer

You can also install `viam-server` on a macOS or Linux computer.
This is useful if you don't have a board available, or if you want to run a Viam [service](/services/) with your robot that requires more computing resources than is otherwise available on an SBC.
Select the tab below for your operating system:

{{< tabs name="Install on computer" >}}
{{% tab name="macOS computer" %}}

### Install on a macOS computer

`viam-server` is available for macOS users through [Homebrew](https://docs.brew.sh/Installation), and supports both Intel and Apple Silicon macOS computers.
To install `viam-server` on a macOS computer:

1. Go to the [Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots/#add-a-new-robot).
   If this is your first time using the Viam app, you must create an account first.

1. On the **Setup** tab, select `Mac` for **Mode**.

1. Follow the steps shown on the **Setup** tab to install `viam-server` on your macOS computer.

1. Once `viam-server` is installed and running, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your computer has successfully connected.

{{% /tab %}}
{{% tab name="Linux computer" %}}

### Install on a Linux computer

`viam-server` is distributed for Linux as an [AppImage](https://appimage.org/).
The AppImage is a single, self-contained binary that runs on 64-bit Linux systems running the `aarch64` or `x86_64` architectures, with no need to install any dependencies.
To install `viam-server` on a Linux computer:

1. Go to the [Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots/#add-a-new-robot).
   If this is your first time using the Viam app, you must create an account first.

1. On the **Setup** tab, select `Linux` for **Mode** and select the appropriate **Architecture** for your computer.
   On most Linux operating systems, you can run `uname -m` to confirm your computer's architecture.

1. Follow the steps shown on the **Setup** tab to install `viam-server` on your Linux computer.

1. Once `viam-server` is installed and running, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your computer has successfully connected.

By default, `viam-server` will start automatically when your system boots, but you can [change this behavior](/installation/manage/) if desired.

{{% /tab %}}
{{< /tabs >}}

## Next Steps

{{< cards >}}
  {{% card link="/manage/configuration/" %}}
  {{% card link="/tutorials/" %}}
  {{% card link="/try-viam/" %}}
{{< /cards >}}
