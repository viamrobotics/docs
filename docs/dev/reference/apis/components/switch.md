---
title: "Switch API"
linkTitle: "Switch"
weight: 200
type: "docs"
description: "Give commands for getting the state of a physical switch that has two or more discrete positions."
icon: true
images: ["/icons/components/switch.svg"]
date: "2025-02-20"
# updated: ""  # When the content was last entirely checked
---

The switch API allows you to give commands to your [switch components](/operate/reference/components/switch/) for reading the state of a physical switch that has multiple discrete positions.
A simple switch has two positions, and a knob could have any number of positions.

The switch component supports the following methods:

{{< readfile "/static/include/components/apis/generated/switch-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your switch and the rest of your machine, go to your machine's page on the [Viam app](https://app.viam.com),
Navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have an switch called `"my_switch"` configured as a component of your machine.
If your switch has a different name, change the `name` in the code.

Import the switch package for the SDK you are using:

{{< tabs >}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/switch"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/components/apis/generated/switch.md" >}}
