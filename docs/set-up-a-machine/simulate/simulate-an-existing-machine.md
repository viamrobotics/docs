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

For MuJoCo, the `mujoco-sim` Claude Code plugin in the [MuJoCo module's repository](https://github.com/viam-labs/viam-mujoco-sim#build-a-cell-with-an-agent) can make the copy and check its resource names, frames, and arm kinematics against the original's.

## Prerequisites {#prerequisites}

- A configured Viam machine to copy, with real hardware or with fake components.
  The comparison in step 4 needs it online: check its status in the Viam app, or check that `read_part_status` returns `online`.
- A computer or GPU to run the simulator:
  - For MuJoCo, an Apple Silicon Mac or a Linux x86_64 computer.
    Check with `uname -sm`, which prints `Darwin arm64` or `Linux x86_64`.
    See the prerequisites in [Run a MuJoCo simulation on your computer](/set-up-a-machine/simulate/mujoco/#prerequisites).
  - For Isaac Sim, a Viam cloud GPU, billed per minute, or your own RTX Linux computer.
    See the prerequisites in [Run an Isaac Sim simulation](/set-up-a-machine/simulate/isaac-sim/#prerequisites).

## How a simulated copy works {#how-a-simulated-copy-works}

The simulated copy is a separate machine whose config matches the original's, except for each hardware component's `model` and `attributes`.
Every simulated component names a world component in its `world` attribute, and the world runs the simulator.
To learn why only the models change, see [What's different from real hardware](/set-up-a-machine/simulate/how-simulation-works/#whats-different-from-real-hardware).

## 1. Create the simulated machine {#create-the-simulated-machine}

Create a new machine for the simulation, in the same location as the original.
Never add the simulation to the original machine: a separate machine keeps simulated commands away from the real hardware and simulated images out of the real machine's data.

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On the location's page in the Viam app, click **Add machine**.
2. Enter a name that marks it as the copy, such as `<original-name>-sim`, and click **Add machine**.

{{% /tab %}}
{{% tab name="CLI" %}}

```sh {class="command-line" data-prompt="$"}
viam machines create --name=<original-name>-sim --location=<location-id>
```

{{% /tab %}}
{{% tab name="MCP" %}}

`create_machine`.
It takes the original's `location_id`, which `read_machine_config` returns for the original, and a `name` that's unique in the location, such as `<original-name>-sim`.
The new machine imports your organization's default fragments, if it has any.

{{% /tab %}}
{{< /tabs >}}

The new machine appears on the location's page and hasn't connected yet: `read_part_status` returns `awaiting_setup`.
If its config has a `fragments` array, remove each fragment that configures real hardware.

## 2. Start the simulated machine {#start-the-simulated-machine}

{{< tabs >}}
{{% tab name="MuJoCo" %}}

On the Mac or Linux computer that will run the simulation, install `viam-server` as the new machine.
See [Set up your first machine](/set-up-a-machine/first-machine/).
This step runs on that computer, so the Viam MCP server can't do it.

The machine shows as online in the Viam app, and `read_part_status` returns `online`.

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

Start the new machine in the Viam cloud or on your own GPU.
See step 1 of [Run an Isaac Sim simulation](/set-up-a-machine/simulate/isaac-sim/#start-the-machine).

A cloud simulation is billed per minute to the machine's organization until it stops or goes idle.
With the Viam MCP server, `start_simulation` starts it with no confirmation prompt.
It takes the new machine's `machine_id` and uses the main part if you leave out `part_name`.
If a simulation is already starting or running, it returns that one with `created` set to `false`.

Startup takes a few minutes, and longer when it waits for a GPU.
`read_simulation` reports `pending` or `provisioning` while it starts and `started` once it's up.
Then `read_part_status` returns `online`.

{{% /tab %}}
{{< /tabs >}}

## 3. Copy the config and replace each hardware model with a simulated one {#copy-the-config-and-replace-each-hardware-model-with-a-simulated-one}

Your code finds each component and service by its name, so keep every `name`, `api`, and `frame` from the original, and change only each hardware component's `model` and `attributes`, as the table below shows.
Every simulated component names the world in its `world` attribute, so add the world first, named `sim-world`.

Each hardware component in the original maps to one simulated model:

| In the original                                           | In a MuJoCo copy                                                                                                   | In an Isaac Sim copy                                                         |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| (none)                                                    | World: `viam-labs:mujoco-sim:world`                                                                                | World: `viam-labs:isaac-sim:world`                                           |
| UFactory Lite6 arm                                        | `viam-labs:mujoco-sim:arm`, `asset` `lite6`                                                                        | `viam-labs:isaac-sim:arm`, `asset` `lite6`                                   |
| Universal Robots UR5e arm                                 | `viam-labs:mujoco-sim:arm`, `asset` `ur5e`                                                                         | `viam-labs:isaac-sim:arm`, `asset` `ur5e`                                    |
| Another Universal Robots arm, such as a UR20              | Your own model; see [Use your own robot model](/set-up-a-machine/simulate/build-a-scene/#use-your-own-robot-model) | `viam-labs:isaac-sim:arm`, `asset` such as `ur20`                            |
| UFactory Lite6 gripper                                    | `viam-labs:mujoco-sim:gripper`, `asset` `lite6_gripper`, `mount` the arm's name                                    | `viam-labs:isaac-sim:gripper`, `asset` `lite6_gripper`, `arm` the arm's name |
| Robotiq 2F-85 gripper                                     | `viam-labs:mujoco-sim:gripper`, `asset` `robotiq_2f85`, `mount` the arm's name                                     | `viam-labs:isaac-sim:gripper`, `asset` `robotiq_2f_85`, `arm` the arm's name |
| Camera                                                    | `viam-labs:mujoco-sim:camera`                                                                                      | `viam-labs:isaac-sim:camera`                                                 |
| Any other hardware component, such as a motor or a sensor | `rdk:builtin:fake`, no attributes                                                                                  | `rdk:builtin:fake`, no attributes                                            |

Carries over unchanged: every resource's `name` and `api`, frames (with the MuJoCo exceptions in step 3), obstacle components, and services that don't drive hardware, such as the motion service.

Doesn't carry over:

- `fragments` and `fragment_mods`: the copy holds the fragments' resources instead, so it never loads the real hardware's config.
- The data manager service, any shell service, and every component's `service_configs`, so simulated images never mix with the original machine's data.
- Services whose model comes from a hardware driver module.
- API keys, tokens, passwords, and webhook URLs in module `env` values or attributes.
- The arm's current pose: a simulated arm starts in its home pose.

For every attribute of each simulated model, see the [MuJoCo module README](https://github.com/viam-labs/viam-mujoco-sim#models) or the [Isaac Sim module README](https://github.com/viam-modules/viam-isaac-sim#readme).

Each simulator has its own limits on frames and cameras:

{{< tabs >}}
{{% tab name="MuJoCo" %}}

- **Floor:** if the original's frames put the origin above the floor, such as at an arm's base on a table, set the world's `floor_z` to the floor's height below the origin, in meters, such as `-0.9` for a workbench.
  Otherwise the simulated floor cuts through the table.
- **Arm frames:** a MuJoCo arm's frame parent must be `world` or a simulated base.
  For an arm mounted on another component, set its parent to `world` and its pose relative to the world.
- **Home pose:** if the arm's home pose puts the gripper into a table, set `home_joints` to the real arm's stow pose, as [Use your own robot model](/set-up-a-machine/simulate/build-a-scene/#use-your-own-robot-model) shows.
- **Camera frames:** a MuJoCo camera can ride an arm but not a gripper.
  For a camera whose frame parent is a gripper, change the parent to the arm and add the gripper's offset to the camera's translation.
- **Camera settings:** set `width`, `height`, and `fov_deg` (the vertical field of view) to match the real camera, and `depth` to `true` for a depth camera.

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

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

- **Camera settings:** set `width`, `height`, and `fov_deg` (the horizontal field of view) to match the real camera, and `depth` to `true` for a depth camera.

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

{{% /tab %}}
{{< /tabs >}}

Copy the config and change it:

{{< tabs >}}
{{% tab name="Viam app" %}}

1. Add the simulator's world component to the new machine, named `sim-world`, and save.
   For MuJoCo, follow [Add the MuJoCo world](/set-up-a-machine/simulate/mujoco/#add-the-mujoco-world).
   For Isaac Sim, add only the world from step 2 of [Run an Isaac Sim simulation](/set-up-a-machine/simulate/isaac-sim/#add-the-isaac-sim-world-and-a-starter-cell).
   Adding the world also adds the simulator's module to the config.
2. On the original machine's **CONFIGURE** tab, click **JSON**, and copy the `components` and `services` arrays.
3. On the new machine's **CONFIGURE** tab, click **JSON**.
   Paste the components into its `components` array after `sim-world`, and the services into its `services` array.
4. If the original's JSON has a `fragments` array, copy the resources from each fragment's own **JSON** view, and replace any fragment variables with their values.
   If it has a `fragment_mods` array, apply each override to the resources you copied.
   Don't copy the `fragments` or `fragment_mods` arrays.
5. Change each resource as the table above shows, and remove what doesn't carry over.
6. If no camera sees the whole cell, add a simulated camera that does, so you can watch the copy.
   For MuJoCo, see [Add a camera](/set-up-a-machine/simulate/mujoco/#add-a-camera).
7. Click **Save**.

{{% /tab %}}
{{% tab name="MCP" %}}

`read_machine_config` on the original returns `rendered_config`, the config the machine runs, with fragments already resolved and robot credentials removed.
Copy its components and services from there, not from `config`, which holds only fragment references.
Module `env` values and attributes can still hold secrets, so remove them as the table says.

Write the copy with `add_machine_config_item`, one call per resource, starting with `sim-world`.
Each call saves at once, validates registry models and resource references, and adds a missing module with its component.
Alternatively, `set_machine_config` replaces the new machine's whole config in one call, using the `revision` that `read_machine_config` returns for the new machine; it's experimental.

{{% /tab %}}
{{< /tabs >}}

The new machine's config lists every component and service name from the original, plus `sim-world`, and has no `fragments` array.
Check it on the **CONFIGURE** tab, or with `read_machine_config` on the new machine.
Obstacle components carry over, so the motion planner avoids the same shapes it does on the original.
To make the simulated arm collide with them too, and to add tables and objects the original's config doesn't describe, see [Build a simulated scene](/set-up-a-machine/simulate/build-a-scene/).

## 4. Verify the copy {#verify-the-copy}

Compare the frames on both machines:

{{< tabs >}}
{{% tab name="Viam app" %}}

Open the original machine's **3D SCENE** tab and the new machine's **3D SCENE** tab side by side.
Each component appears in the same place on both.
Then, on the new machine's **CONTROL** tab, open each camera's card and turn on its stream.
The arm, gripper, and objects appear where that camera sees them on the original machine.

{{% /tab %}}
{{% tab name="MCP" %}}

Call `get_world_state` on both machines.
Each frame in the original appears in the copy with the same `parent`, and each frame whose `movable` is `false` has the same `pose_in_world`.
Frames on an arm differ until both arms are in the same pose.
`get_world_state` connects to each machine with its default API key, and creates the key if the machine has none.

{{% /tab %}}
{{< /tabs >}}

Then run your code against the copy:

1. On the new machine's **CONNECT** tab, select **SDK code sample**, and copy the machine address, API key, and API key ID.
   The Viam MCP server doesn't return API keys, so this step uses the Viam app.
2. Replace the original machine's address and credentials in your code with these values, and run it.

Your code runs against the simulated copy, and the moves it makes appear in the camera streams.
If your code asks a camera for an image by source name, note that simulated depth cameras serve images named `color` and `depth`.

## Replace fake components with simulated ones {#replace-fake-components-with-simulated-ones}

A machine built from fake components, such as one from a motion planning quickstart, can run the simulation itself instead of through a copy, since there's no real hardware to protect.
The machine must run the simulator: for MuJoCo, it's a Mac or Linux computer, and for Isaac Sim, a cloud GPU or your own RTX machine.

1. On the machine's **CONFIGURE** tab, add the simulator's world component, named `sim-world`, as step 3 of this page does for a copy.
2. Click **JSON**.
3. For each fake arm, gripper, and camera, change `model` from `rdk:builtin:fake` to the simulated model in the table in [step 3](#copy-the-config-and-replace-each-hardware-model-with-a-simulated-one), and replace `attributes` with the simulated attributes.
   Keep each `name` and `frame`.
4. Click **Save**.

With the Viam MCP server, make the change with `set_machine_config`, which replaces the whole config.
`update_machine_config_item` can't change a component's `model`.

Check the machine as step 4 of this page does, without the side-by-side comparison.

## What's next {#whats-next}

- [Build a simulated scene](/set-up-a-machine/simulate/build-a-scene/): add the tables, objects, and camera angles of your real cell to the copy.
- [Move a simulated machine to real hardware](/set-up-a-machine/simulate/move-to-real-hardware/): take code you develop against the copy back to the real machine.
- [How simulation works](/set-up-a-machine/simulate/how-simulation-works/): what behaves the same in simulation as on real hardware, and what doesn't.
