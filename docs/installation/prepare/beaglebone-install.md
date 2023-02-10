---
title: "BeagleBone AI-64 Setup Guide"
linkTitle: "BeagleBone Setup"
weight: 20
type: "docs"
description: "How to flash a BeagleBone AI-64 to prepare it for viam-server installation."
aliases:
    - "/installation/beaglebone-install/"
# SMEs: Shawn, Matt Dannenberg, and Rand
---

The [BeagleBone AI-64](https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/) from [BeagleBoard.org](https://beagleboard.org/) is an open-source single-board computer with a Debian GNU/Linux operating system based on the Texas Instruments TDA4VM processor.
Follow this guide to set up your BeagleBone AI-64 and prepare it for `viam-server` installation.

<img src="../../img/beaglebone-install/image4.png" alt="The front of a BeagleBone AI-64 single-board computer at a 45° angle.">

## Hardware Requirements

You need the following hardware, tools, and software to install `viam-server` on a BeagleBone AI-64:

1. A [BeagleBone AI-64](https://beagleboard.org/ai-64)
2. A 5V barrel jack (recommended) and/or USB-C power supply, to power the BeagleBone
3. Ethernet cable and/or WiFi dongle, to establish network connection on the BeagleBone
4. (Optional) A microSD card and a way to connect the microSD card to the computer (like a microSD slot or microSD reader)
    - This is required if you need to set up your BeagleBone for the first time or update your BeagleBone to the latest software image.


{{% alert title="Note" color="note" %}}

If you have already powered up and connected to your BeagleBone before coming to this guide, skip ahead to the [installation guide](/installation/install/).

However, you might need to update your BeagleBone to the latest software so your OS can run `viam-server`.

If you experience any issues getting Viam working on your BeagleBone, consult the [BeagleBone documentation](https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/ch03.html) for help updating your BeagleBone, or reach out on the [the Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw).

{{% /alert %}}

The following instructions mirror the instructions given in the BeagleBoard documentation at [Connecting up your BeagleBone](https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/ch03.html) and [Getting Started with your BeagleBone](https://beagleboard.org/getting-started).
If you want additional help setting up your BeagleBone, you can follow the guides there and return to the Viam docs after SSH'ing into your BeagleBone.



### Step 1: Power your BeagleBone

Power your board by plugging a 5VDC power source into the BeagleBone's barrel jack.
You can also power the BeagleBone with a USB-C cable, but a 5VDC power source is recommended for more reliable performance.

If the board has power, the LED on the board labeled *PWR* or *ON* is lit steadily.

### Step 2: Enable a network connection

You need to enable a network connection on your BeagleBone to install `viam-server` on it.
You can do this in multiple ways:
- Connect an ethernet cable to your BeagleBone's ethernet port.
- If you are on macOS, use [internet sharing over USB](https://support.apple.com/guide/mac-help/share-internet-connection-mac-network-users-mchlp1540/mac) to connect to the internet.
   After enabling the option on your machine, SSH into your BeagleBone and run `sudo dhclient usb1`.
- If you are one Linux machine, follow the tutorial at [fastbitlab.com/how-to-enable-internet-over-usb/](https://fastbitlab.com/how-to-enable-internet-over-usb/) to enable internet sharing over USB.

{{% alert title="Note" color="note" %}}

You can also connect to the internet via internet connection sharing.

If your personal computer is macOS, you can use [internet sharing over USB](https://support.apple.com/guide/mac-help/share-internet-connection-mac-network-users-mchlp1540/mac) to connect to the internet.
After enabling the option on your machine, SSH into your BeagleBone and run the following command: `sudo dhclient usb1`.

If your PC is Linux, you can follow the tutorial at [fastbitlab.com/how-to-enable-internet-over-usb/](https://fastbitlab.com/how-to-enable-internet-over-usb/) to enable internet sharing over USB.

{{% /alert %}}

- If your personal computer supports mDNS (Multicast DNS), you can check to see if your BeagleBone board has established a network connection by visiting [beaglebone.local](https://beaglebone.local).

### Step 3: SSH into your BeagleBone from your PC

You can SSH into your BeagleBone by running the following command in your terminal:

`ssh <your-username>@<your-hostname>.local`

By default, the hostname, username and password on a BeagleBone are:

- Hostname: `beaglebone`
- Username: `debian`
- Password: `temppwd`
  
Therefore, if you are using the default settings on your BeagleBone, the command is:

`ssh debian@beaglebone.local`

### Step 4: Update your BeagleBone

After SSH'ing into your BeagleBone, verify all packages are up to date:

`sudo apt update && sudo apt dist-upgrade && sudo reboot`

### Step 5: Install `viam-server`

Now that your BeagleBone has a Viam-compatible operating system installed, continue to our [viam-server installation guide](/installation/install/) to install `viam-server` on the board.

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
