---
title: "Motor API"
linkTitle: "Motor"
weight: 20
type: "docs"
description: "Give commands to operate a motor or get its current status."
icon: true
images: ["/icons/components/motor.svg"]
---

The motor API allows you to give commands to your [motor components](/components/motor/) for operating a motor or getting its current status.

The motor component supports the following methods:

{{< readfile "/static/include/components/apis/generated/motor-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have a motor called `"my_motor"` configured as a component of your machine.
If your motor has a different name, change the `name` in the code.

Be sure to import the motor package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.motor import Motor
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/motor"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/components/apis/generated/motor.md" >}}
