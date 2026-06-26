---
title: "Phase 4: Local Python script"
linkTitle: "4. Local Python script"
type: "docs"
slug: "local-python-script"
weight: 40
description: "Connect from your laptop, run the static sequence, then add perception to complete the pick-and-sort loop."
workshop: "pick-and-place"
phase: 4
phase_total: 5
time_estimate: "30 minutes"
prev: "/tutorials/pick-and-place/static-positions/"
next: "/tutorials/pick-and-place/inline-module/"
languages: ["python"]
draft: true
---

This is the core phase of the workshop: you write and run a Python script on your laptop that connects to the robot, executes the static pick-and-place sequence from Phase 3, and then adds live color detection to sort cubes autonomously.

{{< workshop-phases >}}

## Why a script before a module

<!-- TODO: explain from slides Phase 4 why starting with a local script (fast iteration, local debugger, print statements) is the right approach before packaging as a module. -->

## Check your environment

<!-- TODO: present the environment setup steps from slides Phase 4 and plan page 04. -->
<!-- TODO: present uv as the primary path; pip is a fallback only. -->

## Connect to your robot

<!-- TODO: show the RobotClient.at_address / at_cloud pattern from slides Phase 4, including where to find the machine address and API key in the Viam app. -->

## Run the static sequence

<!-- TODO: walk through the starter script from plan page 04 / companion repo that calls the named positions defined in Phase 3, with expected arm movement to verify. -->

## The frame system and transforms

<!-- TODO: explain transform_pose and how the frame system converts camera-space detections to world-space arm targets, from slides Phase 4. -->

## Add perception

<!-- TODO: integrate the vision service call into the loop from slides Phase 4: detect objects, select the target, compute the pick pose. -->
<!-- TODO: use len(o.point_cloud) to pick the largest object, NOT o.point_cloud.size (slide error corrected in plan). -->

## Pass obstacles to the motion service

<!-- TODO: show how to pass the table obstacle geometry to move_to_position so the motion planner avoids it, from slides Phase 4. -->

## Debugging guide

<!-- TODO: list common failure modes from slides Phase 4 and plan page 04: connection errors, frame mismatch symptoms, gripper timing, vision false positives. -->

{{< workshop-nav >}}
