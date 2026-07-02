---
title: "Phase 4: Control the robot from Python"
linkTitle: "4. Control from Python"
type: "docs"
slug: "control-the-robot-from-python"
weight: 40
description: "Connect from your laptop and drive the saved static pick-and-place sequence from a Python script."
workshop: "pick-and-place"
toc_hide: true
phase: 4
phase_total: 6
time_estimate: "15 minutes"
prev: "/tutorials/pick-and-place/static-positions/"
next: "/tutorials/pick-and-place/perception-guided-picking/"
languages: ["python"]
---

In this phase you write and run a Python script on your laptop that connects to the robot and executes the static pick-and-place sequence from Phase 3. This proves your connection, environment, and named positions work end to end before you add perception in Phase 5.

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

## Debugging guide

<!-- TODO: list common failure modes from slides Phase 4 and plan page 04: connection errors, environment setup issues, gripper timing. Perception-specific failure modes (frame mismatch, vision false positives) move to the Phase 5 debugging guide. -->

{{< workshop-nav >}}
