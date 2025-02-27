---
linkTitle: "Set up a computer or SBC"
title: "Set up a computer or SBC"
weight: 20
layout: "docs"
type: "docs"
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
no_list: false
description: "Install the software that drives hardware and connects your device to the cloud."
aliases:
  - /installation/viam-server-setup/
  - /how-tos/configure/
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

Get started by installing [`viam-server`](/operate/reference/viam-server/),the open-source software that drives your hardware and connects your device to the cloud.

{{< expand "Supported systems" >}}

`viam-server` can run on any computer that runs one of the following operating systems:

- Linux 64-bit operating systems running on AArch64 (ARM64) or x86-64 architectures
- macOS
- Windows
  - Native: Use native if you are using a WSL version prior to WSL 2 or need native USB support
  - WSL: Use WSL if you are using Python modules or other Linux dependencies

`viam-server` can run on Windows Subsystem for Linux (WSL), but WSL itself does not currently support exposing many types of Windows hardware to the embedded Linux kernel.
This means that some hardware, such as a connected webcam, may not be available to `viam-server` with WSL, even though it is fully supported for native Linux systems.

For 32-bit systems, see [Set up an ESP32](/operate/get-started/setup-micro/).

{{< /expand >}}

## Install `viam-server` and connect your machine to the cloud

Install `viam-server` on the computer or single-board computer (SBC) that is directly connected to your hardware (for example sensors, cameras, or motors).

{{< expand "Prerequisite: Install a compatible operating system" >}}
If you're using Viam with a single-board computer that does not yet have a 64-bit Linux operating system installed, start by flashing an OS.
For convenience, we provide operating system installation instructions for some popular SBCs.
If your SBC or other computer already has a supported operating system installed, you can skip this step.

{{< cards >}}
{{% card link="/operate/reference/prepare/rpi-setup/" class="small" %}}
{{% card link="/operate/reference/prepare/odroid-c4-setup/" class="small" %}}
{{% card link="/operate/reference/prepare/orange-pi-3-lts/" class="small" %}}
{{% card link="/operate/reference/prepare/orange-pi-zero2/" class="small" %}}
{{% card link="/operate/reference/prepare/beaglebone-setup/" class="small" %}}
{{% card link="/operate/reference/prepare/jetson-agx-orin-setup/" class="small" %}}
{{% card link="/operate/reference/prepare/jetson-nano-setup/" class="small" %}}
{{% card link="/operate/reference/prepare/pumpkin/" class="small" %}}
{{% card link="/operate/reference/prepare/sk-tda4vm/" class="small" %}}
{{< /cards >}}

{{< /expand >}}

1. Make sure your computer or SBC is powered on and connected to the internet.

1. Create a [Viam app](https://app.viam.com) account.
   The Viam app is the online hub for configuring and managing devices and data.

1. Add a new _{{< glossary_tooltip term_id="machine" text="machine" >}}_ using the button in the top right corner of the **LOCATIONS** tab in the app.
   A machine represents your device.

1. From your machine's page in the Viam app, follow the setup instructions to install `viam-server` on your device and connect it to the cloud.

1. A secure connection is automatically established between your machine and the Viam app.
   When you update your machine's configuration, `viam-server` automatically gets the updates.

   [You are ready to configure your machine's hardware ->](/operate/get-started/supported-hardware/)

## The details

### How the configuration works

The machine setup steps displayed in the Viam app copy your machine's credentials to your machine.
When you turn on your machine, `viam-server` starts up and uses the provided credentials to fetch its configuration from the Viam app.
Once the machine has a configuration, it caches it locally and can use the config for up to 60 days.
Since the configuration is cached locally, your machine does not need to stay connected to the Viam app after it has obtained its configuration file.

If it is online, the machine checks for new configurations every 15 seconds and changes its config automatically when a new config is available.
All communication happens securely over HTTPS using secret tokens that are in the machine's config.

If your machine will never connect to the internet, you can also create a [local configuration file](/operate/reference/viam-server/local-configuration-file/) on the machine itself.

### Installation methods: `viam-agent` versus manual

`viam-agent` is a service manager that automatically updates `viam-server` and includes tools for [provisioning your devices](/manage/fleet/provision/setup/), networking, and configuring operating system settings.

When you set up a Linux device in the Viam app, you'll see an option to install using `viam-agent`, or to manually install only `viam-server`.
Using `viam-agent` is generally recommended when installing `viam-server` on a single-board computer.

When you set up a native Windows device in the Viam app, you must use the [Viam Agent installer](https://storage.googleapis.com/packages.viam.com/apps/viam-agent/viam-agent-stable.msi).

`viam-agent` is not available for macOS, Windows Subsystem for Linux (WSL), or microcontrollers.
Instead use manual install for those systems.

### Manage your installation

On Linux installs, by default `viam-server` or `viam-agent` and `viam-server` will start automatically when your system boots.
On macOS installs, `viam-server` does not start automatically on boot.
You can change this behavior if desired.

To learn how to run, update, or uninstall `viam-agent`, see [Manage `viam-agent`](/manage/reference/viam-agent/manage-viam-agent/).

For manual installs of only `viam-server`, see [Manage `viam-server`](/operate/reference/viam-server/manage-viam-server/).
