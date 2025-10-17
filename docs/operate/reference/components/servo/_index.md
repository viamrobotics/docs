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
date: "2024-10-21"
# SME: #team-bucket
---

The servo component provides an API for controlling the angular position of a servo precisely or getting its current status.

If you have a physical ["RC" or "hobby" servo motor](https://learn.adafruit.com/adafruit-motor-selection-guide/rc-servos) with built-in potentiometer position sensors, configure it as a servo component.

If you have an industrial servo motor, configure or [create](/operate/modules/support-hardware/) a [motor component](/operate/reference/components/motor/) that supports your hardware.

## Configuration

To use a hobby servo, you need to add it to your machine's configuration.

Go to your machine's **CONFIGURE** page, and add a model that supports your servo.

For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:servo" type="servo" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`gpio`](gpio-micro-rdk/) | A hobby servo. |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The [servo API](/dev/reference/apis/components/servo/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/servo-table.md" >}}

## Troubleshooting

If your servo is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review your servo model's documentation to ensure you have configured all required attributes.
1. Check that all wires are securely attached to the correct pins on the board.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the servo there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
