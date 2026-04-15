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

You need the arm to move in a controlled way, such as following a straight line for
welding, keeping the end effector level to carry a cup of water, or both. Without
constraints, the planner finds any collision-free path, which may curve or tilt
the end effector unpredictably.

## Prerequisites

- A running machine with an arm and [frame system](/motion-planning/frame-system/) configured
- Familiarity with [Move Arm to Pose](/motion-planning/motion-how-to/move-arm-to-pose/)

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

You can apply both linear and orientation constraints simultaneously.

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

- **Start with larger tolerances** (10-20 mm, 10-15 degrees) and tighten
  only as needed. Tight constraints increase planning time and failure rate.
- **Constraints combine with obstacles.** If obstacles block the straight-line
  path, the planner may fail because it cannot satisfy both the linear
  constraint and the obstacle avoidance requirement.
- **Orientation constraints check against both start and goal.** The planner
  ensures the current orientation stays within tolerance of whichever endpoint
  is closer.

## What's next

- [Configure Motion Constraints](/motion-planning/constraints/):
  full reference for all four constraint types.
- [Plan Collision-Free Paths](/motion-planning/motion-how-to/avoid-obstacles/):
  combine constraints with obstacle avoidance.
