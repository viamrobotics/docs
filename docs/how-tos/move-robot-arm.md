---
title: "Access and move a robot arm"
linkTitle: "Move a robot arm"
weight: 70
type: "docs"
tags: ["data management", "data", "services"]
images: ["/tutorials/motion/preview.jpg"]
description: "Access and control one of the most fundamental systems in robotics: A robotic arm."
aliases:
  - /tutorials/motion/accessing-and-moving-robot-arm
  - /tutorials/motion/
languages: []
viamresources: []
platformarea: ["mobility"]
level: "Intermediate"
date: "2024-10-31"
# updated: ""  # When the tutorial was last entirely checked
cost: "8400"
---

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/motion/access_01_xarm6.png" resize="500x" declaredimensions=true alt="A picture of the UFACTORY xArm 6." style="width: 150px" >}}
</div>

If you have a robot arm, you can use Viam to access data about the arm and program it to move.
After configuring your machine, you can use the Python or Go SDKs to access data about the state of the arm and the end effector pose and issue movement commands.

{{< alert title="In this page" color="tip" >}}

1. [Access the arm](#access-the-arm)
1. [Move the arm](#move-the-arm)

{{< /alert >}}

{{< alert title="Caution" color="caution" >}}
Be careful when instructing robot arms to move.
Before running any code, ensure your robotic arm has enough space and that there are no obstacles.
Also pay attention to your surroundings, double-check your code for correctness, and make sure anyone nearby is aware and alert before issuing commands to your machine.
{{< /alert >}}

## Access the arm

{{< table >}}
{{% tablestep link="/configure/" %}}
**1. Configure a machine with an arm**

{{% snippet "setup.md" %}}

[Configure an arm](/components/arm/#configuration).

{{<imgproc src="/how-tos/access-arm/config.png" resize="500x" class="fill aligncenter" style="width: 400px" declaredimensions=true alt="Configuration builder UI with a blank arm component">}}

Refer to the [documentation for the model](/components/arm/#configuration) for information about your arm's configuration attributes.

Save your config.

{{< alert title="Tip" color="tip" >}}
If you do not have a robotic arm of your own, configure a [`fake` arm](/components/arm/fake/) with `"arm-model": "xArm6"` in its `attributes`.
{{< /alert >}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Get a code sample**

Go to the **Code sample** page of the **CONNECT** tab and select either Python or Go.

{{% snippet "show-secret.md" %}}

{{<imgproc src="/how-tos/access-arm/code-sample.png" resize="700x" class="fill aligncenter" style="width: 400px" declaredimensions=true alt="Code sample page of the CONNECT tab">}}

Then, copy and paste the sample code into a file and run the resulting script to verify you can connect to your machine.

{{% /tablestep %}}
{{% tablestep link="/fleet/fragments/" %}}
**3. Get the position of the end effector**

One way to describe the state of a robot arm is with the position of the end effector, or the "tool" or "hand" of the arm.
To access this information, add the following lines of code to your script:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# End Position of myArm
my_arm_return_value = await my_arm.get_end_position()
print(f"myArm get_end_position return value: {my_arm_return_value}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// End Position of myArm
myArmReturnValue, err:= myArmComponent.EndPosition(context.Background(), map[string]interface{}{})
if err!=nil {
  logger.Error(err)
  return
}
logger.Infof("myArm EndPosition return value: %+v", myArmReturnValue)
```

{{% /tab %}}
{{< /tabs >}}

Run your script again to see the position of the end effector output as a [`Pose`](/internals/orientation-vector/).
For more information, see [`GetEndPosition`](/appendix/apis/components/arm/#getendposition).

{{% /tablestep %}}
{{% tablestep %}}
<!-- {{<imgproc src="/how-tos/one-to-many/delete.png" class="fill alignleft" resize="500x" style="width: 200px" declaredimensions=true alt="Delete">}} -->

**4. Get the joint positions**

The state of a robot arm can also be described as the **combined positions of each joint** attached to the arm.
To get that information, add the following code right after the code that gets the end effector pose from the prior code sample:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Joint Positions of myArm
my_arm_joint_positions = await my_arm.get_joint_positions()
print(f"myArm get_joint_positions return value: {my_arm_joint_positions}")
```

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

{{% /tab %}}
{{< /tabs >}}

Run your code again.
Each individual value corresponds to the current position of a particular joint on your robot.
You can also see these values reflected on the **CONTROL** tab in the Viam app for your robot arm.

{{% /tablestep %}}
{{< /table >}}

## Move the arm

The two main options for specifying arm movement are through **joint position commands** and through **pose commands**.

{{< table >}}
{{% tablestep %}}
**1. Initiate motion with a joint position command**

Add the following code to your existing script:

{{< tabs >}}
{{% tab name="Python" %}}
Add the following line to your import list to be able to assign values to a `JointPositions` data structure:

```python {class="line-numbers linkable-line-numbers"}
from viam.proto.component.arm import JointPositions
```

```python {class="line-numbers linkable-line-numbers"}
# Command a joint position move: move the forearm of the arm slightly up
cmd_joint_positions = JointPositions(values=[0, 0, -30.0, 0, 0, 0])
await my_arm.move_to_joint_positions(positions=cmd_joint_positions)
```

{{% /tab %}}
{{% tab name="Go" %}}
You must import an additional Go library to access the data structure that Viam uses to encode joint positions, which is shown next.

Add `armapi "go.viam.com/api/component/arm/v1"` to your import list to be able to assign values to an `armapi.JointPositions` data structure.

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

Run the code.
The third joint of your arm should move a small amount (30 degrees).
For more information, see [`MoveToJointPositions`](/appendix/apis/components/arm/#movetojointpositions).

{{% /tablestep %}}
{{% tablestep %}}
{{<imgproc src="/how-tos/one-to-many/repeat.svg" class="fill alignleft" style="width: 120px"  declaredimensions=true alt="Repeat">}}
**2. Repeat for each machine**

Repeat step 1 for each of the machines that you want to configure in the same way.

If some of your machines have slight differences, you can still add the fragment and then add fragment overwrites in the next section.

{{% /tablestep %}}
{{< /table >}}

## Next steps

If you would like to continue onto working with Viam's motion service, check out one of these tutorials:

{{< cards >}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper" %}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{< /cards >}}

{{< snippet "social.md" >}}

For more resources on robot kinematics, read through the Wikipedia pages for [Forward kinematics](https://en.wikipedia.org/wiki/Forward_kinematics) and [Inverse kinematics](https://en.wikipedia.org/wiki/Inverse_kinematics).
