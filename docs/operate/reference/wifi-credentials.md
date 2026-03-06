---
title: "Add WiFi Credentials to a Raspberry Pi"
linkTitle: "Add WiFi Credentials"
weight: 96
type: "docs"
description: "Update or add WiFi network credentials on a Raspberry Pi."
date: "2022-01-01"
---

If you move your Raspberry Pi to a different WiFi network, you will have to update the WiFi credentials.

You can update the WiFi configuration by creating a new `wpa_supplicant.conf` file on the "boot" partition:

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
