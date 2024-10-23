---
title: "SLAM service API"
linkTitle: "SLAM"
weight: 60
type: "docs"
tags: ["slam", "services"]
description: "Give commands to get a machine's position within a map."
icon: true
images: ["/services/icons/slam.svg"]
---

The SLAM service API allows you to get a machine's position within a map.

The [SLAM service](/services/slam/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/slam-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on the [Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following code examples assume that you have a machine configured with a SLAM service called `"my_slam_service"`.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.slam import SLAMClient
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/services/slam"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/services/apis/generated/slam.md" >}}
