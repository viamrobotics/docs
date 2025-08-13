---
title: "Complete end-user setup for a machine"
linkTitle: "Set up machine (end-user)"
weight: 69
type: "docs"
description: "If you have received a machine that uses Viam and have been pointed to this guide, this guide will show you how to set it up."
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

If you have received a machine with Viam pre-installed on it, this guide will show you how to complete your device setup using either the [Viam mobile app](#set-up-your-machine-using-the-viam-mobile-app) or the [{{< glossary_tooltip term_id="captive-web-portal" text="captive portal" >}}](#set-up-your-machine-using-the-captive-portal).

Unless you have been told to use the captive portal, we recommend you use the Viam mobile app.

## Prerequisites

- Physical hardware constituting a machine
- A WiFi-enabled computer, or mobile device (if using the Viam mobile app)

## Set up your machine using the Viam mobile app

{{<video webm_src="/platform/provisioning-demo.webm" mp4_src="/platform/provisioning-demo.mp4" alt="Using the Viam mobile app to provision a new machine with viam-agent." poster="/platform/provisioning-demo.jpg" max-width="300px" class="">}}

{{< table >}}
{{% tablestep number=1 %}}
**Install the Viam mobile app**

You can find the mobile app on the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) and on [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).

<a href="https://apps.apple.com/vn/app/viam-robotics/id6451424162" target="_blank">
  <img src="https://github.com/viamrobotics/docs/assets/90707162/a470b65d-1b97-412f-9f97-daf902f2f053" width="200px" alt="apple store icon" class="center-if-small" >
</a>

<a href="https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US" target="_blank">
  <img src="https://github.com/viamrobotics/docs/assets/90707162/6ebd6960-08c5-41d4-81f9-42293fbfdfd4" width="200px" alt="google play store icon" class="center-if-small" >
</a>

{{% /tablestep %}}
{{% tablestep number=2 %}}
**Create a machine**

Open the Viam mobile app and sign in.
Then, select an organization and location for your machine.
If you have already created a machine, select it.
If you have not yet created a machine, click on **Add new smart machine** and give your machine a name.
{{% /tablestep %}}
{{% tablestep number=3 %}}
**Follow the instructions in the app**

Turn on the smart machine you are attempting to connect to.
Then leave the app and navigate to your mobile device's WiFi settings and connect to the WiFi hotspot your machine has created.
You may need to wait a short time for your machine to boot and create its WiFi hotspot.
Your machine's WiFi hotspot name will begin with `viam-setup-`.
Unless you have been given other instructions, the WiFi password for this hotspot network is `viamsetup`.

Once you are connected to your machine's WiFi hotspot return to the Viam mobile app.
{{% /tablestep %}}
{{% tablestep number=4 %}}
**Provide the network information for the machine**

In the mobile app, you will be prompted to provide the network information for the machine.

The machine will now disable the hotspot network and attempt to connect using the provided network information.
If the machine cannot establish a connection using the provided network information, the machine will create the hotspot again and prompt you to re-enter the network information until a connection is successfully established.
{{% /tablestep %}}
{{% tablestep number=5 %}}
**Wait for machine to complete setup**

If the machine can successfully connect to the network it will now complete its setup and become **live**.

Note that any features that require internet access will not function if the connected WiFi network is not connected to the internet.
{{% /tablestep %}}
{{< /table >}}

## Set up your machine using the captive portal

{{< table >}}
{{% tablestep number=1 %}}
**Turn on the smart machine**

Turn on the smart machine you are attempting to set up.
{{% /tablestep %}}
{{% tablestep number=2 %}}
**Connect to your machine's WiFi hotspot**

On a laptop or mobile device, navigate to your WiFi settings and connect to the WiFi hotspot your machine has created.
You may need to wait a short time for your machine to boot and create its WiFi hotspot.
Your machine's WiFi hotspot name will begin with `viam-setup-`.
Unless you have been given other instructions, the WiFi password for this hotspot network is `viamsetup`.

Once you are connected to your machine's WiFi hotspot you will be redirected to a sign-in page.
If you are using a laptop or are not redirected, try opening [http://viam.setup/](http://viam.setup/) in a browser.
{{% /tablestep %}}
{{% tablestep number=3 %}}
**Follow the captive portal's instructions to provide network information**

In the captive web portal, you will then be prompted to provide the network information for the machine.
{{% /tablestep %}}
{{% tablestep number=4 %}}
**If prompted, provide a machine cloud credentials configuration**

Depending on how the machine was set up so far, the captive portal may also require you to paste machine cloud credentials.
This is the JSON object which contains your machine part secret key and cloud app address, which your machine's `viam-server` instance needs to connect to Viam.

On [Viam](https://app.viam.com), create a new machine.

To copy your machine cloud credentials:

- Navigate to your machine's page.
- Select the part status dropdown to the right of your machine's name on the top of the page.
  {{<imgproc src="configure/machine-part-info.png" resize="500x" declaredimensions=true alt="Machine part info dropdown" class="shadow" >}}
- Click the copy icon next to **Machine cloud credentials**.
- Paste the credentials when prompted.

{{% /tablestep %}}
{{% tablestep number=5 %}}
**Wait for machine to complete setup**

The machine will now disable the hotspot network and attempt to connect using the provided network information.
If the machine cannot establish a connection using the provided network information, the machine will create the hotspot again and prompt you to re-enter the network information until a connection is successfully established.

If the machine can successfully connect to the network it will now complete its setup and become **live**.

Note that any features that require internet access will not function if the connected WiFi network is not connected to the internet.
{{% /tablestep %}}
{{< /table >}}

## Next Steps

You can now use your machine.

If your machine needs to be able to connect to more than one WiFi network, you can add additional networks in the [`viam-agent` network configuration](/manage/reference/viam-agent/#network_configuration).
You can also override other configuration details in the [`viam-agent` configuration](/manage/reference/viam-agent/#configuration).

To control your machine, you can navigate to its **CONTROL** tab.
