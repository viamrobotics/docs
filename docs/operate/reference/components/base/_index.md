---
title: "Base Component"
linkTitle: "Base"
weight: 14
type: "docs"
no_list: true
description: "The base component allows you to move a mobile robot without needing to send commands to individual components like motors."
tags: ["base", "components"]
icon: true
images: ["/icons/components/base.svg"]
modulescript: true
aliases:
  - "/components/base/"
  - "/micro-rdk/base/"
  - "/build/micro-rdk/base/"
hide_children: true
date: "2024-10-21"
# SMEs: Steve B
---

The base component provides an API for moving all configured drive motors of a mobile robot platform as a whole without needing to send commands to individual motor components.

If you have a mobile robot, use a base component to coordinate the motion of its motor components.

<p>
<img src="/components/base/base-trk-rover-w-arm.png" alt="A robot comprised of a wheeled base (motors, wheels and chassis) as well as some other components. The wheels are highlighted to indicate that they are part of the concept of a 'base', while the non-base components are not highlighted. The width and circumference are required attributes when configuring a base component." class="imgzoom aligncenter" style="width: 550px">
</p>

## Configuration

Most mobile robots with a base use the following hardware:

- Some actuators to move the base, such as [motors](/operate/reference/components/motor/) attached to wheels or propellers
- Some sort of chassis to hold everything together

To use a rover or other base, you need to add each component as well as the base to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your base.

The following list shows the available base models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:base" type="base" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`two_wheeled_base`](two_wheeled_base/) | Mobile robot with two wheels |

{{% readfile "/static/include/micro-create-your-own.md" %}}

{{% /tab %}}
{{< /tabs >}}

## API

The [base API](/dev/reference/apis/components/base/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/base-table.md" >}}

## Troubleshooting

If your base is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review your base model's documentation to ensure you have configured all required attributes.
1. Review your configuration for any motors that are components of the base.
   Check that the names of the motor components match the list of motors you configured on the base.
1. If a motor is spinning in an unexpected direction, try using the `dir_flip` attribute in its config, or try swapping the wires running to the motor to change its direction.
1. Check that all wires are securely attached to the correct pins.
1. If you are using a battery to power the base, check that it is adequately charged.
   If the motors are drawing more power than the battery can supply, the single-board computer may be power cycling.
   Consider using a wall power supply for testing purposes to rule out this issue.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the base there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{% card link="/tutorials/configure/configure-rover/" noimage="true" %}}
{{% card link="/tutorials/control/drive-rover/" noimage="true" %}}
{{< /cards >}}

You can also use the base component with the following services:

- [Navigation service](/operate/reference/services/navigation/): to navigate with GPS
- [SLAM service](/operate/reference/services/slam/): for mapping
