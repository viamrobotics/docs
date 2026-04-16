---
linkTitle: "Pick an object"
title: "Pick an object"
weight: 10
layout: "docs"
type: "docs"
description: "Detect, localize, and grasp an object with a robot arm and gripper."
aliases:
  - /motion-planning/motion-how-to/pick-an-object/
---

Picking an object has four steps, and each step has a failure mode. The camera
has to see the object (detection). The vision service has to report it in 3D
(localization, not just a 2D bounding box). The arm has to approach without
colliding with the table or a neighboring fixture. The gripper has to close on
the object, not in front of it or past it. This guide walks through all four
steps, calls out the common places things go wrong, and leaves the result
ready for the
[placement](/motion-planning/pick-and-place/place-an-object/) half.

## Prerequisites

- Arm with [frame system](/motion-planning/frame-system/) and
  [kinematics](/motion-planning/reference/kinematics/) configured
- Gripper configured as a component
- Camera [calibrated](/motion-planning/frame-system/camera-calibration/) and registered
  in the frame system
- Vision service configured for object detection
- [Obstacles](/motion-planning/obstacles/) defined for every surface the arm could collide with (the table the arm is mounted on, any walls or equipment in reach)

## Steps

### 1. Detect and localize the object

Detection tells you _which_ object the camera sees; localization tells you
_where_ it is in 3D. For grasping, you need both. 2D detections from
`GetDetections` are not enough on their own: use `GetObjectPointClouds`, which
returns 3D geometries in the camera's frame, then `TransformPose` the result
into the world frame so the motion service can plan against the pose.

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
    # The center of the first geometry is the object's position
    # in the camera's reference frame
    center = obj.geometries.geometries[0].center
    obj_in_camera = PoseInFrame(
        reference_frame="my-camera",
        pose=Pose(x=center.x, y=center.y, z=center.z)
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

### 2. Approach the object from above

A grasp is easiest to plan as two motions: first to a pre-grasp pose 100 mm
above the object with the gripper oriented downward, then a short vertical
descent. The two-motion approach gives the planner a clean path that does not
brush obstacles on the way down, and it makes the grasp itself nearly
deterministic since only one axis is moving at the end.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient
motion_service = MotionClient.from_robot(machine, "builtin")

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
    component_name="my-arm",
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
    component_name="my-arm",
    destination=grasp_pose,
    world_state=world_state
)
print("At grasp position")
```

{{% /tab %}}
{{< /tabs >}}

### 4. Grasp and lift

The grasp itself closes the gripper on the object, confirms contact, and lifts
straight up before planning any further motion. `gripper.grab()` returns a
boolean: true if the gripper's contact sensor confirms closure, false if it
closed but sensed nothing. Treat a false return as "try again with a different
approach": pressing onward with an empty gripper wastes time and can damage
downstream setups.

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
    component_name="my-arm",
    destination=lift_pose,
    world_state=world_state
)
print("Object lifted")
```

{{% /tab %}}
{{< /tabs >}}

## Tips

- **Let the gripper touch the object.** By default the planner refuses any
  path with frame-on-frame contact, which blocks grasps by design. Allow the
  gripper-object pair with `CollisionSpecification`; see
  [Allow frame collisions](/motion-planning/obstacles/allow-frame-collisions/).
- **Add vertical clearance to the grasp height.** Vision depth estimates are
  rarely accurate to the millimeter. A 5-10 mm margin above the object's
  reported top surface prevents the gripper from crashing into it when depth
  is off.
- **Confirm the grasp before moving.** `gripper.grab()`'s boolean return is
  fast but not infallible. For fragile or expensive objects, poll force
  feedback or `is_moving` for a second after closure to catch slippage before
  you lift.

## What's next

- [Place an object](/motion-planning/pick-and-place/place-an-object/):
  move the grasped object to a target location.
- [Configure motion constraints](/motion-planning/move-an-arm/constraints/):
  use CollisionSpecification to allow gripper-object contact.
