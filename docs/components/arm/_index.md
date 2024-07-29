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

A robotic arm is a serial chain of joints and links, with a fixed end and an end effector end.
Joints may rotate, translate, or both, while a link is a rigid connector between joints.

In simple terms, an _arm_ has two ends: one fixed in place, and one with a device you can position.

When controlling an arm component, you can place the end effector at arbitrary cartesian positions relative to the base of the arm.
You can do this by calling the `MoveToPosition` method to move the end effector to specified cartesian coordinates, or by controlling the joint positions directly with the `MoveToJointPositions` method.

When controlling an arm with `viam-server`, the following features are implemented for you:

- Linear motion planning
- Self-collision prevention
- Obstacle avoidance

## Motion planning with your arm's built-in software

Each arm model is supported with a driver that is compatible with the software API that the model's manufacturer supports.
While some arm models build inverse kinematics into their software, many do not.

- Most of the arm drivers for the Viam RDK bypass any onboard inverse kinematics, and use Viam's [motion service](/services/motion/) instead.

- This driver handles turning the arm on and off, querying the arm for its current joint position, sending requests for the arm to move to a specified set of joint positions, and engaging brakes as needed, if supported.

Arm drivers are also paired, in the RDK, with JSON files that describe the kinematics parameters of each arm.

- When you configure a supported arm model to connect to `viam-server`, the Arm driver will load and parse the kinematics file for the Viam RDK's [frame system](/services/frame-system/) service to use.

- The [frame system](/services/frame-system/) will allow you to easily calculate where any part of your machine is relative to any other part, other machine, or piece of the environment.

- All arms have a `Home` position, which corresponds to setting all joint angles to 0.

- When an arm is moved with a `move_to_position` call, the movement will follow a straight line, and not deviate from the start or end orientations more than the start and orientations differ from one another

- If there is no way for the arm to move to the desired location in a straight line, or if it would self-collide or collide with an obstacle that was passed in as something to avoid, then the `move_to_position` call will fail.

## Related services

{{< cards >}}
{{< relatedcard link="/services/motion/" >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/data/" >}}
{{< /cards >}}

## Available models

To use your arm component, check whether one of the following models supports it.

For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="RDK" %}}

{{<resources api="rdk:component:arm" type="arm" no-intro="true">}}

{{< alert title="Add support for other models" color="tip" >}}

If none of the existing models fit your use case, you can [create a modular resource](/registry/) to add support for it.

You can follow [this guide](/registry/examples/custom-arm/) to implement your custom arm as a [modular resource](/registry/).

{{< /alert >}}

{{% /tab %}}
{{% tab name="micro-RDK" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component in the micro-RDK.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## Control your arm with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have an arm called `"my_arm"` configured as a component of your machine.
If your arm has a different name, change the `name` in the code.

Be sure to import the arm package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.arm import Arm
# To use move_to_position:
from viam.proto.common import Pose
# To use move_to_joint_positions:
from viam.proto.component.arm import JointPositions
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/arm"
  // To use MoveToPosition:
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/spatialmath"
  // To use MoveToJointPositions ("armapi" name optional, but necessary if importing other packages called "v1"):
  armapi "go.viam.com/api/component/arm/v1"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The arm component supports the following methods:

{{< readfile "/static/include/components/apis/generated/arm-table.md" >}}

{{< readfile "/static/include/components/apis/generated/arm.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

{{< cards >}}
{{% card link="/tutorials/services/accessing-and-moving-robot-arm" %}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{< /cards >}}
