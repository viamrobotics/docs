---
linkTitle: "Pick an Object"
title: "Pick an Object"
weight: 50
layout: "docs"
type: "docs"
description: "Detect, localize, and grasp an object with a robot arm and gripper."
---

You need to pick up an object from a workspace. This requires detecting the
object with a camera, determining its 3D position, planning a collision-free
approach path, and controlling the gripper to grasp it.

## Prerequisites

- Arm with [frame system](/motion-planning/frame-system/) and
  [kinematics](/motion-planning/reference/kinematics/) configured
- Gripper configured as a component
- Camera [calibrated](/motion-planning/camera-calibration/) and registered
  in the frame system
- Vision service configured for object detection
- [Obstacles](/motion-planning/obstacles/) defined (at minimum, the table)

## Steps

### 1. Detect and localize the object

Use a vision service to detect the object in 2D, then transform its position
to the world frame.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.vision import VisionClient
from viam.proto.common import PoseInFrame, Pose

vision = VisionClient.from_robot(machine, "my-detector")

# Get detections from the camera
detections = await vision.get_detections_from_camera("my-camera")
if not detections:
    print("No objects detected")
    exit()

target = detections[0]
print(f"Detected: {target.class_name} ({target.confidence:.2f})")

# For 3D localization, use GetObjectPointClouds
objects = await vision.get_object_point_clouds("my-camera")
if objects:
    obj = objects[0]
    # Position is in camera frame
    obj_in_camera = PoseInFrame(
        reference_frame="my-camera",
        pose=Pose(
            x=obj.geometry_in_frame.pose.x,
            y=obj.geometry_in_frame.pose.y,
            z=obj.geometry_in_frame.pose.z
        )
    )
    # Transform to world frame
    obj_in_world = await machine.transform_pose(obj_in_camera, "world")
    print(f"Object position in world: "
          f"x={obj_in_world.pose.x:.1f}, "
          f"y={obj_in_world.pose.y:.1f}, "
          f"z={obj_in_world.pose.z:.1f}")
```

{{% /tab %}}
{{< /tabs >}}

### 2. Plan approach and pre-grasp pose

Move the arm to a position above the object (pre-grasp pose) before descending
to grasp.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient
from viam.proto.common import ResourceName

motion_service = MotionClient.from_robot(machine, "builtin")
arm_name = ResourceName(
    namespace="rdk", type="component",
    subtype="arm", name="my-arm"
)

# Pre-grasp: 100mm above the object, end effector pointing down
pre_grasp = PoseInFrame(
    reference_frame="world",
    pose=Pose(
        x=obj_in_world.pose.x,
        y=obj_in_world.pose.y,
        z=obj_in_world.pose.z + 100,
        o_x=0, o_y=0, o_z=-1, theta=0
    )
)

await motion_service.move(
    component_name=arm_name,
    destination=pre_grasp,
    world_state=world_state
)
print("At pre-grasp position")
```

{{% /tab %}}
{{< /tabs >}}

### 3. Open gripper and descend

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.gripper import Gripper

gripper = Gripper.from_robot(machine, "my-gripper")

# Open gripper
await gripper.open()

# Descend to grasp position
grasp_pose = PoseInFrame(
    reference_frame="world",
    pose=Pose(
        x=obj_in_world.pose.x,
        y=obj_in_world.pose.y,
        z=obj_in_world.pose.z,
        o_x=0, o_y=0, o_z=-1, theta=0
    )
)

await motion_service.move(
    component_name=arm_name,
    destination=grasp_pose,
    world_state=world_state
)
print("At grasp position")
```

{{% /tab %}}
{{< /tabs >}}

### 4. Grasp and lift

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Close gripper to grasp
grabbed = await gripper.grab()
if grabbed:
    print("Object grasped")
else:
    print("Grasp failed")

# Lift the object
lift_pose = PoseInFrame(
    reference_frame="world",
    pose=Pose(
        x=obj_in_world.pose.x,
        y=obj_in_world.pose.y,
        z=obj_in_world.pose.z + 200,
        o_x=0, o_y=0, o_z=-1, theta=0
    )
)

await motion_service.move(
    component_name=arm_name,
    destination=lift_pose,
    world_state=world_state
)
print("Object lifted")
```

{{% /tab %}}
{{< /tabs >}}

## Tips

- Use `CollisionSpecification` constraints to allow the gripper to contact the
  target object during the grasp phase.
- Add a small offset to the grasp height to account for measurement uncertainty.
- After grasping, re-verify with the gripper's `is_moving` or force feedback
  before proceeding.

## What's Next

- [Place an Object](/motion-planning/motion-how-to/place-an-object/):
  move the grasped object to a target location.
- [Configure Motion Constraints](/motion-planning/constraints/):
  use CollisionSpecification to allow gripper-object contact.
