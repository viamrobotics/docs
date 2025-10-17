---
title: "Motor Component"
linkTitle: "Motor"
childTitleEndOverwrite: "Motor Component"
weight: 70
type: "docs"
description: "A motor is a rotating machine that transforms electrical energy into mechanical energy."
tags: ["motor", "components"]
icon: true
images: ["/icons/components/motor.svg"]
no_list: true
modulescript: true
aliases:
  - "/components/motor/"
  - /micro-rdk/motor/
  - /build/micro-rdk/motor/
hide_children: true
date: "2024-10-21"
# SME: Rand
---

The motor component provides an API for operating a motor or getting its current status.

If you have a device that converts electricity into rotary motion, such as a brushed DC motor, a brushless DC motor, or a stepper motor, configure it as a motor component.

If you have a hobby servo, configure it as a [servo component](/operate/reference/components/servo/) instead.

## Configuration

To use a motor, you need to add it to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your motor and its motor driver.

The following list shows the available motor models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:motor" type="motor" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`gpio`](./gpio-micro-rdk/) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor) |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The [motor API](/dev/reference/apis/components/motor/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/motor-table.md" >}}

## Troubleshooting

If your motor is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review your motor model's documentation to ensure you have configured all required attributes.
1. Check that all wires are securely attached to the correct pins.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the motor there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
