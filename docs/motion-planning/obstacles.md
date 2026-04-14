---
linkTitle: "Obstacles"
title: "Define obstacles"
weight: 30
layout: "docs"
type: "docs"
description: "Define collision geometry so the motion planner computes safe, collision-free paths."
aliases:
  - /work-cell-layout/define-obstacles/
  - /build/work-cell-layout/define-obstacles/
  - /operate/mobility/define-obstacles/
  - /operate/mobility/define-dynamic-obstacles/
  - /operate/mobility/define-geometry/
  - /operate/mobility/move-arm/configure-additional/
  - /services/frame-system/nested-frame-config/
  - /mobility/frame-system/nested-frame-config/
  - /reference/services/frame-system/nested-frame-config/
---

A robot arm that does not know about its surroundings will plan the shortest path
to a target position, even if that path goes through a table, a wall, or another
piece of equipment. Without obstacle definitions, the motion planner has no way
to know that certain regions of space are occupied by physical objects.

By defining obstacles (tables, walls, posts, equipment, and other fixtures in
your workspace) you give the motion planner the information it needs to plan
collision-free paths. The planner routes the arm around obstacles, and if no
collision-free path exists, it returns an error rather than commanding a
dangerous motion.

## Concepts

### Geometry types

Viam supports five geometry types for defining obstacles. The three primitives
are the most commonly used:

| Type        | JSON `type` | Config fields                          | Best for                                      |
| ----------- | ----------- | -------------------------------------- | --------------------------------------------- |
| **Box**     | `"box"`     | `x`, `y`, `z` (dimensions in mm)       | Tables, walls, shelves, rectangular equipment |
| **Sphere**  | `"sphere"`  | `r` (radius in mm)                     | Balls, rounded objects, keep-out zones        |
| **Capsule** | `"capsule"` | `r` (radius in mm), `l` (length in mm) | Posts, pipes, cylindrical objects             |
| **Point**   | `"point"`   | (none, position only)                  | Single points in space                        |
| **Mesh**    | `"mesh"`    | `mesh_data`, `mesh_content_type`       | Complex shapes from STL/PLY files             |

Each geometry has a center point (pose) that defines where it sits in space. The
pose is relative to a reference frame, typically the world frame. Geometry
configs also support `translation` and `orientation` offsets to shift the shape
relative to the frame origin.

You do not need to model every surface detail of an obstacle. Approximate shapes
that fully enclose the real object are safer and work better with the motion
planner.

Capsule validation: the length must be at least twice the radius. If length
equals exactly twice the radius, Viam creates a sphere instead.

### Static vs dynamic obstacles

**Static obstacles** are permanent fixtures in your workspace. You configure
them by adding geometry to a component's frame configuration in the Viam app.
They are always present and do not require code changes. Examples: the table
the arm is mounted on, walls, permanent fixtures.

**Dynamic obstacles** are objects that you define at runtime and pass to the
motion service through WorldState. They can change between calls. Examples: a box
that was just placed on the table, a temporary keep-out zone, objects detected
by a vision system.

Both types use the same geometry primitives.

### WorldState

WorldState is the container that holds obstacle and transform information passed
to the motion service at call time. It contains:

- **obstacles**: a list of `GeometriesInFrame`, where each entry specifies a
  reference frame and one or more geometries in that frame
- **transforms**: supplemental frame transforms that augment the frame system
  for this call only

You construct a WorldState in your code and pass it to the `Move` call.

### Keep-out zones

A keep-out zone is a region of space where the robot should never enter. Define
it the same way as any other obstacle, as a box, sphere, or capsule positioned
in the workspace. The motion planner treats it identically to a physical
obstacle.

### Collision buffer

The motion planner does not add clearance around obstacle geometries by
default. The built-in collision buffer is effectively zero (1e-8 mm, present
only to prevent numerical edge cases). To keep the robot clear of physical
obstacles, size your obstacle geometries to fully enclose the real object plus
any desired safety margin. 20 to 50 mm is a reasonable starting point for most
arms.

You can override the buffer on a per-call basis by passing
`collision_buffer_mm` in the `extra` map on a Move request. This adds the
specified clearance in millimeters to every collision check for that call.

## Steps

### 1. Add geometry to a component frame

For permanent fixtures, add geometry directly to a component's frame
configuration.

**Example: a table under the arm.**

1. Go to [app.viam.com](https://app.viam.com) and navigate to your machine.
2. Click the **CONFIGURE** tab.
3. Add a new component to represent the table obstacle (or add the geometry to
   an existing component's frame).
4. Configure the frame with a geometry:

```json
{
  "parent": "world",
  "translation": { "x": 0, "y": 0, "z": -20 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  },
  "geometry": {
    "type": "box",
    "x": 800,
    "y": 600,
    "z": 40
  }
}
```

This defines a table as a box 800 mm wide, 600 mm deep, and 40 mm thick. The
center of the box is at z = -20 mm (20 mm below the world frame origin), so
the top surface of the 40 mm thick table aligns with z = 0.

Click **Save**. The table geometry is now part of the frame system and the
motion planner will avoid it automatically.

### 2. Define obstacles programmatically with WorldState

For obstacles that change at runtime, build a WorldState in your code.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import (
    Pose, Vector3, RectangularPrism, Capsule, Sphere,
    Geometry, GeometriesInFrame, WorldState
)

# Define a table as a box
table_origin = Pose(x=-202.5, y=-546.5, z=-19.0)
table_dims = Vector3(x=635.0, y=1271.0, z=38.0)
table_obstacle = Geometry(
    center=table_origin,
    box=RectangularPrism(dims_mm=table_dims),
    label="table"
)

# Define a post as a capsule
post_origin = Pose(x=200, y=0, z=150)
post_obstacle = Geometry(
    center=post_origin,
    capsule=Capsule(radius_mm=25, length_mm=300),
    label="post"
)

# Define a ball as a sphere
ball_origin = Pose(x=100, y=100, z=50)
ball_obstacle = Geometry(
    center=ball_origin,
    sphere=Sphere(radius_mm=40),
    label="ball"
)

# Combine into WorldState
obstacles_in_frame = GeometriesInFrame(
    reference_frame="world",
    geometries=[table_obstacle, post_obstacle, ball_obstacle]
)
world_state = WorldState(obstacles=[obstacles_in_frame])
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "github.com/golang/geo/r3"
    "go.viam.com/rdk/referenceframe"
    "go.viam.com/rdk/spatialmath"
)

obstacles := make([]spatialmath.Geometry, 0)

// Define a table as a box
tableOrigin := spatialmath.NewPose(
    r3.Vector{X: -202.5, Y: -546.5, Z: -19.0},
    &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: 1, Theta: 0},
)
tableDims := r3.Vector{X: 635.0, Y: 1271.0, Z: 38.0}
tableObj, err := spatialmath.NewBox(tableOrigin, tableDims, "table")
if err != nil {
    logger.Fatal(err)
}
obstacles = append(obstacles, tableObj)

// Define a post as a capsule
postOrigin := spatialmath.NewPose(
    r3.Vector{X: 200, Y: 0, Z: 150},
    &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: 1, Theta: 0},
)
postObj, err := spatialmath.NewCapsule(postOrigin, 25, 300, "post")
if err != nil {
    logger.Fatal(err)
}
obstacles = append(obstacles, postObj)

// Define a ball as a sphere
ballOrigin := spatialmath.NewPose(
    r3.Vector{X: 100, Y: 100, Z: 50},
    &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: 1, Theta: 0},
)
ballObj, err := spatialmath.NewSphere(ballOrigin, 40, "ball")
if err != nil {
    logger.Fatal(err)
}
obstacles = append(obstacles, ballObj)

// Combine into WorldState
obstaclesInFrame := referenceframe.NewGeometriesInFrame(
    referenceframe.World, obstacles)
worldState, err := referenceframe.NewWorldState(
    []*referenceframe.GeometriesInFrame{obstaclesInFrame}, nil)
if err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

### 3. Use WorldState with the motion service

Pass the WorldState to the motion service's `Move` method.

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

# Move with obstacle avoidance
await motion_service.move(
    component_name="my-arm",
    destination=destination,
    world_state=world_state
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "go.viam.com/rdk/services/motion"
)

motionService, err := motion.FromProvider(machine, "builtin")
if err != nil {
    logger.Fatal(err)
}

destination := referenceframe.NewPoseInFrame("world",
    spatialmath.NewPose(
        r3.Vector{X: 300, Y: 200, Z: 400},
        &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: -1, Theta: 0},
    ))

moveReq := motion.MoveReq{
    ComponentName: "my-arm",
    Destination:   destination,
    WorldState:    worldState,
}
_, err = motionService.Move(ctx, moveReq)
if err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

If the motion planner cannot find a collision-free path, it returns an error.
This typically means the obstacles are too restrictive, the destination is inside
an obstacle, or the arm physically cannot reach the destination without
colliding.

### 4. Visualize obstacles

Check the Viam app to see your obstacle geometry:

1. Navigate to your machine in the Viam app.
2. Click the **3D SCENE** tab.
3. Obstacles defined in component frame configurations appear as translucent
   shapes in the 3D view.

Dynamic obstacles (defined through WorldState in code) do not appear in the
3D SCENE tab because they only exist during the `Move` call.

## Try it

1. Add a table geometry to a component frame in the CONFIGURE tab (step 1).
   Open the 3D SCENE tab and verify the table appears.
2. Write code to define a dynamic obstacle using WorldState (step 2) and pass
   it to a `Move` call (step 3).
3. Place a test obstacle between the arm and a target position. Verify the arm
   takes an indirect path to avoid it.
4. Remove the test obstacle and move again. Verify the arm takes a more direct
   path.

## Troubleshooting

{{< expand "Motion planner cannot find a path" >}}

- The obstacles may be too large or too close together, leaving no valid path.
  Reduce obstacle dimensions slightly.
- The destination may be inside or very close to an obstacle.
- The motion planner does not add clearance by default. If paths come too
  close to obstacles, increase obstacle dimensions or pass a larger
  `collision_buffer_mm` value through the `extra` map on the Move request.

{{< /expand >}}

{{< expand "Obstacles appear in the wrong position" >}}

- Verify the reference frame. Positions are relative to the specified frame's
  origin.
- Check units. Positions are in millimeters, not centimeters or meters.
- Use the 3D SCENE tab to see where obstacles appear.

{{< /expand >}}

{{< expand "Arm clips through obstacles" >}}

- The obstacle geometry may be too small. Add a 20-50 mm safety margin.
- The arm's own collision geometry may be missing. Check the arm's kinematics
  file for link geometry definitions.
- Make thin obstacles (walls, panels) at least 20 mm thick.

{{< /expand >}}

## What's next

- [Move an Arm to a Target Pose](/motion-planning/motion-how-to/move-arm-to-pose/):
  use the motion service to move the arm while avoiding obstacles.
- [Configure Motion Constraints](/motion-planning/constraints/): restrict how
  the arm moves between poses.
- [How motion planning works](/motion-planning/how-planning-works/):
  understand how the planner computes collision-free paths.
