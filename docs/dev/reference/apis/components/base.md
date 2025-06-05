---
title: "Base API"
linkTitle: "Base"
weight: 20
type: "docs"
description: "Give commands for moving all configured components attached to a mobile platform as a whole without needing to send commands to individual components."
icon: true
images: ["/icons/components/base.svg"]
date: "2022-01-01"
aliases:
  - /appendix/apis/components/base/
# updated: ""  # When the content was last entirely checked
---

The base API allows you to give commands to your [base components](/operate/reference/components/base/) for moving all configured components attached to a platform as a whole without needing to send commands to individual components.

The base component supports the following methods:

{{< readfile "/static/include/components/apis/generated/base-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your base and the rest of your machine, go to your machine's page, navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have a wheeled base called `"my_base"` configured as a component of your machine.
If your base has a different name, change the `name` in the code.

Import the base package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.base import Base
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/base"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/components/apis/generated/base.md" >}}
