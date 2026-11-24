---
title: "How simulation works"
linkTitle: "How simulation works"
weight: 10
type: "docs"
layout: "docs"
description: "How a simulator module stands in for hardware on a Viam machine, and how MuJoCo and Isaac Sim differ."
capabilities: ["simulation", "motion-planning", "viam-server"]
diataxis: explanation
date: "2026-11-24"
---

A simulated Viam machine is an ordinary machine whose hardware layer is replaced by a simulator module.
`viam-server`, the machine's config, its services, and your code are the same ones a real machine uses.
Only the components change: instead of a driver module talking to a physical arm or camera, a simulator module answers the same API calls from a physics simulation.

That one substitution explains most of what you see.
The motion planner, the 3D scene, and the SDKs work unchanged because they only talk to component APIs.
Driver modules for physical devices don't work, because there's no device for them to reach.
This page explains how the pieces fit together, where the simulation can run, and how to choose between the two simulators Viam supports: MuJoCo and Isaac Sim.

## A world component owns the scene {#a-world-component-owns-the-scene}

Each simulator module provides a `world` model and a set of component models: arms, grippers, cameras, bases, and others.
A machine has exactly one `world`.
It owns the simulated scene, including the floor, the objects in it, and the loop that steps the physics forward.
Every other simulation component names the world in its `world` attribute.
That dependency makes `viam-server` start the world before anything that uses it.

All of a module's components run in one module process and share that one simulation.
When your code calls `MoveToJointPositions` on a simulated arm, `viam-server` passes the call to the module, the module drives the arm's joints in the simulation, and the world's step loop moves it.
A simulated camera renders the same scene from its own viewpoint.

```text
  Your code (SDK)        Viam app (CONTROL, 3D SCENE)
         │                        │
         └──── component APIs ────┘
                     │
  ┌──────────────── viam-server ────────────────┐
  │  motion service   frame system   data mgr   │
  │                     │                       │
  │  ┌──────────── simulator module ─────────┐  │
  │  │  arm ─────┐                           │  │
  │  │  gripper ─┼──►  world: scene,         │  │
  │  │  camera ──┘     objects, step loop    │  │
  │  │                 (MuJoCo or Isaac Sim) │  │
  │  └───────────────────────────────────────┘  │
  └─────────────────────────────────────────────┘
```

Components are placed in the scene by their standard Viam frame, the same `frame` block a real component has, with its translation in millimeters.
Placing them this way keeps Viam's view of the machine consistent with the simulation: the frame system, the motion planner, and the **3D SCENE** tab all read the same frames that put the robot in the scene.
For each model's attributes and the commands the world accepts, see the [MuJoCo module README](https://github.com/viam-labs/viam-mujoco-sim#readme) and the [Isaac Sim module README](https://github.com/viam-modules/viam-isaac-sim#readme).

## Where the simulation runs {#where-the-simulation-runs}

A simulation runs wherever `viam-server` runs, because the simulator module runs inside the machine like any other module.
There are two places that can be.

**Your own computer.**
You install `viam-server` on your computer, set it up as a machine, and add the simulator module to its config.
MuJoCo runs this way on a Mac or a Linux computer.
Isaac Sim runs this way on an Ubuntu computer with an NVIDIA RTX GPU, where the module installs Isaac Sim the first time it runs.
Nothing extra is billed.

**A Viam cloud container.**
For Isaac Sim, Viam can start a container with an NVIDIA GPU that runs `viam-server` as one of your machine's parts.
The container has Isaac Sim already installed, and `viam-server` in it reads the part's saved config from the Viam app, as it does on any computer.
You configure, control, and connect to the part as if it were on your desk.
A cloud simulation is billed per minute while it runs, after any monthly cloud credit your organization has is used, and it stops after at most 60 minutes in which the machine doesn't actuate.
If you don't see the simulate option, simulation isn't turned on for your organization yet.
Starting, stopping, and billing are covered in [Run an Isaac Sim simulation](/set-up-a-machine/simulate/isaac-sim/).

## What works the same as on real hardware {#what-works-the-same-as-on-real-hardware}

Anything that works through component APIs and the frame system works on a simulated machine:

- **The motion service** plans for a simulated arm as it does for a real one.
  Each simulated arm serves kinematics for its robot model, so the planner computes inverse kinematics and avoids collisions itself rather than handing that to the simulator.
- **The frame system and the 3D SCENE tab** show components where their frames put them.
- **The SDKs** connect to a simulated machine with its address and credentials, like any other machine.
- **Data capture** records from simulated cameras like real ones.
- **Vision services** run on simulated camera images.

What doesn't work is any module that drives a physical device, such as a specific camera, motor, or sensor.
Those modules expect hardware that isn't there.
In a simulation, the simulator module's models take their place.

Simulated sensors are also cleaner than real ones.
For example, MuJoCo's depth images have no noise or holes, and every ray of a simulated LIDAR scan samples the same instant.
Code that works in simulation can still need tuning for real sensor noise.

## MuJoCo versus Isaac Sim {#mujoco-versus-isaac-sim}

Both simulators expose the same Viam APIs, so the code you write doesn't depend on which one you choose.
They differ in what they're built for and what they need to run.

**MuJoCo** is a physics simulator that runs on the CPU.
Its module is a few tens of megabytes, and it runs on a Mac as well as on Linux, so you can simulate on the laptop you already have at no cost.
Cameras render with OpenGL and serve color and depth images.
The module bundles a UFactory Lite6 and a Universal Robots UR5e arm, several grippers, mobile bases, LIDARs and other sensors, and conveyor and scale parts for workcells.
Your own robot loads from an MJCF or URDF file.
When you change the config, the module rebuilds the affected components right away: an edited arm returns to its home pose, and editing the world rebuilds everything that depends on it.
Choose MuJoCo to learn Viam, to develop motion and pick-and-place code, and to iterate quickly on a scene.

**Isaac Sim** is NVIDIA's simulator, with RTX rendering for realistic camera images.
It needs an NVIDIA RTX GPU on Ubuntu, either your own or a Viam cloud container.
The Isaac Sim download is over 10 GB, and the world's first start takes minutes while Isaac Sim boots and builds its caches.
The module knows several Universal Robots arms, a Franka arm, and a Jetbot base, and loads any other robot from a USD file.
Cameras serve color images.
Isaac Sim can't be restarted inside a running module, so changes to the world's config or to where a component spawns take effect only after the module restarts.
Choose Isaac Sim when your project depends on realistic images, such as training or testing a vision model, or when you need a robot that's available as USD.

## How simulated and real configs map {#how-simulated-and-real-configs-map}

A simulated machine and its real counterpart share everything your code depends on:

- **Resource names**, such as `arm-1` or `wrist-cam`.
- **APIs**: a simulated arm is an `arm` and a simulated camera is a `camera`.
- **Services**, such as the motion service and vision services, and their config.
- **Frames**: where each component sits relative to the others.

They differ only in the parts that make the simulation run:

- **Component models**: `viam-labs:mujoco-sim:arm` in simulation, the arm vendor's model on real hardware.
- **The module** that provides those models.
- **The world component** and the objects in its scene.

Because your code addresses components by name and API, moving between simulation and hardware is a config change, not a code change: swap each model, add or remove the world, and keep the names and frames.
Your code then connects to the other machine by changing only its address and credentials.
Objects that exist only in the simulated scene don't carry over, so anything the motion planner must avoid on the real machine needs to be configured as an obstacle there.

## What's next {#whats-next}

- [Run a MuJoCo simulation on your computer](/set-up-a-machine/simulate/mujoco/): start a free simulation on your Mac or Linux computer.
- [Run an Isaac Sim simulation](/set-up-a-machine/simulate/isaac-sim/): start a simulation with realistic rendering on a Viam cloud GPU or your own.
- [Simulate a machine you already have](/set-up-a-machine/simulate/simulate-an-existing-machine/): make a simulated copy of an existing machine that keeps its names and frames.
- [Move a simulated machine to real hardware](/set-up-a-machine/simulate/move-to-real-hardware/): run the code you wrote in simulation on your real robot.
