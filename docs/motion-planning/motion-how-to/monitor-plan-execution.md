---
linkTitle: "Monitor execution"
title: "Monitor and control plan execution"
weight: 70
layout: "docs"
type: "docs"
description: "Track plan status, retrieve plan details, and stop executing plans."
---

You need to monitor whether a motion plan is still executing, check if it
succeeded or failed, or cancel it mid-execution.

## Important limitation

The builtin motion service does **not** support `GetPlan`, `ListPlanStatuses`,
or `StopPlan`. These methods return "not supported" errors. They are only
available from motion service implementations that support `MoveOnMap` or
`MoveOnGlobe` (typically provided by modules or the navigation service).

If you are using the builtin motion service with `Move()` for arms and gantries,
the `Move()` call blocks until the motion completes or fails. You do not need
to poll for status.

## Methods (when supported)

### GetPlan

Retrieves the plan being executed or most recently executed for a component.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient

motion_service = MotionClient.from_robot(machine, "my-motion-service")

response = await motion_service.get_plan(
    component_name="my-base",
)
plan_status = response.current_plan_with_status.status
print(f"Plan state: {plan_status.state}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
response, err := motionService.PlanHistory(ctx, motion.PlanHistoryReq{
    ComponentName: "my-base",
})
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Plan state: %v\n", response[0].StatusHistory[0].State)
```

{{% /tab %}}
{{< /tabs >}}

### ListPlanStatuses

Lists all active and recently completed plans.

{{< tabs >}}
{{% tab name="Python" %}}

```python
statuses = await motion_service.list_plan_statuses()
for s in statuses:
    print(f"Component: {s.component_name}, "
          f"State: {s.status.state}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
statuses, err := motionService.ListPlanStatuses(ctx, motion.ListPlanStatusesReq{})
if err != nil {
    logger.Fatal(err)
}
for _, s := range statuses {
    fmt.Printf("Component: %s, State: %v\n", s.ComponentName, s.Status.State)
}
```

{{% /tab %}}
{{< /tabs >}}

Plan states:

| State         | Meaning                                |
| ------------- | -------------------------------------- |
| `IN_PROGRESS` | Plan is currently executing.           |
| `STOPPED`     | Plan was stopped by a `StopPlan` call. |
| `SUCCEEDED`   | Plan completed successfully.           |
| `FAILED`      | Plan failed during execution.          |

### StopPlan

Cancels an executing plan for a component.

{{< tabs >}}
{{% tab name="Python" %}}

```python
await motion_service.stop_plan(
    component_name="my-base",
)
print("Plan stopped")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
err = motionService.StopPlan(ctx, motion.StopPlanReq{
    ComponentName: "my-base",
})
if err != nil {
    logger.Fatal(err)
}
fmt.Println("Plan stopped")
```

{{% /tab %}}
{{< /tabs >}}

## For builtin Move() calls

Since `Move()` blocks, handle errors directly:

{{< tabs >}}
{{% tab name="Python" %}}

```python
try:
    await motion_service.move(
        component_name="my-arm",
        destination=destination,
        world_state=world_state
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
    WorldState:    worldState,
})
if err != nil {
    fmt.Printf("Motion failed: %v\n", err)
} else {
    fmt.Println("Motion succeeded")
}
```

{{% /tab %}}
{{< /tabs >}}

## What's next

- [Motion Service Configuration](/motion-planning/reference/motion-service/):
  full configuration reference including DoCommand options.
- [Motion Service API](/motion-planning/reference/api/):
  complete API reference.
