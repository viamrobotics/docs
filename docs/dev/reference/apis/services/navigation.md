---
title: "Navigation service API"
linkTitle: "Navigation"
weight: 50
type: "docs"
tags: ["navigation", "services", "base", "rover"]
description: "Give commands to define waypoints and move your machine along those waypoints while avoiding obstacles."
icon: true
images: ["/services/icons/navigation.svg"]
date: "2022-01-01"
aliases:
  - /appendix/apis/services/navigation/
# updated: ""  # When the content was last entirely checked
---

The navigation service API allows you to define waypoints and move your machine along those waypoints while avoiding obstacles.

The [navigation service](/operate/reference/services/navigation/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/navigation-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page, navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following code examples assume that you have a machine configured with a `Navigation` service.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.navigation import NavigationClient
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/services/navigation"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/services/apis/generated/navigation.md" >}}
