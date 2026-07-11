---
title: "Miniature Palletizing with the SO-ARM101"
linkTitle: "SO-ARM101 Palletizing Workshop"
type: "docs"
weight: 60
description: "Build a desktop palletizing robot with an affordable SO-ARM101 arm, the physical twin of the simulated Viam 101 palletizer. Teach its poses by hand, then program a collision-free pick-and-stack in Python."
authors: []
level: "Intermediate"
languages: ["python"]
viamresources: ["arm", "gripper", "motion", "frame_system"]
platformarea: ["mobility", "core"]
tags: ["tutorial", "workshop", "arm", "motion", "frame-system"]
workshop: "so-arm101-palletizing"
workshop_overview: true
time_estimate: "2 hours"
hardware:
  - "SO-ARM101 (5-DOF + gripper)"
  - "8 × ~20 mm cubes"
  - "Raspberry Pi or laptop host"
companion_repo: "https://github.com/viam-devrel/so-arm101-palletizing"
no_list: true
draft: true
---

You will build a miniature palletizing cell: an SO-ARM101 arm picks cubes from a staging spot and stacks them on a small pallet, two layers of four. It's the same set of concepts as the simulated Viam 101 course, but running on a real arm you can hold in your hands.

The workshop is structured as six sequential phases, each ending with checkpoints you can verify before moving on. Finishing Phase 4, where you drive the robot from your own Python code through a static, pre-planned pack, is a complete success. Phases 5 and 6 go further.

## What you'll build

You will configure an SO-ARM101 arm with its finger gripper, teach it a small set of anchor poses by hand using its freedrive (torque-off) capability, then write a Python script that reads those poses back and plans a collision-free pick-and-stack sequence. By the end, you will have packed a two-by-two-by-two stack of cubes onto a marked pallet area, all driven by code you wrote yourself.

<!-- ASSET hero-cell-overview (PHOTO): staged SO-ARM101 + cubes + pallet grid + staging spot -->

## Required hardware

- **SO-ARM101**: the five degree-of-freedom (5-DOF) arm with a finger gripper, connected to its host over USB serial.
- **Eight cubes**, roughly 20 mm on a side.
- **A flat surface** with a marked pallet area about 60 by 60 mm, plus a staging spot for the cubes.
- **A host**, either a Raspberry Pi or a laptop, running `viam-agent` and `viam-server`.

You do not need a camera or a 3D-printed jig for this workshop.

## Phases

Phases 1 through 4 are the core workshop. Phase 5 adds obstacle avoidance, and Phase 6 is optional.

1. **[Platform mental model](/tutorials/so-arm101-palletizing/platform-mental-model/)** (~15 min)
2. **[Configure the SO-ARM101](/tutorials/so-arm101-palletizing/configure-the-arm/)** (~20 min)
3. **[Teach the cell by hand](/tutorials/so-arm101-palletizing/teach-the-cell/)** (~20 min)
4. **[Pack from Python](/tutorials/so-arm101-palletizing/pack-from-python/)** (~20 min, milestone one: a static pack from your own code)
5. **[Avoid placed cubes](/tutorials/so-arm101-palletizing/avoid-placed-cubes/)** (~22 min, milestone two: a collision-free full pack)
6. **[Wrap it in a module](/tutorials/so-arm101-palletizing/inline-module/)** (~15 min, optional)

## How this relates to Viam 101

This workshop is the physical twin of the simulated palletizer in the Viam 101 course: the same frame system, motion, and WorldState ideas apply here. On real hardware, you also learn to map the physical world into the arm's frame and to reason about a 5-DOF arm's reach. A 5-DOF arm plans to a target position without pinning the final orientation, and because the cubes are rotationally symmetric, that does not matter for this task.

## Companion code

All supporting files for this workshop live in the [viam-devrel/so-arm101-palletizing](https://github.com/viam-devrel/so-arm101-palletizing) repository. `helpers.py` is provided for you; you build `palletizer.py` yourself as you work through the phases.

## Prerequisites

This is a self-serve workshop, so confirm each of the following before you start:

- **A Viam account with an online machine.** Log in at [app.viam.com](https://app.viam.com), [create a machine](https://docs.viam.com/set-up-a-machine/first-machine/), and confirm the green **Live** indicator before you begin.
- **Python 3.10 or newer.** Install it with [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or from [python.org](https://www.python.org/downloads/).
- **An SO-ARM101 that's built, has its motors configured, and is calibrated.** Follow the first-time arm setup steps in the [SO-ARM101 module](https://app.viam.com/module/devrel/so101-arm) documentation: install the LeRobot software, configure the motors, build the arm, and calibrate it.

### Validate your environment

Before starting Phase 1, confirm your environment is ready:

```sh
python3 --version          # 3.10 or newer
uv run --with viam-sdk python -c "import viam; print(viam.__version__)"   # prints a version
```

If either command fails, revisit the checklist above before continuing.
