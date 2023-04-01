---
title: "Raspberry Pi Setup Guide"
linkTitle: "Raspberry Pi Setup"
weight: 15
type: "docs"
description: "Image a Raspberry Pi to prepare it for viam-server installation."
image: "/installation/img/thumbnails/raspberry-pi-4-b-2gb.jpg"
imageAlt: "Raspberry Pi"
aliases:
    - /getting-started/rpi-setup/
    - /installation/rpi-setup/
# SME: James
---

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/drl2p2of-qA">}}
<br>

To install the Viam [RDK](/appendix/glossary/#rdk_anchor), you need a Raspberry Pi running a 64-bit Linux distribution.

If you already have a 64-bit Linux distribution installed on your Pi, skip ahead to [enable the required communication protocols for your hardware](#enable-communication-protocols).

{{%expand "Click to check whether the Linux installation on your Raspberry Pi is 64-bit" %}}

If you already have a 64-bit Linux distribution installed on your Pi, you can skip ahead to [installing `viam-server`](../../#install-viam-server).
To check whether the Linux installation on your Raspberry Pi is 64-bit (required for running viam-server), `ssh` into your Pi and then run `lscpu`.

Example output:

![Screenshot of a terminal running the "lscpu" command. The output lists of this command on a Raspberry Pi. A red box highlights the command and the top of the output which reads "Architecture: aarch64."](../../img/rpi-setup/lscpu-output.png)

If the value of "Architecture: _'xxxxxx'_" ends in "64", you can skip ahead to [installing `viam-server`](../../#install-viam-server).

{{% /expand%}}

## Hardware requirements

* A [Raspberry Pi single board computer](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
* A microSD card
* An internet-connected computer
* A way to connect the microSD card to the computer (microSD slot or microSD reader)

## Install Raspberry Pi OS

To install Raspberry Pi OS (formerly called Raspbian) on a microSD card from which the Pi boots, connect the microSD card to your computer.

1. Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) and launch it.

    ![Raspberry Pi Imager launcher window showing a "Choose OS" and "Choose Storage" buttons.](../../img/rpi-setup/imager-launch-screen.png)

2. Select `CHOOSE OS`.
   Click on `Raspberry Pi OS (other)`.
   ![Raspberry Pi Imager window showing "Raspberry Pi OS (Other) is selected.](../../img/rpi-setup/select-other-custom-os.png)
   Select `Raspberry Pi OS Lite (64-bit)` from the  menu.
   ![Raspberry Pi Imager window showing "Raspberry Pi OS Lite (64-bit)" is selected.](../../img/rpi-setup/select-other-rpi.png)
   You should be brought back to the initial launch screen.
3. To make your Raspberry Pi easier to access in the next step, configure your Raspberry Pi's hostname, ssh credentials, and wifi.
   Click the gear-shaped settings icon in the lower right to bring up the Advanced options menu.

   {{% alert title="Note" color="note" %}}
   If you are using a non-Raspberry Pi OS, altering the Advanced options will cause the initial boot to fail.
   {{% /alert  %}}

   ![Raspberry Pi Imager window showing the advanced options menu.](/installation/img/rpi-setup/imager-set-hostname.png)

   Check `Set hostname` and enter the name you would like to access the Pi by in that field.

   There are two ways you can secure your Raspberry Pi: with an SSH key or with password authentication.

   To use the SSH key method: check `Enable SSH`.
   Using SSH Keys for authentication is a great way of securing your Raspberry Pi as only someone with the private SSH key will be able to authenticate to your system.
   If you select `Allow public-key authentication only`, and the section `set authorized_ keys for 'pi'` is pre-populated, that means you do have an existing public SSH key that is ready to use.
   In that case, you do not have to change this section.

   If this section is empty, you can either generate a new SSH key using [these instructions](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), or you can use password authentication instead.

   ![Raspberry Pi Imager window showing "Set Hostname" and "Enable SSH" both selected.](/installation/img/rpi-setup/imager-set-ssh.png)

   If you decide to use the password authentication method: click on `Use password authentication`.
   If you scroll down, you have the option to change the username, then to set a password:

   ![Raspberry Pi Imager window showing the "Set username and password" option is selected.](/installation/img/rpi-setup/imager-set-passwordauthentication.png)

    {{% alert title="Tip" color="tip" %}}
Be sure that you remember the `hostname`, `username`, and `password` you use, as you will need this when you SSH into your Pi.
    {{% /alert  %}}

    {{< alert title="Caution" color="caution" >}}
The default username and password on Raspberry Pis are

* username: pi
* password: raspberry

However, it's bad practice to keep the default username and password on a Raspberry Pi since doing so makes it easy for hackers to get access to your Pi.
In the past, malware infected thousands of Raspberry Pi devices that were using the default username and password.

Source: [https://www.zdnet.com/article/linux-malware-enslaves-raspberry-pi-to-mine-cryptocurrency/](https://www.zdnet.com/article/linux-malware-enslaves-raspberry-pi-to-mine-cryptocurrency/)
    {{< /alert >}}

    Lastly, you should connect your Pi to Wi-Fi, so that you can run `viam-server` wirelessly.
    Check `Configure wireless LAN` and enter your wireless network credentials.
    SSID (short for Service Set Identifier) is your Wi-Fi network name, and password is the network password.
    Change the section `Wireless LAN country` to where your router is currently being operated and then hit save:
    ![Raspberry Pi Imager window showing the "Configure wireless LAN" option selected with SSID and password information for a wireless network.](../../img/rpi-setup/imager-set-wifi.png)

    This should return you to the initial screen.

4. Now you need to pick your storage medium, so click `CHOOSE STORAGE`:

    ![Raspberry Pi Imager window showing the main page, and the "Choose Storage" button is selected.](../../img/rpi-setup/imager-selected-os.png)

    You may have many devices listed, select the microSD card you intend to use in your Raspberry Pi.
    If this page is blank and you do not have any listed, make sure your microSD card is connected to your computer correctly:

    ![The storage screen is shown with a generic SD card available as an option.](../../img/rpi-setup/imager-select-storage.png)

5. After clicking save, double check your OS and Storage settings and then click `WRITE`:

    ![A warning is shown that says "All existing data on the SD card will be erased. Are you sure that you want to continue?"](../../img/rpi-setup/imager-write-confirm.png)

    You will be prompted to confirm erasing your microSD card: select `YES`.
    You may also be prompted by your operating system to enter an Administrator password:

    ![macOS admin password confirmation screen.](../../img/rpi-setup/imager-permission.png)

    After granting permissions to the Imager, it will begin writing and then verifying the Linux installation to the MicroSD card:

    ![The Raspberry Pi Imager will display information on the status of the write.](../../img/rpi-setup/imager-writing.png)

    Remove the microSD card from your computer when it is complete:

    ![You will be notified with a dialogue box informing you that Raspberry Pi OS Lite has been written successfully."](../../img/rpi-setup/imager-done.png)

6. Place the SD card into your Raspberry Pi and boot the Pi by plugging it in to an outlet.
    A red LED will turn on to indicate that the Pi is connected to power.

## Connect with SSH

Once your Raspberry Pi is plugged in and turned on, wait a minute to let your Pi boot up.

Launch your terminal on your computer and run this command:

{{% alert title="Tip" color="tip" %}}
The text in <> should be replaced (including the < and > symbols themselves) with the user and host names you configured when you set up your Pi.

Example: if your username is 'USERNAME' and your hostname is 'pi': then it should be `ssh USERNAME@pi.local`

{{% /alert  %}}

```bash
ssh <USERNAME>@<HOSTNAME>.local
```

If you are prompted "Are you sure you want to continue connecting?", type "yes" and hit enter.
Then, enter your password.
You should be greeted by a login message and a command prompt.

Next, it's good practice to update your Raspberry Pi to ensure all the latest packages are installed:

```bash
sudo apt update
sudo apt upgrade
```

## Enable Communication Protocols

If you are using hardware that requires I2C, SPI, serial, or one-wire protocols to communicate with your Pi, you will need to enable them using `raspi-config`.

Launch the config tool by running the following command:

```bash
sudo raspi-config
```

Use your keyboard to select "Interface Options" and enable the relevant protocols.

![Screenshot of the Raspi Config screen with a red box and red arrow pointing to the "3 Interface Options" option where you can find the I2C and other drivers](../../img/rpi-setup/Installation-Raspberry-Pi-I2C-Raspi-Config-Interfacing-Options.png)

{{< alert title="Note" color="note" >}}
When using a CSI camera, you need to enable legacy camera support.
{{< /alert >}}

For these changes to take effect, you need to restart your Raspberry Pi if it hasn't already prompted you to do so.

```bash
sudo reboot
```

## Next Steps

Now that your Pi has a Viam-compatible operating system installed, and you learned how to enable specific communication protocols and add additional Wifi credentials, continue to [install `viam-server`](../../#install-viam-server).

## Troubleshooting

### Add additional Wifi credentials

If you move your robot to a different Wifi network, you will have to update the Wifi credentials.

You can update the Wifi configuration by creating a new `wpa_supplicant.conf` file on the "boot" partition.

The steps are explained below.

1. Plug your Pi's microSD card into your computer and create a plain text file called `wpa_supplicant.conf`.

2. Paste the following example into the file, replacing "Name of your wireless LAN" and "Password for your wireless LAN" with your credentials.
   Be sure to use UNIX (LF) line breaks in your text editor.

3. Save the file and eject the microSD card.

4. Put the microSD card back into the Pi and boot the Pi.

The `wpa_supplicant.conf` file will be read by the Pi on boot, and the file will disappear but the Wifi credentials will be updated.

You can duplicate the "network" section to add additional Wifi networks (for example your work, and your home).

The "priority" attribute is optional and can be used to prioritize networks if multiple networks are configured (higher numbers are prioritized).

```bash  {class="line-numbers linkable-line-numbers"}
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

## Next Steps

Now that your Pi has a Viam-compatible operating system installed, and you learned how to enable specific communication protocols and add additional Wifi credentials, continue to our [`viam-server` installation guide](../../#install-viam-server).
