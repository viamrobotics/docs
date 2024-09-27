---
title: "Control your servo with the servo API"
linkTitle: "Servo"
weight: 20
type: "docs"
description: "The servo API allows you to give commands to your servo components with code instead of with the graphical interface of the Viam app"
icon: true
images: ["/icons/components/servo.svg"]
---

The servo API allows you to give commands to your [servo components](/components/servo/) with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).

The servo component supports the following methods:

{{< readfile "/static/include/components/apis/generated/servo-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a servo called `"my_servo"` configured as a component of your machine.
If your servo has a different name, change the `name` in the code.

Be sure to import the servo package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.servo import Servo
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/servo"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/components/apis/generated/servo.md" >}}
