---
title: "Phase 1: Platform mental model"
linkTitle: "1. Platform mental model"
type: "docs"
slug: "platform-mental-model"
weight: 10
description: "How demonstration-based robot learning maps onto Viam, and what the policy sees and does."
workshop: "xarm-act-stacking"
toc_hide: true
phase: 1
phase_total: 7
time_estimate: "20 minutes"
prev: "/tutorials/xarm-act-stacking/"
next: "/tutorials/xarm-act-stacking/configure-the-cell/"
languages: ["python"]
capabilities: ["teleop", "sequences", "ml-training", "ml-models", "docs"]
diataxis: tutorial
draft: true
---

This phase gives you the mental model for the whole workshop before you touch any hardware. You learn how teaching by demonstration works, which Viam piece handles each stage, and what the policy sees and does. Every later phase builds one stage of that loop, so it comes first.

## Programming by demonstration

Instead of writing code that says how to stack a block, you show the robot. This is imitation learning. You record what a person does, and a model learns to map observations (camera images plus joint state) to actions (the next joint positions).

This workshop uses ACT, which stands for Action Chunking with Transformers. ACT predicts a chunk of future actions at once instead of one action at a time. That is why it handles smooth, precise motion well with about 50 demonstrations.

## The loop on Viam

Each stage of the loop maps to a Viam piece and to the phase where you build it:

1. **Teleop:** the Cartesian teleop service lets you steer the xArm6 with a leader arm (Phase 2).
2. **Record:** the capture control sensor and the capture-control webapp record each demonstration as one [data sequence](/data/sequences/), using [capture on demand](/data/capture-sync/capture-on-demand/) (Phase 3).
3. **Curate:** you review the episodes and build a sequence dataset from the keepers (Phase 4).
4. **Train:** a [custom training job](/train/custom-training-scripts/) trains the policy on a cloud GPU (Phase 5).
5. **Deploy:** the `viam-labs:vla` policy and controller services run the trained model on the machine (Phase 6).

<!-- ASSET diagram-loop (DIAGRAM): five stages left to right, with Viam resource names under each -->

## Two arms, one policy

The leader arm is 5-DOF (degrees of freedom) and the xArm6 is 6-DOF, so copying joint angles from one to the other doesn't work. Cartesian teleop maps the leader's tool pose into the follower's frame, and the motion service solves the xArm's joints.

The policy only ever sees the follower's joints and cameras. The leader is just a way to steer the arm. You could swap in a gamepad or a different leader without retraining.

## What the policy sees and does

|             | Contents                                                                                                              |
| ----------- | --------------------------------------------------------------------------------------------------------------------- |
| Observation | `wrist-cam` and `scene-cam` images, six xArm joint angles, and the gripper opening normalized to 0 = open, 1 = closed |
| Action      | The next six joint angles plus the gripper value                                                                      |

Both run at 10 Hz.

{{< checkpoint >}}
Open your machine in the Viam app. The machine shows the green **Live** indicator. You can name the five stages of the loop and the arm whose joints the policy learns. If the machine isn't Live, start `viam-server` before continuing.
{{< /checkpoint >}}

{{< workshop-nav >}}
