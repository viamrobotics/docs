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

The API for camera components allows you to:

- Request single images or a stream in 2D color, or display z-depth.

- Request a point cloud.
  Each 3D point cloud image consists of a set of coordinates (x,y,z) representing depth in mm.

The configuration of your camera component depends on your camera model.
You can use different models to:

- Configure physical cameras that generate images or point clouds.
- Combine streams from multiple cameras into one.
- Transform and process images.

## Related services

{{< cards >}}
{{< relatedcard link="/services/data/" >}}
{{< relatedcard link="/services/vision/" >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/slam/" >}}
{{< relatedcard link="/services/ml/deploy/" alt_title="Machine Learning" >}}
{{< /cards >}}

## Supported models

{{<resources api="rdk:component:camera" type="camera">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Control your camera with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a camera called `"my_camera"` configured as a component of your machine.
If your camera has a different name, change the `name` in the code.

Be sure to import the camera package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.camera import Camera
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/camera"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The camera component supports the following methods:

{{< readfile "/static/include/components/apis/generated/camera-table.md" >}}

{{< readfile "/static/include/components/apis/generated/camera.md" >}}

## Next steps

{{< cards >}}
{{% card link="/services/vision" %}}
{{% card link="/tutorials/services/basic-color-detection" %}}
{{% card link="/tutorials/services/color-detection-scuttle" %}}
{{< /cards >}}

{{< snippet "social.md" >}}
