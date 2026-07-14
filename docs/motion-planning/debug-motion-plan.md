---
linkTitle: "Debug a motion plan"
title: "Debug a motion plan"
weight: 84
layout: "docs"
type: "docs"
description: "Find why a motion plan failed or moved unexpectedly by inspecting frames, obstacles, and reach, either visually in the 3D scene or from the command line with the Viam CLI."
aliases:
  - /motion-planning/3d-scene/debug-motion-plan/
  - /motion-planning/debug-motion-with-cli/
  - /motion-planning/motion-how-to/debug-motion-with-cli/
---

When a motion plan fails with a collision error, or the arm ends up somewhere unexpected,
the first question is the same: is the frame system wrong, or is the plan wrong? You can
answer it two ways. If your machine has the **3D SCENE** tab, inspect the world the planner
sees by eye. From any shell, the Viam CLI reports the same frame poses and tests
reachability. This page covers both.

To render the plan's trajectory itself, the path the arm takes from start to goal, see
[Visualize a motion plan](/motion-planning/visualize-a-motion-plan/).

## Prerequisites

- A machine with an arm or gantry configured and at least one frame defined.
- A motion plan that is failing or producing unexpected results.
- For the CLI checks: the Viam CLI installed and authenticated, and the `--part` identifier
  for the machine part you want to inspect.

## In the 3D scene

Open the **3D SCENE** tab on your machine's page in the [Viam app](https://app.viam.com). It
loads your frame system configuration and, when the machine is online, connects for live
pose data. Work through the checks below; most planning failures show up in one of them.

### Check frame positions

In the **World** panel in the upper-left, expand the tree and click each component in turn.
The Details panel on the right shows the selected entity's **world position** and **world
orientation**, plus editable **local position** and **local orientation** relative to the
parent frame. Compare these values to your physical measurements.

Three common mismatches to look for:

- **Wrong location**: translation values in the frame configuration do not match the physical setup. Compare **local position** (mm) to your physical measurements.
- **Wrong orientation**: the arm base is rotated 90 degrees, or a camera points the wrong direction. Check **local orientation** in the Details panel.
- **Wrong parent**: the component is attached to the wrong parent, which places it in an unexpected part of the scene. Check the **parent frame** field in the Details panel.

### Check obstacle geometry

Obstacles appear as translucent shapes in the scene and as child rows under their parent
frame in the **World** panel. Select each obstacle from the tree to see its **geometry** type
and **dimensions** in the Details panel.

Verify that:

- Every physical obstacle in your workspace has a corresponding geometry in the scene.
- Each geometry covers the actual physical object. If a box geometry is too small, the
  planner will find paths that clip the real obstacle.
- Geometries are positioned correctly. A table surface defined at `z: 0` when the arm base
  is at `z: 500` will not protect against table collisions.

If obstacles are missing or misplaced, see
[Verify obstacles](/motion-planning/obstacles/verify-obstacles/).

### Look for impossible targets

If the motion plan target is outside the arm's reach or inside an obstacle, the planner
cannot find a path.

In the **World** panel, expand the arm and select its tip link or the gripper frame
(whichever is configured as the motion target). Read the **world position** and compare it to
the target pose your code commanded. Then place the target: is it inside an obstacle
geometry? Is it further than the arm can reach from its base?

If the target is inside an obstacle geometry, either move the target or adjust the obstacle
definition.

### Check for self-collision geometry

Some arm models include collision geometry for each link. If a motion plan fails with a
self-collision error, inspect the arm's link geometries for overlap in the current
configuration.

If the arm renders without collision geometry, the feature may be disabled: open **Settings →
Scene → Arm Models** and verify that the rendering mode includes colliders.

Self-collisions can happen when wrist joints are commanded to positions that bring adjacent
links too close together. If the overlap is a modeling artifact rather than a real collision,
allow the frame pair with
[`CollisionSpecification`](/motion-planning/obstacles/allow-frame-collisions/).

## With the CLI

When the 3D scene tab is not available, or you want to script the checks, the Viam CLI
reports the same information from the shell. Three commands cover most cases: `print-config`
dumps the configured frame tree, `print-status` prints every frame's current world-frame
pose, and `set-pose` drives a component to a pose to test reachability. For the full flag
reference, see [Motion CLI commands](/motion-planning/reference/cli-commands/).

### Frames are in the wrong place

The arm reports reaching `x=300, y=200` but physically sits elsewhere, or the
scene shows the gripper off to the side of the arm. Both symptoms point to a frame
configuration that disagrees with the physical setup. Dump the configured frame tree:

```sh
viam machines part motion print-config --part "my-machine-main"
```

Each frame part shows its name, parent, translation, and orientation. Compare against your
JSON configuration and physical measurements. Common issues: a **wrong parent** (a component
parented to the world frame instead of the arm, or vice versa), **wrong units** (centimeters
instead of millimeters), or a **missing frame** (a component with no entry, usually because
its frame configuration did not save).

Then check the live world-frame poses:

```sh
viam machines part motion print-status --part "my-machine-main"
```

`print-status` prints one line per frame part with its computed world-frame pose:

```text
        my-arm : X:    0.00 Y:    0.00 Z:    0.00 OX:   0.00 OY:   0.00 OZ:   1.00 Theta:   0.00
    my-gripper : X:    0.00 Y:    0.00 Z:  110.00 OX:   0.00 OY:   0.00 OZ:   1.00 Theta:  90.00
```

A pose that does not match where the component physically sits means the frame configuration
is wrong. Edit the configuration in the Viam app, then run both commands again to confirm the
change took effect.

### Find where one component is

To read a single component's pose without the rest of the frame tree:

```sh
viam machines part motion get-pose \
    --part "my-machine-main" \
    --component "my-arm"
```

The output is the same single-line format as `print-status`, limited to the component. This
is useful for scripting: log it, compare between runs, or read the arm's position before and
after a physical move to check it matches what the arm reports.

### Check whether a target pose is reachable

Drive toward the target in small steps to find where planning fails. First read the current
pose with `get-pose`, then move a small distance:

```sh
viam machines part motion set-pose \
    --part "my-machine-main" \
    --component "my-arm" \
    --x 100
```

`set-pose` overrides only the fields you pass, so this moves the arm to `X=100` while keeping
the current Y, Z, and orientation. If this small step fails, the planner cannot reach any pose
near the current position, which usually means a configuration error rather than a
target-reachability issue. If it succeeds, increase the delta and work toward the pose you
want. The last successful pose and the first failing pose bracket the problem. If `set-pose`
fails at a pose that should be reachable, return to `print-config` and `print-status`: frame
configuration errors often show up as unexpected unreachability.

### The arm moved to the wrong place after a motion call

Your code called `motion.Move` or `arm.MoveToPosition` and the arm ended up somewhere other
than the commanded pose. Immediately after the motion, capture the actual final pose with
`get-pose` and compare it to the pose you commanded. Differences beyond the arm's positioning
tolerance suggest a frame configuration mismatch or a kinematics calibration problem.

If `print-status` shows the arm where it physically is but that does not match the pose you
commanded, the pose may have been interpreted in an unexpected reference frame. Check the
`reference_frame` on the target `PoseInFrame`: the same `(x, y, z)` in the arm's frame and in
the world frame describes two different places.

The CLI commands `print-status`, `get-pose`, and `set-pose` call the motion service's
`GetPose`, which is deprecated in favor of the frame system service's `GetPose`; the
commands and their output format are stable.
`set-pose` calls the motion service's `Move` and blocks until the motion finishes or fails,
returning a non-zero exit status with the error message on failure.

## Common causes of motion plan failures

| Symptom                       | Likely cause                                  | What to check                                                              |
| ----------------------------- | --------------------------------------------- | -------------------------------------------------------------------------- |
| "no valid path found"         | Target unreachable or blocked by obstacles    | Is the target inside an obstacle? Is it within the arm's reach?            |
| Collision error               | Obstacle geometry intersects the planned path | Are obstacles positioned correctly? Are they the right size?               |
| Path goes through the table   | Table obstacle missing or too small           | Is there a geometry covering the table surface? Does it extend far enough? |
| Arm takes an unexpected route | Obstacles force the planner to go around      | Are there obstacles you did not intend to add? Is geometry oversized?      |
| Self-collision error          | Arm links collide with each other             | Do link geometries overlap in the failing configuration?                   |

## What's next

- [Visualize a motion plan](/motion-planning/visualize-a-motion-plan/):
  render the plan's trajectory and goals as custom visuals when a visual check is not enough.
- [Verify obstacles](/motion-planning/obstacles/verify-obstacles/):
  check obstacle geometry against the real workspace.
- [Motion CLI commands](/motion-planning/reference/cli-commands/):
  the full flag reference for the motion commands.
- [How motion planning works](/motion-planning/how-planning-works/):
  why a plan can be infeasible and what to adjust.
