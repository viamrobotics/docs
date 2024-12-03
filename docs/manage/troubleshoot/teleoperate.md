---
title: "Teleoperate"
linkTitle: "Teleoperate"
weight: 20
type: "docs"
description: "Use the Viam app control tab or the Viam mobile app to monitor and remotely operate your machines."
tags: ["teleop", "fleet management", "control", "app"]
languages: []
viamresources: ["sensor", "camera", "movement sensor"]
platformarea: ["viz", "data"]
images: ["/how-tos/teleop/full-workspace.png"]
level: "Intermediate"
date: "2024-11-13"
# updated: ""  # When the content was last entirely checked
cost: "0"
---

You can remotely control, test, and operate any configured machine using a [custom control interface](#custom-control-interface) or the [default control interface](#default-control-interface).

## Custom control interface

Create a custom teleop workspace to operate a machine and visualize and aggregate its data.

### Prerequisites

{{% expand "A configured machine with teleoperable components" %}}

Make sure your machine has at least one camera, movement sensor, sensor, base, arm, board, gantry, gripper, motor or servo.

See [configure a machine](/how-tos/configure/) for more information.

{{% /expand%}}

### Configure a workspace

{{< table >}}
{{% tablestep %}}
**1. Create a workspace in the Viam app**

Log in to the [Viam app](https://app.viam.com/).

Navigate to the **FLEET** page's **TELEOP** tab.
Create a workspace by clicking **+ Create workspace**.
Give it a name.

{{<imgproc src="/how-tos/teleop/blank-workspace.png" resize="800x" style="width: 500px" class="fill aligncenter imgzoom" declaredimensions=true alt="Blank teleop page.">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Add widgets**

Click **Add widget** and select the appropriate widget for your machine.
Repeat as many times as necessary.

Now your workspace setup is complete:

{{<imgproc src="/how-tos/teleop/configured-workspace.png" resize="700x" style="width: 500px" class="fill aligncenter" declaredimensions=true alt="Teleop workspace with values configured for each of the four widgets.">}}

{{% /tablestep %}}
{{% tablestep %}}
**3. Select a machine**

Now, select a machine with which to make your teleop workspace come to life.
Select **Monitor** in the top right corner to leave editing mode.
Click **Select machine** and select your configured machine.

Your dashboard now shows the configured widgets for the data from your machine:

{{<imgproc src="/how-tos/teleop/full-workspace.png" resize="900x" style="width: 500px" class="fill aligncenter imgzoom" declaredimensions=true alt="Teleop workspace with values configured for each of the four widgets on monitor mode.">}}

You can go back to **Edit** mode and drag and drop the widgets' panes around to edit their appearance.
For example:

{{<imgproc src="/how-tos/teleop/four-panes.png" resize="900x" style="width: 500px" class="fill aligncenter imgzoom" declaredimensions=true alt="Teleop workspace with values configured for each of the four widgets on monitor mode with four panes.">}}

{{% /tablestep %}}
{{< /table >}}

## Default control interface

### Viam app

The **CONTROL** tab provides a control interface for each component and service that you have configured for you machine.

For example, if you have configured a base with wheels, you can move your machine's with an arrow pad and control the base's speed by setting its power with a slider.
If you have configured a camera component, a window in the **CONTROL** tab displays the camera output.

{{<gif webm_src="/fleet/control.webm" mp4_src="/fleet/control.mp4" alt="Using the control tab" max-width="800px">}}

You can also switch between different machine parts directly from the **CONTROL** tab and control the selected machine part.

### Viam mobile app

{{<gif webm_src="/fleet/mobile-app-control.webm" mp4_src="/fleet/mobile-app-control.mp4" alt="Using the control interface under the locations tab on the Viam mobile app" class="alignright" max-width="300px">}}

In addition to the Viam app, the [Viam mobile app](/fleet/control/#control-interface-in-the-viam-mobile-app) also allows you to test, monitor and remotely operate machines in your fleet.

For example, you can view live camera feeds, adjust components' runtime parameters, and switch between controllable components.

Additionally, the app allows you to:

- see if your machines are online
- [view a machine's logs](/cloud/machines/#logs)
- [upload images from your phone to the cloud](/how-tos/upload-data/#upload-images-with-the-viam-mobile-app)
- [invite people to collaborate with you and modify access](/cloud/rbac/#use-the-mobile-app)

<br>

You can find the mobile app on the [App Store](https://apps.apple.com/vn/app/viam-robotics/id6451424162) and on [Google Play](https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US).

<a href="https://apps.apple.com/vn/app/viam-robotics/id6451424162" target="_blank">
  <img src="https://github.com/viamrobotics/docs/assets/90707162/a470b65d-1b97-412f-9f97-daf902f2f053" width="200px" alt="apple store icon" class="center-if-small" >
</a>

<a href="https://play.google.com/store/apps/details?id=com.viam.viammobile&hl=en&gl=US" target="_blank">
  <img src="https://github.com/viamrobotics/docs/assets/90707162/6ebd6960-08c5-41d4-81f9-42293fbfdfd4" width="200px" alt="google play store icon" class="center-if-small" >
</a>
