---
title: "Generic Component"
linkTitle: "Generic"
childTitleEndOverwrite: "Generic Component"
weight: 55
type: "docs"
description: "A component that does not fit any of the other APIs."
tags: ["generic", "components"]
icon: true
images: ["/icons/components/generic.svg"]
no_list: true
modulescript: true
aliases:
  - "/components/generic/"
  - /micro-rdk/generic/
  - /build/micro-rdk/generic/

hide_children: true
# SMEs:
---

The _generic_ component {{< glossary_tooltip term_id="subtype" text="subtype" >}} enables you to add support for unique types of hardware that do not already have an [appropriate API](/appendix/apis/#component-apis) defined for them.

For example, when using an [arm component](/components/arm/), it makes sense to use the [arm API](/components/arm/#api), which provides specific functionality an arm component needs, such as moving to position or stopping movement.
However, if you want to use an LED display for example, you need very different functionality that isn't currently exposed in any API.
Instead, you can use the generic component API to add support for your unique type of hardware, like LED displays, to your machine.

Use generic for a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} model that represents a unique type of hardware.
If you are adding new high-level software functionality, rather than supporting new hardware components, use the [generic service](/services/generic/) instead.

There are no built-in generic component models (other than `fake`).

{{% alert title="Important" color="note" %}}

The generic component API only supports the `DoCommand` method.
If you use the generic subtype, your module needs to define any and all component functionality and pass it through `DoCommand`.

Whenever possible, it is best to use an [existing component API](/components/) instead of generic so that you do not have to replicate code.
If you want to use most of an existing API but need just a few other functions, try using the `DoCommand` endpoint and extra parameters to add custom functionality to an [existing subtype](/components/), instead of using the generic component.

{{% /alert %}}

## Supported models

{{<resources api="rdk:component:generic" type="generic">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

### micro-RDK

If your micro-RDK machine includes a resource that isn't a [base](/components/base/), [board](/components/board/),[encoder](/components/encoder/), [movement sensor](/components/movement-sensor/), [motor](/components/motor/), or [servo](/components/servo/), you can create a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} to add support for it as a custom model of the generic subtype.

{{< alert title="Important" color="note" >}}
The micro-RDK works differently from the RDK, so creating modular resources for it is different.
Refer to the [Micro-RDK Module Template on GitHub](https://github.com/viamrobotics/micro-rdk/tree/main/templates/module) for information on how to create custom resources for your micro-RDK machine.
You will need to [recompile and flash your ESP32 yourself](/get-started/installation/microcontrollers/development-setup/) instead of using Viam's prebuilt binary and installer.
{{< /alert >}}

## Control your board with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by getting your `generic` component from the machine with `FromRobot` and adding API method calls, as shown in the following examples.

These examples assume you have a board called "my_board" configured as a component of your machine.
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

The generic component supports the following method:

{{< readfile "/static/include/components/apis/generated/generic_component-table.md" >}}

{{< readfile "/static/include/components/apis/generated/generic_component.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
