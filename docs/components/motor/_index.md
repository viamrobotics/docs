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

If you have a physical motor that convert electricity into rotary motion, configure it as a _motor_ component.

The motor component is often used with the following services:

- [motion service](/services/slam/): to move machines or components of machines
- [navigation service](/services/navigation/): to navigate with GPS
- [SLAM service](/services/slam/): for mapping

## Available models

To use a motor, you have to add it, as well as any dependencies, such as a [board component](/components/board/), to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your motor.

The _motor_ component type natively supports brushed DC motors, brushless DC motors, and stepper motors controlled by a variety of [motor drivers](https://www.wellpcb.com/what-is-motor-driver.html).

The following list shows you the available arm models.
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

To get started using your motor, see the [motor API](/appendix/apis/components/motor/), which supports the following methods:

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
