---
title: "Vision service API"
linkTitle: "Vision"
weight: 20
type: "docs"
tags: ["vision", "computer vision", "CV", "services"]
description: "The vision service API allows you to get detections, classifications, or point cloud objects, depending on the ML model the vision service is using."
icon: true
images: ["/services/icons/vision.svg"]
tags: ["vision", "computer vision", "CV", "services"]
---

The vision service API allows you to get detections, classifications, or point cloud objects, depending on the ML model the vision service is using.

The [vision service](/services/vision/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/vision-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume that you have a machine configured with a [camera](/components/camera/) and a vision service [detector](/services/vision/#detections), [classifier](/services/vision/#classifications) or [segmenter](/services/vision/#segmentations).

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.vision import VisionClient
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/services/vision"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/services/apis/generated/vision.md" >}}
