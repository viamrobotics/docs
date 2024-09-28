---
title: "Control your gripper with the gripper API"
linkTitle: "Gripper"
weight: 20
type: "docs"
description: "The gripper API allows you to give commands to your gripper components for opening and closing a device."
icon: true
images: ["/icons/components/gripper.svg"]
---

The gripper API allows you to give commands to your [gripper components](/components/gripper/) for opening and closing a device.

The gripper component supports the following methods:

{{< readfile "/static/include/components/apis/generated/gripper-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a gripper called `"my_gripper"` configured as a component of your machine.
If your gripper has a different name, change the `name` in the code.

Be sure to import the gripper package for the SDK you are using:

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
