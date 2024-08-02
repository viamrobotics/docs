---
title: "Orange Pi 3 LTS Setup Guide"
linkTitle: "Orange Pi 3 LTS Setup"
weight: 16
type: "docs"
description: "Image an Orange Pi 3 LTS to prepare it for viam-server installation."
images: ["/installation/thumbnails/orange-pi-3-LTS.png"]
imageAlt: "Orange Pi 3 LTS"
no_list: true
aliases:
  - /get-started/installation/prepare/orange-pi-3-lts/
  - /get-started/prepare/orange-pi-3-lts/
# SME: Olivia Miller
---

The [Orange Pi 3 LTS](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/Orange-Pi-Zero-2.html) is a highly compact, open-source single-board computer equipped with dual-band WiFi and Bluetooth 5.0.
It can run Ubuntu, Android10, or Debian distributions.

{{<imgproc src="installation/thumbnails/orange-pi-3-LTS.png" alt="The Orange Pi 3 LTS single-board computer." resize="350x" declaredimensions=true >}}

Follow this guide to set up your Orange Pi 3 LTS to run `viam-server`.

## Hardware requirements

- Development machine: laptop or computer workstation
- An [Orange Pi 3 LTS](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/orange-pi-3-LTS.html)
- A 5V 3A power supply with a USB-C connector
- A micro-SD card (TF card): Minimum of 8GB, 16GB recommended
- [SD card reader](https://www.amazon.com/Reader-Beikell-Connector-Memory-Adapter/dp/B0BGNZGDTC/) (recommended with USB-C connector)
- A monitor: for display
- [HDMI cable](https://www.amazon.com/Highwings-Braided-Cord-Supports-ARC-Compatible-Ethernet/dp/B07TDH11BJ/): to connect Orange Pi to monitor display
- USB keyboard and mouse
- [USB-C to USB-A cables](https://www.amazon.com/Anker-2-Pack-Premium-Samsung-Galaxy/dp/B07DD5YHMH/): to connect keyboard and mouse to USB hub or Orange Pi ports (recommended, hardware dependent)
- [USB hub](https://www.amazon.com/BYEASY-Extended-Portable-Splitter-MacBook/dp/B07TVH9NHP/) with USB-A connector (recommended)

## Power your Orange Pi 3 LTS

Before you power the board, you need to install an operating system.

1. First, download an [Orange Pi 3 LTS Ubuntu image](https://drive.google.com/drive/folders/1KzyzyByev-fpZat7yvgYz1omOqFFqt1k) to your development machine.
   We recommend `ubuntu_jammy_desktop`.
1. Unzip the image.
1. Insert the micro-SD card into the SD card reader and connect the reader to your development machine.
1. Follow the [Orange Pi guide to prepare your microSD card](https://sbc-community.org/docs/general_guides/prepare_sd_card/) to flash the OS to your micro-SD card using [balenaEtcher](https://etcher.balena.io/).
1. Insert the micro-SD into the Orange Pi.

To power your Orange Pi 3 LTS, connect your power adapter to the LTS's USB-C port.
The LED should light up, which indicates that the board is powered.

{{% alert title="Tip" color="tip" %}}
If your board's LED does not light up when powered, try re-flashing your micro-SD card with the `ubuntu_jammy_desktop` image or using a different micro-SD card.
The Orange Pi will only power on with a compatible operating system installed.
{{% /alert %}}

To connect to a display, connect the HDMI cable to the Orange Pi's HDMI port and the other end to your monitor.
Then, connect your keyboard and mouse to the two USB-A ports on your Orange Pi.
Alternatively, you can connect your peripherals to a USB hub and connect the USB hub to your Orange Pi's USB-A port.

{{% alert title="Tip" color="tip" %}}
For board schematics, consult the [Orange Pi 3 LTS documentation](http://www.orangepi.org/html/hardWare/computerAndMicrocontrollers/details/orange-pi-3-LTS.html).
{{% /alert %}}

Once the Orange Pi successfully boots, you should be greeted with the Orange Pi desktop display.
If you are prompted for a login password, note that the default password for Orange Pi devices is "orangepi".

## Establish a network connection

The Orange Pi 3 LTS comes equipped with a wireless network antenna.
To connect to WiFi through the desktop, click on the WiFi icon in the top right of the monitor display, select your preferred network or hotspot, and enter the password.

{{% alert title="Tip" color="tip" %}}
You can also connect to WiFi while connected to the Orange Pi on the terminal with several different methods, including the `nmcli` tool.
For more information, consult the [official user manual](https://drive.google.com/file/d/1jka7avWnzNeTIQFkk78LoJdygWaGH2iu/view) (page 80).
{{% /alert %}}

## Install `viam-server`

Launch the browser on your Orange Pi display by selecting **Applications** from the left-hand menu, then **Internet**, then **Firefox Web Browser**.

Also, launch the terminal by selecting **Applications** and **Terminal**.
Complete the following instructions to install `viam-server`, noting that if you are prompted for a password in the terminal, the default password for Orange Pis is "orangepi".

{{< readfile "/static/include/install/install-linux-aarch.md" >}}

## Next steps

[Configure an `orangepi` board as a component](/components/board/orangepi/) to integrate the GPIO pins of the single-board computer into your smart machine.

## Troubleshooting

Visit the [Orange Pi Forum](http://www.orangepi.org/orangepibbsen/) for troubleshooting tips and tricks specific to the Orange Pi.
