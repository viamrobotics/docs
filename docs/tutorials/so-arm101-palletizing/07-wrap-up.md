---
title: "Wrap-up and next steps"
linkTitle: "Wrap-up"
type: "docs"
slug: "wrap-up"
weight: 70
description: "Review what you built in the SO-ARM101 palletizing workshop, the parts of the Viam platform you exercised, and where to take your solution next."
workshop: "so-arm101-palletizing"
toc_hide: true
prev: "/tutorials/so-arm101-palletizing/inline-module/"
languages: ["python"]
draft: true
---

Congratulations, you have finished the SO-ARM101 palletizing workshop! Starting from an empty machine, you configured a real desktop arm, taught it the cell by hand, and wrote the code that packs cubes onto a pallet.

## What you built

- **Milestone one.** You drove the arm through a static bottom-layer pack from your own Python script, proving your connection, your configured resources, and the poses you taught by hand all hold up under real code.
- **Milestone two.** You closed the loop with obstacle avoidance: the motion service plans a collision-free path around the cubes already on the pallet and the cube in the gripper, so the second layer stacks cleanly on top of the first.

If you completed the optional Phase 6, you also packaged that same pack loop as a module that runs on the machine itself.

## What you exercised on the platform

This workshop was small on purpose, but it touched most of the moving parts you will use on any Viam machine:

- **Configuration and runtime:** the Viam app as the single source of truth (the CONFIGURE tab and its JSON view), `viam-server` running your resources while `viam-agent` keeps it alive, and the module system, including a discovery service that suggested the arm and gripper configuration for you.
- **Resources:** the arm and gripper components from the SO-ARM101 module, with the gripper attached to the arm through the frame system, plus the calibration sensor that made the arm's joint positions accurate.
- **Frame system and motion:** placing the arm at the world origin so hand-taught poses are world poses, teaching real-world anchor poses by back-driving the arm with torque disabled, and letting the motion service plan to the arm's end point. You also learned how a five degree-of-freedom (5-DOF) arm plans to a position without pinning orientation, and how a WorldState of placed and held cubes keeps the planner from routing through the stack.
- **Code:** the Python SDK (`RobotClient`, the typed `Gripper` and `MotionClient`, and `motion.move`), built up one method at a time into `palletizer.py`, plus packaging that same script as an inline module.

## Where to go next

Everything above is a foundation you can build on. A few directions, each with a starting point in the docs:

- **Extend the pack.** Add more layers, change the grid pattern, or force a straight-line descent into each cell with a [motion constraint](/motion-planning/move-an-arm/move-with-constraints/).
- **Add perception.** Replace the fixed staging spot with a camera that finds cubes: [capture and sync images](/data/capture-sync/), [build a dataset and train a model](/train/train-a-model/), then deploy it through the [ML model vision service](/reference/services/vision/mlmodel/) so the arm picks whatever it sees.
- **Build an interface.** Put a browser UI in front of the cell with a [Viam application](/build-apps/): start a pack and watch progress from a dashboard instead of a terminal.
- **Operationalize it.** Reuse this configuration across machines with a [fragment](/hardware/fragments/) and [capture data](/data/capture-sync/) from every run.
- **Run the module unattended.** The optional Phase 6 module runs a pack on demand through `do_command`. Drive it on a cadence with a [trigger](/reference/triggers/) so the cell packs on its own.
- **Explore the rest of the platform.** The same patterns work from other [SDKs](/reference/sdks/) (Go, TypeScript, C++, Flutter) and across the full [component and service APIs](/reference/apis/).

When you are ready to build on your own hardware, the [Viam documentation](/) and the [module registry](https://app.viam.com/registry) are where to start.

{{< workshop-nav >}}
