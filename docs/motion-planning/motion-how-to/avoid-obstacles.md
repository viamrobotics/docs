---
linkTitle: "Avoid obstacles"
title: "Plan collision-free paths"
weight: 30
layout: "docs"
type: "docs"
description: "Configure obstacles and plan motion paths that avoid collisions."
---

Your arm needs to reach a target while avoiding the table it's mounted on,
walls, equipment, or objects placed in the workspace. This guide shows how to
set up a complete obstacle environment and verify collision avoidance.

## Prerequisites

- [Frame system](/motion-planning/frame-system/) configured
- [Obstacles concept](/motion-planning/obstacles/) understood

## Steps

### 1. Define your workspace obstacles

Build a `WorldState` that models the significant obstacles in your workspace.

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

### 3. Test collision avoidance

Place a test obstacle directly between the arm and the target. The arm should
take an indirect path around it.

Then remove the obstacle and move again. The arm should take a more direct path.

### 4. Add static geometry to frames

For permanent obstacles, add geometry directly to component frames in the
**CONFIGURE** tab instead of using WorldState. This way the planner always
accounts for them without code changes.

See [Define Obstacles](/motion-planning/obstacles/) for the full configuration
reference.

## What's next

- [Move an Arm to a Target Pose](/motion-planning/motion-how-to/move-arm-to-pose/)
- [Pick an Object](/motion-planning/motion-how-to/pick-an-object/)
