---
linkTitle: "Replanning"
title: "Replanning behavior by method"
weight: 50
layout: "docs"
type: "docs"
description: "Which motion service methods replan during execution, when, and why. The single most common mental-model mismatch for new users."
---

A common expectation for new users is that "obstacle avoidance" means
the planner re-evaluates the world continuously while the robot moves.
In Viam's motion service, whether the planner replans depends entirely
on which method you called. `Move` never replans. `MoveOnGlobe` and
`MoveOnMap` do, on clear triggers. This page is the reference for that
distinction.

## At a glance

| Method        | Replans during execution? | Triggers replan                                                   |
| ------------- | :-----------------------: | ----------------------------------------------------------------- |
| `Move`        |            No             | —                                                                 |
| `MoveOnGlobe` |            Yes            | Deviation beyond `plan_deviation_m`, or a new transient obstacle. |
| `MoveOnMap`   |            Yes            | Same as `MoveOnGlobe`.                                            |

Modules that implement their own motion service may choose different
behavior. This page describes the built-in motion service.

## Move: plan once, execute

`Move` is synchronous. The planner:

1. Reads the current component pose and the frame system.
2. Uses the provided `WorldState` (obstacles + supplemental transforms)
   as the static picture of the world.
3. Runs cBiRRT to produce a complete joint-level path from current pose
   to the target.
4. Smooths the path.
5. Executes it to completion.

There is **no loop** between steps 1-5 during execution. If an obstacle
moves into the arm's path after planning, the arm keeps going. If a
vision service reports a new obstacle, `Move` does not see it. The path
the planner chose at step 3 is the path the arm follows.

**Implications:**

- Obstacles must be known at the moment of the call. Everything you pass
  through `WorldState` is the planner's view of the world.
- Dynamic obstacle avoidance is the caller's responsibility. If you need
  it with `Move`, check the world between calls, then call `Move` again
  with the updated `WorldState`.
- The "collision check" the planner performs is against the geometries
  you passed, not against live sensor data.

## MoveOnGlobe and MoveOnMap: plan, monitor, replan

`MoveOnGlobe` and `MoveOnMap` are non-blocking. They return immediately
with an `ExecutionID`. The motion service then runs a control loop that
continues until the robot reaches the destination, fails, or is
stopped:

1. Plan the current leg based on current position and known obstacles.
2. Start executing.
3. Poll the movement sensor (or SLAM service, when `MoveOnMap` is
   used) at `position_polling_frequency_hz` to track the robot's
   position. If the frequency is unset, the implementation chooses a
   rate.
4. Poll each configured `obstacle_detector` at
   `obstacle_polling_frequency_hz` for transient obstacles.
5. If the robot drifts more than `plan_deviation_m` from the current
   plan, or a new obstacle is reported, generate a new plan with the
   updated world state.
6. Continue.

A replan creates a **new `Plan`** but keeps the same `ExecutionID`. You
can observe this through
[`GetPlan`](/motion-planning/reference/plan-monitoring/#getplan): the
current plan is in `current_plan_with_status`; prior plans are in
`replan_history`.

## Triggers in detail

### Deviation from plan

Set by `plan_deviation_m` in the `MotionConfiguration`. Default is
2.6 m for `MoveOnGlobe` and 1.0 m for `MoveOnMap`. When the robot's
reported position is farther than this threshold from the nearest
point on the current plan, the service triggers a replan.

Tune this relative to your movement sensor's accuracy. Standard GPS
gives ~3 m of drift, so a 2.6 m deviation threshold produces frequent
replans. Raise the threshold for standard GPS, lower it for RTK.

### Transient obstacles

Each `obstacle_detector` is a vision service plus camera pair. The
motion service queries each pair at
`obstacle_polling_frequency_hz`. When a new obstacle appears in a
detection result, the motion service transforms the obstacle into the
planner's frame, then triggers a replan that accounts for it.

Detectors are only active during execution. They do not contribute to
initial planning; that picture of the world comes from the obstacles
you passed in the request or configured statically on the machine.

### Replan cost factor (navigation service only)

When the navigation service drives a base through `MoveOnGlobe`, its
`replan_cost_factor` attribute multiplies the cost of the current plan
before comparing it to a candidate replan. Higher values prefer the
current plan (less eager to replan); lower values replan more
aggressively. See
[Navigation service configuration](/navigation/reference/navigation-service/).

## What replanning does not do

Several things users reasonably expect from "replanning" that Viam's
motion service does not do:

- **Replan across arm `Move` calls.** `Move` is single-shot. There is
  no `MoveOnArm` equivalent that loops.
- **Replan on ambient sensor changes.** Only the configured detectors
  contribute to replanning. Data from sensors not in the
  `obstacle_detectors` list does not reach the planner during
  execution.
- **Undo completed motion.** Replanning generates a new plan from the
  robot's current position. If the robot has already passed through an
  area and conditions changed behind it, the new plan starts from
  where the robot is, not from the original start.
- **Replace a failed plan.** If the planner cannot find a path from
  the robot's current position (after a deviation or obstacle trigger),
  the execution transitions to `FAILED` rather than trying different
  approaches automatically.

## Practical consequences

Because `Move` does not replan, arm motion through the motion service
gives you predictable, committed paths. If you need dynamic obstacle
avoidance for an arm, you build it in application code: monitor the
world, call `Move` with a new `WorldState`. The motion service does
not do this for you.

`MoveOnGlobe` and `MoveOnMap` replan during execution. That makes base
navigation resilient to changing conditions but harder to reason about
offline: `GetPlan` can return different answers a second apart.

## What's next

- [Monitor a running plan](/motion-planning/motion-how-to/monitor-a-running-plan/):
  observe plan state transitions including replans.
- [Plan monitoring](/motion-planning/reference/plan-monitoring/):
  reference for `GetPlan`, `ListPlanStatuses`, and `StopPlan`.
- [MotionConfiguration](/motion-planning/reference/motion-configuration/):
  the per-call options that tune replanning, including
  `plan_deviation_m` and polling frequencies.
- [How motion planning works](/motion-planning/how-planning-works/):
  the planning algorithm that runs before execution, and what it does
  not do.
