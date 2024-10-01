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
# SME: Rand
---

The motor component provides an API for operating a motor or getting its current status.

If you have a device that converts electricity into rotary motion, such as a brushed DC motor, a brushless DC motor, or a stepper motor, configure it as a motor component.

If you have a hobby servo, configure it as a [servo component](/components/servo/) instead.

## Available models

To use a motor, you need to add it to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your motor.

Because your machine controls your motor using a [motor driver](https://www.wellpcb.com/what-is-motor-driver.html), you technically need to select a motor model that supports your motor driver rather than the motor itself.

The following list shows the available motor models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:motor" type="motor" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`gpio`](./gpio-micro-rdk/) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor) |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The [motor API](/appendix/apis/components/motor/) supports the following methods:

The motor component supports the following methods:

{{< readfile "/static/include/components/apis/generated/motor-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{% card link="/get-started/control-motor/" noimage="true" %}}
{{< /cards >}}
