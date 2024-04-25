---
title: "Odroid C4 Setup Guide"
linkTitle: "Odroid C4 Setup"
weight: 15
type: "docs"
description: "Image a Odroid C4 to prepare it for viam-server installation."
images:
  [
    "/Users/skyleilani/docs/assets/get-started/installation/thumbnails/odroid-c4.png",
  ]
imageAlt: "Odroid C4"
no_list: true
# SME:
---

The [Odroid C4](https://wiki.odroid.com/start)is a single-board computer that features an Amlogic S905x3 CPU and runs a variety of Linux or Android distributions.

{{<imgproc src="get-started/installation/thumbnails/odroid-c4.png" alt="The Odroid C4 single board computer." resize="350x" declaredimensions=true >}}

Follow this guide to set up your Odroid C4.

## Hardware requirements

- An [Odroid C4 board](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- A 12V/2A power supply
- A Micro USB to HDMI cable, for display
- An ethernet cable and/or USB Wi-Fi dongle, for network connectivity
- A computer, for development
- (Optional) A microSD card, if you plan to boot from SD instead of eMMC

## Prepare the microSD card

Before you can use the Odroid C4, you need to install an operating system on a microSD card:

1. Download the latest version of your preferred operating system from the [Odroid website](https://wiki.odroid.com/getting_started/os_installation_guide#downloads) or a trusted source.
1. Download and install [Etcher](https://etcher.balena.io/a).
1. Insert your microSD card into your computer and launch Etcher.
1. Select the OS image file you downloaded.

   {{<imgproc src="get-started/installation/odroidc4-setup/etcher-choose-os.png" alt="The etcher imager with an ubuntu OS image set as the first option." resize="700x" style="min-width: 600px" declaredimensions=true >}}

1. Choose your microSD card as the target.

   {{<imgproc src="get-started/installation/odroidc4-setup/etcher-choose-os.png" alt="The etcher imager with a generic microSD card selected as the target" resize="700x" style="min-width: 600px" declaredimensions=true >}}

1. Then click `Flash!` to begin.

## Power your Odroid C4

Connect your power adapter to the Odroid C4's power jack.
The red LED should light up, which indicates that the board is powered.

To connect to a display, connect the micro HDMI end of your cable to the Odroid and the other end to your monitor.

## Establish a network connection

- Plug the Ethernet cable into the Odroid C4 to connect to the internet through a wired network.
- Alternatively, you can connect a USB Wi-Fi dongle and configure Wi-Fi using your operating system settings.

## Access and update your Odroid C4

You can access your Odroid C4 using SSH if you know its IP address.

If not, connect a keyboard and a mouse to interact with it directly using a connected display.

To update your system, open a terminal and run the following commands:

```json
sudo apt update && sudo apt upgrade
```

## Install `viam-server`

{{< readfile "/static/include/install/install-linux.md" >}}

## Troubleshooting

Visit the [Odroid Forum](https://forum.odroid.com/viewforum.php?f=200) for troubleshooting tips and tricks specific to the Odroid C4.
