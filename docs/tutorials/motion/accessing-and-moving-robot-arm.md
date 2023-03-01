---
title: "Accessing and Moving a Robot Arm"
linkTitle: "Access and Move a Robot Arm"
weight: 5
type: "docs"
description: "A quick orientation in accessing and controlling one of the most fundamental systems in robotics: A robotic arm."
tags: ["arm", "motion"]
# SMEs: William S.
---

{{< alert title="Caution" color="caution" >}}
Before continuing, a word of caution: Whether you are using a real robotic arm or a virtual one, please keep in mind that all Motion tutorials are heavily geared towards action.
You are tasking robots to move through space and around obstacles, so pay attention to your surroundings, double-check your code for correctness, and make sure anyone nearby is aware and alert before issuing commands to your robot.
Stay safe!
{{< /alert >}}

Your first experiences with Viam's Motion service typically starts with a robotic arm.
Before going down the path of doing complex maneuvers with Viam's Motion service, we suggest getting familiar with the Arm component, its interfaces, and how these things work with real robotic hardware.
This tutorial shows you how to interact with arms, helps you understand the ways in which arms describe their state, and assists you in issuing movement commands to a robotic arm.
Code examples in this tutorial assume the use of a [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6), but any supported arm model may be used.

<img src="../../img/motion/access_01_xarm6.png" width="400px" alt="A picture of the UFACTORY xArm 6">

<!-- TODO: Content below struck out for the moment, saved to refer to impending changes in Arm component docs outlining the ability to use a fully virtual arm. -->
<!--
In the event that you do not have a robotic arm of your own, the section on Fake models in the [Arm component page](/components/arm/#fake-arm-modeling) shows how you can set up a virtual robotic arm with the same kinematic model as a real robotic arm.
You can then continue through the code examples in this tutorial without making any changes (and without needing to buy or build an expensive robot arm)!
-->

## Prerequisites

This tutorial should be attempted only after you are comfortable setting up a robot on the Viam app ([https://app.viam.com](https://app.viam.com)) and with running `viam-server`.

Experience working with one Viam SDK is also required.
Sample code is provided throughout this tutorial for both the [Viam Python SDK](https://python.viam.dev/) and the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme), but you should ensure one of these SDKs are properly installed before continuing.

If you are connecting to a real robotic arm during this tutorial, make sure your computer can communicate with the controller before continuing.

## Configure A Robot

1. Navigate to the [robot page on the Viam app](https://app.viam.com/robots).
2. Create a new robot
3. Select the **CONFIG** tab
4. Under the **COMPONENTS** section, create a component with the following attributes:

* Choose `Arm` as the **type** selection
* Choose your desired model in the **model** selection
  * The `xArm 6` choice may be further down the model list
* Enter `myArm` as the **name** for this component

5. In the newly created `myArm` component, fill in some additional details:

* Enter the IP address for your robot controller in the **Host** field
* Enter a desired velocity *(in degrees per second)* for the robot arm's motions in the **Speed** field
  * For an `xArm 6`, a safe value is **15** degrees per second.

6. Add a **Frame** to this component
  * You will not need to change the default values that populate the new frame card

<img src="../../img/motion/access_02_arm_config.png" width="700px" alt="Sample robot arm configuration with several fields filled out.">

7. Save this robot configuration

Before leaving the Viam app, go to the **CODE SAMPLE** tab and copy the code sample for the programming language you are working in.
Paste this boilerplate code into a new script and run the script to verify you can connect to your robot.
Several parts of this code sample will be replaced or amended, so we have provided a full tutorial script at the bottom of this tutorial if confusion arises.

This robot configuration should be specified as you launch `viam-server` before going through the rest of this tutorial.

## Accessing the Arm 

Once you have set up the server with the robot configuration from earlier, you can use the `Arm` component in your client scripts to start interacting with your robotic arm!
The `Arm` component library has several methods to simplify accessing and working with robotic arms.
This tutorial will start with accessing and fetching data about the robotic arm's current position:

{{< tabs >}}
{{% tab name="Go" %}}
The following lines from the full **Go** tutorial code enable you to use the `myArm` component you configured earlier, and then call the `EndPosition` method to get the position of the **end of the robot arm with respect to the arm's base**.

<!-- Insert code link here to portion of Go sample with ...
    myArmResource = arm.Named("myArm")
    myArmComponent, err := arm.FromRobot(robot, "myArm")
    myArmReturnValue, err := myArmComponent.EndPosition(context.Background(), nil)
    if err != nil { 
      fmt.Println(err) 
    }
    fmt.Println("myArm EndPosition return value: %s", myArmReturnValue)
-->
{{% /tab %}}
{{% tab name="Python" %}}
The following lines from the full **Python** tutorial code enable you to use the `myArm` component you configured earlier, and then call the `get_end_position` method to get the position of the **end of the robot arm with respect to the arm's base**.

<!-- Insert code link here to portion of Python sample with ...
    my_arm_resource = Arm.get_resource_name("myArm")
    my_arm_component = Arm.from_robot(robot, "myArm")
    my_arm_return_value = await my_arm_component.get_end_position()
    print(f"myArm get_end_position return value: {my_arm_return_value}")
-->
{{% /tab %}}
{{< /tabs >}}

The state of a robot arm can also be described as the **combined positions of each joint** attached to the arm.
You can access a robot arm's "joint states" (as they are sometimes referred) by calling a different method on the arm component.
The code below can be executed right after you get the end effector pose from the prior code sample; notice the different way in which these two pieces of information are presented.

{{< tabs >}}
{{% tab name="Go" %}}
<!-- Insert code link here to portion of Go sample with ...
    myArmJointPositions, err := myArmComponent.JointPositions(context.Background(), nil)
    if err != nil { 
      fmt.Println(err) 
    }
    fmt.Println("myArm JointPositions return value: %s", myArmJointPositions)
-->
{{% /tab %}}
{{% tab name="Python" %}}
<!-- Insert code link here to portion of Python sample with ...
    my_arm_joint_positions = await my_arm_component.get_joint_positions()
    print(f"myArm get_joint_positions return value: {my_arm_joint_positions}")
-->
{{% /tab %}}
{{< /tabs >}}

Both representations of an arm's state are important.
Sometimes you may wish to direct an arm in terms of joint positions, sometimes you may need to describe the position of another object with respect to the end of the robot arm.
There is a mathematical relationship that allows us to convert between these two representations, known as the **forwards and inverse kinematics**, which is foundational to complex robotic motion.
We will not cover forwards and inverse kinematics in this tutorial, but resources for further reading on these topics are linked in the **Next Steps** section.

## Moving the Arm

Moving a robotic arm with Viam has a very similar feel to retrieving the state of a robotic arm.
The two main options for specifying arm movement are through **joint position commands** and through **pose commands**.
You can use these distinct approaches without adding anything else to your robot.
You can simply use what is already provided through the arm component interface.
Let's start with joint position commands, as their formulation is a little simpler.

### Joint Position Commands

First, you can initiate motion with a joint position command.
You must import an additional Go library to access the data structure that Viam uses to encode joint positions, which is shown next. A final note:

{{< alert title="Caution" color="caution" >}}
Executing code presented after this point WILL induce motion in a connected robotic arm!
{{< /alert >}}

{{< tabs >}}
{{% tab name="Go" %}}
Add `armapi "go.viam.com/api/component/arm/v1"` to your import list, and you will now be able to assign values to an `armapi.JointPositions` data structure.
See the [Arm reference document](https://docs.viam.com/components/arm/#movetojointpositions) for further details on how to structure data being passed to the `MoveToJointPositions` function.

<!-- Insert code link here to portion of Go sample with ...
    cmdJointPositions := &armapi.JointPositions{Values: []float64{0.0, 0.0, 0.0, 0.0, 0.0, 0.1}}
    err = myArmComponent.MoveToJointPositions(ctx, cmdJointPositions, nil)
    if err != nil { 
      fmt.Println(err) 
    }
-->
{{% /tab %}}
{{% tab name="Python" %}}
Add `from viam.proto.component.arm import JointPositions` to your import list, and you will now be able to assign values to a `JointPositions` data structure.
See the [Arm reference document](https://docs.viam.com/components/arm/#movetojointpositions) for further details on how to structure data being passed to the `move_to_joint_positions` function.

<!-- Insert code link here to portion of Python sample with ...
    cmd_joint_positions = JointPositions(values=[0, 0, 0, 0, 0, 0.1])
    await my_arm_component.move_to_joint_positions(positions=cmd_joint_positions)
-->
{{% /tab %}}
{{< /tabs >}}

If you execute the sample joint move statement above, your arm should move the last joint a small amount.
Feel free to experiment further with joint position commands by changing the values for each joint and re-sending the commands.

When ready to move on, this next section will show you how to use **pose commands**.
When you asked the robot for the end position of the arm, this data was returned in the format of a `Pose`.
In this instance, the `Pose` is a combination of position and orientation data that indicates the end of the arm's full 6-dimensional configuration in space.
You can read up more on poses (and their respective formatting styles in each SDK) in other Viam documentation, but this tutorial shows a shorthand method for quickly generating poses for an arm.

### Pose Commands

The code sample below reuses previously demonstrated methods to get the pose of the end of the arm so that you can make small adjustments at will.
You can then pass the adjusted pose back to the arm as a **goal** pose for the purposes of starting motion.
For example, the below code gets the arm's end position, makes a 100 millimeter adjustment in the +Z direction, and then uses that adjustment as a goal when commanding arm motion.

{{< tabs >}}
{{% tab name="Go" %}}
You must import some additional Go packages to synthesize new poses through the `spatialmath` library, and to provide an empty `WorldState` to the arm component's `MoveToPosition` command.
Add `"go.viam.com/rdk/referenceframe"` and `"go.viam.com/rdk/spatialmath"` to your import list and then add the sample code below to your own client script.

<!-- Insert code link here to portion of Go sample with ...
    currentArmPose, err := myArmComponent.EndPosition(context.Background(), nil)
    if err != nil {
      fmt.Println(err)
    }
    adjustedArmPoint := currentArmPose.Point()
    adjustedArmPoint.Z += 100.0
    cmdArmPose := spatialmath.NewPose(adjustedArmPoint, currentArmPose.Orientation())

    err = myArmComponent.MoveToPosition(context.Background(), cmdArmPose, &referenceframe.WorldState{}, nil)
    if err != nil {
      fmt.Println(err)
    }
-->
{{% /tab %}}
{{% tab name="Python" %}}
You must import some additional Python packages to synthesize new poses and to provide an empty `WorldState` to the arm component's `move_to_position` command.
Add `from viam.proto.common import Pose, WorldState` to your import list and add the sample code below to your own client script.

<!-- Insert code link here to portion of Python sample with ...
    # Generate a simple pose move +100mm in the +Z direction of the arm
    cmd_arm_pose = await my_arm_component.get_end_position()
    cmd_arm_pose.z += 100.0
    await arm_component.move_to_position(pose=cmd_arm_pose, world_state=WorldState())
-->
{{% /tab %}}
{{< /tabs >}}

In this way, you can quickly adjust one or more elements of position AND orientation simultaneously, by modifying other elements of the original arm pose.

For all motion actions taken in this tutorial, there may be joint positions or poses that are unreachable for particular reasons (potential collisions, a pose in space is unreachable because the arm is too short). Keep an eye on your client script's feedback and the `viam-server` logs for any issues that may arise.

## Next Steps and References

<!-- TODO: Content below struck out for the moment, saved to point at the next tutorial "Plan Motions with an Arm and with a Gripper" -->
<!-- 
If you would like to continue onto working with Viam's Motion service, go to the next tutorial in this series: "[Plan Motions with an Arm and with a Gripper](/tutorials/motion/plan-motions-with-arm-gripper/)".
-->

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, be sure to head over to the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw).

For more resources on robot kinematics, read through the Wikipedia pages for [Forward kinematics](https://en.wikipedia.org/wiki/Forward_kinematics) and [Inverse kinematics](https://en.wikipedia.org/wiki/Inverse_kinematics).

## Full Tutorial Code

{{< tabs >}}
{{% tab name="Go" %}}

```go {id="access-move-arm-go-ex" class="line-numbers linkable-line-numbers" data-line=""}
package main

import (
  "context"
  "fmt"

  "github.com/edaniels/golog"
  armapi "go.viam.com/api/component/arm/v1"
  "go.viam.com/rdk/components/arm"
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/rdk/spatialmath"
  "go.viam.com/rdk/utils"
  "go.viam.com/utils/rpc"
)

func main() {
  logger := golog.NewDevelopmentLogger("client")
  robot, err := client.New(
      context.Background(),
      "<ROBOT ADDRESS>",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "<ROBOT SECRET PAYLOAD>",
      })),
  )
  if err != nil {
      logger.Fatal(err)
  }
  defer robot.Close(context.Background())

  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // myArm
  myArmResource = arm.Named("myArm")
  myArmComponent, err := arm.FromRobot(robot, "myArm")
  if err != nil { 
    fmt.Println(err) 
  }

  // End Position of myArm
  myArmEndPosition, err := myArmComponent.EndPosition(context.Background(), nil)
  if err != nil { 
    fmt.Println(err) 
  }
  fmt.Println("myArm EndPosition return value: %s", myArmEndPosition)

  // Joint Positions of myArm
  myArmJointPositions, err := myArmComponent.JointPositions(context.Background(), nil)
  if err != nil { 
    fmt.Println(err) 
  }
  fmt.Println("myArm JointPositions return value: %s", myArmJointPositions)

  // Command a joint position move, small adjustment to the last joint
  cmdJointPositions := &armapi.JointPositions{Values: []float64{0.0, 0.0, 0.0, 0.0, 0.0, 0.1}}
  err = myArmComponent.MoveToJointPositions(ctx, cmdJointPositions, nil)
  if err != nil { 
    fmt.Println(err) 
  }

  // Generate a simple pose move +100mm in the +Z direction of the arm
  currentArmPose, err := myArmComponent.EndPosition(context.Background(), nil)
  if err != nil {
    fmt.Println(err)
  }
  adjustedArmPoint := currentArmPose.Point()
  adjustedArmPoint.Z += 100.0
  cmdArmPose := spatialmath.NewPose(adjustedArmPoint, currentArmPose.Orientation())

  err = myArmComponent.MoveToPosition(context.Background(), cmdArmPose, &referenceframe.WorldState{}, nil)
  if err != nil {
    fmt.Println(err)
  }
}
```

{{% /tab %}}
{{% tab name="Python" %}}

```python {id="access-move-arm-python-ex" class="line-numbers linkable-line-numbers" data-line=""}
import asyncio

from viam.components.arm import Arm
from viam.proto.common import WorldState
from viam.proto.component.arm import JointPositions
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions


async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='<ROBOT SECRET PAYLOAD>')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('<ROBOT ADDRESS>', opts)

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)
    
    # myArm
    my_arm_resource = Arm.get_resource_name("myArm")
    my_arm_component = Arm.from_robot(robot, "myArm")

    # End Position of myArm
    my_arm_end_position = await my_arm_component.get_end_position()
    print(f"myArm get_end_position return value: {my_arm_end_position}")

    # Joint Positions of myArm
    my_arm_joint_positions = await my_arm_component.get_joint_positions()
    print(f"myArm get_joint_positions return value: {my_arm_joint_positions}")

    # Command a joint position move, small adjustment to the last joint
    cmd_joint_positions = JointPositions(values=[0, 0, 0, 0, 0, 0.1])
    await my_arm_component.move_to_joint_positions(positions=cmd_joint_positions)

    # Generate a simple pose move +100mm in the +Z direction of the arm
    cmd_arm_pose = await my_arm_component.get_end_position()
    cmd_arm_pose.z += 100.0
    await arm_component.move_to_position(pose=cmd_arm_pose, world_state=WorldState())

    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{< /tabs >}}
