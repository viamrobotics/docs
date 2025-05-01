---
title: "ML model service API"
linkTitle: "ML model"
weight: 30
type: "docs"
tags: ["data management", "ml", "model training"]
description: "Give commands to your ML model service to make inferences based on a provided ML model."
icon: true
images: ["/services/icons/ml.svg"]
date: "2022-01-01"
aliases:
  - /appendix/apis/services/ml/
# updated: ""  # When the content was last entirely checked
---

The ML model service API allows you to make inferences based on a provided ML model.

The [ML Model service](/data-ai/ai/deploy/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/mlmodel-table.md" >}}

## Establish a connection

{{< alert title="Viam Python SDK Support" color="note" >}}

To use the ML model service from the [Viam Python SDK](https://python.viam.dev/), install the Python SDK using the `mlmodel` extra:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[mlmodel]'
```

{{< /alert >}}

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on the [Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume that you have a machine configured with an `MLModel` service called `"my_mlmodel_service"`, and that you have installed the `mlmodel` extra for the Python SDK.
If your ML model service has a different name, change the `name` in the code.

Import the mlmodel package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.mlmodel import MLModelClient
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/services/mlmodel"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/services/apis/generated/mlmodel.md" >}}
