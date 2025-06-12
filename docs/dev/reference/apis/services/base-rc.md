---
title: "Base remote control service API"
linkTitle: "Base remote control"
weight: 70
type: "docs"
tags: ["base", "services", "rover", "input controller", "remote control"]
description: "Give commands to get a list of inputs from the controller that are being monitored for that control mode."
icon: true
images: ["/services/icons/base-rc.svg"]
date: "2022-01-01"
aliases:
  - /appendix/apis/services/base-rc/
# updated: ""  # When the content was last entirely checked
---

The base remote control service API allows you to get a list of inputs from the controller that are being monitored for that control mode.

The [SLAM service](/operate/reference/services/slam/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/base_remote_control-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page, navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

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

{{< readfile "/static/include/services/apis/generated/base_remote_control.md" >}}
