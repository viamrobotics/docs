---
title: "SK-TDA4VM Setup Guide"
linkTitle: "SK-TDA4VM Setup"
weight: 25
type: "docs"
image: "/installation/thumbnails/tda4vm.png"
imageAlt: "S K - T D A 4 V M"
images: ["/installation/thumbnails/tda4vm.png"]
description: "Image a Texas Instruments TDA4VM starter kit board to prepare it for viam-server installation."
no_list: true
#SMEs: Matt Dannenberg
---

## Hardware requirements

- A [Texas Instruments TDA4VM single-board computer](https://www.ti.com/tool/SK-TDA4VM)
- A USB-C power cable to power the TDA4VM board
- A microSD card
- A desktop or laptop computer for flashing the microSD card
- A way to connect the microSD card to the computer (a microSD slot or microSD reader)
- An Ethernet cable
- An HDMI cable

## Required downloads

Download the following files to your computer:

- Download the <a href="https://www.ti.com/tool/download/PROCESSOR-SDK-LINUX-SK-TDA4VM" target="_blank">PROCESSOR-SDK-LINUX-SK-TDA4VM — Linux SDK for edge AI applications on TDA4VM Jacinto™ processors</a> image.

- Next, download and install the <a href="https://github.com/balena-io/etcher/releases/tag/v1.7.0" target="_blank">Balena Etcher</a> for your desktop/laptop OS.
  You will use the Balena Etcher to flash the microSD card.

## Flash the image

{{% alert title="Important" color="note" %}}
You must extract the image from the zip file before flashing the microSD card.
{{% /alert %}}

{{< imgproc alt="The Balena Etcher interface." src="/installation/sk-tda4vm/etcher.png" resize="600x" declaredimensions=true >}}

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

{{< imgproc alt="Successful image flash completion screen." src="/installation/sk-tda4vm/completed.png" resize="600x" declaredimensions=true >}}

## Install Viam dependencies on the TDA4VM

1. Connect the board to Ethernet.

2. Connect the board to a monitor with the HDMI cable.

3. Connect the board to power using the USB-C power cable.

4. Use the credentials and IP address displayed in the upper right-hand corner of the monitor to SSH into the board.

From the SSH session on the TDA4VM board:

1. Clone the TDA4VM repo:

   ```sh {class="command-line" data-prompt="$"}
   git clone https://github.com/viam-labs/tda4vm-setup.git
   ```

2. Navigate to the setup directory:

   ```sh {class="command-line" data-prompt="$"}
   cd tda4vm-setup/
   ```

3. Make the server setup script executable:

   ```sh {class="command-line" data-prompt="$"}
   chmod +x tda4vm-viam-setup.sh
   ```

4. Launch the setup script to install `viam-server` dependencies:

   ```sh {class="command-line" data-prompt="$"}
   ./tda4vm-viam-setup.sh
   ```

   Once this process completes, the board will reboot.

## Install `viam-server`

{{< readfile "/static/include/install/install-linux.md" >}}

## Next Steps

{{< cards >}}
{{% card link="/manage/configuration/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/program/" %}}
{{< /cards >}}

## Need assistance?

{{< snippet "social.md" >}}
