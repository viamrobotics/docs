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

Generic components provide an API for running model-specific commands using [`DoCommand`](/appendix/apis/components/generic/#docommand).

If you have a physical device or a program that does not fit into any of the provided [components APIs](/appendix/apis/#component-apis), use a generic component.

For example, if you want to use an LED display, you need functionality that isn't currently exposed in an existing API.
Instead, you can use the generic component API to add support for your unique type of hardware, like LED displays, to your machine.

You should use the generic component for {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} that represent a unique type of hardware.
If you are adding new high-level software functionality, rather than supporting new hardware components, use the [generic service](/services/generic/) instead.

{{% alert title="Important" color="note" %}}

The generic component API only supports the `DoCommand` method.
If you use the generic subtype, your module needs to define any and all component functionality and pass it through `DoCommand`.

Whenever possible, it is best to use an [existing component API](/components/) instead of generic so that you do not have to replicate code.
If you want to use most of an existing API but need just a few other functions, try using the `DoCommand` endpoint and extra parameters to add custom functionality to an [existing subtype](/components/), instead of using the generic component.

{{% /alert %}}

## Configuration

To use a generic component, check whether one of the following models supports it.

For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:generic" type="generic" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

If your `viam-micro-server` machine includes a resource that isn't a [base](/components/base/), [board](/components/board/),[encoder](/components/encoder/), [movement sensor](/components/movement-sensor/), [motor](/components/motor/), or [servo](/components/servo/), you can create a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} to add support for it as a custom model of the generic subtype.

{{< alert title="Important" color="note" >}}
`viam-micro-server` works differently from the RDK, so creating modular resources for it is different.
Refer to the [Micro-RDK Module Template on GitHub](https://github.com/viamrobotics/micro-rdk/tree/main/templates/module) for information on how to create custom resources for your `viam-micro-server` machine.
You will need to [recompile and flash your ESP32 yourself](/installation/viam-micro-server-setup/#install-viam-micro-server) instead of using Viam's prebuilt binary and installer.
{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The [generic API](/appendix/apis/components/generic/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/generic_component-table.md" >}}

## Troubleshooting

If your generic component is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
2. Review your generic component model's documentation to ensure you have configured all required attributes.
3. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the generic component there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{< /cards >}}
