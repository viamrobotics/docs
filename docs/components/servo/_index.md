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

The servo component provides an API for controlling the angular position of a servo precisely or getting its current status.

If you have a physical ["RC" or "hobby" servo motor](https://learn.adafruit.com/adafruit-motor-selection-guide/rc-servos) with built-in potentiometer position sensors, configure it as a servo component.

If your motor is coupled with an [encoder](/components/encoder/), not a potentiometer, for position feedback, you should configure it as an [encoded motor](/components/motor/encoded-motor/) instead.

## Available models

To use a hobby servo, you need to add it to your machine's configuration.

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

The [servo API](/appendix/apis/components/servo/) supports the following methods:

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
