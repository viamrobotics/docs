---
title: "Micro-RDK Generic Models"
linkTitle: "Generic"
weight: 30
type: "docs"
description: "The micro-RDK generic component for generic component types."
images: ["/icons/components/generic.svg"]
icon: true
tags: ["generic", "components", "micro-rdk"]
no_list: true
# SMEs: Gautham V.
---

The _generic_ component {{< glossary_tooltip term_id="subtype" text="subtype" >}} enables you to add support for unique types of hardware that do not already have an [appropriate API](/appendix/apis/#component-apis) defined for them.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Generic Component](/components/generic/).

If your micro-RDK machine includes a resource that isn't a [base](/build/micro-rdk/base/), [board](/build/micro-rdk/board/),[encoder](/build/micro-rdk/encoder/), [movement sensor](/build/micro-rdk/movement-sensor/), [motor](/build/micro-rdk/motor/), or [servo](/build/micro-rdk/servo/), you can create a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} to add support for it as a custom model of the generic subtype.

{{< alert title="Important" color="note" >}}
The micro-RDK works differently from the RDK, so creating modular resources for it is different.
Refer to the [Micro-RDK Module Template on GitHub](https://github.com/viamrobotics/micro-rdk/tree/main/templates/module) for information on how to create custom resources for your micro-RDK machine.
You will need to [recompile and flash your ESP32 yourself](/get-started/installation/microcontrollers/development-setup/) instead of using Viam's prebuilt binary and installer.
{{< /alert >}}

<!--
## Supported models

For configuration information, click on the supported generic model name:
Model | Description
----- | -----------
[`fake`](fake/) | A model used for testing, with no physical hardware. -->

## API

The micro-RDK [generic API](/components/generic/#api) supports only the following client SDK API method, which operates the same as in the full-featured RDK:

- [`DoCommand()`](/components/generic/#docommand)
