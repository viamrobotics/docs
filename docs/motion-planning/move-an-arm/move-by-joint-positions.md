---
linkTitle: "Move by joint positions"
title: "Move an arm by setting joint positions"
weight: 30
layout: "docs"
type: "docs"
description: "Command an arm directly in joint space using MoveToJointPositions, MoveThroughJointPositions, and MoveThroughJointPositionsStreamed, bypassing the motion planner."
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
moving. `MoveThroughJointPositionsStreamed` does not: you open a stream, push
batches of waypoints onto it, and the arm executes the points it already has
while you keep appending. Reach for it when the trajectory is produced as the
motion runs: a teleoperation feed, a visual-servoing loop, or a trajectory long
enough that you do not want to hold all of it in memory.

Each waypoint is a `TrajectoryPoint`: a time offset from the start of the
motion, a joint configuration to be at by then, and optional velocity and
acceleration targets. The time of the first point must be zero, and times must
strictly increase across the whole stream, not just within a batch. If a point
carries constraints, the velocities on the t=0 point must all be zero.

Batching is purely your pacing choice. Points execute in the order you send
them regardless of how you group them, so a batch is just how much you hand
over at once.

{{< alert title="SDK availability" color="caution" >}}
`MoveThroughJointPositionsStreamed` is available in the **Go SDK** and the
**C++ SDK**. The Python and TypeScript SDKs do not expose it yet.
{{< /alert >}}

{{< tabs >}}
{{% tab name="Go" %}}

The call blocks until the trajectory finishes or fails. You own both channels:
send batches on `batches` and close it when the trajectory is complete, read
acknowledgments off `responses` for the life of the call, and close `responses`
only after the call returns.

```go
import (
    "math"
    "time"

    "go.viam.com/rdk/components/arm"
    "go.viam.com/rdk/referenceframe"
)

// One batch of three waypoints. Times are offsets from the start of the
// motion; positions are radians, matching referenceframe.Input.
firstBatch := []arm.TrajectoryPoint{
    {
        Time:      0,
        Positions: []referenceframe.Input{0, -math.Pi / 4, math.Pi / 2, 0, math.Pi / 4, 0},
        // Velocities on the t=0 point must be zero.
        Constraints: &arm.KinematicConstraints{
            Velocities: []float64{0, 0, 0, 0, 0, 0},
        },
    },
    {
        Time:      500 * time.Millisecond,
        Positions: []referenceframe.Input{0, -math.Pi / 8, math.Pi / 2, 0, math.Pi / 8, 0},
    },
    {
        Time:      time.Second,
        Positions: []referenceframe.Input{0, 0, math.Pi / 2, 0, 0, 0},
    },
}

batches := make(chan []arm.TrajectoryPoint)
responses := make(chan arm.Response)

// Drain acknowledgments. The arm is not obliged to acknowledge every batch,
// but a caller that stops reading stalls the stream.
go func() {
    for range responses {
    }
}()

// Feed the trajectory, then close to signal that no more points are coming.
go func() {
    defer close(batches)
    for _, batch := range [][]arm.TrajectoryPoint{firstBatch /*, more batches */} {
        select {
        case batches <- batch:
        case <-ctx.Done():
            return
        }
    }
}()

err := myArm.MoveThroughJointPositionsStreamed(ctx, batches, responses, nil)
close(responses)
if err != nil {
    logger.Fatal(err)
}
```

{{% /tab %}}
{{% tab name="C++" %}}

The C++ SDK inverts the control flow: instead of you pushing onto a channel,
the SDK pulls from a `batch_source` callback until it returns `boost::none`,
and reports progress through an `update_handler` callback. Returning `false`
from `update_handler` stops the trajectory early.

```cpp
#include <viam/sdk/components/arm.hpp>

using viam::sdk::Arm;

std::vector<std::vector<Arm::trajectory_point>> trajectory = {
    {
        // Positions and velocities are in degrees, unlike the Go SDK.
        // Velocities on the t=0 point must be zero.
        Arm::trajectory_point{std::chrono::microseconds(0),
                              {0, -45, 90, 0, 45, 0},
                              Arm::trajectory_point::kinematic_constraints{{0, 0, 0, 0, 0, 0},
                                                                          boost::none}},
        Arm::trajectory_point{std::chrono::milliseconds(500), {0, -22.5, 90, 0, 22.5, 0}, boost::none},
        Arm::trajectory_point{std::chrono::seconds(1), {0, 0, 90, 0, 0, 0}, boost::none},
    },
};

std::size_t next = 0;
auto batch_source = [&]() -> boost::optional<std::vector<Arm::trajectory_point>> {
    if (next == trajectory.size()) {
        return boost::none;  // No more points are coming.
    }
    return trajectory[next++];
};

// Return false here to halt the trajectory early.
auto update_handler = [](Arm::trajectory_update) { return true; };

const auto outcome = my_arm->move_through_joint_positions_streamed(batch_source, update_handler);
if (outcome == Arm::stream_outcome::k_halted_by_update_handler) {
    // The trajectory was stopped before its natural end.
}
```

The two callbacks may be invoked from different threads and may run
concurrently with each other, so synchronize any state you share between them.
A fault is reported by throwing, and an exception thrown out of either callback
propagates to the caller rather than being swallowed.

{{% /tab %}}
{{< /tabs >}}

### Units, again

The unit split from `MoveToJointPositions` carries over, and the C++ SDK adds a
third position:

| Interface                   | Positions                        | Velocities                         |
| --------------------------- | -------------------------------- | ---------------------------------- |
| Proto wire format           | degrees, millimeters             | degrees/second, millimeters/second |
| Go `arm.TrajectoryPoint`    | radians (`referenceframe.Input`) | radians/second                     |
| C++ `Arm::trajectory_point` | degrees                          | degrees/second                     |

Accelerations follow their velocity unit, squared.

### What the SDK checks before the wire

The Go client validates each waypoint against the arm's joint limits as it
encodes it, the same check the unary path makes, advancing through the
trajectory point by point. Because batches are already in flight by the time a
bad waypoint appears, a rejected waypoint tears the whole stream down rather
than returning an error for that point alone. If the arm's kinematics are not
registered, the client logs a warning and skips the check.

`MoveThroughJointPositionsStreamed` is safety-heartbeat monitored: if the
session that last called it stops sending heartbeats, the arm is stopped. A
client that dies mid-trajectory does not leave the arm executing the rest of
what it was sent.

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

| Motion path                                       | Use when                                                                                            |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `arm.MoveToJointPositions`                        | You know the joint angles you want.                                                                 |
| `arm.MoveThroughJointPositions` (Go)              | You have a sequence of joint targets and want per-call velocity or acceleration caps.               |
| `arm.MoveThroughJointPositionsStreamed` (Go, C++) | You are producing the trajectory as the arm moves and cannot supply it all up front.                |
| `arm.MoveToPosition`                              | You have a Cartesian target pose but don't need obstacle avoidance.                                 |
| `motion.Move`                                     | You have a Cartesian target and want obstacle avoidance, constraints, and IK picked by the planner. |

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

{{< expand "Streamed trajectory behaves oddly across a batch boundary" >}}

Times are offsets from the start of the whole motion, not from the start of the
batch they arrive in. The first point of the stream must be at time zero and
every later point must be strictly greater than the one before it, across batch
boundaries as well as within a batch. Restarting the clock at each batch sends
the arm a trajectory that goes backwards in time.

`viam-server` does not check this for you. Enforcement is left to the arm
module, so what a violation looks like depends on the module: an error, a
refused batch, or motion you did not intend.

{{< /expand >}}

{{< expand "Streamed trajectory fails with a joint range error" >}}

The Go client checks each waypoint against the arm's joint limits as it encodes
it, and refuses one that is out of range. Earlier batches are already in flight
by then, so a rejected waypoint tears the whole stream down instead of failing
just that point.

The error names the joint index and the range it violated, not which waypoint
carried it: `joint 1 needs to be within range [-360, 360] and cannot be moved
to 400`. Check the whole trajectory against the joint limits before you start
streaming if you need to know which point is at fault.

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
