---
title: "Machine Control Interface"
linkTitle: "Control Interface"
weight: 30
type: "docs"
description: "Use the Viam app control tab or the Viam mobile app to monitor and remotely operate your machines."
tags: ["fleet management", "control", "app"]
images: ["/components/base/cropped-control.png"]
date: "2024-10-22"
# updated: ""  # When the content was last entirely checked
---

Once you have [configured components and services](/configure/) for your machine, you can test, monitor, and remotely operate them from the **CONTROL** tab in the [Viam app](https://app.viam.com) or the [Viam mobile app](/fleet/control/#control-interface-in-the-viam-mobile-app).

## Control interface in the Viam app

The **CONTROL** tab in the [Viam app](https://app.viam.com) gives you the ability to test, monitor, and operate the machines in your fleet.
The **CONTROL** tab provides a control interface for each component and service that you have configured for you machine.

For example, if you have configured a base with wheels, you can move your machine's with an arrow pad and control the base's speed by setting its power with a slider.
If you have configured a camera component, a window in the **CONTROL** tab displays the camera output.

If you use remote control in the [Viam app](https://app.viam.com) UI, all communication to the machine uses [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection).
For local communication between [parts](/architecture/parts/#machine-parts) Viam uses gRPC or WebRTC.

{{<gif webm_src="/fleet/control.webm" mp4_src="/fleet/control.mp4" alt="Using the control tab" max-width="800px">}}

You can also switch between different machine parts directly from the **CONTROL** tab and control the selected machine part.

For more information on configuring and controlling machine parts, see [Machine Architecture](/architecture/parts/#machine-parts).

### Components

For more detailed information on how to operate and test your resources, expand the relevant resource below:

{{% expand "Arm" %}}
{{< readfile "/static/include/components/test-control/arm-control.md" >}}
{{% /expand%}}

{{% expand "Base" %}}
{{< readfile "/static/include/components/test-control/base-control.md" >}}
{{% /expand%}}

{{% expand "Board" %}}

## Test `analogs`

{{< readfile "/static/include/components/board/test-board-analogs.md" >}}

## Test `digital_interrupts`

{{< readfile "/static/include/components/board/test-board-digital-interrupts.md" >}}
{{% /expand%}}

{{% expand "Camera" %}}
{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}
{{% /expand%}}

{{% expand "Encoder" %}}
{{< readfile "/static/include/components/test-control/encoder-control.md" >}}
{{% /expand%}}

{{% expand "Gantry" %}}
{{< readfile "/static/include/components/test-control/gantry-control.md" >}}
{{% /expand%}}

{{% expand "Generic component" %}}
{{< readfile "/static/include/components/test-control/generic-control.md" >}}
{{% /expand%}}

{{% expand "Gripper" %}}
{{< readfile "/static/include/components/test-control/gripper-control.md" >}}
{{% /expand%}}

{{% expand "Input controller" %}}
{{< readfile "/static/include/components/test-control/input-controller-control.md" >}}
{{% /expand%}}

{{% expand "Motor" %}}
{{< readfile "/static/include/components/test-control/motor-control.md" >}}
{{% /expand%}}

{{% expand "Movement sensor (GPS)" %}}
{{< readfile "/static/include/components/test-control/movement-sensor-gps-control.md" >}}
{{% /expand%}}

{{% expand "Movement sensor (IMU)" %}}
{{< readfile "/static/include/components/test-control/movement-sensor-imu-control.md" >}}
{{% /expand%}}

{{% expand "Power sensor" %}}
{{< readfile "/static/include/components/test-control/power-sensor-control.md" >}}
{{% /expand%}}

{{% expand "Sensor" %}}

## Test the sensor

{{< readfile "/static/include/components/test-control/sensor-control.md" >}}

{{% /expand%}}

{{% expand "Servo" %}}
{{< readfile "/static/include/components/test-control/servo-control.md" >}}
{{% /expand%}}

### Services

The following services also provide control interfaces:

- [SLAM](/services/slam/cartographer/#create-a-new-map): for creating a new SLAM map and for using the motion service to move a machine on a SLAM map
- [Navigation](/services/navigation/#control-tab-usage): for moving a machine to waypoints on a map

## Control interface in the Viam mobile app

{{<gif webm_src="/fleet/mobile-app-control.webm" mp4_src="/fleet/mobile-app-control.mp4" alt="Using the control interface under the locations tab on the Viam mobile app" class="alignright" max-width="300px">}}

In addition to the [Viam app](https://app.viam.com), the fully featured web application where you can access all fleet management tools, there is a Viam mobile app.

The [Viam mobile app](/fleet/control/#control-interface-in-the-viam-mobile-app) allows you to test, monitor and remotely operate machines in your fleet.
It provides a control interface for each component and service that you have configured for you machine.

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
