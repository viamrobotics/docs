---
linkTitle: "Monitor mode"
title: "Monitor mode"
weight: 10
layout: "docs"
type: "docs"
description: "Watch your machine's live state in the 3D scene, read any frame's pose, and replay saved motion plans."
capabilities: ["scene-3d", "motion-planning"]
diataxis: explanation
---

Monitor mode is where the 3D scene starts. It shows your machine as it is: its frames, its configured geometry, and, when the machine is online, live poses, point clouds, and custom visuals. Nothing in Monitor mode changes your machine or its configuration, so it's the safe place to look around.

## Live and configured state

What the scene shows depends on whether the machine is online:

- **Online**: component poses, point clouds, and custom visuals update as the machine runs.
- **Offline**: the scene shows only the saved configuration, with every component at its configured pose. Point clouds and custom visuals are absent.

The scene fetches each kind of live data at its own rate, which you set under **Settings** > **Connection**. A data stream set to off never updates, so check these rates when part of the scene seems frozen. For other reasons a scene can look wrong, see [Troubleshoot the 3D scene](/visualization/troubleshoot-the-3d-scene/).

## Read a frame's pose

Select any entity, in the viewport or in the **World** panel, to see its pose in the Details panel: its **world position** and **world orientation**, its **parent frame**, and its **local position** and **local orientation** relative to that parent. In Monitor mode these fields are read-only. To change them, use [Build mode](/visualization/3d-scene/build-mode/).

To read where an arm's end effector is, expand the arm in the **World** panel and select its last link or the frame attached to it, such as a gripper. For the meaning of each field, see [3D scene controls and settings](/visualization/3d-scene/controls-and-settings/#details-panel-fields).

## Replay a saved plan

The **Motion Plan Replayer** loads plans the motion service saved and steps through them in the scene. It's the way to see a plan the service already computed, from your code or from [Move mode](/visualization/3d-scene/move-mode/), without writing any code.

Replay also shows something the scene can't show otherwise: the obstacles a request passed in its `WorldState`. Those obstacles never appear in the live scene, but a saved plan records them, and a replayed plan draws them in place.

### Save plans

The motion service saves plans only when its configuration tells it to:

- `plan_file_path` sets the directory for plan files. It's required by both settings below.
- `log_planner_errors: true` saves plans that fail. A failed plan's file holds the request only, with no trajectory, but replaying it still shows the scene the planner was working in.
- `log_slow_plan_threshold_ms` saves plans that take longer than that many milliseconds. Set it to `-1` to save every plan, which is what captures successful plans for replay.

These settings apply only to the motion service you configure them on, and to plans requested through that service. In Move mode, check which service the move controls use. See [Motion service configuration](/motion-planning/reference/motion-service/#configuration-attributes).

Then add the plan directory to the data manager's `additional_sync_paths` so the files reach the cloud (see [Upload external data](/data/capture-sync/upload-other-data/)). Syncing walks the `tag=` subdirectories the service writes and carries those tags to the cloud, which is how the replayer finds the plans. For example:

```json
{
  "name": "data_manager-1",
  "api": "rdk:service:data_manager",
  "model": "rdk:builtin:builtin",
  "attributes": {
    "additional_sync_paths": ["${environment.HOME}/.viam/plans"]
  }
}
```

### Load and play a plan

1. Open the **Motion Plan Replayer**.
2. Click **Import from data**, then pick up to five plans. The dialog lists synced files tagged `motion-plan`, which are plans that succeeded, and `motion-plan-err`, which are plans that failed. It searches the current machine by default; widen it to the whole organization if the plan ran elsewhere. You can also upload a plan file from your computer.
3. Select a plan to render it. A failed plan has no trajectory, so it renders the scene it planned against with nothing to step through.
4. Play, pause, step, or scrub through the plan. Each step moves the arm's links and joints to their pose at that waypoint, with the plan's obstacles in place.

Select a plan's entity to change its color, opacity, or axes helper in the Details panel; those edits hold as you scrub.

### What replay shows

Replay steps through the plan's waypoints only. A plan with many closely spaced waypoints, such as one with a linear constraint, plays smoothly. A plan with just a start and an end jumps between them, so replay won't show how the arm got around an obstacle. To see the motion between waypoints, preview the same move in [Move mode](/visualization/3d-scene/move-mode/), where you can switch to **Interpolated** playback.

Saved plans include previews from Move mode, even ones you never ran, so the import list can include plans that never moved the machine.

A loaded plan stays in the scene when you switch to Build or Move mode, and you can only remove it from Monitor mode. Remove it before you switch: in Move mode, the plan's copy of the machine counts as real geometry in the **Collisions** readout.

## What's next

- [Move mode](/visualization/3d-scene/move-mode/): plan and run a move from the scene.
- [Visualize a motion plan](/motion-planning/visualize-a-motion-plan/): publish a plan as custom visuals to keep it live while the machine runs.
- [Troubleshoot the 3D scene](/visualization/troubleshoot-the-3d-scene/): trace a wrong or missing element to its source.
