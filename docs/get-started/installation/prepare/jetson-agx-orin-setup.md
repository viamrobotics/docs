---
title: "NVIDIA Jetson AGX Orin Setup Guide"
linkTitle: "Jetson AGX Orin Setup"
weight: 20
type: "docs"
image: "/get-started/installation/thumbnails/jetson-agx-orin-dev-kit.png"
imageAlt: "Jetson A G X Orin Developer Kit"
images: ["/get-started/installation/thumbnails/jetson-agx-orin-dev-kit.png"]
description: "Set up the Jetson AGX Orin Developer Kit to prepare your NVIDIA Jetson AGX Orin for viam-server installation."
no_list: true
aliases:
  - /installation/prepare/jetson-agx-orin-setup/
# SMEs: Pete Garafano
---

<div class="td-max-width-on-larger-screens text-center">
{{<imgproc src="get-started/installation/thumbnails/jetson-agx-orin-dev-kit.png" alt="The grey and chunky front of the NVIDIA Jetson AGX Orin single-board computer development kit." resize="200x" declaredimensions=true >}}
</div>

The [Jetson AGX Orin](https://developer.nvidia.com/embedded/jetson-orin) from [NVIDIA](https://www.nvidia.com/) is a single-board computer that supports modern AI workloads and application development.
Follow this guide to set up the [Jetson AGX Orin Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-agx-orin-devkit) to prepare your NVIDIA Jetson AGX Orin for `viam-server` installation.

<div style="clear:both;"><br /></div>

{{< alert title="Important" color="note" >}}

This guide assumes that you have a Jetson AGX Orin Developer Kit with a Jetson AGX Orin module and reference carrier board.
If you want to use a different carrier board to incorporate your Orin into your machine, the type of carrier board you use will affect your hardware requirements.

{{% /alert %}}

{{% alert title="CAUTION: Use 3.3V inputs and outputs" color="caution" %}}

The GPIO pins on Jetson boards are rated 3.3V signals. 5V signals from encoders and sensors can cause damage to a pin. We recommend selecting hardware that can operate 3.3V signals or lower.
For details, see your boards specification.

{{% /alert %}}

## Hardware Requirements

You need the following hardware, tools, and software to install `viam-server` on a Jetson AGX Orin with the Jetson AGX Orin Developer Kit:

**Initial Setup with Display Attached:**

1. A [Jetson AGX Orin Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-agx-orin-devkit)
2. A PC monitor (HDMI or DisplayPort)
3. USB keyboard and mouse
4. A DisplayPort to HDMI adapter/cable, to connect the Orin to the monitor
5. USB Type-C power supply, to power the Orin (included with the AGX Orin Developer Kit)
6. (Optional) Ethernet cable, to connect the Orin to the internet without Wifi access

**Initial Setup in Headless Mode:**

1. A [Jetson AGX Orin Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-agx-orin-devkit)
2. An internet-connected Windows, Linux, or macOS computer
3. A way to connect the computer to the Orin (for example, the USB Type-A to USB Type-C Cable included with the AGX Orin Developer Kit)

   (Optional) If your computer doesn't have a USB Type-A port, you may need to attach a [USB-C hub](https://toomanyadapters.com/best-usb-hubs/) or similar device to your computer to connect to the Orin

4. USB Type-C power supply, to power the Orin (included with the AGX Orin Developer Kit)
5. (Optional) Ethernet cable, to connect the Orin to the internet without Wifi access

## Jetson Orin Setup Guide

Follow the instructions in [Getting Started with Jetson AGX Orin Developer Kit](https://developer.nvidia.com/embedded/learn/get-started-jetson-agx-orin-devkit) to boot up your Orin for the first time.

If you have already booted up your Orin, start with "Step 2 - Install JetPack Components" to make sure you have installed the latest NVIDIA JetPack components.

Look at the Troubleshooting section below for help navigating these instructions.
Once you have reached _Next Steps_, return to the Viam docs.

{{< alert title="Tip: <code>viam-server</code> installation with <code>curl</code>" color="tip" >}}

If `curl` is not installed on your Orin, run `sudo apt install curl` before downloading the `viam-server` binary.

If this command fails, try using `wget https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-latest-aarch64.AppImage` to download the `viam-server` binary.

{{% /alert %}}

## Install `viam-server`

{{< readfile "/static/include/install/install-linux-aarch.md" >}}

## Camera Setup

1. Install E-Con Systems [e-CAM20_CUOAGX](https://www.e-consystems.com/nvidia-cameras/jetson-agx-orin-cameras/full-hd-ar0234-color-global-shutter-camera.asp) AR0234 driver.
   Consult the instructions you received when purchasing your device for more information.
2. Ensure the driver has successfully installed by running `sudo dmesg | grep ar0234`. The output should include `ar0234 Detected Ar0234 sensor`.
3. Connect the AR0234 camera module and daughterboard to the J509 port located at the bottom of the Developer Kit.
4. Configure the camera as a [webcam](/components/camera/webcam/).

## Serial Communication Protocol Tips

To change the pins that are in use for modes of serial communication, launch <file>jetson-io.py</file> with the following commands:

```sh { class="command-line" data-prompt="$"}
cd ~
sudo /opt/nvidia/jetson-io/jetson-io.py
```

In the interactive menu that opens, select **Configure Jetson 40 Pin Header** and **Configure header pins manually** to select and deselect pins to enable use.
For a Jetson AGX Orin, reference the following:

<!-- prettier-ignore -->
| Data Sheet ID | GPIO Header Pin | Viam Bus ID | `jetson-io.py` ID | `/dev` Path ID | Notes |
| ------------- | --------------- | ----------- | ----------------- | ----------- | ----- |
| I2C_GP2_DAT, I2C_GP2_CLK | 3, 5 | `7` | `i2c2` | `/dev/i2c-2` | |
| I2C_GP5_DAT, I2C_GP5_CLK | 27, 28 | `1` | `i2c8` | `/dev/i2c-8` | |
| SPI1_DOUT, SPI1_DIN, SPI1_SCK, SPI1_CS0, SPI1_CS1 | 19, 21, 23, 24, 26 | `0` | `spi1` | `/dev/spidev0.0`, `/dev/spidev0.1` | Must be enabled to use SPI bus, must add `spidev` to `/etc/modules` |

Note that I2C buses do not need to be configured through <file>jetson-io.py</file>.
See NVIDIA's documentation on [Configuring the Jetson Expansion Headers](https://docs.nvidia.com/jetson/archives/r35.1/DeveloperGuide/text/HR/ConfiguringTheJetsonExpansionHeaders.html) for more information.

## Next Steps

{{< cards >}}
{{% card link="/build/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/build/program/" %}}
{{< /cards >}}

## Troubleshooting

- NVIDIA Step 1 - Run through Ubuntu Setup (oem config)

  - Headless Mode Tips:
    - Once you reach **step e** which instructs you to connect through the host serial port, the instructions to connect are immediately under **step e**.
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
- If you do not see an interactive menu after launching <file>jetson-io.py</file>, try resizing your window to a large size.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
