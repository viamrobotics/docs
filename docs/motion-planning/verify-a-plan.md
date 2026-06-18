---
linkTitle: "Verify a plan"
title: "Verify a motion plan without executing it"
weight: 60
layout: "docs"
type: "docs"
description: "Use armplanning.PlanMotion to compute and inspect a trajectory before the arm moves, and learn how to get the same plan over the motion service API."
---

Before an arm moves, you often want to know whether the motion is even possible:
whether a goal is reachable, whether a path exists around the obstacles you have
declared, or what trajectory the planner would produce. Executing a `Move` to
find out is slow and, on real hardware, risky. Planning without executing
answers those questions first, then leaves it to you whether to run the result.

`armplanning.PlanMotion` runs the same planner the motion service uses, but
returns the `Plan` instead of moving the arm. This page shows how to compute and
inspect a plan in process, and closes with how to get the same plan over the
motion service API from a remote client.

## When to plan without executing

- **Preview a motion.** Inspect the trajectory the planner produces before
  committing the arm to it.
- **Check feasibility.** Confirm a goal is reachable and a collision-free path
  exists, without driving the arm into a failed attempt.
- **Validate from a hypothetical state.** Plan from a start configuration the
  arm is not currently in, to test reachability before you move there.

## PlanMotion compared to Move

`Move` and `PlanMotion` share the planner, but differ in what they do with the
result and where they run:

- `Move` is a motion service API call. It plans, then executes, moving the arm.
- `PlanMotion` is an in-process Go function. It plans and returns the trajectory.
  Nothing moves until you execute the result yourself.

Because `PlanMotion` runs in process, you assemble the planning inputs directly
rather than letting the service collect them from the robot. That is more setup,
but it gives you the plan as data with no side effects.

## Assemble a PlanRequest

A `PlanRequest` carries everything the planner needs: the frame system, the
world state, the start state, and one or more goals. Build the frame system from
the running machine, set the start state to the configuration you want to plan
from, and give the goal as a pose for a named frame.

```go
import (
    "go.viam.com/rdk/motionplan/armplanning"
    "go.viam.com/rdk/referenceframe"
    "go.viam.com/rdk/spatialmath"
    "github.com/golang/geo/r3"
)

// Frame system from the running machine.
fsCfg, err := machine.FrameSystemConfig(ctx)
if err != nil {
    logger.Fatal(err)
}
fs, err := referenceframe.NewFrameSystem("robot", fsCfg.Parts, nil)
if err != nil {
    logger.Fatal(err)
}

// Plan from a known start configuration. Use the arm's current joints to
// verify a real move, or any configuration to test a hypothetical one.
startState := armplanning.NewPlanState(nil, referenceframe.FrameSystemInputs{
    "my-arm": []referenceframe.Input{0, 0, 0, 0, 0, 0},
})

// Goal: place the gripper frame at a pose in the world frame.
goal := armplanning.NewPlanState(referenceframe.FrameSystemPoses{
    "my-gripper": referenceframe.NewPoseInFrame("world",
        spatialmath.NewPose(
            r3.Vector{X: 400, Y: 0, Z: 300},
            &spatialmath.OrientationVectorDegrees{OZ: -1},
        )),
}, nil)

// Fail fast on an infeasible goal instead of grinding for the full default.
opts := armplanning.NewBasicPlannerOptions()
opts.Timeout = 15

plan, _, err := armplanning.PlanMotion(ctx, logger, &armplanning.PlanRequest{
    FrameSystem:    fs,
    StartState:     startState,
    Goals:          []*armplanning.PlanState{goal},
    PlannerOptions: opts,
})
```

The default planner timeout is 300 seconds, so an infeasible plan grinds for
five minutes before failing. When you are verifying feasibility, set a shorter
`Timeout` so an impossible goal fails quickly.

## Read the plan

If `PlanMotion` returns without an error, the goal is feasible from the start
state: the planner found a complete, collision-free trajectory. `plan.Trajectory()`
is that trajectory, a sequence of joint configurations the arm would pass
through.

```go
if err != nil {
    logger.Infof("goal is not feasible: %v", err)
    return
}

traj := plan.Trajectory()
logger.Infof("feasible: %d steps", len(traj))
for i, step := range traj {
    fmt.Printf("step %d: %v\n", i, step["my-arm"])
}
```

An error means no plan was found within the timeout, which is your feasibility
answer. A returned trajectory is yours to inspect, log, compare against an
expected path, or hand to the arm for execution once you are satisfied.

## Plan over the wire with the motion service

`PlanMotion` requires running Go in process with the machine. A remote client
that only has the motion service API can still get a plan without executing, by
sending the plan request through the service's `DoCommand` interface. The
built-in motion service handles a `"plan"` command that runs the same planner as
`Move` and returns the trajectory without moving the arm.

The mechanism is: build a `MoveRequest`, serialize it, and send it under the key
`"plan"`.

```go
import "google.golang.org/protobuf/encoding/protojson"

req := motion.MoveReq{
    ComponentName: "my-gripper",
    Destination:   destination,
}
pbReq, err := req.ToProto("builtin")
if err != nil {
    logger.Fatal(err)
}
payload, err := protojson.Marshal(pbReq)
if err != nil {
    logger.Fatal(err)
}

// The key must be the lowercase string "plan".
resp, err := motionService.DoCommand(ctx, map[string]interface{}{
    "plan": string(payload),
})
if err != nil {
    logger.Fatal(err)
}
// resp carries the planned trajectory under the "plan" key.
```

The trade-offs versus the in-process call:

- The response is untyped. The trajectory comes back as generic map data, and
  its exact shape depends on the transport, so you parse it by hand rather than
  receiving a typed `Plan`.
- You drive it with string keys instead of typed parameters, which is easier to
  get wrong.
- It works for any remote client of the motion service, with no need to
  assemble the frame system or pull the planner into your process.

Use the in-process `PlanMotion` when you have Go access to the machine and want
the plan as typed data. Use the `"plan"` `DoCommand` when you are a remote client
and the motion service is all you have. The
[viamkit](https://github.com/viam-labs/viamkit) library wraps the `DoCommand`
form and smooths over the response parsing.

## What's next

- [Move through waypoints](/motion-planning/move-an-arm/multiple-waypoints/):
  plan one trajectory through an ordered list of goals.
- [How motion planning works](/motion-planning/how-planning-works/):
  why a plan can be infeasible and what to adjust.
- [Debug motion with the CLI](/motion-planning/debug-motion-with-cli/):
  inspect frames and poses from the command line.
