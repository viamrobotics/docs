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
# SMEs: Bijan, vision team
---

The camera component provides an API for getting images or point clouds.

If you have a physical camera or software that generates 2D images or 3D point clouds, use a camera component.

You can use the camera component to configure a webcam, lidar, time-of-flight sensor, or another type of camera.
You can also use camera models to manipulate the output of other cameras to transform, crop, or otherwise change the output.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/iKCMo89oyfw">}}

## Available models

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
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`fake`](fake-micro-server/) | A camera model for testing. |
| [`esp32-camera`](esp32-camera/) | A camera on an ESP32. |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The [camera API](/appendix/apis/components/camera/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/camera-table.md" >}}

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/how-tos/image-data/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{% card link="/get-started/detect-people/" noimage="true" %}}
{{< /cards >}}

You can also use the camera component with the following services:

- [Data management service](/services/data/): To capture and sync the camera's data
- [Vision service](/services/vision/): To use computer vision to interpret the camera stream
- [SLAM service](/services/slam/): for mapping
