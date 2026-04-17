---
linkTitle: "Plan monitoring"
title: "Plan monitoring reference"
weight: 35
layout: "docs"
type: "docs"
description: "Reference for the motion service methods, types, and states used to track long-running motion plans."
---

`MoveOnMap` and `MoveOnGlobe` return immediately; the actual motion runs in the background. To monitor and control a running plan, callers use `GetPlan`, `ListPlanStatuses`, and `StopPlan`, backed by the `Plan`, `PlanStatus`, and `PlanState` types. This page lists those methods, types, and the state machine that ties them together.

## Which implementations track plans

| Motion service implementation                       | Tracks plans?                                                             |
| --------------------------------------------------- | ------------------------------------------------------------------------- |
| Builtin                                             | No. `Move` is synchronous; the plan-tracking RPCs return "not supported". |
| Modules that implement `MoveOnGlobe` or `MoveOnMap` | Yes (typical case).                                                       |

If you are using navigation: the navigation service uses a motion
service internally. When you configure navigation with a plan-tracking
motion service, navigation's own `GetPaths`, `GetLocation`, and mode
transitions expose progress without calling `GetPlan` directly.

## PlanState

Plans move through a well-defined state machine.

| State         | Terminal | Meaning                                                                   |
| ------------- | :------: | ------------------------------------------------------------------------- |
| `IN_PROGRESS` |    No    | Plan is currently executing.                                              |
| `STOPPED`     |   Yes    | Plan was stopped by a `StopPlan` call.                                    |
| `SUCCEEDED`   |   Yes    | Robot reached the destination successfully.                               |
| `FAILED`      |   Yes    | Plan failed during execution. The status `reason` field may describe why. |

An `UNSPECIFIED` state exists in the proto but should never be observed in
practice.

## Types

- **`Plan`** — unique `id`, owning `component_name`, `execution_id`, and a
  list of `PlanStep` entries (pose targets per component).
- **`PlanStatus`** — `state`, `timestamp`, optional `reason` string (used
  for replan reasons on `IN_PROGRESS` transitions and error messages on
  `FAILED`).
- **`PlanStatusWithID`** — a `PlanStatus` plus the `plan_id`,
  `execution_id`, and `component_name` it applies to.
- **`PlanWithStatus`** — a `Plan` plus its current `status` and the prior
  `status_history`.

## Methods

### GetPlan

Returns the plan (or plans, if replanned) for the most recent execution
of a component.

| Parameter        | Description                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| `component_name` | The component whose plan is requested.                                               |
| `last_plan_only` | If true, returns only the latest plan for the execution. Default false.              |
| `execution_id`   | Optional. Request plans from a specific prior execution rather than the most recent. |

Returns a `current_plan_with_status` and, if the execution was replanned,
a `replan_history` of earlier plans. If there is no matching execution
within the TTL, returns an error.

### ListPlanStatuses

Returns the statuses of all plans whose execution is in progress or
changed state within the last 24 hours. Supports `only_active_plans` to
filter to running executions.

### StopPlan

Stops the currently executing plan for a component. Takes effect at the
next planner tick; the plan's final state becomes `STOPPED`.

## ExecutionID

Every `MoveOnGlobe` or `MoveOnMap` call returns a unique `ExecutionID`.
When the motion service replans mid-execution (for example, after a
deviation), it creates a new `Plan` but the `ExecutionID` stays the
same. This lets callers query the full plan history for one execution.

## Plan TTL

Plans and statuses are retained for 24 hours after they reach a terminal
state, or until `viam-server` reinitializes (whichever comes first).
After the TTL, `GetPlan` and `ListPlanStatuses` no longer return them.

## Go polling helper

The Go SDK provides a convenience helper for callers that want to block
until a non-blocking plan completes:

```go
import (
    "context"
    "time"

    "go.viam.com/rdk/services/motion"
)

err := motion.PollHistoryUntilSuccessOrError(
    ctx,
    motionService,
    time.Second,
    motion.PlanHistoryReq{
        ComponentName: "my-base",
        ExecutionID:   executionID,
    },
)
```

The helper polls `PlanHistory` at the given interval and returns `nil`
when the state reaches `SUCCEEDED`, or an error if the state reaches
`STOPPED` or `FAILED`.

The Python SDK has no equivalent helper, so Python callers poll `get_plan` in a loop; [Monitor a running plan](/motion-planning/monitor-a-running-plan/) shows the pattern.

## What's next

- [Monitor a running plan](/motion-planning/monitor-a-running-plan/):
  start a non-blocking motion and react to state changes.
- [Motion service API](/motion-planning/reference/api/): the full motion
  service method list.
- [Motion service configuration](/motion-planning/reference/motion-service/):
  which methods the builtin implementation supports.
