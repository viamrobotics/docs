---
title: "Base Remote Control service API"
linkTitle: "Base Remote Control"
weight: 70
type: "docs"
tags: ["base", "services", "rover", "input controller", "remote control"]
description: "Give commands to get a list of inputs from the controller that are being monitored for that control mode."
icon: true
images: ["/services/icons/slam.svg"]
---

The Base Remote Control service API allows you to get a list of inputs from the controller that are being monitored for that control mode.

The [SLAM service](/services/slam/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/slam-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

{{< tabs >}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/services/baseremotecontrol"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/services/apis/generated/slam.md" >}}
