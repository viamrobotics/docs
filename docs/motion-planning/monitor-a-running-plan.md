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

`MoveOnMap` and `MoveOnGlobe` return immediately with an `ExecutionID` and run
the actual motion in the background. Your code has to poll that execution to
learn when it completes, fails, or stops. This page gives the polling pattern
in Go and Python.

Neither RPC is implemented by the built-in motion service: the built-in
returns "not supported" for both. You need the
[navigation service](/navigation/), which calls `MoveOnGlobe` internally,
or a motion-service module that provides them. If you are using the
built-in `Move` instead (which blocks until completion), skip to the
last section.

For background on the methods and states, see
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

### Safety-stop pattern

A non-blocking motion runs independently of your polling loop. Treat `StopPlan`
as the cut-off switch: any condition your application reads (a safety
button, an external sensor, a higher-level task abort) should call
`StopPlan` directly without waiting for the polling loop to notice. Run
the safety check and the polling loop concurrently so either can call
`StopPlan` without waiting on the other.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# `safety_condition_triggered()` is your application-specific check
# (a button, a sensor reading, an external abort signal).
async def watch_for_abort(motion_service, component_name):
    while True:
        if await safety_condition_triggered():
            await motion_service.stop_plan(component_name=component_name)
            return
        await asyncio.sleep(0.1)

# Run the poll loop and the watchdog concurrently. The first task to
# finish wins; cancel the other so it does not run forever.
poll_task = asyncio.create_task(
    poll_until_terminal(motion_service, "my-base", execution_id)
)
watch_task = asyncio.create_task(
    watch_for_abort(motion_service, "my-base")
)
done, pending = await asyncio.wait(
    {poll_task, watch_task}, return_when=asyncio.FIRST_COMPLETED,
)
for task in pending:
    task.cancel()
```

Wrap the polling logic in `poll_until_terminal(motion_service, component_name, execution_id)` (the `while True` body from the polling pattern above).

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Run the poll loop and the watchdog in separate goroutines.
watchCtx, cancelWatch := context.WithCancel(ctx)
defer cancelWatch()

go func() {
    ticker := time.NewTicker(100 * time.Millisecond)
    defer ticker.Stop()
    for {
        select {
        case <-watchCtx.Done():
            return
        case <-ticker.C:
            if safetyConditionTriggered() {
                _ = motionService.StopPlan(ctx, motion.StopPlanReq{
                    ComponentName: "my-base",
                })
                return
            }
        }
    }
}()
```

{{% /tab %}}
{{< /tabs >}}

After `StopPlan` returns, the plan's terminal state transitions to
`STOPPED`. The polling loop then exits on the next `GetPlan` cycle. If
you call `StopPlan` after a plan has already reached a terminal state,
behavior depends on the module; check the motion-service module's docs.

## Replanning and ExecutionID

If the motion service replans during execution (for example, after the
robot deviates from the path), it creates a new `Plan` but keeps the
same `ExecutionID`. This means:

- `GetPlan` with the `ExecutionID` returns the latest plan in
  `current_plan_with_status` and earlier plans in `replan_history`.
- Polling the `execution_id` continues to work across replans.
- The plan state transitions you observe reflect the most recent plan.

## List plans across components

`ListPlanStatuses` returns every plan currently running or recently completed
on the machine, keyed by component name. Two common uses: a dashboard that
shows all in-progress motion at once, and a shutdown routine that stops every
component without having to track the `ExecutionID` of each one.

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

`ListPlanStatuses` has a 24-hour retention window. Plans from executions that
reached a terminal state more than 24 hours ago are dropped from the list, and
any restart of `viam-server` clears the history regardless of age. If you need
longer-lived plan audit, log the `ExecutionID` and plan state to your own
store at each poll.

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
