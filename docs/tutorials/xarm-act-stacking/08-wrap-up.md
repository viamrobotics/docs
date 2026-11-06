---
title: "Wrap-up and next steps"
linkTitle: "Wrap-up"
type: "docs"
slug: "wrap-up"
weight: 80
description: "Review what you built in the xArm6 robot learning workshop, the parts of the Viam platform you exercised, and where to take your policy next."
capabilities: ["teleop", "sequences", "ml-training", "ml-models", "docs"]
diataxis: tutorial
workshop: "xarm-act-stacking"
toc_hide: true
prev: "/tutorials/xarm-act-stacking/evaluate-and-iterate/"
languages: ["python"]
draft: true
---

Congratulations, you have finished the xArm6 robot learning workshop! Starting from a leader arm and a follower arm, you recorded your own demonstrations, trained a policy on them, and watched the xArm6 stack the red block on the blue one on its own.

## What you built

- **Milestone one.** You trained an ACT (Action Chunking with Transformers) model version from your own demonstrations, and it's now in the registry as `xarm-stacking`.
- **Milestone two.** You deployed that model on the machine, and the xArm6 stacked the red block on the blue one with no human input.

If you completed the optional Phase 7, you also measured success rates across two model versions, so you know whether your extra demonstrations helped.

## What you exercised on the platform

This workshop touched most of the moving parts of the Viam data and machine learning pipeline:

- **Configuration and modules:** a fragment that configures the whole cell, the Cartesian teleop service, the capture control sensor and webapp, and the `viam-labs:vla` module that runs the policy and controller services.
- **Frame system and motion:** Cartesian teleop across two arms with different kinematics, where the leader's tool pose becomes the follower's target and the motion service solves the joints.
- **Data:** capture on demand, sequences, sequence datasets, and tags.
- **Training:** custom training scripts on cloud GPUs, and model versions in the registry.
- **Deployment:** registry packages, and the generic service `DoCommand` pattern for starting and stopping a policy.

## Where to go next

Everything above is a foundation you can build on. A few directions:

- **Try language-conditioned policies.** [SmolVLA](https://github.com/viam-labs/smolvla-so101-training) trains a single policy for multiple tasks that you steer with a text instruction.
- **Try end-effector actions.** The `delta-ee` action space in [vla-inference-service](https://github.com/viam-labs/vla-inference-service) runs policies that output end-effector pose changes instead of joint angles.
- **Use the same pipeline on other robots.** Any arm with teleop and cameras records the same way.
- **Deploy to a fleet.** Add the `vla` module and your model package to the fragment you started from in Phase 2, and [roll the policy out to many machines](/fleet/reuse-configuration/).

When you are ready to build on your own hardware, the [Viam documentation](/) and the [module registry](https://app.viam.com/registry) are where to start.

{{< workshop-nav >}}
