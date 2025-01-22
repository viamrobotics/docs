---
linkTitle: "Move an arm"
title: "Move an arm"
weight: 50
layout: "docs"
type: "docs"
description: "Move an arm with joint positions or automated motion planning."
aliases:
  - /how-tos/move-robot-arm/
  - /tutorials/motion/accessing-and-moving-robot-arm/
  - /tutorials/motion/
---

You have two options for moving a robotic [arm](/operate/reference/components/arm/):

- Use direct joint position commands and simple linear commands with the [arm API](/dev/reference/apis/components/arm/)
- Use automated complex motion planning with the [motion planning service API](/dev/reference/apis/services/motion/)

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

## Configure and connect to your arm

{{< table >}}
{{% tablestep link="/operate/get-started/supported-hardware/" %}}
**1. Configure an arm component**

First, physically connect the arm to your machine.

Then, navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Search for and select a model that supports your arm.

Complete the arm configuration, then use the **TEST** panel in the configuration card to test that the arm is working.

{{% /tablestep %}}
{{% tablestep link="/operate/control/headless-app/" %}}
**2. Connect code to your arm**

Go to your machine's **CONNECT** tab in the Viam app.
Select your preferred programming language and copy the code snippet.

See [Create a web app](/operate/control/web-app/), [Create a mobile app](/operate/control/mobile-app/), or [Create a headless app](/operate/control/headless-app/) for more information, depending on your use case.

{{% /tablestep %}}
{{< /table >}}

## Move the arm using the arm API

The two main options for controlling arm movement with the arm API are through **joint position commands** and through **pose commands**.
Joint position commands allow for more detailed control and flexibility instead of commanding movement with the end effector position in a pose command.

{{< alert title="Caution" color="caution" >}}
Be careful when instructing robot arms to move.
Before running any code, ensure your robotic arm has enough space and that there are no obstacles.
Also pay attention to your surroundings, double-check your code for correctness, and make sure anyone nearby is aware and alert before issuing commands to your machine.
{{< /alert >}}

{{< table >}}
{{% tablestep %}}
**1. Initiate motion with a joint position command**

{{< tabs >}}
{{% tab name="Python" %}}
Add the following line to your import list to be able to assign values to a `JointPositions` data structure:

```python
from viam.proto.component.arm import JointPositions
```

Add the following code to your script:

```python
# Command a joint position move: move the forearm of the arm slightly up
cmd_joint_positions = JointPositions(values=[0, 0, -30.0, 0, 0, 0])
await arm_1.move_to_joint_positions(positions=cmd_joint_positions)
```

{{% /tab %}}
{{% tab name="Go" link="/dev/reference/apis/components/arm/#movetojointpositions" %}}
Add `armapi "go.viam.com/api/component/arm/v1"` to your import list.
Add the following code to your script:

```go
// Command a joint position move: move the forearm of the arm slightly up
cmdJointPositions := &armapi.JointPositions{Values: []float64{0.0, 0.0, -30.0, 0.0, 0.0, 0.0}}
err = arm1.MoveToJointPositions(context.Background(), cmdJointPositions, nil)
if err != nil {
    logger.Error(err)
    return
}
```

{{% /tab %}}
{{< /tabs >}}

{{<gif webm_src="/how-tos/joint_positions.webm" mp4_src="/how-tos/joint_positions.mp4" alt="The robot arm moving through joint position commands" max-width="200px" class="alignleft">}}

Run the code.
The third joint of your arm should move 30 degrees.
For more information, see [`MoveToJointPositions`](/dev/reference/apis/components/arm/#movetojointpositions).

{{% /tablestep %}}
{{% tablestep link="/dev/reference/apis/components/arm/#movetoposition" %}}
**2. Command to move to position**

{{< tabs >}}
{{% tab name="Python" %}}

Add the following code to your script:

```python
# Generate a simple pose move +100mm in the +Z direction of the arm
cmd_arm_pose = await arm_1.get_end_position()
cmd_arm_pose.z += 100.0
await arm_1.move_to_position(pose=cmd_arm_pose)
```

{{% /tab %}}
{{% tab name="Go" %}}
Add `"go.viam.com/rdk/spatialmath"` to your import list.

Add the following code to your script:

```go
// Generate a simple pose move +100mm in the +Z direction of the arm
currentArmPose, err := arm1.EndPosition(context.Background(), nil)
if err != nil {
  logger.Error(err)
  return
}
adjustedArmPoint := currentArmPose.Point()
adjustedArmPoint.Z += 100.0
cmdArmPose := spatialmath.NewPose(adjustedArmPoint, currentArmPose.Orientation())

err = arm1.MoveToPosition(context.Background(), cmdArmPose, nil)
if err != nil {
  logger.Error(err)
  return
}
```

{{% /tab %}}
{{< /tabs >}}

{{<gif webm_src="/how-tos/move_to_position.webm" mp4_src="/how-tos/move_to_position.mp4" alt="A robot arm moving to a commanded position" max-width="200px" class="alignright">}}

This code gets the arm's end position, makes a 100 millimeter adjustment in the +Z direction, and then uses that adjustment as a goal [`Pose`](/operate/reference/orientation-vector/) when commanding arm motion.
Run the code to see your arm move 100 mm upwards.
For more information, see [`MoveToPosition`](/dev/reference/apis/components/arm/#movetoposition).

{{% /tablestep %}}
{{< /table >}}

## Use automated complex motion planning

The following tutorials demonstrate how to plan complex motion with a robot arm:

{{< cards >}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper/" %}}
{{% card link="/tutorials/services/constrain-motion/" %}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{< /cards >}}
