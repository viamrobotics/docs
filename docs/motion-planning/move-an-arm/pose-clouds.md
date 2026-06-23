---
linkTitle: "Pose clouds"
title: "Relax a goal with a pose cloud"
weight: 45
layout: "docs"
type: "docs"
description: "Give the planner a region of acceptable destinations instead of a single exact pose, so it can find a solution faster and more reliably."
---

By default `Move` requires a destination pose, which defines where the end effector must
move to, and the planner holds the end effector to it tightly. For many tasks that is more
precise than needed. Dropping a part into a bin, sanding a flat surface, or pointing a
camera at an injection molding station all have different tolerance requirements for the destination pose,
and demanding tight tolerances on the target pose can lead to issues. An over-constrained goal makes the planner work harder, fail more often, and sometimes reject a goal that would have been valid for the task.

A `pose cloud` replaces the exact goal with a region of acceptable poses. You
give the planner a target pose plus a set of tolerances, and any pose within
those tolerances is considered valid. This page explains what a pose cloud
relaxes and how to use a `pose cloud` with the motion service.

## When to reach for a pose cloud

- **Target regions.** When the destination is a region rather than one exact pose, use a
  pose cloud. For example, an object that may rest anywhere on a table, or a soup can that
  may spin about its long axis.
- **Dynamic collisions.** When the target area may contain obstacles, a pose cloud lets
  the planner place the object at a clear spot while avoiding collisions at the destination.
- **Kinematic constraints.** When a goal fails or plans slowly because the arm struggles
  to reach that exact pose, relaxing the destination tolerance enlarges the solution space
  and often turns a failing plan into a success.

Pose clouds are powerful when coupled with motion constraints: together they describe the motion you want without pinning down the destination exactly. Moving a cup of water is a good example. You define an
orientation constraint to keep the cup upright, but you may not know which exact target
pose lets the arm hold that orientation across its workspace. A pose cloud lets the planner
choose a destination within a region instead:

{{<imgproc src="/motion-planning/move-an-arm/pose-cloud-cup.svg" declaredimensions=true alt="A cobot arm holds a cup of water above a table. A translucent dashed region on the table marks the pose cloud, with several faded ghost cups inside it showing acceptable destinations. The cup may land anywhere in the region at any rotation while staying upright." style="max-width:760px" class="aligncenter">}}

## Relaxing the destination pose

A pose cloud defines a tolerance on each component of the goal pose.
Each permits +/- deviation, so the goal becomes a box around the target pose rather than a single
pose. The destination pose is the center of the box.

```go
&referenceframe.PoseCloud{
    X:     50, // 50 mm of slack in x
    Y:     50, // 50 mm of slack in y
    Theta: 90, // up to 90 degrees of rotation about the orientation axis
    // Z, OX, OY, and OZ are omitted, so they default to 0 and stay exact.
}
```

| Field            | Units    | Relaxes                                                           | Default                   |
| ---------------- | -------- | ----------------------------------------------------------------- | ------------------------- |
| `X`, `Y`, `Z`    | mm       | Position along each axis                                          | `0`: position held exact  |
| `OX`, `OY`, `OZ` | unitless | The orientation vector components (the direction the tool points) | `0`: direction held exact |
| `Theta`          | degrees  | Rotation about the orientation axis                               | `0`: rotation held exact  |

A tolerance of zero on a field holds that component to the exact target value; a
larger tolerance gives the planner more room on that component. You relax only what
the task allows: a part dropped into a wide bin can take large `X` and `Y`
tolerance while keeping `Z` tight, and a tool that may spin freely about its axis
can take a large `Theta` while keeping its pointing direction fixed.

The position tolerances (`X`, `Y`, `Z`) are millimeters and `Theta` is degrees. The
orientation-vector tolerances (`OX`, `OY`, `OZ`) are unitless deviations of the pointing
direction on a unit sphere, not angles: a value of `1` accepts any value for that
component, and `0` holds it exact.

The more freedom you give the planner, the larger the set of arm configurations
that satisfy the goal, so inverse kinematics is more likely to find a solution
and the search reaches it faster.

## Tolerances are measured in the target's frame

The tolerances are evaluated in the reference frame of the target, not in world
coordinates. This matters whenever the target is tilted relative to the world.

Consider a gripper approaching an inclined surface. You want to allow tolerance
_along_ the surface but stay tight _into_ it, so the tool rides the surface
instead of driving through it. Expressed in world coordinates that is an awkward
mix of all three axes, because the surface is tilted. Expressed in the surface's
own frame, you give large tolerance on the two in-plane axes and tight tolerance on the
axis normal to the surface.
Because pose clouds use the target's frame, you describe the tolerance the way
the task is shaped rather than translating it into world axes by hand.

{{<imgproc src="/motion-planning/move-an-arm/pose-cloud-target-frame.svg" declaredimensions=true alt="Two panels. On the left, a pose-cloud region drawn as a thin slab lying along an inclined surface, large along the surface and tight into it, with the target frame tilted to match the surface. On the right, the orientation tolerance shown as a cone around the tool's pointing direction for OX and OY, plus an ellipse for Theta rotation about the axis." style="max-width:820px" class="aligncenter">}}

## Use a pose cloud with the motion service

A pose cloud attaches to the destination object. In Go, attach a pose cloud to the destination with
`NewPoseInFrameWithGoalCloud`, then pass that destination to `Move`. The pose is
the center of the region and the `PoseCloud` is the tolerance around it. This example includes an orientation constraint for the water example, so the cup stays upright for the whole motion, not only at
the goal.

```go
import (
    "github.com/golang/geo/r3"
    "go.viam.com/rdk/motionplan"
    "go.viam.com/rdk/referenceframe"
    "go.viam.com/rdk/services/motion"
    "go.viam.com/rdk/spatialmath"
)

// Place the cup somewhere on the table. The exact spot does not matter, and the
// cup may end up rotated about vertical, but it must stay upright.
destination := referenceframe.NewPoseInFrameWithGoalCloud(
    "table", // the target frame: tolerances follow the table surface
    spatialmath.NewPose(
        r3.Vector{X: 0, Y: 0, Z: 0},                   // center of the region, on the table surface
        &spatialmath.OrientationVectorDegrees{OZ: -1}, // upright: the tool's z-axis points into the table
    ),
    // Tolerances are applied in the table frame, each as [-value, +value].
    &referenceframe.PoseCloud{
        X:     75,  // mm of slack across the table surface in x
        Y:     75,  // mm of slack across the table surface in y
        Z:     0,   // hold the cup on the surface
        Theta: 180, // degrees: any rotation about vertical; spinning the cup does not spill it
        // OX, OY, OZ stay 0, so the upright pointing direction is held exact.
    },
)

// Keep the cup upright along the whole path, within 5 degrees, not just at the goal.
constraints := &motionplan.Constraints{
    OrientationConstraint: []motionplan.OrientationConstraint{
        {OrientationToleranceDegs: 5},
    },
}

_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "my-gripper",
    Destination:   destination,
    Constraints:   constraints,
})
if err != nil {
    logger.Fatal(err)
}
```

{{% alert title="Available through the Go SDK" color="note" %}}
Today the Go SDK provides the `NewPoseInFrameWithGoalCloud` constructor;
The goal cloud travels on the destination's `PoseInFrame`, which is part of the
`Move` request sent to the motion service, so the planner honors it server side.
{{% /alert %}}

## What's next

- [Configure motion constraints](/motion-planning/move-an-arm/constraints/):
  restrict the path between poses, the complement to relaxing the goal.
- [Move through waypoints](/motion-planning/move-an-arm/multiple-waypoints/):
  use pose clouds for the waypoints where close enough is fine.
- [How motion planning works](/motion-planning/how-planning-works/):
  why a larger solution set makes the search succeed more often.
