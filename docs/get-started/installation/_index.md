---
title: "Installation Guide"
linkTitle: "Installation Guide"
childTitleEndOverwrite: "Try Viam"
weight: 100
no_list: true
type: docs
images: ["/get-started/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
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

`viam-server` is the binary built from [Robot Development Kit](https://github.com/viamrobotics/rdk) that contains and manages communications between all Viam's built-in hardware drivers ({{< glossary_tooltip term_id="component" text="components" >}}) and software {{< glossary_tooltip term_id="service" text="services" >}}, connects your machine to the cloud, manages machine configuration, and manages dependencies including {{< glossary_tooltip term_id="module" text="modules" >}}.

To use Viam software with your machine, install and run `viam-server` on the single-board computer (SBC) or other computer that will run your machine and is connected to your hardware.
Installing on a laptop or desktop computer is useful if you don't have an SBC available, or if you want to run a Viam [service](/services/) with your machine that requires more computing resources than are otherwise available on an SBC.

For an overview of the Viam software platform, see [Viam in 3 minutes](/get-started/viam/).

## Compatibility

`viam-server` supports:

- Linux 64-bit operating systems running on the `aarch64` or `x86_64` architectures
- Windows Subsystem for Linux (WSL)
- macOS

{{< readfile "/static/include/install/windows-support.md" >}}

## Prepare your board

If you are using one of the following boards, click on the card to follow the guide for that board:

{{< cards >}}
{{% card link="/get-started/prepare/rpi-setup/" class="small" %}}
{{% card link="/get-started/prepare/odroid-c4-setup/" class="small" %}}
{{% card link="/get-started/prepare/orange-pi-3-lts/" class="small" %}}
{{% card link="/get-started/prepare/orange-pi-zero2/" class="small" %}}
{{% card link="/get-started/prepare/beaglebone-setup/" class="small" %}}
{{% card link="/get-started/prepare/jetson-agx-orin-setup/" class="small" %}}
{{% card link="/get-started/prepare/jetson-nano-setup/" class="small" %}}
{{% card link="/get-started/prepare/pumpkin/" class="small" %}}
{{% card link="/get-started/prepare/sk-tda4vm/" class="small" %}}
{{< /cards >}}

Viam also provides a lightweight version of `viam-server` which can run on resource-limited embedded systems that cannot run the fully-featured Robot Development Kit (RDK).
If you are using a microcontroller, prepare your board using the following guide:

{{< cards >}}
{{% card link="/get-started/installation/microcontrollers" class="small" %}}
{{< /cards >}}

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

1. Go to the [Viam app](https://app.viam.com). Create an account if you haven't already.

1. Add a new machine by providing a name in the **New machine** field and clicking **Add machine**:

   ![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

1. Navigate to the **CONFIGURE** tab and find your machine's card.
   An alert will be present directing you to **Set up your machine part**:

   ![Machine setup alert in a newly created machine](/get-started/installation/setup-part.png)

   Click **View setup instructions** to open the setup instructions.

1. Select **Mac** as your system's OS and **RDK** as your RDK type.

1. Follow the steps shown to install `viam-server` on your macOS computer.

1. Once you have followed the steps on the setup instructions, `viam-server` is installed and running.
   Wait for confirmation that your computer has successfully connected.

{{% /tab %}}
{{% tab name="Windows" %}}

1. Go to the [Viam app](https://app.viam.com).
   Create an account if you haven't already.

1. Add a new machine by providing a name in the **New machine** field and clicking **Add machine**:

   ![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

1. Navigate to the **CONFIGURE** tab and find your machine's card.
   An alert will be present directing you to **Set up your machine part**:

   ![Machine setup alert in a newly-created machine](/get-started/installation/setup-part.png)

   Click **View setup instructions** to open the setup instructions:

   ![Setup instructions](/get-started/installation/wsl-setup-instructions.png)

1. Select **Windows** as your system's OS and **RDK** as your RDK type.

1. Follow the steps shown to install `viam-server` on your Windows machine.

1. Once you have followed the steps on the setup instructions, `viam-server` is installed and running.
   Wait for confirmation that your computer has successfully connected.

{{% /tab %}}
{{< /tabs >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/gmIW9JoWStA">}}

### Manage `viam-server`

To learn how to run, update, or uninstall `viam-server`, see [Manage `viam-server`](/get-started/installation/manage/).

## Next steps

{{< cards >}}
{{% card link="/build/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/build/program/" %}}
{{< /cards >}}
