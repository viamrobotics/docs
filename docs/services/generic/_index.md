---
title: "Generic Service"
linkTitle: "Generic Service"
childTitleEndOverwrite: "Generic Service"
weight: 500
type: "docs"
description: "A service that does not fit any of the other APIs."
tags: ["generic", "services"]
icon: true
images: ["/icons/components/generic.svg"]
no_list: true
modulescript: true
hide_children: true
aliases:
  - /registry/advanced/generic/
# SMEs:
---

The _generic_ service {{< glossary_tooltip term_id="subtype" text="subtype" >}} enables you to add support for unique types of services that do not already have an [appropriate API](/appendix/apis/#service-apis) defined for them.

For example, when writing code to manage [simultaneous localization and mapping (SLAM)](/services/slam/) for your machine, it makes sense to use the existing [SLAM API](/services/slam/#api), which provides specific functionality required for generating accurate maps of an environment.
However, if you want to create a new service to monitor your machine's CPU and RAM usage for example, you need very different functionality that isn't currently exposed in any API.
Instead, you can use the generic service API to add support for your unique type of service, like local system monitoring, to your machine.

Use generic for a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} model that represents a unique type of service.
If you are adding support for unique or proprietary hardware, rather than adding new high-level software functionality, use the [generic component](/components/generic/) instead.

There are no built-in generic service models (other than `fake`).

{{% alert title="Important" color="note" %}}

The generic service API only supports the `DoCommand` method.
If you use the generic subtype, your module needs to define any and all service functionality and pass it through `DoCommand`.

Whenever possible, it is best to use an [existing service API](/services/) instead of generic so that you do not have to replicate code.
If you want to use most of an existing API but need just a few other functions, try using the `DoCommand` endpoint and extra parameters to add custom functionality to an [existing subtype](/services/), instead of using the generic service.

{{% /alert %}}

## Available models

{{<resources_svc api="rdk:service:generic" type="generic">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Control your machine with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, navigate to your machine's **CONNECT** tab on the [Viam app](https://app.viam.com) and select the **Code sample** page.
Select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by getting your `generic` service from the machine with `FromRobot` and adding API method calls, as shown in the following examples.

Be sure to import the generic service package for the SDK you are using:

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

The generic service supports the following method:

{{< readfile "/static/include/services/apis/generated/generic_service-table.md" >}}

{{< readfile "/static/include/services/apis/generated/generic_service.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
