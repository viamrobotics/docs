---
title: "Encoder API"
linkTitle: "Encoder"
weight: 20
type: "docs"
description: "Give commands for getting the position of a motor or a joint in ticks or degrees."
icon: true
images: ["/icons/components/encoder.svg"]
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

The encoder API allows you to give commands to your [encoder components](/components/encoder/) for getting the position of a motor or a joint in ticks or degrees.

The encoder component supports the following methods:

{{< readfile "/static/include/components/apis/generated/encoder-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your encoder and the rest of your machine, go to your machine's page on the [Viam app](https://app.viam.com),
Navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume you have an encoder called `"my_encoder"` configured as a component of your machine.
If your encoder has a different name, change the `name` in the code.

Import the encoder package for the SDK you are using:

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
