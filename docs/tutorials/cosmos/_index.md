---
title: "Train NVIDIA Cosmos 3 in Viam Sim"
linkTitle: "NVIDIA Cosmos 3 workshop"
type: "docs"
weight: 40
date: "2026-10-29"
description: "Use Viam's agentic flows and Isaac Sim to customize a workcell, generate training data, train a Cosmos 3 Edge policy, and deploy it in simulation."
capabilities: ["ml-training", "ml-models", "datasets", "docs"]
diataxis: overview
authors: []
level: "Intermediate"
languages: ["python"]
viamresources: ["arm", "gripper", "camera", "mlmodel", "generic"]
platformarea: ["ml"]
tags: ["tutorial", "workshop", "simulation", "machine learning"]
workshop: "cosmos"
workshop_overview: true
companion_repo: "https://github.com/viam-labs/cosmos-tutorial"
no_list: true
draft: false
---

In this workshop you’ll use our agentic flows and simulator to design a robot workcell, design a task for it, and then create a motion policy for it based on NVIDIA Cosmos 3 Edge, a 4B parameter world action model sized for edge deployment. You won’t need access to any physical robotics hardware, and the entire process is supported by agent skills and our native model training flow.

You’ll use your coding harness and our agentic flows to: connect to Viam, use the built-in NVIDIA Isaac Sim open simulation framework, and collect training data. You can use cutting-edge coding models, including frontier visual and spatial intelligence models like GPT-6 Astra, to automate the detailed work of training data design and workcell layout.

We encourage people to try this workshop even if robotics or vision model training seem daunting. With Viam as the harness for physical AI, if you can control an agent, you can train a robot.

## About the tools

NVIDIA Cosmos 3 Edge is a world action model. A world action model comprises a pre-trained vision model that can understand and predict physical motion, and an action model that can produce joint sequences to control robotics hardware. Because they come pretrained with an understanding of spatial relationships, new task-specific policies can be post-trained on a small set of demonstration episodes. Learn more here.

Viam is an agentic platform for developing and operating robots. It provides developers and agents with the entire lifecycle of creating and training a robot, from design to deployment to data.

## What you’ll accomplish

By the end of this workshop, you will have:

- Designed a workcell in Isaac Sim
- Designed a simulated task for it to perform
- Run through randomized task episodes to collect a training set with videos and robot poses
- Trained a motion policy
- Deployed the policy back to the simulator and run it to execute your trained motion

You’ll use the Viam agentic skills and simulation environments throughout; you can use these at a very high level, giving the agent large steps and only inspecting the videos, or you can dive deeper, designing the robot action yourself and executing or editing the scripts.

If you’re new to these concepts, you’ll come away from this workshop understanding how to collect training data for a robot policy, how to deploy it, and how to apply the visual reasoning capabilities of frontier LLMs like Astra and Fable.

Our agent tools will guide you at each step, and if you get stuck, you can use the [fast path with a premade policy](/tutorials/cosmos/deploy-the-policy/#fast-path-existing-trained-policy).

## Who is this for

You should be comfortable working in an agentic coding harness and running python commands in the terminal, but you don’t need a physical robot or prior ML experience.

The scripts were developed for MacOS and Ubuntu Linux; Windows through WSL may work as well, but has not been tested.

## Phases

1. **[Set up your environment](/tutorials/cosmos/setting-up-your-environment/)**
2. **[Design your robot and tasks](/tutorials/cosmos/design-your-robot-and-tasks/)**
3. **[Create training episodes](/tutorials/cosmos/create-training-episodes/)**
4. **[Train your policy](/tutorials/cosmos/train-your-policy/)**
5. **[Deploy the policy to your robot](/tutorials/cosmos/deploy-the-policy/)**

When you finish, the **[wrap-up](/tutorials/cosmos/next-steps/)** describes the path from simulation to a live robot.
