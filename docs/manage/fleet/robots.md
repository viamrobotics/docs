---
title: "Manage Robots"
linkTitle: "Robots"
weight: 10
type: "docs"
description: "A robot is an organizational concept, consisting of either one or multiple parts working closely together to complete tasks."
tags: ["fleet management", "cloud", "app"]
images: ["/manage/control.gif"]
---

A robot is an organizational concept, consisting of either one <em>{{< glossary_tooltip term_id="part" text="part" >}}</em>, or multiple _parts_ working closely together to complete tasks.
The robot represents the configuration and entry point for one or more computers (and the components they control) coupled into one logical grouping of parts that work together to complete tasks.
A robot usually reflects a physical device, from a camera collecting images, to a wheeled rover, or an articulated arm on a factory floor.
A robot always has a main part that receives client requests, and any number of other parts.

## Add a new robot

Add a new robot by providing a name in the **New Robot** field and clicking **Add robot**.

![The 'First Location' page on the Viam app with a new robot name in the New Robot field and the Add robot button next to the field highlighted.](/manage/app-usage/create-robot.png)

Click the name of a robot to go to that robot's page, where you'll find a variety of tools for working with your robot.

## Navigating the robot page

The banner at the top of the robot page displays the robot's location, name, and a drop down list of all {{< glossary_tooltip term_id="part" text="parts" >}} of that robot.

If you've connected your robot to a machine running `viam-server`, the banner also displays when the robot was last online, which version of `viam-server` it is running, the host name, the IP address or addresses, and its operating system.

![The robot page with menu tabs](/manage/app-usage/robot-page.png)

For each robot in your fleet, you start by setting up the robot on the **Setup** tab:

### Setup

The **Setup** tab contains information for starting an instance of `viam-server` on your robot's computer.

Once you select the correct **Architecture** for your system in the upper left of the tab, follow the instructions on the page to connect and set up your robot.

{{% alert title="Tip" color="tip" %}}
More in-depth information on installing `viam-server` can be found in our [Install Guide](/installation/#install-viam-server).
{{% /alert %}}

### Configuration

When a robot or a {{< glossary_tooltip term_id="part" text="robot part" >}} that is managed with the Viam app first comes online, it requests its configuration from the [Viam app](https://app.viam.com).
Once the robot has a configuration, it caches it locally and can use the configuration for up to 60 days.
The robot checks for new configurations every 15 seconds and changes its configuration automatically when a new configuration is available.

After connecting your robot, go to the **Config** tab, and start adding robot {{< glossary_tooltip term_id="component" text="components" >}}, {{< glossary_tooltip term_id="service" text="services" >}}, and other {{< glossary_tooltip term_id="resource" text="robot resources" >}}.

For more information, see the [configuration documentation](../../configuration/#the-config-tab).

{{< alert title="Tip" color="tip" >}}
If you are managing a large fleet, you can use {{< glossary_tooltip term_id="fragment" text="fragments" >}} when [configuring your robot](../../configuration/).
{{< /alert >}}

### History

The configuration of your robot and the code it runs are kept separate to make debugging easier.
The **History** tab shows timestamped changes to your robot's configuration.

If you want to revert changes that you made, you can load a previous configuration by clicking the **Load config** button next to the respective configuration.

{{<gif webm_src="/manage/load-prev-config.webm" mp4_src="/manage/load-prev-config.mp4" alt="Load a previous config from the UI" max-width="800px">}}

You can also change your timestamp format to ISO or Local depending on your preference.

### Logs

To make debugging issues with your robots easier, each robot automatically sends its logs to the cloud.
You can access your logs from the **Logs** tab in the [Viam app](https://app.viam.com) and filter your logs for specific keywords or log levels:

{{<gif webm_src="/manage/log-filtering.webm" mp4_src="/manage/log-filtering.mp4" alt="Filter logs by term of log level in the UI" max-width="800px">}}

You can also change your timestamp format to ISO or Local depending on your preference.

### Control

Once you have configured components and services for your robot, you can visually test and remotely operate them from the **Control** tab in the [Viam app](https://app.viam.com).
For example, if you have configured a base with wheels, you can control your robot's movement with an arrow pad and fields to change base’s speed.
If you have configured a camera component, a window in the **Control** tab displays the camera output.

If you use remote control in the [Viam app](https://app.viam.com) UI, all communication to the robot uses [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection).
For local communication between [parts](../../parts-and-remotes/#robot-parts) Viam uses gRPC or WebRTC.

{{<gif webm_src="/manage/control.webm" mp4_src="/manage/control.mp4" alt="Using the control tab" max-width="800px">}}

<br>

You can also access the control interface using the [Viam mobile app](/manage/fleet/#the-viam-mobile-app), which you can find on the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) and on [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).

### Code Sample

To start programming your robot, go to the **Code sample** tab which contains boilerplate code snippets you can copy and paste into your SDK code to connect to your robot.

{{% snippet "show-secret.md" %}}

For more information on the SDKs, see [Program your Robot with Viam's SDKs](../../../program/apis/).

There is also a JSON stub you can copy if you wish to have your robot communicate with another robot as a [remote](../../parts-and-remotes/).

### Security

Your robot and the Viam app communicate securely using [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection) with unique secrets.

The **Security** tab allows you to access and change the **Robot part API keys** of your robot.

![The Security tab of a robot`s page noting the Robot part API keys drop-down menu, with the clipboard icon on the far right and the Generate Key button underneath the drop-down.](/manage/app-usage/robot-secrets.png)

Copy the part secret key by clicking on the clipboard icon.
Click on the **Generate Key** button to generate a new key.

{{% snippet "secret-share.md" %}}

## Delete a robot

You can delete a robot by navigating to its page in [the Viam app](https://app.viam.com) and selecting **Sure?** and **Delete robot** in the lower left corner of the page.

{{< imgproc alt="The delete robot button and the confirmation checkbox (Sure?) next to it." src="/manage/app-usage/delete.png" resize="300x" >}}
