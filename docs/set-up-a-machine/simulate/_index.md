---
linkTitle: "Simulate a machine"
title: "Simulate a machine"
weight: 3
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
To learn how simulation works and how to choose between MuJoCo and Isaac Sim, see [How simulation works](/set-up-a-machine/simulate/how-simulation-works/).

## Start with a new machine

{{< cards >}}
{{% card link="/set-up-a-machine/simulate/mujoco/" noimage="true" customDescription="For an Apple Silicon Mac or a Linux computer. Free, and running in minutes." %}}
{{% card link="/set-up-a-machine/simulate/isaac-sim/" noimage="true" customDescription="For realistic cameras and Isaac Sim's robots, on a Viam cloud GPU or your own RTX machine." %}}
{{< /cards >}}

## Start from a machine you already have

{{< cards >}}
{{% card link="/set-up-a-machine/simulate/simulate-an-existing-machine/" noimage="true" customDescription="Make a simulated copy of a machine with real hardware, or give a machine built from fake components physics and cameras." %}}
{{< /cards >}}

If your workcell isn't on Viam yet, either [set it up on Viam](/set-up-a-machine/first-machine/) first and then make a simulated copy, or start with a new machine and [use your own robot model](/set-up-a-machine/simulate/build-a-scene/#use-your-own-robot-model).

## Once it runs

{{< cards >}}
{{% card link="/set-up-a-machine/simulate/build-a-scene/" noimage="true" customDescription="Place robots, objects, and cameras so the scene matches your cell." %}}
{{% card link="/set-up-a-machine/simulate/move-to-real-hardware/" noimage="true" customDescription="Swap simulated components for real ones and keep the code that works." %}}
{{< /cards >}}
