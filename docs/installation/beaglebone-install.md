---
title: "BeagleBone AI-64 Setup Guide"
linkTitle: "BeagleBone Setup"
weight: 20
type: "docs"
description: "How to install and run viam-server on a BeagleBone AI-64."
# SMEs: Joe Karlsson, Shawn, Matt, and Rand
---

The <a href="https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/" target="_blank">BeagleBone AI-64</a> from <a href="https://beagleboard.org/" target="_blank">BeagleBoard.org</a> is an open-source computer based on the Texas Instruments TDA4VM processor.
In this tutorial, we will show you how to set up your BeagleBone AI-64 with Debian, and install Viam.

{{% figure src="../img/beaglebone-install/image4.png" alt="BeagleBone AI-64 front at 45° angle." title="BeagleBone AI-64 front at 45° angle." %}}

## What you'll need for this guide

You will need the following hardware, tools, and software to install Viam on a BeagleBone AI-64:

1. The BeagleBone AI-64
2. A microSD card
3. A 5V barrel jack power supply
4. [Optional] A microSD card reader
5. [Optional] An ethernet cable or a WIFI card

## BeagleBone AI-64 Installation Guide

{{% alert title="Note" color="note" %}}

Depending on how old of a software image you already have running on your BeagleBone, you might need to update your BeagleBone to the latest software image.
If you experience any issues getting Viam working on your BeagleBone, you should consult the BeagleBone getting started documentation at <a href="https://beagleboard.org/getting-started" target="_blank">beagleboard.org/getting-started</a> for steps on updating your BeagleBone.

{{% /alert %}}

### Power your BeagleBone

You need a data connection from the BeagleBone to your computer. A USB-C to USB-C from your computer to your BeagleBone is the most convenient method to make the data connection.
Although it is possible to power the BeagleBone via its USB-C connection, we recommend that you use a separate 5VDC power source (e.g., 5VDC charger) via the BeagleBoard's barrel jack as that is more reliable.
When powered on, you'll see the power (PWR or ON) LED lit steadily. Other LEDs will begin blinking within a minute or so.
Within a minute or so, you should see the other LEDs blinking.

### Enable a network connection

You will need to connect an ethernet cable to your BeagleBone in order to connect to it.
If your computer supports mDNS (Multicast DNS), you should see your Beagle at <a href="beaglebone.local" target="_blank">beaglebone.local</a>.
Using any web browser (except Internet Explorer) you can test to see if your BeagleBone has successfully connected to the internet.

{{% alert title="Note" color="note" %}}

You can also connect to the internet via _internet connection sharing_.

If you are connecting to your BeagleBone with macOS, you can use <a href="https://support.apple.com/guide/mac-help/share-internet-connection-mac-network-users-mchlp1540/mac" target="_blank">Internet Sharing over USB</a>[^mac] to connect to the internet.
After enabling it on your machine, SSH into your BeagleBone, and run the following: `sudo dhclient usb1`.

For Linux, you can follow this <a href="https://fastbitlab.com/how-to-enable-internet-over-usb/" target="_blank">tutorial for enabling internet over USB</a>.

{{% /alert %}}

The below table summarizes the typical addresses and should dynamically update to indicate an active connection.

|     IP Address      | Connection Type  | Operating System(s)  |  Status   |
|:------------------: |:---------------: |:-------------------: |:--------: |
| 192.168.7.2         | USB              | Windows              | Inactive  |
| 192.168.6.2         | USB              | Mac OS X, Linux      | Inactive  |
| 192.168.8.1         | WiFi             | all                  | Inactive  |
| beaglebone.local    | all              | mDNS enabled         | Inactive  |
| beaglebone-2.local  | all              | mDNS enabled         |           |

### SSH into your BeagleBone

You can SSH into your BeagleBone by running the following from your terminal:

{{% alert title="Note" color="note" %}}

The default username and password supplied by BeagleBone is:

* Username: `debian`
* Password: `temppwd`

{{% /alert %}}

```bash
ssh debian@beaglebone.local
```

### Check that your BeagleBone is connected to the internet

After you SSH into your BeagleBone, you can check that your BeagleBone is connected to the internet by running the following command:

```bash
ping -c 3 google.com
```

If you see a response like the one below, you are connected to the internet.

```bash
PING google.com (209.85.234.138): 56 data bytes
64 bytes from 209.85.234.138: icmp_seq=0 ttl=55 time=31.852 ms
64 bytes from 209.85.234.138: icmp_seq=1 ttl=55 time=35.585 ms
64 bytes from 209.85.234.138: icmp_seq=2 ttl=55 time=43.308 ms

--- google.com ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 31.852/36.915/43.308/4.771 ms
```

### Update your BeagleBone

Next, best practice suggests that you always ensure that the latest packages are installed.
Run the following command to do verify the packages are up to date:

```bash
sudo apt update && sudo apt dist-upgrade && sudo reboot
```

### Setup your BeagleBone on the Viam app

* Go to <a href="https://app.viam.com" target="_blank">app.viam.com</a>
* Create a new robot
* Go to the **SETUP** tab
* Follow the instructions for a Linux with an Aarch64 architecture installation.
* Wait for the Viam app to confirm that you have connected to your BeagleBone.

{{% figure src="../img/beaglebone-install/image2.png" width="50%" alt="Screenshot from the Viam app showing a dialog box with a green checkmark and text that reads, 'Your robot is successfully connected! Proceed to the config tab.'" %}}

{{% alert title="Tip" color="tip" %}}

For more information on installing Viam on a Linux machine, check out our [Linux installation guide](/installation/linux-install/).

{{% /alert %}}

## Next steps

Now that you have viam-server up and running on your BeagleBone, you can start configuring your robot and the real fun can begin!

We recommend that you try our [LED blink tutorial](/tutorials/make-an-led-blink-with-a-raspberry-pi-and-sdk/) and [configuring a robot with a USB camera](/tutorials/configure-a-camera/) tutorial.
These are a great place to get started and to ensure that your board is configured correctly.
You can check out [our complete list of tutorials](https://docs.viam.com/tutorials/) for step-by-step project walk throughs demonstrating robot configuration.

[^mac]: <a href="https://support.apple.com/guide/mac-help/share-internet-connection-mac-network-users-mchlp1540/mac" target="_blank">macOS: Internet Sharing: htt<span></span>tps://support.apple.com/guide/mac-help/share-internet-connection-mac-network-users-mchlp1540/mac</a>
