---
title: "Changelog option 2"
linkTitle: "Changelog2"
weight: 110
draft: false
type: "docs"
description: "Changelog"
# SME:
---

{{%expand "Upcoming" %}}
`<staged changes>`
{{% /expand%}}

{{%expand "25 April 2023" %}}

Release versions:
...

{{% /expand%}}

{{%expand "28 February 2023" %}}
This will be visible if the reader clicks on the expander
{{% /expand%}}

{{%expand "31 January 2023" %}}
This will be visible if the reader clicks on the expander
{{% /expand%}}

{{%expand "28 December 2023" %}}

This will be visible if the reader clicks on the expander

{{% /expand%}}

{{%expand "28 November 2022" %}}

Release versions:

- rdk - v0.2.3
- api - v0.1.12
- slam - v0.1.9

### Camera reconnection issue

**Fixed** an issue with camera reconnection.
Previously, when users supplied a video path in their camera configuration, they encountered issues if the camera tried to reconnect because the supplied video path was already being used for the old connection.
Now, when a camera loses connection, it automatically closes the connection to its video path.

### Camera configuration changes

**Changed** the configuration schemes for the following camera models:

- Webcam
- FFmpeg
- Transform
- Join pointclouds

For information on configuring any camera model, see [Camera Component](/components/camera/).

### App tab name update

**Changed** the name of the **Connect** tab to **Code sample** based on user feedback.

{{% /expand%}}
{{%expand "15 November 2022" %}}

Release versions:

- rdk - v0.2.0
- api - v0.1.7
- slam - v0.1.7
- viam-python-sdk - v0.2.0
- goutils - v0.1.4
- rust-utils - v0.0.5

### New servo model

**Added** a new [servo model called `gpio`](/components/servo/gpio/) for servos connected to boards other than Raspberry Pis.

### RTT indicator in the app

**Added** a badge in the Viam app displaying RTT (round trip time) of a request from your client to the robot.
Find this indicator of the time to complete one request/response cycle on your robot's **Control** tab, in the **Operations & Sessions** card.

### Python 3.8 support

**Added** Python SDK support for Python 3.8, in addition to 3.9 and 3.10.

### New parameter: `extra`

**Added** a new API method parameter, `extra`, that allows you to extend {{< glossary_tooltip term_id="resource" text="resource" >}} functionality by implementing the new field according to whatever logic you choose.
`extra` has been added to the following APIs: arm, data management, gripper, input controller, motion, movement sensor, navigation, pose tracker, sensor, SLAM, vision.

{{% alert title="IMPORTANT: Breaking change" color="note" %}}

Users of the Go SDK _must_ update code to specify `extra` in the arguments that pass into each request.

`extra` is an optional parameter in the Python SDK.

{{% /alert %}}

### Service dependencies

**Added** dependencies to services: `viam-server` now initializes and configures resources in the correct order.
For example, if the SLAM service depends on a LiDAR, it will always initialize the LiDAR before the SLAM service.

{{% alert title="IMPORTANT: Breaking change" color="note" %}}

If you are using the SLAM service, you now need to specify sensors used by the SLAM service in the `depends_on` field of the SLAM configuration.
Other service configurations are not affected.

{{% /alert %}}

### Removed width and height fields from camera API

**Removed** `width` and `height` from the response of the [`GetImage`](/components/camera/#getimage) method in the camera API.
This does not impact any existing camera models.
If you write a custom camera model, you no longer need to implement the `width` and `height` fields.

{{% /expand%}}
