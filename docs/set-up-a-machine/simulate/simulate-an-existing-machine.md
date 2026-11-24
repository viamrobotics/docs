---
title: "Simulate a machine you already have"
linkTitle: "Simulate an existing machine"
weight: 25
type: "docs"
layout: "docs"
description: "Make a simulated copy of a Viam machine that keeps its resource names and frames, so its code runs unchanged."
capabilities: ["simulation", "machine-config", "frame-system"]
diataxis: how-to
date: "2026-11-24"
---

Make a second machine that runs a simulation of one you already have, with the same resource names and frames as the original.
Your code then connects to the simulated copy by changing only the address and credentials, so you can test it without risk to the real hardware.
To learn why only the models change, see [How simulated and real configs map](/set-up-a-machine/simulate/how-simulation-works/#how-simulated-and-real-configs-map).

## Prerequisites {#prerequisites}

- A configured Viam machine to copy, with real hardware or with fake components.
- A way to run a simulator:
  - For MuJoCo, an Apple Silicon Mac or a Linux x86_64 computer.
    See the prerequisites in [Run a MuJoCo simulation on your computer](/set-up-a-machine/simulate/mujoco/#prerequisites).
  - For Isaac Sim, a Viam cloud GPU or your own RTX Linux machine.
    See the prerequisites in [Run an Isaac Sim simulation](/set-up-a-machine/simulate/isaac-sim/#prerequisites).

## 1. Create the simulated machine {#create-the-simulated-machine}

Create a new machine for the simulation, in the same location as the original.
Never add the simulation to the original machine: a separate machine keeps simulated commands away from the real hardware and simulated images out of the real machine's data.

1. On the location's page in the Viam app, click **Add machine**.
2. Enter a name that marks it as the copy, such as `<original-name>-sim`, and click **Add machine**.

## 2. Start it {#start-it}

{{< tabs >}}
{{% tab name="MuJoCo" %}}

Install `viam-server` on your Mac or Linux computer as the new machine, and wait for the machine to show as online in the Viam app.
See [Set up your first machine](/set-up-a-machine/first-machine/).

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

Start the new machine in the Viam cloud or on your own GPU.
See step 1 of [Run an Isaac Sim simulation](/set-up-a-machine/simulate/isaac-sim/#start-the-machine).

{{% /tab %}}
{{< /tabs >}}

## 3. Copy the config and replace each hardware model with a simulated one {#copy-the-config-and-replace-each-hardware-model-with-a-simulated-one}

Your code finds each component and service by its name, so keep every `name`, `api`, and `frame` from the original, and change only each component's `model` and `attributes`.
Every simulated component names the world in its `world` attribute, so add the world first.

Each simulator has its own models for the arm, gripper, and camera:

{{< tabs >}}
{{% tab name="MuJoCo" %}}

- **Arm:** `viam-labs:mujoco-sim:arm`, with `asset` set to `lite6` for a UFactory Lite6 or `ur5e` for a Universal Robots UR5e.
  Its frame parent must be `world` or a simulated base, so an arm mounted on another component needs `world` as its parent and its pose relative to the world.
- **Gripper:** `viam-labs:mujoco-sim:gripper`, with `mount` set to the arm's name, and `asset` set to `lite6_gripper` for the Lite6's gripper or `robotiq_2f85` for a Robotiq 2F-85.
- **Camera:** `viam-labs:mujoco-sim:camera`.
  Set `width`, `height`, and `fov_deg` (the vertical field of view) to match the real camera, and `depth` to `true` for a depth camera.
  A MuJoCo camera can ride an arm but not a gripper, so for a camera whose frame parent is a gripper, change the parent to the arm and add the gripper's offset to the camera's translation.

For example, a real UR5e named `arm-1` becomes:

```json
{
  "name": "arm-1",
  "api": "rdk:component:arm",
  "model": "viam-labs:mujoco-sim:arm",
  "frame": { "parent": "world" },
  "attributes": { "world": "sim-world", "asset": "ur5e" }
}
```

For your own arm or gripper from an MJCF or URDF file, and every attribute of each model, see the [MuJoCo module README](https://github.com/viam-labs/viam-mujoco-sim#models).

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

- **Arm:** `viam-labs:isaac-sim:arm`, with `asset` set to `lite6` for a UFactory Lite6, or to a Universal Robots arm such as `ur5e` or `ur20`.
- **Gripper:** `viam-labs:isaac-sim:gripper`, with `arm` set to the arm's name, and `asset` set to `lite6_gripper` for the Lite6's gripper or `robotiq_2f_85` for a Robotiq 2F-85.
- **Camera:** `viam-labs:isaac-sim:camera`.
  Set `width`, `height`, and `fov_deg` (the horizontal field of view) to match the real camera, and `depth` to `true` for a depth camera.

For example, a real UR5e named `arm-1` becomes:

```json
{
  "name": "arm-1",
  "api": "rdk:component:arm",
  "model": "viam-labs:isaac-sim:arm",
  "frame": { "parent": "world" },
  "attributes": { "world": "sim-world", "asset": "ur5e" }
}
```

After you save, check each component's place on the **3D SCENE** tab.

For other robots, and every attribute of each model, see the [Isaac Sim module README](https://github.com/viam-modules/viam-isaac-sim#readme).

{{% /tab %}}
{{< /tabs >}}

1. Add the simulator's world component to the new machine, named `sim-world`, and save.
   For MuJoCo, follow [Add the MuJoCo world](/set-up-a-machine/simulate/mujoco/#add-the-mujoco-world).
   For Isaac Sim, add only the world from step 2 of [Run an Isaac Sim simulation](/set-up-a-machine/simulate/isaac-sim/#add-the-isaac-sim-world-and-a-starter-cell).
   Adding the world also adds the simulator's module to the config.
2. On the original machine's **CONFIGURE** tab, click **JSON**, and copy the `components` and `services` arrays.
3. On the new machine's **CONFIGURE** tab, click **JSON**.
   Paste the components into its `components` array after `sim-world`, and the services into its `services` array.
4. If the original's JSON has a `fragments` array, the copy holds only a reference to each fragment, not its resources.
   Copy the resources from each fragment's own **JSON** view instead, and replace any fragment variables with their values.
   Don't copy the `fragments` array, or the new machine would load the real hardware's config.
5. For each arm, gripper, and camera, change `model` to the simulated model and replace `attributes` with the simulated attributes, as the tab for your simulator shows.
6. For each other hardware component, such as a motor or a sensor, change `model` to `rdk:builtin:fake` and set `attributes` to `{}`, so code that calls it still finds it.
7. Remove each service whose model comes from a hardware driver module, the data manager service, and every component's `service_configs`.
   Without data capture, simulated images never mix with the original machine's data.
8. Click **Save**.

Obstacle components carry over unchanged, so the motion planner avoids the same shapes it does on the original.
To make the simulated arm collide with them too, and to add tables and objects the original's config doesn't describe, see [Build a simulated scene](/set-up-a-machine/simulate/build-a-scene/).

## 4. Verify the copy {#verify-the-copy}

1. Open the original machine's **3D SCENE** tab and the new machine's **3D SCENE** tab side by side.
   Each component appears in the same place on both.
2. On the new machine's **CONTROL** tab, open each camera's card and turn on its stream.
   The arm, gripper, and objects appear where that camera sees them on the original machine.
3. On the new machine's **CONNECT** tab, select **SDK code sample**, and copy the machine address, API key, and API key ID.
4. Replace the original machine's address and credentials in your code with these values, and run it.

Your code runs against the simulated copy, and the moves it makes appear in the camera streams.
If your code asks a camera for an image by source name, note that simulated depth cameras serve images named `color` and `depth`.

## Replace fake components with simulated ones {#replace-fake-components-with-simulated-ones}

A machine built from fake components, such as one from a motion planning quickstart, can run the simulation itself instead of through a copy, since there's no real hardware to protect.

1. On the machine's **CONFIGURE** tab, add the simulator's world component, as in step 3.
2. Click **JSON**.
3. For each fake arm, gripper, and camera, change `model` from `rdk:builtin:fake` to the simulated model, and replace `attributes` with the simulated attributes.
   Keep each `name` and `frame`.
4. Click **Save**.

The machine must run the simulator: on MuJoCo, it's a Mac or Linux computer, and on Isaac Sim, a cloud GPU or your own RTX machine.
Verify it as in step 4, without the side-by-side comparison.

## What's next {#whats-next}

- [Build a simulated scene](/set-up-a-machine/simulate/build-a-scene/): add the tables, objects, and camera angles of your real cell to the copy.
- [Move a simulated machine to real hardware](/set-up-a-machine/simulate/move-to-real-hardware/): take code you develop against the copy back to the real machine.
- [How simulation works](/set-up-a-machine/simulate/how-simulation-works/): what behaves the same in simulation as on real hardware, and what doesn't.
