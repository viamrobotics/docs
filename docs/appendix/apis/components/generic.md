---
title: "Control your generic component with the generic API"
linkTitle: "Generic"
weight: 20
type: "docs"
description: "The generic API allows you to give commands to your generic components for running model-specific commands using DoCommand."
icon: true
images: ["/icons/components/generic.svg"]
---

The generic API allows you to give commands to your [generic components](/components/generic/) for running model-specific commands using [`DoCommand`](#docommand).

The generic component supports the following method:

{{< readfile "/static/include/components/apis/generated/generic_component-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by getting your `generic` component from the machine with `FromRobot` and adding API method calls, as shown in the following examples.

The following examples assume you have a board called "my_board" configured as a component of your machine.
If your board has a different name, change the `name` in the code.

Be sure to import the generic component package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.generic import Generic
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/generic"
)
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp
#include <viam/sdk/components/generic/generic.hpp>
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/components/apis/generated/generic_component.md" >}}
