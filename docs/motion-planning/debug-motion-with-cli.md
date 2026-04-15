---
linkTitle: "Debug motion with the CLI"
title: "Debug motion with the Viam CLI"
weight: 75
layout: "docs"
type: "docs"
description: "Diagnose frame configuration and motion issues from the command line using the Viam CLI motion commands."
aliases:
  - /motion-planning/motion-how-to/debug-motion-with-cli/
---

When a motion plan fails or the arm ends up somewhere you did not
expect, the Viam CLI can answer the first round of diagnostic questions
without writing code: is the frame system configured the way I think it
is? Where is each component in the world frame right now? Can the
motion service reach this pose at all?

This guide walks through the most common debugging flows. For the
visual equivalent on machines where the **3D scene** tab is available,
see [Debug a motion plan](/motion-planning/3d-scene/debug-motion-plan/).
For the dry command reference, see
[Motion CLI commands](/motion-planning/reference/cli-commands/).

## Before you start

- The Viam CLI installed and authenticated.
- A machine with configured components and at least one frame defined.
- The `--part` identifier for the machine part you want to inspect.

## Symptom: the frame system does not match my configuration

You configured translations and orientations, but the resulting frame
layout does not match your physical setup.

### 1. Dump the configured frame system

```sh
viam machines part motion print-config --part "my-machine-main"
```

Read through the output. Each frame part shows its name, parent,
translation, and orientation. Compare against your JSON configuration
and against physical measurements.

Common issues you will catch at this step:

- **Wrong parent**: a component you intended to attach to the arm is
  parented to the world frame (or vice versa).
- **Wrong units**: translations expressed in centimeters rather than
  millimeters.
- **Missing frames**: a component that should have a frame has no entry
  in the output at all, which usually means its frame configuration did
  not save.

### 2. Check the live world-frame poses

```sh
viam machines part motion print-status --part "my-machine-main"
```

The output is every frame part and its computed world-frame pose:

```text
         my-arm : X:    0.00 Y:    0.00 Z:    0.00 OX:   0.00 OY:   0.00 OZ:   1.00 Theta:   0.00
    my-gripper : X:    0.00 Y:    0.00 Z:  110.00 OX:   0.00 OY:   0.00 OZ:   1.00 Theta:  90.00
```

Compare these poses against where each component physically is. A
mismatch means the frame configuration is wrong.

### 3. Adjust the config and re-check

Edit the frame configuration in the Viam app. Run `print-config` and
`print-status` again to confirm the change took effect.

## Symptom: I need to know where one component is right now

You want a single component's pose without the rest of the frame tree.

```sh
viam machines part motion get-pose \
    --part "my-machine-main" \
    --component "my-arm"
```

Output is the same single-line format as `print-status`, limited to
the specified component.

This is useful for scripting: pipe the output to a log, compare between
runs, or read the arm's position before and after a physical move to
verify it matches what the arm reports.

## Symptom: I am not sure if a target pose is reachable

Write the target pose in world coordinates and try to drive there.

### 1. Read the current pose

```sh
viam machines part motion get-pose \
    --part "my-machine-main" \
    --component "my-arm"
```

Note the X, Y, Z values.

### 2. Move a small delta

Start with a small step from the current pose. This isolates "can I
move at all?" from "is my target reachable?".

```sh
viam machines part motion set-pose \
    --part "my-machine-main" \
    --component "my-arm" \
    --x 100
```

`set-pose` overrides only the fields you pass. In this example, it
moves the arm to X=100 while keeping the current Y, Z, and orientation.

### 3. Move toward the real target incrementally

If the small step succeeds, increase the delta. Work toward the pose
you ultimately want. If an intermediate step fails, the last successful
pose and the first failing pose bracket the problem: the planner can
reach the first but not the second.

### 4. Compare against the frame system

If `set-pose` fails at a pose that should be reachable, return to
`print-config` and `print-status` to check whether the planner's view
of the arm's location matches reality. Frame configuration errors
often manifest as unexpected unreachability.

## Symptom: the arm moved to the wrong place after a motion call

Your code called `motion.Move` or `arm.MoveToPosition` and the arm
ended up somewhere other than the commanded pose.

### 1. Capture the actual final pose

Immediately after the motion completes:

```sh
viam machines part motion get-pose \
    --part "my-machine-main" \
    --component "my-arm"
```

Compare this to the pose you commanded. Differences that exceed the
arm's positioning tolerance suggest either a frame configuration
mismatch or a kinematics calibration problem.

### 2. Cross-check with arm joint values

The arm's own `GetJointPositions` reports joint angles. For a built-in
arm model, you can verify those match the expected kinematic solution
for the commanded pose. A large offset between forward-kinematic
prediction and reality points to incorrect kinematic parameters.

### 3. If frames look correct, look at the target

If `print-status` shows the arm where it physically is, but that does
not match the pose you commanded, the pose you commanded may have been
interpreted in an unexpected reference frame. Double-check the
`reference_frame` on the target `PoseInFrame`: the same `(x, y, z)` in
the arm's frame and in the world frame describes two different places.

## Limitations

- The CLI commands use the deprecated `Motion.GetPose` RPC internally
  for `print-status`, `get-pose`, and `set-pose`. They still work
  today, but `Robot.GetPose` is the long-term API. The CLI output is
  unaffected; only the internal call path is deprecated.
- `set-pose` calls the motion service's `Move`, which blocks until the
  motion completes or fails. Plan failures surface as the CLI returning
  a non-zero exit status with an error message. Collect that message as
  the starting point for the rest of your debugging.
- The CLI does not currently report plan state (`PlanState`), plan
  history, or replan reasons. For non-blocking executions, see
  [Monitor a running plan](/motion-planning/motion-how-to/monitor-a-running-plan/).

## What's next

- [Motion CLI commands](/motion-planning/reference/cli-commands/): the
  full flag reference.
- [Frame system](/motion-planning/frame-system/): the concept these
  commands inspect.
- [Debug a motion plan](/motion-planning/3d-scene/debug-motion-plan/):
  the 3D-scene equivalent when your machine has the visualization tab.
- [How motion planning works](/motion-planning/how-planning-works/):
  understand when the planner fails and what the failure means.
