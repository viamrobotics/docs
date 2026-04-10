---
linkTitle: "Motion Service"
title: "Motion Service Configuration"
weight: 10
layout: "docs"
type: "docs"
description: "Configure the motion service for planning and executing component movements."
aliases:
  - /reference/services/motion/
  - /services/motion/
  - /mobility/motion/
---

The motion service enables your machine to plan and move its components relative
to itself, other machines, and the world. The builtin motion service is enabled
by default on every machine running `viam-server`. You do not need to add it
to your configuration.

## Builtin service limitations

The builtin motion service supports the `Move()` method for arms and gantries.
The following methods return "not supported" errors from the builtin
implementation and require a module or the navigation service:

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

motionService, err := motion.FromRobot(machine, "builtin")
if err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

## Configuration attributes

The builtin motion service accepts the following optional configuration
attributes:

| Attribute                         | Type   | Default          | Description                                                                                     |
| --------------------------------- | ------ | ---------------- | ----------------------------------------------------------------------------------------------- |
| `log_file_path`                   | string | (none)           | Path to write planning debug logs.                                                              |
| `num_threads`                     | int    | (system default) | Number of threads for parallel planning.                                                        |
| `plan_file_path`                  | string | (none)           | Path to write plan output files.                                                                |
| `plan_directory_include_trace_id` | bool   | false            | Include trace ID in plan output directory names.                                                |
| `log_planner_errors`              | bool   | false            | Log planning errors to the log file.                                                            |
| `log_slow_plan_threshold_ms`      | int    | (none)           | Log plans that take longer than this threshold in milliseconds.                                 |
| `input_range_override`            | object | (none)           | Override joint input ranges. Map of component name to map of joint name to `{min, max}` limits. |

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

## MotionConfiguration (per-request)

When calling `MoveOnGlobe` or `MoveOnMap` (through a supporting implementation),
you can pass a `MotionConfiguration` to override per-request settings:

| Field                           | Type  | Default                | Description                                                   |
| ------------------------------- | ----- | ---------------------- | ------------------------------------------------------------- |
| `obstacle_detectors`            | list  | (none)                 | Vision service + camera pairs for dynamic obstacle detection. |
| `position_polling_frequency_hz` | float | (unset)                | How often to poll the machine's position, in Hz.              |
| `obstacle_polling_frequency_hz` | float | (unset)                | How often to poll vision services for obstacles, in Hz.       |
| `plan_deviation_m`              | float | 2.6 (globe), 1.0 (map) | Maximum allowed deviation from the plan, in meters.           |
| `linear_m_per_sec`              | float | 0.3                    | Linear velocity, in meters per second.                        |
| `angular_degs_per_sec`          | float | 60.0                   | Angular velocity, in degrees per second.                      |

## Planning defaults

The builtin motion service uses the following compiled defaults:

| Parameter                  | Value           | Description                                               |
| -------------------------- | --------------- | --------------------------------------------------------- |
| Planning timeout           | 300 seconds     | Maximum time to search for a path.                        |
| Resolution                 | 2.0             | Constraint-checking granularity (mm or degrees per step). |
| Max IK solutions           | 100             | Maximum inverse kinematics solutions to seed the search.  |
| Smoothing iterations       | 30              | Post-planning path smoothing passes.                      |
| Collision buffer           | 150 mm          | Clearance added around obstacles during planning.         |
| MoveOnMap plan deviation   | 1000 mm (1.0 m) | Default for `MoveOnMap` calls.                            |
| MoveOnGlobe plan deviation | 2600 mm (2.6 m) | Default for `MoveOnGlobe` calls.                          |

## DoCommand

The builtin motion service supports the following commands through `DoCommand`:

| Command               | Description                                                               |
| --------------------- | ------------------------------------------------------------------------- |
| `"plan"`              | Generate a motion plan without executing it.                              |
| `"execute"`           | Execute a previously generated plan.                                      |
| `"executeCheckStart"` | Execute a plan after verifying the arm is at the expected start position. |

## CLI commands

The Viam CLI provides commands for inspecting and testing the motion service
from the command line. These are useful for debugging frame configurations and
testing motion without writing code.

All commands require the `--part` flag to identify the machine part.

### print-config

Prints the frame system configuration for the specified machine part.

```sh
viam machines part motion print-config --part "my-machine-main"
```

### print-status

Prints the current pose of every component relative to the world frame.

```sh
viam machines part motion print-status --part "my-machine-main"
```

Output shows X, Y, Z position (mm) and orientation (OX, OY, OZ, Theta in
degrees) for each frame.

### get-pose

Gets the current pose of a specific component in the world frame.

```sh
viam machines part motion get-pose --part "my-machine-main" --component "my-arm"
```

### set-pose

Moves a component to a specified pose using the motion service. Only the
position and orientation values you provide are changed; the rest are kept from
the component's current pose.

```sh
viam machines part motion set-pose --part "my-machine-main" --component "my-arm" \
  --x 300 --y 200 --z 400
```

Available flags: `--x`, `--y`, `--z` (position in mm), `--ox`, `--oy`, `--oz`,
`--theta` (orientation vector in degrees).

## What's next

- [Motion Service API](/motion-planning/reference/api/): full API reference.
- [Motion Planning Algorithms](/motion-planning/reference/algorithms/): how the planner
  works.
- [Configure Motion Constraints](/motion-planning/constraints/): restrict arm
  movement during planning.
