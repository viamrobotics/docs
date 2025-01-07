---
title: "Control your gripper with the gripper API"
linkTitle: "Gripper"
weight: 80
type: "docs"
description: "Give commands for opening and closing a gripper device."
icon: true
images: ["/icons/components/gripper.svg"]
date: "2022-01-01"
aliases:
  - /appendix/apis/components/gripper/
# updated: ""  # When the content was last entirely checked
---

The gripper API allows you to give commands to your [gripper components](/operate/reference/components/gripper/) for opening and closing a device.

The gripper component supports the following methods:

{{< readfile "/static/include/components/apis/generated/gripper-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your gripper and the rest of your machine, go to your machine's page on the [Viam app](https://app.viam.com),
Navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have a gripper called `"my_gripper"` configured as a component of your machine.
If your gripper has a different name, change the `name` in the code.

Import the gripper package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.gripper import Gripper
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/gripper"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/components/apis/generated/gripper.md" >}}
