---
title: "Run a MuJoCo simulation on your computer"
linkTitle: "MuJoCo on your computer"
weight: 20
type: "docs"
layout: "docs"
description: "Run the MuJoCo simulator module on your own Mac or Linux computer to build and test a robot cell at no cost."
capabilities: ["simulation", "machine-config"]
diataxis: how-to
date: "2026-11-24"
---

Run a simulated arm, gripper, and camera in MuJoCo on your own computer, and control them from the Viam app and your code as you would real hardware.
MuJoCo runs on your computer's CPU, so the simulation costs nothing.
To learn how a simulated machine works and how MuJoCo compares with Isaac Sim, see [How simulation works](/set-up-a-machine/simulate/how-simulation-works/).

## Prerequisites {#prerequisites}

- An Apple Silicon Mac or a Linux x86_64 computer.
  The MuJoCo module is built for these two platforms only.
- `viam-server` running on that computer as a Viam machine, online in the Viam app.
  See [Set up your first machine](/set-up-a-machine/first-machine/).
- To configure the simulation from an AI client instead of the Viam app, the [Viam MCP server](/reference/mcp/) connected to that client.

## 1. Add the MuJoCo world {#add-the-mujoco-world}

The world component owns the MuJoCo scene and runs the simulation.
Every other simulated component names it, so add it first.

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On your machine's **CONFIGURE** tab, click **+**, then select **Blocks**.
2. Search for `mujoco-sim` and select the `viam-labs:mujoco-sim:world` model.
3. Name the component `sim-world` and click **Add to machine**.
   The Viam app also adds the `viam-labs:mujoco-sim` module to your machine's config.
4. Leave the attributes empty.
   Every world attribute is optional; the defaults give you a floor and lighting.
5. Click **Save**.

{{% /tab %}}
{{% tab name="MCP server" %}}

With the [Viam MCP server](/reference/mcp/) connected, ask your MCP client something like:

> On my machine `<machine-name>`, add a generic component named `sim-world` with the model `viam-labs:mujoco-sim:world` from the `viam-labs:mujoco-sim` module, with no attributes.

The client calls the `add_machine_config_item` tool, which saves the change right away and adds the `viam-labs:mujoco-sim` module along with the component.

{{% /tab %}}
{{< /tabs >}}

`viam-server` downloads the module and runs its first-run script, which installs the module's Python environment.
On Linux, the script also installs `libegl1` if it's missing, so cameras can render on the GPU.
The first start takes longer than later ones.

## 2. Add simulated hardware {#add-simulated-hardware}

Add a simulated model for each piece of hardware your robot has.
Each one names the world in its `world` attribute and is placed by its frame, in millimeters.
This example adds a UFactory Lite6 arm and its gripper.

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On the **CONFIGURE** tab, click **JSON**.
2. Add these two objects to the `components` array, after `sim-world`:

   ```json
   {
     "name": "pick-arm",
     "api": "rdk:component:arm",
     "model": "viam-labs:mujoco-sim:arm",
     "frame": { "parent": "world" },
     "attributes": {
       "world": "sim-world",
       "asset": "lite6",
       "max_joint_deg_s": 30
     }
   },
   {
     "name": "pick-gripper",
     "api": "rdk:component:gripper",
     "model": "viam-labs:mujoco-sim:gripper",
     "frame": {
       "parent": "pick-arm",
       "translation": { "x": 0, "y": 0, "z": 81.1 }
     },
     "attributes": {
       "world": "sim-world",
       "mount": "pick-arm"
     }
   }
   ```

3. Click **Save**.

{{% /tab %}}
{{% tab name="MCP server" %}}

Ask your MCP client something like:

> On my machine `<machine-name>`, add two components from the `viam-labs:mujoco-sim` module:
>
> - An arm named `pick-arm` with the model `viam-labs:mujoco-sim:arm`, the attributes `{"world": "sim-world", "asset": "lite6", "max_joint_deg_s": 30}`, and a frame with parent `world`.
> - A gripper named `pick-gripper` with the model `viam-labs:mujoco-sim:gripper`, the attributes `{"world": "sim-world", "mount": "pick-arm"}`, and a frame with parent `pick-arm` and translation `{"x": 0, "y": 0, "z": 81.1}`.

The client adds each component with `add_machine_config_item`, then sets its frame with `update_machine_config_item`.

{{% /tab %}}
{{< /tabs >}}

This config sets:

- **`pick-arm`**: the bundled UFactory Lite6 arm, standing at the world origin.
  `max_joint_deg_s` limits each joint to 30 degrees per second, so you can watch it move.
- **`pick-gripper`**: the Lite6's own gripper, on `pick-arm`.
  Its frame's `z` of 81.1 mm puts the motion planner's tool point at the fingertips.

For other bundled arms, grippers, bases, and sensors, and every attribute of each model, see the [MuJoCo module README](https://github.com/viam-labs/viam-mujoco-sim#models).

## 3. Add a camera {#add-a-camera}

A simulated camera renders the MuJoCo scene from its own viewpoint.
It's how you see the simulation in the Viam app, and it's what vision services and data capture read from, so add one whatever hardware your robot has.

{{< tabs >}}
{{% tab name="Viam app" %}}

1. On the **CONFIGURE** tab, click **JSON**.
2. Add this object to the `components` array:

   ```json
   {
     "name": "scene-cam",
     "api": "rdk:component:camera",
     "model": "viam-labs:mujoco-sim:camera",
     "frame": {
       "parent": "world",
       "translation": { "x": 1200, "y": 1200, "z": 1000 }
     },
     "attributes": {
       "world": "sim-world",
       "target": [0.3, 0, 0.15]
     }
   }
   ```

3. Click **Save**.

{{% /tab %}}
{{% tab name="MCP server" %}}

Ask your MCP client something like:

> On my machine `<machine-name>`, add a camera named `scene-cam` with the model `viam-labs:mujoco-sim:camera` from the `viam-labs:mujoco-sim` module, the attributes `{"world": "sim-world", "target": [0.3, 0, 0.15]}`, and a frame with parent `world` and translation `{"x": 1200, "y": 1200, "z": 1000}`.

{{% /tab %}}
{{< /tabs >}}

`scene-cam` is a fixed camera 1.2 meters along both the x and y axes from the arm, and 1 meter up.
`target` aims it at a point in meters, not millimeters, just above the arm's base.

## 4. Verify the cell {#verify-the-cell}

Check each simulated component from the Viam app, watching through the camera.

1. On the **CONTROL** tab, open the camera's card and turn on its stream.
   The image shows your simulated hardware in the scene.
   In the example, `scene-cam` shows the arm standing on the floor.
2. Open the **3D SCENE** tab.
   Each component appears where its frame puts it.
   In the example, the arm is at the origin, with the gripper on its end.
3. On the **CONTROL** tab, move a component from its card, and watch it move in the camera stream.
   In the example, open the `pick-arm` card and change the first joint's position by 30 degrees; the arm turns about its base.

If all three checks pass, the simulation is running and responds to the same component APIs as real hardware.

## Troubleshooting {#troubleshooting}

{{% expand "On Linux, the camera shows no image" %}}

**Cause:** the module's first-run script couldn't install `libegl1`, which cameras need to render.
It installs the package only when `viam-server` runs as root or the user has passwordless `sudo`.
The **LOGS** tab shows `libEGL.so.1 missing and no root or passwordless sudo; cameras will not render` or `libegl1 install failed; cameras will not render`.

**Fix:** install the package yourself, then restart `viam-server`:

```sh {class="command-line" data-prompt="$"}
sudo apt-get install -y libegl1
```

{{% /expand %}}

{{% expand "The logs show warnings that say got stderr when the module first starts" %}}

**Cause:** the module's first-run script writes its Python install progress to stderr, and `viam-server` logs each line of a first-run script's stderr as a warning.
This is normal.

**Fix:** none needed.
Wait for the log line `first run script succeeded`; the world and the other components start after it.

{{% /expand %}}

## What's next {#whats-next}

- [Build a simulated scene](/set-up-a-machine/simulate/build-a-scene/): add objects and cameras, use your own robot model, and reload the scene after you change it.
- [Move your first arm](/motion-planning/quickstarts/first-arm/): plan arm moves with the motion service, which plans for `pick-arm` as it would for a real arm.
- [Move a simulated machine to real hardware](/set-up-a-machine/simulate/move-to-real-hardware/): run the code you write against this simulation on a real robot.
- [Build a cell with an agent](https://github.com/viam-labs/viam-mujoco-sim#build-a-cell-with-an-agent): use the module's Claude Code plugin to build and test a MuJoCo cell from a description.
