---
linkTitle: "Motion service"
title: "Motion service configuration"
weight: 10
layout: "docs"
type: "docs"
description: "Configure the motion service for planning and executing component movements."
aliases:
  - /reference/services/motion/
  - /services/motion/
  - /mobility/motion/
---

The motion service plans and executes component motion: arm end-effector moves, base moves across a SLAM map, and base moves to a GPS coordinate. The builtin service ships with every machine running `viam-server`, so you do not need to add it to your configuration.

## Builtin service limitations

The builtin service implements only `Move` (plus `DoCommand` and `GetStatus`). The other motion RPCs return "not supported" errors; to use them, install a module that implements them or, for GPS navigation, use the navigation service.

- `MoveOnMap()`: requires a SLAM service (not recommended)
- `MoveOnGlobe()`: use the [navigation service](/navigation/) instead
- `GetPlan()`, `ListPlanStatuses()`, `StopPlan()`: only available with
  implementations that support `MoveOnMap` or `MoveOnGlobe`

## Access the motion service

Use the resource name `"builtin"` to get the default motion service client:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.motion import MotionClient

motion_service = MotionClient.from_robot(machine, "builtin")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import "go.viam.com/rdk/services/motion"

motionService, err := motion.FromProvider(machine, "builtin")
if err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

## Configuration attributes

The builtin motion service accepts the following optional configuration
attributes:

| Attribute                         | Type   | Default          | Description                                                                                                                                                                                                                                                                    |
| --------------------------------- | ------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `log_file_path`                   | string | (none)           | Path to write planning debug logs.                                                                                                                                                                                                                                             |
| `num_threads`                     | int    | (system default) | Number of threads for parallel planning.                                                                                                                                                                                                                                       |
| `plan_file_path`                  | string | (none)           | Path to write plan output files.                                                                                                                                                                                                                                               |
| `plan_directory_include_trace_id` | bool   | false            | Include trace ID in plan output directory names.                                                                                                                                                                                                                               |
| `log_planner_errors`              | bool   | false            | Log planning errors to the log file.                                                                                                                                                                                                                                           |
| `log_slow_plan_threshold_ms`      | int    | (none)           | Log plans that take longer than this threshold in milliseconds.                                                                                                                                                                                                                |
| `input_range_override`            | object | (none)           | Narrow a joint's allowed range below its kinematic limits. The value is a map from frame name to a map from joint index (string) to `{"min": <value>, "max": <value>}`. For example, `{"my-arm": {"3": {"min": 0, "max": 2}}}` restricts joint 3 of `my-arm` to the range 0-2. |

Example configuration:

```json
{
  "name": "builtin",
  "api": "rdk:service:motion",
  "model": "rdk:builtin:builtin",
  "attributes": {
    "log_planner_errors": true,
    "log_slow_plan_threshold_ms": 5000
  }
}
```

## Per-request configuration

Pass a `MotionConfiguration` on a `MoveOnGlobe` or `MoveOnMap` call to override per-request settings. See [MotionConfiguration](/motion-planning/reference/motion-configuration/) for the full field reference.

## Planning defaults

The builtin service compiles the defaults below into the binary. To change them at runtime, pass overrides through the `extra` map on a `Move` call (see the algorithms reference for the tunable list).

| Parameter                  | Value                      | Description                                                                                                                                                          |
| -------------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Planning timeout           | 300 seconds                | Maximum time to search for a path.                                                                                                                                   |
| Resolution                 | 2.0                        | Constraint-checking granularity (mm or degrees per step).                                                                                                            |
| Max IK solutions           | 100                        | Maximum inverse kinematics solutions to seed the search.                                                                                                             |
| Smoothing iterations       | 3 passes of sizes 10, 3, 1 | Post-planning path smoothing passes applied in sequence.                                                                                                             |
| Collision buffer           | 1e-8 mm (effectively zero) | Default buffer. Size obstacle geometries to include any safety margin, or pass `collision_buffer_mm` through the `extra` map on a Move call to override per request. |
| MoveOnMap plan deviation   | 1000 mm (1.0 m)            | Default for `MoveOnMap` calls.                                                                                                                                       |
| MoveOnGlobe plan deviation | 2600 mm (2.6 m)            | Default for `MoveOnGlobe` calls.                                                                                                                                     |

## DoCommand

The builtin motion service supports the following commands through `DoCommand`:

| Command               | Description                                                               |
| --------------------- | ------------------------------------------------------------------------- |
| `"plan"`              | Generate a motion plan without executing it.                              |
| `"execute"`           | Execute a previously generated plan.                                      |
| `"executeCheckStart"` | Execute a plan after verifying the arm is at the expected start position. |

## CLI commands

The Viam CLI provides `print-config`, `print-status`, `get-pose`, and `set-pose` for inspecting the motion service from the command line. See [Motion CLI commands](/motion-planning/reference/cli-commands/) for the full flag reference.

## What's next

- [Motion Service API](/motion-planning/reference/api/): full API reference.
- [How motion planning works](/motion-planning/how-planning-works/):
  how the planner searches for collision-free paths.
- [Configure Motion Constraints](/motion-planning/move-an-arm/constraints/): restrict arm
  movement during planning.
