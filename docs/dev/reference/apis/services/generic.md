---
title: "Generic service API"
linkTitle: "Generic"
weight: 60
type: "docs"
tags: ["generic", "services"]
description: "Give commands to your generic components for running model-specific commands using DoCommand."
icon: true
images: ["/icons/components/generic.svg"]
date: "2022-01-01"
aliases:
  - /appendix/apis/services/generic/
  - /services/generic/
# updated: ""  # When the content was last entirely checked
---

The generic service API allows you to give commands to your [generic services](/operate/reference/services/generic/) for running model-specific commands using [`DoCommand`](/dev/reference/apis/services/generic/#docommand).

The generic service supports the following methods:

{{< readfile "/static/include/services/apis/generated/generic_service-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page, navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.generic import Generic
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/services/generic"
)
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp
#include <viam/sdk/services/generic/generic.hpp>
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/services/apis/generated/generic_service.md" >}}
