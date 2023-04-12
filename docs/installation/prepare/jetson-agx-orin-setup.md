---
title: "NVIDIA Jetson AGX Orin Setup Guide"
linkTitle: "Jetson AGX Orin Setup"
weight: 20
type: "docs"
image: "/installation/img/jetson-agx-orin-setup/jetson-agx-orin-dev-kit.png"
imageAlt: "Jetson A G X Orin Developer Kit"
description: "Set up the Jetson AGX Orin Developer Kit to prepare your NVIDIA Jetson AGX Orin for viam-server installation."
# SMEs: Pete Garafano
---

<div class="td-max-width-on-larger-screens">
<img src="../../img/jetson-agx-orin-setup/jetson-agx-orin-dev-kit.png" style="max-width:200px" class="alignright" alt="The grey and chunky front of the NVIDIA Jetson AGX Orin single-board computer development kit."></div>

The [Jetson AGX Orin](https://developer.nvidia.com/embedded/jetson-orin) from [NVIDIA](https://www.nvidia.com/) is a single-board computer that supports modern AI workloads and application development.
Follow this guide to set up the [Jetson AGX Orin Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-agx-orin-devkit) to prepare your NVIDIA Jetson AGX Orin for `viam-server` installation.

<div style="clear:both;"><br /></div>

{{< alert title="Note" color="note" >}}

This board is experimental.
Stability is not guaranteed.
This guide assumes that you have a Jetson AGX Orin Developer Kit with a Jetson AGX Orin module and reference carrier board, but you may want to use a different carrier board to incorporate your Orin into your robot.
If so, the type of carrier board you use will affect your hardware requirements.

{{% /alert %}}

## Hardware Requirements

You need the following hardware, tools, and software to install `viam-server` on a Jetson AGX Orin with the Jetson AGX Orin Developer Kit:

**Initial Setup with Display Attached:**

1. A [Jetson AGX Orin Developer Kit](https://www.arrow.com/en/products/945-13730-0000-000/nvidia)
2. A PC monitor (HDMI or DisplayPort)
3. USB keyboard and mouse
4. A DisplayPort to HDMI adapter/cable, to connect the Orin to the monitor
5. USB Type-C power supply, to power the Orin (included with the AGX Orin Developer Kit)
6. (Optional) Ethernet cable, to connect the Orin to the internet without Wifi access

**Initial Setup in Headless Mode:**

1. A [Jetson AGX Orin Developer Kit](https://www.arrow.com/en/products/945-13730-0000-000/nvidia)
2. An internet-connected Windows, Linux, or Mac computer
3. A way to connect the computer to the Orin (for example, the USB Type-A to USB Type-C Cable included with the AGX Orin Developer Kit)

   (Optional) If your computer doesn't have a USB Type-A port, you may need to attach a [USB-C hub](https://toomanyadapters.com/best-usb-hubs/) or similar device to your computer to connect to the Orin

4. USB Type-C power supply, to power the Orin (included with the AGX Orin Developer Kit)
5. (Optional) Ethernet cable, to connect the Orin to the internet without Wifi access

## Jetson Orin Setup Guide

1. Follow the instructions in [Getting Started with Jetson AGX Orin Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-agx-orin-devkit) to boot up your Orin for the first time.

    If you have already booted up your Orin, start with "Step 2 - Install JetPack Components" to make sure you have installed the latest NVIDIA JetPack components.

    Look at the Troubleshooting section below for help navigating these instructions.
    Once you have reached *Next Steps*, return to the Viam docs.

2. Your Jetson AGX Orin now has a Viam-compatible operating system installed.
    Continue to our [viam-server installation guide](/installation#install-viam-server).
    Note that the Jetson AGX Orin has aarch64 CPU architecture.

{{< alert title="Tip: <code>viam-server</code> installation with <code>curl</code>" color="tip" >}}

If `curl` is not installed on your Orin, run `sudo apt install curl` before downloading the `viam-server` binary.

If this command fails, try using `wget http://packages.viam.com/apps/viam-server/viam-server-latest-aarch64.AppImage` to download the `viam-server` binary.

{{% /alert %}}

## Serial Communication Protocol Tips

| Data Sheet ID | GPIO Header Pin | Viam Bus ID | `jetson-io.py` ID | `/dev` Path ID | Notes |
| ------------- | --------------- | ----------- | ----------------- | ----------- | ----- |
| I2C_GP2_DAT, I2C_GP2_CLK | 3, 5 | `7` | `i2c2` | `/dev/i2c-2` | |
| I2c_GP5_DAT, I2C_GP5_CLK | 27, 28 | `1` | `i2c8` | `/dev/i2c-8` | |
| SPI1_DOUT, SPI1_DIN, SPI1_SCK, SPI1_CS0, SPI1_CS1 | 19, 21, 23, 24, 26 | `0` | `spi1` | `/dev/spidev0.0`, `/dev/spidev0.1` | Must be enabled, must add `spidev` to `/etc/modules` |

## Troubleshooting

- NVIDIA Step 1 - Run through Ubuntu Setup (oem config)
  - Headless Mode Tips:
    - Once you reach **step e** which instructs you to connect through the host host serial port, the instructions to connect are immediately under **step e**.
      Follow those steps according to the type of computer you're using.
    - After running `sudo screen`, note that the `Password` input prompt immediately following refers to your computer's system password.
  - "Jetson Initial configuration" (oem-config) Command Prompt Tips:
    - App Partition: default is fine.
    - Nvomodel mode: default is fine.
    - Chromium install: not necessary, you can skip.
    - Signing into online accounts: not necessary, you can skip.

- NVIDIA Step 2 - Install JetPack Components
  - After running `sudo apt dist-upgrade`, if you are prompted with "Package distributer has shipped an updated version" hit `y` to install the updated version.
  - Do not run `sudo apt install nvidia-jetpack` in your terminal until after `sudo reboot` has completed.
  - If your board is powered off after `sudo reboot` has completed and refuses to turn on, disconnect and reconnect the power cable.
  - It is normal for JetPack installation to take a very long time, up to an hour or more.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
