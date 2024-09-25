---
title: "Servo Component"
linkTitle: "Servo"
childTitleEndOverwrite: "Servo Component"
weight: 80
type: "docs"
description: "A hobby servo is a special type of small motor whose position you can precisely control."
tags: ["servo", "components"]
icon: true
images: ["/icons/components/servo.svg"]
no_list: true
modulescript: true
aliases:
  - "/components/servo/"
  - /micro-rdk/servo/
  - /build/micro-rdk/servo/
hide_children: true
# SME: #team-bucket
---

The servo component supports ["RC" or "hobby" servo motors](https://learn.adafruit.com/adafruit-motor-selection-guide/rc-servos).
These are small motors with built-in potentiometer position sensors, enabling you to control the angular position of the servo precisely.

As servos can use a lot of power, drawing voltage away from a [board](/components/board/), you should power your servo with its own power supply in most cases.
The following shows an example wiring diagram for a hobby servo wired to a [`viam:raspberry-pi:rpi` board](https://github.com/viam-modules/raspberry-pi):

![A diagram showing the signal wire of a servo connected to pin 16 on a Raspberry Pi. The servo's power wires are connected to a 4.8V power supply.](/components/servo/servo-wiring.png)

The colors of the servo wires in this diagram may not match your servo.
Refer to your servo's data sheet for wiring specifications.

Most machines with a servo need at least the following hardware:

- A [board component](/components/board/) that can run `viam-server`
- A servo
- A power supply for the board
- A power supply for the servo

## Related services

{{< cards >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/data/" >}}
{{< /cards >}}

{{% alert title="Tip" color="tip" %}}

The Viam servo component supports [hobby servos](https://learn.adafruit.com/adafruit-motor-selection-guide/rc-servos).

If your motor is coupled with an [encoder](/components/encoder/), not a potentiometer, for position feedback, you should not configure it as a servo.
Check your device's data sheet and configure that type of servo as an [encoded motor](/components/motor/encoded-motor/).

{{% /alert %}}

## Available models

To use your servo component, check whether one of the following models supports it.

For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:servo" type="servo" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`gpio`](gpio-micro-rdk/) | A hobby servo. |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The servo component supports the following methods:

{{< readfile "/static/include/components/apis/generated/servo-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/projects/guardian" %}}
{{% card link="/tutorials/configure/configure-rover" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai" %}}
{{< /cards >}}
