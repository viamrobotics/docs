---
title: "Access and Move a Robot Arm"
linkTitle: "Move a Robot Arm"
type: "docs"
description: "Access and control one of the most fundamental systems in robotics: A robotic arm."
imageAlt: "A robotic arm"
images: ["/tutorials/motion/preview.jpg"]
tags: ["arm", "motion", "services"]
aliases:
  - "/tutorials/motion/accessing-and-moving-robot-arm"
  - "/tutorials/motion/"
authors: []
languages: ["python", "go"]
viamresources: ["arm"]
level: "Intermediate"
date: "2023-03-07"
# updated: ""
cost: 8400
no_list: true
---

<!-- LEARNING GOALS
After following this tutorial, you will know how to set up your components in the frame system and to move your components without the motion service. You will know that the motion service exists.
-->

{{< alert title="Caution" color="caution" >}}
Be careful when instructing robot arms to move.
Before running any code, ensure your robotic arm has enough space and that there are no obstacles.
Also pay attention to your surroundings, double-check your code for correctness, and make sure anyone nearby is aware and alert before issuing commands to your machine.
{{< /alert >}}

The following instructions show you how to interact with an [arm component](/components/arm/), help you understand how an arm describes its state, and assist you in issuing movement commands to your robotic arm.

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/motion/access_01_xarm6.png" resize="500x" declaredimensions=true alt="A picture of the UFACTORY xArm 6." class="alignright" style="max-width: 400px" >}}
</div>

Code examples in this tutorial use a [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6), but you can use any [arm model](/components/arm/).

If you do not have a robotic arm of your own, the [fake arm component page](/components/arm/fake/) shows how you can set up a virtual robotic arm with the same kinematic model as a real robotic arm.
Configure it with `"arm-model": "xArm6"` in its `attributes`.
You can then continue through the code examples in this tutorial without making any changes (and without needing to buy or build an expensive robot arm)!

The [full tutorial code](#full-tutorial-code) is available at the end of this page.

## Prerequisites

Before starting this tutorial, make sure you have the [Viam Python SDK](https://python.viam.dev/) or the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme) installed.

If you are connecting to a real robotic arm during this tutorial, make sure your computer can communicate with the controller before continuing.

## Configure a machine

{{% snippet "setup.md" %}}

1. Once your machine is live, select the **CONFIGURE** tab.
1. Click on the **+** symbol next to your machine in the **Builder** panel and select **Component** in the menu that opens:

   - Choose `arm` as the type.
   - Choose your desired model.
     - For example, if you're using an xArm 6, choose the `xArm6` model from the list.
   - Enter `myArm` as the **Name** for this component, then click **Create**.

1. In the newly created `myArm` component panel, configure any attributes as needed.
   Refer to the documentation for the model for information about your arm's model.

1. Switch to the **Frame** mode and select `myArm` in the left-hand menu to see the default values for your arm.
   You do not need to change the default values that populate the new frame card.

   <!-- TODO -->

   {{<imgproc src="/tutorials/motion/access_02_arm_config.png" resize="1000x" declaredimensions=true alt="Sample machine arm configuration with several fields filled out." style="max-width: 600px" >}}

1. Save your machine configuration.

1. Go to the **Code sample** page of the **CONNECT** tab and select the programming language you are working in.

   {{% snippet "show-secret.md" %}}

   Then, copy and paste the boilerplate code into a file and run the resulting script to verify you can connect to your machine.
   Throughout the rest of this tutorial, you will replace and amend this code.
   The [full tutorial code](#full-tutorial-code) is available at the bottom of this tutorial for reference.

## Access the arm

The `arm` component library has several methods to simplify accessing and working with robotic arms.
In this step, you'll fetch data about the robotic arm's current position.

{{< tabs >}}
{{% tab name="Python" %}}
Your script will resemble the following lines from the [full **Python** tutorial code](#full-tutorial-code) which enable you to use the `myArm` component you configured earlier.
The code then calls the [`get_end_position`](/components/arm/#getendposition) method to get the position of the **end of the robot arm with respect to the arm's base**.

```python {class="line-numbers linkable-line-numbers"}
# Access myArm
my_arm = Arm.from_robot(machine, "myArm")

# End Position of myArm
my_arm_return_value = await my_arm.get_end_position()
print(f"myArm get_end_position return value: {my_arm_return_value}")
```

You should see output that looks similar to the following:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
myArm get_end_position return value: x: 200.73450755898915
y: 0.0028507667654201754
z: 108.63966593621173
o_x: -0.019650946400315308
o_y: -1.5485718223024914e-07
o_z: -0.99980690150926033
theta: -179.99979233107763
```

The `x`, `y`, and `z` values correspond to the `position` element of the pose, while the `o_x`, `o_y`, `o_z`, and `theta` values are for the `orientation` element of the pose (presented as an [Orientation Vector](/internals/orientation-vector/)).

{{% /tab %}}
{{% tab name="Go" %}}
Your script will resemble the following lines from the [full **Go** tutorial code](#full-tutorial-code) which enable you to use the `myArm` component you configured earlier.
The code then calls the [`EndPosition`](/components/arm/#getendposition) method to get the position of the **end of the robot arm with respect to the arm's base**.

```go {class="line-numbers linkable-line-numbers"}
// Access myArm
myArmComponent, err := arm.FromRobot(machine, "myArm")
if err!=nil {
  logger.Error(err)
  return
}

// End Position of myArm
myArmReturnValue, err:= myArmComponent.EndPosition(context.Background(), map[string]interface{}{})
if err!=nil {
  logger.Error(err)
  return
}
logger.Infof("myArm EndPosition return value: %+v", myArmReturnValue)

```

You should see output that looks similar to the following:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
myArm EndPosition position return value: (200.734507558989150766137755, 0.002850766765420175395673, 108.639665936211727625959611)
```

The `Position` value is part of a `Pose`.

{{% /tab %}}
{{< /tabs >}}

The state of a robot arm can also be described as the **combined positions of each joint** attached to the arm.
You can access a robot arm's "joint states" (as they are sometimes referred to) by calling a different method on the arm component.
Add the following code right after the code that gets the end effector pose from the prior code sample.
When you run the code, you'll see that these two pieces of information are presented differently.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Joint Positions of myArm
my_arm_joint_positions = await my_arm.get_joint_positions()
print(f"myArm get_joint_positions return value: {my_arm_joint_positions}")
```

You should see output that looks similar to the following:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
myArm get_joint_positions return value: values: 0.00043945314765093886
values: 0.46724854536551791
values: 0.64500731344456741
values: -0.00098876951707685271
values: 0.013732909913080547
values: 0.00076904296930648713
```

Each individual value corresponds to the current position of a particular joint on your robot.
You can also see these values reflected on the Control tab in the Viam app for your robot arm.

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Joint Positions of myArm
myArmJointPositions, err := myArmComponent.JointPositions(context.Background(), nil)
if err != nil {
  logger.Error(err)
  return
}
logger.Infof("myArm JointPositions return value:", myArmJointPositions)
```

You should see output that looks similar to the following:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
myArm JointPositions return value: values:0.00043945314765093886  values:0.4672485453655179  values:0.6450073134445674  values:-0.0009887695170768527  values:0.013732909913080547  values:0.0007690429693064871
```

Each individual value corresponds to the current position of a particular joint on your robot.
You can also see these values reflected on the **Control** tab in the Viam app for your robot arm.

{{% /tab %}}
{{< /tabs >}}

Both representations of an arm's state are important.
Sometimes you may wish to direct an arm in terms of joint positions.
Other times you may need to describe the position of another object with respect to the end of the robot arm.
There is a mathematical relationship that allows you to convert between these two representations, known as the **forward and inverse kinematics**, which is foundational to complex robotic motion.
We will not cover forward and inverse kinematics in this tutorial, but resources for further reading on these topics are linked in the [**Next Steps**](#next-steps-and-references) section.

## Move the arm

The two main options for specifying arm movement are through **joint position commands** and through **pose commands**.
Let's start with joint position commands, as their formulation is a little simpler.

### Joint position commands

First, you can initiate motion with a joint position command.
A final note:

{{< alert title="Caution" color="caution" >}}
Executing code presented after this point _will_ induce motion in a connected robotic arm!
{{< /alert >}}

{{< tabs >}}
{{% tab name="Python" %}}
Add the following line to your import list to be able to assign values to a `JointPositions` data structure:

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.component.arm import JointPositions
```

See the [arm reference document](/components/arm/#movetojointpositions) for further details on how to structure data that you pass to the `move_to_joint_positions` function.

```python {class="line-numbers linkable-line-numbers"}
# Command a joint position move: move the forearm of the arm slightly up
cmd_joint_positions = JointPositions(values=[0, 0, -30.0, 0, 0, 0])
await my_arm.move_to_joint_positions(positions=cmd_joint_positions)
```

{{% /tab %}}
{{% tab name="Go" %}}
You must import an additional Go library to access the data structure that Viam uses to encode joint positions, which is shown next.

Add `armapi "go.viam.com/api/component/arm/v1"` to your import list to be able to assign values to an `armapi.JointPositions` data structure.
See the [arm reference document](/components/arm/#movetojointpositions) for further details on how to structure data that you pass to the `MoveToJointPositions` function.

```go {class="line-numbers linkable-line-numbers"}
// Command a joint position move: move the forearm of the arm slightly up
cmdJointPositions := &armapi.JointPositions{Values: []float64{0.0, 0.0, -30.0, 0.0, 0.0, 0.0}}
err = myArmComponent.MoveToJointPositions(context.Background(), cmdJointPositions, nil)
if err != nil {
  logger.Error(err)
  return
}
```

{{% /tab %}}
{{< /tabs >}}

If you execute the sample joint move statement above, the third joint of your arm should move a small amount (30 degrees).
Feel free to experiment further with joint position commands by changing the values for each joint and re-sending the commands.

When you are ready to move on, the next section will show you how to use **pose commands**.

### Pose commands

When you [got the end position of the arm](#access-the-arm), this data was returned in the format of a `Pose`.
The returned `Pose` is a combination of position and orientation data that indicates the end of the arm's full 6-dimensional configuration in space.

The following code sample reuses the methods to get the pose of the end of the arm so that you can make small adjustments at will.
You can then pass the adjusted pose back to the arm as a **goal** pose for the purposes of starting motion.
For example, the following code gets the arm's end position, makes a 100 millimeter adjustment in the +Z direction, and then uses that adjustment as a goal when commanding arm motion.

{{< tabs >}}
{{% tab name="Python" %}}
Add the sample code below to your own client script to try using the arm component's [`move_to_position`](/components/arm/#movetoposition) command.
This example gets a `Pose` from `get_end_position()` so no additional imports are required.
If you want to synthesize new poses directly, note that you must import an additional Python package by adding `from viam.proto.common import Pose` to your import list.

```python {class="line-numbers linkable-line-numbers"}
# Generate a simple pose move +100mm in the +Z direction of the arm
cmd_arm_pose = await my_arm.get_end_position()
cmd_arm_pose.z += 100.0
await my_arm.move_to_position(pose=cmd_arm_pose)
```

{{% /tab %}}
{{% tab name="Go" %}}
You must import some additional Go packages to synthesize new poses through the `spatialmath` library for the arms's [`MoveToPosition`](/components/arm/#movetoposition) command.
Add `"go.viam.com/rdk/referenceframe"` and `"go.viam.com/rdk/spatialmath"` to your import list and then add the sample code below to your own client script.

```go {class="line-numbers linkable-line-numbers"}
// Generate a simple pose move +100mm in the +Z direction of the arm
currentArmPose, err := myArmComponent.EndPosition(context.Background(), nil)
if err != nil {
  logger.Error(err)
  return
}
adjustedArmPoint := currentArmPose.Point()
adjustedArmPoint.Z += 100.0
cmdArmPose := spatialmath.NewPose(adjustedArmPoint, currentArmPose.Orientation())

err = myArmComponent.MoveToPosition(context.Background(), cmdArmPose, nil)
if err != nil {
  logger.Error(err)
  return
}
```

{{% /tab %}}
{{< /tabs >}}

Using this code you can quickly adjust one or more elements of position AND orientation simultaneously, by modifying other elements of the original arm pose.

For all motion actions taken in this tutorial, there may be joint positions or poses that are unreachable for particular reasons (potential collisions, a pose in space is unreachable because the arm is too short).
Regularly check your client script's feedback and the `viam-server` logs for any issues that may arise.

## Next steps and references

If you would like to continue onto working with Viam's motion service, check out one of these tutorials:

{{< cards >}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper" %}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{< /cards >}}

{{< snippet "social.md" >}}

For more resources on robot kinematics, read through the Wikipedia pages for [Forward kinematics](https://en.wikipedia.org/wiki/Forward_kinematics) and [Inverse kinematics](https://en.wikipedia.org/wiki/Inverse_kinematics).

## Full tutorial code

{{< tabs >}}
{{% tab name="Python" %}}

```python {id="access-move-arm-python-ex" class="line-numbers linkable-line-numbers" data-line=""}
import asyncio

from viam.components.arm import Arm
from viam.proto.component.arm import JointPositions
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions


async def connect():
    opts = RobotClient.Options.with_api_key(
      # Replace "<API-KEY>" (including brackets) with your machine's API key
      api_key='<API-KEY>',
      # Replace "<API-KEY-ID>" (including brackets) with your machine's API key
      # ID
      api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)


async def main():
    machine = await connect()

    print('Resources:')
    print(machine.resource_names)

    # Access myArm
    my_arm = Arm.from_robot(machine, "myArm")

    # End Position of myArm
    my_arm_end_position = await my_arm.get_end_position()
    print(f"myArm get_end_position return value: {my_arm_end_position}")

    # Joint Positions of myArm
    my_arm_joint_positions = await my_arm.get_joint_positions()
    print(f"myArm get_joint_positions return value: {my_arm_joint_positions}")

    # Command a joint position move: small adjustment to the last joint
    cmd_joint_positions = JointPositions(values=[0, 0, 0, 0, 0, 15.0])
    await my_arm.move_to_joint_positions(
        positions=cmd_joint_positions)

    # Generate a simple pose move +100mm in the +Z direction of the arm
    cmd_arm_pose = await my_arm.get_end_position()
    cmd_arm_pose.z += 100.0
    await my_arm.move_to_position(pose=cmd_arm_pose)

    # Don't forget to close the robot when you're done!
    await machine.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% snippet "show-secret.md" %}}

{{% /tab %}}
{{% tab name="Go" %}}

```go {id="access-move-arm-go-ex" class="line-numbers linkable-line-numbers" data-line=""}
package main

import (
  "context"

  armapi "go.viam.com/api/component/arm/v1"
  "go.viam.com/rdk/logging"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/utils/rpc"
  "go.viam.com/rdk/components/arm"
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/spatialmath"
  "go.viam.com/rdk/utils"
  "go.viam.com/utils/rpc"
)

func main() {
  logger := logging.NewLogger("client")
  machine, err := client.New(
      context.Background(),
      "ADDRESS FROM THE VIAM APP",
      logger,
      client.WithDialOptions(rpc.WithEntityCredentials(
      // Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
      "<API-KEY-ID>",
      rpc.Credentials{
          Type:    rpc.CredentialsTypeAPIKey,
          // Replace "<API-KEY>" (including brackets) with your machine's API key
          Payload: "<API-KEY>",
      })),
  )
  if err != nil {
      logger.Fatal(err)
  }
  defer machine.Close(context.Background())

  logger.Info("Resources:")
  logger.Info(machine.ResourceNames())

  // Access myArm
  myArmComponent, err := arm.FromRobot(machine, "myArm")
  if err != nil {
    logger.Error(err)
    return
  }

  // End Position of myArm
  myArmReturnValue, err := myArmComponent.EndPosition(context.Background(), nil)
  if err != nil {
    logger.Error(err)
    return
  }
  logger.Infof("myArm EndPosition return value: %+v", myArmReturnValue)

  // Joint Positions of myArm
  myArmJointPositions, err := myArmComponent.JointPositions(context.Background(), nil)
  if err != nil {
    logger.Error(err)
    return
  }
  logger.Infof("myArm JointPositions return value:", myArmJointPositions)

  // Command a joint position move: small adjustment to the last joint
  cmdJointPositions := &armapi.JointPositions{Values: []float64{0.0, 0.0, 0.0, 0.0, 0.0, 15.0}}
  err = myArmComponent.MoveToJointPositions(context.Background(), cmdJointPositions, nil)
  if err != nil {
    logger.Error(err)
    return
  }

  // Generate a simple pose move +100mm in the +Z direction of the arm
  currentArmPose, err := myArmComponent.EndPosition(context.Background(), nil)
  if err != nil {
    logger.Error(err)
    return
  }
  adjustedArmPoint := currentArmPose.Point()
  adjustedArmPoint.Z += 100.0
  cmdArmPose := spatialmath.NewPose(adjustedArmPoint, currentArmPose.Orientation())

  err = myArmComponent.MoveToPosition(context.Background(), cmdArmPose, nil)
  if err != nil {
    logger.Error(err)
    return
  }
}
```

{{% snippet "show-secret.md" %}}

{{% /tab %}}
{{< /tabs >}}
