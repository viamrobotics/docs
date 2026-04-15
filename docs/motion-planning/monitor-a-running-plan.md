---
linkTitle: "Monitor a running plan"
title: "Monitor a running plan"
weight: 80
layout: "docs"
type: "docs"
description: "Start a non-blocking motion plan and react to progress, completion, and failure."
aliases:
  - /motion-planning/motion-how-to/monitor-plan-execution/
  - /operate/mobility/monitor-plan-execution/
  - /motion-planning/motion-how-to/monitor-a-running-plan/
---

`MoveOnMap` and `MoveOnGlobe` return immediately with an `ExecutionID`.
The motion runs in the background; your code needs to monitor it and
react when it completes, fails, or needs to be stopped. This guide shows
the polling pattern for both Go and Python, and points out what changes
for the builtin `Move` case (which blocks).

## Before you start

- You need a motion service implementation that supports
  `MoveOnMap`/`MoveOnGlobe`. The built-in motion service does not — it
  returns "not supported" for these calls. The navigation service or a
  module that implements them is required.
- For background on the methods and states, see
  [Plan monitoring](/motion-planning/reference/plan-monitoring/).

## The polling pattern

1. Start a non-blocking motion. Save the returned `ExecutionID`.
2. Poll `GetPlan` on an interval, passing the component name and the
   `ExecutionID`.
3. Inspect the returned `current_plan_with_status.status.state`.
4. Exit the loop on any terminal state: `SUCCEEDED`, `STOPPED`, or
   `FAILED`.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from viam.services.motion import MotionClient
from viam.proto.common import GeoPoint
from viam.proto.service.motion import PlanState

motion_service = MotionClient.from_robot(machine, "my-motion-service")

# Start a non-blocking motion.
destination = GeoPoint(latitude=40.6640, longitude=-73.9387)
execution_id = await motion_service.move_on_globe(
    component_name="my-base",
    destination=destination,
    movement_sensor_name="my-gps",
)

# Poll until the plan reaches a terminal state.
terminal = {
    PlanState.PLAN_STATE_SUCCEEDED,
    PlanState.PLAN_STATE_STOPPED,
    PlanState.PLAN_STATE_FAILED,
}

while True:
    response = await motion_service.get_plan(
        component_name="my-base",
        execution_id=execution_id,
    )
    status = response.current_plan_with_status.status
    print(f"state={status.state} reason={status.reason or '-'}")
    if status.state in terminal:
        break
    await asyncio.sleep(1)

if status.state == PlanState.PLAN_STATE_SUCCEEDED:
    print("Arrived at destination")
else:
    print(f"Motion did not complete: {status.state}")
```

{{% /tab %}}
{{% tab name="Go" %}}

Go callers can either poll directly, or use the
`PollHistoryUntilSuccessOrError` helper that wraps the loop and returns
on the first terminal state.

```go
import (
    "context"
    "time"

    geo "github.com/kellydunn/golang-geo"
    "go.viam.com/rdk/services/motion"
)

// Start a non-blocking motion.
executionID, err := motionService.MoveOnGlobe(ctx, motion.MoveOnGlobeReq{
    ComponentName:      "my-base",
    Destination:        geo.NewPoint(40.6640, -73.9387),
    MovementSensorName: "my-gps",
})
if err != nil {
    logger.Fatal(err)
}

// Block until the plan reaches a terminal state.
err = motion.PollHistoryUntilSuccessOrError(
    ctx,
    motionService,
    time.Second,
    motion.PlanHistoryReq{
        ComponentName: "my-base",
        ExecutionID:   executionID,
    },
)
if err != nil {
    logger.Warnf("motion did not complete: %v", err)
} else {
    logger.Info("Arrived at destination")
}
```

{{% /tab %}}
{{< /tabs >}}

## Stop a running plan

Call `StopPlan` with the component name to cancel an in-progress motion.
The plan's final state becomes `STOPPED`.

{{< tabs >}}
{{% tab name="Python" %}}

```python
await motion_service.stop_plan(component_name="my-base")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err = motionService.StopPlan(ctx, motion.StopPlanReq{ComponentName: "my-base"})
```

{{% /tab %}}
{{< /tabs >}}

## Replanning and ExecutionID

If the motion service replans during execution (for example, after the
robot deviates from the path), it creates a new `Plan` but keeps the
same `ExecutionID`. This means:

- `GetPlan` with the `ExecutionID` returns the latest plan in
  `current_plan_with_status` and earlier plans in `replan_history`.
- Polling the `execution_id` continues to work across replans.
- The plan state transitions you observe reflect the most recent plan.

## List plans across components

To see every plan currently running or recently completed on the
machine, call `ListPlanStatuses`. Useful for dashboards or for stopping
every component in one pass.

{{< tabs >}}
{{% tab name="Python" %}}

```python
statuses = await motion_service.list_plan_statuses()
for s in statuses:
    print(f"{s.component_name}: {s.status.state}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
statuses, err := motionService.ListPlanStatuses(ctx, motion.ListPlanStatusesReq{})
if err != nil {
    logger.Fatal(err)
}
for _, s := range statuses {
    logger.Infof("%s: %v", s.ComponentName, s.Status.State)
}
```

{{% /tab %}}
{{< /tabs >}}

Only plans from in-progress executions or executions that reached a
terminal state in the last 24 hours are returned. After the TTL expires
or if `viam-server` reinitializes, older plans are no longer available.

## If you are using the builtin Move instead

The builtin motion service's `Move` call blocks until the motion
completes or fails. Polling is not needed; handle the return value
directly.

{{< tabs >}}
{{% tab name="Python" %}}

```python
try:
    await motion_service.move(
        component_name="my-arm",
        destination=destination,
    )
    print("Motion succeeded")
except Exception as e:
    print(f"Motion failed: {e}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
_, err = motionService.Move(ctx, motion.MoveReq{
    ComponentName: "my-arm",
    Destination:   destination,
})
if err != nil {
    logger.Warnf("motion failed: %v", err)
} else {
    logger.Info("motion succeeded")
}
```

{{% /tab %}}
{{< /tabs >}}

## What's next

- [Plan monitoring](/motion-planning/reference/plan-monitoring/):
  method, type, and state reference.
- [Navigate to a waypoint](/navigation/how-to/navigate-to-waypoint/):
  end-to-end example using the navigation service, which internally
  uses `MoveOnGlobe` and exposes its own progress API.
- [Move an arm to a pose](/motion-planning/move-an-arm/move-to-pose/):
  the builtin `Move` equivalent for arms and gantries.
