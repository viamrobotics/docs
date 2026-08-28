---
linkTitle: "Visualize a motion plan"
title: "Visualize a motion plan"
weight: 86
layout: "docs"
type: "docs"
description: "Publish a motion plan's trajectory and goals as custom visuals so the 3D scene renders the path against obstacles and reach."
aliases:
  - /motion-planning/3d-scene/visualize-a-motion-plan/
capabilities:
  - motion-planning
---

The **3D SCENE** tab renders your configured frame system and live component poses, and the
[visual checks for a failing plan](/motion-planning/debug-motion-plan/) find most
problems by eye. When those checks do not reveal the problem, or you want to see the
trajectory itself, publish the plan as **custom visuals** through a world state store
service. The scene then renders the path you can otherwise only read as numbers.

This page shows how to turn a plan into transforms the scene can draw, and how to
use the rendered path to debug a plan that failed or moved unexpectedly.

## Replay a saved plan in the 3D scene

If the plan already ran, you do not need to write any code to see it. The motion service
dumps qualifying plans as JSON files, and the **3D SCENE** tab replays those files step by
step.

The service does not dump every plan. Configure which ones it keeps
(see [Motion service configuration](/motion-planning/reference/motion-service/)):

- `plan_file_path` is where the dumps go. On its own it writes nothing; it is required by
  both of the settings below.
- `log_planner_errors: true` dumps a plan that failed. A failed dump is the request only,
  with no trajectory to replay, but it still shows the world the planner was working in.
- `log_slow_plan_threshold_ms` dumps a plan that took longer than that many milliseconds.
  This is what captures successful plans, trajectory included, so set it if you want to
  replay plans that worked.

Then add the plan directory to the data manager's `additional_sync_paths` so the files reach
the cloud (see [Upload external data](/data/capture-sync/upload-other-data/)). Syncing
walks the `tag=` subdirectories the service writes and carries those tags to the cloud,
which is how the import dialog finds the plans.

With plans synced, open the **3D SCENE** tab in monitor mode:

1. Open the **Motion Plan Replayer** panel from the top-center toolbar.
2. Click **Import from data**, then pick up to five plans. The dialog lists synced files
   tagged `motion-plan`, which are plans that succeeded, and `motion-plan-err`, which are
   plans that failed. It searches the current machine by default; widen it to the whole
   organization if the plan ran elsewhere. You can also upload a plan JSON from your
   computer instead.
3. Select a plan to render it. A plan that failed is a request without a trajectory, so it
   renders the scene it planned against with nothing to step through.
4. Scrub the trajectory with the player at the bottom of the viewport: play and pause, step
   one position at a time, jump to either end, or drag the slider. Each step moves the arm's
   links and joints to their pose at that step, with the plan's obstacles in place.

Select a plan's entity to change its color, opacity, or axes helper in the Details panel;
those edits hold as you scrub. Plan frames render without axes helpers by default.

Replay shows a plan the service already computed. To render a plan you are computing
yourself, or to keep visuals live while the machine runs, publish the plan as custom
visuals instead.

## Prerequisites

The custom-visuals path below starts from a plan you already have in Go:

- A `plan` from `armplanning.PlanMotion`, and the `fs` (`*referenceframe.FrameSystem`) you
  assembled into its `PlanRequest`. See
  [Verify a plan](/motion-planning/verify-a-plan/) for building both.
- The goal pose you passed to the planner, to mark the destination.
- A module that can serve a world state store service, which is how the transforms reach
  the scene. See
  [Publish visuals from a module](/visualization/publish-visuals-from-a-module/).

## Why publish the plan as custom visuals

A plan is a sequence of joint configurations. Rendered in the scene, the path
shows immediately whether it clips an obstacle, swings wide, or aims at a
target outside the arm's reach. Publishing
the plan as world state store transforms puts the trajectory and goals in the
same 3D view as the frames and obstacle geometry the planner used, so you can see
the path and the world together.

## Convert the trajectory into poses

A plan's `Trajectory` is a sequence of joint configurations
(`FrameSystemInputs`), one per step. The scene places geometry by pose, so
convert each step into end-effector poses with the frame system. `ComputePoses`
takes a configuration and returns the pose of each frame:

```go
var transforms []*commonpb.Transform
for i, step := range plan.Trajectory() {
    poses, err := step.ComputePoses(fs)
    if err != nil {
        return err
    }
    gripperPose := poses["my-gripper"].Pose()
    // stepMarker (next section) turns this pose into a visual.
    transform, err := stepMarker(i, gripperPose)
    if err != nil {
        return err
    }
    transforms = append(transforms, transform)
}

// Mark the destination you passed to the planner (goalMarker, next section).
goalTransform, err := goalMarker(0, goalPose)
if err != nil {
    return err
}
transforms = append(transforms, goalTransform)
// Serve transforms through a world state store service (last section).
```

Each `step` is the arm's configuration at that point in the trajectory, and
`poses["my-gripper"]` is where the gripper sits in that configuration.

## Build transforms for the plan

With a pose per step, build the visuals with the `draw` library: a marker per
trajectory step and a marker for each goal. Give each a stable UUID so the scene
can update them when you re-plan.

```go
import (
    "fmt"

    "github.com/viam-labs/motion-tools/draw"
    commonpb "go.viam.com/api/common/v1"
    "go.viam.com/rdk/spatialmath"
)

// Distinct colors keep the trajectory and its goals apart in the scene.
var (
    stepColor = draw.NewColor(draw.WithName("blue"))
    goalColor = draw.NewColor(draw.WithName("green"))
)

func stepMarker(i int, pose spatialmath.Pose) (*commonpb.Transform, error) {
    id := fmt.Sprintf("step-%d", i)
    // Build the sphere at the origin; WithPose below places it at the step pose.
    sphere, err := spatialmath.NewSphere(spatialmath.NewZeroPose(), 5, id)
    if err != nil {
        return nil, err
    }
    drawn, err := draw.NewDrawnGeometry(sphere, draw.WithGeometryColor(stepColor))
    if err != nil {
        return nil, err
    }
    // WithID derives a stable UUID from the string, so re-planning updates each
    // marker in place instead of drawing a duplicate.
    return drawn.Draw(id, draw.WithID(id), draw.WithPose(pose))
}

// goalMarker draws a destination pose. Unlike the trajectory poses, a goal pose is
// not a ComputePoses output: it is the destination you passed to the planner.
func goalMarker(i int, goalPose spatialmath.Pose) (*commonpb.Transform, error) {
    id := fmt.Sprintf("goal-%d", i)
    sphere, err := spatialmath.NewSphere(spatialmath.NewZeroPose(), 8, id)
    if err != nil {
        return nil, err
    }
    drawn, err := draw.NewDrawnGeometry(sphere, draw.WithGeometryColor(goalColor))
    if err != nil {
        return nil, err
    }
    return drawn.Draw(id, draw.WithID(id), draw.WithPose(goalPose))
}
```

The trajectory poses come from `ComputePoses`, but the goal pose is the destination
you passed to the planner. `goalMarker` draws it with a distinct color, so the target
stands out from the trajectory leading to it.

## Serve the transforms to the scene

Serve the transforms through a world state store service so the **3D SCENE** tab
renders them. Return your step and goal markers from the service's `ListUUIDs`,
`GetTransform`, and `StreamTransformChanges` methods, and the plan streams in alongside
the frames and obstacle geometry the scene already shows. For those methods, the
poll-and-update loop, and how a module pulls data from its dependencies, see
[Publish visuals from a module](/visualization/publish-visuals-from-a-module/).

## Diagnose a failed or surprising plan

With the plan rendered, debugging becomes visual. Compare the trajectory against
the rest of the scene:

- **Where does the path collide?** If a step marker passes through an obstacle
  geometry, that is where the planner reports a collision. Check whether the
  obstacle is real or an oversized geometry.
- **Does the goal fall outside the arm's reach?** If a goal marker sits far from
  any reachable arm configuration, the goal is out of reach. Move the goal or
  check the frame system.
- **Why the detour?** An unexpected route usually means an obstacle is forcing
  the planner around it. Look for stray geometry between the start and goal.

For checking the obstacle geometry itself, separate from the plan, see
[Verify obstacles](/motion-planning/obstacles/verify-obstacles/).

## When to visualize versus inspect or verify

The 3D scene serves three distinct purposes, and it helps to keep them straight:

- **Visualize a plan** (this page): publish the trajectory and goals as custom
  visuals to see the path in context.
- **[Inspect static frames and geometry](/motion-planning/debug-motion-plan/)**:
  use the stock scene to check frame positions and obstacle coverage with no plan involved.
- **Check feasibility**: use `armplanning.PlanMotion` to confirm a goal is
  reachable and a path exists before you visualize or run anything.

Visualization shows you _what the path looks like_; static inspection shows you
_what the world looks like_; feasibility checking tells you _whether a plan
exists at all_. Reach for the one that matches the question you are asking.

## What's next

- [Debug a motion plan](/motion-planning/debug-motion-plan/):
  the no-code visual checks to try first.
- [Publish visuals from a module](/visualization/publish-visuals-from-a-module/):
  the world state store service that serves these transforms.
- [Verify obstacles](/motion-planning/obstacles/verify-obstacles/):
  check obstacle geometry against the real workspace.
- [How motion planning works](/motion-planning/how-planning-works/):
  why a plan can be infeasible and what to adjust.
