---
title: "Servo API"
linkTitle: "Servo"
weight: 140
type: "docs"
description: "Commands for controlling the angular position of a servo precisely or getting its current status."
icon: true
images: ["/icons/components/servo.svg"]
date: "2022-10-10"
aliases:
  - /appendix/apis/components/servo/
# updated: ""  # When the content was last entirely checked
---

The servo API allows you to give commands to your [servo components](/operate/reference/components/servo/) for controlling the angular position of a servo precisely or getting its current status.

The servo component supports the following methods:

{{< readfile "/static/include/components/apis/generated/servo-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your servo and the rest of your machine, go to your machine's page on the [Viam app](https://app.viam.com),
Navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have a servo called `"my_servo"` configured as a component of your machine.
If your servo has a different name, change the `name` in the code.

Import the servo package for the SDK you are using:

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
