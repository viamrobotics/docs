---
linkTitle: "Constraints"
title: "Configure Motion Constraints"
weight: 40
layout: "docs"
type: "docs"
description: "Restrict how the arm moves between poses using linear, orientation, and collision constraints."
aliases:
  - /reference/services/motion/constraints/
  - /services/motion/constraints/
  - /mobility/motion/constraints/
---

By default, the motion planner finds any collision-free path from the current
pose to the target pose. The path may curve, twist, or take the end effector
through any orientation along the way. For many tasks this is fine, but some
tasks require the arm to move in a specific way:

- Carrying a cup of water requires the end effector to stay level.
- Welding a seam requires the tool to follow a straight line.
- Moving near obstacles may require relaxing collision checking between specific
  frame pairs.

Constraints let you specify these rules. The motion planner only returns paths
that satisfy all constraints.

## Constraint types

Viam supports four constraint types. You can combine multiple constraints in a
single motion request.

### LinearConstraint

Forces the end effector to stay close to a straight line between the start and
goal poses. Use this for straight-line tool paths.

| Parameter                    | Type             | Description                                                                                 |
| ---------------------------- | ---------------- | ------------------------------------------------------------------------------------------- |
| `line_tolerance_mm`          | float (optional) | Maximum deviation from the straight line, in millimeters. Only checked when greater than 0. |
| `orientation_tolerance_degs` | float (optional) | Maximum orientation deviation during motion, in degrees. Only checked when greater than 0.  |

When `line_tolerance_mm` is set, the planner checks that the end effector stays
within that distance of the line segment connecting start and goal positions.
When `orientation_tolerance_degs` is set, the planner checks that the end
effector orientation stays within that angular distance of either the start or
goal orientation.

### OrientationConstraint

Forces the end effector to maintain a consistent orientation throughout the
motion. Use this when the end effector must stay level or keep a fixed
orientation (for example, carrying a liquid).

| Parameter                    | Type             | Description                                                                  |
| ---------------------------- | ---------------- | ---------------------------------------------------------------------------- |
| `orientation_tolerance_degs` | float (optional) | Maximum orientation deviation, in degrees. Only checked when greater than 0. |

The planner checks that the current orientation stays within the specified
tolerance of whichever is closer: the start orientation or the goal orientation.
This allows smooth transitions when start and goal have different orientations.

### PseudolinearConstraint

Like LinearConstraint but uses proportional tolerances instead of fixed values.
The actual tolerance scales with the distance between start and goal.

| Parameter                      | Type             | Description                                                                                         |
| ------------------------------ | ---------------- | --------------------------------------------------------------------------------------------------- |
| `line_tolerance_factor`        | float (optional) | Proportional factor. Actual tolerance = factor x distance(start, goal).                             |
| `orientation_tolerance_factor` | float (optional) | Proportional factor for orientation. Actual tolerance = factor x orientation_distance(start, goal). |

Use this when you want the constraint to adapt to the length of the motion. A
short move gets a tight tolerance; a long move gets a proportionally larger one.

### CollisionSpecification

Allows specific pairs of frames to collide during planning. By default, the
planner rejects any path where any two frames collide. CollisionSpecification
lets you whitelist specific pairs.

| Parameter | Type                | Description                                          |
| --------- | ------------------- | ---------------------------------------------------- |
| `allows`  | list of frame pairs | Each entry has `frame1` and `frame2` (string names). |

This is useful when:

- A gripper is expected to contact the object it is picking up.
- Two components are physically close and their simplified collision geometries
  overlap, but the real components do not collide.

Frame names support hierarchical matching: specifying `"my-arm"` matches all
sub-geometries of the arm (such as `my-arm:upper_arm_link`,
`my-arm:forearm_link`).

## Using constraints in code

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient
from viam.proto.service.motion import Constraints, LinearConstraint, OrientationConstraint
from viam.proto.common import PoseInFrame, Pose

motion_service = MotionClient.from_robot(machine, "builtin")

# Keep the end effector on a straight line with a level orientation
constraints = Constraints(
    linear_constraint=[
        LinearConstraint(
            line_tolerance_mm=5.0,
        )
    ],
    orientation_constraint=[
        OrientationConstraint(
            orientation_tolerance_degs=5.0,
        )
    ]
)

destination = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=300, y=200, z=400, o_x=0, o_y=0, o_z=-1, theta=0)
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
import (
    motionpb "go.viam.com/api/service/motion/v1"
    "go.viam.com/rdk/services/motion"
)

motionService, err := motion.FromRobot(machine, "builtin")
if err != nil {
    logger.Fatal(err)
}

lineTolerance := float32(5.0)
orientTolerance := float32(5.0)

constraints := &motionpb.Constraints{
    LinearConstraint: []*motionpb.LinearConstraint{
        {
            LineToleranceMm: &lineTolerance,
        },
    },
    OrientationConstraint: []*motionpb.OrientationConstraint{
        {
            OrientationToleranceDegs: &orientTolerance,
        },
    },
}

// Pass constraints in the Move request
_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "my-arm",
    Destination:   destination,
    Constraints:   constraints,
})
```

{{% /tab %}}
{{< /tabs >}}

### Allowing specific collisions

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.service.motion import (
    Constraints, CollisionSpecification
)

# Allow the gripper to contact the target object
collision_spec = CollisionSpecification(
    allows=[
        CollisionSpecification.AllowedFrameCollisions(
            frame1="my-gripper",
            frame2="target-object"
        )
    ]
)

constraints = Constraints(
    collision_specification=[collision_spec]
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
constraints := &motionpb.Constraints{
    CollisionSpecification: []*motionpb.CollisionSpecification{
        {
            Allows: []*motionpb.CollisionSpecification_AllowedFrameCollisions{
                {
                    Frame1: "my-gripper",
                    Frame2: "target-object",
                },
            },
        },
    },
}
```

{{% /tab %}}
{{< /tabs >}}

## Performance considerations

Constraints make the planner's job harder. The planner must check each candidate
path segment against all constraints, and constrained solutions are harder to
find than unconstrained ones.

- **Tight tolerances** (small `line_tolerance_mm` or `orientation_tolerance_degs`)
  increase planning time and may cause the planner to fail if no path exists
  within the tolerance.
- **Start with larger tolerances** and tighten only as needed. A 10 mm linear
  tolerance is easier to satisfy than a 1 mm tolerance.
- **Combining constraints** multiplies the difficulty. Use the minimum set of
  constraints required for your task.

## What's Next

- [Move an Arm with Constraints](/motion-planning/motion-how-to/move-arm-with-constraints/):
  practical examples of constrained motion.
- [Motion Planning Algorithms](/motion-planning/reference/algorithms/): how the planner
  searches for constrained paths.
- [Define Obstacles](/motion-planning/obstacles/): define the geometry the
  planner uses for collision checking.
