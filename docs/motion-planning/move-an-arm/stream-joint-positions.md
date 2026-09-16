---
linkTitle: "Stream joint positions"
title: "Stream joint positions to an arm"
weight: 35
layout: "docs"
type: "docs"
description: "Push joint trajectory points to an arm while it is already moving, using MoveThroughJointPositionsStreamed."
capabilities: ["motion-planning", "hw-arm"]
---

`MoveThroughJointPositionsStreamed` opens a stream onto which you push joint
trajectory points while the arm is already moving: the arm executes the points
it has while you keep appending. The
[other joint-space methods](/motion-planning/move-an-arm/move-by-joint-positions/)
take the whole motion up front, the configurations to hit and optional
ceilings on how fast to get there. The arm module picks the motion profile from
there.

Streaming hands the arm a time-parameterized trajectory: be at this
configuration at this time, moving at this velocity. You produce that schedule.

Reach for streaming when the trajectory is produced as the motion runs: a
teleoperation feed, a visual-servoing loop, a force-feedback correction on a
surface-finishing path, or a trajectory long enough that you want to keep only
part of it in memory.

{{< alert title="Joint-space moves bypass the motion planner" color="caution" >}}
You are responsible for obstacle avoidance, constraint satisfaction, and path
smoothing. A trajectory point that puts the arm through the table or your
workspace fixture executes as sent. Everything you stream must already be safe.
{{< /alert >}}

`MoveThroughJointPositionsStreamed` is safety-heartbeat monitored: if the
session that last called it stops sending heartbeats, `viam-server` stops the
arm. A client that dies mid-trajectory leaves the arm stopped.

## Prerequisites

- A configured arm component and an SDK client.
- An arm module that implements streaming. Streaming is currently supported for the [`viam:ufactory`](https://app.viam.com/module/viam/ufactory) and [`viam:universal-robots`](https://app.viam.com/module/viam/universal-robots) modules.
- A source of trajectory points that stays within the arm's joint limits.

## What a trajectory point contains

A trajectory point carries the following:

- **Time**, measured from the start of the motion. The first point must be
  zero, and every point after it must be strictly later than the one before.
- **Positions**, one value per joint, matching the arm's degrees of freedom.
- **Constraints**, optional and set per point. A point either carries no constraints at all or carries a velocity for every joint, with accelerations an optional addition on top. The arm starts from rest, so the first point is the arm standing still: either leave constraints off that point, or give every joint a velocity of zero. Only velocities have to be zero there; an acceleration on the first point is allowed.

Each SDK uses different units for positions and constraints. For reference, see [Units](/motion-planning/move-an-arm/move-by-joint-positions/#units-python-uses-degrees-go-uses-radians).

## How batching works

A batch is a request of one or more trajectory points. Point times are offsets
from the start of the motion, so the same trajectory sent whole and sent in
three batches produces the same motion. Batching controls delivery; the point
times control the arm.

Batch size controls how far ahead of the arm you commit. A point you
have sent is final: points cannot be replaced or revoked. Large batches cost
fewer round trips and leave more of the trajectory queued if your producer
falls behind, at the price of a longer committed stretch. Small batches keep
the last committed point close to where the arm is now, so a fresh sensor
reading can still change the next move.

## Stream a trajectory

Each SDK exposes the same stream through a different control flow. Python takes
an async iterator and gives you one back. Go hands you two channels that you
own.

{{< alert title="SDK availability" color="caution" >}}
`MoveThroughJointPositionsStreamed` is available in the **Python, Go, and C++
SDKs**. The TypeScript SDK does not expose it yet.
{{< /alert >}}

{{< tabs >}}
{{% tab name="Python" %}}

`move_through_joint_positions_streamed` takes an async iterator of batches and
returns an async iterator of `Arm.TrajectoryUpdate` values. Iterate the result
to read updates as the arm works through the trajectory. Each list you yield
becomes one `TrajectoryBatch` request.

```python
from datetime import timedelta

from viam.components.arm import Arm

my_arm = Arm.from_robot(machine, "my-arm")

# Times are offsets from the start of the motion; positions are degrees.
first_batch = [
    Arm.TrajectoryPoint(
        time=timedelta(0),
        positions=[0, -45, 90, 0, 45, 0],
        # Velocities on the t=0 point must be zero.
        constraints=Arm.KinematicConstraints(velocities=[0, 0, 0, 0, 0, 0]),
    ),
    Arm.TrajectoryPoint(
        time=timedelta(milliseconds=500),
        positions=[0, -22.5, 90, 0, 22.5, 0],
    ),
    Arm.TrajectoryPoint(
        time=timedelta(seconds=1),
        positions=[0, 0, 90, 0, 0, 0],
    ),
]


async def batches():
    # Yield a list per batch. Returning ends the trajectory.
    yield first_batch


async for update in my_arm.move_through_joint_positions_streamed(batches()):
    # Updates arrive as the arm executes. Stopping this loop early closes
    # the stream.
    pass
```

{{% /tab %}}
{{% tab name="Go" %}}

You create both channels. Write batches to `batches` and close it to end the
motion. Drain `responses` for the life of the call, because the client blocks
while it waits to hand one over, and close it after the call returns.

```go
import (
    "math"
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

    // Give up if the call returns early, so this goroutine never blocks on a
    // channel nobody is reading.
    send := func(b []arm.TrajectoryPoint) bool {
        select {
        case batches <- b:
            return true
        case <-ctx.Done():
            return false
        }
    }

    // Ten waypoints, 100ms apart, sent five at a time.
    batch := make([]arm.TrajectoryPoint, 0, 5)
    for i := 0; i < 10; i++ {
        batch = append(batch, arm.TrajectoryPoint{
            Time: time.Duration(i*100) * time.Millisecond,
            // Revolute joint values are radians, matching referenceframe.Input.
            Positions: []referenceframe.Input{
                0, -math.Pi/4 + float64(i)*math.Pi/40, math.Pi / 2, 0, math.Pi / 4, 0,
            },
        })
        if len(batch) == 5 {
            if !send(batch) {
                return
            }
            batch = make([]arm.TrajectoryPoint, 0, 5)
        }
    }
    if len(batch) > 0 {
        send(batch)
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

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Streamed trajectory behaves oddly across a batch boundary" >}}

Times are offsets from the start of the whole motion, not from the start of the
batch they arrive in. The first point of the stream must be at time zero and
every later point must be strictly greater than the one before it, across batch
boundaries as well as within a batch. Restarting the clock at each batch sends
the arm a trajectory that goes backwards in time.

`viam-server` leaves enforcement to the arm module, so what a violation looks
like depends on the module: an error, a refused batch, or unintended motion.

{{< /expand >}}

{{< expand "Streamed trajectory fails with a joint range error" >}}

The error names the joint index and the range it violated, not which trajectory
point carried it: `joint 1 needs to be within range [-360, 360] and cannot be
moved to 400`. Check the whole trajectory against the joint limits before you
start streaming to find the point at fault.

The Go client raises this one as it encodes each point, the same check the
unary path makes, advancing through the trajectory point by point. Earlier
batches are already in flight by the time a bad point appears, so a rejected
point tears the whole stream down instead of returning an error for that
point alone. If the arm's kinematics are unregistered, the client logs a warning
and skips the check.

{{< /expand >}}

{{< expand "Wrong number of values error" >}}

The `positions` array must match the arm's degrees of freedom. A 6-DOF
arm expects six values, a 7-DOF arm expects seven. Check the arm
module's documentation or the kinematics file.

{{< /expand >}}

## What's next

- [Move by joint positions](/motion-planning/move-an-arm/move-by-joint-positions/):
  the unary methods, for trajectories you have in hand before the arm moves.
- [Move an arm to a pose](/motion-planning/move-an-arm/move-to-pose/):
  Cartesian motion with obstacle avoidance through `motion.Move`.
- [Arm kinematics](/motion-planning/reference/kinematics/): the
  kinematic file that declares joint limits.
