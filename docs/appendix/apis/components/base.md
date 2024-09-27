---
title: "Base API"
linkTitle: "Base"
weight: 20
type: "docs"
description: "The base API allows you to give commands to your base components with code instead of with the graphical interface of the Viam app"
icon: true
images: ["/icons/components/base.svg"]
---

The base API allows you to give commands to your [base components](/components/base/) with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).

The base component supports the following methods:

{{< readfile "/static/include/components/apis/generated/base-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a wheeled base called `"my_base"` configured as a component of your machine.
If your base has a different name, change the `name` in the code.

Be sure to import the base package for the SDK you are using:

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
