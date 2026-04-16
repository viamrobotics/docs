---
linkTitle: "Allow frame collisions"
title: "Allow specific frames to collide"
weight: 40
layout: "docs"
type: "docs"
description: "Permit specific pairs of frames to collide so the motion planner stops flagging expected contact as a collision failure."
aliases:
  - /motion-planning/motion-how-to/allow-frame-collisions/
---

Some contact is part of the job. A gripper has to touch the object it grasps.
A vision-based obstacle detector mounted on an arm will see the arm as an
obstacle. Two adjacent links in a simplified kinematic model may register as
overlapping even though the real hardware does not. In each of these cases,
the motion planner's default rejection of any frame-on-frame contact blocks
plans that should succeed.

`CollisionSpecification` tells the planner which pairs of frames are allowed
to touch. Use it to unblock planning for contact you have already accounted
for elsewhere.

## Before you start

- A configured arm (or other frame-producing component) and a working
  motion service.
- You know which frames are being flagged. Plan failures that mention
  "collision detected" include the frame names; read them carefully.
- For the arm-detects-itself case, a camera that produces obstacle
  detections (a vision service + camera pair).
- If you are migrating from MoveIt's self-filter or body padding
  mechanism, `CollisionSpecification` is Viam's equivalent.

## The basic pattern

A `CollisionSpecification` is a list of allowed frame pairs; you build one,
wrap it in a `Constraints` object, and pass it to `Move`. Everything else on
this page is either specific use cases for this pattern or troubleshooting
when a frame name does not match.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient
from viam.proto.service.motion import Constraints, CollisionSpecification
from viam.proto.common import PoseInFrame, Pose

motion_service = MotionClient.from_robot(machine, "builtin")

# Allow the gripper to contact the object it is picking up.
collision_spec = CollisionSpecification(
    allows=[
        CollisionSpecification.AllowedFrameCollisions(
            frame1="my-gripper",
            frame2="target-object",
        ),
    ],
)

constraints = Constraints(collision_specification=[collision_spec])

destination = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=300, y=200, z=400, o_x=0, o_y=0, o_z=-1, theta=0),
)

await motion_service.move(
    component_name="my-arm",
    destination=destination,
    constraints=constraints,
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "go.viam.com/rdk/motionplan"
    "go.viam.com/rdk/services/motion"
)

// Allow the gripper to contact the object it is picking up.
constraints := &motionplan.Constraints{
    CollisionSpecification: []motionplan.CollisionSpecification{
        {
            Allows: []motionplan.CollisionSpecificationAllowedFrameCollisions{
                {Frame1: "my-gripper", Frame2: "target-object"},
            },
        },
    },
}

_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "my-arm",
    Destination:   destination,
    Constraints:   constraints,
})
```

{{% /tab %}}
{{< /tabs >}}

The planner still checks every other pair of frames for collisions.
Listing one pair in `CollisionSpecification` does not disable collision
checking in general.

## Hierarchical matching

Frame names in `AllowedFrameCollisions` match hierarchically. Naming `my-arm`
covers every link in the arm's kinematics (`my-arm:base_link`,
`my-arm:upper_arm_link`, `my-arm:forearm_link`, and so on) plus any origin
geometry you configured. Naming `my-arm:upper_arm_link` covers only that one
link.

- `frame1 = "my-arm"` matches every link of `my-arm`: `my-arm:base_link`,
  `my-arm:upper_arm_link`, `my-arm:forearm_link`, and so on.
- `frame1 = "my-arm:upper_arm_link"` matches only the upper arm link.
- Names that do not match any known geometry produce an error that lists
  the available geometry names, which is often the fastest way to find
  the right name.

For most allow-list use cases, the parent component name (`"my-arm"`,
`"my-gripper"`) is what you want. Use a specific link name only when you
know the exact sub-frame and other sub-frames must continue to be
collision-checked.

Passing the same name for both `frame1` and `frame2` (for example
`AllowedFrameCollisions(frame1="my-arm", frame2="my-arm")`) disables all
self-collision checks within that component: every link is whitelisted
against every other link. Use this when the kinematic model reports
false self-collisions between adjacent links but the arm is mechanically
safe.

## Use case: arm detects itself through a vision service

The single most common reason to reach for `CollisionSpecification`: an
arm with an onboard or overhead camera feeds a vision service that
reports 3D obstacles, and the arm appears in the camera's view. The
obstacle detection sees the arm as an obstacle, the planner sees the arm
colliding with itself, and motion halts.

1. Look at the plan failure. The collision pair will include your arm's
   frame and a vision-detected obstacle frame (usually named after the
   detector, for example `my-vision:detection-0`).
2. Add a `CollisionSpecification` that allows the arm to collide with
   the detection frames. In practice, this usually means allowing the
   arm to collide with anything the camera detects:

{{< tabs >}}
{{% tab name="Python" %}}

```python
collision_spec = CollisionSpecification(
    allows=[
        CollisionSpecification.AllowedFrameCollisions(
            frame1="my-arm",
            frame2="my-vision",
        ),
    ],
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
constraints := &motionplan.Constraints{
    CollisionSpecification: []motionplan.CollisionSpecification{
        {
            Allows: []motionplan.CollisionSpecificationAllowedFrameCollisions{
                {Frame1: "my-arm", Frame2: "my-vision"},
            },
        },
    },
}
```

{{% /tab %}}
{{< /tabs >}}

3. Re-run the motion. If the arm still fails on a real obstacle the
   camera reported, the collision was legitimate, and you need to
   address the motion target or obstacle geometry rather than expanding
   the allow list.

This is Viam's equivalent of MoveIt's self-filter or body padding.
Instead of filtering camera data, you tell the planner that specific
overlaps are expected.

## Use case: gripper grasping an object

A grasp _requires_ contact between the gripper and the object. Without a
`CollisionSpecification` allowing it, the planner rejects the final approach
as a collision. Allow the gripper-object pair and the plan completes.

```python
collision_spec = CollisionSpecification(
    allows=[
        CollisionSpecification.AllowedFrameCollisions(
            frame1="my-gripper",
            frame2="target-object",
        ),
    ],
)
```

After the grasp, if you want to move the gripper plus its held object
as one unit, attach the object to the gripper frame system through
`WorldState.transforms` on subsequent Move requests. See
[Attach and detach geometries](/motion-planning/obstacles/attach-detach-geometries/)
for the runtime-attach/detach pattern and
[Define obstacles: passive objects attached to a component](/motion-planning/obstacles/#passive-objects-attached-to-a-component)
for the permanent-attachment pattern.

## Use case: adjacent arm links whose geometries overlap

Some kinematic models have simplified collision geometry that causes
adjacent links to register as colliding in certain joint configurations,
even though the real hardware does not. If you are sure the overlap is
a modeling artifact and not a real collision:

```python
collision_spec = CollisionSpecification(
    allows=[
        CollisionSpecification.AllowedFrameCollisions(
            frame1="my-arm:upper_arm_link",
            frame2="my-arm:forearm_link",
        ),
    ],
)
```

Be conservative here. Self-collision errors are often legitimate and
silencing them can mask real hardware problems.

## Verify the change

1. Plan the motion that was failing. It should succeed.
2. Plan a motion you expect to fail for other reasons (target inside an
   unrelated obstacle, target outside reach). The planner should still
   reject those.
3. Visually confirm the motion in the **3D SCENE** tab before running on
   hardware. See
   [Debug a motion plan](/motion-planning/3d-scene/debug-motion-plan/).

## Troubleshooting

{{< expand "The planner still fails with a collision error" >}}

- The collision pair may involve different frames than the ones you
  allowed. Read the error message carefully and check both frame names
  against your `CollisionSpecification`.
- Sub-geometry names include the component name as a prefix with a
  colon, for example `my-arm:upper_arm_link`. Unprefixed names do not
  match.

{{< /expand >}}

{{< expand "Error: geometry specification allow name does not match any known geometries" >}}

The error message lists the available geometry names. Copy the exact
name from that list into your `CollisionSpecification`. Common causes:

- Typos in the component name.
- A component you configured does not have collision geometry (the arm
  has no kinematics file or the component has no `geometry` field in
  its frame config).
- The arm module did not export the link names you expected.

{{< /expand >}}

{{< expand "Allowed collisions are silencing real problems" >}}

If you find yourself adding entries to `CollisionSpecification` to get
a plan to succeed, stop and check whether the geometry itself is wrong.
Oversized obstacle geometries or geometry positioned incorrectly in the
frame system frequently masquerade as collision errors. Fixing the
geometry is usually the right answer.

{{< /expand >}}

## What's next

- [Configure motion constraints](/motion-planning/move-an-arm/constraints/): the
  other three constraint types (Linear, Orientation, Pseudolinear).
- [Define obstacles](/motion-planning/obstacles/): the obstacle geometry
  that the planner checks against.
- [Debug a motion plan](/motion-planning/3d-scene/debug-motion-plan/):
  visualize frame overlaps in the **3D SCENE** tab.
