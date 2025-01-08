---
linkTitle: "Start a new machine"
title: "Start a new machine"
weight: 10
layout: "docs"
type: "docs"
no_list: false
description: "Install the software that drives hardware and connects your device to the cloud."
aliases:
  - /installation/microcontrollers/
  - /installation/prepare/microcontrollers/
  - /installation/prepare/microcontrollers/
  - /build/micro-rdk/
  - /get-started/installation/microcontrollers/
  - /installation/viam-micro-server-setup/
  - /installation/viam-server-setup/
  - /how-tos/configure/
  - /cloud/account/
---

Get started by installing the open-source software that drives your hardware and connects your device to the cloud.
The easiest way to do this is through the Viam app, so that your machines are automatically connected to configuration and remote operation tools.

## Quickstart

{{< expand "Prerequisite: Operating system setup" >}}
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

1. Create a [Viam app](https://app.viam.com) account.
   The Viam app is the online hub for configuring and managing devices as well as viewing data.
1. Add a new _{{< glossary_tooltip term_id="machine" text="machine" >}}_ in the app.
   A machine represents your device.
1. From your machine's page in the Viam app, follow the setup instructions to install `viam-server` or `viam-micro-server` on your device and connect it to the cloud.
   [`viam-server`](/operate/reference/viam-server/) is the executable binary that runs on your device and manages hardware drivers, software, and data capture and sync.
   [`viam-micro-server`](/operate/reference/viam-micro-server/) is the lightweight version of `viam-server` for microcontrollers.
1. Use the **+** button on your machine's **CONFIGURE** tab to add [supported hardware components](/operate/get-started/supported-hardware/) so that `viam-server` can control your specific hardware.
1. Use this same **+** button to configure software services such as [data capture and sync](/data-ai/capture-data/capture-sync/).

As soon as you configure each component and save the configuration, you can use the **TEST** panel of the component's config card to, for example, view your camera's stream or turn your motor.

## Concepts

### What is a machine?

A _machine_ is a computer (often a single-board computer like a Raspberry Pi or Jetson) or microcontroller and all the hardware attached to it, as well as the software running on it.
You can think of one machine as representing one device, or one robot.

When you create a new machine in the Viam app, Viam generates a unique set of credentials for that machine that connect the physical machine to its instance in the Viam app.

### Installation methods: `viam-agent` versus manual

`viam-agent` is a service manager that automatically updates `viam-server` and includes tools for [provisioning your devices](/manage/fleet/provision/setup/) and configuring operating system updates.

When you set up a Linux device in the Viam app, you'll see an option to install using `viam-agent`, or to manually install only `viam-server`.
Using `viam-agent` is generally recommended when installing `viam-server` on a single-board computer.

`viam-agent` is not available for macOS, Windows Subsystem for Linux (WSL), or microcontrollers, so use manual install for those systems.

### How the configuration works

The machine setup steps displayed in the Viam app copy your machine's credentials to your machine.
When you turn on your machine, `viam-server` starts up and uses the provided credentials to fetch its configuration from the Viam app.
Once the machine has a configuration, it caches it locally and can use the config for up to 60 days.
Since the configuration is cached locally, your machine does not need to stay connected to the Viam app after it has obtained its configuration file.

If it is online, the machine checks for new configurations every 15 seconds and changes its config automatically when a new config is available.
All communication happens securely over HTTPS using secret tokens that are in the machine's config.

If your machine will never connect to the internet, you can also create a [local configuration file](/operate/reference/viam-server/local-configuration-file/) on the machine itself.

### Manage your installation

On Linux installs, by default `viam-server` or `viam-agent` and `viam-server` will start automatically when your system boots.
On macOS installs, `viam-server` does not start automatically on boot.
You can change this behavior if desired.

To learn how to run, update, or uninstall `viam-agent`, see [Manage `viam-agent`](/manage/reference/viam-agent/manage-viam-agent/).

For manual installs of only `viam-server`, see [Manage `viam-server`](/operate/reference/viam-server/manage-viam-server/).

## Supported systems

Viam can run on any computer that runs one of the following operating systems:

- Linux 64-bit operating systems running on AArch64 (ARM64) or x86-64 architectures
- macOS

Viam also offers a lightweight binary to support the following 32-bit microcontrollers:

- [ESP32-WROVER Series](https://www.espressif.com/en/products/modules/esp32)
- [ESP32-WROOM Series](https://www.espressif.com/en/products/modules/esp32) (until v0.1.7)

ESP32 microcontrollers must have at least 2 cores, 384kB SRAM, 2MB PSRAM and 4MB flash to work with Viam.

Viam can run on Windows Subsystem for Linux (WSL), but WSL itself does not currently support exposing many types of Windows hardware to the embedded Linux kernel.
This means that some hardware, such as a connected webcam, may not be available to `viam-server` with WSL, even though it is fully supported for native Linux systems.
