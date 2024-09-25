---
title: "Control your encoder with the encoder API"
linkTitle: "Encoder"
weight: 20
type: "docs"
description: "The encoder API allows you to give commands to your encoder components with code instead of with the graphical interface of the Viam app"
icon: true
images: ["/icons/components/encoder.svg"]
---

The encoder API allows you to give commands to your encoder components with code instead of with the graphical interface of the [Viam app](https://app.viam.com/).

The encoder component supports the following methods:

{{< readfile "/static/include/components/apis/generated/encoder-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have an encoder called `"my_encoder"` configured as a component of your machine.
If your encoder has a different name, change the `name` in the code.

Be sure to import the encoder package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.encoder import Encoder
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/encoder"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/components/apis/generated/encoder.md" >}}
