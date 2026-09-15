---
linkTitle: "Move by joint positions"
title: "Move an arm by setting joint positions"
weight: 30
layout: "docs"
type: "docs"
description: "Command an arm directly in joint space using MoveToJointPositions, MoveThroughJointPositions, and streamed trajectories, bypassing the motion planner."
capabilities: ["motion-planning", "hw-arm"]
aliases:
  - /motion-planning/motion-how-to/move-arm-joint-positions/
---

Cartesian motion asks "what pose should the end effector reach?" and lets the
planner pick the joint angles that get there. Joint-space motion asks "what
configuration should the arm be in?" and skips the planner entirely. The two
are different tools. You reach for joint-space when:

- You already know the joint angles (from a previous capture, a
  teach-pendant run, or a saved configuration).
- You want to avoid the planner picking an unexpected IK solution that
  causes a wrist flip or elbow reconfiguration.
- You want predictable motion between two configurations you both
  control.
- You are building a control loop that computes its own joint targets.

**A caveat before you dive in.** Joint-space moves bypass the motion planner.
No obstacle avoidance, no constraint satisfaction, no path smoothing. If the
commanded configuration makes the arm swing through the table or your
workspace fixture, the arm will swing through the table. Joint-space is for
configurations you have already verified safe.

## Prerequisites

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

// Go's Input type is an alias for float64, storing radians for revolute joints.
targets := []referenceframe.Input{
    0,
    -math.Pi / 4, // -45 degrees
    math.Pi / 2,  // 90 degrees
    0,
    math.Pi / 4, // 45 degrees
    0,
}

if err := myArm.MoveToJointPositions(ctx, targets, nil); err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}

### Units: Python uses degrees, Go uses radians

This is the single most common source of joint-position bugs in Viam arm
code. The proto wire format and the Python SDK use degrees for revolute
joints and millimeters for prismatic joints. The Go SDK uses
`referenceframe.Input`, which stores radians for revolute joints. Conversion
happens at the wire boundary, so Python values of `90` and Go values of
`math.Pi / 2` both command the same angle.

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
    {0, -math.Pi / 4, math.Pi / 2, 0, math.Pi / 4, 0},
    {0, 0, math.Pi / 2, 0, 0, 0},
    {0, math.Pi / 4, 0, 0, -math.Pi / 4, 0},
}

// Go MoveOptions uses radians per second. The proto wire format uses
// degrees, but the SDK field names and values are in radians.
options := &arm.MoveOptions{
    MaxVelRads: 30.0 * math.Pi / 180, // Cap every joint at 30 deg/s.
    MaxAccRads: 60.0 * math.Pi / 180, // Cap every joint at 60 deg/s^2.
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

| Field                          | Type                  | Description                                                                                                      |
| ------------------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `max_vel_degs_per_sec`         | `double` (optional)   | Uniform velocity cap across every joint, in degrees per second.                                                  |
| `max_acc_degs_per_sec2`        | `double` (optional)   | Uniform acceleration cap across every joint, in degrees per second squared.                                      |
| `max_vel_degs_per_sec_joints`  | `[]double` (repeated) | Per-joint velocity caps. Length must match the arm's degrees of freedom. Overrides the uniform cap when set.     |
| `max_acc_degs_per_sec2_joints` | `[]double` (repeated) | Per-joint acceleration caps. Length must match the arm's degrees of freedom. Overrides the uniform cap when set. |
| `max_tcp_speed`                | `double` (optional)   | Caps the tool center point's speed, in meters per second. Unset means no cap.                                    |

All fields are optional ceilings. Any combination may be set. Each cap
you set applies along the whole trajectory; the arm module is responsible
for enforcing it.
Per-joint fields take precedence over global fields. Pass `nil`
options to use the module's default motion profile.

The field names above are the proto field names, also used by the Python
SDK. The Go SDK `arm.MoveOptions` struct uses shorter names and stores
values in **radians**: `MaxVelRads`, `MaxAccRads`, `MaxVelRadsJoints`,
`MaxAccRadsJoints`, `MaxTCPSpeedMPerSec`. The conversion happens at the
wire boundary.

## MoveThroughJointPositionsStreamed

`MoveThroughJointPositions` needs the whole trajectory before the arm starts
moving. That is fine for a handful of waypoints you already know. It stops
working when you are producing waypoints as you go: a teleoperation loop, a
trajectory arriving from another process, or a path still being optimized
while the arm executes the start of it.

The streamed form takes waypoints in batches over an open stream. The arm
starts moving on the first batch, so generating the trajectory and executing
it overlap.

### Waypoints carry time

The two APIs describe motion differently. `MoveThroughJointPositions` takes
positions and a `MoveOptions` ceiling, then leaves the arm to work out the
timing. A streamed `TrajectoryPoint` names the time at which the arm should
arrive, and optionally the velocities and accelerations it should have when it
gets there. You hand the arm a time-parameterized trajectory instead of asking
it to build one.

- `Time` is measured from the start of the motion. The first point must be
  zero, and every point after it must be strictly later than the one before.
- `Constraints` is optional and set per point. If you set it on the first
  point, the velocities there must be zero.
- Positions, velocities, and accelerations use radians and millimeters, the
  same `referenceframe.Input` convention as `MoveToJointPositions`. The wire
  format uses degrees.

### Stream a trajectory

You create both channels. Write batches to `batches` and close it to end the
motion. Read `responses` so a slow reader never stalls the client, and close
it after the call returns.

```go
import (
    "time"

    "go.viam.com/rdk/components/arm"
    "go.viam.com/rdk/referenceframe"
)

batches := make(chan []arm.TrajectoryPoint)
responses := make(chan arm.Response)

// The arm is free to acknowledge nothing at all, so this goroutine drains the
// channel rather than tracking progress.
go func() {
    for range responses {
    }
}()

go func() {
    defer close(batches)

    // Ten waypoints, 100ms apart, sent five at a time. nextWaypoint stands in
    // for whatever is producing your trajectory.
    batch := make([]arm.TrajectoryPoint, 0, 5)
    for i := 0; i < 10; i++ {
        batch = append(batch, arm.TrajectoryPoint{
            Time:      time.Duration(i*100) * time.Millisecond,
            Positions: nextWaypoint(i),
        })
        if len(batch) == 5 {
            batches <- batch
            batch = make([]arm.TrajectoryPoint, 0, 5)
        }
    }
}()

// Blocks until the arm finishes the trajectory, the stream fails, or another
// operation cancels it.
err := myArm.MoveThroughJointPositionsStreamed(ctx, batches, responses, nil)
close(responses)
if err != nil {
    logger.Fatal(err)
}
```

Batches append to the motion in the order you send them. A waypoint cannot be
replaced or withdrawn once it is on the wire, so a trajectory you might still
revise is one to send late rather than early.

Acknowledgments carry no payload, and an arm may send none, so they tell you
nothing about how far the motion has progressed. Read `GetJointPositions` if
you need to know where the arm actually is.

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

Pair `GetJointPositions` with `MoveToJointPositions` to capture a
configuration by hand (teach-by-demonstration) and replay it
programmatically.

## Joint-space moves compared to motion.Move

| Motion path                             | Use when                                                                                            |
| --------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `arm.MoveToJointPositions`              | You know the joint angles you want.                                                                 |
| `arm.MoveThroughJointPositions` (Go)    | You have a sequence of joint targets and want per-call velocity or acceleration caps.               |
| `arm.MoveThroughJointPositionsStreamed` | You are producing waypoints as you go, or the trajectory is too long to send in one request.        |
| `arm.MoveToPosition`                    | You have a Cartesian target pose but don't need obstacle avoidance.                                 |
| `motion.Move`                           | You have a Cartesian target and want obstacle avoidance, constraints, and IK picked by the planner. |

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

{{< expand "Streamed trajectory rejected for point times" >}}

A streamed trajectory is time-parameterized, so the arm rejects a batch whose
point times do not advance. The first point of the motion must be at time
zero, and every point after it must be strictly later than the one before,
across batch boundaries as well as within a batch. Check the time on the first
point of each batch against the last point of the batch before it.

{{< /expand >}}

{{< expand "Wrong number of values error" >}}

The `values` array must match the arm's degrees of freedom. A 6-DOF
arm expects six values, a 7-DOF arm expects seven. Check the arm
module's documentation or the kinematics file.

{{< /expand >}}

## What's next

- [Move an arm to a pose](/motion-planning/move-an-arm/move-to-pose/):
  Cartesian motion with obstacle avoidance through `motion.Move`.
- [Move with constraints](/motion-planning/move-an-arm/move-with-constraints/):
  Cartesian motion with linear or orientation constraints.
- [Arm kinematics](/motion-planning/reference/kinematics/): the
  kinematic file that declares joint limits.
- [Motion service API](/motion-planning/reference/api/): the alternative
  path through the motion service for Cartesian moves.
