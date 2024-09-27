---
title: "Camera API"
linkTitle: "Camera"
weight: 20
type: "docs"
description: "The camera API allows you to give commands to your camera components with code instead of with the graphical interface of the Viam app"
icon: true
images: ["/icons/components/camera.svg"]
---

The camera API allows you to give commands to your [camera components](/components/camera/) with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).

The API for camera components allows you to:

- Request single images or a stream in 2D color, or display z-depth.
- Request a point cloud.
  Each 3D point cloud image consists of a set of coordinates (x,y,z) representing depth in mm.

The camera component supports the following methods:

{{< readfile "/static/include/components/apis/generated/camera-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

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

{{< readfile "/static/include/components/apis/generated/camera.md" >}}
