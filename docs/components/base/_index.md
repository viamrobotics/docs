---
title: "Base Component"
linkTitle: "Base"
weight: 10
type: "docs"
no_list: true
description: "The base component allows your to move A moving platform together without needing to address individual components like wheels."
tags: ["base", "components"]
icon: true
images: ["/icons/components/base.svg"]
modulescript: true
aliases:
  - "/components/base/"
  - "/micro-rdk/base/"
  - "/build/micro-rdk/base/"
hide_children: true
# SMEs: Steve B
---

A base is the platform of a robot with other components, such as wheels, attached to it.
By using a base you can coordinate movement of the robot as a whole without needing to send commands to individual components.

<p>
<img src="/components/base/base-trk-rover-w-arm.png" alt="A robot comprised of a wheeled base (motors, wheels and chassis) as well as some other components. The wheels are highlighted to indicate that they are part of the concept of a 'base', while the non-base components are not highlighted. The width and circumference are required attributes when configuring a base component." class="imgzoom aligncenter" style="max-width: 500px">
</p>

## Available models

To use a rover or other base, you have to add it to your machine's configuration.

Most mobile robots with a base need at least the following hardware:

- A [board](/components/board/).
- Some sort of actuators to move the base.
  Usually [motors](/components/motor/) attached to wheels or propellers.
- A power supply for the board.
- A power supply for the actuators.
- Some sort of chassis to hold everything together.

Go to your machine's **CONFIGURE** page, and add your individual a model that supports your base.
Then add your base.

The following list shows you the available arm models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:base" type="base" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`two_wheeled_base`](two_wheeled_base/) | Mobile robot with two wheels |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## Related services

The base component is often used with the following services:

{{< cards >}}
{{< relatedcard link="/services/base-rc/" >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/navigation/" >}}
{{< /cards >}}

## API

The base component supports the following methods:

{{< readfile "/static/include/components/apis/generated/base-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/configure/configure-rover/" %}}
{{% card link="/how-tos/drive-rover/" %}}
{{% card link="/tutorials/services/webcam-line-follower-robot/" %}}
{{< /cards >}}
