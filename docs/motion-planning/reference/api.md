---
linkTitle: "API"
title: "Motion service API"
weight: 20
layout: "docs"
type: "docs"
description: "The motion service API for planning and executing component movements."
aliases:
  - /reference/apis/services/motion/
  - /appendix/apis/services/motion/
---

The motion service exposes the methods below for planning and executing component motion. Most methods are implemented only by module-based motion services. The builtin service implements `Move`, `GetPose` (deprecated), `DoCommand`, and `GetStatus`.

`MoveOnMap`, `MoveOnGlobe`, `StopPlan`, `ListPlanStatuses`, and `GetPlan` return a `not supported by builtin` error; module-based motion services may implement them.

{{< readfile "/static/include/services/apis/generated/motion-table.md" >}}

For full method signatures, parameters, and code examples, see the
[auto-generated motion API reference](/reference/apis/services/motion/).

## Method overview

### Move

Plans and executes a motion to a destination pose. This is the primary method for arm and gantry planning.

Key parameters:

- `component_name`: the component to move (typically an arm or gantry in this section's examples)
- `destination`: a `PoseInFrame` specifying the target pose and reference frame
- `world_state`: optional obstacles and transforms
- `constraints`: optional linear, orientation, or collision constraints

### MoveOnMap, MoveOnGlobe, StopPlan, ListPlanStatuses, and GetPlan

Navigate mobile bases and manage the resulting plans. The builtin motion service returns a `not supported by builtin` error for each of these methods (for example, `MoveOnMap not supported by builtin`); module-based motion services implement them.

### GetPose (deprecated)

Returns a component's pose. Deprecated in favor of the robot service's `GetPose`. Python callers still use this motion-service method today; see the [Frame system API reference](/motion-planning/reference/frame-system-api/).

### DoCommand

Sends arbitrary commands. The builtin motion service supports a `"plan"`
command (returns a trajectory without executing it), an `"execute"` command
(runs a trajectory; add the `"executeCheckStart"` key to an execute request
to verify the resource is at the trajectory's start first), and the teleop
commands (`teleop_start`, `teleop_move`, `teleop_stop`, and `teleop_status`).

### GetStatus

Returns generic resource status for the motion service. `GetStatus` is a common resource RPC, so the generated table above omits it. Use it for liveness checks.
