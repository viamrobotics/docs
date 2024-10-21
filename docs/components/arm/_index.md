---
title: "Arm Component"
linkTitle: "Arm"
childTitleEndOverwrite: "Arm Component"
weight: 10
type: "docs"
description: "A robotic arm is made up of a series of links and joints, ending with a device you can position."
no_list: true
tags: ["arm", "components"]
icon: true
images: ["/icons/components/arm.svg"]
modulescript: true
aliases:
  - "/components/arm/"
hide_children: true
outputs:
  - html
  - typesense
date: "2024-10-21"
# SME: Peter L
---

The arm component provides an API for linear motion planning, including self-collision prevention and obstacle avoidance.

If you have a physical robotic arm, consisting of a serial chain of joints and links, with a fixed end and an end effector end, use an arm component.

Arms have two ends: one fixed in place, and one with a device you can position.
When controlling an arm, you can place its end effector at arbitrary cartesian positions relative to the base of the arm.

## Configuration

To use a robotic arm, you need to add it to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your arm.

The following list shows the available arm models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:arm" type="arm" no-intro="true">}}

{{< alert title="Add support for other models" color="tip" >}}

If none of the existing models fit your use case, you can create a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} to add support for it.

You can follow [this guide](/registry/examples/custom-arm/) to implement your arm model.

{{< /alert >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component in `viam-micro-server`.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The [arm API](/appendix/apis/components/arm/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/arm-table.md" >}}

## Motion planning with your arm

Each arm model provided by Viam wraps the arm manufacturer's API with the Viam [arm API](#api).
The arm API handles turning the arm on and off, sending requests for the arm to move to a set of joint positions, and engaging brakes, if supported.
Viam's motion service provides an [API for moving the end of the arm to a given position, around any obstacles](/services/motion/#api).
Some arm manufacturers build inverse kinematics into their software, but the Viam motion service bypasses it, so all arms are controlled by the motion service in the same way.

For each arm model, there is a JSON file that describes the [kinematics parameters of the arm](/internals/kinematic-chain-config/#kinematic-parameters).
When you configure an arm model, the arm driver will load and parse the kinematics file for the [frame system](/services/frame-system/) service to use.
The frame system allows the motion service to calculate where any component of your machine is relative to any other component, other machine, or object in the environment.

## Troubleshooting

If your arm is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
2. Review your arm model's documentation to ensure you have configured all required attributes.
3. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the arm there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{% card link="/tutorials/services/accessing-and-moving-robot-arm" noimage="true" %}}
{{< /cards >}}

You can also use the arm component with the following services:

- [Motion service](/services/slam/): To move machines or components of machines
- [Frame system service](/services/navigation/): To configure the positions of your components
