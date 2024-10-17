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

If none of the existing models fit your use case, you can [create a modular resource](/registry/) to add support for it.

You can follow [this guide](/registry/examples/custom-arm/) to implement your custom arm as a [modular resource](/registry/).

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

## Motion planning with your arm's built-in software

Each arm model is supported with a driver that is compatible with the software API that the model's manufacturer supports.
While some arm models build inverse kinematics into their software, many do not.

- Most of the arm drivers for the Viam RDK bypass any onboard inverse kinematics, and use Viam's [motion service](/services/motion/) instead.

- This driver handles turning the arm on and off, querying the arm for its current joint position, sending requests for the arm to move to a specified set of joint positions, and engaging brakes as needed, if supported.

Arm drivers are also paired, in the RDK, with JSON files that describe the kinematics parameters of each arm.

- When you configure a supported arm model to connect to `viam-server`, the Arm driver will load and parse the kinematics file for the Viam RDK's [frame system](/services/frame-system/) service to use.

- The [frame system](/services/frame-system/) will allow you to easily calculate where any part of your machine is relative to any other part, other machine, or piece of the environment.

- All arms have a `Home` position, which corresponds to setting all joint angles to 0.

- When an arm is moved with a `move_to_position` call, the movement will follow a straight line, and not deviate from the start or end orientations more than the start and orientations differ from one another.

- If there is no way for the arm to move to the desired location in a straight line, or if it would self-collide or collide with an obstacle that was passed in as something to avoid, then the `move_to_position` call will fail.

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
