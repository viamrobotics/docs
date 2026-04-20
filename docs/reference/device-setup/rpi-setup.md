---
title: "Raspberry Pi Setup Guide"
linkTitle: "Raspberry Pi Setup"
weight: 15
type: "docs"
description: "Image a Raspberry Pi to prepare it for viam-server installation."
images: ["/installation/thumbnails/raspberry-pi-4-b-2gb.png"]
imageAlt: "Raspberry Pi"
no_list: true
aliases:
  - /operate/reference/wifi-credentials/
  - /operate/reference/prepare/rpi-setup/
  - /getting-started/rpi-setup/
  - /installation/rpi-setup/
  - /installation/prepare/rpi-setup/
  - /get-started/installation/prepare/rpi-setup/
  - /get-started/prepare/rpi-setup/
  - /operate/reference/prepare/rpi-enable-protocols/
  - /operate/reference/prepare/wifi-credentials/
# SME: James
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/drl2p2of-qA">}}

We recommend using Viam on a 64-bit Linux distribution.
Support for older Raspberry Pis running on 32-bit ARM v7 is in beta.

If you already have a Linux distribution installed on your {{< glossary_tooltip term_id="pi" text="Pi" >}}, you can skip ahead to [install `viam-server`](/set-up-a-machine/overview/).

{{% expand "Click to check whether the Linux installation on your Raspberry Pi is 64-bit or 32-bit" %}}

To check whether the Linux installation on your Raspberry Pi is 64-bit or 32-bit, `ssh` into your Pi and then run `lscpu`.

Example output:

{{< imgproc alt="Screenshot of a terminal running the 'lscpu' command. The output lists of this command on a Raspberry Pi. A red box highlights the command and the top of the output which reads 'Architecture: aarch64.'" src="/installation/rpi-setup/lscpu-output.png" resize="800x" declaredimensions=true class="shadow" >}}

If the value of "Architecture: _'xxxxxx'_" ends in "64", you can skip ahead to [install `viam-server`](/set-up-a-machine/overview/).

{{% /expand%}}

## Hardware requirements

- A [Raspberry Pi single-board computer](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- A microSD card
- An internet-connected computer
- A way to connect the microSD card to the computer (microSD slot or microSD reader)

## Install Raspberry Pi OS

The Raspberry Pi boots from a microSD card.
You need to install Raspberry Pi OS (formerly called Raspbian) on the microSD card you will use with your Pi:

1. Connect the microSD card to your computer.

1. Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) and launch it.

   {{< imgproc alt="Raspberry Pi Imager launcher window showing a 'Choose OS' and 'Choose Storage' buttons." src="/installation/rpi-setup/imager-launch-screen.png" resize="800x" declaredimensions=true class="shadow" >}}

1. Click **CHOOSE DEVICE**.
   Select your model of Pi.

   {{< imgproc alt="Raspberry Pi Imager window showing available pi models." src="/installation/rpi-setup/select-pi-models.png" resize="800x" declaredimensions=true class="shadow" >}}

1. Click **CHOOSE OS**.
   Select **Raspberry Pi OS (other)**.

   {{< imgproc alt="Raspberry Pi Imager window showing Raspberry Pi OS (Other) is selected." src="/installation/rpi-setup/select-other-custom-os.png" resize="800x" declaredimensions=true class="shadow" >}}

   Select **Raspberry Pi OS Full (64-bit)** or **Raspberry Pi OS Full (32-bit)** from the menu.

   {{< imgproc alt="Raspberry Pi Imager window showing Raspberry Pi OS (Legacy, 64-bit) Full is selected." src="/installation/rpi-setup/select-other-rpi.png" resize="800x" declaredimensions=true class="shadow"  >}}

   You should be brought back to the initial launch screen.

1. Click **CHOOSE STORAGE**.
   From the list of devices, select the microSD card you intend to use in your Raspberry Pi.

   If no devices are listed, make sure your microSD card is connected to your computer correctly.

   {{< imgproc alt="The storage screen is shown with a generic SD card available as an option." src="/installation/rpi-setup/imager-select-storage.png" resize="800x" declaredimensions=true class="shadow"  >}}

1. Configure your Raspberry Pi for remote access.
   Click **Next**.
   When prompted to apply OS customization settings, select **EDIT SETTINGS**.

   {{< imgproc alt="Raspberry Pi Imager window showing gear-shaped settings icon is selected." src="/installation/rpi-setup/advanced-options.png" resize="800x" declaredimensions=true class="shadow"  >}}

   {{% alert title="Important" color="note" %}}

   If you are using a non-Raspberry Pi OS, altering the OS customization settings will cause the initial boot to fail.

   {{% /alert %}}

   Check **Set hostname** and enter the name you would like to access the Pi by in that field:

   {{< imgproc alt="Raspberry Pi Imager window showing the advanced options menu with set hostname checked and set to my-machine.local." src="/installation/rpi-setup/imager-set-hostname.png" resize="600x" declaredimensions=true class="shadow"  >}}

   There are two ways you can secure your Raspberry Pi: with an SSH key or with password authentication.

   - For a learning project or a fun hobby project, we recommend using password authentication because it is easiest to set up for first-time users.
   - For production use, we recommend using SSH keys for more secure authentication; only someone with the private SSH key will be able to authenticate to your system.

   {{< tabs >}}

{{% tab name="Password" %}}

1. Select the checkbox next to **Set username and password** and set a username (for example, your first name) and a unique password that you will use to log into the Pi:

   {{< imgproc alt="Raspberry Pi Imager window showing the 'Set username and password' option is selected. The user has entered username 'Robota' and some hidden password." src="/installation/rpi-setup/imager-set-passwordauthentication.png" resize="550x" declaredimensions=true class="shadow"  >}}

2. Select the **SERVICES** tab.
3. Check **Enable SSH**.

{{% alert title="IMPORTANT" color="note" %}}

Be sure that you remember the `hostname`, `username`, and `password` you set, as you will need them when you SSH into your Pi.

Do not use the default username and password on a Raspberry Pi, as this poses a [security risk](https://www.zdnet.com/article/linux-malware-enslaves-raspberry-pi-to-mine-cryptocurrency/).

{{% /alert  %}}

{{% /tab %}}
{{% tab name="SSH" %}}

To set up SSH authentication:

1. Select the checkbox for **Set username and password** and set a username (for example, your first name) that you will use to log into the Pi.
   If you skip this step, the default username will be `pi` (not recommended for security reasons).
   You do not need to specify a password.

   {{< imgproc alt="Raspberry Pi Imager with username specified as 'Robota' and the password field left blank." src="/installation/rpi-setup/imager-set-username.png" resize="500x" declaredimensions=true class="shadow"  >}}

1. Select the **SERVICES** tab.
1. Check **Enable SSH**.
1. Select **Allow public-key authentication only**.

   If you select **Allow public-key authentication only**, and the section **Set authorized\_ keys for ''** is pre-populated, that means you have a public SSH key that is ready to use.
   In that case, you can leave the pre-populated key as-is.
   If this section is empty, you can either generate a new SSH key using [these instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), or you can use password authentication instead.

   {{< imgproc alt="Raspberry Pi Imager window showing 'Set Hostname' and 'Enable SSH' both selected." src="/installation/rpi-setup/imager-set-ssh.png" resize="500x" declaredimensions=true class="shadow"  >}}

{{% alert title="IMPORTANT" color="note" %}}

Be sure that you remember the `hostname` and `username` you set, as you will need this when you SSH into your Pi.

{{% /alert  %}}

{{% /tab %}}
{{< /tabs >}}

    Lastly, connect your Pi to Wi-Fi so that you can run `viam-server` wirelessly.
    Check **Configure wireless LAN** and enter your wireless network credentials.
    SSID (short for Service Set Identifier) is your Wi-Fi network name, and password is the network password.
    Change the section `Wireless LAN country` to where your router is currently being operated:

    {{< imgproc alt="Raspberry Pi Imager window showing the 'Configure wireless LAN' option selected with SSID and password information for a wireless network." src="/installation/rpi-setup/imager-set-wifi.png" resize="550x" declaredimensions=true class="shadow"  >}}

    Click **SAVE**.

1.  Double check your OS and Storage settings and then click `YES`:

    {{< imgproc alt="Edit image customization options window" src="/installation/rpi-setup/apply-settings-yes.png" resize="800x" declaredimensions=true class="shadow"  >}}

    You will be prompted to confirm erasing your microSD card: select `YES`.

    {{< imgproc alt="Edit image customization options window" src="/installation/rpi-setup/imager-write-confirm.png" resize="800x" declaredimensions=true class="shadow"  >}}

    You may also be prompted by your operating system to enter an administrator password:

    {{< imgproc alt="macOS admin password confirmation screen." src="/installation/rpi-setup/imager-permission.png" resize="300x" declaredimensions=true class="shadow"  >}}

    After granting permissions to the Imager, it will begin writing and then verifying the Linux installation to the MicroSD card.

    Remove the microSD card from your computer when the installation is complete.

    {{< alert title="Tip: How to think about building a machine" color="tip" >}}

While the Imager is flashing your microSD card, we recommend reading [How to think about building a machine](/set-up-a-machine/overview/).

    {{< /alert >}}

2.  Place the SD card into your Raspberry Pi and boot the Pi by plugging it in to an outlet.
    A red LED will turn on to indicate that the Pi is connected to power.

## Next steps

Continue setting up `viam-server` on your Raspberry Pi in [the Viam app](https://app.viam.com/):

{{< cards >}}
{{% card link="/set-up-a-machine/overview/" %}}
{{< /cards >}}
