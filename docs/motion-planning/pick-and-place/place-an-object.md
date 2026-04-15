---
linkTitle: "Place an object"
title: "Place an object"
weight: 20
layout: "docs"
type: "docs"
description: "Move a grasped object to a target location and release it."
aliases:
  - /motion-planning/motion-how-to/place-an-object/
---

You have an object in the gripper and need to place it at a specific location.
This involves planning a collision-free path to the placement pose, descending
to the surface, releasing, and retreating.

## Prerequisites

- Object already grasped (see [Pick an Object](/motion-planning/motion-how-to/pick-an-object/))
- Placement location known in world coordinates

## Steps

### 1. Move to pre-place position

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Pre-place: above the target location
pre_place = PoseInFrame(
    reference_frame="world",
    pose=Pose(
        x=500, y=0, z=200,
        o_x=0, o_y=0, o_z=-1, theta=0
    )
)

await motion_service.move(
    component_name="my-arm",
    destination=pre_place,
    world_state=world_state
)
```

{{% /tab %}}
{{< /tabs >}}

### 2. Descend to placement surface

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Place: at the surface.
# Set z to the height of the placement surface in your workspace.
# For example, if you detected the target location, use its z coordinate.
SURFACE_HEIGHT = 50  # mm — adjust for your setup
place_pose = PoseInFrame(
    reference_frame="world",
    pose=Pose(
        x=500, y=0, z=SURFACE_HEIGHT,
        o_x=0, o_y=0, o_z=-1, theta=0
    )
)

await motion_service.move(
    component_name="my-arm",
    destination=place_pose,
    world_state=world_state
)
```

{{% /tab %}}
{{< /tabs >}}

### 3. Release and retreat

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Open gripper to release
await gripper.open()
print("Object placed")

# Retreat: lift straight up
retreat_pose = PoseInFrame(
    reference_frame="world",
    pose=Pose(
        x=500, y=0, z=200,
        o_x=0, o_y=0, o_z=-1, theta=0
    )
)

await motion_service.move(
    component_name="my-arm",
    destination=retreat_pose,
    world_state=world_state
)
print("Retreated from placement")
```

{{% /tab %}}
{{< /tabs >}}

## Tips

- Use `OrientationConstraint` during descent to keep the object level.
- The retreat path should go straight up to avoid disturbing the placed object.
- After releasing, the object becomes a potential obstacle. Update your
  `WorldState` if the arm needs to move near the placement location again.

## What's next

- [Pick an Object](/motion-planning/motion-how-to/pick-an-object/):
  the pick half of the pick-and-place workflow.
- [Monitor a running plan](/motion-planning/motion-how-to/monitor-a-running-plan/):
  track plan status during execution.
