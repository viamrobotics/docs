---
title: "Add Constraints to a Motion Plan"
linkTitle: "Add Motion Constraints"
weight: 25
type: "docs"
description: "Use constraints with the Motion Service to move robot components in specific ways."
webmSrc: "/tutorials/videos/motion_armmoving.webm"
mp4Src: "/tutorials/videos/motion_armmoving.mp4"
videoAlt: "An arm moving in a plane with the Motion Service"
tags: ["arm", "gripper", "motion", "services"]
# SMEs: Motion Team
---

{{< alert title="Caution" color="caution" >}}
Be careful when instructing robot arms to move.
Before running any code, ensure your robotic arm has enough space and that there are no obstacles.
Also pay attention to your surroundings, double-check your code for correctness, and make sure anyone nearby is aware and alert before issuing commands to your robot.
{{< /alert >}}

Say you want your robot to pass you a cup of water, but you don't want it to spill the water or bump into the tasty treats on the table.

If you followed along in [part 2 of the Motion Service tutorial series](../plan-motion-with-arm-gripper/), you used the [Motion Service](/services/motion/) to move a robot arm and end effector to desired positions.
This tutorial builds on that and shows you how to use [constraints](/services/motion/constraints/) to control the way your robot moves between its start and end position.

In this tutorial, you will learn to move a cup across a table without hitting another object, and while remaining upright.

{{< alert title="Note" color="note" >}}
Code examples in this tutorial use a [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6/), but you can use any [arm model](/components/arm/).
The [full tutorial code](#full-tutorial-code) is available at the end of this page.
{{< /alert >}}

## Prerequisites

Before starting this tutorial, make sure you have the [Viam Python SDK](https://python.viam.dev/) or the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme/) installed.

If you are connecting to a real robotic arm during this tutorial, make sure your computer can communicate with the controller before continuing.

Familiarize yourself with the concepts outlined in the second Motion tutorial, [Plan Motion with an Arm and a Gripper](../plan-motion-with-arm-gripper/), before continuing.
This tutorial picks up right where **Plan Motion with an Arm and a Gripper** stops, so further examples depend on having a connected robot, client and service access, and other infrastructure in place.
This also helps simplify and shorten the code examples presented below.

For a helpful recap of the code we previously added, look at [the full code sample from the prior tutorial](../plan-motion-with-arm-gripper/#full-tutorial-code).

## Configure your robot

Use the robot configuration from [the previous tutorial](../plan-motion-with-arm-gripper/) for this tutorial, including the [arm](../../../components/arm/) and [gripper](../../../components/gripper/) components with [frames](../../../services/frame-system/) configured.

The Motion Service is one of the "built-in" services, so you don't need to do anything to enable it on your robot.

{{% expand "Click for an example raw JSON config." %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "myArm",
      "type": "arm",
      "model": "xArm6",
      "attributes": {
        "host": "<ip-address>",
        "port": 0,
        "speed_degs_per_sec": 15,
        "acceleration_degs_per_sec_per_sec": 0
      },
      "depends_on": [],
      "frame": {
        "parent": "world",
        "translation": {
          "x": 0,
          "y": 0,
          "z": 0
        },
        "orientation": {
          "type": "ov_degrees",
          "value": {
            "x": 0,
            "y": 0,
            "z": 1,
            "th": 0
          }
        }
      }
    },
    {
      "name": "myGripper",
      "type": "gripper",
      "model": "fake",
      "attributes": {},
      "depends_on": [
        "myArm"
      ],
      "frame": {
        "parent": "myArm",
        "translation": {
          "x": 0,
          "y": 0,
          "z": 90
        },
        "orientation": {
          "type": "ov_degrees",
          "value": {
            "x": 0,
            "y": 0,
            "z": 1,
            "th": 0
          }
        },
        "geometry": {
          "x": 73,
          "y": 73,
          "z": 90,
          "translation": {
            "x": 0,
            "y": 0,
            "z": 0
          }
        }
      }
    }
  ]
}
```

{{% /expand %}}

<!--
## Visualize your table

In the previous tutorial you [created a representation of a table](../plan-motion-with-arm-gripper/#describe-the-robots-working-environment) in your client code.
You will use this same code later in this tutorial.

Since this tutorial gets a bit more complicated than the last, let's configure a representation of the table so you can see it in the Frame System visualizer.
This configured table won't be taken into account by the Motion Service, but it's useful to be able to see it.

On your robot's **Config** tab, create a new component called `table` with **Type** `generic` and **Model** `fake`.
Click **Create component**, then click **Add frame**.

Go to the **Frame System** subtab.
Click **table** on the left menu.
For **Geometry** click **box**.

Set the dimensions (**Size**) to `1000` x `1000` x `20`.
Notice that the top of the table is now 10mm above the origin, because the 20mm thickness is centered on the centerpoint.
Account for this by giving the table a **Translation** of `-10` in the Z direction, moving the top of the table to 0.

![The Frame System subtab of the Components tab with a 1000 wide, 1000 deep, 200 millimeter thick box representing the top of the table.](../../img/constrain-motion/frame-table.jpg)

### Visualize obstacles on the table
-->

## Add an obstacle on the table

In the last tutorial, you [added a table obstacle](../plan-motion-with-arm-gripper/#describe-the-robots-working-environment) to prevent the arm and gripper from hitting the table upon which the arm is mounted.
In this tutorial, keep that table code and add an additional obstacle: a cake sitting on the table.

You can adjust the dimensions and position of this obstacle to describe your own scenario, but here is an example:

```python {class="line-numbers linkable-line-numbers"}
# Add a table obstacle to the WorldState
table_origin = Pose(x=-202.5, y=-546.5, z=-19.0)
table_dims = Vector3(x=635.0, y=1271.0, z=38.0)
table_object = Geometry(center=table_origin, table_box=RectangularPrism(dims_mm=table_dims))

# Add a cake obstacle to the WorldState
cake_origin = Pose(x=-202.5, y=-546.5, z=-19.0)
cake_dims = Vector3(x=300.0, y=300.0, z=160.0)
cake_object = Geometry(center=cake_origin, cake_box=RectangularPrism(dims_mm=cake_dims))

obstacles_in_frame = GeometriesInFrame(reference_frame="world", geometries=[table_object, cake_object])
```

## Determine the gripper's axes

You need to figure out how the gripper's frame corresponds to its hardware.
That is, you need to know which axis points from the "wrist" to the end of the gripper, which axis lines up with the direction the jaws actuate, and if the gripper was holding a cup, which axis would pass vertically through the cup.

All example code below assumes +Z points from the base of the gripper to the point where its jaws close, +Y points towards the ground when the gripper is holding a cup from the side, and the X axis is the axis along which the jaws close, following the [right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule/).

<!--
TODO: Insert diagram
-->

If you are using a `fake` gripper, there is no real hardware and you can [continue this tutorial](#use-a-transform-to-represent-a-drinking-cup).

If you are using a real arm and gripper, use the **Control** tab in the [Viam app](https://app.viam.com/) to move the gripper, look at its reported orientations, and map them to its orientation in the real world.
If the axes are different from those described above, take these differences into account in your code.

## Use a transform to represent a drinking cup

Imagine your cup is 120 millimeters tall and 90 millimeters in diameter.
<!-- When the gripper is holding the middle of the cup from the side, the cup will extend 90mm out from the gripper, and 60mm down from the gripper's center.
-->
You need to take this space into account to avoid bumping objects on the table with the cup.

You can pass transforms to the [Motion Service `move` method](../../../services/motion/#move) to represent objects that are connected to the robot but are not actual robotic components.
To represent the drinking cup held in your robot's gripper, add this to your code:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Create a transform to represent the cup as a 120mm tall (plus radii), 90mm across capsule shape
cup_geometry = Geometry(center=Pose(x=0, y=0, z=155),
    cup_capsule=Capsule(dims_mm=Vector3(diameter=90, length=120)))
transforms = [
    # Name the reference frame "cup" and point its long axis along the y axis of the gripper
    Transform(reference_frame="cup", pose_in_observer_frame=PoseInFrame(reference_frame="myGripper",
        pose=Pose(x=0, y=0, z=45, o_x=0, o_y=-1, o_z=0, theta=0)), physical_object=cup_geometry)
]
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}

The 155mm offset along the gripper's Z axis accounts for the radius of the gripper (45mm), plus the distance from the gripper's origin (where it meets the arm) and what you can think of as the palm of its hand.
In this example, that distance is 110mm, but if you have a different gripper, change the offset accordingly.

Now that you have created the table and cake obstacles and the cup transform, create a WorldState that includes all of them:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Create a WorldState that includes the table and cake obstacles, and the cup transform
world_state = WorldState(obstacles=[obstacles_in_frame], transforms = transforms)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}

## Define start and end poses

You need to tell the robot where to pick up the cup, and where to put it down.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Create a start pose, where the cup starts between the gripper's jaws, on the table
# Start pose has Z of 60mm to grab the middle of the 120mm tall cup
start_pose = Pose(x=200, y=215, z=60.0, o_x=1, o_y=0, o_z=0, theta=0)
start_pose_in_frame = PoseInFrame(reference_frame="world", pose=start_pose)

# Create a pose to which to move the cup
end_pose = Pose(x=200, y=-210, z=60.0, o_x=1, o_y=0, o_z=0, theta=0)
end_pose_in_frame = PoseInFrame(reference_frame="world", pose=end_pose)

# Move to the starting position and grab the cup
# This motion has no orientation constraints because it hasn't picked up the cup yet
await motion_service.move(component_name=my_gripper_resource_name, destination=start_pose_in_frame, world_state=world_state)
await my_gripper.grab()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}

## Add an orientation constraint

To keep the cup upright as the arm moves it from one place on the table to another, create an [orientation constraint](../../../services/motion/constraints/#orientation-constraint).
Then, when you tell the robot to move the cup from one upright position to another, the orientation will be maintained throughout the planned path.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Create an orientation constraint to keep the cup upright as it moves
constraints={"motion_profile": "orientation"}

# Move the cup to the end position without hitting the cake on the table,
# and while keeping the cup upright
await motion_service.move(component_name=my_gripper_resource_name, destination=end_pose_in_frame,
    world_state=world_state, constraints=constraints)

# Put down the cup
await my_gripper.open()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}

## Next steps

If you would like to continue onto working with Viam's Motion Service, check out this tutorial:

{{< cards >}}
  {{% card link="/tutorials/projects/claw-game/" size="small" %}}
{{< /cards >}}

Or, try adding a [linear constraint](../../../services/motion/constraints/#linear-constraint) or different obstacles to your robot!

{{< snippet "social.md" >}}

## Full tutorial code

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.arm import Arm
from viam.proto.component.arm import JointPositions
from viam.components.gripper import Gripper
from viam.services.motion import MotionClient
# from viam.proto.common import Pose, PoseInFrame, Vector3, Geometry, GeometriesInFrame, RectangularPrism
from viam.proto.common import *

async def connect():
    creds = Credentials(type="robot-location-secret", payload="<ROBOT SECRET PAYLOAD>")
    opts = RobotClient.Options(refresh_interval=0, dial_options=DialOptions(credentials=creds))
    return await RobotClient.at_address("<ROBOT ADDRESS", opts)


async def main():
    robot = await connect()

    # myArm
    my_arm = Arm.from_robot(robot, "myArm")
    my_arm_resource_name = Arm.get_resource_name("myArm")

    # myGripper
    my_gripper = Gripper.from_robot(robot, "myGripper")
    my_gripper_resource_name = Gripper.get_resource_name("myGripper")

    # Get the pose of the arm from the arm API
    cmd_arm_pose = await my_arm.get_end_position()
    print(f"Pose of end of myArm from get_end_position:", cmd_arm_pose)

    # Access the Motion Service
    motion_service = MotionClient.from_robot(robot, "builtin")

    # Get the pose of myArm from the Motion Service
    my_arm_motion_pose = await motion_service.get_pose(my_arm_resource_name, "world")
    print(f"Pose of myArm from the Motion Service: {my_arm_motion_pose}")

    # Create a table obstacle
    table_origin = Pose(x=-202.5, y=-546.5, z=-19.0)
    table_dims = Vector3(x=635.0, y=1271.0, z=38.0)
    table_object = Geometry(center=table_origin, table_box=RectangularPrism(dims_mm=table_dims))

    # Create a cake obstacle
    cake_origin = Pose(x=-202.5, y=-546.5, z=-19.0)
    cake_dims = Vector3(x=300.0, y=300.0, z=160.0)
    cake_object = Geometry(center=cake_origin, cake_box=RectangularPrism(dims_mm=cake_dims))

    obstacles_in_frame = GeometriesInFrame(reference_frame="world", geometries=[table_object, cake_object])

    # Create a transform to represent the cup as a 120mm tall (plus radii), 90mm across capsule shape
    cup_geometry = Geometry(center=Pose(x=0, y=0, z=155),
        cup_capsule=Capsule(dims_mm=Vector3(diameter=90, length=120)))
    transforms = [
        # Name the reference frame "cup" and point its long axis along the y axis of the gripper
        Transform(reference_frame="cup", pose_in_observer_frame=PoseInFrame(reference_frame="myGripper",
            pose=Pose(x=0, y=0, z=45, o_x=0, o_y=-1, o_z=0, theta=0)), physical_object=cup_geometry)
    ]

    # Create a WorldState that includes the table and cake obstacles, and the cup transform
    world_state = WorldState(obstacles=[obstacles_in_frame], transforms = transforms)

    # Create a start pose, where the cup starts between the gripper's jaws, on the table
    # Start pose has Z of 60mm to grab the middle of the 120mm tall cup
    start_pose = Pose(x=200, y=215, z=60.0, o_x=1, o_y=0, o_z=0, theta=0)
    start_pose_in_frame = PoseInFrame(reference_frame="world", pose=start_pose)

    # Create a pose to which to move the cup
    end_pose = Pose(x=200, y=-210, z=60.0, o_x=1, o_y=0, o_z=0, theta=0)
    end_pose_in_frame = PoseInFrame(reference_frame="world", pose=end_pose)
    
    # Move to the starting position and grab the cup
    # This motion has no orientation constraints because it hasn't picked up the cup yet
    await motion_service.move(component_name=my_gripper_resource_name, destination=start_pose_in_frame, world_state=world_state)
    await my_gripper.grab()

    # Create an orientation constraint to keep the cup upright as it moves
    constraints={"motion_profile": "orientation"}

    # Move the cup to the end position without hitting the cake on the table,
    # and while keeping the cup upright
    await motion_service.move(component_name=my_gripper_resource_name, destination=end_pose_in_frame,
        world_state=world_state, constraints=constraints)
    
    # Put down the cup
    await my_gripper.open()

    # Don't forget to close the robot when you're done!
    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())

```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
package main

import (
  "context"
  "fmt"

  "github.com/edaniels/golog"
  "github.com/golang/geo/r3"
  armapi "go.viam.com/api/component/arm/v1"
  "go.viam.com/rdk/components/arm"
  "go.viam.com/rdk/components/gripper"
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/rdk/services/motion"
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
```

{{% /tab %}}
{{< /tabs >}}
