---
title: "Control your gantry with the gantry API"
linkTitle: "Gantry"
weight: 20
type: "docs"
description: "The gantry API allows you to give commands to your gantry components with code instead of with the graphical interface of the Viam app"
---

The gantry API allows you to give commands to your gantry components with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).

The gantry component supports the following methods:

{{< readfile "/static/include/components/apis/generated/gantry-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a gantry called `"my_gantry"` configured as a component of your machine.
If your gantry has a different name, change the `name` in the code.

Be sure to import the gantry package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.gantry import Gantry
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/gantry"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/components/apis/generated/gantry.md" >}}
