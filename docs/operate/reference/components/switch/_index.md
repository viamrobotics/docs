---
title: "Switch Component"
linkTitle: "Switch"
childTitleEndOverwrite: "Switch Component"
weight: 100
type: "docs"
description: "A physical multi-position switch on a machine."
tags: ["switch", "components"]
icon: true # this should be used when the image is an icon, it will adjust the sizing and object-fit
images: ["/icons/components/switch.svg"]
no_list: true
modulescript: true
date: "2025-02-20"
# SMEs:
---

The switch component provides an API for reading the state of a physical switch on a machine that has multiple discrete positions.
A simple switch has two positions, and a knob could have any number of positions.

## Configuration

To use your switch, you need to add it to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your switch.

The following list shows the available switch models.
For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:switch" type="component" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component compatible with the Micro-RDK.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The [switch API](/dev/reference/apis/components/switch/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/switch-table.md" >}}

## Troubleshooting

If your switch is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review your switch model's documentation to ensure you have configured all required attributes.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the switch there.
1. Disconnect and reconnect your switch.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper" noimage="true" %}}
{{< /cards >}}
