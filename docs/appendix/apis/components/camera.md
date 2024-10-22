---
title: "Camera API"
linkTitle: "Camera"
weight: 20
type: "docs"
description: "Give commands for getting images or point clouds."
icon: true
images: ["/icons/components/camera.svg"]
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

The camera API allows you to give commands to your [camera components](/components/camera/) for getting images or point clouds.

The API for camera components allows you to:

- Request single images or a stream in 2D color, or display z-depth.
- Request a point cloud.
  Each 3D point cloud image consists of a set of coordinates (x,y,z) representing depth in mm.

The camera component supports the following methods:

{{< readfile "/static/include/components/apis/generated/camera-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have a camera called `"my_camera"` configured as a component of your machine.
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

{{< readfile "/static/include/components/apis/generated/camera.md" >}}
