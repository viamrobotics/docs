---
linkTitle: "Move with constraints"
title: "Move an arm with motion constraints"
weight: 20
layout: "docs"
type: "docs"
description: "Move an arm along a straight line or with a fixed orientation using motion constraints."
aliases:
  - /tutorials/services/constrain-motion/
  - /motion-planning/motion-how-to/move-arm-with-constraints/
---

Welding requires the torch to follow a straight line. Carrying a cup of water
requires the end effector to stay level. The motion planner's default behavior
satisfies neither: it finds any collision-free path, which typically curves
through intermediate poses and tilts the end effector along the way.
`Constraints` let you bound what the planner will accept.

## Prerequisites

- A running machine with an arm and [frame system](/motion-planning/frame-system/) configured
- Familiarity with [Move Arm to Pose](/motion-planning/move-an-arm/move-to-pose/)

## Steps

### 1. Move in a straight line

Use a `LinearConstraint` to keep the end effector within a tolerance of the
direct line between start and goal.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient
from viam.proto.service.motion import Constraints, LinearConstraint
from viam.proto.common import PoseInFrame, Pose

motion_service = MotionClient.from_robot(machine, "builtin")

constraints = Constraints(
    linear_constraint=[
        LinearConstraint(line_tolerance_mm=5.0)
    ]
)

destination = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=400, y=200, z=300, o_x=0, o_y=0, o_z=-1, theta=0)
)

await motion_service.move(
    component_name="my-arm",
    destination=destination,
    constraints=constraints
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import "go.viam.com/rdk/motionplan"

constraints := &motionplan.Constraints{
    LinearConstraint: []motionplan.LinearConstraint{
        {LineToleranceMm: 5.0},
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

### 2. Maintain end effector orientation

Use an `OrientationConstraint` to keep the end effector level (or at any
fixed orientation) throughout the motion.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.service.motion import OrientationConstraint

constraints = Constraints(
    orientation_constraint=[
        OrientationConstraint(orientation_tolerance_degs=5.0)
    ]
)

await motion_service.move(
    component_name="my-arm",
    destination=destination,
    constraints=constraints
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
constraints := &motionplan.Constraints{
    OrientationConstraint: []motionplan.OrientationConstraint{
        {OrientationToleranceDegs: 5.0},
    },
}
```

{{% /tab %}}
{{< /tabs >}}

### 3. Combine constraints

Linear and orientation constraints compose: pass both in the same `Constraints`
object and the planner enforces both simultaneously. This is the usual setup
for welding and other tasks that require a straight-line path plus a fixed tool
orientation.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Straight line, level orientation
constraints = Constraints(
    linear_constraint=[
        LinearConstraint(line_tolerance_mm=5.0)
    ],
    orientation_constraint=[
        OrientationConstraint(orientation_tolerance_degs=3.0)
    ]
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
constraints := &motionplan.Constraints{
    LinearConstraint: []motionplan.LinearConstraint{
        {LineToleranceMm: 5.0},
    },
    OrientationConstraint: []motionplan.OrientationConstraint{
        {OrientationToleranceDegs: 3.0},
    },
}
```

{{% /tab %}}
{{< /tabs >}}

### 4. Use proportional tolerances

`PseudolinearConstraint` scales the tolerance with the motion distance. Useful
when the same code handles both short and long moves.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.service.motion import PseudolinearConstraint

constraints = Constraints(
    pseudolinear_constraint=[
        PseudolinearConstraint(
            line_tolerance_factor=0.1,
            orientation_tolerance_factor=0.1
        )
    ]
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
constraints := &motionplan.Constraints{
    PseudolinearConstraint: []motionplan.PseudolinearConstraint{
        {
            LineToleranceFactor:        0.1,
            OrientationToleranceFactor: 0.1,
        },
    },
}
```

{{% /tab %}}
{{< /tabs >}}

## Tips

- **Start with loose tolerances, tighten only if the task requires it.** 10-20
  mm and 10-15 degrees is a reasonable starting point. Tight tolerances raise
  both planning time and failure rate.
- **Constraints and obstacles compete.** If an obstacle blocks the
  straight-line path, the planner has to pick one constraint to violate and
  typically fails. Either widen the constraint or move the obstacle.
- **Orientation is checked against the nearer endpoint.** The planner compares
  the current orientation to the start and goal, then uses whichever is closer
  as the reference. This lets the constraint track intent as the motion
  progresses rather than locking to one endpoint.

## What's next

- [Configure Motion Constraints](/motion-planning/move-an-arm/constraints/):
  full reference for all four constraint types.
- [Plan Collision-Free Paths](/motion-planning/obstacles/avoid-obstacles/):
  combine constraints with obstacle avoidance.
