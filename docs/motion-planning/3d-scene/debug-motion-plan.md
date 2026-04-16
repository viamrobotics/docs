---
linkTitle: "Debug a motion plan"
title: "Debug a motion plan"
weight: 45
layout: "docs"
type: "docs"
description: "Use the 3D scene to inspect the frame system and obstacle geometry behind a motion plan that failed or produced unexpected results."
---

When a motion plan fails with a collision error or produces a path that
does not look right, the **3D SCENE** tab lets you inspect the static view
of the world the planner sees at the moment you look: configured frame
positions, collision geometries, and the arm's current pose. Most
motion planning failures come down to one of a few problems that are
immediately visible in 3D.

The **3D SCENE** tab does not replay motion plans and has no timeline,
scrubber, or plan-playback control. It is an inspector of the
configured frame system and live component poses. If you need to watch
a plan execute over time, poll `GetPlan` from code (see
[Monitor a running plan](/motion-planning/monitor-a-running-plan/)) or
step the arm to intermediate joint positions manually and reinspect.

## Prerequisites

- A machine with an arm or gantry configured and at least one frame defined.
- A motion plan that is failing or producing unexpected results.

## Diagnose the problem

### 1. Open the 3D SCENE tab

Navigate to your machine in the [Viam app](https://app.viam.com) and
click the **3D SCENE** tab. The scene loads your current frame system
configuration.

If your machine is online, the scene connects for live pose data.
If your machine is offline, the scene still renders the configured
frame positions.

### 2. Check frame positions

In the **World** panel in the upper-left, expand the tree and click
each component in turn. The Details panel on the right shows the
selected entity's **world position** and **world orientation**, plus
editable **local position** and **local orientation** relative to the
parent frame. Compare these values to your physical measurements.

Three common mismatches to look for:

- **Wrong location**: translation values in the frame configuration do not match the physical setup. Compare **local position** (mm) to your physical measurements.
- **Wrong orientation**: the arm base is rotated 90 degrees, or a camera points the wrong direction. Check **local orientation** in the Details panel.
- **Wrong parent**: the component is attached to the wrong parent, which places it in an unexpected part of the scene. Check the **parent frame** field in the Details panel.

### 3. Check obstacle geometry

Obstacles appear as translucent shapes in the scene and as child rows
under their parent frame in the **World** panel. Select each obstacle
from the tree to see its **geometry** type and **dimensions** in the
Details panel.

Verify that:

- Every physical obstacle in your workspace has a corresponding
  geometry in the scene.
- Each geometry covers the actual physical object. If a box geometry
  is too small, the planner will find paths that clip the real
  obstacle.
- Geometries are positioned correctly. A table surface defined at
  `z: 0` when the arm base is at `z: 500` will not protect against
  table collisions.

If obstacles are missing or misplaced, see
[Set up obstacle avoidance](/motion-planning/3d-scene/set-up-obstacle-avoidance/).

### 4. Look for impossible targets

If the motion plan target is outside the arm's reach or inside an
obstacle, the planner cannot find a path.

In the **World** panel, expand the arm and select its tip link or the
gripper frame (whichever is configured as the motion target). Read the
**world position** and compare it to the target pose your code
commanded. Then mentally place the target: is it inside an obstacle
geometry? Is it further than the arm can reach from its base?

If the target is inside an obstacle geometry, either move the target
or adjust the obstacle definition.

### 5. Check for self-collision geometry

Some arm models include collision geometry for each link. If a motion
plan fails with a self-collision error, inspect the arm's link
geometries for overlap in the current configuration.

If the arm renders without collision geometry, the feature may be
disabled: open **Settings → Scene → Arm Models** and verify that the
rendering mode includes colliders.

Self-collisions can happen when wrist joints are commanded to
positions that bring adjacent links too close together. If the
overlap is a modeling artifact rather than a real collision, allow
the frame pair with
[`CollisionSpecification`](/motion-planning/obstacles/allow-frame-collisions/).

## Common causes of motion plan failures

| Symptom                       | Likely cause                                  | What to check in 3D SCENE                                                  |
| ----------------------------- | --------------------------------------------- | -------------------------------------------------------------------------- |
| "no valid path found"         | Target unreachable or blocked by obstacles    | Is the target inside an obstacle? Is it within the arm's reach?            |
| Collision error               | Obstacle geometry intersects the planned path | Are obstacles positioned correctly? Are they the right size?               |
| Path goes through the table   | Table obstacle missing or too small           | Is there a geometry covering the table surface? Does it extend far enough? |
| Arm takes an unexpected route | Obstacles force the planner to go around      | Are there obstacles you did not intend to add? Is geometry oversized?      |
| Self-collision error          | Arm links collide with each other             | Do link geometries overlap in the failing configuration?                   |
