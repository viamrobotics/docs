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

The motion service API supports the following methods:

{{< readfile "/static/include/services/apis/generated/motion-table.md" >}}

For full method signatures, parameters, and code examples, see the
[auto-generated motion API reference](/reference/apis/services/motion/).

## Method overview

### Move

Plans and executes a motion for a component to a destination pose. This is the
primary method for arm and gantry motion planning.

**Supported by:** builtin motion service.

Key parameters:

- `component_name`: the arm or gantry to move
- `destination`: a `PoseInFrame` specifying the target pose and reference frame
- `world_state`: optional obstacles and transforms
- `constraints`: optional linear, orientation, or collision constraints

### MoveOnMap

Plans and executes motion on a SLAM map.

**Not supported by** the builtin motion service. Requires a module
implementation.

### MoveOnGlobe

Plans and executes motion to a GPS coordinate.

**Not supported by** the builtin motion service. Use the
[navigation service](/navigation/) for GPS-based navigation.

### GetPlan

Retrieves the plan for an executing motion.

**Not supported by** the builtin motion service.

### ListPlanStatuses

Lists all active and recently completed plan statuses.

**Not supported by** the builtin motion service.

### StopPlan

Stops an executing plan.

**Not supported by** the builtin motion service.

### GetPose (deprecated)

Gets the pose of a component. Use `robot.GetPose()` instead.

### DoCommand

Sends arbitrary commands. The builtin motion service supports `"plan"`,
`"execute"`, and `"executeCheckStart"` commands.

### GetStatus

Returns generic resource status for the motion service. Useful for liveness
checks.

**Supported by** the builtin motion service.
