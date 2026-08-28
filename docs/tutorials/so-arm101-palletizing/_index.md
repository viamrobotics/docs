---
title: "Miniature Palletizing with the SO-ARM101"
linkTitle: "SO-ARM101 Palletizing Workshop"
type: "docs"
weight: 60
description: "Build a desktop palletizing robot with an affordable SO-ARM101 arm. Teach its poses by hand, then program a collision-free pick-and-stack in Python."
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
  - "Eight ~20 mm cubes"
  - "Personal computer"
companion_repo: "https://github.com/viam-devrel/mini-palletizer"
no_list: true
---

Warehouse robots spend all day stacking boxes onto pallets. In this workshop you build the same thing in miniature, on your desk: an affordable SO-ARM101 arm that picks up cubes and stacks them neatly, two layers at a time.

It is a hands-on introduction to robot manipulation with Viam, for developers and makers who would rather program a real arm than a simulator. You do not need industrial hardware or prior robotics experience, just a desktop arm you can build yourself. You configure it, teach it where the cubes and the pallet are by guiding it with your own hands, then write the Python that runs the whole packing routine. By the end, the arm packs a full two-by-two-by-two stack of cubes on its own, driven entirely by code you wrote.

<!-- ASSET hero-cell-overview (PHOTO): staged SO-ARM101 + cubes + pallet grid + staging spot -->

## Required hardware

- **An SO-ARM101 arm** with its finger gripper, connected to your computer over USB.
- **Eight cubes and a pallet mat.** You need eight cubes about 20 mm on a side, a two-by-two pallet grid to stack them on, and a staging spot to feed cubes from. The companion project includes a printable template: paper cube nets you fold into 20 mm cubes, and a mat that marks the pallet grid and the staging spot at the exact spacing the code expects. Print it, cut it out, and you are ready. Wooden or foam 20 mm cubes work too if you have them.
- **A personal computer** running `viam-server`, with the arm plugged into it over USB.

## Phases

1. **[Platform mental model](/tutorials/so-arm101-palletizing/platform-mental-model/)**
2. **[Configure the SO-ARM101](/tutorials/so-arm101-palletizing/configure-the-arm/)**
3. **[Teach the cell by hand](/tutorials/so-arm101-palletizing/teach-the-cell/)**
4. **[Pack from Python](/tutorials/so-arm101-palletizing/pack-from-python/)** (milestone one: a static pack from your own code)
5. **[Avoid placed cubes](/tutorials/so-arm101-palletizing/avoid-placed-cubes/)** (milestone two: a collision-free full pack)
6. **[Wrap it in a module](/tutorials/so-arm101-palletizing/inline-module/)** (optional)

When you finish, the **[wrap-up](/tutorials/so-arm101-palletizing/wrap-up/)** reviews what you built and points to next steps.

## Companion code

All supporting files for this workshop live in the [viam-devrel/mini-palletizer](https://github.com/viam-devrel/mini-palletizer) repository, including the printable cube-and-pallet template. `helpers.py` is provided for you; you build `palletizer.py` yourself as you work through the phases.

## Prerequisites

This is a self-serve workshop, so confirm each of the following before you start:

- **A Viam account with an online machine.** Log in at [app.viam.com](https://app.viam.com), [create a machine](https://docs.viam.com/set-up-a-machine/first-machine/), and confirm the green **Live** indicator before you begin.
- **Python 3.10 or newer.** Install it with [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or from [python.org](https://www.python.org/downloads/).
- **An SO-ARM101 that's built, has its motors configured, and is calibrated.** Follow the first-time arm setup steps in the [SO-ARM101 module](https://app.viam.com/module/devrel/so101-arm) documentation: configure the motors, build the arm, and calibrate it.

### Validate your environment

Before starting Phase 1, confirm your environment is ready:

```sh
python3 --version          # 3.10 or newer
uv run --with viam-sdk python -c "import viam; print(viam.__version__)"   # prints a version
```

If either command fails, revisit the checklist above before continuing.

### Where to start

<!-- ASSET P1 live-indicator (UI+): machine page with the green Live indicator boxed -->

- **Arm built and machine online (`viam-server` running):** start at [Phase 1](/tutorials/so-arm101-palletizing/platform-mental-model/).
- **Still building your SO-ARM101:** complete the [first-time arm setup](https://app.viam.com/module/devrel/so101-arm) (configure the motors, build the arm, and calibrate it), then return here for [Phase 1](/tutorials/so-arm101-palletizing/platform-mental-model/).
