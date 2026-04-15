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

The motion service exposes the methods below for planning and executing component motion. Most methods are implemented only by module-based motion services; the builtin service supports `Move`, `DoCommand`, and `GetStatus`.

{{< readfile "/static/include/services/apis/generated/motion-table.md" >}}

For full method signatures, parameters, and code examples, see the
[auto-generated motion API reference](/reference/apis/services/motion/).

## Method overview

### Move

Plans and executes a motion to a destination pose. This is the primary method for arm and gantry planning.

Key parameters:

- `component_name`: the arm or gantry to move
- `destination`: a `PoseInFrame` specifying the target pose and reference frame
- `world_state`: optional obstacles and transforms
- `constraints`: optional linear, orientation, or collision constraints

### MoveOnMap

Plans and executes motion on a SLAM map.

### MoveOnGlobe

Plans and executes motion to a GPS coordinate. Use the [navigation service](/navigation/) for GPS-based navigation.

### GetPlan

Retrieves the plan for an executing motion.

### ListPlanStatuses

Lists all active and recently completed plan statuses.

### StopPlan

Stops an executing plan.

### GetPose (deprecated)

Returns a component's pose. Deprecated: the robot service's `GetPose` replaces it. (Python callers currently still use this motion-service method; see the frame system API reference.)

### DoCommand

Sends arbitrary commands. The builtin motion service supports `"plan"`,
`"execute"`, and `"executeCheckStart"` commands.

### GetStatus

Returns generic resource status for the motion service. Useful for liveness checks.
