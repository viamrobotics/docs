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

## Debug a failed plan with Inspect IK

When a plan fails, the error tells you what collided, but not always whether the goal itself is impossible or only the route to it is blocked. **Inspect IK** answers that. Each plan in Replay mode's list has an **Inspect IK** button, which reruns the inverse kinematics (IK) for the plan's request and lists every candidate arm configuration it finds for the goal. **Back to plans** returns to the plan list.

Candidates are grouped by seed. Each seed is a different starting point for the search, so different seeds tend to find different arm configurations, such as elbow up or elbow down. You can also sort all candidates by cost; unscored candidates sort last. Each candidate gets one of three statuses:

- **Valid**: the end pose and the direct path to it are both clear.
- **Path blocked**: the end pose is reachable, but the direct path to it fails, by colliding with something or by violating a constraint in the request.
- **Goal blocked**: the end pose itself collides, with an obstacle or with another part of the machine. Candidates marked **unscored** are also goal blocked: the solver found no configuration at all from that seed, so there's no pose to show.

Read the overall pattern first:

- **Every candidate is goal blocked**: the goal is the problem. No configuration of the arm reaches it without a collision, so move the target or the obstacle.
- **Most candidates are path blocked**: the goal is reachable, but the route is obstructed. Look at what the path runs into.
- **Valid or path-blocked candidates appear only in the seed cache groups**: a solution exists, but in an arm configuration far from where the arm started.

Select a candidate to see it in the scene and read its failure detail, which names the geometries or the constraint involved. For a goal-blocked candidate, you can show its start and failing poses. For a path-blocked candidate, you can also play its direct path, interpolated over the number of steps you choose, and show its **Last good** pose: the last pose on the path before the failure. The path shows the blocked route, so the arm passes through whatever blocks it.

The direct path is a straight line in joint space, not the path the planner would take. With a linear or orientation constraint in the request, nearly every direct path violates the constraint, so most candidates show as path blocked whatever else is in the way. For those plans, read each candidate's failure detail before drawing conclusions.

## What's next

- [Save plans for replay](/motion-planning/visualize-a-motion-plan/#save-plans-for-replay): configure the motion service to save plans and sync them.
- [Move mode](/visualization/3d-scene/move-mode/): plan a move from the scene and preview it, including the motion between waypoints.
- [Debug a motion plan](/motion-planning/debug-motion-plan/): check frames, obstacles, and reach when a plan fails.
