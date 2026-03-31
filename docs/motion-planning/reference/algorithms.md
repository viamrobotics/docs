---
linkTitle: "Algorithms"
title: "Motion Planning Algorithms"
weight: 50
layout: "docs"
type: "docs"
description: "How Viam's motion planner computes collision-free paths for robot arms."
aliases:
  - /reference/services/motion/algorithms/
  - /services/motion/algorithms/
  - /mobility/motion/algorithms/
---

## When you need this

Most users do not need to understand the planning algorithm. You define frames,
obstacles, and constraints, then call `Move`. The planner handles the rest.

This page is useful when:

- You need to tune planning performance (timeout, resolution).
- You are debugging why the planner fails to find a path.
- You want to understand what the planner is doing under the hood.

## The cBiRRT algorithm

Viam's motion service uses **cBiRRT** (Constrained Bidirectional
Rapidly-Exploring Random Tree), based on Berenson et al. 2009. This is the
only planning algorithm in the builtin motion service. There is no
configuration option to select a different algorithm.

### How it works

cBiRRT grows two search trees simultaneously: one from the start configuration
and one from the goal configuration. At each iteration, the algorithm:

1. **Samples** a random configuration in joint space.
2. **Extends** the nearest node in one tree toward the sample, checking
   constraints and collisions at each step.
3. **Attempts to connect** the two trees. If a connection is found, the path
   is complete.
4. **Projects** each new configuration onto the constraint manifold, ensuring
   constraints are satisfied throughout the path.

The bidirectional approach is significantly faster than growing a single tree,
because both trees converge toward the middle simultaneously.

### Why it works well for robot arms

- **High-dimensional spaces**: A 6-axis arm has 6 degrees of freedom. cBiRRT
  handles this efficiently through random sampling.
- **Constraint satisfaction**: The projection step ensures constraints (linear,
  orientation) are satisfied, not just checked.
- **Bidirectional search**: Finding a path in 6D space from both ends is much
  faster than searching from one end only.

### What it does not do

- **No optimal paths**: cBiRRT finds _a_ valid path, not the shortest or
  smoothest path. The builtin service applies path smoothing (default 30
  iterations) after planning to improve the result.
- **No dynamic replanning**: The planner computes a full path before execution
  begins. It does not adjust the path during execution.

## Tuning parameters

The planner accepts configuration through the motion service config and through
per-request options. Most users do not need to change these.

### Service-level config

These are set in the motion service configuration:

| Field                        | Type   | Default          | Description                             |
| ---------------------------- | ------ | ---------------- | --------------------------------------- |
| `num_threads`                | int    | (system default) | Number of threads for parallel planning |
| `log_file_path`              | string | (none)           | Path to write planning logs             |
| `log_planner_errors`         | bool   | false            | Log planning errors                     |
| `log_slow_plan_threshold_ms` | int    | (none)           | Log plans that take longer than this    |

### Planning defaults

These defaults are compiled into the builtin motion service:

| Parameter            | Default     | Description                                              |
| -------------------- | ----------- | -------------------------------------------------------- |
| Timeout              | 300 seconds | Maximum time to search for a path                        |
| Resolution           | 2.0         | Constraint-checking granularity (mm or degrees per step) |
| Max IK solutions     | 100         | Maximum inverse kinematics solutions to seed the search  |
| Smoothing iterations | 30          | Post-planning path smoothing passes                      |
| Collision buffer     | 150 mm      | Clearance around obstacles                               |

### When planning fails

If the planner returns an error ("no path found" or similar), consider:

1. **Loosen constraints.** Tight linear or orientation tolerances can make the
   constrained space too small to navigate.
2. **Reduce obstacle sizes.** Oversized obstacles leave no room for the arm
   to pass.
3. **Check joint limits.** If the kinematics file has joint limits tighter than
   the physical arm, the planner may not explore valid configurations.
4. **Check the destination.** The destination pose must be reachable and not
   inside an obstacle.
5. **Increase timeout.** For complex environments, the default 300-second
   timeout may not be enough, though this is rare.

## What's Next

- [Configure Motion Constraints](/motion-planning/constraints/): the
  constraint types that cBiRRT enforces during planning.
- [Define Obstacles](/motion-planning/obstacles/): collision geometry that
  the planner routes around.
- [Motion Service Configuration](/motion-planning/reference/motion-service/):
  full configuration reference.
