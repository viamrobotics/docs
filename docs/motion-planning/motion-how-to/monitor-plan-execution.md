---
linkTitle: "Monitor Execution"
title: "Monitor and Control Plan Execution"
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

plan = await motion_service.get_plan(
    component_name=base_name,
)
print(f"Plan status: {plan.status}")
```

{{% /tab %}}
{{< /tabs >}}

### ListPlanStatuses

Lists all active and recently completed plans.

{{< tabs >}}
{{% tab name="Python" %}}

```python
statuses = await motion_service.list_plan_statuses()
for status in statuses:
    print(f"Component: {status.component_name}, "
          f"Status: {status.state}")
```

{{% /tab %}}
{{< /tabs >}}

Plan states:

| State | Meaning |
|-------|---------|
| `IN_PROGRESS` | Plan is currently executing. |
| `STOPPED` | Plan was stopped by a `StopPlan` call. |
| `SUCCEEDED` | Plan completed successfully. |
| `FAILED` | Plan failed during execution. |

### StopPlan

Cancels an executing plan for a component.

{{< tabs >}}
{{% tab name="Python" %}}

```python
await motion_service.stop_plan(
    component_name=base_name,
)
print("Plan stopped")
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
        component_name=arm_name,
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
    ComponentName: armName,
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

## What's Next

- [Motion Service Configuration](/motion-planning/reference/motion-service/):
  full configuration reference including DoCommand options.
- [Motion Service API](/motion-planning/reference/api/):
  complete API reference.
