---
title: "Complete end-user setup for a machine"
linkTitle: "Set up machine (end-user)"
weight: 69
type: "docs"
description: "If you have a machine that uses Viam and have been pointed to this guide, this guide will show you how to set it up."
images: ["/platform/provisioning-demo.gif"]
videos: ["/platform/provisioning-demo.webm", "/platform/provisioning-demo.mp4"]
languages: []
viamresources: []
platformarea: ["fleet"]
level: "Intermediate"
prev: "/manage/fleet/provision/"
date: "2024-08-21"
aliases:
  - /provision/
# updated: ""  # When the tutorial was last entirely checked
cost: "0"
---

If you have a machine with Viam pre-installed on it, this guide will show you how to complete your device setup using either the [Viam mobile app](#set-up-your-machine-using-the-viam-mobile-app) or the [{{< glossary_tooltip term_id="captive-web-portal" text="captive portal" >}}](#set-up-your-machine-using-the-captive-portal).

Whether you need to use the Viam mobile app or the captive portal, depends on how [provisioning was set up](/manage/fleet/provision/setup/) on your machine.

## Prerequisites

- Physical hardware constituting a machine
- A WiFi-enabled computer, or mobile device (if using the Viam mobile app)

## Set up your machine using the Viam mobile app

{{<video webm_src="/platform/provisioning-demo.webm" mp4_src="/platform/provisioning-demo.mp4" alt="Using the Viam mobile app to provision a new machine with viam-agent." poster="/platform/provisioning-demo.jpg" max-width="300px" class="">}}

{{< table >}}
{{% tablestep start=1 %}}
**Install the Viam mobile app**

You can find the mobile app on the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) and on [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).

<a href="https://apps.apple.com/vn/app/viam-robotics/id6451424162" target="_blank">
  <img src="https://github.com/viamrobotics/docs/assets/90707162/a470b65d-1b97-412f-9f97-daf902f2f053" width="200px" alt="apple store icon" class="center-if-small" >
</a>

<a href="https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US" target="_blank">
  <img src="https://github.com/viamrobotics/docs/assets/90707162/6ebd6960-08c5-41d4-81f9-42293fbfdfd4" width="200px" alt="google play store icon" class="center-if-small" >
</a>

{{% /tablestep %}}
{{% tablestep %}}
**Create a machine**

Open the Viam mobile app and sign in.
Then, select an organization and location for your machine.
Create a new machine or click on an existing machine that has not yet been set up and follow the instructions.

{{% /tablestep %}}
{{% tablestep %}}
**Turn on your machine and follow the app instructions**

Turn on the smart machine you are attempting to connect to.
Then leave the app and navigate to your mobile device's WiFi settings and connect to the WiFi hotspot your machine has created.
You may need to wait a short time for your machine to boot and create its WiFi hotspot.

Select the machine's WiFi hotspot and enter the password.
By default, the name will begin with `viam-setup-` and the password is `viamsetup`.

Return to the Viam mobile app once connected.

{{% /tablestep %}}
{{% tablestep %}}
**Provide the network information for the machine**

In the mobile app, follow the instructions to provide the network information for the machine.

The machine will now disable the hotspot network and attempt to connect using the provided network information.
If the machine cannot establish a connection using the provided network information, the machine will create the hotspot again and prompt you to re-enter the network information until a connection is successfully established.

{{% /tablestep %}}
{{% tablestep %}}
**Wait for machine to complete setup**

If the machine can successfully connect to the network it will now complete its setup and become **live**.

Any features that require internet access will not function if the connected WiFi network is not connected to the internet.
{{% /tablestep %}}
{{< /table >}}

## Set up your machine using the captive portal

{{< table >}}
{{% tablestep start=1 %}}
**Turn on the smart machine**

Turn on the smart machine you are attempting to set up.
{{% /tablestep %}}
{{% tablestep %}}
**Connect to your machine's WiFi hotspot**

On a laptop or mobile device, open your WiFi settings and connect to the WiFi hotspot your machine has created.
You may need to wait a short time for your machine to boot and create its WiFi hotspot.
Select the machine's WiFi hotspot and enter the password.
By default, the name will begin with `viam-setup-` and the password is `viamsetup`.

Once you are connected to your machine's WiFi hotspot you will be redirected to a {{< glossary_tooltip term_id="captive-web-portal" text="captive portal" >}}.
If you are using a laptop or are not redirected, try opening [http://viam.setup/](http://viam.setup/) in a browser.
{{% /tablestep %}}
{{% tablestep %}}
**Follow the captive portal's instructions to provide network information**

In the captive web portal, follow the instructions to provide the network information for the machine.
{{% /tablestep %}}
{{% tablestep %}}
**If prompted, provide a machine cloud credentials configuration**

Depending on how the machine was set up so far, the captive portal may also require you to paste machine cloud credentials.
This is the JSON object which contains your machine part secret key and cloud app address, which your machine needs to connect to Viam.

Log into [Viam](https://app.viam.com), and use an existing machine or create a new machine.

To copy your machine cloud credentials:

- Navigate to your machine's page.
- Select the part status dropdown to the right of your machine's name on the top of the page.
  {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Machine part info dropdown" class="shadow" >}}
- Click the copy icon next to **Machine cloud credentials**.
- Paste the credentials when prompted.

{{% /tablestep %}}
{{% tablestep %}}
**Wait for machine to complete setup**

The machine will now disable the hotspot network and attempt to connect using the provided network information.
If the machine cannot establish a connection using the provided network information, the machine will create the hotspot again and prompt you to re-enter the network information until a connection is successfully established.

If the machine can successfully connect to the network it will now complete its setup and become **live**.

Any features that require internet access will not function if the connected WiFi network is not connected to the internet.
{{% /tablestep %}}
{{< /table >}}

## Troubleshooting

### Bluetooth connection issues

If you're having trouble with Bluetooth provisioning:

1. **Check Bluetooth permissions**: Ensure the app used for provisioning has [Bluetooth permissions enabled](https://github.com/viamrobotics/viam_flutter_bluetooth_provisioning_widget?tab=readme-ov-file#platform-requirements) on your device.

1. **Verify Bluetooth is enabled**: Make sure Bluetooth is turned on in your mobile device settings.

1. **Restart Bluetooth**: Try turning Bluetooth off and on again on your mobile device.

1. **Remove and re-add**: If you've already connected to the machine over Bluetooth, remove or forget the device from your mobile device's settings, and re-add it.

If you can open a terminal on the machine:

1. Check if Bluetooth is available:

   ```sh {class="command-line" data-prompt="$"}
   bluetoothctl list
   ```

1. Restart Bluetooth service:

   ```sh {class="command-line" data-prompt="$"}
   sudo systemctl restart bluetooth
   ```

1. **Configuration check**: If you set up provisioning, verify that `disable_bt_provisioning` is set to `false` in your configuration.

### WiFi connection issues

If you cannot connect to your machine's temporary WiFi hotspot, confirm you are using the correct password.
The default password, unless changed by the manufacturer, is `viamsetup`,

If your machine cannot connect to your permanent office or home WiFi network:

1. **Check network credentials**: Verify that the WiFi network name (SSID) and password are correct.

1. **Check network compatibility**: Ensure your WiFi network is compatible with your machine's WiFi band frequency (2.4ghz vs 5ghz).

1. **Try a different network**: If possible, try connecting to a different WiFi network to isolate the issue.

## Next Steps

The machine is now usable.

If the machine needs to be able to connect to more than one WiFi network, you can add additional networks in the [`viam-agent` network configuration](/manage/reference/viam-agent/#network_configuration).
You can also override other configuration details in the [`viam-agent` configuration](/manage/reference/viam-agent/#configuration).
