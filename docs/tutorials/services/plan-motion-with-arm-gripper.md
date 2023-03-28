---
title: "Plan Motion with an Arm and a Gripper"
linkTitle: "Plan Motion with an Arm"
weight: 20
type: "docs"
description: "Use the Motion Service to move robot arms and other components."
tags: ["arm", "gripper", "motion"]
# SMEs: William S.
---

{{< alert title="Caution" color="caution" >}}
Be careful when instructing robot arms to move.
Before running any code, ensure your robotic arm has enough space and that there are no obstacles.
Also pay attention to your surroundings, double-check your code for correctness, and make sure anyone nearby is aware and alert before issuing commands to your robot.
{{< /alert >}}

Moving individual components is a good way to start using Viam, but there is so much more you can do.
The [Motion Service](/services/motion/) enables sophisticated movements involving one or many components of your robot.
The Motion Service is one of the "built-in" services, which means that no initial configuration is required to start planning and executing complex motion.
All you need is a robot with a component that can move, such as a robotic arm.

{{< alert title="Note" color="note" >}}
Code examples in this tutorial use a [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6), but you can use any [arm model](/components/arm/).
{{< /alert >}}

## Prerequisites

Before starting this tutorial, make sure you have the [Viam Python SDK](https://python.viam.dev/) or the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme) installed.

If you are connecting to a real robotic arm during this tutorial, make sure your computer can communicate with the controller before continuing.

Make sure you have mastery of the concepts outlined in the first Motion tutorial, [Access and Move a Robot Arm](/tutorials/motion/accessing-and-moving-robot-arm), before continuing.
This tutorial picks up right where **Access and Move a Robot Arm** stops, so further examples depend on having a connected robot, client and service access, and other infrastructure in place.
This also helps simplify and shorten the code examples presented below.

For a helpful recap of the code we previously added, look at [the full code sample from the prior tutorial](/tutorials/motion/accessing-and-moving-robot-arm#full-tutorial-code).

## Configure a robot

The [robot configuration from the prior tutorial](/tutorials/motion/accessing-and-moving-robot-arm/#configure-a-robot) should be used for this tutorial.
We will revisit that robot configuration and add new components during specific sections below.

## Accessing the Motion Service

Accessing the Motion Service is very similar to accessing any other component or service within the Viam ecosystem.

{{< tabs >}}
{{% tab name="Python" %}}

<!-- TODO: Add Python -->
```python {class="line-numbers linkable-line-numbers"}
```

{{% /tab %}}
{{% tab name="Go" %}}
You must import an additional Go package to access the Motion service.
Add `"go.viam.com/rdk/services/motion"` to your import list and then add the sample code below to your own client script.

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")
if err != nil {
  logger.Fatal(err)
}
```
{{% /tab %}}
{{< /tabs >}}

Once the Motion Service can be accessed, some familiar features become available.
The Motion service has a method that can get the Pose of a component relative to a **reference frame**.
In the tutorial where we interacted with an arm component, we used the `EndPosition` method to determine the pose of the end effector of `myArm`.
The `GetPose` method provided by the Motion Service serves a similar function to `EndPosition`, but allows for querying of pose data with respect to other elements of the robot (such as another component or the robot's fixed "world" frame).

{{< tabs >}}
{{% tab name="Python" %}}

<!-- TODO: Add Python -->
```python {class="line-numbers linkable-line-numbers"}
```

{{% /tab %}}
{{% tab name="Go" %}}
Note the use of `referenceframe.World` in the following code example.
This is a constant string value in the RDK's `referenceframe` library that is maintained for user and programmer convenience.

```go {class="line-numbers linkable-line-numbers"}
myArmMotionPose, err = motionService.GetPose(context.Background(), myArmResource, referenceframe.World, nil, nil)
if err != nil {
  fmt.Println(err)
}
fmt.Println("GetPose result for myArm position:", myArmMotionPose.Point())  // TODO: Correct?
fmt.Println("GetPose result for myArm orientation:", myArmMotionPose.Orientation())  // TODO: Correct?
```
{{% /tab %}}
{{< /tabs >}}

In this example, we are asking the Motion Service where the end of `myArm` is with respect to the root "world" reference frame.

## Describing the robot's working environment

Now that the Motion service has been properly introduced, a small detour is warranted.
The world around a robot may be full of objects that you may wish to prevent your robot from running into when commanding it to move.
There could be many reasons for this: you are sitting near your robot, there are things in the environment you want the robot to avoid, or you have mounted your robot to a fixed object, such as a table.

You can pass additional information about the environment to various parts of the Viam system through a particular data structure, aptly named `WorldState`.
The code samples below detail how to add geometry to the WorldState to indicate the presence of other objects in your robot's working environment.

{{< tabs >}}
{{% tab name="Python" %}}

<!-- TODO: Add Python -->
```python {class="line-numbers linkable-line-numbers"}
```

{{% /tab %}}
{{% tab name="Go" %}}
The `WorldState` is available through the `referenceframe` library, but additional geometry data must be added in a piecewise fashion.

```go {class="line-numbers linkable-line-numbers"}
// Add a table obstacle to a WorldState
obstacles := make([]spatialmath.Geometry, 0)

tableOrigin := spatialmath.NewPose(
  r3.Vector{X: 0.0, Y: 0.0, Z: -10.0},
  &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
)
tableDims := r3.Vector{X: 2000.0, Y: 2000.0, Z: 20.0}
tableObj, _ := spatialmath.NewBox(tableOrigin, tableDims, "table")
obstacles = append(obstacles, tableObj)

// Create a WorldState that has the GeometriesInFrame included
obstaclesInFrame := referenceframe.NewGeometriesInFrame(referenceframe.World, obstacles)
worldState := &referenceframe.WorldState{
  Obstacles: []*referenceframe.GeometriesInFrame{obstaclesInFrame},
}
```
{{% /tab %}}
{{< /tabs >}}

This example adds a "table" with the assumption that you mounted your robot arm to an elevated surface.
The 2000 millimeter by 2000 millimeter dimensions ensure that a sufficiently large box is considered, regardless of the real physical footprint of your mounting surface.
Feel free to change these dimensions, including thickness (the Z coordinate in the above code samples), to match your environment more closely.
Additional obstacles can also be *appended* as desired.

{{< alert title="Tip" color="note" >}}
Within the App, the **Frame System** tab in the **Config** section of your robot gives you the ability to experiment with various geometry representations with better visual feedback.
{{< /alert >}}

<!-- TODO : Add a picture example of a geometry specified through the Frame System tab -->

## Commanding an arm to move with the Motion Service

Commanding motion with the Motion Service has a more general feel than previous examples that were commanding motion for individual components.
In previous examples you controlled motion of individual components.
Now you will use the Motion Service to control the motion of the robot as a whole.
You will use the Motion Service's `Move` method to execute more general robotic motion.
You can designate specific components for motion planning by passing in the resource name (note the use of the arm resource in the code samples below).
The `worldState` we constructed earlier is also passed in so that the Motion Service can consider additional information when planning.

The sample pose given below can be adjusted to fit your specific circumstances.
Remember that X, Y, and Z coordinates are specified in millimeters.

Again, a note:

{{< alert title="Caution" color="caution" >}}
Executing code presented after this point *will* induce motion in a connected robotic arm!
Keep the space around the arm clear!
Keep the space around the arm clear!
{{< /alert >}}
<br><br>
{{< tabs >}}
{{% tab name="Python" %}}

<!-- TODO: Add Python -->
```python {class="line-numbers linkable-line-numbers"}
```

{{% /tab %}}
{{% tab name="Go" %}}
Because of ongoing experimental API changes, we must pass in a `slam` service resource name when using the Motion service to `Move`.
Add `"go.viam.com/rdk/services/slam"` to your import list to provide access to the `slam` service.
This tutorial will not cover any other SLAM content.

```go {class="line-numbers linkable-line-numbers"}
// Generate a sample "start" pose to demonstrate motion
testStartPose := spatialmath.NewPose(
  r3.Vector{X: 510.0, Y: 0.0, Z: 526.0},
  &spatialmath.OrientationVectorDegrees{OX: 0.7071, OY: 0.0, OZ: -0.7071, Theta: 0.0},
)
testStartPoseInFrame := referenceframe.NewPoseInFrame(referenceframe.World, testStartPose)
_, err = motionService.Move(context.Background(), myArmResource, testStartPoseInFrame, worldState, nil, slam.Named(""), nil)
if err != nil {
  logger.Fatal(err)
}
```
{{% /tab %}}
{{< /tabs >}}

<!-- TODO : In the future, we should add some specific information on the importance of the frame chosen as the point of reference for PoseInFrame variables -->
<!-- ## Managing Pose References -->

## Commanding other components to move with the Motion Service

This section will require you to add a new component to your robot.
One device that is very commonly attached to the end of a robot arm is a **gripper**.
Most robot arms pick up and manipulate objects in the world through the use of a gripper, so learning how to directly command a gripper to move is highly valuable.
Though various Motion Service commands cause the gripper to move, ultimately the arm is doing all of the work in these situations.
This is possible because the Motion Service considers other parts of the robot (through the [Frame System](/services/frame-system/) when calculating how to achieve the desired motion.

### Add a gripper component

We need to do several things to prepare a new gripper component for motion.

1. Go back to your robot configuration in the Viam app.
2. Under the **COMPONENTS** section, add a new `gripper` component to your robot with the following attributes:

* Set `myGripper` as the **Name** of this new component
* Set the **Type** to `gripper`
* Set the **Model** to `fake`

3. Add a **Frame** to this component

* Set the parent as `myArm`
* Set the translation as something small in the +Z direction, such as 90 mm
* Leave the orientation as the default
* For **Geometry Type** choose **Box**
* Enter desired values for the box's **Length**, **Width**, and **Height**, and the box origin's **X**, **Y**, and **Z** values.

4. Include the `myArm` component in the **Depends On** drop-down for `myGripper`
5. Save this new robot configuration
  * Your `viam-server` instance should update automatically.

<!-- TODO : Add a picture of a sample gripper configuration -->

Because the new gripper component is "attached" (with the parent specification in the Frame) to `myArm`, we can produce motion plans using `myGripper` instead of `myArm` 

{{< tabs >}}
{{% tab name="Python" %}}

<!-- TODO: Add Python -->
```python {class="line-numbers linkable-line-numbers"}
```

{{% /tab %}}
{{% tab name="Go" %}}
The last library you must import is the `gripper` library.
Do this by adding the `"go.viam.com/rdk/components/gripper"` library to your import list.

```go {class="line-numbers linkable-line-numbers"}
gripperName := "myGripper"
gripperResource := gripper.Named(gripperName)

// This will move the gripper in the -Z direction with respect to its own reference frame
gripperPoseRev := spatialmath.NewPose(
  r3.Vector{X: 0.0, Y: 0.0, Z: -100.0},
  &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
)
gripperPoseRevInFrame := referenceframe.NewPoseInFrame(gripperName, gripperPoseRev) // Note the change in frame name

_, err = motionService.Move(context.Background(), gripperResource, gripperPoseRevInFrame, worldState, nil, slam.Named(""), nil)
if err != nil {
  logger.Fatal(err)
}
```
{{% /tab %}}
{{< /tabs >}}

For the gripper pose, you could change the reference frame information to consider other frames as the point of reference.
This has implications for how motion is calculated, what magnitude and direction is considered, and what future motions might have to consider.

## Next Steps and References

<!-- TODO: Content below struck out for the moment, saved to point at the next tutorial "Plan Motion with an Arm and with a Gripper" -->
<!--
If you would like to continue onto specific complex motion constraints, go to the next tutorial in this series: "[Put Constraints on a Motion Plan](/tutorials/motion/plan-motion-with-arm-gripper/)".
-->

{{< snippet "social.md" >}}

<!-- TODO : Add more content here -->

## Full Tutorial Code

{{< tabs >}}
{{% tab name="Python" %}}

<!-- TODO: Add Python -->
```python {id="plan-motion-python-ex" class="line-numbers linkable-line-numbers" data-line=""}

```

{{% /tab %}}
{{% tab name="Go" %}}

```go {id="plan-motion-go-ex" class="line-numbers linkable-line-numbers" data-line=""}
package main

import (
  "context"
  "fmt"

  "github.com/edaniels/golog"
  armapi "go.viam.com/api/component/arm/v1"
  "go.viam.com/rdk/components/arm"
  "go.viam.com/rdk/components/gripper"
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/rdk/services/motion"
  "go.viam.com/rdk/services/slam"
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

  // Access myArm
  myArmResource := arm.Named("myArm")
  fmt.Println("myArmResource:", myArmResource)
  myArmComponent, err := arm.FromRobot(robot, "myArm")
  if err != nil {
    fmt.Println(err)
  }

  // End Position of myArm
  myArmEndPosition, err := myArmComponent.EndPosition(context.Background(), nil)
  if err != nil {
    fmt.Println(err)
  }
  fmt.Println("myArm EndPosition position value:", myArmEndPosition.Point())
  fmt.Println("myArm EndPosition orientation value:", myArmEndPosition.Orientation())

  // Joint Positions of myArm
  myArmJointPositions, err := myArmComponent.JointPositions(context.Background(), nil)
  if err != nil {
    fmt.Println(err)
  }
  fmt.Println("myArm JointPositions return value:", myArmJointPositions)

  // Command a joint position move: small adjustment to the last joint
  cmdJointPositions := &armapi.JointPositions{Values: []float64{0.0, 0.0, 0.0, 0.0, 0.0, 15.0}}
  err = myArmComponent.MoveToJointPositions(context.Background(), cmdJointPositions, nil)
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

  motionService, err := motion.FromRobot(robot, "builtin")
  if err != nil {
    logger.Fatal(err)
  }

  // Add a table obstacle to a WorldState
  obstacles := make([]spatialmath.Geometry, 0)

  tableOrigin := spatialmath.NewPose(
    r3.Vector{X: 0.0, Y: 0.0, Z: -10.0},
    &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
  )
  tableDims := r3.Vector{X: 2000.0, Y: 2000.0, Z: 20.0}
  tableObj, _ := spatialmath.NewBox(tableOrigin, tableDims, "table")
  obstacles = append(obstacles, tableObj)

  // Create a WorldState that has the GeometriesInFrame included
  obstaclesInFrame := referenceframe.NewGeometriesInFrame(referenceframe.World, obstacles)
  worldState := &referenceframe.WorldState{
    Obstacles: []*referenceframe.GeometriesInFrame{obstaclesInFrame},
  }

  myArmMotionPose, err = motionService.GetPose(context.Background(), myArmResource, referenceframe.World, nil, nil)
  if err != nil {
    fmt.Println(err)
  }
  fmt.Println("GetPose result for myArm position:", myArmMotionPose.Point())
  fmt.Println("GetPose result for myArm orientation:", myArmMotionPose.Orientation())

  // Generate a sample "start" pose to demonstrate motion
  testStartPose := spatialmath.NewPose(
    r3.Vector{X: 510.0, Y: 0.0, Z: 526.0},
    &spatialmath.OrientationVectorDegrees{OX: 0.7071, OY: 0.0, OZ: -0.7071, Theta: 0.0},
  )
  testStartPoseInFrame := referenceframe.NewPoseInFrame(referenceframe.World, testStartPose)
  _, err = motionService.Move(context.Background(), myArmResource, testStartPoseInFrame, worldState, nil, slam.Named(""), nil)
  if err != nil {
    logger.Fatal(err)
  }

	gripperName := "myGripper"
	gripperResource := gripper.Named(gripperName)

	// This will move the gripper in the -Z direction with respect to its own reference frame
	gripperPoseRev := spatialmath.NewPose(
		r3.Vector{X: 0.0, Y: 0.0, Z: -100.0},
		&spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
	)
	gripperPoseRevInFrame := referenceframe.NewPoseInFrame(gripperName, gripperPoseRev) // Note the change in frame name

	_, err = motionService.Move(context.Background(), gripperResource, gripperPoseRevInFrame, worldState, nil, slam.Named(""), nil)
	if err != nil {
		logger.Fatal(err)
	}
}
```

{{% /tab %}}
{{< /tabs >}}
