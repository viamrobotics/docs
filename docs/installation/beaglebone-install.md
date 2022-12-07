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

{{% alert title="Note" color="note" %}}

You can find an official guide from BeagleBone on getting started at <a href="https://beagleboard.org/getting-started" target="_blank">beagleboard.org/getting-started</a>.

{{% /alert %}}

## What you'll need for this guide

You will need the following hardware, tools, and software to install Viam on a BeagleBone AI-64:

1. The BeagleBone AI-64
2. A microSD card
3. A microSD card reader
4. A power supply
5. [Optional] An ethernet cable or a WIFI card

## BeagleBone AI-64 Installation Guide

### Update BeagleBone with the latest software

Download the latest Debian image from <a href="https://beagleboard.org/latest-images" target="_blank">beagleboard.org/latest-images</a>.
We recommend that you install the Buster IoT TIDL (without a graphical desktop and with machine learning acceleration tools) for BeagleBone AI.

{{% figure src="../img/beaglebone-install/image3.png" width="50%" alt="Screenshot from the beaglebone.org website with a red box highlighting the Buster IoT Debian image." title="Screenshot from the beaglebone.org website." %}}

After downloading this operating system image, you can flash your microSD card with it.

### Install SD card programming utility

You'll need to use a program like <a href="https://www.balena.io/etcher/" target="_blank">balenaEtcher</a> in order to flash your microSD drive.

{{% figure src="../img/beaglebone-install/image5.png" width="50%" alt="Screenshot from the balenaEtcher homepage." title="Screenshot from the balenaEtcher homepage." %}}

### Connect your SD card to your computer

After downloading and installing Etcher plug your microSD reader into your computer and insert the SD card.

### Select the image

Click the "Select image" button and find the image you just downloaded.
It should have either the `.img` extension or the `.img.xy` extension (Etcher supports using either a compressed or decompressed image).

### Write the image to your SD card

After you select the image you may also need to select the microSD card from the drives on your machine.
Then you can select "Flash!" and wait for the process to finish. That process should take a few minutes.

{{% figure src="../img/beaglebone-install/image1.png" width="50%" alt="Screenshot from balenaEtcher showing an image and microSD card selected with a big blue button that says, 'Flash!'" title="Screenshot from balenaEtcher showing an image and microSD card selected with a big blue button that says, 'Flash!'" %}}

### Eject the SD card and boot your board off of the SD card

After Etcher is done flashing your microSD card your operating system might prompt you to eject it.
If it doesn't, go ahead and remove the drive from the SD card reader. Insert the SD card into your (powered-down) board.

### Power your BeagleBone

You will need to connect your BeagleBone to your computer and power it, the most convenient way to do that is to connect it with a USB-C to USB-C from your computer to your BeagleBone.
However, we recommend that you power your BeagleBoard using the barrel jack, since it's more reliable to separate power. The barrel jack can be powered with a 5V charger.
If it's being powered, you'll see the power (PWR or ON) LED lit steadily. Within a minute or so, you should see the other LEDs blinking.

### Enable a network connection

You will need to connect an ethernet cable to your BeagleBone in order to connect to it.
If your computer supports mDNS, you should see your Beagle at <a href="beaglebone.local" target="_blank">beaglebone.local</a>.
Using either <a href="https://www.google.com/chrome" target="_blank">Chrome</a> or <a href="https://www.mozilla.org/en-US/firefox/new/" target="_blank">Firefox</a> you can test to see if your BeagleBone has successfully connected to the internet.

{{% alert title="Note" color="note" %}}

You can also use internet over USB to connect your BeagleBone to the network.

If you are connecting to your BeagleBone with macOS, you can use <a href="https://support.apple.com/guide/mac-help/share-internet-connection-mac-network-users-mchlp1540/mac" target="_blank">Internet Sharing over USB</a> to connect to the internet.
After enabling it on your machine, SSH into your BeagleBone, and run the following: `sudo dhclient usb1`.

For Linux, you can follow this [tutorial for enabling internet over USB](https://fastbitlab.com/how-to-enable-internet-over-usb/). 

{{% /alert %}}

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

### Update your BeagleBone

Next, it's good practice to update your BeagleBone to ensure all the latest packages are installed:

```bash
sudo apt update && sudo apt dist-upgrade && sudo reboot
```

### Setup your BeagleBone on the Viam app

- Go to <a href="https://app.viam.com" target="_blank">app.viam.com</a>
- Create a new robot
- Go to the **SETUP** tab
- Follow the instructions for a Linux with an Aarch64 architecture installation.
- Wait for the Viam app to confirm that you have connected to your BeagleBone.

{{% figure src="../img/beaglebone-install/image2.png" width="50%" alt="Screenshot from the Viam app showing a dialog box with a green checkmark and text that reads, 'Your robot is successfully connected! Proceed to the config tab.'" %}}

{{% alert title="Tip" color="tip" %}}

For more information on installing Viam on a Linux machine, check out our [Linux installation guide](/installation/linux-install/)

{{% /alert %}}

## Next steps

Now that you have the viam-server up and running on your BeagleBone, you can start configuring your robot and the real fun can begin!

We recommend that you try our [LED blink tutorial](/tutorials/make-an-led-blink-with-a-raspberry-pi-and-sdk/) and [configuring a robot with a USB camera](/tutorials/configure-a-camera/) tutorial. These are a great place to get started an to ensure that your board is configured correctly.
You can check out [our complete list of tutorials](https://docs.viam.com/tutorials/) for step-by-step project walkthroughs demonstrating robot configuration.
