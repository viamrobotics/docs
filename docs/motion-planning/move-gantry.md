---
linkTitle: "Move a gantry"
title: "Move a gantry"
weight: 70
layout: "docs"
type: "docs"
description: "Control gantry axes directly or plan complex gantry motion."
aliases:
  - /operate/mobility/move-gantry/
  - /motion-planning/motion-how-to/move-gantry/
---

A gantry is a Cartesian robot: three linear axes, no joint-angle to pose
conversion to do. Most gantry motion is a direct axis command and nothing
more. But if the gantry shares its workspace with obstacles, carries a payload
that must avoid something, or moves alongside another machine, the motion
service plans a collision-aware path the same way it does for an arm. This
guide covers both.

## Direct axis control

Use the gantry component API for simple, direct movements.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.gantry import Gantry

gantry = Gantry.from_robot(machine, "my-gantry")

# Read current position (mm for each axis)
positions = await gantry.get_position()
print(f"Current positions: {positions}")

# Read axis lengths
lengths = await gantry.get_lengths()
print(f"Axis lengths: {lengths}")

# Move to a specific position (speeds are required, one per axis, in mm/s)
await gantry.move_to_position(
    positions=[200, 300, 100],
    speeds=[100, 100, 100],
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import "go.viam.com/rdk/components/gantry"

myGantry, err := gantry.FromProvider(machine, "my-gantry")
if err != nil {
    logger.Fatal(err)
}

positions, err := myGantry.Position(ctx, nil)
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Current positions: %v\n", positions)

lengths, err := myGantry.Lengths(ctx, nil)
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Axis lengths: %v\n", lengths)

// Speeds are required, one per axis, in mm/s.
err = myGantry.MoveToPosition(
    ctx,
    []float64{200, 300, 100},
    []float64{100, 100, 100},
    nil,
)
if err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

## Motion-service planning

The motion service treats a gantry the same way it treats an arm: you pass a
target pose and a `WorldState`, and it returns a collision-free path. Use it
when the gantry has obstacles to avoid, when you want to compose a gantry move
with other components, or when you want the same planning API across every
machine in your fleet.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient
from viam.proto.common import PoseInFrame, Pose

motion_service = MotionClient.from_robot(machine, "builtin")

destination = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=200, y=300, z=100, o_x=0, o_y=0, o_z=1, theta=0)
)

await motion_service.move(
    component_name="my-gantry",
    destination=destination,
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
destination := referenceframe.NewPoseInFrame("world",
    spatialmath.NewPose(
        r3.Vector{X: 200, Y: 300, Z: 100},
        &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: 1, Theta: 0},
    ))

_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "my-gantry",
    Destination:   destination,
})
```

{{% /tab %}}
{{< /tabs >}}

## What's next

- [Move Arm to Pose](/motion-planning/move-an-arm/move-to-pose/):
  similar workflow for robot arms.
- [Define Obstacles](/motion-planning/obstacles/):
  add obstacle geometry for collision avoidance.
