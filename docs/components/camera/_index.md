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

A camera component is a source of 2D and/or 3D images.
You can use the component to configure a webcam, lidar, time-of-flight sensor, or another type of camera.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/iKCMo89oyfw">}}

## Available models

To use a camera with your machine, you have to add it to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your camera.

The following list shows you the available camera models.
You can use different models to:

- Configure physical cameras that generate images or point clouds.
- Combine streams from multiple cameras into one.
- Transform and process images.


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

## Related services

{{< cards >}}
{{< relatedcard link="/services/data/" >}}
{{< relatedcard link="/services/vision/" >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/slam/" >}}
{{< relatedcard link="/services/ml/deploy/" alt_title="Machine Learning" >}}
{{< /cards >}}

## API

The camera component supports the following methods:

{{< readfile "/static/include/components/apis/generated/camera-table.md" >}}

## Next steps

{{< cards >}}
{{% card link="/services/vision" %}}
{{% card link="/how-tos/detect-color/" %}}
{{% card link="/tutorials/services/color-detection-scuttle" %}}
{{< /cards >}}

{{< snippet "social.md" >}}
