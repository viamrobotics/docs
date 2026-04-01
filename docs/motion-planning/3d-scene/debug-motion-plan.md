---
linkTitle: "Debug a motion plan"
title: "Debug a motion plan"
weight: 10
layout: "docs"
type: "docs"
description: "Use the 3D scene to diagnose why a motion plan failed or produced unexpected results."
---

When a motion plan fails with a collision error or produces a path that does not look right, the 3D scene tab lets you see exactly what the planner sees: the arm's kinematic model, the obstacle geometry, and the frame positions that define the workspace.
Most motion planning failures come down to one of a few problems that are immediately visible in 3D.

## Prerequisites

- A machine with an arm or gantry configured and at least one frame defined.
- A motion plan that is failing or producing unexpected results.

## Diagnose the problem

### 1. Open the 3D scene tab

Navigate to your machine in the [Viam app](https://app.viam.com) and click the **3D scene** tab.
The scene loads your current frame system configuration.

If your machine is online, the scene also connects to it for live pose data.
If your machine is offline, the scene still renders the configured frame positions.

### 2. Check frame positions

Click through components in the tree view and verify that each one appears where you expect it in 3D space.
Common problems:

- **Component in the wrong location**: the translation values in the frame configuration do not match the physical setup. The details panel shows the local position in mm relative to the parent frame. Compare these to your physical measurements.
- **Component with wrong orientation**: the arm base is rotated 90 degrees, or a camera is pointing the wrong direction. Check the local orientation values in the details panel.
- **Wrong parent frame**: a component is attached to the wrong parent, placing it in an unexpected part of the scene. Check the parent frame field in the details panel.

### 3. Check obstacle geometry

Obstacles appear as translucent shapes in the scene.
Verify that:

- Every physical obstacle in your workspace has a corresponding geometry in the scene.
- Each geometry covers the actual physical object. If a box geometry is too small, the planner will find paths that clip the real obstacle.
- Geometries are positioned correctly. A table surface defined at `z: 0` when the arm base is at `z: 500` will not protect against table collisions.

If obstacles are missing or misplaced, see [Set up obstacle avoidance](/motion-planning/3d-scene/set-up-obstacle-avoidance/).

### 4. Look for impossible targets

If the motion plan target is outside the arm's reach or inside an obstacle, the planner cannot find a path.
Use the details panel to check the world position of the arm's end effector and compare it to your target pose.

If the target is inside an obstacle geometry, either move the target or adjust the obstacle definition.

### 5. Check for self-collision geometry

Some arm models include collision geometry for each link.
If a motion plan fails with a self-collision error, open the 3D scene to see whether the arm's own link geometries overlap in certain configurations.
This can happen when wrist joints are commanded to positions that bring adjacent links too close together.

## Common causes of motion plan failures

| Symptom                       | Likely cause                                  | What to check in 3D scene                                                  |
| ----------------------------- | --------------------------------------------- | -------------------------------------------------------------------------- |
| "no valid path found"         | Target unreachable or blocked by obstacles    | Is the target inside an obstacle? Is it within the arm's reach?            |
| Collision error               | Obstacle geometry intersects the planned path | Are obstacles positioned correctly? Are they the right size?               |
| Path goes through the table   | Table obstacle missing or too small           | Is there a geometry covering the table surface? Does it extend far enough? |
| Arm takes an unexpected route | Obstacles force the planner to go around      | Are there obstacles you did not intend to add? Is geometry oversized?      |
| Self-collision error          | Arm links collide with each other             | Do link geometries overlap in the failing configuration?                   |
