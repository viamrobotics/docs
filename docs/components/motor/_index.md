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

Electric motors are machines that convert electricity into rotary motion.
They are the most common form of [actuator](https://en.wikipedia.org/wiki/Actuator) in robotics.
The _motor_ component type natively supports brushed DC motors, brushless DC motors, and stepper motors controlled by a variety of [motor drivers](https://www.wellpcb.com/what-is-motor-driver.html).

Most machines with a motor need at least the following hardware:

- The motor itself.
- A compatible motor driver.
  This takes signals from the computer and sends the corresponding signals and power to the motor.
  Selected based on the type of motor (for example, brushed, brushless, or stepper) and its power requirements.
- A [board component](/components/board/) to send signals to the motor driver[^dmcboard].
  For example, a Raspberry Pi, or another model of single-board computer with GPIO (general purpose input/output) pins.

[^dmcboard]: The `DMC4000` model does not require a board.

## Related services

{{< cards >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/motion/" >}}
{{< relatedcard link="/services/navigation/" >}}
{{< relatedcard link="/services/slam/" >}}
{{< /cards >}}

## Supported models

To use your motor component, check whether one of the following models supports it.

For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="RDK" %}}

{{<resources api="rdk:component:motor" type="motor" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="micro-RDK" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`gpio`](./gpio-micro-rdk/) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor) |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## Control your motor with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a motor called `"my_motor"` configured as a component of your machine.
If your motor has a different name, change the `name` in the code.

Be sure to import the motor package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.motor import Motor
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/motor"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The motor component supports the following methods:

{{< readfile "/static/include/components/apis/generated/motor-table.md" >}}

{{< alert title="micro-RDK Support" color="note" >}}
The motor API is limited to the following supported client SDK API methods for microcontrollers:

- [`SetPower()`](/components/motor/#setpower)
- [`GetPosition()`](/components/motor/#getposition)
- [`GetProperties()`](/components/motor/#getproperties)
- [`Stop()`](/components/motor/#stop)
- [`IsMoving()`](/components/motor/#ismoving)
{{< /alert >}}

{{< readfile "/static/include/components/apis/generated/motor.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next steps

{{< cards >}}
{{% card link="/tutorials/get-started/confetti-bot/" %}}
{{% card link="/tutorials/get-started/lazy-susan/" %}}
{{% card link="/tutorials/configure/configure-rover" %}}
{{< /cards >}}
