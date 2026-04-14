---
linkTitle: "Algorithms"
title: "Motion planning algorithms"
weight: 50
layout: "docs"
type: "docs"
description: "The planning algorithm used by the built-in motion service and the tuning surfaces exposed to callers."
aliases:
  - /reference/services/motion/algorithms/
  - /services/motion/algorithms/
  - /mobility/motion/algorithms/
---

The built-in motion service uses a single planning algorithm. This page
catalogs the algorithm, its defaults, and where each tunable is exposed
to callers. For the conceptual explanation (how the algorithm works,
what it does not do, what to try when it fails), see
[How motion planning works](/motion-planning/how-planning-works/).

## Algorithm

| Field        | Value                                                                  |
| ------------ | ---------------------------------------------------------------------- |
| Name         | cBiRRT (Constrained Bidirectional Rapidly-Exploring Random Tree)       |
| Source code  | `rdk/motionplan/armplanning/cBiRRT.go`                                 |
| Source paper | Berenson et al., _Manipulation planning on constraint manifolds_, 2009 |
| Properties   | Sampling-based, bidirectional, probabilistic                           |

## Planning defaults

The full default set is documented in
[Motion service configuration](/motion-planning/reference/motion-service/#planning-defaults).
The planner-relevant entries are:

| Parameter            | Default                    |
| -------------------- | -------------------------- |
| Planning timeout     | 300 seconds                |
| Resolution           | 2.0 (mm or degrees/step)   |
| Max IK solutions     | 100                        |
| Smoothing iterations | 3 passes of sizes 10, 3, 1 |
| Collision buffer     | 1e-8 mm (effectively zero) |

## Tuning surfaces

There are two ways to override a default.

| Where                                | Scope                   | Example tunables                                                    |
| ------------------------------------ | ----------------------- | ------------------------------------------------------------------- |
| Motion service config (`attributes`) | Persistent, per-service | `num_threads`, `input_range_override`, planner-diagnostic flags     |
| `extra` map on a Move request        | Per-request             | `collision_buffer_mm`, `max_ik_solutions`, `timeout`, `smooth_iter` |

See [Motion service configuration](/motion-planning/reference/motion-service/)
for the full list of configuration attributes.

## What's next

- [How motion planning works](/motion-planning/how-planning-works/):
  conceptual explanation of cBiRRT and its limits.
- [Motion service configuration](/motion-planning/reference/motion-service/):
  full configuration reference.
- [Configure motion constraints](/motion-planning/constraints/):
  the four constraint types the planner enforces.
