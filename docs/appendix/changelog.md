---
title: "Changelog"
linkTitle: "Changelog"
weight: 110
draft: false
type: "docs"
description: "Changelog"
# SME:
---

## Upcoming

## 25 April 2023

## 28 February 2023

## 31 January 2023

## 28 December 2022

Release versions:

- rdk - v0.2.9
- api - v0.1.63
- slam - v0.1.13
- viam-python-sdk - v0.2.6
- goutils - v0.1.6
- rust-utils - v0.0.6

### Added: Modular resources

You can now implement your own custom {{< glossary_tooltip term_id="resource" text="resources" >}} as [_modular resources_](/extend/modular-resources).

The [old method](/modular-resources/advanced/custom-components-remotes/) of using a separate server to implement a custom resource is still supported, but implementation as a modular resource reduces network requests and is strongly recommended.

{{% alert title="Important: Breaking Change" color="note" %}}

All users need to update to the latest version of the RDK (V3.0.0) to access robots using the Viam app.

{{% /alert %}}

### Added: URDF kinematic file support

You can now supply kinematic information using URDF files when implementing your own arm models.

### Added: New movement sensor models

There are two new movement sensor {{< glossary_tooltip term_id="model" text="models" >}}:

- [ADXL345](/components/movement-sensor/adxl345/): A 3-axis accelerometer
- [MPU-6050](/components/movement-sensor/mpu6050/): A 6-axis accelerometer and gyroscope

### Improved: Camera performance and reliability

- Improved server-side logic to choose a mime type based on the camera image type, unless a specified mime type is supplied in the request.
  **The default mime type for color cameras is now JPEG**, which improves the streaming rate across every SDK.
- Added discoverability when a camera reconnects without changing video paths.
  This now triggers the camera discovery process, where previously users would need to manually restart the RDK to reconnect to the camera.

### Improved: Motion planning with remote components

The [motion service](/services/motion/) is now agnostic to the networking topology of a robot.

- Kinematic information is now transferred over the robot API.
  This means that the motion service is able to get kinematic information for every component on the robot, regardless of whether it is on a main or remote viam-server.
- Arms are now an input to the motion service.
  This means that the motion service can plan for a robot that has an arm component regardless of whether the arm is connected to a main or {{< glossary_tooltip term_id="remote" text="remote" >}} instance of `viam-server`.

### Improved: Motion planning path smoothing

- RRT\* paths now undergo rudimentary smoothing, resulting in improvements to path quality with negligible change to planning performance.
- Plan manager now performs direct interpolation for any solution within some factor of the best score, instead of only in the case where the best inverse kinematics solution could be interpolated.

### Improved: Data synchronization reliability

Previously, data synchronization used bidirectional streaming.
Now is uses a simpler unary approach that is more performant on batched unary calls, is easier to load balance, and maintains ordered captures.

### Fixed: `viam-server` shutdown failure

Fixed a bug where `viam-server` shutdown requests sometimes failed when connected to serial components.

## 28 November 2022

Release versions:

- rdk - v0.2.3
- api - v0.1.12
- slam - v0.1.9

### Fixed: Camera reconnection issue

Previously, when users supplied a video path in their camera configuration, they encountered issues if the camera tried to reconnect because the supplied video path was already being used for the old connection.
Now, when a camera loses connection, it automatically closes the connection to its video path.

### Changed: Camera configuration

**Changed** the configuration schemes for the following camera models:

- Webcam
- FFmpeg
- Transform
- Join pointclouds

For information on configuring any camera model, see [Camera Component](/components/camera/).

### Changed: App code sample tab name update

Changed the name of the **Connect** tab to **Code sample** based on user feedback.

## 15 November 2022

Release versions:

- rdk - v0.2.0
- api - v0.1.7
- slam - v0.1.7
- viam-python-sdk - v0.2.0
- goutils - v0.1.4
- rust-utils - v0.0.5

### Added: New servo model

A new [servo model called `gpio`](/components/servo/gpio/) supports servos connected to non-Raspberry Pi boards.

### Added: RTT indicator in the app

A badge in the Viam app now displays RTT (round trip time) of a request from your client to the robot.
Find this indicator of the time to complete one request/response cycle on your robot's **Control** tab, in the **Operations & Sessions** card.

### Added: Python 3.8 support

The Python SDK now supports Python 3.8, in addition to 3.9 and 3.10.

### Added: New parameter: `extra`

A new API method parameter, `extra`, allows you to extend {{< glossary_tooltip term_id="resource" text="resource" >}} functionality by implementing the new field according to whatever logic you choose.
`extra` has been added to the following APIs: arm, data management, gripper, input controller, motion, movement sensor, navigation, pose tracker, sensor, SLAM, vision.

{{% alert title="IMPORTANT: Breaking change" color="note" %}}

Users of the Go SDK _must_ update code to specify `extra` in the arguments that pass into each request.

`extra` is an optional parameter in the Python SDK.

{{% /alert %}}

### Added: Service dependencies

`viam-server` now initializes and configures resources in the correct order.
For example, if the SLAM service depends on a LiDAR, it will always initialize the LiDAR before the SLAM service.

{{% alert title="IMPORTANT: Breaking change" color="note" %}}

If you are using the SLAM service, you now need to specify sensors used by the SLAM service in the `depends_on` field of the SLAM configuration.
Other service configurations are not affected.

{{% /alert %}}

### Removed: width and height fields from camera API

Removed `width` and `height` from the response of the [`GetImage`](/components/camera/#getimage) method in the camera API.
This does not impact any existing camera models.
If you write a custom camera model, you no longer need to implement the `width` and `height` fields.
