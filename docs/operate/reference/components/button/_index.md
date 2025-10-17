---
title: "Button Component"
linkTitle: "Button"
childTitleEndOverwrite: "Button Component"
weight: 20
type: "docs"
description: "A physical button on a machine."
tags: ["button", "components"]
icon: true # this should be used when the image is an icon, it will adjust the sizing and object-fit
images: ["/icons/components/button.svg"]
no_list: true
modulescript: true
date: "2025-02-20"
# SMEs:
---

The button component provides an API for getting presses of a physical button on a machine.

## Configuration

To use your button component, check whether one of the following models supports it.

For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:button" type="component" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component compatible with the Micro-RDK.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The [button API](/dev/reference/apis/components/button/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/button-table.md" >}}

## Troubleshooting

If your button is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review your button model's documentation to ensure you have configured all required attributes.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the button there.
1. Disconnect and reconnect your button.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper" noimage="true" %}}
{{< /cards >}}
