---
title: "Odroid C4 Setup Guide"
linkTitle: "Odroid C4 Setup"
weight: 15
type: "docs"
description: "Image a Odroid C4 to prepare it for viam-server installation."
images: ["/get-started/installation/thumbnails/odroid-c4.png"]
imageAlt: "Odroid C4"
no_list: true
# SME:
---

The [Odroid C4](https://wiki.odroid.com/start) is a single-board computer that features an Amlogic S905x3 CPU and runs a variety of Linux or Android distributions.

{{<imgproc src="get-started/installation/thumbnails/odroid-c4.png" alt="The Odroid C4 single board computer." resize="350x" declaredimensions=true >}}

Follow this guide to set up your Odroid C4.

## Hardware requirements

- An [Odroid C4 board](https://www.hardkernel.com/shop/odroid-c4/)
- A 12V/2A power supply
- An ethernet cable and/or USB Wi-Fi dongle, for network connectivity
- A computer, for development
- A microSD card, if you plan to boot from SD instead of eMMC
- (Optional) An HDMI cable, for display

## Power your Odroid C4

Before you power the board, you need to install an operating system.
Visit [Odroid's OS Installation Guide](https://wiki.odroid.com/getting_started/os_installation_guide#os_installation_guide) to choose the right OS for your needs and follow the instructions to flash the OS to your microSD card or eMMC.

To power your Odroid C4, connect your power adapter to the Odroid C4's power jack.
The red LED should light up, which indicates that the board is powered.

To connect to a display, connect one end of your HDMI cable to the Odroid and the other end to your monitor.

## Establish a network connection

Plug the Ethernet cable into your Odroid C4for a wired internet connection.
For a wireless connection, you can connect a USB Wi-Fi dongle and configure Wi-Fi settings through your operating system.

## Access and update your Odroid C4

To access your Odroid remotely, use an SSH client like [TeraTerm](https://teratermproject.github.io/index-en.html).
You'll also need the IP address of your Odroid C4 board to connect remotely.
Alternatively, connect a keyboard and mouse to interact with the board directly using a connected monitor.

Once you're connected, open a terminal and run the following commands:

```json
sudo apt update && sudo apt upgrade
```

## Install `viam-server`

{{< readfile "/static/include/install/install-linux.md" >}}

## Troubleshooting

Visit the [Odroid Forum](https://forum.odroid.com/index.php) for troubleshooting tips and tricks specific to the Odroid C4.
