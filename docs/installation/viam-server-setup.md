---
title: "viam-server Installation Guide"
linkTitle: "viam-server setup"
weight: 9
no_list: true
type: docs
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
description: "To use Viam, install and run viam-server on the computer that will run your machine and is connected to your hardware."
date: "2024-08-19"
# updated: ""  # When the content was last entirely checked
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
  - /get-started/installation/
---

To use Viam, you need to install either the `viam-server` binary or `viam-micro-server`.

[`viam-server`](/architecture/rdk/) is the binary built from the [Robot Development Kit](https://github.com/viamrobotics/rdk) that contains and manages communications between all Viam's built-in hardware drivers ({{< glossary_tooltip term_id="component" text="components" >}}) and software {{< glossary_tooltip term_id="service" text="services" >}}, connects your machine to the cloud, manages machine configuration, and manages dependencies including {{< glossary_tooltip term_id="module" text="modules" >}}.

`viam-micro-server` is a lightweight version of `viam-server` which can run on resource-limited embedded systems that cannot run the fully-featured `viam-server`.
To install `viam-micro-server`, see [`viam-micro-server` Installation Guide](/installation/viam-micro-server-setup/) instead.

For an overview of the Viam software platform, see [Learn about Viam](/get-started/).

{{< alert title="In this page" color="note" >}}
{{% toc %}}
{{< /alert >}}

## Platform requirements

`viam-server` can run on any computer that runs a supported operating system:

- Linux 64-bit operating systems running on the `aarch64` or `x86_64` architectures
- Windows Subsystem for Linux (WSL)
- macOS

{{% alert title="Windows Support Notice" color="note" %}}

WSL itself does not currently support exposing many types of Windows hardware to the embedded Linux kernel.
This means that some hardware, such as a connected webcam, may not be available to `viam-server` with WSL, even though it is fully supported for native Linux systems.

Although you cannot access all hardware if you run `viam-server` on your personal computer with WSL, you can [run code to control a machine](/sdks/#run-code) on your personal computer with WSL if you install `viam-server` on a single-board computer running Linux.

{{% /alert %}}

### Operating System installation

`viam-server` can run on **any computer that runs on a [supported platform](#platform-requirements)**, including single-board computers (SBCs) running 64-bit Linux.

For convenience, we provide operating system installation instructions for some popular SBCs.
If you want to use an SBC or other computer which already has a supported operating system installed, proceed to [install `viam-server`](/installation/viam-server-setup/#install-viam-server).

{{< cards >}}
{{% card link="/installation/prepare/rpi-setup/" class="small" %}}
{{% card link="/installation/prepare/odroid-c4-setup/" class="small" %}}
{{% card link="/installation/prepare/orange-pi-3-lts/" class="small" %}}
{{% card link="/installation/prepare/orange-pi-zero2/" class="small" %}}
{{% card link="/installation/prepare/beaglebone-setup/" class="small" %}}
{{% card link="/installation/prepare/jetson-agx-orin-setup/" class="small" %}}
{{% card link="/installation/prepare/jetson-nano-setup/" class="small" %}}
{{% card link="/installation/prepare/pumpkin/" class="small" %}}
{{% card link="/installation/prepare/sk-tda4vm/" class="small" %}}
{{< /cards >}}

## Install `viam-server`

If you have a [compatible operating system](#platform-requirements), follow along with the steps outlined below to install `viam-server`:

1. Go to the [Viam app](https://app.viam.com). Create an account if you haven't already.

1. Add a new machine by providing a name in the **New machine** field and clicking **Add machine**:

   ![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

1. Navigate to the **CONFIGURE** tab and find your machine's card.
   An alert will be present directing you to **Set up your machine part**:

   ![Machine setup alert in a newly created machine](/installation/setup-part.png)

   Click **View setup instructions** to open the setup instructions.

1. Select the platform you want to run on.

1. If you selected **Linux / Aarch 64** or **Linux / x86** also select your installation method:

   - `viam-agent` (recommended): installs viam-agent, which will automatically install (and update) viam-server **and** provide additional functionality such as [provisioning](/fleet/provision/) and operating system update configuration.
   - `manual`: installs only `viam-server` on your machine.

1. Follow the steps shown on the setup page.

1. Once you have followed the steps on the setup instructions, wait for confirmation that your machine has successfully connected.

   On your machine's page on [the Viam app](https://app.viam.com), your machine will show that it's **Live**.

{{< alert title="Linux: Automatic startup" color="note" >}}
On Linux installs, by default `viam-server` or `viam-agent` and `viam-server` will start automatically when your system boots.
You can change this behavior if desired.
If you installed `viam-server` manually see [Manage `viam-server`](/installation/manage-viam-server/).
If you installed `viam-server` through `viam-agent` see [Manage `viam-agent`](/installation/manage-viam-agent/).
{{< /alert >}}

### Manage your installation

To learn how to run, update, or uninstall `viam-agent`, see [Manage `viam-agent`](/installation/manage-viam-agent/).

For manual installs of only `viam-server`, see [Manage `viam-server`](/installation/manage-viam-server/).

### Next steps

{{< cards >}}
{{% card link="/how-tos/configure/" %}}
{{% card link="/how-tos/develop-app/" %}}
{{% card link="/configure/" %}}
{{< /cards >}}
