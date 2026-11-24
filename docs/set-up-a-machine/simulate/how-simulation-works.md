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
Only the components change: instead of a driver talking to a physical arm or camera, the simulator answers the same API calls from a physics simulation.

The motion planner, the 3D scene, and the SDKs work unchanged because they only talk to component APIs.
This page explains how the pieces fit together, how you see a simulation, where it can run, and how to choose between the two simulators Viam supports: MuJoCo and Isaac Sim.

## A world component owns the scene {#a-world-component-owns-the-scene}

Each simulator module provides a `world` model and a set of component models: arms, grippers, cameras, bases, and others.
A machine has exactly one `world`.
It owns the simulated scene, including the floor, the objects in it, and the loop that steps the physics forward.
Every other simulated component names the world in its `world` attribute.
That dependency makes `viam-server` start the world before anything that uses it.

The simulator module runs all of these components in one process, and they share one simulation.
When your code calls `MoveToJointPositions` on a simulated arm, `viam-server` forwards the call to the simulator, which sets the arm's joint targets, and the world's step loop moves the joints toward them.

Components are placed in the scene by their standard Viam frame, the same `frame` block a real component has, with its translation in millimeters.
Placing them this way keeps Viam's view of the machine consistent with the simulation: the frame system, the motion planner, and the **3D SCENE** tab all read the same frames that put the robot in the scene.
For each model's attributes and the commands the world accepts, see the [MuJoCo module README](https://github.com/viam-labs/viam-mujoco-sim#readme) and the [Isaac Sim module README](https://github.com/viam-modules/viam-isaac-sim#readme).

## How you see a simulation {#how-you-see-a-simulation}

You watch a simulated machine in the Viam app in two ways, and they show different things.

- **The 3D SCENE tab** draws Viam's own model of the machine: each component's frame and geometry, the arm in its current joint positions, and the obstacles you configure.
  This is what the motion planner sees.
  The simulator doesn't render it, so it has no textures or lighting, and it shows the loose objects in the scene only if the machine has the simulator's world state service.
  Use it to check where components are and to watch the arm move.
- **A camera component** renders the simulated scene itself from its own viewpoint, as a real camera would: every object, with the simulator's materials and lighting.
  A camera is the only way to see in the Viam app what the simulator sees, and it's what vision services and data capture read from.
  A simulation runs without one, but the getting-started pages add one so you can watch the cell on the **CONTROL** tab.

On your own GPU, Isaac Sim can also stream its full viewport to your laptop.
See [View the Isaac Sim viewport](/set-up-a-machine/simulate/isaac-sim/#advanced-view-the-isaac-sim-viewport).

## Where the simulation runs {#where-the-simulation-runs}

A simulation runs wherever `viam-server` runs, because the simulator module runs inside the machine like any other module.
There are two places that can be.

**Your own computer.**
You install `viam-server` on your computer, set it up as a machine, and add the simulator module to its config.
MuJoCo runs this way on a Mac or a Linux computer.
Isaac Sim runs this way on an Ubuntu computer with an NVIDIA RTX GPU, where the module installs Isaac Sim the first time it runs.
Nothing extra is billed.

**A Viam cloud container.**
For Isaac Sim, Viam can start a container with an NVIDIA GPU that runs as one of your machine's parts.
The container already has Isaac Sim and `viam-server` installed, and reads the part's saved config from the Viam app, as `viam-server` does on any computer.
You configure, control, and connect to the part as if it were on your desk.
A cloud simulation is billed per minute while it runs, after any monthly cloud credit your organization has is used, and it stops after 60 minutes in which the machine doesn't actuate.
Starting, stopping, and billing are covered in [Run an Isaac Sim simulation](/set-up-a-machine/simulate/isaac-sim/).

## What works the same as on real hardware {#what-works-the-same-as-on-real-hardware}

Anything that works through component APIs and the frame system works on a simulated machine:

- **The motion service** plans for a simulated arm as it does for a real one.
  Each simulated arm serves kinematics for its robot model, so the planner computes inverse kinematics and avoids collisions itself rather than handing that to the simulator.
- **The frame system and the 3D SCENE tab** show components where their frames put them.
- **The SDKs** connect to a simulated machine with its address and credentials, like any other machine.
- **Data capture** records from simulated cameras like real ones.
- **Vision services** run on simulated camera images.
- **Resource names, services, and frames** stay the same, so the code and service config that work on one machine work on the other.

## What's different from real hardware {#whats-different-from-real-hardware}

**Component models and the module that provides them.**
A driver module for a physical device expects hardware that isn't there, so a simulated machine uses the simulator's models instead.
For example, a real UFactory Lite6 arm uses the `viam:ufactory:lite6` model from the `viam:ufactory` module, with a `host` attribute set to the arm's IP address.
In MuJoCo, the same arm is a `viam-labs:mujoco-sim:arm` with `asset` set to `lite6` and `world` set to the world component's name.
Both are `arm` components, and your code calls them the same way.

**The world and its objects.**
Only a simulated machine has a world component.
Objects that exist only in the simulated scene don't carry over to real hardware, so anything the motion planner must avoid on the real machine needs to be configured as an obstacle there.

Because your code addresses components by name and API, moving between simulation and hardware is a config change, not a code change: swap each model, add or remove the world, and keep the names and frames.
Your code then connects to the other machine by changing only its address and credentials.

**Sensor data is cleaner.**
For example, MuJoCo's depth images have no noise or holes, and every ray of a simulated LIDAR scan samples the same instant.
Code that works in simulation can still need tuning for real sensor noise.

## MuJoCo versus Isaac Sim {#mujoco-versus-isaac-sim}

Both simulators implement the standard Viam component APIs.
A simulated arm answers `MoveToJointPositions` and `GetJointPositions`, and a simulated camera answers `GetImages`, whichever simulator runs them, so the code you write doesn't depend on which one you choose.
They differ in what they're built for and what they need to run.

<!-- prettier-ignore -->
| | MuJoCo | Isaac Sim |
| --- | --- | --- |
| **What it is** | [MuJoCo](https://mujoco.org/), a physics simulator that runs on the CPU | [Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com/), NVIDIA's simulator with RTX rendering |
| **Runs on** | An Apple Silicon Mac or a Linux computer | Ubuntu with an NVIDIA RTX GPU, your own or a Viam cloud container |
| **Cost** | Free | Free on your own GPU; billed per minute in the cloud |
| **Download and first start** | A module of a few tens of megabytes that starts quickly | An Isaac Sim download of over 10 GB; the world's first start takes minutes while Isaac Sim boots and builds its caches |
| **Cameras** | OpenGL rendering, color and depth images | RTX rendering for realistic color images |
| **Robots included** | UFactory Lite6 and Universal Robots UR5e arms, several grippers, mobile bases, LIDARs and other sensors, and conveyor and scale parts | Several Universal Robots arms, a Franka arm, and a Jetbot base |
| **Your own robot** | An MJCF or URDF file | A USD file |
| **After a config change** | The module rebuilds the affected components right away | Changes to the world or to where a component spawns take effect after the module restarts |
| **Choose it to** | Learn Viam, develop motion and pick-and-place code, and iterate quickly on a scene | Train or test a vision model on realistic images, or use a robot that's available as USD |

In MuJoCo, an edited arm returns to its home pose when the module rebuilds it, and editing the world rebuilds everything that depends on it.
Isaac Sim can't be restarted inside a running module, which is why its changes wait for a module restart.

## What's next {#whats-next}

- [Run a MuJoCo simulation on your computer](/set-up-a-machine/simulate/mujoco/): start a free simulation on your Mac or Linux computer.
- [Run an Isaac Sim simulation](/set-up-a-machine/simulate/isaac-sim/): start a simulation with realistic rendering on a Viam cloud GPU or your own.
- [Simulate a machine you already have](/set-up-a-machine/simulate/simulate-an-existing-machine/): make a simulated copy of an existing machine that keeps its names and frames.
- [Move a simulated machine to real hardware](/set-up-a-machine/simulate/move-to-real-hardware/): run the code you wrote in simulation on your real robot.
