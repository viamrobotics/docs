---
linkTitle: "Simulate a machine"
title: "Simulate a machine"
weight: 32
layout: "docs"
type: "docs"
no_list: true
description: "Run a simulated robot on Viam with MuJoCo on your own computer or Isaac Sim on a GPU, from scratch or from a machine you have."
capabilities: ["simulation", "section-index"]
diataxis: overview
date: "2026-11-24"
---

A simulated machine is a Viam machine whose arm, gripper, and cameras run in a physics simulator instead of on hardware.
You configure it on the **CONFIGURE** tab, watch it on the **CONTROL** and **3D SCENE** tabs, and program it with the same SDK code you'd run on a real robot.
When the real hardware arrives, you swap the simulated models for real ones and keep your code.

Viam supports two simulators.
**MuJoCo** runs free on your own Mac or Linux computer.
**Isaac Sim** renders realistic camera images and needs an NVIDIA RTX GPU, either your own or a Viam cloud GPU billed per minute.
To learn how a simulated machine works and how the two compare in detail, see [How simulation works](/simulate/how-simulation-works/).

## Before you start {#before-you-start}

Every simulation runs on a Viam machine.
Whether you need to set one up first depends on where the simulation runs:

- **Isaac Sim on a Viam cloud GPU:** no setup needed.
  Create a machine in the Viam app and choose **No hardware yet • Simulate it** in its setup wizard; Viam runs `viam-server` for the machine in the cloud.
- **MuJoCo, or Isaac Sim on your own GPU:** install `viam-server` on the computer that runs the simulation and get the machine online first.
  See [Set up your first machine](/set-up-a-machine/first-machine/).
- **A simulated copy of a machine you have:** you create the copy as part of [Simulate a machine you already have](/simulate/simulate-an-existing-machine/).

## Start a simulation {#start-a-simulation}

<!-- prettier-ignore -->
| If you want to | Start here |
| --- | --- |
| Learn Viam, or develop motion and pick-and-place code, on the computer you have | [Run a MuJoCo simulation on your computer](/simulate/mujoco/) |
| Train or test a vision model on realistic images, or simulate a robot you have as USD | [Run an Isaac Sim simulation](/simulate/isaac-sim/), on a Viam cloud GPU or your own RTX computer |
| Test code for a machine you already have on Viam, with real hardware or fake components | [Simulate a machine you already have](/simulate/simulate-an-existing-machine/) |
| Simulate a workcell that isn't on Viam yet | [Set it up on Viam](/set-up-a-machine/first-machine/) and then make a simulated copy, or start a new simulation and [use your own robot model](/simulate/build-a-scene/#use-your-own-robot-model) |

## Build out the scene {#build-out-the-scene}

Once a simulation runs, [Build a simulated scene](/simulate/build-a-scene/) covers making it match your cell, with steps for both simulators:

- [Place a component](/simulate/build-a-scene/#place-a-component) where it sits in your cell.
- [Add objects](/simulate/build-a-scene/#add-objects) to pick up or avoid, and [add and aim a camera](/simulate/build-a-scene/#add-and-aim-a-camera).
- [Use your own robot model](/simulate/build-a-scene/#use-your-own-robot-model) when the simulator doesn't include your robot.
- [Import a scene from Viam visualization](/simulate/build-a-scene/#import-a-scene-from-viam-visualization) (MuJoCo).
- [Move objects back to their starting poses](/simulate/build-a-scene/#move-objects-back-to-their-starting-poses) between test runs.

## Manage a cloud simulation {#manage-a-cloud-simulation}

A cloud Isaac Sim simulation bills per minute while it runs.
[Check its status, stop it, or restart it](/simulate/isaac-sim/#manage-a-cloud-simulation) from the Viam app, ask the [AI assistant](/hardware/ai-assistant/) on the machine's page, or use the [Viam MCP server's simulation tools](/reference/mcp/#simulation-tools).

## Move to real hardware {#move-to-real-hardware}

[Move a simulated machine to real hardware](/simulate/move-to-real-hardware/) when your code works in simulation: copy the config, swap each simulated model for a real one, replace the world with obstacles, measure frames, and point your code at the real machine.
