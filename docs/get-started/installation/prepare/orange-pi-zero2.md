---
title: "Orange Pi Zero2 Setup Guide"
linkTitle: "Orange Pi Zero2 Setup"
weight: 16
type: "docs"
description: "Image an Orange Pi Zero2 to prepare it for viam-server installation."
images: ["/get-started/installation/thumbnails/orange-pi-zero2.png"]
imageAlt: "Orange Pi Zero2"
no_list: true
# SME: Olivia Miller
---

The [Orange Pi Zero2](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-Zero-2.html) is a highly compact open-source single-board computer equipped with dual-band wireless WiFi and Bluetooth 5.0.
It can run Ubuntu, Android10, or Debian distributions.

{{<imgproc src="get-started/installation/thumbnails/orange-pi-zero2.png" alt="The Orange Pi Zero2 single-board computer." resize="350x" declaredimensions=true >}}

Follow this guide to set up your Orange Pi Zero2 to run `viam-server`.

## Hardware requirements

- Development machine: laptop or computer workstation
- An [Orange Pi Zero2](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/service-and-support/Orange-Pi-Zero-2.html)
- A 5V 3amps(3A) power supply with a USB-C connector
- A microSD card: Minimum of 8 GB, 16 GB recommended
- A monitor: for display
- [Micro-HDMI to HDMI cable](https://www.amazon.com/Amazon-Basics-Flexible-Durable-18Gpbs/dp/B07KSDB25X/): to connect Orange Pi to monitor display
- USB keyboard and mouse
- [USB-C to USB-A cables](https://www.amazon.com/Anker-2-Pack-Premium-Samsung-Galaxy/dp/B07DD5YHMH/): to connect keyboard and mouse to USB hub
- [USB hub](https://www.amazon.com/BYEASY-Extended-Portable-Splitter-MacBook/dp/B07TVH9NHP/) with USB-A connector (recommended)
- [SD card reader](https://www.amazon.com/Reader-Beikell-Connector-Memory-Adapter/dp/B0BGNZGDTC/) with USB-C connector (recommended)

## Power your Orange Pi Zero2

Before you power the board, you need to install an operating system.

1. First, download an [Orange Pi Ubuntu image](https://drive.google.com/drive/folders/1ohxfoxWJ0sv8yEHbrXL1Bu2RkBhuCMup) to your development machine.
   We recommend `ubuntu_jammy_desktop`.
1. Insert the micro-SD card into the SD card reader and connect the reader to your development machine.
1. Follow [this guide](https://sbc-community.org/docs/general_guides/prepare_sd_card/) to flash the OS to your microSD card using [balenaEtcher](https://etcher.balena.io/).
1. Insert the micro-SD into the Orange Pi.

To power your Orange Pi Zero2, connect your power adapter to the Zero2's USB-C port.
The LED should light up, which indicates that the board is powered.

{{% alert title="Tip" color="tip" %}}
If your board's LED does not light up when powered, try re-flashing your micro-SD card with the `ubuntu_jammy_desktop` image or using a different micro-SD card.
The OrangePi will only power on with a compatible operating system installed.
{{% /alert %}}

To connect to a display, connect the micro-HDMI end of your HDMI cable to the Orange Pi and the other end to your monitor.
Then, to connect the keyboard and mouse, plug the two devices into your USB hub and connect the USB hub to your Orange Pi's USB-A port.

You should now be greeted with the Orange Pi display.
If it prompts you for a password, note that the default password for Orange Pi devices is "orangepi".

## Establish a network connection

The Orange Pi Zero2 comes equipped with a wireless network antennae.
To connect to WiFi, click on the WiFi icon in the top right of the monitor display, select your preferred network or hotspot, and enter the password.

For more information, consult the [official user guide](https://drive.google.com/drive/folders/1ToDjWZQptABxfiRwaeYW1WzQILM5iwpb).

## Install `viam-server`

Launch the browser on your Orange Pi display by selecting **Applications** from the left-hand menu, then **Internet**, then **Firefox Web Browser**.

Also, launch the terminal by selecting **Applications** and **Terminal**.
Complete the following instructions to install `viam-server`, noting that if you are prompted for a password in the terminal, the default password for Orange Pis is "orangepi".

{{< readfile "/static/include/install/install-linux-aarch.md" >}}

## Troubleshooting

Visit the [Orange Pi Forum](http://www.orangepi.org/orangepibbsen/) for troubleshooting tips and tricks specific to the Orange Pi.
