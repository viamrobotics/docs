---
linkTitle: "AI & learned control"
title: "AI and learned control"
weight: 45
layout: "docs"
type: "docs"
no_list: true
description: "Run learned policies, vision-language-action models, and LLM-driven task planning on a machine using modules and the Viam APIs."
---

Classic robot control is written by hand: a PID loop, a motion planner, a
state machine. A growing class of applications instead runs a **learned
model** in the loop, a reinforcement-learning policy, a vision-language-action
(VLA) model, or a large language model that decomposes a goal into skills.

On Viam these run the same way any custom capability does: you package the
model in a [module](/build-modules/) that implements a component or service
API, and your application talks to it through the standard APIs. This section
explains how each kind of model fits that pattern.

- [Inference latency and loop rate](inference-latency/): why a model in the
  loop cannot run faster than its own inference time, and how to size it.
- [Learned and policy-based control](learned-and-policy-control/): when a
  trained policy beats a hand-written controller, and how it runs on a machine.
- [Run a vision-language-action model](run-a-vla/): drive a robot from a camera
  frame plus a language prompt.
- [Integrate an LLM with a robot](integrate-an-llm/): use a language model to
  plan tasks and dispatch robot skills, safely.
- [Simulation and sim-to-real](simulation-and-sim-to-real/): develop and
  validate a policy before it touches hardware.
