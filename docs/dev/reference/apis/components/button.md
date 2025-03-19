---
title: "Button API"
linkTitle: "Button"
weight: 35
type: "docs"
description: "Give commands for getting presses from a physical button."
icon: true
images: ["/icons/components/button.svg"]
date: "2025-02-20"
# updated: ""  # When the content was last entirely checked
---

The button API allows you to get button presses from your [button components](/operate/reference/components/button/).

The button component supports the following methods:

{{< readfile "/static/include/components/apis/generated/button-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your button and the rest of your machine, go to your machine's page on the [Viam app](https://app.viam.com),
Navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have an button called `"my_button"` configured as a component of your machine.
If your button has a different name, change the `name` in the code.

Import the button package for the SDK you are using:

{{< tabs >}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/button"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/components/apis/generated/button.md" >}}
