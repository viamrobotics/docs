---
title: "Raspberry Pi Setup Guide"
linkTitle: "Raspberry Pi Setup"
weight: 15
type: "docs"
description: "Image a Raspberry Pi to prepare it for viam-server installation."
images: ["/get-started/installation/thumbnails/raspberry-pi-4-b-2gb.png"]
imageAlt: "Raspberry Pi"
no_list: true
aliases:
  - /getting-started/rpi-setup/
  - /installation/rpi-setup/
  - /installation/prepare/rpi-setup/
# SME: James
---

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/drl2p2of-qA">}}

To install the Viam {{< glossary_tooltip term_id="rdk" text="RDK" >}}, you need a Raspberry Pi running a 64-bit Linux distribution.

If you already have a 64-bit Linux distribution installed on your Pi, skip ahead to [enable the required communication protocols for your hardware](#enable-communication-protocols).

{{%expand "Click to check whether the Linux installation on your Raspberry Pi is 64-bit" %}}

If you already have a 64-bit Linux distribution installed on your Pi, you can skip ahead to [installing `viam-server`](/get-started/installation/#install-viam-server).
To check whether the Linux installation on your Raspberry Pi is 64-bit (required for running `viam-server`), `ssh` into your Pi and then run `lscpu`.

Example output:

{{< imgproc alt="Screenshot of a terminal running the 'lscpu' command. The output lists of this command on a Raspberry Pi. A red box highlights the command and the top of the output which reads 'Architecture: aarch64.'" src="/get-started/installation/rpi-setup/lscpu-output.png" resize="800x" declaredimensions=true >}}

If the value of "Architecture: _'xxxxxx'_" ends in "64", you can skip ahead to [installing `viam-server`](/get-started/installation/#install-viam-server).

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

   {{< imgproc alt="Raspberry Pi Imager launcher window showing a 'Choose OS' and 'Choose Storage' buttons." src="/get-started/installation/rpi-setup/imager-launch-screen.png" resize="800x" declaredimensions=true >}}

1. Click **CHOOSE DEVICE**.
   Select your model of Pi.

   {{< imgproc alt="Raspberry Pi Imager window showing available pi models." src="/get-started/installation/rpi-setup/select-pi-models.png" resize="800x" declaredimensions=true >}}

1. Click **CHOOSE OS**.
   Select **Raspberry Pi OS (other)**.

   {{< imgproc alt="Raspberry Pi Imager window showing Raspberry Pi OS (Other) is selected." src="/get-started/installation/rpi-setup/select-other-custom-os.png" resize="800x" declaredimensions=true >}}

   Select **Raspberry Pi OS (Legacy, 64-bit) Full** from the menu.

   {{< imgproc alt="Raspberry Pi Imager window showing Raspberry Pi OS (Legacy, 64-bit) Full is selected." src="/get-started/installation/rpi-setup/select-other-rpi.png" resize="800x" declaredimensions=true >}}

   You should be brought back to the initial launch screen.

1. Click **CHOOSE STORAGE**.
   From the list of devices, select the microSD card you intend to use in your Raspberry Pi.

   If no devices are listed, make sure your microSD card is connected to your computer correctly.

   {{< imgproc alt="The storage screen is shown with a generic SD card available as an option." src="/get-started/installation/rpi-setup/imager-select-storage.png" resize="800x" declaredimensions=true >}}

1. Configure your Raspberry Pi for remote access.
   Click **Next**.
   When prompted to apply OS customization settings, select **EDIT SETTINGS**.

   {{< imgproc alt="Raspberry Pi Imager window showing gear-shaped settings icon is selected." src="/get-started/installation/rpi-setup/advanced-options.png" resize="800x" declaredimensions=true >}}

   {{% alert title="Important" color="note" %}}

   If you are using a non-Raspberry Pi OS, altering the OS customization settings will cause the initial boot to fail.

   {{% /alert %}}

   Check **Set hostname** and enter the name you would like to access the Pi by in that field:

   {{< imgproc alt="Raspberry Pi Imager window showing the advanced options menu with set hostname checked and set to my-machine.local." src="/get-started/installation/rpi-setup/imager-set-hostname.png" resize="600x" declaredimensions=true >}}

   There are two ways you can secure your Raspberry Pi: with an SSH key or with password authentication.

   - For a learning project or a fun hobby project, we recommend using password authentication because it is easiest to set up for first-time users.
   - For production use, we recommend using SSH keys for more secure authentication; only someone with the private SSH key will be able to authenticate to your system.

   {{< tabs >}}

{{% tab name="Password" %}}

1. Select the checkbox next to **Set username and password** and set a username (for example, your first name) and a unique password that you will use to log into the Pi:

   {{< imgproc alt="Raspberry Pi Imager window showing the 'Set username and password' option is selected. The user has entered username 'Robota' and some hidden password." src="/get-started/installation/rpi-setup/imager-set-passwordauthentication.png" resize="550x" declaredimensions=true >}}

  {{< alert title="Caution" color="caution" >}}

The default username and password on Raspberry Pis are

- username: pi
- password: raspberry

However, it's [bad practice](https://www.zdnet.com/article/linux-malware-enslaves-raspberry-pi-to-mine-cryptocurrency/) to keep the default username and password on a Raspberry Pi since doing so makes it easy for hackers to get access to your Pi.

   {{< /alert >}}

1. Select the **SERVICES** tab.
1. Check **Enable SSH**.

{{% alert title="IMPORTANT" color="note" %}}

Be sure that you remember the `hostname`, `username`, and `password` you set, as you will need them when you SSH into your Pi.

{{% /alert  %}}

{{% /tab %}}
{{% tab name="SSH" %}}

To set up SSH authentication:

1. Select the checkbox for **Set username and password** and set a username (for example, your first name) that you will use to log into the Pi.
   If you skip this step, the default username will be `pi` (not recommended for security reasons).
   You do not need to specify a password.

   {{< imgproc alt="Raspberry Pi Imager with username specified as 'Robota' and the password field left blank." src="/get-started/installation/rpi-setup/imager-set-username.png" resize="500x" declaredimensions=true >}}

1. Select the **SERVICES** tab.
1. Check **Enable SSH**.
1. Select **Allow public-key authentication only**.

   If you select **Allow public-key authentication only**, and the section **Set authorized\_ keys for ''** is pre-populated, that means you have a public SSH key that is ready to use.
   In that case, you can leave the pre-populated key as-is.
   If this section is empty, you can either generate a new SSH key using [these instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), or you can use password authentication instead.

   {{< imgproc alt="Raspberry Pi Imager window showing 'Set Hostname' and 'Enable SSH' both selected." src="/get-started/installation/rpi-setup/imager-set-ssh.png" resize="500x" declaredimensions=true >}}

{{% alert title="IMPORTANT" color="note" %}}

Be sure that you remember the `hostname` and `username` you set, as you will need this when you SSH into your Pi.

{{% /alert  %}}

{{% /tab %}}
{{< /tabs >}}

    Lastly, connect your Pi to Wi-Fi so that you can run `viam-server` wirelessly.
    Check **Configure wireless LAN** and enter your wireless network credentials.
    SSID (short for Service Set Identifier) is your Wi-Fi network name, and password is the network password.
    Change the section `Wireless LAN country` to where your router is currently being operated:

    {{< imgproc alt="Raspberry Pi Imager window showing the 'Configure wireless LAN' option selected with SSID and password information for a wireless network." src="/get-started/installation/rpi-setup/imager-set-wifi.png" resize="550x" declaredimensions=true >}}

    Click **SAVE**.

1.  Double check your OS and Storage settings and then click `YES`:

    {{< imgproc alt="Edit image customization options window" src="/get-started/installation/rpi-setup/apply-settings-yes.png" resize="800x" declaredimensions=true >}}

    You will be prompted to confirm erasing your microSD card: select `YES`.

    {{< imgproc alt="Edit image customization options window" src="/get-started/installation/rpi-setup/imager-write-confirm.png" resize="800x" declaredimensions=true >}}

    You may also be prompted by your operating system to enter an administrator password:

    {{< imgproc class="aligncenter" alt="macOS admin password confirmation screen." src="/get-started/installation/rpi-setup/imager-permission.png" resize="300x" declaredimensions=true >}}

    After granting permissions to the Imager, it will begin writing and then verifying the Linux installation to the MicroSD card.

    Remove the microSD card from your computer when it is complete:

    {{< imgproc class="aligncenter" alt="You will be notified with a dialogue box informing you that Raspberry Pi OS (Legacy, 64-bit) Full has been written successfully." src="/get-started/installation/rpi-setup/imager-done.png" resize="700x" declaredimensions=true >}}

2.  Place the SD card into your Raspberry Pi and boot the Pi by plugging it in to an outlet.
    A red LED will turn on to indicate that the Pi is connected to power.

## Connect with SSH

Once your Raspberry Pi is plugged in and turned on, wait a minute to let your Pi boot up.

Launch your terminal on your computer and run this command:

{{% alert title="Tip" color="tip" %}}
The text in <> should be replaced (including the < and > symbols themselves) with the user and hostname you configured when you set up your Pi.

Example: if your username is 'Robota' and your hostname is 'my-machine': then it should be `ssh Robota@my-machine.local`

{{% /alert  %}}

```sh {class="command-line" data-prompt="$"}
ssh <USERNAME>@<HOSTNAME>.local
```

If you are prompted "Are you sure you want to continue connecting?", type "yes" and hit enter.
Then, enter your password.
You should be greeted by a login message and a command prompt.

Next, it's good practice to update your Raspberry Pi to ensure all the latest packages are installed:

```sh {class="command-line" data-prompt="$"}
sudo apt update
sudo apt upgrade
```

## Enable communication protocols

Certain hardware, such as analog-to-digital converters (ADCs), accelerometers, and sensors, communicates with your Pi using specialized communications protocols, including I2C, SPI, serial, or one-wire protocols.
If you are using hardware that requires these protocols, you must enable support for them on your Pi using `raspi-config`:

1. Launch the configuration tool by running the following command:

   ```sh {class="command-line" data-prompt="$"}
   sudo raspi-config
   ```

1. Use your keyboard to select "Interface Options", and press return.

   {{< imgproc alt="Screenshot of the Raspi Config screen with a red box and red arrow pointing to the '3 Interface Options' option where you can find the I2C and other drivers" src="/get-started/installation/rpi-setup/installation-raspberry-pi-i2c-raspiconfig-interface-options.png" resize="800x" declaredimensions=true >}}

1. Enable the relevant protocols to support your specific hardware. For example:

   - If you are using an analog-to-digital converter (ADC), motor, or other device that requires the SPI protocol, enable **SPI**.
   - If you are using an accelerometer, sensor, or other device that requires the I<sup>2</sup>C protocol, enable **I2C**.
   - If you are using a CSI v1.3 or v2.0 camera, enable **Legacy Camera** support.
   - If you are using a sensor, motor, or other device that communicates over the serial port, enable **Serial Port**.

   Check the documentation for your specific component to verify the communication protocols it requires.

1. Then, to apply the changes, restart your Raspberry Pi if it hasn't already prompted you to do so.

   ```sh {class="command-line" data-prompt="$"}
   sudo reboot
   ```

## Install `viam-server`

{{< readfile "/static/include/install/install-linux.md" >}}

## Next steps

{{< cards >}}
{{% card link="/build/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/build/program/" %}}
{{< /cards >}}

## Troubleshooting

### Write error when imaging Raspberry Pi OS

If you experience the error `Verifying write failed. Contents of SD card is different from what was written to it` when imaging your Raspberry Pi with the Imager in step 5, there might be an issue with your micro SD card reader.

Try a different micro SD card reader, or use a different USB port on your computer.

If you are connecting your SD card reader to your computer through a USB hub, try connecting directly it to your computer instead.

### Error: can't read from I2C address

If you see the error `error: can't read from I2C address` in your logs after installing `viam-server`, you need to enable `I2C` support on your Raspberry Pi.
You can use the command `sudo journalctl --unit=viam-server` to read through the `viam-server` log file.
Follow the instructions to [enable communication protocols](#enable-communication-protocols) on your Pi to resolve this error.

### Add additional WiFi credentials

If you move your machine to a different WiFi network, you will have to update the WiFi credentials.

You can update the WiFi configuration by creating a new `wpa_supplicant.conf` file on the "boot" partition.

The steps are explained below.

1. Plug your Pi's microSD card into your computer and create a plain text file called `wpa_supplicant.conf`.

2. Paste the following example into the file, replacing "Name of your wireless LAN" and "Password for your wireless LAN" with your credentials.
   Be sure to use UNIX (LF) line breaks in your text editor.

3. Save the file and eject the microSD card.

4. Put the microSD card back into the Pi and boot the Pi.

The `wpa_supplicant.conf` file will be read by the Pi on boot, and the file will disappear but the WiFi credentials will be updated.

You can duplicate the "network" section to add additional WiFi networks (for example your work, and your home).

The "priority" attribute is optional and can be used to prioritize networks if multiple networks are configured (higher numbers are prioritized).

```bash {class="line-numbers linkable-line-numbers"}
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=us

network={
 ssid="Name of your wireless LAN"
 psk="Password for your wireless LAN"
 priority=10
}

network={
ssid="Name of your other wireless LAN"
psk="Password for your other wireless LAN"
priority=20
}
```

### Additional troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).
