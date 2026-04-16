---
linkTitle: "Avoid obstacles"
title: "Plan collision-free paths"
weight: 20
layout: "docs"
type: "docs"
description: "Configure obstacles and plan motion paths that avoid collisions."
aliases:
  - /motion-planning/motion-how-to/avoid-obstacles/
---

A motion plan that ignores the table, the back wall, and the fixture on the
bench next to the arm will collide on its way to the target. The motion service
can plan around these obstacles, but only if you describe them in a
`WorldState`. This guide walks through building a `WorldState` for a typical
bench setup, running a plan against it, and verifying that the planner actually
routes around each obstacle.

This page covers dynamic `WorldState` obstacles passed at call time. For
permanent fixtures (the table the arm is bolted to, the back wall, a
mounted tool), configure the obstacle in the component's frame
configuration once instead of re-sending it on every `Move`. See
[Define obstacles](/motion-planning/obstacles/).

## Prerequisites

- An arm or gantry configured on a machine.
- [Frame system](/motion-planning/frame-system/) configured.
- [Obstacles concept](/motion-planning/obstacles/) understood.

## Steps

### 1. Describe your workspace obstacles

A `WorldState` is a list of geometries expressed in a reference frame. Each
geometry needs a shape (box, capsule, or sphere), a pose relative to the frame,
and a label. Model every significant obstacle: surfaces the arm can press into,
fixtures it can strike, and vertical obstructions like posts or walls.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import (
    Pose, Vector3, RectangularPrism, Capsule,
    Geometry, GeometriesInFrame, WorldState
)

# Table
table = Geometry(
    center=Pose(x=0, y=0, z=-20),
    box=RectangularPrism(dims_mm=Vector3(x=800, y=600, z=40)),
    label="table"
)

# Back wall
wall = Geometry(
    center=Pose(x=0, y=400, z=500),
    box=RectangularPrism(dims_mm=Vector3(x=1200, y=20, z=1000)),
    label="back-wall"
)

# Support post
post = Geometry(
    center=Pose(x=300, y=0, z=200),
    capsule=Capsule(radius_mm=25, length_mm=400),
    label="support-post"
)

obstacles = GeometriesInFrame(
    reference_frame="world",
    geometries=[table, wall, post]
)
world_state = WorldState(obstacles=[obstacles])
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
obstacles := make([]spatialmath.Geometry, 0)

table, _ := spatialmath.NewBox(
    spatialmath.NewPose(r3.Vector{X: 0, Y: 0, Z: -20},
        &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: 1, Theta: 0}),
    r3.Vector{X: 800, Y: 600, Z: 40}, "table")
obstacles = append(obstacles, table)

wall, _ := spatialmath.NewBox(
    spatialmath.NewPose(r3.Vector{X: 0, Y: 400, Z: 500},
        &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: 1, Theta: 0}),
    r3.Vector{X: 1200, Y: 20, Z: 1000}, "back-wall")
obstacles = append(obstacles, wall)

post, _ := spatialmath.NewCapsule(
    spatialmath.NewPose(r3.Vector{X: 300, Y: 0, Z: 200},
        &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: 1, Theta: 0}),
    25, 400, "support-post")
obstacles = append(obstacles, post)

obstaclesInFrame := referenceframe.NewGeometriesInFrame(
    referenceframe.World, obstacles)
worldState, _ := referenceframe.NewWorldState(
    []*referenceframe.GeometriesInFrame{obstaclesInFrame}, nil)
```

{{% /tab %}}
{{< /tabs >}}

### 2. Move with obstacle avoidance

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient
from viam.proto.common import PoseInFrame, Pose

motion_service = MotionClient.from_robot(machine, "builtin")

destination = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=300, y=200, z=400, o_x=0, o_y=0, o_z=-1, theta=0)
)

await motion_service.move(
    component_name="my-arm",
    destination=destination,
    world_state=world_state
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "my-arm",
    Destination:   destination,
    WorldState:    worldState,
})
```

{{% /tab %}}
{{< /tabs >}}

### 3. Verify the planner is actually routing around obstacles

You need a concrete test that proves `WorldState` reached the planner.
A before-and-after with an obstacle placed between start and target works:
run the motion with a box placed directly between the arm's start pose
and the target, and the arm should take an indirect path around it.
Remove the box, rerun the same motion, and the arm should take a more
direct path. If the paths look the same with and without the obstacle,
the `WorldState` is not reaching the planner.

## What's next

- [Move an arm to a target pose](/motion-planning/move-an-arm/move-to-pose/)
- [Pick an object](/motion-planning/pick-and-place/pick-an-object/)
- [Allow frame collisions](/motion-planning/obstacles/allow-frame-collisions/) — when the planner rejects expected contact
