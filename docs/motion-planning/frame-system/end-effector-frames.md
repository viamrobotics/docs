---
linkTitle: "End effector frames"
title: "End effector frames"
weight: 5
layout: "docs"
type: "docs"
description: "How Move places a named frame at a target pose, and how the frame attribute and WorldState transforms set which point on the robot a frame represents."
---

When you move an arm with the motion service, you move a _frame_. The
destination you pass is a pose for a named frame in the frame system, and the
planner solves for joint angles that place that frame's origin at the
destination. The frame you name decides whether the tool tip lands on the target
or the arm's mounting flange lands there instead.

This page explains how `Move` resolves a component name to a frame, how the
`frame` attribute defines an end effector frame, and how a `WorldState`
transform lets you add or reposition that frame for a single request.

## Which frame Move acts on

The `Move` request takes a component name and a destination. The component name
resolves to a frame in the frame system. The planner then searches for an arm
configuration that brings that frame's origin to the destination pose.

```python
await motion_service.move(
    component_name="my-gripper",
    destination=destination,
)
```

Passing `"my-gripper"` here moves the gripper's frame, so the destination
describes where the gripper should end up. Passing `"my-arm"` instead moves the
arm's frame, which sits at the arm's mounting flange. The two are different
physical points, so the same destination pose produces different motions. Name
the frame whose position you actually care about.

This is why motion is expressed in terms of frames: a single arm carries many
frames worth targeting (the flange, a gripper's tool center point, a wrist
camera), and the planner needs to know which one you mean.

## Define an end effector frame with the frame attribute

A component's frame is defined through its `frame` attribute, the same
parent, translation, and orientation you configure for any component. For an
end effector, the translation is what moves the frame origin from the arm's
flange out to the working point.

A gripper whose tool center point sits 120 mm past the flange uses a frame like
this:

```json
{
  "parent": "my-arm",
  "translation": { "x": 0, "y": 0, "z": 120 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

With this frame configured, calling `Move` with `component_name="my-gripper"`
positions the point 120 mm past the flange at the destination. Without it, the
planner has no model of the tool's length and positions the flange instead, so
the physical tool overshoots the target by 120 mm. For a worked example with an
arm, gripper, and camera, see
[Arm with gripper and wrist camera](/motion-planning/frame-system/arm-gripper-camera/).

## How the frame system maintains frames

The frame system stores every configured frame in a single tree rooted at the
world frame, and recomputes each frame's pose as the arm's joints move. Because
the gripper frame is a child of the arm, it tracks the flange automatically:
when the arm moves, the gripper's tool center point moves with it, and the
planner reasons about the tool's position at every step of a candidate path.

This tree is built from your saved configuration. To target a frame absent from
the saved configuration, or to shift an existing one for a single motion, you
extend the tree at request time with a transform.

## Extend the frame system with a WorldState transform

`WorldState` carries supplementary transforms alongside obstacles. A transform
adds a frame to the frame system for the duration of one request, without
editing the saved configuration. You give the new frame a name, a parent frame
to attach to, and an offset pose relative to that parent.

Attaching a transform as a child of the end effector creates a new frame offset
from it. This is how you reposition the point the planner aims for: define a
frame at the tip of a held object or at an offset from the gripper, then target
that frame in the destination.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import (
    Transform, PoseInFrame, Pose, WorldState
)

# A frame named "object-tip" 80mm beyond the gripper, attached to the gripper.
object_tip = Transform(
    reference_frame="object-tip",
    pose_in_observer_frame=PoseInFrame(
        reference_frame="my-gripper",
        pose=Pose(x=0, y=0, z=80, o_x=0, o_y=0, o_z=1, theta=0),
    ),
)

world_state = WorldState(transforms=[object_tip])

# Now Move can target "object-tip" as the frame to place at the destination.
await motion_service.move(
    component_name="object-tip",
    destination=destination,
    world_state=world_state,
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// A frame named "object-tip" 80mm beyond the gripper, attached to the gripper.
objectTip := referenceframe.NewLinkInFrame(
    "my-gripper",
    spatialmath.NewPoseFromPoint(r3.Vector{X: 0, Y: 0, Z: 80}),
    "object-tip",
    nil,
)

worldState, err := referenceframe.NewWorldState(
    nil, []*referenceframe.LinkInFrame{objectTip})
if err != nil {
    logger.Fatal(err)
}

// Now Move can target "object-tip" as the frame to place at the destination.
_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "object-tip",
    Destination:   destination,
    WorldState:    worldState,
})
```

{{% /tab %}}
{{< /tabs >}}

Because the transform is a child of `my-gripper`, the new frame moves with the
gripper, and the planner places `object-tip` rather than the gripper's own
origin at the destination. When the request finishes, the frame disappears: the
saved frame system is unchanged.

## WorldState versus the world state store service

The names are similar, but `WorldState` and the world state store service are
different things, and only one affects a `Move`.

- `WorldState` is the argument you pass to a single `Move` call. The obstacles
  and transforms in it exist only for that request: the planner uses them to
  plan this motion, and they are gone when the call returns. The transform in
  the previous section is a `WorldState` transform, so it shapes the plan.
- The world state store service is a separate service that holds transforms for
  client-side visualization in the [3D scene](/motion-planning/3d-scene/). The
  motion planner reads only the `WorldState` you pass to `Move`, so a transform
  published to the store renders in the scene while planning stays driven by
  `WorldState` alone.

To change where the arm goes, put the transform in the `WorldState` you pass to
`Move`, as shown above. To render a custom visual without affecting planning,
publish it to the world state store service instead.

## What's next

- [Frame system overview](/motion-planning/frame-system/overview/):
  configure parent, translation, orientation, and geometry for every component.
- [Arm with gripper and wrist camera](/motion-planning/frame-system/arm-gripper-camera/):
  a worked end effector configuration.
- [Move an arm to a pose](/motion-planning/move-an-arm/move-to-pose/):
  target a frame with the motion service.
- [Attach and detach geometries](/motion-planning/obstacles/attach-detach-geometries/):
  carry a grasped object's geometry with the end effector.
