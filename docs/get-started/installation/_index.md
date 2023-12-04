---
title: "Installation Guide"
linkTitle: "Installation Guide"
childTitleEndOverwrite: "Try Viam"
weight: 100
no_list: true
type: docs
image: "/get-started/installation/thumbnails/install.png"
imageAlt: "Install Viam"
images: ["/get-started/installation/thumbnails/install.png"]
description: "To use Viam software with your machine, install and run the viam-server binary on the computer that will run your machine and is connected to your hardware."
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
  - /installation/
---

To use Viam software with your machine, install and run the `viam-server` binary on the single board computer (SBC) or other computer that will run your machine and is connected to your hardware.
Installing on a laptop or desktop computer is useful if you don't have an SBC available, or if you want to run a Viam [service](/services/) with your robot that requires more computing resources than are otherwise available on an SBC.

{{< alert title="Compatibility" color="note" >}}

`viam-server` supports:

- Linux 64-bit operating systems running on the `aarch64` or `x86_64` architectures
- macOS

{{< /alert >}}

For an overview of the Viam software platform, see [Viam in 3 minutes](/get-started/viam/).

## Prepare your board

If you are using one of the following boards, click on the card to follow the guide for that board:

{{< cards >}}
{{% card link="/get-started/installation/prepare/rpi-setup/" class="small" %}}
{{% card link="/get-started/installation/prepare/beaglebone-setup/" class="small" %}}
{{% card link="/get-started/installation/prepare/sk-tda4vm/" class="small" %}}
{{% card link="/get-started/installation/prepare/jetson-nano-setup/" class="small" %}}
{{% card link="/get-started/installation/prepare/jetson-agx-orin-setup/" class="small" %}}
{{% card link="/get-started/installation/prepare/pumpkin/" class="small" %}}
{{< /cards >}}

<br>

Viam also provides a lightweight version of `viam-server` which can run on resource-limited embedded systems that cannot run the fully-featured Robot Development Kit (RDK).
If you are using a microcontroller, prepare your board using the following guide:

{{< cards >}}
{{% card link="/get-started/installation/prepare/microcontrollers" class="small" %}}
{{< /cards >}}

<br>

Other SBCs such as the [RockPi S](https://wiki.radxa.com/RockpiS) and [Orange Pi Zero 2](https://orangepi.com/index.php?route=product/product&path=237&product_id=849) can run Viam with an experimental [periph.io](https://periph.io/) based [modular component](https://github.com/viam-labs/periph_board).

## Install `viam-server`

If you have a [compatible operating system](/get-started/installation/), follow along with the steps outlined below or with the video beneath it to install `viam-server`:

{{< tabs name="Install on computer" >}}
{{% tab name="Linux computer" %}}

{{< readfile "/static/include/install/install-linux.md" >}}

{{% /tab %}}
{{% tab name="macOS computer" %}}

`viam-server` is available for macOS users through Homebrew, and supports both Intel and Apple Silicon macOS computers.
To install `viam-server` on a macOS computer:

1. If not installed already, install [Homebrew](https://brew.sh/).

1. Go to the [Viam app](https://app.viam.com) and add a new robot by providing a name in the **New Robot** field and clicking **Add robot**.
   If this is your first time using the Viam app, you must create an account first.

   ![The 'First Location' page on the Viam app with a new robot name in the New Robot field and the Add robot button next to the field highlighted.](/fleet/app-usage/create-robot.png)

1. On the **Setup** tab, select `Mac` as the **Architecture**.

1. Follow the steps shown on the **Setup** tab to install `viam-server` on your macOS computer.

1. Once you have followed the steps on the **Setup** tab, `viam-server` is installed and running.
   Return to the **Setup** page on the Viam app and wait for confirmation that your computer has successfully connected.

{{% /tab %}}
{{< /tabs >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/gmIW9JoWStA">}}

### Manage `viam-server`

To learn how to run, update, or uninstall `viam-server`, see [Manage `viam-server`](/get-started/installation/manage/).

## Next Steps

{{< cards >}}
{{% card link="/build/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/build/program/" %}}
{{< /cards >}}
