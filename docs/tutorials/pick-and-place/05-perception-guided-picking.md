---
title: "Phase 5: Perception-guided picking"
linkTitle: "5. Perception-guided picking"
type: "docs"
slug: "perception-guided-picking"
weight: 50
description: "Add the vision pipeline and write the perception loop that detects a block, transforms it to the world frame, and picks it with motion planning."
workshop: "pick-and-place"
toc_hide: true
phase: 5
phase_total: 6
time_estimate: "22 minutes"
prev: "/tutorials/pick-and-place/control-the-robot-from-python/"
next: "/tutorials/pick-and-place/inline-module/"
languages: ["python"]
---

In this phase you replace the fixed grasp pose from Phase 4 with live perception: the vision service detects a block, the frame system transforms its position into world space, and the motion service plans a collision-free pick.

{{< workshop-phases >}}

## Configure the vision pipeline

<!-- TODO: authored in a later task -->

## The frame system and transform_pose

<!-- TODO: authored in a later task. Explain transform_pose and how the frame system converts camera-space detections to world-space arm targets, from slides Phase 4. -->

## Detect from home (the wrist-camera rule)

<!-- TODO: authored in a later task -->

## Compute the approach and grasp poses

<!-- TODO: authored in a later task. Integrate the vision service call into the loop: detect objects, select the target, compute the pick pose. Use len(o.point_cloud) to pick the largest object, NOT o.point_cloud.size (slide error corrected in plan). -->

## Run the full pick loop

<!-- TODO: authored in a later task. Show how to pass the table obstacle geometry to move_to_position so the motion planner avoids it, from slides Phase 4. -->

## Debugging guide

<!-- TODO: authored in a later task. List perception-specific failure modes from slides Phase 4 and plan page 04: frame mismatch symptoms, vision false positives. -->

{{< workshop-nav >}}
