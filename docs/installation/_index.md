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
description: "To use Viam software with your smart machine, install and run the viam-server binary on the computer that will run your smart machine and is connected to your hardware."
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

To use Viam software with your smart machine, install and run the `viam-server` binary on the single board computer (SBC) or other computer that will run your smart machine and is connected to your hardware.
Installing on a laptop or desktop computer is useful if you don't have an SBC available, or if you want to run a Viam [service](/services/) with your robot that requires more computing resources than are otherwise available on an SBC.

{{< alert title="Compatibility" color="note" >}}

`viam-server` supports:

- Linux 64-bit operating systems running on the `aarch64` or `x86_64` architectures
- macOS

{{< /alert >}}

For an overview of the Viam software platform, see [Viam in 3 minutes](/viam/).

## Prepare your board

If you are using one of the following boards, click on the card to follow the guide for that board:

{{< cards >}}
{{% card link="/installation/prepare/rpi-setup/" class="small" %}}
{{% card link="/installation/prepare/beaglebone-setup/" class="small" %}}
{{% card link="/installation/prepare/sk-tda4vm/" class="small" %}}
{{% card link="/installation/prepare/jetson-nano-setup/" class="small" %}}
{{% card link="/installation/prepare/jetson-agx-orin-setup/" class="small" %}}
{{% card link="/installation/prepare/pumpkin/" class="small" %}}
{{< /cards >}}

<br>

Viam also provides a lightweight version of `viam-server` which can run on resource-limited embedded systems that cannot run the fully-featured Robot Development Kit (RDK).
If you are using a microcontroller, prepare your board using the following guide:

{{< cards >}}
{{% card link="/installation/prepare/microcontrollers" class="small" %}}
{{< /cards >}}

<br>

Other SBCs such as the [RockPi S](https://wiki.radxa.com/RockpiS) and [Orange Pi Zero 2](https://orangepi.com/index.php?route=product/product&path=237&product_id=849) can run Viam with an experimental [periph.io](https://periph.io/) based [modular component](https://github.com/viam-labs/periph_board).

## Install `viam-server`

If you have a [compatible operating system](/installation/), follow along with the steps outlined below or with the video beneath it to install `viam-server`:

{{< tabs name="Install on computer" >}}
{{% tab name="Linux computer" %}}

{{< readfile "/static/include/install/install-linux.md" >}}

{{% /tab %}}
{{% tab name="macOS computer" %}}

`viam-server` is available for macOS users through [Homebrew](https://brew.sh/), and supports both Intel and Apple Silicon macOS computers.
To install `viam-server` on a macOS computer:

1. Go to the [Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots/#add-a-new-robot).
   If this is your first time using the Viam app, you must create an account first.

1. On the **Setup** tab, select `Mac` as the **Architecture**.

1. Follow the steps shown on the **Setup** tab to install `viam-server` on your macOS computer.

1. Once `viam-server` is installed and running, return to the **Setup** page on the [Viam app](https://app.viam.com) and wait for confirmation that your computer has successfully connected.

{{% /tab %}}
{{< /tabs >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/gmIW9JoWStA">}}

## Next Steps

{{< cards >}}
{{% card link="/manage/configuration/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/try-viam/" %}}
{{< /cards >}}
