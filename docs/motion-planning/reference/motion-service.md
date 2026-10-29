---
linkTitle: "Motion service"
title: "Motion service configuration"
weight: 10
layout: "docs"
type: "docs"
description: "Configure the motion service for planning and executing component movements."
capabilities: ["motion-planning"]
diataxis: reference
aliases:
  - /reference/services/motion/
  - /services/motion/
  - /mobility/motion/
---

The motion service plans and executes component motion: arm end-effector moves, base moves across a SLAM map, and base moves to a GPS coordinate. The builtin service ships with every machine running `viam-server`, so you do not need to add it to your configuration.

Most users never configure the motion service. Read this page if you need to save plans for debugging or replay, or narrow a joint's range below its kinematic limits.

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

Every machine includes a default motion service named `builtin`, which has no configuration. To set the attributes below, add a motion service with the model `rdk:builtin:builtin` to your machine's configuration. In the Viam app, its configuration panel sets the plan-file and log attributes under **Plan files** and **Logs**. If you name the service `builtin`, it replaces the default service. With any other name, both services run, and your settings apply only to requests sent to the service you added.

All attributes are optional:

| Attribute                         | Type             | Default                           | Description                                                                                                                                                                                                                                                                                                                                                                                                                      |
| --------------------------------- | ---------------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `log_file_path`                   | string           | (none)                            | Path to write planning debug logs.                                                                                                                                                                                                                                                                                                                                                                                               |
| `plan_file_path`                  | string           | (none)                            | Directory to write plan files to. Required by `log_planner_errors` and `log_slow_plan_threshold_ms`; on its own, it writes nothing.                                                                                                                                                                                                                                                                                              |
| `plan_directory_include_trace_id` | bool             | false                             | Include trace ID in plan output directory names.                                                                                                                                                                                                                                                                                                                                                                                 |
| `log_planner_errors`              | bool             | false                             | Write a plan file for every request that fails to plan. A failed plan's file holds the request only, with no trajectory.                                                                                                                                                                                                                                                                                                         |
| `log_slow_plan_threshold_ms`      | int              | (none)                            | Write a plan file for every plan that takes longer than this many milliseconds. Set it to `-1` to write a file for every plan. The **Save motion plans** toggle in the Viam app does this.                                                                                                                                                                                                                                       |
| `input_range_override`            | object           | (none)                            | Narrow a joint's allowed range below its kinematic limits. The value is a map from frame name to a map from joint index (string) to `{"min": <value>, "max": <value>}`. For example, `{"my-arm": {"3": {"min": 0, "max": 2}}}` restricts joint 3 of `my-arm` to the range 0-2.                                                                                                                                                   |
| `cable_constraint`                | bool             | (unset)                           | Keep each rotational joint of an arm within `max_cable_twist_degs` of its reference position, so cables routed along the arm don't wind up. `true` constrains every arm (every kinematic model in the frame system), or only the arms in `cable_constraint_frames`. `false` turns the constraint off. When unset, the service constrains every arm that carries a camera; see [Cable twist constraint](#cable-twist-constraint). |
| `cable_constraint_frames`         | array of strings | (none)                            | Names of the arms to constrain; each must be a kinematic model in the frame system, or planning fails. Takes effect when `cable_constraint` is `true`, or when it is unset and some arm carries a camera. See [Cable twist constraint](#cable-twist-constraint).                                                                                                                                                                 |
| `max_cable_twist_degs`            | float            | 180                               | How far, in degrees, each rotational joint of a constrained arm may turn from its reference position. In the service configuration, negative values are rejected and `0` selects the default; in `extra`, the value must be positive. See [Cable twist constraint](#cable-twist-constraint).                                                                                                                                     |
| `cable_twist_reference_degs`      | object           | (midpoint of each joint's limits) | Map from arm name to the joint positions, in degrees, at which that arm's cables are untwisted. Give one value per joint. For example, `{"my-arm": [0, 0, 0, 0, 0, 0]}`. See [Cable twist constraint](#cable-twist-constraint).                                                                                                                                                                                                  |

Example configuration:

```json
{
  "name": "builtin",
  "api": "rdk:service:motion",
  "model": "rdk:builtin:builtin",
  "attributes": {
    "plan_file_path": "${environment.HOME}/.viam/plans",
    "log_planner_errors": true,
    "log_slow_plan_threshold_ms": 5000
  }
}
```

To replay saved plans in the **3D SCENE** tab, sync the plan directory to the cloud; see [Replay a saved plan in the 3D scene](/motion-planning/visualize-a-motion-plan/#replay-a-saved-plan-in-the-3d-scene).

### Cable twist constraint

`viam-server` v1.14.0 and later apply this constraint.
Cables for a camera or tool mounted on an arm usually run along the arm, so turning a joint too far winds them up.
The cable twist constraint keeps every rotational joint of a constrained arm within `max_cable_twist_degs` (180 by default) of its reference position.
The reference is the midpoint of the joint's limits unless `cable_twist_reference_degs` sets one.
A joint that starts a move outside that range can stay there or turn back toward the reference, but the planner never turns it further away.

If you don't set `cable_constraint`, the service turns the constraint on for `Move` requests on every arm that has a camera mounted on it, or on anything attached to it, in the frame system.
An arm with an `input_range_override` is left out.
On a constrained arm, the planner uses only joint positions within the allowed range.
It can reach the same poses as before, but it can choose a different joint solution, and planning fails if no path keeps every joint in range.

To turn the constraint off for every arm, set `"cable_constraint": false`.
To change it for one request, pass any of these four attributes in the `extra` map of a `Move` call; each one you pass overrides the service configuration.
The service configuration and the camera default apply to `Move` requests only; other planning, such as teleoperation, applies the constraint only when its own `extra` sets `cable_constraint`.

```json
{
  "name": "builtin",
  "api": "rdk:service:motion",
  "model": "rdk:builtin:builtin",
  "attributes": {
    "cable_constraint": true,
    "cable_constraint_frames": ["my-arm"],
    "max_cable_twist_degs": 150
  }
}
```

## Planning defaults

The builtin service compiles the defaults below into the binary. To change them at runtime, pass overrides through the `extra` map on a `Move` call (see the algorithms reference for the tunable list).

| Parameter            | Value                      | Description                                                                                                                                                          |
| -------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Planning timeout     | 300 seconds                | Maximum time to search for a path.                                                                                                                                   |
| Resolution           | 2.0                        | Constraint-checking granularity (mm or degrees per step).                                                                                                            |
| Max IK solutions     | 100                        | Maximum inverse kinematics solutions to test for a direct path and seed the fallback search.                                                                         |
| Smoothing iterations | 3 passes of sizes 10, 3, 1 | Path smoothing passes applied in sequence to cBiRRT fallback paths.                                                                                                  |
| Collision buffer     | 1e-8 mm (effectively zero) | Default buffer. Size obstacle geometries to include any safety margin, or pass `collision_buffer_mm` through the `extra` map on a Move call to override per request. |

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

- [Motion service API](/motion-planning/reference/api/): full API reference.
- [How motion planning works](/motion-planning/how-planning-works/):
  how the planner searches for collision-free paths.
- [Configure motion constraints](/motion-planning/move-an-arm/constraints/): restrict arm
  movement during planning.
