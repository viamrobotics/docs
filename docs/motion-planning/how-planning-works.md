---
linkTitle: "How planning works"
title: "How motion planning works"
weight: 90
layout: "docs"
type: "docs"
description: "How Viam plans arm motion: the direct joint-space path it tries first, the cBiRRT fallback, and what to try when planning fails."
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

When planning fails (and it sometimes will, because the fallback search
is probabilistic), the error messages mean little unless you understand
what the planner was trying to do. This page gives you that model.

## First attempt: a straight line in joint space

The planner tries the simplest possible motion before it searches.
For each goal, it:

1. **Generates goal configurations.** An inverse kinematics (IK) solver
   produces up to 100 joint configurations that place the moving frame
   at the target pose.
2. **Ranks them by joint travel.** Each configuration is scored by how
   far the joints move from the start configuration, with a small
   preference for keeping joints near the middle of their range.
3. **Checks a straight line to each.** The planner interpolates directly
   through joint space from the start to each configuration, checking
   collisions and constraints every 2 mm or 2 degrees of movement.

If a configuration passes the straight-line check at a reasonable cost
(within three times the joint travel of the best-ranked configuration),
the planner returns that straight-line path immediately. In an
uncluttered workspace, most requests end here: each joint sweeps from
its start angle to its goal angle, and the sampling search described
below never runs.

A [linear constraint](/motion-planning/move-an-arm/constraints/) keeps
planning in this stage. The planner splits the motion into short
Cartesian steps (shorter steps for tighter tolerances) and solves each
step with its own straight-line path. Tolerances below 10 mm or
10 degrees also turn off the fallback: the constraint rules out
detours, so planning fails when any step lacks a valid straight-line
solution.

## Fallback: cBiRRT

When an obstacle or constraint blocks every straight-line candidate,
the planner falls back to **cBiRRT** (Constrained Bidirectional
Rapidly-Exploring Random Tree), which handles the general arm-planning
case. It is the only fallback algorithm in the built-in service;
modules may implement alternative planners.

cBiRRT comes from [Berenson et al., 2009](https://www.ri.cmu.edu/publications/manipulation-planning-on-constraint-manifolds/). The name unpacks to three ideas:
the "constrained" part enforces orientation and linear constraints, the
"bidirectional" part searches from the start and the goal at the same time,
and the "RRT" part samples random configurations to explore joint space.

The goal tree starts from the IK configurations that failed the
straight-line check, so the work from the first stage seeds the search.
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
sequential passes with triplet step sizes of 10, 3, and 1) to remove
unnecessary detours. Straight-line paths from the first stage skip
smoothing; they are already as direct as possible.

## Why this two-stage design works for arms

- **Cheap wins stay cheap.** The straight-line check costs a handful of
  IK solves and collision checks. When it succeeds, the arm gets a
  direct, predictable motion and the request skips the sampled search.
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

Setting the right expectations matters. The two-stage planner is not a
silver bullet.

**It does not find globally optimal paths.** A successful first stage
returns the straight line in joint space, the shortest motion to that
IK solution. The fallback finds a valid path, not the shortest or
smoothest one. The three-pass smoothing improves the result, but the
result is not guaranteed to be close to optimal.

**The fallback is probabilistic.** Because cBiRRT samples randomly, the
same request can succeed sometimes and fail other times. This is a
fundamental property of the algorithm family, not a bug. Callers should
be prepared to retry when a plan fails, and should not be surprised if a
previously-successful request sometimes times out.

**It does not replan mid-execution.** The motion service computes the
full path before execution begins. If a new obstacle appears after the
arm starts moving, the planner does not react.

**It is not a controller.** The planner produces the plan, but the arm's
module executes it. Vendor-level protections (singularity protective
stops, joint-limit safety, speed overrides) are applied by the module
and may cause execution-time errors even after planning succeeds.

## When planning fails

The planner returns an error if it cannot find a path within the
planning timeout (300 seconds by default). Common causes:

1. **Frames are not linked to the world frame.** If any configured frame
   has a parent that does not exist or creates an orphaned subtree
   disconnected from the world frame, the motion service returns an
   error listing the unlinked parts. Fix the frame configuration so
   every component traces back to the world frame through its parent
   chain. This commonly happens when you rename a component (such as an
   arm) without updating the `parent` field on components attached to
   it (such as a gripper or camera).
2. **Constraints are too tight.** A linear or orientation tolerance below
   a few millimeters or a few degrees can make the constrained space too
   small for the algorithm to explore. Start with larger tolerances and
   tighten only as needed.
3. **Obstacles leave no room.** Oversized obstacle geometries close off
   valid corridors. Try smaller geometries or remove temporarily to
   isolate the problem.
4. **Joint limits are more restrictive than you expect.** Check the
   kinematics file: the planner only explores configurations inside the
   declared limits.
5. **The destination is inside an obstacle or outside the arm's reach.**
   Use `GetEndPosition` on the arm to read its current pose, then try a
   simpler target close to the current position to isolate whether the
   planner works at all.
6. **Multiple IK solutions exist but the one the planner picks is bad.**
   The planner prefers the IK solution with the least joint travel, but
   when the fallback runs, cBiRRT returns the first feasible path it
   finds. For some Cartesian targets it routes through a wrist flip or
   an elbow reconfiguration that is physically feasible but undesirable.
   Move the arm to a configuration that biases the planner toward the
   IK branch you want by calling `MoveToJointPositions` first, or break
   the motion into smaller steps.

If the failure is non-deterministic (the same plan worked last time but
fails now), retry a few times before changing the request. The
fallback's probabilistic nature means some retries succeed.

## What's next

- [Motion service configuration](/motion-planning/reference/motion-service/):
  tune planning defaults through config attributes or per-call `extra`.
- [Motion planning algorithms](/motion-planning/reference/algorithms/):
  terse summary of the planning stages, defaults, and tuning surface.
- [Configure motion constraints](/motion-planning/move-an-arm/constraints/):
  the four constraint types the planner enforces.
