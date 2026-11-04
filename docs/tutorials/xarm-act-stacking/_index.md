---
title: "Teach an xArm6 to Stack Blocks"
linkTitle: "xArm6 Robot Learning Workshop"
type: "docs"
weight: 70
date: "2026-11-03"
description: "Teleoperate an xArm6 with an SO-ARM101 leader, record demonstrations, train an ACT policy in the cloud, and deploy it so the arm stacks blocks on its own."
capabilities:
  [
    "teleop",
    "data-capture",
    "sequences",
    "datasets",
    "ml-training",
    "ml-models",
    "hw-arm",
    "docs",
  ]
diataxis: overview
authors: []
level: "Intermediate"
languages: ["python"]
viamresources: ["arm", "gripper", "camera", "sensor", "data_manager", "motion"]
platformarea: ["ml", "data", "mobility"]
tags: ["tutorial", "workshop", "arm", "ml", "imitation-learning", "teleop"]
workshop: "xarm-act-stacking"
workshop_overview: true
time_estimate: "Full day"
hardware:
  - "uFactory xArm6 with gripper"
  - "SO-ARM101 leader arm with gripper"
  - "Intel RealSense wrist camera"
  - "USB webcam"
  - "Two blocks"
  - "x86 Linux computer"
companion_repo: "https://github.com/viam-devrel/xarm-act-stacking"
no_list: true
draft: true
---

You'll teach a robot arm a skill by showing it rather than programming it. You hand-guide an SO-ARM101 leader arm, the xArm6 follows, Viam records each demonstration, and a policy trained on those recordings stacks blocks on its own.

The hardware is mixed on purpose. The leader and follower have different kinematics, and the platform connects them through Cartesian teleop and the frame system.

<!-- ASSET hero-cell (PHOTO): xArm6 over the mat holding a block above another, SO-ARM101 leader beside it, both cameras visible -->

## This is a workshop

This is a multi-phase workshop, not a single page. Each phase ends with a checkpoint that confirms it worked before you move on, so finish the phases in order.

Milestone one is a trained model version (Phase 5). Milestone two is the arm stacking a block on its own (Phase 6). Phase 7 is optional, and it's where hackathon teams branch off.

## Required hardware

- **A uFactory xArm6 with its gripper**, the follower arm that does the stacking.
- **An SO-ARM101 leader arm with its gripper**, which you move by hand to demonstrate the task.
- **An Intel RealSense wrist camera**, mounted on the xArm6. The workshop uses it for color only.
- **A USB webcam**, fixed on a stand facing the mat.
- **Two blocks** in contrasting colors, sized for the xArm gripper.
- **A printable mat** from the companion repo, which marks where the blocks start.
- **An x86 Linux computer** that runs `viam-server` and inference. An NVIDIA GPU is recommended for inference.

## Phases

1. **[Platform mental model](/tutorials/xarm-act-stacking/platform-mental-model/)**
2. **[Configure the cell](/tutorials/xarm-act-stacking/configure-the-cell/)**
3. **[Record demonstrations](/tutorials/xarm-act-stacking/record-demonstrations/)**
4. **[Review and build a dataset](/tutorials/xarm-act-stacking/review-and-build-a-dataset/)**
5. **[Train a policy](/tutorials/xarm-act-stacking/train-a-policy/)** (milestone one: a trained model)
6. **[Deploy the policy](/tutorials/xarm-act-stacking/deploy-the-policy/)** (milestone two: an autonomous stack)
7. **[Evaluate and iterate](/tutorials/xarm-act-stacking/evaluate-and-iterate/)** (optional)

When you finish, the **[wrap-up](/tutorials/xarm-act-stacking/wrap-up/)** reviews what you built and points to next steps.

## Plan your day

| Phase                              | Time estimate                                  |
| ---------------------------------- | ---------------------------------------------- |
| 1. Platform mental model           | 20 minutes                                     |
| 2. Configure the cell              | 75 minutes                                     |
| 3. Record demonstrations           | 90 minutes                                     |
| 4. Review and build a dataset      | 30 minutes                                     |
| 5. Train a policy                  | 20 minutes plus a 60 to 90 minute training job |
| 6. Deploy the policy               | 60 minutes                                     |
| 7. Evaluate and iterate (optional) | 90 minutes plus a retrain                      |

The Phase 5 training job runs for 60 to 90 minutes, so submit it before lunch and use the wait for a break.

## Companion code

All supporting files for this workshop live in the [viam-devrel/xarm-act-stacking](https://github.com/viam-devrel/xarm-act-stacking) repository:

- `training/`: the ACT (Action Chunking with Transformers) training script, already published to the registry, so you don't write it.
- `config/`: the machine fragment and the policy and controller configuration.
- `printables/`: the mat.

## Prerequisites

This is a self-serve workshop, so confirm each of the following before you start:

- **A Viam account with an online machine.** Log in at [app.viam.com](https://app.viam.com), [create a machine](/set-up-a-machine/first-machine/), and confirm the green **Live** indicator before you begin.
- **`viam-server` v0.119.0 or later.**
  <!-- TODO(dep): recheck the minimum when the teleop module is extracted -->
- **`git` and `curl` on the machine.** The policy module needs both to install its dependencies in Phase 6.
- **An xArm6 that's networked and reachable from the machine.**
- **An SO-ARM101 leader that's built and calibrated.** Follow the setup steps in the [SO-ARM101 module](https://app.viam.com/module/devrel/so101-arm) documentation: configure the motors, build the arm, and calibrate it.
- **The Viam CLI, installed and logged in.** See the [Viam CLI documentation](/cli/).
- **Python 3 with pip**, to run the dataset script in Phase 4.
- **Optional: the [pick-and-place workshop](/tutorials/pick-and-place/)**, a gentler introduction to the xArm6.

### Where to start

- **Hardware ready and machine online (`viam-server` running):** start at [Phase 1](/tutorials/xarm-act-stacking/platform-mental-model/).
- **Still building your SO-ARM101 leader:** complete the [SO-ARM101 setup](https://app.viam.com/module/devrel/so101-arm) first, then return here for [Phase 1](/tutorials/xarm-act-stacking/platform-mental-model/).
