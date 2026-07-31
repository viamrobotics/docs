---
linkTitle: "Motion planning algorithms"
title: "Motion planning algorithms"
weight: 50
layout: "docs"
type: "docs"
description: "The two-stage planning strategy the built-in motion service uses and the tuning surfaces exposed to callers."
aliases:
  - /reference/services/motion/algorithms/
  - /operate/reference/services/motion/algorithms/
  - /services/motion/algorithms/
  - /mobility/motion/algorithms/
---

The builtin motion service plans in two stages. It first generates inverse kinematics (IK) solutions for the goal pose and checks whether the arm can reach one along a straight line through joint space. When no straight-line path clears collisions and constraints, it falls back to the cBiRRT search algorithm. When you need to change how the motion service plans, this page tells you what runs in each stage, what the defaults are, and where each tunable lives. For how the two stages work, their limits, and what to try when planning fails, see [How motion planning works](/motion-planning/how-planning-works/).

## Planning strategy

| Stage                   | What runs                                                                     | Outcome                                                                              |
| ----------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| 1. Direct interpolation | IK solution generation plus a straight-line joint-space collision check       | Returns the straight-line path when a low-cost IK solution passes the check          |
| 2. cBiRRT fallback      | Sampling-based bidirectional tree search seeded with the stage-1 IK solutions | Returns a smoothed path, or an error when no path exists within the planning timeout |

## cBiRRT

| Field        | Value                                                                                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Name         | cBiRRT (Constrained Bidirectional Rapidly-Exploring Random Tree)                                                                                             |
| Role         | Fallback when no low-cost IK solution has a valid straight-line path                                                                                         |
| Source code  | `rdk/motionplan/armplanning/cBiRRT.go`                                                                                                                       |
| Source paper | Berenson et al., [_Manipulation planning on constraint manifolds_](https://www.ri.cmu.edu/publications/manipulation-planning-on-constraint-manifolds/), 2009 |
| Properties   | Sampling-based, bidirectional, probabilistic                                                                                                                 |

## Planning defaults

The full default set is documented in
[Motion service configuration](/motion-planning/reference/motion-service/#planning-defaults).
The planner-relevant entries are:

| Parameter                           | Default                                     |
| ----------------------------------- | ------------------------------------------- |
| Planning timeout                    | 300 seconds                                 |
| Resolution                          | 2.0 (mm or degrees/step)                    |
| Max IK solutions                    | 100                                         |
| Direct-path cost gate               | 3x the joint travel of the best IK solution |
| Smoothing iterations (cBiRRT paths) | 3 passes of sizes 10, 3, 1                  |
| Collision buffer                    | 1e-8 mm (effectively zero)                  |

## Tuning surfaces

Callers override a default in one of two places: persistently in the motion service config, or per call through the `extra` map on a `Move` request. The table below shows which tunables live where.

| Where                                | Scope                   | Example tunables                                                |
| ------------------------------------ | ----------------------- | --------------------------------------------------------------- |
| Motion service config (`attributes`) | Persistent, per-service | `num_threads`, `input_range_override`, planner-diagnostic flags |
| `extra` map on a Move request        | Per-request             | `collision_buffer_mm`, `max_ik_solutions`, `timeout`            |

See [Motion service configuration](/motion-planning/reference/motion-service/)
for the full list of configuration attributes.

## What's next

- [How motion planning works](/motion-planning/how-planning-works/):
  conceptual explanation of the two planning stages and their limits.
- [Motion service configuration](/motion-planning/reference/motion-service/):
  full configuration reference.
- [Configure motion constraints](/motion-planning/move-an-arm/constraints/):
  the four constraint types the planner enforces.
