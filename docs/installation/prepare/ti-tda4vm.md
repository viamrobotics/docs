---
title: "TI TDA4VM Setup Guide"
linkTitle: "TDA4VM Setup"
weight: 25
type: "docs"
description: "A guide to imaging a TDA4VM to prepare it for viam-server installation."
---

## Hardware requirements

* A [Texas Instruments TDA4VM single-board computer](https://www.ti.com/tool/SK-TDA4VM)
* A USB-C power cable to power the TDA4VM board
* A microSD card
* A desktop or laptop computer for flashing the microSD card
* A way to connect the microSD card to the computer (a microSD slot or microSD reader)
* An Ethernet cable
* An HDMI cable

## Required downloads

Download the following files to your computer:

* Download the <a href="https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM" target="_blank">PROCESSOR-SDK-LINUX-SK-TDA4VM — Linux SDK for edge AI applications on TDA4VM Jacinto™ processors</a> image.

* Next, download and install the <a href="https://github.com/balena-io/etcher/releases/tag/v1.7.0" target="_blank">Balena Etcher</a> for your desktop/laptop OS.
You will use the Balena Etcher to flash the microSD card.

## Flash the image

{{% alert title="Note" color="note" %}}
You must extract the image from the zip file before flashing the microSD card.
{{% /alert %}}

<img src="../../img/ti-tda4vm/etcher.png" width="600px" alt="The Balena Etcher interface.">

<br>
<br>

1. Insert the microSD card into a reader connected to your computer.

2. Launch Balena Etcher.

3. Click **Flash from File** to open the file selector.

4. Navigate to and select the image you downloaded.

5. Click **Select Target** to choose the storage device corresponding to your microSD card from the selector window.

6. Click on the desired device, then click **Select** to continue.

7. Click **Flash!**.
   If you receive a warning concerning the size of the microSD card, ensure that you have inserted the proper microSD and also selected the proper device, then click, **Yes, I'm sure** to flash the board.
   The flashing and verification process may take 10-20 minutes, depending on your system.

8. On completion of the flashing and validation process, remove the microSD card from your computer and insert it into the TDA4VM.

<img src="../../img/ti-tda4vm/completed.png" width="600px" alt="Successful image flash completion screen." >

## Install Viam dependencies on the TDA4VM

1. Connect the Ethernet and HDMI cables to the board.

2. Connect the board to power using the USB-C power cable.

3. Use the credentials and IP address displayed in the upper right-hand corner of the monitor to SSH into the board:

<img src="../../img/ti-tda4vm/welcomescreen.png" width="600px" alt="TI Welcome Screen." title="TI Welcome Screen." >

<br>
<br>

From the SSH session on the TDA4VM board:

1. Clone the TDA4VM repo:

   ```bash
   git clone https://github.com/viam-labs/tda4vm-setup.git
   ```

2. Navigate to the setup directory:

   ```bash
   cd tda4vm-setup/
   ```

3. Make the server setup script executable:

   ```bash
   chmod +x tda4vm-viam-setup.sh
   ```

4. Launch the setup script to install viam-server dependencies:

   ```bash
   ./tda4vm-viam-setup.sh
   ```

   Once this process completes, the board will reboot.

## Next steps

Now that your board has a Viam-compatible operating system installed, continue to our [viam-server installation guide](/installation/install/).

## Need assistance?

You can ask questions on the [Viam Community Slack](http://viamrobotics.slack.com) and we will be happy to help.
