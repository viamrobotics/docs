---
title: "Plan Motion with an Arm and a Gripper"
linkTitle: "Plan Motion with an Arm"
type: "docs"
description: "Use the motion service to move robot arms and other components."
videos:
  [
    "/tutorials/videos/motion_armmoving.webm",
    "/tutorials/videos/motion_armmoving.mp4",
  ]
videoAlt: "An arm moving with the motion service"
tags: ["arm", "gripper", "motion", "services"]
authors: []
languages: ["python", "go"]
viamresources: ["arm", "gripper", "motion", "frame_system"]
level: "Intermediate"
date: "2023-03-07"
# updated: ""
cost: 8400
no_list: true
---

With Viam you can move individual components, like [an arm](../accessing-and-moving-robot-arm/) by issuing command like `MoveToPosition()` or `MoveToJointPosition`.
The [motion service](/mobility/motion/) enables you to do much more sophisticated movement involving one or many components of your robot.
The service abstracts the lower level commands away so that you can call the `Move()` command with the desired destination position in a frame, alongside any obstacles and geometries attached to your machine, and the service will move your machine to the desired location for you.

{{< alert title="Learning Goals" color="info" >}}
After following this tutorial, you will be able to:

- provide a representation of objects in the world to Viam
- use the motion service to move machines or components of your machine

{{< /alert >}}

Code examples in this tutorial use a [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6), but you can use any [arm model](/components/arm/).

The [full tutorial code](#full-tutorial-code) is available at the end of this page.

{{< alert title="Caution" color="caution" >}}
Be careful when instructing robot arms to move.
Before running any code, ensure your robotic arm has enough space and that there are no obstacles.
Also pay attention to your surroundings, double-check your code for correctness, and make sure anyone nearby is aware and alert before issuing commands to your robot.
{{< /alert >}}

## Prerequisites

Before starting this tutorial, make sure you have the [Viam Python SDK](https://python.viam.dev/) or the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme) installed.

If you are connecting to a real robotic arm during this tutorial, make sure your computer can communicate with the controller before continuing.

Make sure you have mastery of the concepts outlined in the first motion tutorial, [Access and Move a Robot Arm](../accessing-and-moving-robot-arm/), before continuing.
This tutorial picks up right where **Access and Move a Robot Arm** stops, so further examples depend on having a connected robot, client and service access, and other infrastructure in place.
This also helps simplify and shorten the code examples presented below.

For a helpful recap of the code we previously added, look at [the full code sample from the prior tutorial](../accessing-and-moving-robot-arm/#full-tutorial-code).

## Configure a robot

The [robot configuration from the prior tutorial](../accessing-and-moving-robot-arm/#configure-a-machine) should be used for this tutorial.
We will revisit that robot configuration and add new components during specific sections below.

The motion service is one of the "built-in" services, which means that no initial configuration is required to start planning and executing complex motion.
All you need is a robot with a component that can move, such as a robotic arm.

## Access the motion service

Accessing the motion service is very similar to accessing any other component or service within the Viam ecosystem.

{{< tabs >}}
{{% tab name="Python" %}}
You must import an additional Python library to access the motion service.
Add the following line to your import list:

```python
from viam.services.motion import MotionClient
```

Then add the sample code below to your client script:

```python
# Access the motion service
motion_service = MotionClient.from_robot(robot, "builtin")
```

{{% /tab %}}
{{% tab name="Go" %}}
You must import an additional Go package to access the motion service.
Add the following line to your import list:

```go
"go.viam.com/rdk/services/motion"
```

Then add the sample code below to your client script:

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")
if err != nil {
  logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

The Motion service has a method that can get the _pose_ of a component relative to a [_reference frame_](/mobility/frame-system/).
In the tutorial where we interacted with an arm component, we used the `GetEndPosition` method to determine the pose of the end effector of `myArm`.
The `GetPose` method provided by the motion service serves a similar function to `GetEndPosition`, but allows for querying of pose data with respect to other elements of the robot (such as another component or the robot's fixed "world" frame).

### Get the `ResourceName`

When you use the [arm API](/components/arm/#api), you call methods on your arm component itself.
To use the [motion service API](/mobility/motion/#api) with an arm, you need to pass an argument of type `ResourceName` to the motion service method.

Add the following to the section of your code where you access the arm:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
my_arm_resource_name = Arm.get_resource_name("myArm")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
myArmResourceName := arm.Named("myArm")
```

{{% /tab %}}
{{< /tabs >}}

Now you are ready to run a motion service method on your arm.

{{< tabs >}}
{{% tab name="Python" %}}
Note the use of a hardcoded literal "world" in the following code example.
Any components that have frame information (and, as a result, are added to the frame system) are connected to the "world".

```python {class="line-numbers linkable-line-numbers"}
# Get the pose of myArm from the motion service
my_arm_motion_pose = await motion_service.get_pose(my_arm_resource_name,
                                                   "world")
print(f"Pose of myArm from the motion service: {my_arm_motion_pose}")
```

{{% /tab %}}
{{% tab name="Go" %}}
Note the use of `referenceframe.World` in the following code example.
This is a constant string value in the RDK's `referenceframe` library that is maintained for user and programmer convenience.
Any components that have frame information (and, as a result, are added to the frame system) are connected to the "world".

```go {class="line-numbers linkable-line-numbers"}
// Get the pose of myArm from the motion service
myArmMotionPose, err := motionService.GetPose(context.Background(), myArmResourceName, referenceframe.World, nil, nil)
if err != nil {
  fmt.Println(err)
}
fmt.Println("Position of myArm from the motion service:", myArmMotionPose.Pose().Point())
fmt.Println("Orientation of myArm from the motion service:", myArmMotionPose.Pose().Orientation())
```

{{% /tab %}}
{{< /tabs >}}

In this example, we are asking the motion service where the end of `myArm` is with respect to the root "world" reference frame.

## Describe the robot's working environment

The motion service can also use information you provide about the environment around a robot.
The world around a robot may be full of objects that you may wish to prevent your robot from running into when it moves.
There could be many reasons for this: there are places or things in the environment you want the robot to avoid, or you may have mounted your robot to a fixed object, such as a table.

You can pass additional information about the environment to various parts of the Viam system through a particular data structure, aptly named `WorldState`.
The code samples below detail how to add geometry to the WorldState to indicate the presence of other objects in your robot's working environment.

{{< tabs >}}
{{% tab name="Python" %}}
The `WorldState` is available through the `viam.proto.common` library, but additional geometry data must be added in a piecewise fashion.
You must add additional imports to access `Pose`, `PoseInFrame`, `Vector3`, `Geometry`, `GeometriesInFrame`, and `RectangularPrism` from the proto `common` library.

```python {class="line-numbers linkable-line-numbers"}
# Add a table obstacle to a WorldState
table_origin = Pose(x=0.0, y=0.0, z=-19.0)
table_dims = Vector3(x=2000.0, y=2000.0, z=38.0)
table_object = Geometry(center=table_origin,
                        box=RectangularPrism(dims_mm=table_dims))

obstacles_in_frame = GeometriesInFrame(reference_frame="world",
                                       geometries=[table_object])

# Create a WorldState that has the GeometriesInFrame included
world_state = WorldState(obstacles=[obstacles_in_frame])
```

{{% /tab %}}
{{% tab name="Go" %}}
You must import the r3 package to be able to add an `r3.Vector`, so add `"github.com/golang/geo/r3"` to your import list.
The `WorldState` is available through the `referenceframe` library, but additional geometry data must be added in a piecewise fashion.

```go {class="line-numbers linkable-line-numbers"}
// Add a table obstacle to a WorldState
obstacles := make([]spatialmath.Geometry, 0)

tableOrigin := spatialmath.NewPose(
  r3.Vector{X: 0.0, Y: 0.0, Z: -19.0},
  &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
)
tableDims := r3.Vector{X: 2000.0, Y: 2000.0, Z: 38.0}
tableObj, err := spatialmath.NewBox(tableOrigin, tableDims, "table")
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
The 2000 millimeter by 2000 millimeter dimensions ensure that a sufficiently large box is constructed, regardless of the real physical footprint of your mounting surface.
Setting the Z component of the origin to -19 mm (half the table's thickness) conveniently positions the top surface of the table at 0.
Feel free to change these dimensions, including thickness (the Z coordinate in the above code samples), to match your environment more closely.
Additional obstacles can also be _appended_ as desired.

{{< alert title="Tip" color="note" >}}
Within the app, the **Frame System** subtab of your machine's **Config** tab gives you the ability to experiment with various geometry representations with better visual feedback.
{{< /alert >}}

<div class="td-max-width-on-larger-screens">
  {{<imgproc src="/tutorials/motion/plan_01_frame_system_tab.png" resize="900x" declaredimensions=true alt="A picture of the frame system tab in use.">}}
</div>

## Command an arm to move with the motion service

In previous examples you controlled motion of individual components.
Now you will use the motion service to control the motion of the robot as a whole.
You will use the motion service's [`Move`](/mobility/motion/#move) method to execute more general robotic motion.
You can designate specific components for motion planning by passing in the resource name (note the use of the arm resource in the code samples below).
The `worldState` we constructed earlier is also passed in so that the motion service takes that information into account when planning.

The sample pose given below can be adjusted to fit your specific circumstances.
Remember that X, Y, and Z coordinates are specified in millimeters.

Again, a note:

{{< alert title="Caution" color="caution" >}}
Executing code presented after this point _will_ induce motion in a connected robotic arm!
Keep the space around the arm clear!
{{< /alert >}}
<br><br>
{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Generate a sample "start" pose to demonstrate motion
test_start_pose = Pose(x=510.0,
                       y=0.0,
                       z=526.0,
                       o_x=0.7071,
                       o_y=0.0,
                       o_z=-0.7071,
                       theta=0.0)
test_start_pose_in_frame = PoseInFrame(reference_frame="world",
                                       pose=test_start_pose)

await motion_service.move(component_name=my_arm_resource_name,
                          destination=test_start_pose_in_frame,
                          world_state=world_state)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Generate a sample "start" pose to demonstrate motion
testStartPose := spatialmath.NewPose(
  r3.Vector{X: 510.0, Y: 0.0, Z: 526.0},
  &spatialmath.OrientationVectorDegrees{OX: 0.7071, OY: 0.0, OZ: -0.7071, Theta: 0.0},
)
testStartPoseInFrame := referenceframe.NewPoseInFrame(referenceframe.World, testStartPose)

_, err = motionService.Move(context.Background(), myArmResourceName, testStartPoseInFrame, worldState, nil, nil)
if err != nil {
  logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

<!-- TODO : In the future, we should add some specific information on the importance of the frame chosen as the point of reference for PoseInFrame variables -->
<!-- ## Managing Pose References -->

## Command other components to move with the motion service

In this section you will add a new component to your machine.
One device that is very commonly attached to the end of a robot arm is a [_gripper_](/components/gripper/).
Most robot arms pick up and manipulate objects in the world with a gripper, so learning how to directly move a gripper is very useful.
Though various motion service commands cause the gripper to move, ultimately the arm is doing all of the work in these situations.
This is possible because the motion service considers other components of the robot (through the [frame system](/mobility/frame-system/)) when calculating how to achieve the desired motion.

### Add a gripper component

We need to do several things to prepare a new gripper component for motion.

1. Go back to your robot configuration in the [Viam app](https://app.viam.com).
2. Navigate to the **Components** tab and click **Create component** in the lower-left corner to add a new gripper component to your robot:
   - Select `gripper` for the type and `fake` for the model.
   - Enter `myGripper` for the name of your gripper component.
   - Click **Create**.
3. Add a **Frame** to the gripper component:
   - Set the parent as `myArm`.
   - Set the translation as something small in the +Z direction, such as `90` millimeters.
   - Leave the orientation as the default.
   - For **Geometry Type** choose **Box**.
   - Enter desired values for the box's **Length**, **Width**, and **Height**, and the box origin's **X**, **Y**, and **Z** values.
4. Include the `myArm` component in the **Depends On** dropdown for `myGripper`.
5. Save this new machine configuration.
   - Your `viam-server` instance should update automatically.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/motion/plan_03_gripper_config.png" resize="700x" declaredimensions=true alt="Sample gripper configuration with several fields filled out.">}}
</div>

Because the new gripper component is "attached" (with the parent specification in the Frame) to `myArm`, we can produce motion plans using `myGripper` instead of `myArm`.

The last library you must import is the `gripper` library.

{{< tabs >}}
{{% tab name="Python" %}}

Add the following line to your import list:

```python
from viam.components.gripper import Gripper
```

Then add this code to your `main()`:

```python {class="line-numbers linkable-line-numbers"}
my_gripper_resource = Gripper.get_resource_name("myGripper")

# Move the gripper in the -Z direction with respect to its own reference frame
gripper_pose_rev = Pose(x=0.0,
                        y=0.0,
                        z=-100.0,
                        o_x=0.0,
                        o_y=0.0,
                        o_z=1.0,
                        theta=0.0)
# Note the change in frame name
gripper_pose_rev_in_frame = PoseInFrame(
    reference_frame=my_gripper_resource.name,
    pose=gripper_pose_rev)

await motion_service.move(component_name=my_gripper_resource,
                          destination=gripper_pose_rev_in_frame,
                          world_state=world_state)
```

{{% /tab %}}
{{% tab name="Go" %}}
Add the following line to your import list:

```go
"go.viam.com/rdk/components/gripper"
```

Then add this code to your `main()`:

```go {class="line-numbers linkable-line-numbers"}
gripperName := "myGripper"
gripperResource := gripper.Named(gripperName)

// This will move the gripper in the -Z direction with respect to its own reference frame
gripperPoseRev := spatialmath.NewPose(
  r3.Vector{X: 0.0, Y: 0.0, Z: -100.0},
  &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
)
gripperPoseRevInFrame := referenceframe.NewPoseInFrame(gripperName, gripperPoseRev) // Note the change in frame name

_, err = motionService.Move(context.Background(), gripperResource, gripperPoseRevInFrame, worldState, nil, nil)
if err != nil {
  logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

For the gripper pose, you can change the reference frame information to consider other objects or user-generated frames that exist in the frame system.
Specifying other reference frames is an easy way to move with respect to those frames.
For example, you can specify a pose that is 100 millimeters above the table obstacle featured earlier in this tutorial.
You do not need to calculate that exact pose with respect to the **arm** or **world**.
You must only provide the object name (instead of the `gripperName` you saw in the code samples above) when making the `PoseInFrame` to pass into the `Move` function.
This has implications for how motion is calculated, and what final configuration your robot will rest in after moving.

## Next steps

If you would like to continue onto working with Viam's motion service, check out one of these tutorials:

{{< cards >}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{% card link="/tutorials/services/constrain-motion/" %}}
{{< /cards >}}

{{< snippet "social.md" >}}

## Full tutorial code

{{< tabs >}}
{{% tab name="Python" %}}

```python {id="plan-motion-python-ex" class="line-numbers linkable-line-numbers" data-line=""}
import asyncio

from viam.components.arm import Arm
from viam.components.gripper import Gripper
from viam.proto.common import Geometry, GeometriesInFrame, Pose, PoseInFrame, \
    RectangularPrism, Vector3, WorldState
from viam.proto.component.arm import JointPositions
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.motion import MotionClient


async def connect():
    opts = RobotClient.Options.with_api_key(
      # Replace "<API-KEY>" (including brackets) with your machine's API key
      api_key='<API-KEY>',
      # Replace "<API-KEY-ID>" (including brackets) with your machine's API key
      # ID
      api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('<ROBOT ADDRESS>', opts)


async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    # Access myArm
    my_arm_resource_name = Arm.get_resource_name("myArm")
    my_arm_component = Arm.from_robot(robot, "myArm")

    # End Position of myArm
    my_arm_end_position = await my_arm_component.get_end_position()
    print(f"myArm get_end_position return value: {my_arm_end_position}")

    # Joint Positions of myArm
    my_arm_joint_positions = await my_arm_component.get_joint_positions()
    print(f"myArm get_joint_positions return value: {my_arm_joint_positions}")

    # Command a joint position move: move the forearm of the arm slightly up
    cmd_joint_positions = JointPositions(values=[0, 0, -30.0, 0, 0, 0])
    await my_arm_component.move_to_joint_positions(
        positions=cmd_joint_positions)

    # Generate a simple pose move +100mm in the +Z direction of the arm
    cmd_arm_pose = await my_arm_component.get_end_position()
    cmd_arm_pose.z += 100.0
    await my_arm_component.move_to_position(pose=cmd_arm_pose)

    # Access the motion service
    motion_service = MotionClient.from_robot(robot, "builtin")

    # Get the pose of myArm from the motion service
    my_arm_motion_pose = await motion_service.get_pose(my_arm_resource_name,
                                                       "world")
    print(f"Pose of myArm from the motion service: {my_arm_motion_pose}")

    # Add a table obstacle to a WorldState
    table_origin = Pose(x=-202.5, y=-546.5, z=-19.0)
    table_dims = Vector3(x=635.0, y=1271.0, z=38.0)
    table_object = Geometry(center=table_origin,
                            box=RectangularPrism(dims_mm=table_dims))

    obstacles_in_frame = GeometriesInFrame(reference_frame="world",
                                           geometries=[table_object])

    # Create a WorldState that has the GeometriesInFrame included
    world_state = WorldState(obstacles=[obstacles_in_frame])

    # Generate a sample "start" pose to demonstrate motion
    test_start_pose = Pose(x=510.0,
                           y=0.0,
                           z=526.0,
                           o_x=0.7071,
                           o_y=0.0,
                           o_z=-0.7071,
                           theta=0.0)
    test_start_pose_in_frame = PoseInFrame(reference_frame="world",
                                           pose=test_start_pose)

    await motion_service.move(component_name=my_arm_resource_name,
                              destination=test_start_pose_in_frame,
                              world_state=world_state)

    my_gripper_resource = Gripper.get_resource_name("myGripper")

    # This will move the gripper in the -Z direction with respect to its own
    # reference frame
    gripper_pose_rev = Pose(x=0.0,
                            y=0.0,
                            z=-100.0,
                            o_x=0.0,
                            o_y=0.0,
                            o_z=1.0,
                            theta=0.0)
    # Note the change in frame name
    gripper_pose_rev_in_frame = PoseInFrame(
        reference_frame=my_gripper_resource.name,
        pose=gripper_pose_rev)

    await motion_service.move(component_name=my_gripper_resource,
                              destination=gripper_pose_rev_in_frame,
                              world_state=world_state)

    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% snippet "show-secret.md" %}}

{{% /tab %}}
{{% tab name="Go" %}}

```go {id="plan-motion-go-ex" class="line-numbers linkable-line-numbers" data-line=""}
package main

import (
  "context"
  "fmt"

  "github.com/golang/geo/r3"
  armapi "go.viam.com/api/component/arm/v1"
  "go.viam.com/rdk/components/arm"
  "go.viam.com/rdk/components/gripper"
  "go.viam.com/rdk/logging"
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/rdk/services/motion"
  "go.viam.com/rdk/spatialmath"
  "go.viam.com/rdk/utils"
  "go.viam.com/utils/rpc"
)

func main() {
  logger := logging.NewLogger("client")
  robot, err := client.New(
      context.Background(),
      "<ROBOT ADDRESS>",
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
  defer robot.Close(context.Background())

  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Access myArm
  myArmResourceName := arm.Named("myArm")
  fmt.Println("myArmResourceName:", myArmResourceName)
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

  // Command a joint position move: move the forearm of the arm slightly up
  cmdJointPositions := &armapi.JointPositions{Values: []float64{0.0, 0.0, -30.0, 0.0, 0.0, 0.0}}
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

  // Access the motion service
  motionService, err := motion.FromRobot(robot, "builtin")
  if err != nil {
    logger.Fatal(err)
  }

  // Get the pose of myArm from the motion service
  myArmMotionPose, err := motionService.GetPose(context.Background(), myArmResourceName, referenceframe.World, nil, nil)
  if err != nil {
    fmt.Println(err)
  }
  fmt.Println("Position of myArm from the motion service:", myArmMotionPose.Pose().Point())
  fmt.Println("Orientation of myArm from the motion service:", myArmMotionPose.Pose().Orientation())

  // Add a table obstacle to a WorldState
  obstacles := make([]spatialmath.Geometry, 0)

  tableOrigin := spatialmath.NewPose(
    r3.Vector{X: 0.0, Y: 0.0, Z: -10.0},
    &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
  )
  tableDims := r3.Vector{X: 2000.0, Y: 2000.0, Z: 20.0}
  tableObj, err := spatialmath.NewBox(tableOrigin, tableDims, "table")
  obstacles = append(obstacles, tableObj)

  // Create a WorldState that has the GeometriesInFrame included
  obstaclesInFrame := referenceframe.NewGeometriesInFrame(referenceframe.World, obstacles)
  worldState := &referenceframe.WorldState{
    Obstacles: []*referenceframe.GeometriesInFrame{obstaclesInFrame},
  }

  // Generate a sample "start" pose to demonstrate motion
  testStartPose := spatialmath.NewPose(
    r3.Vector{X: 510.0, Y: 0.0, Z: 526.0},
    &spatialmath.OrientationVectorDegrees{OX: 0.7071, OY: 0.0, OZ: -0.7071, Theta: 0.0},
  )
  testStartPoseInFrame := referenceframe.NewPoseInFrame(referenceframe.World, testStartPose)

  _, err = motionService.Move(context.Background(), myArmResourceName, testStartPoseInFrame, worldState, nil, nil)
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

  _, err = motionService.Move(context.Background(), gripperResource, gripperPoseRevInFrame, worldState, nil, nil)
  if err != nil {
    logger.Fatal(err)
  }
}
```

{{% snippet "show-secret.md" %}}

{{% /tab %}}
{{< /tabs >}}
