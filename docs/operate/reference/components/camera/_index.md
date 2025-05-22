---
title: "Camera Component"
linkTitle: "Camera"
childTitleEndOverwrite: "Camera Component"
weight: 40
type: "docs"
description: "A camera captures 2D or 3D images and sends them to the computer controlling the machine."
no_list: true
tags: ["camera", "components"]
icon: true
images: ["/icons/components/camera.svg"]
modulescript: true
aliases:
  - "/tutorials/configure-a-camera"
  - "/components/camera/"
date: "2024-10-21"
# SMEs: Bijan, vision team
---

The camera component provides an API for getting images or point clouds.

If you have a physical camera or software that generates 2D images or 3D point clouds, use a camera component.

You can use the camera component to configure a webcam, lidar, time-of-flight sensor, or another type of camera.
You can also use camera models to manipulate the output of other cameras to transform, crop, or otherwise change the output.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/iKCMo89oyfw">}}

## Configuration

To use a camera with your machine, you need to add it to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your camera.

The following list shows the available camera models.
The configuration of your camera component depends on your camera model.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:camera" type="camera" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`fake`](fake-micro-server/) | A camera model for testing. |
| [`esp32-camera`](esp32-camera/) | A camera on an ESP32. |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The [camera API](/dev/reference/apis/components/camera/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/camera-table.md" >}}

## Troubleshooting

If your camera is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.

2. Review your camera model's documentation to ensure you have configured all required attributes.
3. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the camera there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

### Common errors

{{% expand "Failed to find the best driver that fits the constraints" %}}

When working with a [camera](/operate/reference/components/camera/) component, depending on the camera, you may need to explicitly provide some camera-specific configuration parameters.

Check the specifications for your camera, and manually provide configuration parameters such as width and height to the camera component configuration page on the [Viam app](https://app.viam.com).
On the **CONFIGURE** page, find your camera, then fill in your camera's specific configuration either using the **Show more** button to show the relevant configuration options, or the **{}** (Switch to Advanced) button in the top right of the component panel to enter these attributes manually.
Provide at least the width and height values to start.

{{% /expand%}}

{{% expand "Frame read failed: Too many retries" %}}

**Description:** This error typically occurs with IR camera modules and similar specialized cameras.
It happens when the camera module is still initializing or calibrating itself, but `viam-server` is already attempting to read frames from it.
This can also be caused by I2C communication issues between the board and the camera module, particularly on Raspberry Pi 5 systems.

**Solution:** Try one of the following approaches:

1. **Reduce the refresh rate for I2C cameras**:
   For I2C-based cameras (like some IR modules), try setting the refresh rate to a lower value (for example, 2Hz instead of 4Hz).
   This can help with I2C bus timing issues, especially on Raspberry Pi 5 systems.

1. **Check physical connections**:

   - Ensure the camera module is properly connected.
   - For I2C cameras, verify that the SCK (clock) pin is properly connected and not shorted to ground or power.
     If the pin has been shorted, this can permanently damage the hardware.

If these steps don't resolve the issue, check your machine logs for additional error messages that might provide more specific information about the problem.

{{% /expand%}}

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/data-ai/capture-data/capture-sync/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}

You can also use the camera component with the following services:

- [Data management service](/data-ai/capture-data/capture-sync/): To capture and sync the camera's data
- [Vision service](/operate/reference/services/vision/): To use computer vision to interpret the camera stream
- [SLAM service](/operate/reference/services/slam/): for mapping

{{% hiddencontent %}}
There's no model of transform camera available to mirror the camera image.
{{% /hiddencontent %}}
