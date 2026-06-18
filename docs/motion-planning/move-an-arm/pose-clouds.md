---
linkTitle: "Pose clouds"
title: "Relax a goal with a pose cloud"
weight: 45
layout: "docs"
type: "docs"
description: "Give the planner a region of acceptable destinations instead of a single exact pose, so it can find a solution faster and more reliably."
---

A single target pose tells the planner exactly where the end effector must end
up, down to the millimeter and the degree. For many tasks that is more precise
than you need. Dropping a part into a bin, touching a flat surface, or pointing a
tool roughly at a target all have slack in them, and demanding an exact pose
throws that slack away. An over-constrained goal makes the planner work harder,
fail more often, and sometimes reject a goal that a slightly looser target would
have reached.

A _pose cloud_ replaces the exact goal with a region of acceptable poses. You
give the planner a target pose plus a set of tolerances, and any pose within
those tolerances counts as having arrived. This page explains what a pose cloud
relaxes, why its tolerances are measured in the target's own frame, and how to
pass one to the motion service.

## How a pose cloud relaxes a goal

A pose cloud defines a tolerance, or leeway, on each component of the goal pose.
Each leeway permits deviation in the range from its negative to its positive
value, so the goal becomes a box around the target pose rather than a single
point.

| Field            | Units    | Relaxes                                                           |
| ---------------- | -------- | ----------------------------------------------------------------- |
| `X`, `Y`, `Z`    | mm       | Position along each axis                                          |
| `OX`, `OY`, `OZ` | unitless | The orientation vector components (the direction the tool points) |
| `Theta`          | degrees  | Rotation about the orientation axis                               |

A leeway of zero on a field holds that component to the exact target value; a
larger leeway gives the planner more room on that component. You relax only what
the task allows: a part dropped into a wide bin can take large `X` and `Y`
leeways while keeping `Z` tight, and a tool that may spin freely about its axis
can take a large `Theta` while keeping its pointing direction fixed.

The more freedom you give the planner, the larger the set of arm configurations
that satisfy the goal, so inverse kinematics is more likely to find a solution
and the search reaches it faster. A goal that fails as an exact pose often
succeeds as a pose cloud.

## Tolerances are measured in the target's frame

The leeways are evaluated in the reference frame of the target, not in world
coordinates. This matters whenever the target is tilted relative to the world.

Consider a gripper approaching an inclined surface. You want to allow slack
_along_ the surface but stay tight _into_ it, so the tool does not push through.
Expressed in world coordinates that is an awkward mix of all three axes, because
the surface is tilted. Expressed in the surface's own frame it is simple: large
leeway on the two in-plane axes, tight leeway on the axis normal to the surface.
Because pose clouds use the target's frame, you describe the tolerance the way
the task is shaped rather than translating it into world axes by hand.

## Use a pose cloud with the motion service

In Go, attach a pose cloud to the destination with
`NewPoseInFrameWithGoalCloud`, then pass that destination to `Move`. The pose is
the center of the region and the `PoseCloud` is the leeway around it.

```go
import (
    "go.viam.com/rdk/services/motion"
    "go.viam.com/rdk/referenceframe"
    "go.viam.com/rdk/spatialmath"
)

// Point the tool at the cup, but allow slack in the approach orientation.
destination := referenceframe.NewPoseInFrameWithGoalCloud(
    "cup",
    spatialmath.NewPoseFromOrientation(
        &spatialmath.OrientationVectorDegrees{OX: 1, OZ: 0, Theta: 180},
    ),
    &referenceframe.PoseCloud{OX: 1, OY: 1, OZ: 0.1, Theta: 10},
)

_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "my-gripper",
    Destination:   destination,
})
if err != nil {
    logger.Fatal(err)
}
```

Here the destination is expressed in the `cup` frame, so the leeways apply
relative to the cup. The planner is free to satisfy the goal with any gripper
pose inside the cloud.

{{% alert title="Available through the Go SDK" color="note" %}}
The goal cloud travels on the destination's `PoseInFrame`, which is part of the
`Move` request sent to the motion service, so the planner honors it server side.
The convenience constructor `NewPoseInFrameWithGoalCloud` is part of the Go SDK;
other SDKs do not yet provide an equivalent helper.
{{% /alert %}}

## When to reach for a pose cloud

- **Slack placement.** Dropping or setting down an object where any spot in a
  region is acceptable. Relax the in-plane position and the spin about the
  vertical.
- **Surface contact.** Touching, wiping, or sanding a surface where the contact
  point can move along the surface but must stay on it. Relax the in-plane axes,
  keep the normal tight.
- **Faster, more reliable planning.** Any goal that is failing or planning
  slowly as an exact pose. Relaxing the components the task does not constrain
  enlarges the solution set and often turns a failing plan into a quick success.

If the task genuinely requires an exact pose, use a plain destination. A pose
cloud is for the common case where "close enough" is correct and exactness only
makes the planner's job harder.

## What's next

- [Configure motion constraints](/motion-planning/move-an-arm/constraints/):
  restrict the path between poses, the complement to relaxing the goal.
- [Move through waypoints](/motion-planning/move-an-arm/multiple-waypoints/):
  use pose clouds for the waypoints that do not need an exact pose.
- [How motion planning works](/motion-planning/how-planning-works/):
  why a larger solution set makes the search succeed more often.
