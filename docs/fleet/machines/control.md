---
title: "Control Machines"
linkTitle: "Control Machines"
weight: 10
type: "docs"
description: "A machine is an organizational concept, consisting of either one or multiple parts working closely together to complete tasks."
tags: ["fleet management", "control", "app"]
images: ["/fleet/control.gif"]
---

Once you have configured components and services for your machine, you can test, monitor, and remotely operate them from the **CONTROL** tab in the [Viam app](https://app.viam.com) or the [Viam mobile app](/fleet/#the-viam-mobile-app).

## Control interface in the Viam app

The **CONTROL** tab in the [Viam app](https://app.viam.com) gives you the ability to test, monitor, and operate the machines in your fleet.
The **CONTROL** tab provides a control interface for each component and service that you have configured for you machine.

For example, if you have configured a base with wheels, you can move your machine's with an arrow pad and control the base's speed by setting its power with a slider.
If you have configured a camera component, a window in the **CONTROL** tab displays the camera output.

If you use remote control in the [Viam app](https://app.viam.com) UI, all communication to the machine uses [WebRTC](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection).
For local communication between [parts](/build/configure/parts/#machine-parts) Viam uses gRPC or WebRTC.

{{<gif webm_src="/fleet/control.webm" mp4_src="/fleet/control.mp4" alt="Using the control tab" max-width="800px">}}

### Components

For more detailed information on how to operate and test your resources, expand the relevant resource below:

{{% expand "Arm" %}}
{{< readfile "/static/include/components/test-control/arm-control.md" >}}
{{% /expand%}}

{{% expand "Base" %}}
{{< readfile "/static/include/components/test-control/base-control.md" >}}
{{% /expand%}}

{{% expand "Board" %}}
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
{{< readfile "/static/include/components/test-control/sensor-control.md" >}}
{{% /expand%}}

{{% expand "Servo" %}}
{{< readfile "/static/include/components/test-control/servo-control.md" >}}
{{% /expand%}}

### Services

The following services also provide control interfaces:

- [SLAM](/mobility/slam/cartographer/#create-a-new-map): for creating a new SLAM map and for using the motion service to move a machine on a SLAM map
- [Motion](/mobility/motion/#test-the-motion-service): for moving a machine on a map

## Control interface in the Viam mobile app

The [Viam mobile app](/fleet/#the-viam-mobile-app) gives you the ability to test, monitor and remotely operate machines in your fleet.
The mobile app provides a control interface for each component and service that you have configured for you machine.

For example, you can view live camera feeds, adjust components' runtime parameters, and switch between controllable components.

{{<gif webm_src="/fleet/mobile-app-control.webm" mp4_src="/fleet/mobile-app-control.mp4" alt="Using the control interface under the locations tab on the Viam mobile app" max-width="300px">}}

Additionally, the machine control interface provides a menu for:

- [viewing a machine's logs](/fleet/machines/#logs)
- [uploading images from your phone to the cloud](/data/upload/#upload-images-with-the-viam-mobile-app)
