---
linkTitle: "Replay mode"
title: "Replay mode"
weight: 35
layout: "docs"
type: "docs"
description: "Step through saved motion plans in the 3D scene, including the obstacles each plan was planned against."
capabilities: ["scene-3d", "motion-planning"]
diataxis: explanation
---

Replay mode loads plans the motion service saved and steps through them in the scene. It shows a plan the motion service already computed, whatever requested it: your code, a module, the CLI, or [Move mode](/visualization/3d-scene/move-mode/).

Replay also shows something the scene can't show otherwise: the obstacles a request passed in its `WorldState`. Those obstacles never appear in the live scene, but a saved plan records them, and a replayed plan draws them in place.

Replay needs saved plans: the motion service has to be configured to save them, and the files synced to the cloud. To set that up, see [Save plans for replay](/motion-planning/visualize-a-motion-plan/#save-plans-for-replay).

## Load and play a plan

1. Switch to Replay mode.
2. Click **Import from data**, then pick up to five plans. The dialog lists synced files tagged `motion-plan`, which are plans that succeeded, and `motion-plan-err`, which are plans that failed. It searches the current machine by default; widen it to the whole organization if the plan ran elsewhere. You can also upload a plan file from your computer.
3. Select a plan to render it. A failed plan has no trajectory, so it renders the scene it planned against with nothing to step through.
4. Play, pause, step, or scrub through the plan. Each step moves the arm's links and joints to their pose at that waypoint, with the plan's obstacles in place.

Select a plan's entity to change its color, opacity, or axes helper in the Details panel; those edits hold as you scrub.

## What replay shows

Replay steps through the plan's waypoints only. A plan with many closely spaced waypoints, such as one with a linear constraint, plays smoothly. A plan with just a start and an end jumps between them, so replay won't show how the arm got around an obstacle. To see the motion between waypoints, preview the same move in [Move mode](/visualization/3d-scene/move-mode/), where you can switch to **Interpolated** playback.

Saved plans include previews from Move mode, even ones you never ran, so the import list can include plans that never moved the machine.

A loaded plan appears only in Replay mode. Switching to another mode hides it, so it doesn't affect the live scene or the **Collisions** readout in Move mode.

## What's next

- [Save plans for replay](/motion-planning/visualize-a-motion-plan/#save-plans-for-replay): configure the motion service to save plans and sync them.
- [Move mode](/visualization/3d-scene/move-mode/): plan a move from the scene and preview it, including the motion between waypoints.
- [Debug a motion plan](/motion-planning/debug-motion-plan/): check frames, obstacles, and reach when a plan fails.
