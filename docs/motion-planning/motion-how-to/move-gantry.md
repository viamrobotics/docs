---
linkTitle: "Move a Gantry"
title: "Move a Gantry"
weight: 40
layout: "docs"
type: "docs"
description: "Control gantry axes directly or plan complex gantry motion."
aliases:
  - /operate/mobility/move-gantry/
---

You have a gantry (a Cartesian robot with linear axes) and need to move it to
specific positions. You can either control axes directly with the gantry API
or use the motion service for planned, collision-aware movement.

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

# Move to a specific position
await gantry.move_to_position(positions=[200, 300, 100])
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import "go.viam.com/rdk/components/gantry"

myGantry, err := gantry.FromRobot(machine, "my-gantry")
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

err = myGantry.MoveToPosition(ctx, []float64{200, 300, 100}, nil)
if err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

## Motion-planned movement

For complex paths or collision avoidance, use the motion service.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient
from viam.proto.common import PoseInFrame, Pose, ResourceName

motion_service = MotionClient.from_robot(machine, "builtin")

gantry_name = ResourceName(
    namespace="rdk", type="component",
    subtype="gantry", name="my-gantry"
)

destination = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=200, y=300, z=100, o_x=0, o_y=0, o_z=1, theta=0)
)

await motion_service.move(
    component_name=gantry_name,
    destination=destination,
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
gantryName := resource.Name{
    API:  resource.NewAPI("rdk", "component", "gantry"),
    Name: "my-gantry",
}

destination := referenceframe.NewPoseInFrame("world",
    spatialmath.NewPose(
        r3.Vector{X: 200, Y: 300, Z: 100},
        &spatialmath.OrientationVectorDegrees{OX: 0, OY: 0, OZ: 1, Theta: 0},
    ))

_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: gantryName,
    Destination:   destination,
})
```

{{% /tab %}}
{{< /tabs >}}

## What's Next

- [Move Arm to Pose](/motion-planning/motion-how-to/move-arm-to-pose/):
  similar workflow for robot arms.
- [Define Obstacles](/motion-planning/obstacles/):
  add obstacle geometry for collision avoidance.
