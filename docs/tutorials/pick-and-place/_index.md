---
title: "Vision-Guided Pick-and-Place with the xArm6"
linkTitle: "Pick-and-Place Workshop"
type: "docs"
weight: 50
description: "Build a vision-guided robot that detects blocks by shape and places them into a bin with motion planning, from manual control to programming an autonomous workflow in Python."
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

The workshop is structured as six sequential phases, each ending with checkpoints you can verify before moving on. The workshop has two milestones: by the end of Phase 4 you drive the robot from your own code through a static, pre-planned sequence (milestone one), and by the end of Phase 5 you close the loop with live perception so the robot detects, picks, and places blocks on its own (milestone two).

## What you'll build

<!-- ASSET P0 hero-hardware-overview (PHOTO): complete rig staged (xArm6 + gripper + wrist RealSense + blocks + bin + Meerkat). See plans/2026-07-02-pick-and-place-shot-list.md -->

{{<imgproc src="/tutorials/pick-and-place/hero-hardware-overview.jpeg" resize="1200x" declaredimensions=true alt="The staged pick-and-place workstation: a uFactory xArm6 arm with a two-finger gripper and a wrist-mounted RealSense camera, colored blocks, and a bin.">}}

You will configure an xArm6 robotic arm fitted with a two-finger gripper and a wrist-mounted Intel RealSense depth camera. A shape-detection vision service finds blocks, and the motion service plans collision-free picks that place each block in the bin. By the end, you will have a Python script you run from your laptop and a deployable module that drives the full detect-pick-place loop.

## Required hardware

- **uFactory xArm6**: the six-axis robotic arm that picks and places the blocks.
- **Intel RealSense D435**: the wrist-mounted depth camera that detects block positions by shape.
- **uFactory finger gripper**: the end-effector that grasps the blocks.
- **System76 Meerkat**: the on-robot mini-PC that runs the Viam machine server.

## Phases

Phases 1 through 5 are the core workshop. Phase 6 is optional.

1. **[Platform mental model](/tutorials/pick-and-place/platform-mental-model/)** (~20 min)
2. **[Configure resources and explore the app](/tutorials/pick-and-place/configure-resources/)** (~15 min)
3. **[Static positions and obstacles](/tutorials/pick-and-place/static-positions/)** (~20 min)
4. **[Control the robot from Python](/tutorials/pick-and-place/control-the-robot-from-python/)** (~15 min, milestone one)
5. **[Perception-guided picking](/tutorials/pick-and-place/perception-guided-picking/)** (~22 min, milestone two)
6. **[Inline module](/tutorials/pick-and-place/inline-module/)** (~20 min, optional)

When you finish, the **[wrap-up](/tutorials/pick-and-place/wrap-up/)** reviews what you built and points to next steps.

## Companion code

All supporting files for this workshop live in the [viam-devrel/pick-and-place](https://github.com/viam-devrel/pick-and-place) repository. You do not need it to start, but the prerequisites below reference its `scripts/` project, and later phases pull from it.

- `config/` holds a machine config fragment and an obstacles template. Use them to check your work after you configure resources by hand.
- `scripts/` holds the starter script for Phase 4 and the reference solution for Phase 5.

## Prerequisites

This is a self-serve workshop, so confirm each of the following before you start:

- **Python 3.10 or newer.** Install it with [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or from [python.org](https://www.python.org/downloads/).
- **The Viam Python SDK.** The companion `scripts/` project already declares `viam-sdk`, so `uv run` installs it for you in Phase 4. See the [Python SDK docs](https://python.viam.dev/) for reference. Pip works too if you prefer it.
- **A working terminal** on the machine you will run the Phase 4 and Phase 5 scripts from, typically your personal computer rather than the robot's Meerkat.
- **A Viam account with an online machine.** Log in at [app.viam.com](https://app.viam.com), [create a machine](https://docs.viam.com/set-up-a-machine/first-machine/), and confirm the green **Live** indicator before you begin.

### Validate your environment

<!-- ASSET P1 env-validate (TERM): python3 --version and uv run --with viam-sdk import viam printing a version -->

Before starting Phase 4, confirm your environment is ready:

```sh
python3 --version   # 3.10 or newer
uv run --with viam-sdk python -c "import viam; print(viam.__version__)"   # prints a version
```

If either command fails, revisit the checklist above before continuing.

### Where to start

<!-- ASSET P1 live-indicator (UI+): machine page with the green Live indicator boxed -->

{{<imgproc src="/tutorials/pick-and-place/live-indicator.png" resize="1200x" declaredimensions=true alt="A Viam machine page showing the green Live indicator.">}}

- **Hardware ready (`viam-server` running):** start at [Phase 1](/tutorials/pick-and-place/platform-mental-model/).
- **Provisioning your own hardware:** complete [the hardware setup](https://docs.viam.com/set-up-a-machine/first-machine/), then return here for [Phase 1](/tutorials/pick-and-place/platform-mental-model/).
