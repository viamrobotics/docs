---
linkTitle: "Configure constraints"
title: "Configure motion constraints"
weight: 5
layout: "docs"
type: "docs"
description: "Restrict how the arm moves between poses using linear, orientation, and collision constraints."
aliases:
  - /reference/services/motion/constraints/
  - /services/motion/constraints/
  - /mobility/motion/constraints/
  - /motion-planning/constraints/
---

By default, the motion planner returns any collision-free path to the target
pose. The path may curve, twist, or take the end effector through any
orientation along the way. For many tasks this is fine, but some tasks require
the arm to move in a specific way:

- Carrying a cup of water requires the end effector to stay level.
- Welding a seam requires the tool to follow a straight line.
- Picking an object requires the gripper to contact the object without the
  planner rejecting the path.

Constraints let you specify these rules, and the motion planner only returns
paths that satisfy all of them.

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

When `line_tolerance_mm` is set, the planner keeps the end effector within
that distance of the line segment between start and goal. When
`orientation_tolerance_degs` is set, the planner keeps the end effector
orientation within that angular distance of whichever is closer: the start
orientation or the goal orientation.

### OrientationConstraint

Forces the end effector to maintain a consistent orientation throughout the
motion. Use this when the end effector must stay level or keep a fixed
orientation (for example, carrying a liquid).

| Parameter                    | Type             | Description                                                                                                                                               |
| ---------------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `orientation_tolerance_degs` | float (required) | Maximum orientation deviation, in degrees, for orientations that fall outside the start-to-goal box. A value of 0 rejects any deviation outside that box. |

The planner checks each orientation vector component (`OX`, `OY`, `OZ`,
`Theta`) against the start and goal independently. If every component of
the current orientation falls between the corresponding start and goal
values, the constraint is satisfied with zero error.

Otherwise, the planner measures the angular distance to whichever
endpoint is closer (start or goal) and rejects the path if that distance
exceeds `orientation_tolerance_degs`. The per-component box check allows
smooth transitions when start and goal have different orientations; the
tolerance gives a cushion on either side.

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
`my-arm:forearm_link`). For hierarchical matching details, self-collision
patterns, and worked examples (arm detecting itself through a vision
service, gripper holding an object), see
[Allow frame collisions](/motion-planning/obstacles/allow-frame-collisions/).

## Pass constraints to Move

Build a `Constraints` object containing one or more constraint entries
and pass it on the `Move` request's `Constraints` field. For worked
examples (straight-line tool path, level end effector, combined
constraints), see
[Move with constraints](/motion-planning/move-an-arm/move-with-constraints/).
For `CollisionSpecification` (allow specific frame pairs to collide), see
[Allow frame collisions](/motion-planning/obstacles/allow-frame-collisions/).

## Performance considerations

Every constraint adds a check to every candidate path segment, and
tight tolerances shrink the set of valid paths. Both raise planning time
and the failure rate.

- **Tight tolerances** (small `line_tolerance_mm` or `orientation_tolerance_degs`)
  increase planning time and may cause the planner to fail if no path exists
  within the tolerance.
- **Start with larger tolerances** and tighten only as needed. A 10 mm linear
  tolerance is easier to satisfy than a 1 mm tolerance.
- **Combining constraints** multiplies the difficulty. Use the minimum set of
  constraints required for your task.

## What's next

- [Move an arm with constraints](/motion-planning/move-an-arm/move-with-constraints/):
  practical examples of constrained motion.
- [How motion planning works](/motion-planning/how-planning-works/):
  how the planner searches for constrained paths.
- [Define obstacles](/motion-planning/obstacles/): define the geometry the
  planner uses for collision checking.
