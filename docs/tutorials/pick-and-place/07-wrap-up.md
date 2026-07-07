---
title: "Wrap-up and next steps"
linkTitle: "Wrap-up"
type: "docs"
slug: "wrap-up"
weight: 70
description: "Review what you built in the pick-and-place workshop, the parts of the Viam platform you exercised, and where to take your solution next."
workshop: "pick-and-place"
toc_hide: true
prev: "/tutorials/pick-and-place/inline-module/"
languages: ["python"]
---

You have finished the pick-and-place workshop. Starting from an empty machine, you configured every resource by hand and wrote the code that drives a vision-guided robot to detect a block, plan around obstacles, and place it in a bin.

## What you built

A robot that finds blocks by shape and places each one into a bin, reached in two milestones:

- **Milestone one (Phase 4).** You drove the arm through a fixed pick-and-place sequence from your own Python script, proving your connection, resources, and saved poses all hold up under real code.
- **Milestone two (Phase 5).** You closed the loop with live perception: the vision service detects a block, the frame system transforms its position into world coordinates, and the motion service plans a collision-free pick, all from a pose your code computes each cycle.

If you completed the optional Phase 6, you also packaged that same loop as a module that runs on the robot itself, with no laptop attached.

## What you exercised on the platform

This workshop was small on purpose, but it touched most of the moving parts you will use on any Viam machine:

- **Configuration and runtime:** the Viam app as the single source of truth (the CONFIGURE tab and its JSON view), `viam-server` running your resources while `viam-agent` keeps it alive, and the module system, including a discovery service that configured the camera for you.
- **Resources:** components for the arm, gripper, depth camera, and pose-saving switches; obstacles configured as components so the planner sees the table and safety walls; and services for capability, a two-stage vision pipeline (a shape detector feeding a 3D segmenter) and the builtin motion service.
- **Motion and perception:** the frame system and `transform_pose` turning a wrist-camera detection into a world-frame pose, collision-aware planning against your configured obstacles, and the wrist-camera rule of detecting from a known pose.
- **Code:** the Python SDK (`RobotClient`, typed component and service clients, and `motion.move`), plus, if you did Phase 6, reaching the machine-management API from inside a module.

## Where to go next

Everything above is a foundation you can build on. A few directions, each with a starting point in the docs:

- **Extend the pick logic.** Sort blocks by color or shape into separate bins, add more saved poses, or force a straight-line descent with a [motion constraint](/motion-planning/move-an-arm/move-with-constraints/).
- **Train your own detector.** Replace the shape-finder with a custom ML model: [capture and sync images](/data/capture-sync/), [build a dataset and train a model](/train/train-a-model/), then deploy it through the [ML model vision service](/reference/services/vision/mlmodel/).
- **Build an interface.** Put a browser UI in front of the robot with a [Viam application](/build-apps/): stream the camera and trigger a pick from a dashboard instead of a script.
- **Operationalize it.** Reuse this configuration across machines with a [fragment](/hardware/fragments/) and [capture data](/data/capture-sync/) from every run.
- **Run the module unattended.** The optional Phase 6 module runs one cycle per `do_command`. Drive that on a cadence so the robot picks on its own: an internal loop that calls `run_pick_cycle` between sleeps, or a [trigger](/reference/triggers/) that sends `do_command` on a schedule.
- **Explore the rest of the platform.** The same patterns work from other [SDKs](/reference/sdks/) (Go, TypeScript, C++, Flutter) and across the full [component and service APIs](/reference/apis/).

When you are ready to build on your own hardware, the [Viam documentation](/) and the [module registry](https://app.viam.com/registry) are where to start.

{{< workshop-nav >}}
