---
title: "Raspberry Pi Setup Guide"
linkTitle: "Raspberry Pi Setup"
weight: 15
type: "docs"
description: "A guide to imaging a Pi, installing viam-server and syncing the Pi with the Viam app."
# SME: James
---

## Prerequisites

This tutorial requires the following hardware:

* A Raspberry Pi single board computer
* A microSD card
* An internet-connected computer
* A way to connect the microSD card to the computer (ex, microSD slot or microSD reader)

### Identifying the architecture of your Raspberry Pi

Before installing the Viam [RDK](/appendix/glossary/#rdk_anchor), you will need a Raspberry Pi running a 64-bit Linux distribution.
If you do not have Linux installed on your Raspberry Pi, skip ahead to [Installing Raspian on the Raspberry Pi](#installing-raspian-on-the-raspberry-pi).
If you already have a Raspberry Pi with Linux installed on it, check if the Linux installation on your Raspberry Pi is 64-bit.
First, `ssh` into your Pi and then run `lscpu`.
Example output:

![Screenshot of a terminal running the "lscpu" command. The output lists of this command on a Raspbery Pi. A red box highlights the command and the "Architecture: aarch64.](../../getting-started/img/rpi-setup/lscpu-output.png)

If the value of “Architecture: _'xxxxxx'_” ends in "64", you can skip ahead to [installing viam-server](#follow-the-steps-on-the-setup-tab).
Otherwise continue to [Installing Raspian on the Raspberry Pi](#installing-raspian-on-the-raspberry-pi).

## Installing Raspian on the Raspberry Pi

A Raspberry Pi boots from a microSD card.
The first step is to set up a Linux installation on that microSD card.
Connect the microSD card to your computer.

You will be using the Raspberry Pi Imager to flash the microSD card.

{{% alert title="Note" color="note" %}}
If you do not already have the <a href="https://www.raspberrypi.com/software/" target="_blank">Raspberry Pi Imager</a>, you can download and follow the installation instructions.
{{% /alert  %}}

After installing successfully, connect your microSD card to your computer and launch the Raspberry Pi Imager.
You should be greeted with a window that looks like:

![Raspberry Pi Imager launcher window showing a "Choose OS" and "Choose Storage" buttons.](../../getting-started/img/rpi-setup/imager-launch-screen.png)

Select `CHOOSE OS`.
Since you need a 64-bit version of Linux, you will need to select it from the `Rapsberry Pi OS (other)` menu.

![Raspberry Pi Imager window showing "Raspberry Pi OS (Other) is selected.](../../getting-started/img/rpi-setup/select-other-custom-os.png)

Then select the entry titled `Raspberry Pi OS Lite (64-bit)`.

![Raspberry Pi Imager window showing "Raspberry Pi OS Lite (64-bit)" is selected.](../../getting-started/img/rpi-setup/select-other-rpi.png)

You should be brought back to the initial launch screen.
To make your Raspberry Pi easier to access in the next step, it's recommended that you configure your Raspberry Pi's hostname, ssh credentials, and wifi now.
Click the gear-shaped settings icon in the lower right to bring up the Advanced options menu.

{{% alert title="Note" color="note" %}}
If you are using a non-Raspberry Pi OS, altering the Advanced options will cause the initial boot to fail.
{{% /alert  %}}

![Raspberry Pi Imager window showing the advanced options menu.](../../getting-started/img/rpi-setup/imager-set-hostname.png)

Check `Set hostname` and enter the name you would like to access the Pi by in that field.

There are two ways you can secure your Raspberry Pi: You can either use an SSH key or password authentication.

To use the SSH key method: check `Enable SSH`.
Using SSH Keys for authentication is a great way of securing your Raspberry Pi as only someone with the private SSH key will be able to authenticate to your system.
If you select `Allow public-key authentication only`, and the section `set authorized_ keys for 'pi'` is pre-populated, that means you do have an existing public SSH key that is ready to use.
In that case, you do not have to change this section.

If this section is empty, you can either generate a new SSH key using <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent" target="_blank">these instructions</a>[^sshkey], or you can use password authentication instead.

[^sshkey]:SSH Key Generation: <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent" target="_blank">ht<span></span>tps://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent</a>

![Raspberry Pi Imager window showing "Set Hostname" and "Enable SSH" both selected.](../../getting-started/img/rpi-setup/imager-set-ssh.png)

If you decide to use password authentication method: click on `Use password authentication`.
If you scroll down, you have the option to change the username, then to set a password:

![Raspberry Pi Imager window showing the "Set username and password" option is selected.](../../getting-started/img/rpi-setup/imager-set-passwordauthentication.png)

{{% alert title="Tip" color="tip" %}}
Be sure that you remember the `hostname`, `username`, and `password` you use, as you will need this when you SSH into your Pi.
{{% /alert  %}}

{{< alert title="Caution" color="caution" >}}
The default username and password on Raspberry Pi's are

* username: pi
* password: raspberry
  
However, it's bad practice to keep the default username and passwords on a Raspberry Pi since they make it easy for hackers to get access to your Pi.
In the past, a malware infected thousands of Raspberry Pi devices that were using the default username and password.

Source: <a href="https://www.zdnet.com/article/linux-malware-enslaves-raspberry-pi-to-mine-cryptocurrency/" target="_blank">ht<span></span>tps://www.zdnet.com/article/linux-malware-enslaves-raspberry-pi-to-mine-cryptocurrency/</a>
{{< /alert >}}

Lastly, you should connect your Pi to Wi-Fi, so that you can run viam-server wirelessly.
Check `Configure wireless LAN` and enter your wireless network credentials.
SSID (short for Service Set Identifier) is your Wi-Fi's name, followed by password.
Change the section `Wireless LAN country` to where your router is currently being operated and then you will hit save:
![Raspberry Pi Imager window showing the "Configure wireless LAN" option selected with SSID and password information for a wireless network.](../../getting-started/img/rpi-setup/imager-set-wifi.png)

This should return you to the initial screen.
Now you need to pick your storage medium, so click `CHOOSE STORAGE`:

![Raspberry Pi Imager window showing the main page, and the "Choose Storage" button is selected.](../../getting-started/img/rpi-setup/imager-selected-os.png)

You may have many devices listed, select the microSD card you intend to use in your Raspberry Pi.
If this page is blank and you do not have any listed, make sure your microSD card is connected to your computer correctly:

![The storage screen is shown with a generic SD card is available as an option.](../../getting-started/img/rpi-setup/imager-select-storage.png)

After clicking save, double check your OS and Storage settings and then click `WRITE`:

![A warning is shown that says "All exisiting data on the SD card will be erased. Are you sure that you want to continue?"](../../getting-started/img/rpi-setup/imager-write-confirm.png)

You will be prompted to confirm erasing your microSD card: select `YES`.
You may also be prompted by your operating system to enter an Administrator password:

![macOS admin password confirmation screen.](../../getting-started/img/rpi-setup/imager-permission.png)

After granting permissions to the Imager, it will begin writing and then verifying the Linux installation to the MicroSD card:

![The Rasperberry Pi Imager will display information on the status of the write.](../../getting-started/img/rpi-setup/imager-writing.png)

Remove the microSD card from your computer when it is complete:

![You will be notified with a dialouge box informing you that Raspberry Pi OS Lite has been written successfully."](../../getting-started/img/rpi-setup/imager-done.png)

Place the SD card into your Raspberry Pi and boot the Pi by plugging it in to an outlet.
A red led will turn on to indicate its on.

## Connecting to your Pi with SSH

Once your Raspberry Pi is plugged in and turned on, wait a minute to let your Pi boot up.

Launch your terminal on your computer and run this command:

{{% alert title="Tip" color="tip" %}}
The text in <> should be replaced (including the < and > symbols themselves) with the user and host names you configured when you setup your Pi.

Example: if your username is 'USERNAME' and your hostname is 'pi': then it should be `ssh USERNAME@pi.local`

{{% /alert  %}}

```bash
ssh <USERNAME>@<HOSTNAME>.local
```

If you are prompted “Are you sure you want to continue connecting?”, type “yes” and hit enter.
Then, enter your password.
You should be greeted by a login message and a command prompt.

Next, it's good practice to update your Raspberry Pi to ensure all the latest packages are installed:

```bash
sudo apt update
sudo apt upgrade
```

## Enabling Specific Communication Protocols on the Raspberry Pi

If you are using hardware that requires I2C, SPI, Serial, or one-wire protocols to communicate with your Pi, you will need to enable them via `raspi-config`.

Launch the config tool by running the following command:

```bash
sudo raspi-config
```

Use your keyboard to select "Interface Options" and enable the relevant protocols.

![Screenshot of the Raspi Config screen with a red box and red arrow pointing to the "3 Interface Options" option where you can find the I2C and other drivers](../../getting-started/img/rpi-setup/Installation-Raspberry-Pi-I2C-Raspi-Config-Interfacing-Options.png)

For these changes to take effect, you need to restart your Raspberry Pi if it hasn't already prompted you to do so.

```bash
sudo reboot
```

## Adding your Pi on the Viam app

In your web browser, navigate to the Viam app ([https://app.viam.com](https://app.viam.com)) and log in.

Once you are logged in, a location will be created for you by default, or you can create a new location by filling out the field on the left and then clicking **ADD**.
Location are just a way of organizing robots. You can find more information on [managing robot fleets here](../../product-overviews/fleet-management/#how-to-use-the-viam-app).

![Screenshot from the Viam app showing the add new location page.](../../getting-started/img/rpi-setup/add-location.png)

Select your location and use the form on the right to create a new Robot. If this is the first robot in this location, the app displays an arrow pointer to the **New Robot** field (upper RH-corner). Enter a name for your robot, then click **Add Robot**:

![Screenshot from the Viam app showing the create a robot page.](../../getting-started/img/rpi-setup/add-robot.png)

Navigate to your new robot, which should show the setup page as shown below:

![Screenshot from the Viam app showing the Setup page.](../img/rpi-setup/view-robot.png)

## Follow the steps on the setup tab

Follow the steps on the setup tab to install the Viam software on your Raspberry Pi.

Once you have installed viam-server on your Pi, refresh the page on the Viam app ([https://app.viam.com](https://app.viam.com)) to confirm your Pi has successfully connected and pulled the config by looking at the top of the Robot page and seeing that `host` and `ips` fields are populated and that the `last online` field reads `live`.

You should also see the the notification on the setup page that says "Your robot is connected!"

![Screenshot from the Viam app showing a dialouge box with a greencheckmark and text that reads, "Your robot is successfully connected! Proceed to the config tab."](../img/rpi-setup/your-robot-is-connected.jpg)

## Next Steps

Now that you have the viam-server up and running, you can start configuring your robot and the real fun can begin!

Check out [our list of tutorials](/tutorials/) for step-by-step project walkthroughs demonstrating robot configuration and using Viam's [Python SDK](https://python.viam.dev/) and [Golang SDks](https://pkg.go.dev/go.viam.com/rdk).

If you already have a project in mind, head to your newly connected robot's `CONFIG` tab. Here you can describe the hardware attached to your Pi which will allow Viam to actuate the hardware and expose APIs for it.
Click on `NEW COMPONENT` and then populate the resulting component with the configuration information for your hardware.
Find information on how to configure specific component types in their respective [component](/components/) and [service](/services/) docs.
Once your configuration changes are saved, you can switch to the `CONTROL` tab to actuate your hardware using buttons in the app.
