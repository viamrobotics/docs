---
title: "TI TDA4VM Setup Guide"
linkTitle: "TDA4VM Setup Guide"
weight: 25
type: "docs"
description: "A guide to imaging a TDA4VM, installing viam-server, and syncing the TDA4VM with the Viam app."
# Doc contact - Mike
---
## Overview

The TDA4VM board is designed for high-performance processing, performing up to 8 trillion operations per second. It provides multiple interfaces, including USB 3.0, CAN-FD, UART (over USB), M.2 Keys E and M, as well as multi-camera support via CSI-2 (R-Pi compatible) and a 40-pin Semtec connector that supports up to eight cameras (requires a TIDA-01413 sensor fusion add-on).

## Texas Instruments Resources

* Product Page
(Spec sheet and Errata): 
<a href="https://www.ti.com/product/TDA4VM" target="blank">ht<span></span>tps://www.ti.com/product/TDA4VM</a>

* Overview Page: 
<a href="https://www.ti.com/tool/SK-TDA4VM" target="blank">ht<span></span>tps://www.ti.com/tool/SK-TDA4VM</a>

* SK-TDA4VM User's Guide: 
  <a href="https://www.ti.com/lit/ug/spruj21c/spruj21c.pdf" target="blank">ht<span></span>tps://www.ti.com/lit/ug/spruj21c/spruj21c.pdf</a>

* Support and Training: 
<a href="https://www.ti.com/tool/SK-TDA4VM#support-training" target="blank">ht<span></span>tps://www.ti.com/tool/SK-TDA4VM#support-training</a>

## Downloads

Download the <a href="https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM" target="_blank">PROCESSOR-SDK-LINUX-SK-TDA4VM — Linux SDK for edge AI applications on TDA4VM Jacinto™ processors</a>[^image] image.

[^image]:PROCESSOR-SDK-LINUX-SK-TDA4VM — Linux SDK for edge AI applications on TDA4VM Jacinto™ processors: <a href="https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM">ht<span></span>tps://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM.

Next, download and install the <a href="https://github.com/balena-io/etcher/releases/tag/v1.7.0" target="_blank">Balena Etcher</a>[^etcher] for your OS.

[^etcher]:Balena Etcher <a href="https://github.com/balena-io/etcher/releases/tag/v1.7.0" target="_blank">ht<span><span>tps://github.com/balena-io/etcher/releases/tag/v1.7.0</a>

You will use the Balena Etcher to flash the micro-SD card.

## Flashing the Image


{{% alert="Note" color="note" %}}
You must extract the image from the zip file before attempting to flash the microSD card.
{{% /alert %}}

{{< figure src="../img/tda4vm/etcher.png" width="600px" alt="The Balena Etcher interface." title="The Balena Etcher interface." >}}

1. Insert the microSD card into a reader connected to your computer.
1. Launch Balena Etcher.
1. Click **Flash from File** to open the file selector.
3. Navigate to and select the image you downloaded.
4. Click **Select Target** to choose the storage device corresponding to your microSD card from the selector window.
5. Click on the desired device, then click **Select** to continue.
6. Click **Flash!**. 
   If you receive a warning concerning the size of the microSD card, ensure that you have inserted the proper microSD and also selected the proper device, then click, **Yes, I'm sure** to flash the board. 
   The flashing and verification process may take 10-20 minutes, depending on your system.
7. On completion of the flashing and validation process, remove the microSD card from your computer and insert it into the TDA4VM.

{{< figure src="../img/tda4vm/completed.png" width="600px" alt="Successful image flash completion screen." title="Successful image flash completion screen." >}}

## Installing Viam Server on the TDA4VM

### External Connection and Login

1. Connect the ethernet, hdmi, and USB-C power cables to the board. 

2. Use the credentials and IP address displayed in the upper right-hand corner of the monitor to SSH into the board:

{{< figure src="../img/tda4vm/welcomescreen.png" width="600px" alt="TI Welcome Screen." title="TI Welcome Screen." >}}

## Installing Viam-Server

You must be logged in to the board to perform this section.

1. Clone the TDA4VM repo: git clone https://github.com/viam-labs/tda4vm-setup.git
1. Navigate to the setup directory: cd tda4vm-setup/
2. Make the server setup script executable: chmod +x tda4vm-viam-setup.sh
3. Launch the setup script: ./tda4vm-viam-setup.sh
1. In the Viam App, navigate to the **CONFIG** tab. 
2. In the **Create Component** pane, enter a **Name** for the board, select "board" from the **Type** drop-down, and select "ti" from the **Model** drop-down.
3. Click **Create Component**.
4. Click **Save Config**.
5. Navigate to the **SETUP** tab.
6. Copy the command string provided in Item #1, then run the command in your terminal session to download the Viam app config to the board.
7. Copy the command string provided in Item #2, then run the command in your terminal session to download and install the viam-server on the board.
8. Await the connection confirmation. When the viam-server is connected, the Viam app displays:

{{< figure src="../img/tda4vm/connected.png" width="300px" alt="Successful image flash completion screen." title="Successful image flash completion screen." >}}

## Restarting the Server

After SSHing into the board, run:

<file>systemctl restart viam-server</file>

to restart the viam-server if necessary, or click **Restart** in the Viam App.

## Next steps

Now that you have viam-server up and running on your TDA4VM, you can start configuring your robot and the real fun can begin!

## Need Assistance?

You can ask questions on the [Viam Community Slack](http://viamrobotics.slack.com) and we will be happy to help.
