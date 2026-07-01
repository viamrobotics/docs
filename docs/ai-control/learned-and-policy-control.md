---
linkTitle: "Learned and policy-based control"
title: "Learned and policy-based control"
weight: 10
layout: "docs"
type: "docs"
description: "Understand when a trained control policy beats a hand-written PID or motion planner, how you package a policy as a module, and the real-time constraints it must meet on hardware."
---

Consider a quadruped that needs to trot across loose gravel, or a gripper that
has to pick up a crumpled cloth from a camera image. The dynamics are hard to
write down: contact with the ground is intermittent, the cloth deforms as you
touch it, and the "right" motor command depends on subtle features of what the
sensors currently see. A hand-tuned controller can struggle here, because there
is no clean equation from sensor reading to motor command that a person can
author directly.

A learned control policy takes a different route. Instead of encoding the rule
by hand, you train a function that maps observations to actions and let that
function drive the machine. This page explains what such a policy is, how it
relates to the built-in control tools Viam already provides, and what it takes
to run one on real hardware.

## What a control policy is

A control policy is a function. It reads an observation, the current state as
the machine perceives it (joint angles, an IMU reading, a camera frame, a goal),
and returns an action (target joint torques, wheel velocities, a gripper
command). At runtime the policy runs inside a loop: observe, decide, act, repeat,
usually at a fixed rate.

Two families of methods produce these policies:

- **Reinforcement learning (RL)** trains a policy by repeated trial against a
  reward signal, most often in simulation. The policy explores actions, and
  behavior that earns reward becomes more likely. RL suits problems where good
  behavior is easy to score but hard to demonstrate, such as a stable gait.
- **Imitation learning** trains a policy to reproduce demonstrations, for
  example teleoperated grasps recorded from an expert. It suits problems where
  you can show the desired behavior more easily than you can define a reward.

In both cases the output is the same kind of artifact: a trained model that
turns observations into actions.

## When a learned policy is warranted, and when it is not

Viam ships a mature classical control stack. The
[controls package](/reference/controls-package/) provides PID control for
regulating a single quantity toward a setpoint, and the motion service plans
collision-free paths for arms and mobile bases. These tools are predictable,
require no training data, and are the right default for most tasks.

A PID loop or a motion plan is the better choice when the task has a clear model:
holding a motor at a target speed, driving to a pose in a known map, or moving an
arm through free space. These controllers are cheap to configure, easy to reason
about, and behave consistently.

A learned policy earns its cost when the mapping from perception to action
resists hand authoring:

- **Rich, high-dimensional observations.** Policies that act directly on camera
  images (visuomotor control) can learn features that are impractical to
  hand-engineer.
- **Contact-rich or deformable dynamics.** Legged locomotion, in-hand
  manipulation, and grasping soft objects involve dynamics that are hard to
  model in closed form.
- **Behavior that is easier to demonstrate or reward than to specify.** If you
  can show the task or score it, but cannot write the rule, learning fills the
  gap.

The trade-off is real. A learned policy needs training data or a simulator,
compute to train, and careful validation, and it generalizes only as far as its
training distribution. When a classical controller already does the job, prefer
it.

## How a policy runs on Viam

Viam does not include a built-in reinforcement learning trainer. Training happens
in your own stack, typically a simulator plus an ML framework. What Viam provides
is the deployment and integration layer: a clean way to run your trained policy
against real hardware.

You deploy a policy as a [custom module](/build-modules/). The module loads your
trained model and runs its own control loop:

1. It reads observations through component APIs, for example camera frames from a
   camera, joint positions from an arm, or orientation from a movement sensor.
2. It runs the observation through the policy to compute an action.
3. It commands components through their APIs, for example setting motor power or
   arm joint positions.

Because the module talks to hardware through the same component APIs that the
rest of Viam uses, the policy is portable across machines that expose those
components, and it composes with everything else in the configuration: data
capture, other services, and remote control. Your training pipeline stays in
your own environment; the module is the bridge that carries the result onto the
machine.

## The real-time constraint

A control loop runs at a rate, for example 50 Hz for a walking gait, which gives
the policy a fixed budget per cycle, 20&nbsp;ms at 50 Hz. Everything in one iteration,
reading sensors, running inference, and sending commands, must fit inside that
budget. If it does not, the loop slows down or skips cycles, and a controller
that was stable in simulation can oscillate or fall over on hardware.

Inference latency, the time to run one forward pass of the model, is usually the
largest and most variable part of that budget. It depends on model size, the
compute available on the machine, and whether the model runs on CPU, GPU, or an
accelerator. Before you commit a policy to hardware, measure its worst-case
inference time on the target device and confirm it leaves room for sensor reads
and actuation within the loop period. See
[inference latency](/ai-control/inference-latency/) for how to reason about this
budget.

This constraint often shapes the policy itself. A smaller or quantized model that
meets the loop rate can control the machine better than a larger, more accurate
model that cannot keep up, because a control policy that misses its deadline is
not really controlling in real time.

## Next steps

- Learn how to package and deploy code on a machine in
  [Build modules](/build-modules/).
- Understand the timing budget in [inference latency](/ai-control/inference-latency/).
- Review the classical baseline in the
  [controls package](/reference/controls-package/) before reaching for a learned
  policy.
