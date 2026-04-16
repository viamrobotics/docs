---
linkTitle: "How planning works"
title: "How motion planning works"
weight: 90
layout: "docs"
type: "docs"
description: "The algorithm Viam uses to plan robot arm motion, why it works for arms, and what to try when planning fails."
---

Motion planning finds a safe, joint-level path from one arm configuration to
another. The planner takes the arm's kinematic model, the target pose, the
world state (obstacles and supplementary transforms), and any motion
constraints, and it returns a sequence of joint configurations the arm can
execute without colliding with itself or its environment.

This is a search problem in a high-dimensional space: a 6-DOF arm has
six joints, so every configuration is a point in six-dimensional joint
space. The planner has to find a continuous path through this space
that satisfies all the constraints.

## The algorithm: cBiRRT

Viam's built-in motion service uses **cBiRRT**: Constrained Bidirectional
Rapidly-Exploring Random Tree. This is the only planning algorithm in
the built-in service. Modules may implement alternative planners, but
cBiRRT handles the general arm-planning case.

cBiRRT comes from [Berenson et al., 2009](https://www.ri.cmu.edu/pub_files/2009/5/berenson_dmitry_2009_2.pdf). The name unpacks to three ideas:
the "constrained" part enforces orientation and linear constraints, the
"bidirectional" part searches from the start and the goal at the same time,
and the "RRT" part samples random configurations to explore joint space.

## How the planner searches

At each iteration, the planner:

1. **Samples** a random configuration in joint space.
2. **Extends** the nearest node in one of the two trees toward the
   sample, checking constraints and collisions at small steps along the
   way.
3. **Attempts to connect** the two trees. If a configuration in one tree
   reaches a configuration in the other without violating a constraint or
   colliding with anything, the search ends.
4. **Projects** each new configuration onto the constraint manifold,
   adjusting joint angles so the resulting pose satisfies any
   orientation or line constraint.

When the two trees meet, the planner smooths the resulting path (three
sequential passes of 10, 3, and 1 iterations) to remove unnecessary
detours.

## Why this works well for arms

- **High-dimensional spaces.** A 6-DOF arm's joint space is far too large
  to search exhaustively. Random sampling is asymptotically complete:
  given enough time, the algorithm finds a path if one exists.
- **Constraint satisfaction, not just collision avoidance.** The
  projection step actively enforces constraints on every intermediate
  configuration, so the planner does not return paths that silently
  violate orientation or line constraints.
- **Bidirectional search.** Growing both trees toward the middle is
  significantly faster than searching from one end only. This matters
  when paths are long or the goal is hard to reach from the start.

## What the planner does not do

Setting the right expectations matters. cBiRRT is not a silver bullet.

**It does not find optimal paths.** cBiRRT finds a valid path, not the
shortest or smoothest one. The three-pass smoothing improves the result,
but the result is not guaranteed to be close to optimal.

**It is probabilistic.** Because sampling is random, the same request
can succeed sometimes and fail other times. This is a fundamental
property of the algorithm family, not a bug. Callers should be prepared
to retry when a plan fails, and should not be surprised if a
previously-successful request sometimes times out.

**It does not replan mid-execution.** The motion service computes the
full path before execution begins. If a new obstacle appears after the
arm starts moving, the planner does not react. Base navigation through
`MoveOnMap` and `MoveOnGlobe` is different: those methods monitor plan
deviation and replan dynamically.

**It is not a controller.** cBiRRT produces the plan, but the arm's
module executes it. Vendor-level protections (singularity protective
stops, joint-limit safety, speed overrides) are applied by the module
and may cause execution-time errors even after planning succeeds.

## When planning fails

The planner returns an error if it cannot find a path within the
planning timeout (300 seconds by default). Common causes:

1. **Constraints are too tight.** A linear or orientation tolerance below
   a few millimeters or a few degrees can make the constrained space too
   small for the algorithm to explore. Start with larger tolerances and
   tighten only as needed.
2. **Obstacles leave no room.** Oversized obstacle geometries close off
   valid corridors. Try smaller geometries or remove temporarily to
   isolate the problem.
3. **Joint limits are more restrictive than you expect.** Check the
   kinematics file: the planner only explores configurations inside the
   declared limits.
4. **The destination is inside an obstacle or outside the arm's reach.**
   Use `GetEndPosition` on the arm to read its current pose, then try a
   simpler target close to the current position to isolate whether the
   planner works at all.
5. **Multiple IK solutions exist but the one the planner picks is bad.**
   cBiRRT plans shortest-path in joint space, so for some Cartesian targets
   it routes through a wrist flip or an elbow reconfiguration that is
   physically feasible but undesirable. Seed the planner by calling
   `MoveToJointPositions` first, or break the motion into smaller steps.

If the failure is non-deterministic (the same plan worked last time but
fails now), retry a few times before changing the request. The
algorithm's probabilistic nature means some retries succeed.

## What's next

- [Motion service configuration](/motion-planning/reference/motion-service/):
  tune planning defaults through config attributes or per-call `extra`.
- [Motion planning algorithms](/motion-planning/reference/algorithms/):
  terse summary of the algorithm, defaults, and tuning surface.
- [Configure motion constraints](/motion-planning/move-an-arm/constraints/):
  the four constraint types the planner enforces.
- [Monitor a running plan](/motion-planning/monitor-a-running-plan/):
  handle non-blocking plans and reason about state transitions.
