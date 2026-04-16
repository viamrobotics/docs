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

Placing is the mirror image of picking, but with a different failure mode:
releasing the object is the moment you lose control of it. A placement that
lets go too early drops the object; one that descends too far jams it into
the surface. This guide walks through a four-step placement that controls
those two failure modes: move to a pre-place pose, descend to the placement
surface, release, and retreat straight up so you do not disturb what you
just set down.

## Prerequisites

- Object already grasped (see [Pick an object](/motion-planning/pick-and-place/pick-an-object/)).
- Placement location known in world coordinates.

The code below continues from [Pick an object](/motion-planning/pick-and-place/pick-an-object/);
`motion_service`, `gripper`, and `world_state` are already defined in that script.

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

### 2. Descend to the placement surface

The descent pose puts the object where you want it to end up.
`SURFACE_HEIGHT` is the world-frame z of the placement surface plus half the
object's height (roughly: you want the bottom of the object touching the
surface at release). For a known surface, measure once and hard-code it. For
a detected surface, set it from the vision result.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Place: at the surface.
# Set z to the height of the placement surface in your workspace.
# For example, if you detected the target location, use its z coordinate.
SURFACE_HEIGHT = 50  # mm: world-frame z of the surface plus half the object's height
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

- **Keep the object level on the way down.** A carried object with an open
  top (a cup, an open box) spills if the gripper tilts during descent. Add an
  [`OrientationConstraint`](/motion-planning/move-an-arm/constraints/),
  which locks the end effector's tilt, with a tolerance of 3 to 5 degrees
  for the descent segment; remove it for the retreat.
- **Retreat straight up.** Any lateral motion during retreat can catch the
  object the gripper just released. Plan the retreat pose with the same x
  and y as the place pose and only the z raised.
- **Update `WorldState` after release.** The placed object is now a static
  obstacle. If the next motion passes near the placement location, add a
  `Geometry` matching the placed object to `WorldState.obstacles` so the
  planner routes around it.

## What's next

- [Pick an object](/motion-planning/pick-and-place/pick-an-object/):
  the pick half of the pick-and-place workflow.
- [Monitor a running plan](/motion-planning/monitor-a-running-plan/):
  track plan status during execution.
