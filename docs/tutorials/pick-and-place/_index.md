---
title: "Vision-Guided Pick-and-Place with the xArm6"
linkTitle: "Pick-and-Place Workshop"
type: "docs"
weight: 50
description: "Build a robot that detects, picks, and sorts colored cubes with vision and motion planning, from static poses to a Python script to an optional module."
authors: []
level: "Intermediate"
languages: ["python"]
viamresources:
  ["arm", "gripper", "camera", "vision", "motion", "frame_system", "switch"]
platformarea: ["mobility", "core"]
tags: ["tutorial", "workshop", "arm", "vision", "motion"]
workshop: "pick-and-place"
workshop_overview: true
time_estimate: "2 hours"
hardware:
  - "uFactory xArm6"
  - "Intel RealSense D435"
  - "uFactory finger gripper"
  - "System76 Meerkat"
companion_repo: "https://github.com/viam-devrel/pick-and-place"
no_list: true
---

In this workshop you build a vision-guided robot that detects colored cubes, picks each one up, and drops it in the correct bin, sorted by color. The workshop is structured as six sequential phases, each ending with a working system state you can verify before moving on. Completing Phase 4 (the local Python script) is a full success; Phase 5 (packaging your script as an inline module) is optional.

## What you'll build

You will configure an xArm6 robotic arm fitted with a finger gripper and an Intel RealSense depth camera. A color-detection vision service identifies cube positions in camera space; the Viam motion service plans and executes collision-free arm movements to pick each cube and place it in the right bin. By the end of Phase 4 you have a Python script you can run from your laptop that drives the full pick-and-sort cycle autonomously.

<!-- TODO: add hardware-overview photo to assets/tutorials/pick-and-place/ and reference via images frontmatter once available -->

## Hardware

- **uFactory xArm6**: the six-axis robotic arm that picks and places the cubes.
- **Intel RealSense D435**: the depth camera mounted to detect cube positions and colors.
- **uFactory finger gripper**: the end-effector that grasps the cubes.
- **System76 Meerkat**: the on-robot mini-PC that runs the Viam machine server.

## Phases

1. **[Platform mental model](/tutorials/pick-and-place/platform-mental-model/)** (~15 min)
2. **[Configure resources and explore the app](/tutorials/pick-and-place/configure-resources/)** (~20 min)
3. **[Static positions and safety obstacles](/tutorials/pick-and-place/static-positions/)** (~20 min)
4. **[Control the robot from Python](/tutorials/pick-and-place/control-the-robot-from-python/)** (~15 min) — milestone one
5. **[Perception-guided picking](/tutorials/pick-and-place/perception-guided-picking/)** (~22 min) — milestone two
6. **[Inline module](/tutorials/pick-and-place/inline-module/)** (~20 min, optional)

## Prerequisites

**Hardware pre-provisioned for you:** if you are in a guided workshop where the hardware is already set up, skip directly to [Phase 1](/tutorials/pick-and-place/platform-mental-model/).

**Provisioning your own hardware:** complete the hardware setup guide first (forthcoming), then return here for [Phase 1](/tutorials/pick-and-place/platform-mental-model/). The setup guide covers mounting the camera, connecting the arm controller, and installing viam-server on the Meerkat.

Before Phase 4 you also need Python 3.10 or newer and the Viam Python SDK on the machine you will run the script from. Verify with:

```sh
python3 --version          # 3.10 or newer
python3 -c "import viam"    # must succeed
```

## Companion code

All supporting files for this workshop live in the [viam-devrel/pick-and-place](https://github.com/viam-devrel/pick-and-place) repository. It contains the machine config fragment you will import in Phase 2, the starter script for Phase 4, and the reference solution for Phase 5.

<!-- TODO: the companion repo does not exist yet; the link above is a placeholder and will 404 until the repo is created and populated. -->
