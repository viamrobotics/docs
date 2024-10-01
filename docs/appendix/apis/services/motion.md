---
title: "Motion Service API"
linkTitle: "Motion"
weight: 40
type: "docs"
description: "Give commands to move a machine based on a SLAM map or GPS coordinates or to move a machine's components form one location to another."
icon: true
images: ["/icons/components/arm.svg"]
---

The motion service API allows you to give commands to your [motion service](/services/motion/) for moving a machine based on a SLAM map or GPS coordinates or for moving a machine's components form one location to another.

The motion service supports the following methods:

{{< readfile "/static/include/services/apis/generated/motion-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

Because the motion service is enabled by default, you don't give it a `"name"` while configuring it.
Use the name `"builtin"` to access the built-in motion service in your code with methods like [`FromRobot()`](/appendix/apis/services/motion/#fromrobot) that require a `ResourceName`.

Be sure to import the motion package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/services/motion"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/services/apis/generated/motion.md" >}}
