---
linkTitle: "End-user device setup"
title: "End-user device setup"
weight: 25
layout: "docs"
type: "docs"
description: "Connect a Viam-powered device to your WiFi network using the mobile app or captive portal."
---

If you received a device with Viam pre-installed, follow these instructions to connect it to your WiFi network and complete setup. The method you use depends on how the device manufacturer configured provisioning.

## Prerequisites

- A Viam-powered device (powered off)
- A WiFi network with internet access
- A mobile device or laptop

## Set up with the Viam mobile app

Use this method if the device manufacturer configured Bluetooth provisioning.

1. Install the Viam mobile app from the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) or [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).
1. Open the app and sign in. Select an organization and location for your machine.
1. Create a new machine or select an existing machine that has not been set up.
1. Power on the device. Wait for it to boot and enable Bluetooth (this may take 1-2 minutes).
1. Follow the app's instructions to connect to the device's Bluetooth signal. The device name begins with `viam-setup-` by default.
1. Provide your WiFi network name and password when prompted.
1. Wait for the device to connect to WiFi and complete setup. The machine appears as **Live** in the app when setup is complete.

If the device cannot connect to the provided network, it re-enables Bluetooth and prompts you to try again.

## Set up with the captive portal

Use this method if the device manufacturer configured WiFi hotspot provisioning.

1. Power on the device. Wait for it to boot and create a WiFi hotspot (this may take 1-2 minutes).
1. On your laptop or mobile device, open WiFi settings and connect to the device's hotspot. The hotspot name begins with `viam-setup-` by default. The password is `viamsetup` unless the manufacturer changed it.
1. A captive portal opens automatically. If it does not, open [http://viam.setup/](http://viam.setup/) in a browser.
1. Enter your WiFi network name and password.
1. If prompted, paste your machine cloud credentials. To get these:
   - Log into [app.viam.com](https://app.viam.com).
   - Navigate to your machine's page.
   - Click the part status dropdown next to the machine name.
   - Click the copy icon next to **Machine cloud credentials**.
1. Wait for the device to connect to WiFi and complete setup.

If the device cannot connect, it recreates the hotspot so you can try again.

## Verify the device is online

After setup, the device should appear as **Live** in the Viam app:

- **Mobile app**: check the machine's status in the app.
- **Web app**: navigate to [app.viam.com/fleet/machines](https://app.viam.com/fleet/machines) and confirm the machine shows as online.

## Troubleshooting

### Bluetooth connection issues

- Ensure Bluetooth is enabled on your mobile device and the Viam app has Bluetooth permissions.
- If you previously connected to this device, remove it from your device's Bluetooth settings and try again.
- Power cycle the device to restart Bluetooth advertising.

### WiFi hotspot not visible

- Wait at least 2 minutes after powering on. The device needs time to boot and create the hotspot.
- Confirm the hotspot password. The default is `viamsetup` unless the manufacturer changed it.
- Move closer to the device. The hotspot has limited range.

### Device does not come online after providing WiFi credentials

- Verify the WiFi network name and password are correct.
- Confirm the WiFi network has internet access. Some networks require a captive portal login (hotel WiFi, corporate guest networks) that the device cannot complete.
- Check WiFi band compatibility. Some devices only support 2.4 GHz networks.
- Power cycle the device to restart the provisioning process and try a different network.

## Next steps

Once the device is online, it operates according to its configured fragment. If the device needs access to additional WiFi networks, you can add them through the machine's system settings. See [system settings](/fleet/system-settings/) for details.
