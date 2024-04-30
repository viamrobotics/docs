---
title: "Add Constraints and Transforms to a Motion Plan"
linkTitle: "Add Motion Constraints"
type: "docs"
description: "Use constraints and transforms with the motion service."
videos:
  [
    "/tutorials/videos/motion_constraints.webm",
    "/tutorials/videos/motion_constraints.mp4",
  ]
images: ["/tutorials/videos/motion_constraints.gif"]
videoAlt: "An arm moving a cup from one side of a tissue box to the other, across a table. The cup stays upright."
tags: ["arm", "gripper", "motion", "services"]
authors: ["Jessamy Taylor"]
languages: ["python"]
viamresources: ["arm", "gripper", "motion", "frame_system"]
level: "Intermediate"
date: "2023-07-03"
# updated: ""
cost: 8400
---

{{< alert title="Caution" color="caution" >}}
Be careful when instructing robot arms to move.
Before running any code, ensure your robotic arm has enough space and that there are no obstacles.
Also pay attention to your surroundings, double-check your code for correctness, and make sure anyone nearby is aware and alert before issuing commands to your robot.
{{< /alert >}}

{{<gif webm_src="/tutorials/videos/motion_constraints.webm" mp4_src="/tutorials/videos/motion_constraints.mp4" alt="An arm moving a cup from one side of a tissue box to the other, across a table. The cup stays upright." class="alignright" max-width="250px">}}

Say you want your robot to pass you a cup of tea, but you don't want it to spill the water or bump into other objects on the table.

If you followed along with the [Plan Motion with an Arm tutorial](../plan-motion-with-arm-gripper/), you used the [motion service](/mobility/motion/) to move a robot arm and end effector to desired positions.
This tutorial builds on this foundation and shows you how to use [constraints](/mobility/motion/constraints/) and transforms to control the way your robot moves between its start and end position.

In this tutorial, you will learn to move a cup across a table without hitting another object, and while remaining upright.

The [full tutorial code](#full-tutorial-code) is available at the end of this page.

## Prerequisites

Before starting this tutorial, you must:

- Install the [Viam Python SDK](https://python.viam.dev/)<!-- or the [Viam Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot/client#section-readme/)-->.
- If you are connecting to a real robotic arm during this tutorial, make sure your computer can communicate with the arm controller before continuing.
  Code examples in this tutorial use a [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6/), but you can use any [arm model](/components/arm/) including a [fake arm model](/components/arm/fake/).
- Complete the previous tutorial, [Plan Motion with an Arm and a Gripper](../plan-motion-with-arm-gripper/), which configures the robot, client and service access, and other infrastructure we'll need for this tutorial.
  For reference, see the [full code sample from the prior tutorial](../plan-motion-with-arm-gripper/#full-tutorial-code).

## Configure your robot

Use the same robot configuration from [the previous tutorial](../plan-motion-with-arm-gripper/) for this tutorial, including the [arm](/components/arm/) and [gripper](/components/gripper/) components with [frames](/mobility/frame-system/) configured.
Make one change: Change the Z translation of the gripper frame from `90` to `0`.

The motion service is one of the "built-in" services, so you don't need to do anything to enable it on your robot.

{{% expand "Click to see what your raw JSON config should look like." %}}

If you completed the previous tutorial, your robot's configuration should match the following.
You can view your robot configuration in [the Viam app](https://app.viam.com/) under the **CONFIGURE** tab by selecting **JSON** mode in the left-hand menu.

If instead you create a new machine for this tutorial, copy and paste the following configuration into the **JSON** field:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "myArm",
      "model": "xArm6",
      "type": "arm",
      "namespace": "rdk",
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
      "model": "fake",
      "type": "gripper",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": ["myArm"],
      "frame": {
        "parent": "myArm",
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

Since this tutorial gets a bit more complicated than the last, let's configure a representation of the table so you can see it in the frame system visualizer.
This configured table won't be taken into account by the motion service, but it's useful to be able to see it.

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `generic` type, then select the `fake` model.
Enter the name `"table"` for your movement sensor and click **Create**.

Select the **Frame** mode on the **CONFIGURE** tab.
Click **table** on the left menu.
For **Geometry** click **box**.

Set the dimensions (**Size**) to `1000` x `1000` x `20`.
Notice that the top of the table is now 10mm above the origin, because the 20mm thickness is centered on the centerpoint.
Account for this by giving the table a **Translation** of `-10` in the Z direction, moving the top of the table to 0.

![The Frame mode of the **CONFIGURE** tab with a 1000 wide, 1000 deep, 200 millimeter thick box representing the top of the table.](../../constrain-motion/frame-table.jpg)

### Visualize obstacles on the table
-->

## Modify your robot's working environment

In the previous tutorial, you [defined a table obstacle](../plan-motion-with-arm-gripper/#describe-the-robots-working-environment) to prevent the arm and gripper from hitting the table upon which the arm is mounted.
In this tutorial, you'll expand on the code that describes your robot's working environment in two ways:

- Define an additional obstacle: a tissue box sitting on the table.
- Add a `z_offset` parameter to the `table_origin` and to the new `box_origin`.
  This makes it easier to calibrate your motion plans based on how high or low your arm is mounted compared to the table.

The following example shows the two obstacles defined such that the table's top surface is at z=0 and the tissue box sits on top of the table.
Adjust the dimensions and positions of the obstacles to describe your own scenario:

```python {class="line-numbers linkable-line-numbers"}
# Use this offset to set your z to calibrate based on where your table actually
# is
z_offset = 10

# Create a table obstacle with its top surface at z=0
table_origin = Pose(x=0.0, y=0.0, z=-19.0+z_offset)
table_dims = Vector3(x=2000.0, y=2000.0, z=38.0)
table_object = Geometry(center=table_origin,
                        box=RectangularPrism(dims_mm=table_dims))

# Create a tissue box obstacle. Setting the box's origin to 50mm above the
# table positions the 100mm tall box on top of the table.
box_origin = Pose(x=400, y=0, z=50+z_offset)
box_dims = Vector3(x=120.0, y=80.0, z=100.0)
box_object = Geometry(center=box_origin,
                      box=RectangularPrism(dims_mm=box_dims))

obstacles_in_frame = GeometriesInFrame(reference_frame="world",
                                       geometries=[table_object, box_object])
```

## Determine the gripper's axes

You need to identify how the gripper's frame corresponds to its hardware so that you can write code that creates your desired behavior.
That is, you need to determine which axis points from the "wrist" to the end of the gripper, which axis lines up with the direction the jaws actuate, and, when the gripper is holding a cup, which axis passes vertically through the cup.

All example code below assumes +Z points from the base of the gripper to the point where its jaws close, +Y points towards the ground when the gripper is holding a cup from the side, and the X axis is the axis along which the jaws close, following the [right-hand rule](https://en.wikipedia.org/wiki/Right-hand_rule).
The following diagram shows this, as well as the global coordinate system.

![A gripper mounted on an arm. The Z axis of the gripper points from the base of the gripper to the end of its jaws. The X axis points up through the gripper. The Y axis points in the direction along which the jaws open and close (following the right-hand rule). The diagram also shows the global coordinate system with Z pointing up, X down the length of the horizontal gripper, and Y pointing horizontally in the opposite direction of the gripper's Y.](/tutorials/constrain-motion/gripper-diagram.png)

If you are using a `fake` gripper, there is no real hardware to calibrate and you can [continue to the next section](#use-a-transform-to-represent-a-drinking-cup), imagining that your fake gripper corresponds to the diagram above.

If you are using a real arm and gripper, use the [**CONTROL** tab](/fleet/machines/control/) in the [Viam app](https://app.viam.com/) to move the gripper, look at its reported orientations, and map them to its orientation in the real world.
If the axes are different from those described above, take these differences into account in your code.

## Use a transform to represent a drinking cup

Imagine your cup is 120 millimeters tall with a radius of 45 millimeters.
You need to take this space into account to avoid bumping objects on the table with the cup.

You can pass transforms to the [motion service `move` method](/mobility/motion/#move) to represent objects that are connected to the robot but are not actual robotic components.
To represent the drinking cup held in your robot's gripper, create a transform with the cup's measurements:

```python {class="line-numbers linkable-line-numbers"}
# Create a transform to represent the cup as a 120mm tall, 45mm radius capsule
# shape
cup_geometry = Geometry(center=Pose(x=0, y=0, z=155),
                        capsule=Capsule(radius_mm=45, length_mm=120))
transforms = [
    # Name the reference frame "cup" and point its long axis along the y axis
    # of the gripper
    Transform(reference_frame="cup",
              pose_in_observer_frame=PoseInFrame(
                  reference_frame="myGripper",
                  pose=Pose(x=0, y=0, z=45, o_x=0, o_y=-1, o_z=0, theta=0)),
              physical_object=cup_geometry)
]
```

Here, we use a 155mm offset along the gripper's Z axis to represent the distance from the base of the gripper to the center of the cup.
We assume the cup is situated against the palm of the gripper's hand.
This offset is then equal to the radius of the cup (45mm) plus the distance from the gripper's origin (where it meets the arm) to its palm (110mm in this example).
If your gripper has different dimensions, change the offset accordingly.

Now that you have created the table and tissue box obstacles as well as the cup transform, create a [WorldState](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState) that includes all of them:

```python {class="line-numbers linkable-line-numbers"}
# Create a WorldState that includes the table and tissue box obstacles, and the
# cup transform
world_state = WorldState(obstacles=[obstacles_in_frame], transforms=transforms)
```

## Define start and end poses

You need to tell the robot where to pick up the cup, and where to put it down.
The previous tutorial [introduced the concept of defining poses](../plan-motion-with-arm-gripper/#command-an-arm-to-move-with-the-motion-service).
For this tutorial, you'll define a pose for the gripper that is just above the table on one side of the tissue box, and another pose on the other side of the tissue box.

You'll also want to define some waypoints.
The motion service has the mathematical ability to plan complex motion from one position to another, even around an obstacle.
However, this is more computationally intensive than planning a linear path from one point to another.
To increase your program's efficiency, add waypoints such that the path between any two consecutive points can be linear, without intersecting the tissue box or the table:

```python {class="line-numbers linkable-line-numbers"}
# Create a start pose, where the cup starts between the gripper's jaws, on the
# table. Start pose has Z of 90mm to grab partway down the 120mm tall cup
start_pose = Pose(x=320, y=240, z=90.0+z_offset, o_x=1, o_y=0, o_z=0, theta=0)
start_pose_in_frame = PoseInFrame(reference_frame="world", pose=start_pose)

# Create waypoints to increase efficiency of motion planning
way1_pose = Pose(x=300, y=240, z=320+z_offset, o_x=1, o_y=0, o_z=0, theta=0)
way1_pose_in_frame = PoseInFrame(reference_frame="world", pose=way1_pose)
way2_pose = Pose(x=300, y=-240, z=320+z_offset, o_x=1, o_y=0, o_z=0, theta=0)
way2_pose_in_frame = PoseInFrame(reference_frame="world", pose=way2_pose)

# Create a pose where the cup will be set down
end_pose = Pose(x=300, y=-250, z=90.0+z_offset, o_x=1, o_y=0, o_z=0, theta=0)
end_pose_in_frame = PoseInFrame(reference_frame="world", pose=end_pose)
```

Though we are passing these waypoints in manually, the motion service will throw an error if we accidentally pass in a pose that would cause the arm or gripper to hit any obstacles we've defined.

Note that the orientations of all the poses are the same.
If we changed the orientation along the way, we might spill the tea!

{{< alert title="Tip" color="tip" >}}
You may be wondering how the orientations of the poses are determined.
Our example gripper's frame is defined such that its orientation vector points from its "wrist" to the tip of its jaws.
In the example code above, all poses have an [orientation vector](/internals/orientation-vector/) pointing along the positive X axis of the world frame, which is a horizontal orientation pointing "forwards" with respect to the xArm 6 base.
When we tell the gripper to move to such a pose, its orientation vector moves to align with the orientation vector of the pose, so its jaws end up pointing along the global X axis, "forwards" from the robot base.
This puts it in a good position for picking up and moving a cup.

Additionally, for our gripper, setting `theta=0` about this particular orientation vector orients the gripper such that its jaws open and close horizontally.
If we changed it to `theta=90` or `theta=270`, the gripper jaws would open vertically, not ideal for picking up a cup!
{{< /alert >}}

## Add a motion constraint

To keep the cup upright as the arm moves it from one place on the table to another, create a [linear constraint](/mobility/motion/constraints/#linear-constraint).
When you tell the robot to move the cup from one upright position to another, the linear constraint forces the gripper to move linearly and to maintain the upright orientation of the cup throughout the planned path.

You could try using an [orientation constraint](/mobility/motion/constraints/#orientation-constraint) instead, which would also constrain the orientation.
However, since this opens up many more options for potential paths, it is much more computationally intensive than the linear constraint.

The code below creates a linear constraint and then uses that constraint to keep the cup upright and move it in a series of linear paths along the predetermined route while avoiding the obstacles we've defined:

```python {class="line-numbers linkable-line-numbers"}
# Create a linear constraint to keep the cup upright and constrain it to a
# linear path
constraints = Constraints(linear_constraint=[LinearConstraint()])

# Move the cup to the end position without hitting the box on the table,
# and while keeping the cup upright
await motion_service.move(component_name=my_gripper_resource_name,
                          destination=way1_pose_in_frame,
                          world_state=world_state,
                          constraints=constraints)
await motion_service.move(component_name=my_gripper_resource_name,
                          destination=way2_pose_in_frame,
                          world_state=world_state,
                          constraints=constraints)
await motion_service.move(component_name=my_gripper_resource_name,
                          destination=end_pose_in_frame,
                          world_state=world_state,
                          constraints=constraints)
print("At end pose")

# Put down the cup
await my_gripper.open()
```

## Full tutorial code

The following code contains everything covered in this tutorial in addition to the `connect()` function, and the resource access code from the last tutorial that you need here as well.
Be sure to change the `<API-KEY>`, `<API-KEY-ID>`, and the `ADDRESS FROM THE VIAM APP` placeholders shown in the code to match your actual robot credentials, and change all relevant parameters such as `z_offset` and other dimensions and poses to match your hardware.
You can find the `<API-KEY>` and `<API-KEY-ID>` values for your machine on the **CONNECT** tab's **API keys** page.

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.arm import Arm
from viam.proto.component.arm import JointPositions
from viam.components.gripper import Gripper
from viam.services.motion import MotionClient
from viam.proto.common import Pose, PoseInFrame, Vector3, Geometry, \
    GeometriesInFrame, RectangularPrism
from viam.proto.service.motion import Constraints, LinearConstraint


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
    robot = await connect()

    # myArm
    my_arm = Arm.from_robot(robot, "myArm")
    my_arm_resource_name = Arm.get_resource_name("myArm")

    # myGripper
    my_gripper = Gripper.from_robot(robot, "myGripper")
    my_gripper_resource_name = Gripper.get_resource_name("myGripper")

    # Get the pose of the arm from the arm API
    cmd_arm_pose = await my_arm.get_end_position()
    print("Pose of end of myArm from get_end_position:", cmd_arm_pose)

    # Access the motion service
    motion_service = MotionClient.from_robot(robot, "builtin")

    # Get the pose of myArm from the motion service
    my_arm_motion_pose = await motion_service.get_pose(my_arm_resource_name,
                                                       "world")
    print("Pose of myArm from the motion service:", my_arm_motion_pose)

    # Use this offset to set your z to calibrate based on where your table
    # actually is
    z_offset = 10

    # Create a table obstacle
    table_origin = Pose(x=0.0, y=0.0, z=-19.0+z_offset)
    table_dims = Vector3(x=2000.0, y=2000.0, z=38.0)
    table_object = Geometry(center=table_origin,
                            box=RectangularPrism(dims_mm=table_dims))

    # Create a tissue box obstacle
    box_origin = Pose(x=400, y=0, z=50+z_offset)
    box_dims = Vector3(x=120.0, y=80.0, z=100.0)
    box_object = Geometry(center=box_origin,
                          box=RectangularPrism(dims_mm=box_dims))

    obstacles_in_frame = GeometriesInFrame(
        reference_frame="world",
        geometries=[table_object, box_object])

    # Create a transform to represent the cup as a 120mm tall, 45mm radius
    # capsule shape
    cup_geometry = Geometry(center=Pose(x=0, y=0, z=155),
                            capsule=Capsule(radius_mm=45, length_mm=120))
    transforms = [
        # Name the reference frame "cup" and point its long axis along the y
        # axis of the gripper
        Transform(reference_frame="cup", pose_in_observer_frame=PoseInFrame(
            reference_frame="myGripper",
            pose=Pose(x=0, y=0, z=45, o_x=0, o_y=-1, o_z=0, theta=0)),
            physical_object=cup_geometry)
    ]

    # Create a WorldState that includes the table and tissue box obstacles, and
    # the cup transform
    world_state = WorldState(obstacles=[obstacles_in_frame],
                             transforms=transforms)

    # Create a start pose, where the cup starts between the gripper's jaws, on
    # the table. Start pose has Z of 90mm to grab partway down the 120mm tall
    # cup
    start_pose = Pose(x=320,
                      y=240,
                      z=90.0+z_offset,
                      o_x=1,
                      o_y=0,
                      o_z=0,
                      theta=0)
    start_pose_in_frame = PoseInFrame(reference_frame="world", pose=start_pose)

    # Create waypoints to increase efficiency of motion planning
    way1_pose = Pose(x=300,
                     y=240,
                     z=320+z_offset,
                     o_x=1,
                     o_y=0,
                     o_z=0,
                     theta=0)
    way1_pose_in_frame = PoseInFrame(reference_frame="world", pose=way1_pose)
    way2_pose = Pose(x=300,
                     y=-240,
                     z=320+z_offset,
                     o_x=1,
                     o_y=0,
                     o_z=0,
                     theta=0)
    way2_pose_in_frame = PoseInFrame(reference_frame="world", pose=way2_pose)

    # Create a pose where the cup will be set down
    end_pose = Pose(x=300,
                    y=-250,
                    z=90.0+z_offset,
                    o_x=1,
                    o_y=0,
                    o_z=0,
                    theta=0)
    end_pose_in_frame = PoseInFrame(reference_frame="world", pose=end_pose)

    # Move to the starting position and grab the cup
    # This motion has no orientation constraints because it hasn't picked up
    # the cup yet
    await motion_service.move(component_name=my_gripper_resource_name,
                              destination=start_pose_in_frame,
                              world_state=world_state)
    print("At start pose")
    await my_gripper.grab()

    # Create a constraint to keep the cup upright as it moves
    constraints = Constraints(linear_constraint=[LinearConstraint()])

    # Move the cup to the end position without hitting the box on the table,
    # and while keeping the cup upright
    await motion_service.move(component_name=my_gripper_resource_name,
                              destination=way1_pose_in_frame,
                              world_state=world_state,
                              constraints=constraints)
    await motion_service.move(component_name=my_gripper_resource_name,
                              destination=way2_pose_in_frame,
                              world_state=world_state,
                              constraints=constraints)
    await motion_service.move(component_name=my_gripper_resource_name,
                              destination=end_pose_in_frame,
                              world_state=world_state,
                              constraints=constraints)
    print("At end pose")

    # Put down the cup
    await my_gripper.open()

    # Don't forget to close the robot when you're done!
    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
```

## Next steps

If you would like to continue onto working with Viam's motion service, check out this tutorial:

{{< cards >}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{< /cards >}}
