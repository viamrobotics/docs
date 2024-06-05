---
title: "Set up a SparkFun RTK Reference Station"
linkTitle: "SparkFun RTK Reference Station Setup"
weight: 20
type: "docs"
description: "Follow this guide to set up your own SparkFun RTK base station, a high-precision GPS module designed for use with the RTK satellite navigation technique."
images: ["/icons/components/imu.svg"]
# SMEs: Susmita
---

Follow this guide to set up your [SparkFun RTK Reference Station](https://www.sparkfun.com/products/22429), a high-precision GPS module designed for use with the Real-Time Kinematic (RTK) satellite navigation technique.
RTK improves the precision of positional data from satellite-based positioning systems like the Global Positioning System (GPS).
When placed in a known location, the RTK Reference Station calculates and transmits correction data to RTK-enabled GPS receivers based on satellite signals it receives.

After following this guide, you can provide the mount point, username, password, and URL from your reference station's fixed-position NTRIP server in your Viam machine config for the [`gps-nmea-rtk-pmtk`](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/) and [`gps-nmea-rtk-serial`](/components/movement-sensor/gps/gps-nmea-rtk-serial/) models of movement sensor to allow a rover or other machine configured with your sensor to apply corrections from the reference station, enabling your machine to achieve centimeter-level accuracy in positioning.

## Reserve an RTK2GO casting service

To distribute the correction information from your reference station, you should reserve an RTK2GO casting service for your station.

Follow the instructions on [New Base Station Reservation](http://rtk2go.com/sample-page/new-reservation/) to enter information about your reference station.
Wait for the confirmation email, to which you will need to reply.
Upon reply, you will receive a password for your mount point.
Save this, as you will need it later in this set up process.

For more information about the RTK2GO reservation system, see [Reservations](http://rtk2go.com/reservations/).

## Set up the reference station hardware

Insert the microSD card that comes with the Reference Station kit into the microSD card slot:

![microSD card slot highlighted on reference station.](/components/movement-sensor/sparkfun-microsd.png)

Connect the GNSS Surveying Antenna included with the Reference Station kit to the **UBLOX** connector on the kit, and connect the kit's SMA WiFi / Bluetooth Antenna to the **ESP32** connector on the kit:

![UBLOX and ESP32 connections highlighted on reference station.](/components/movement-sensor/sparkfun-connectors.png)

## Bring the antenna outside

Bring the surveying antenna outside, where it can have a clear 360 degree view of the sky.
This enables more accurate correction streaming.

## Power up the reference station

You can power up the base station in several ways, described in the [RTK Reference Station Hookup Guide](https://learn.sparkfun.com/tutorials/sparkfun-rtk-reference-station-hookup-guide?_ga=2.100337244.338983596.1711988256-2122519039.1685030641#hardware-overview).
You can choose to power it up using USB-C or Ethernet (PoE):

![Power and PoE ports highlighted on reference station.](/components/movement-sensor/sparkfun-ethernet.png)

## Configure CfgWiFi mode

**CfgWiFi** mode allows you to configure the reference station through WiFi.
You can also configure it using Ethernet (**Cfg Eth** mode) but for that an Ethernet connection is required, which can be limiting for outdoor setup.

To configure **CfgWiFi** mode, select **CfgWiFi** using the reference kit's **MODE** button.
Press it once to activate the **MODE** menu.
Press the button again to step through the available modes.
Once highlighted, pause on **CfgWiFi** to select this mode.

{{% alert title="Tip" color="tip" %}}
For more information, see the [RTK Reference Station Hookup Guide](https://learn.sparkfun.com/tutorials/sparkfun-rtk-reference-station-hookup-guide#hardware-overview) from SparkFun.
{{% /alert %}}

## Use WiFi to configure the reference station

When **CfgWiFi** mode is selected, the reference station broadcasts its own WiFi called “RTK Config”.

{{% alert title="Note" color="note" %}}
It is highly recommended that you use a hotspot for outdoor usage, such as with rovers.
If you do use a hotspot, configure the reference station on the hotspot network.
Also ensure that the hotspot is set to 2.4GHz and not 5GHz because the reference station can not connect to a network over 2.4GHz.
{{% /alert %}}

Connect your phone or computer to the WiFi network called "RTK Config" and use your web browser (Safari or Internet Explorer are recommended over Chrome) to go to the address `192.168.4.1`, which is the default IP address of the reference station.
At that address you will see the RTK setup configure page displayed:

{{< imgproc src="/components/movement-sensor/sparkfun-configure-page.png" alt="The SparkFun RTK Setup configure page displayed with dropdown menu rows showing different options for configuration." resize="900x" style="width:450px" >}}

### Update System configuration

Look on the top of the RTK setup configure page and ensure that the firmware version of the base station is v4.0 or higher:

{{< imgproc src="/components/movement-sensor/sparkfun-rtk-firmware.png" alt="The top of the SparkFun RTK Setup configure page with the RTK Firmware version displayed as v4.0." resize="1000x" style="width:500px" >}}

This is important since as of April 2024, version 4.0 allows the base station to send [RTCM](https://www.xyht.com/gnsslocation-tech/rtcm/) corrections over WiFi.
To update the version of the firmware to 4.0, select the **System Configuration** dropdown and follow the steps provided in [Updating Firmware Over-The-Air](https://docs.sparkfun.com/SparkFun_RTK_Firmware/firmware_update/#updating-firmware-over-the-air).

### Update GNSS configuration

Select the **GNSS Configuration** dropdown on the RTK setup configure page.
Hover over the subsequent **i** button for more information about an option, including default values and limits.
For each option, select the following:

**Measurement Rate:**

- **In Hz:** 4.00 Hz (default).
- **Seconds between measurements:**: 0.25.

**Dynamic Model:** Portable (default).

**Min SV Elevation:** 10.

**Min C/N0**: Keep the default value here as appropriate to your model, **6dBHz** for ZED-F9P and **20dBHz** for ZED-F9R models.

**Constellations:** Keep the default selections here: **GPS**, **SBAS**, **GLONASS**, **BeiDou**, and **Galileo**.

With these recommended values selected, your GNSS Configuration should look like this:

{{< imgproc src="/components/movement-sensor/sparkfun-GNSS-config.png" alt="Recommended GNSS Configuration." resize="900x" style="width:450px" >}}

Now click on the **Message Rates** box.
In the Message Menu enable the following messages:

- GGA
- GLL
- GNS
- GSV
- RMC
- VTG

This is necessary for this use case because Viam’s RTK driver uses these messages.
Your **Message Rates** option should look like this:

{{< imgproc src="/components/movement-sensor/sparkfun-GNSS-message-rates.png" alt="Recommended GNSS Message Rates Configuration." resize="900x" style="width:450px" >}}

### Update Base configuration

Select the **Base Configuration** dropdown on the RTK setup configure page.

**Survey-In:** Enable the **Survey-In** mode, and configure it as follows:

- **Minimum observation time**: 60 (default).
- **Required Mean 3D standard deviation (m)**: 5.00 (default).

**Fixed**: You only want the **Fixed** mode if your reference station will be stationary at a permanent location.
Keep this deselected.

**Enable NTRIP Server:** Enable this option. Enter the following credentials:

- **Caster Host:** rtk2go.com
- **Caster Port:** 2101
- **Caster User:** [insert your email]
- **Mount Point:** [insert name of mountpoint from your [RTK2GO Casting Service reservation](#reserve-an-rtk2go-casting-service)]
- **Mount Point PW:** [insert password from your [RTK2GO Casting Service reservation](#reserve-an-rtk2go-casting-service)]

For example:

{{< imgproc src="/components/movement-sensor/sparkfun-base-configuration.png" alt="Recommended Base Configuration." resize="900x" style="width:450px" >}}

### Update WiFi configuration

Select the **WiFi Configuration** dropdown on the RTK setup configure page.

**Networks:** Enter credentials for up to 4 WiFi networks.
The device tries all networks and uses the best network available.

**Configure Mode:** WiFi.

Your WiFi configuration should look like this, with the examples replaced with your real values:

{{< imgproc src="/components/movement-sensor/sparkfun-wifi-configuration.png" alt="Example WiFi Configuration." resize="1000x" style="width:500px" >}}

### Update Profile configuration

Select the **Profile Configuration** dropdown on the RTK setup configure page.

Select a profile to assign settings to that profile.
At reset, your RTK device will use the selected settings profile.

Your **Profile Configuration** should look like this:

{{< imgproc src="/components/movement-sensor/sparkfun-profile-configuration.png" alt="Example Profile Configuration." resize="900x" style="width:450px" >}}

### Save your configuration changes

Select **Save Configuration** on the RTK setup configure page and wait for your configurations to take effect.

## Start RTK2GO casting

Using the reference kit's **MODE** button, switch the mode back to the default **Base**.
Press the **MODE** button once to activate the menu.
Press the button again to step through the available modes.
Once highlighted, pause on **Base** to select this mode.

Because you configured the base station to be in **Survey-in** mode in the [update Base configuration step](#update-base-configuration), it will take your base station up to six minutes to go into **Xmitting RTCM** mode.
After a few minutes it goes into **Casting** mode.
Once you see **Casting** on the mode menu display screen, go to `rtk2go.com:2101` in your browser and find your mount point in the source table.

## Next steps: configure an RTK movement sensor

Open the configuration instructions for your RTK-enabled movement sensor model:

- [`gps-nmea-rtk-pmtk`](/components/movement-sensor/gps/gps-nmea-rtk-pmtk/)
- [`gps-nmea-rtk-serial`](/components/movement-sensor/gps/gps-nmea-rtk-serial/)

Follow the configuration instructions, providing the values you entered for your NTRIP server [Base configuration](#update-base-configuration) as the equal attributes in your Viam machine config:

- `ntrip_url`: your RTK2GO casting URL, comprised of **Caster Host** and **Caster Port** (like `rtk2go.com:2101`)
- `ntrip_username`: your **Caster User**, which should be your email
- `ntrip_password`: your **Mount Point PW**
- `ntrip_mountpoint`: your **Mount Point** name

Configuring your movement sensor with your NTRIP casting server access information allows your machine to receive both GPS signals and correction data and apply corrections, increasing the positioning capacity of the movement sensor to centimeter-level accuracy.

## Troubleshooting

If your base station loses the WiFi IP address after set up, then trying to reconfigure it in **ConfigWiFi** mode will not work.
In this case, you must connect the base station to your network through an Ethernet cable and then select **ConfigEth** mode in [Use WiFi to configure the reference station](#use-wifi-to-configure-the-reference-station).
Then, during [Update system configuration](#update-system-configuration) use the IP address displayed on the reference station to connect and configure it.
