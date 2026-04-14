---
linkTitle: "Move by joint positions"
title: "Move an arm by setting joint positions"
weight: 15
layout: "docs"
type: "docs"
description: "Command an arm directly in joint space using MoveToJointPositions and MoveThroughJointPositions, bypassing the motion planner."
---

When you move an arm with `motion.Move` or `arm.MoveToPosition`, the
planner solves inverse kinematics to find joint angles that reach the
target Cartesian pose. Most of the time that is what you want. But
sometimes you need to command the arm in joint space directly:

- You already know the joint angles (from a previous capture, a
  teach-pendant run, or a saved configuration).
- You want to avoid the planner picking an unexpected IK solution that
  causes a wrist flip or elbow reconfiguration.
- You want predictable motion between two configurations you both
  control.
- You are building a control loop that computes its own joint targets.

Joint-space moves bypass the motion planner entirely. The arm goes
straight to the commanded angles. There is no obstacle avoidance, no
constraint satisfaction, and no path smoothing.

## Before you start

- A configured arm component and an SDK client.
- You know the joint angles you want. For a 6-DOF arm, this is six
  values; for a 7-DOF arm, seven; and so on.
- You have verified the target is within joint limits. The arm's
  kinematics file declares per-joint min and max; values outside the
  limits produce an error.

## MoveToJointPositions

Drives every joint to a single target configuration in one call. Blocks
until done or cancelled.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.arm import Arm
from viam.proto.component.arm import JointPositions

my_arm = Arm.from_robot(machine, "my-arm")

# Joint angles in degrees. Revolute joint values are degrees;
# prismatic joint values are millimeters.
positions = JointPositions(values=[0, -45, 90, 0, 45, 0])
await my_arm.move_to_joint_positions(positions)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "math"

    "go.viam.com/rdk/components/arm"
    "go.viam.com/rdk/referenceframe"
)

myArm, err := arm.FromProvider(machine, "my-arm")
if err != nil {
    logger.Fatal(err)
}

// Go's Input type is radians. Convert from degrees using referenceframe.FloatsToInputs
// on a radians slice.
targets := referenceframe.FloatsToInputs([]float64{
    0,
    -math.Pi / 4, // -45 degrees
    math.Pi / 2,  // 90 degrees
    0,
    math.Pi / 4,  // 45 degrees
    0,
})

if err := myArm.MoveToJointPositions(ctx, targets, nil); err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

### Units

This is an easy-to-miss detail: the units differ between Python and Go.

- **Proto and Python SDK** use degrees for revolute joints and
  millimeters for prismatic joints. The `JointPositions.values` field
  and the Python `move_to_joint_positions` argument are in these
  units.
- **Go SDK** uses `referenceframe.Input`, which stores radians for
  revolute joints. The conversion happens at the wire boundary.

If you port code between languages, convert values accordingly.

## MoveThroughJointPositions

Drives the arm through a sequence of joint configurations in order,
with optional per-motion velocity and acceleration limits through
`MoveOptions`.

{{< alert title="SDK availability" color="caution" >}}
`MoveThroughJointPositions` is available in the **Go SDK** and through
the proto, but is **not currently exposed by the Python SDK**. Python
callers who need the same behavior must call each waypoint with
`move_to_joint_positions` in sequence.
{{< /alert >}}

{{< tabs >}}
{{% tab name="Go" %}}

```go
import (
    "math"

    "go.viam.com/rdk/components/arm"
    "go.viam.com/rdk/referenceframe"
)

waypoints := [][]referenceframe.Input{
    referenceframe.FloatsToInputs([]float64{0, -math.Pi / 4, math.Pi / 2, 0, math.Pi / 4, 0}),
    referenceframe.FloatsToInputs([]float64{0, 0, math.Pi / 2, 0, 0, 0}),
    referenceframe.FloatsToInputs([]float64{0, math.Pi / 4, 0, 0, -math.Pi / 4, 0}),
}

options := &arm.MoveOptions{
    MaxVelDegsPerSec:   30.0, // Cap every joint at 30 deg/s.
    MaxAccDegsPerSec2:  60.0, // Cap every joint at 60 deg/s^2.
}

if err := myArm.MoveThroughJointPositions(ctx, waypoints, options, nil); err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{% tab name="Python" %}}

The Python SDK does not expose `MoveThroughJointPositions`. Use a loop
with `move_to_joint_positions` for the equivalent behavior:

```python
from viam.components.arm import Arm
from viam.proto.component.arm import JointPositions

my_arm = Arm.from_robot(machine, "my-arm")

waypoints = [
    JointPositions(values=[0, -45, 90, 0, 45, 0]),
    JointPositions(values=[0, 0, 90, 0, 0, 0]),
    JointPositions(values=[0, 45, 0, 0, -45, 0]),
]

for wp in waypoints:
    await my_arm.move_to_joint_positions(wp)
```

Without `MoveOptions` you cannot cap velocity or acceleration per call
from Python; the arm uses its module's default speed profile.

{{% /tab %}}
{{< /tabs >}}

### MoveOptions fields

| Field                          | Type                  | Description                                                                                                        |
| ------------------------------ | --------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `max_vel_degs_per_sec`         | `double` (optional)   | Cap every joint at the given velocity, in degrees per second. Ignored when the per-joint field is set.             |
| `max_acc_degs_per_sec2`        | `double` (optional)   | Cap every joint at the given acceleration, in degrees per second squared. Ignored when the per-joint field is set. |
| `max_vel_degs_per_sec_joints`  | `[]double` (repeated) | Per-joint velocity caps. Length must match the arm's degrees of freedom.                                           |
| `max_acc_degs_per_sec2_joints` | `[]double` (repeated) | Per-joint acceleration caps. Length must match the arm's degrees of freedom.                                       |

Per-joint fields take precedence over global fields. Pass `nil`
options to use the module's default motion profile.

## Reading current joint positions

Use `GetJointPositions` to capture the arm's current configuration
before commanding a new one:

{{< tabs >}}
{{% tab name="Python" %}}

```python
current = await my_arm.get_joint_positions()
print([v for v in current.values])
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
current, err := myArm.JointPositions(ctx, nil)
if err != nil {
    logger.Fatal(err)
}
logger.Infof("joint positions (radians): %v", current)
```

{{% /tab %}}
{{< /tabs >}}

Pair `GetJointPositions` with `MoveToJointPositions` to capture a pose
by hand (teach-by-demonstration) and replay it programmatically.

## Joint-space moves compared to motion.Move

| Motion path                          | Use when                                                                                            |
| ------------------------------------ | --------------------------------------------------------------------------------------------------- |
| `arm.MoveToJointPositions`           | You know the joint angles you want.                                                                 |
| `arm.MoveThroughJointPositions` (Go) | You have a sequence of joint targets and want per-call velocity or acceleration caps.               |
| `arm.MoveToPosition`                 | You have a Cartesian target pose but don't need obstacle avoidance.                                 |
| `motion.Move`                        | You have a Cartesian target and want obstacle avoidance, constraints, and IK picked by the planner. |

Joint-space moves are the right call when you need to control the
posture of the arm precisely. They do not protect against collisions
with obstacles, the environment, or the arm's own body beyond what the
arm module itself enforces.

## Troubleshooting

{{< expand "Error: values out of joint range" >}}

The arm's kinematics file declares per-joint min and max. Commanding a
value outside the limits produces an error. Read the joint limits from
the kinematics file or call
[`GetKinematics`](/motion-planning/reference/api/) to inspect them.
Reduce the out-of-range value, or if the physical arm supports a wider
range, update the kinematics file (see
[Arm kinematics](/motion-planning/reference/kinematics/)).

{{< /expand >}}

{{< expand "Arm moves faster or slower than expected" >}}

Without `MoveOptions`, the speed profile comes from the arm module's
default. Different modules pick different defaults. If you need a
specific speed, use Go's `MoveOptions`, or break a long motion into
shorter `MoveToJointPositions` calls with sleeps between.

{{< /expand >}}

{{< expand "Wrong number of values error" >}}

The `values` array must match the arm's degrees of freedom. A 6-DOF
arm expects six values, a 7-DOF arm expects seven. Check the arm
module's documentation or the kinematics file.

{{< /expand >}}

## What's next

- [Move an arm to a pose](/motion-planning/motion-how-to/move-arm-to-pose/):
  Cartesian motion with obstacle avoidance through `motion.Move`.
- [Move with constraints](/motion-planning/motion-how-to/move-arm-with-constraints/):
  Cartesian motion with linear or orientation constraints.
- [Arm kinematics](/motion-planning/reference/kinematics/): the
  kinematic file that declares joint limits.
- [Motion service API](/motion-planning/reference/api/): the alternative
  path through the motion service for Cartesian moves.
