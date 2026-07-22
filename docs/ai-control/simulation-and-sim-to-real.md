---
linkTitle: "Simulation and sim-to-real"
title: "Simulation and sim-to-real"
weight: 40
layout: "docs"
type: "docs"
description: "Understand why control policies are developed and validated in simulation before hardware, the sim-to-real gap a policy must bridge, and how a validated policy deploys to a machine as a Viam module."
---

Suppose you are training a locomotion policy for a quadruped. Early in training
the policy is bad on purpose: it explores, which means it commands motions that
would slam legs into the ground, tip the robot over, or drive joints past their
limits. Running those first attempts on real hardware would burn out motors and
damage the frame long before the policy learned to walk. You therefore train in
simulation first, where a fall costs nothing, and only bring a policy to
hardware once it can already trot in the simulated world.

This page explains why simulation is central to developing learned control
policies, the gap between simulated and real experience that a policy must
bridge, and how a policy validated in simulation then runs on a machine through
Viam.

## Why simulation comes first

A simulator is a model of the robot and its environment that runs the same
observe, decide, act loop the real machine will run, but in software. For
developing a control policy, this buys four things that hardware cannot offer at
the same time:

- **Safety.** Exploratory and half-trained policies produce dangerous motions.
  In simulation a catastrophic action ends an episode instead of breaking a
  motor or injuring a bystander.
- **Speed.** A physics simulator can run many times faster than real time and in
  hundreds of parallel instances. A policy that would take months of wall-clock
  time to train on one physical robot can train in hours across a fleet of
  simulated ones.
- **Cost.** Simulated robots do not wear out, and you can run thousands of them
  without buying thousands of machines.
- **Reset and reproducibility.** A simulator resets to an exact starting state on
  demand, so every training episode begins from a known condition and a failure
  is repeatable. Resetting real hardware to a precise pose after each attempt is
  slow and imprecise.

Simulation is also where you validate a policy before it touches hardware. You
can measure how the policy behaves across thousands of randomized situations,
check that it stays within joint and torque limits, and catch failure modes
while they are still free to fix. Common simulators for this work include
Gazebo, MuJoCo, and NVIDIA Isaac; Viam does not bundle a simulator, so you
choose the one that fits your robot and train in your own stack.

## The sim-to-real gap

A policy that performs well in simulation can still stumble on hardware, because
the simulated world and the physical world differ. The policy was trained on
simulated observations and its actions were interpreted by a simulated body; on
the real machine both sides of that loop change. This mismatch is the
sim-to-real gap, and it shows up in a few consistent places:

- **Observation gap.** Real sensors are noisier and less consistent than their
  simulated counterparts. A simulated camera renders a clean image; a real
  camera adds motion blur, exposure changes, and lens distortion. A simulated
  IMU reports near-perfect orientation; a real one drifts and jitters. If the
  policy trained only on clean observations, real readings fall outside the
  distribution it learned to handle.
- **Dynamics gap.** The simulator approximates mass, friction, joint backlash,
  motor response, and contact. Real values differ from the modeled ones and vary
  from unit to unit and over time as parts wear. An action that produced one
  motion in simulation can produce a slightly different motion on hardware.
- **Action and latency gap.** In simulation an action often takes effect
  instantly. On real hardware, sensing, inference, and communication each take
  time, so the machine acts on observations that are already slightly stale, and
  commands reach the actuators after a delay. A policy that assumed instant
  response can become unstable when that assumption breaks.

Analyzing where these gaps are largest for a given robot tells you what to
harden the policy against before deployment.

## Domain randomization

One widely used way to bridge the gap is domain randomization: rather than
training against one fixed set of simulator parameters, you vary them across
episodes. Friction coefficients, masses, sensor noise, lighting, textures, and
control latency each get sampled from a range during training. A policy exposed
to that variety learns behavior that holds across many different worlds, and the
real robot becomes just one more sample from the distribution it already handles.
The trade-off is that a policy trained to be robust to wide variation can be more
conservative than one tuned to a single ideal model, so the range is chosen to
cover reality without being needlessly pessimistic.

## From validated policy to running machine

Once a policy performs reliably in simulation across randomized conditions, the
artifact you carry to hardware is the trained model itself. Deployment on Viam
follows the same pattern as any learned controller: you package the model in a
[custom module](/build-modules/) that reads observations through component APIs,
runs the model to compute an action, and commands actuators through their APIs.
Because that module talks to hardware through the standard component APIs, the
same policy runs on any machine that exposes the required components.

The training environment and the deployment target stay cleanly separated: your
simulator and ML framework live in your own stack, and the Viam module is the
bridge that carries the validated result onto real hardware. For the details of
what a policy is and the real-time budget it must meet on the machine, see
[Learned and policy-based control](/ai-control/learned-and-policy-control/).

## An alternative: model-predictive control

Learning a policy in simulation is one way to control a hard-to-model system, but
it is not the only model-based approach. Model-predictive control (MPC) keeps an
explicit model of the system dynamics and, at each control step, uses that model
to predict how candidate action sequences would play out over a short future
horizon. It then executes the first action of the sequence that best achieves the
goal, and repeats the prediction at the next step with fresh observations.

Where a learned policy front-loads its cost into training and then runs a cheap
forward pass at runtime, MPC does its planning online: it needs a reliable
dynamics model and enough compute to solve an optimization every control cycle,
but it requires no training data and adapts its plan as conditions change. The
two approaches also combine well, for instance using a learned model of the
dynamics inside an MPC loop. MPC is a substantial topic in its own right and may
grow into its own page.

## Next steps

- Learn how a trained policy runs on a machine in
  [Learned and policy-based control](/ai-control/learned-and-policy-control/).
- Learn how to package and deploy code on a machine in
  [Build modules](/build-modules/).
