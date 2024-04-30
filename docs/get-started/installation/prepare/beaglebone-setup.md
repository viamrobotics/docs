---
title: "BeagleBone AI-64 Setup Guide"
linkTitle: "BeagleBone Setup"
weight: 20
type: "docs"
description: "Flash a BeagleBone AI-64 to prepare it for viam-server installation."
images: ["/get-started/installation/thumbnails/beaglebone.png"]
imageAlt: "BeagleBone A I-64"
no_list: true
aliases:
  - "/installation/beaglebone-install/"
  - "/installation/prepare/beaglebone-install/"
  - "/installation/prepare/beaglebone-setup/"
# SMEs: Shawn, Matt Dannenberg, and Rand
---

The [BeagleBone AI-64](https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/) from [BeagleBoard.org](https://beagleboard.org/) is an open-source single-board computer with a Debian GNU/Linux operating system based on the Texas Instruments TDA4VM processor.
Follow this guide to set up your BeagleBone AI-64 and prepare it for `viam-server` installation.

<div class="td-max-width-on-larger-screens text-center">
{{< imgproc alt="The front of a BeagleBone AI-64 single-board computer at a 45° angle." src="/get-started/installation/beaglebone-setup/image4.png" resize="400x" declaredimensions=true >}}
</div>

## Hardware requirements

You need the following hardware, tools, and software to install `viam-server` on a BeagleBone AI-64:

1. A [BeagleBone AI-64](https://www.beagleboard.org/boards/beaglebone-ai-64)
2. A 5V barrel jack (recommended) and/or USB-C power supply, to power the BeagleBone
3. Ethernet cable and/or WiFi dongle, to establish network connection on the BeagleBone
4. (Optional) A microSD card and a way to connect the microSD card to the computer (like a microSD slot or microSD reader)
   - This is required if you need to set up your BeagleBone for the first time or update your BeagleBone to the latest software image.

The following instructions mirror the instructions given in the [BeagleBoard Quick Start Guide](https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/02-quick-start.html).

If you want additional help setting up your BeagleBone, you can follow the guides there and return to the Viam docs after SSH'ing into your BeagleBone.

## Power your BeagleBone

Power your board by plugging a 5VDC power source into the BeagleBone's barrel jack.
You can also power the BeagleBone with a USB-C cable, but a 5VDC power source is recommended for more reliable performance.

If the board has power, the LED on the board labeled _PWR_ or _ON_ is lit steadily.

## Enable a network connection

You need to enable a network connection on your BeagleBone to install `viam-server` on it.
You can do this in multiple ways:

- Connect an ethernet cable to your BeagleBone's ethernet port.
- If you are working on a macOS machine, use [internet sharing over USB](https://support.apple.com/guide/mac-help/share-internet-connection-mac-network-users-mchlp1540/mac) to share your connection.
  After enabling the option on your machine, SSH into your BeagleBone and run `sudo dhclient usb1`.
- If you are working on a Linux machine, read [these tips on enabling a network connection](https://elinux.org/Beagleboard:Terminal_Shells).
- If your personal computer supports mDNS (Multicast DNS), you can check to see if your BeagleBone board has established a network connection by visiting [beaglebone.local](https://beaglebone.local).

## SSH into your BeagleBone from your PC

You can SSH into your BeagleBone by running the following command in your terminal:

`ssh <your-username>@<your-hostname>.local`

By default, the hostname, username and password on a BeagleBone are:

- Hostname: `beaglebone`
- Username: `debian`
- Password: `temppwd`

Therefore, if you are using the default settings on your BeagleBone, the command is:

`ssh debian@beaglebone.local`

## Update your BeagleBone

After SSH'ing into your BeagleBone, verify all packages are up to date:

`sudo apt update && sudo apt dist-upgrade && sudo reboot`

## Install `viam-server`

{{< readfile "/static/include/install/install-linux.md" >}}

## Troubleshooting

If you experience any issues getting Viam working on your BeagleBone, consult the [BeagleBone documentation](https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/02-quick-start.html) for help updating your BeagleBone.

{{< snippet "social.md" >}}

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

## Next steps

{{< cards >}}
{{% card link="/build/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/get-started/try-viam/" %}}
{{< /cards >}}
