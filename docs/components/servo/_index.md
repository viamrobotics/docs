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

If you have a physical ["RC" or "hobby" servo motors](https://learn.adafruit.com/adafruit-motor-selection-guide/rc-servos), configure it as a _servo_ component.
Servos are small motors with built-in potentiometer position sensors, enabling you to control the angular position of the servo precisely.

If your motor is coupled with an [encoder](/components/encoder/), not a potentiometer, for position feedback, you should configure it as an [encoded motor](/components/motor/encoded-motor/) instead.
Check your device's data sheet for more information.

## Available models

To use a hobby servo, you have to add it, and its dependencies, to your machine's configuration.
Generally servo's depend on a [board component](/components/board/).

Go to your machine's **CONFIGURE** page, and add a model that supports your servo.

For additional configuration information, click on the model name:

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

To get started using your servo, see the [servo API](/appendix/apis/components/servo/), which supports the following methods:

{{< readfile "/static/include/components/apis/generated/servo-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{< /cards >}}
