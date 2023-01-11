---
title: "TI TDA4VM Setup Guide"
linkTitle: "TDA4VM Setup"
weight: 25
type: "docs"
description: "A guide to imaging a TDA4VM, installing viam-server, and syncing the TDA4VM with the Viam app."
# Doc contact - Mike
---

## Required downloads

You will need to download the following files to your computer:

Download the <a href="https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM" target="_blank">PROCESSOR-SDK-LINUX-SK-TDA4VM — Linux SDK for edge AI applications on TDA4VM Jacinto™ processors</a>[^image] image.

[^image]:PROCESSOR-SDK-LINUX-SK-TDA4VM — Linux SDK for edge AI applications on TDA4VM Jacinto™ processors: <a href="https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM">ht<span></span>tps://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM.

Next, download and install the <a href="https://github.com/balena-io/etcher/releases/tag/v1.7.0" target="_blank">Balena Etcher</a>[^etcher] for your OS.

[^etcher]:Balena Etcher <a href="https://github.com/balena-io/etcher/releases/tag/v1.7.0" target="_blank">ht<span><span>tps://github.com/balena-io/etcher/releases/tag/v1.7.0</a>

You will use the Balena Etcher to flash the micro-SD card.

## Flashing the image

{{% alert title="Note" color="note" %}}
You must extract the image from the zip file before attempting to flash the microSD card.
{{% /alert %}}

{{% alert title="Note" color="note" %}}
If you intend to perform video capture or use the Data Management service, you may need a higher capacity microSD card to hold the cached video or data. Otherwise, a 16GB microSD is sufficient to hold the linux board image and the viam-server. 
{{% /alert %}}

{{< figure src="../img/tda4vm/etcher.png" width="600px" alt="The Balena Etcher interface." title="The Balena Etcher interface." >}}

1. Insert the microSD card into a reader connected to your computer.
1. Launch Balena Etcher.
1. Click **Flash from File** to open the file selector.
1. Navigate to and select the image you downloaded.
1. Click **Select Target** to choose the storage device corresponding to your microSD card from the selector window.
1. Click on the desired device, then click **Select** to continue.
1. Click **Flash!**. 
   If you receive a warning concerning the size of the microSD card, ensure that you have inserted the proper microSD and also selected the proper device, then click, **Yes, I'm sure** to flash the board. 
   The flashing and verification process may take 10-20 minutes, depending on your system.
1. On completion of the flashing and validation process, remove the microSD card from your computer and insert it into the TDA4VM.

{{< figure src="../img/tda4vm/completed.png" width="600px" alt="Successful image flash completion screen." title="Successful image flash completion screen." >}}

## Installing Viam Server on the TDA4VM

### External connection and login

1. Connect the ethernet, HDMI, and USB-C power cables to the board.

2. Use the credentials and IP address displayed in the upper right-hand corner of the monitor to SSH into the board:

{{< figure src="../img/tda4vm/welcomescreen.png" width="600px" alt="TI Welcome Screen." title="TI Welcome Screen." >}}

### Installing viam-server

Login to the board using SSH to complete this section.

<OL>
<li>Clone the TDA4VM repo:<br>
<file>git clone https://github.com/viam-labs/tda4vm-setup.git</file></li>
<li>Navigate to the setup directory:<br> <file>cd tda4vm-setup/</file> </li>
<li>Make the server setup script executable:<br> <file>chmod +x tda4vm-viam-setup.sh</file> </li>
<li>Launch the setup script:<br> <file>./tda4vm-viam-setup.sh </file></li>
<li>In the Viam App, navigate to the <strong>CONFIG</strong> tab. </li>
<li>In the <strong>Create Component</strong> pane, enter a <strong>Name</strong> for the board, select "board" from the <strong>Type</strong> drop-down, and select "ti" from the <strong>Model</strong> drop-down.</li>
<li>Click <strong>Create Component</strong>.</li>
<li>Click <strong>Save Config</strong>.</li>
<li>Navigate to the <strong>SETUP</strong> tab.</li>
<li>Copy the command string provided in <strong>Item #1</strong>, then run the command in your terminal session to download the Viam app config to the board.</li>
<li>Copy the command string provided in <strong>Item #2</strong>, then run the command in your terminal session to download and install the viam-server on the board.</li>
<li>Await the connection confirmation. When the viam-server is connected, the Viam app displays a successful image flash completion screen:
</ol>

{{< figure src="../img/tda4vm/connected.png" width="282px" alt="Successful image flash completion screen." title="Successful image flash completion screen.">}}

### Restarting the server

After SSHing into the board, run:

<file>systemctl restart viam-server</file>

to restart the viam-server if necessary, or click **Restart** in the Viam App.

## Next steps

Now that you have viam-server up and running on your TDA4VM, you can start configuring your robot and the real fun can begin!

## Need assistance?

You can ask questions on the [Viam Community Slack](http://viamrobotics.slack.com) and we will be happy to help.
