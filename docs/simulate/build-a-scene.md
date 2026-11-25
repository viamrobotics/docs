---
title: "Build a simulated scene"
linkTitle: "Build a scene"
weight: 50
type: "docs"
layout: "docs"
description: "Place robots, objects, and cameras in a MuJoCo or Isaac Sim scene and reload the scene after you change it."
capabilities: ["simulation", "motion-planning", "scene-3d"]
diataxis: how-to
date: "2026-11-24"
---

These tasks change what's in a running simulation so it matches your own workcell: where the robots stand, which objects are on the table, where the cameras look, and which robot model you use.

## Prerequisites {#prerequisites}

- A running simulation with a world component.
  See [Run a MuJoCo simulation on your computer](/simulate/mujoco/), [Run an Isaac Sim simulation](/simulate/isaac-sim/), or [Simulate a machine you already have](/simulate/simulate-an-existing-machine/).
- The simulator module's README, which lists every attribute and DoCommand these tasks use: [MuJoCo](https://github.com/viam-labs/viam-mujoco-sim#readme) or [Isaac Sim](https://github.com/viam-modules/viam-isaac-sim#readme).

Most tasks edit a component's JSON on the **CONFIGURE** tab.
To learn how the world component and the other simulated components fit together, see [How simulation works](/simulate/how-simulation-works/).

## Place a component {#place-a-component}

Place arms, bases, and fixed cameras with the component's standard frame, the same way you'd place real hardware.
Translations are in millimeters, and the simulator spawns the component where the frame system puts it, so the motion planner agrees with the simulation.
For more about frames, see [the frame system](/motion-planning/frame-system/).

{{< tabs >}}
{{% tab name="MuJoCo" %}}

Set the frame's `parent` to `world`, or to a simulated base for an arm that rides it:

```json
"frame": {
  "parent": "world",
  "translation": { "x": 0, "y": 300, "z": 0 }
}
```

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

Set the frame's `parent` to `world`:

```json
"frame": {
  "parent": "world",
  "translation": { "x": 0, "y": 300, "z": 0 }
}
```

Isaac Sim uses a frame as the spawn pose only when its parent is `world`.
An arm or base whose frame has another parent spawns at its `position` attribute, or at the origin if it has none, so check where it appears.

{{% /tab %}}
{{< /tabs >}}

Save the config.
The component moves to the new place in a camera image and on the **3D SCENE** tab.
In Isaac Sim, a new place for a component that's already in the scene takes effect only after you [reload the scene](#reload-the-scene-after-you-edit-it).

## Add objects {#add-objects}

Objects that the arm picks up or pushes around are props: they have physics, but the motion planner doesn't see them.
Fixed things the arm must avoid, such as a table or a wall, need to be in the frame system too, so the planner plans around them.

{{< tabs >}}
{{% tab name="MuJoCo" %}}

Add movable objects to the world's `props` attribute.
Positions are in meters, and a prop can be a cube, sphere, cylinder, capsule, or mesh:

```json
"props": [
  {
    "name": "pick_block",
    "size": 0.03,
    "position": [0.3, 0, 0.02],
    "color": [1, 0, 0]
  }
]
```

For a table, wall, bin, or fixture, add a `viam-labs:mujoco-sim:obstacle` component instead.
Its shape is the frame's `geometry` or a `mesh` file, and the motion planner avoids the same shape that MuJoCo simulates:

```json
{
  "name": "table",
  "api": "rdk:component:generic",
  "model": "viam-labs:mujoco-sim:obstacle",
  "frame": {
    "parent": "world",
    "translation": { "x": 400, "y": 0, "z": 0 },
    "geometry": {
      "type": "box",
      "x": 600,
      "y": 800,
      "z": 20,
      "translation": { "x": 0, "y": 0, "z": -10 }
    }
  },
  "attributes": { "world": "sim-world" }
}
```

Save the config.
Obstacles appear on the **3D SCENE** tab right away.
Props appear in camera images, and on the **3D SCENE** tab only if the machine has a `viam-labs:mujoco-sim:world_state` service.
See the [world](https://github.com/viam-labs/viam-mujoco-sim#model-viam-labsmujoco-simworld) and [obstacle](https://github.com/viam-labs/viam-mujoco-sim#model-viam-labsmujoco-simobstacle) sections of the README for every prop and obstacle attribute.

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

Add objects to the world's `props` attribute.
Positions are in meters; a prop is a `cube` or a `usd` file, and `"fixed": true` keeps it in place:

```json
"props": [
  {
    "name": "pick_block",
    "type": "cube",
    "position": [0.3, 0, 0.02],
    "size": 0.03,
    "color": [1, 0, 0]
  },
  {
    "name": "place_pad",
    "type": "cube",
    "fixed": true,
    "position": [0.32, -0.22, 0.005],
    "size": 0.2,
    "scale": [1, 1, 0.05],
    "color": [0.1, 0.3, 0.9]
  }
]
```

Isaac Sim spawns props when the world starts, so [reload the scene](#reload-the-scene-after-you-edit-it) after you save.
Props, fixed or not, aren't in the frame system, so the motion planner doesn't avoid them.
For an object the arm must plan around, also add it as an obstacle; see [Configure workspace obstacles](/motion-planning/obstacles/configure-workspace-obstacles/).
To see props on the **3D SCENE** tab, add the builtin world state store service, as the README's [World state store](https://github.com/viam-modules/viam-isaac-sim#world-state-store) section shows.

{{% /tab %}}
{{< /tabs >}}

## Add and aim a camera {#add-and-aim-a-camera}

A fixed camera watches the whole cell, and a wrist camera rides the arm to see what the gripper sees.

{{< tabs >}}
{{% tab name="MuJoCo" %}}

For a fixed camera, place it with its frame and aim it with `target`, a point in meters:

```json
"frame": {
  "parent": "world",
  "translation": { "x": 1200, "y": 1200, "z": 1000 }
},
"attributes": {
  "world": "sim-world",
  "target": [0.3, 0, 0.15]
}
```

For a wrist camera, make the arm the frame's parent and leave out `target`, which the module rejects on a camera that moves.
With no orientation, the camera looks along the tool axis:

```json
"frame": {
  "parent": "pick-arm",
  "translation": { "x": 0, "y": 60, "z": 30 }
},
"attributes": { "world": "sim-world" }
```

Mount the camera on the arm, not the gripper.
See the [camera section of the README](https://github.com/viam-labs/viam-mujoco-sim#model-viam-labsmujoco-simcamera) for field of view, resolution, and depth.

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

For a fixed camera, place it with its frame and aim it with `target`, a point in meters:

```json
"frame": {
  "parent": "world",
  "translation": { "x": 2200, "y": 2200, "z": 2000 }
},
"attributes": {
  "world": "sim-world",
  "target": [0.3, 0, 0.15]
}
```

For a wrist camera, set `parent_prim` to the arm link the camera rides and `local_position` to its offset from that link, in meters.
An arm's prim is `/World/` followed by its name with hyphens changed to underscores, so the last link of a UR arm named `pick-arm` is `/World/pick_arm/wrist_3_link`:

```json
"attributes": {
  "world": "sim-world",
  "parent_prim": "/World/pick_arm/wrist_3_link",
  "local_position": [0, 0, 0.06]
}
```

Changing `target` or a fixed camera's frame applies when you save.
Changing `parent_prim`, `width`, or `height` needs a [reload](#reload-the-scene-after-you-edit-it).
See the README's [camera attributes](https://github.com/viam-modules/viam-isaac-sim#camera-attributes) for field of view, depth, and orientation.

{{% /tab %}}
{{< /tabs >}}

Open the camera's card on the **CONTROL** tab and check that the image shows what you aimed it at.

## Use your own robot model {#use-your-own-robot-model}

Load your own arm instead of a bundled one, and give it a home pose so it starts clear of the table and objects.
Without a home pose, an arm starts with every joint at zero, which can put the tool inside the table.

{{< tabs >}}
{{% tab name="MuJoCo" %}}

Set the arm's `mjcf` attribute to your arm's MJCF (`.xml`) or URDF (`.urdf`) file, instead of `asset`.
With either file and no `kinematics_url`, the module serves kinematics that match the simulation, so the motion planner can plan for the arm.

Set the start pose with `home_joints`, one value per joint in radians:

```json
"attributes": {
  "world": "sim-world",
  "mjcf": "/path/to/my-arm.urdf",
  "home_joints": [0, -1.57, 1.57, 0, 1.57, 0]
}
```

An MJCF arm can instead use a keyframe from its file, named by `home_keyframe` (default `home`).
To convert a ROS xacro to URDF and fix masses and visuals, see the README's [Bring your own robot](https://github.com/viam-labs/viam-mujoco-sim#bring-your-own-robot) and [Your own arm](https://github.com/viam-labs/viam-mujoco-sim#your-own-arm) sections.

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

Set the arm's `usd_path` attribute to your arm's USD file, instead of `asset`.
`usd_path` also takes a `.urdf`, which the module imports into a USD the first time.
For the motion planner to plan for the arm, set `kinematics_url` to the arm's Viam kinematics file.

Set the start pose with `initial_joint_positions_deg`, one value per joint in degrees.
A custom arm also needs `joint_names`, in the same order:

```json
"attributes": {
  "world": "sim-world",
  "usd_path": "/path/to/my-arm.usd",
  "kinematics_url": "file:///path/to/my-arm.json",
  "joint_names": ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"],
  "initial_joint_positions_deg": [0, -90, 90, 0, 90, 0]
}
```

See the README's [arm attributes](https://github.com/viam-modules/viam-isaac-sim#arm-attributes) for URDF import settings, derived kinematics, and arms that share one articulation.
A new robot model replaces a prim that's already in the scene, so [reload the scene](#reload-the-scene-after-you-edit-it) after you save.

{{% /tab %}}
{{< /tabs >}}

The arm appears on the **3D SCENE** tab in its home pose.
Move one joint from the arm's card on the **CONTROL** tab, and check that the arm moves the same way in a camera image.

## Import a scene from Viam visualization {#import-a-scene-from-viam-visualization}

Viam visualization can [export a scene](/visualization/viam-visualization/#export-a-scene-for-simulation) as MJCF, so you can load a cell you've laid out there into MuJoCo.

{{< tabs >}}
{{% tab name="MuJoCo" %}}

1. In Viam visualization, hide the arms, grippers, and other components your simulation already has as their own components.
   The export leaves hidden objects out, so the scene doesn't hold a second copy of them.
1. Export the scene and unzip <file>scene-urdf-mjcf.zip</file> on the computer that runs the simulation.
1. Add a `viam-labs:mujoco-sim:scene` component that points at the export's <file>mjcf/scene.xml</file>.
   Its frame places the file's origin, must have parent `world`, and must have no `geometry`:

   ```json
   {
     "name": "cell",
     "api": "rdk:component:generic",
     "model": "viam-labs:mujoco-sim:scene",
     "frame": { "parent": "world" },
     "attributes": {
       "world": "sim-world",
       "mjcf": "/path/to/scene-urdf-mjcf/mjcf/scene.xml"
     }
   }
   ```

1. Save the config.

Cameras and physics see the whole scene, and the motion planner sees its fixed geometry.
Free bodies in the file become props named `cell/<body>`, which the world's prop commands move.
A scene file can't have actuators, so a robot with motors in it fails to load; read <file>export-notes.txt</file> and the [scene section of the README](https://github.com/viam-labs/viam-mujoco-sim#model-viam-labsmujoco-simscene) if it does.

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

Importing a Viam visualization export into Isaac Sim isn't supported.

<!-- Q6 in DOCS-5142: add steps here if Isaac Sim can load the URDF export. -->

{{% /tab %}}
{{< /tabs >}}

The scene's fixed geometry appears on the **3D SCENE** tab, and the whole scene appears in camera images.

## Reload the scene after you edit it {#reload-the-scene-after-you-edit-it}

How a change reaches a running simulation depends on the simulator and on what you changed.

{{< tabs >}}
{{% tab name="MuJoCo" %}}

A config change applies when you save: `viam-server` rebuilds each component you changed, and editing the world rebuilds every component that depends on it.
A rebuild resets that part of the cell, sending arms back home, so don't edit the config while your code is running.

A file you edit on disk, such as a scene or arm MJCF, isn't a config change, so restart the module to load it again:

1. On the **CONFIGURE** tab, find the `viam-labs_mujoco-sim` module.
1. Open its **...** menu and click **Restart**.

Mesh and texture URLs are downloaded only once.
To pick up a changed file at the same URL, change the URL, for example by adding `?v=2`.

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

Isaac Sim can't rebuild the scene while it runs.
Changes to the world, including its props, and to how a component spawns, such as its place, robot model, or camera resolution, apply only after you restart the module.
A component you add to the config spawns when you save, and a new arm resets the simulation as it spawns.

To restart the module:

1. On the **CONFIGURE** tab, find the Isaac Sim module.
1. Open its **...** menu and click **Restart**.

Isaac Sim takes minutes to start again, and in the cloud those minutes are billed like any other simulation time.

{{% /tab %}}
{{< /tabs >}}

When the module is running again, check the change in a camera image or on the **3D SCENE** tab.

## Move objects back to their starting poses {#move-objects-back-to-their-starting-poses}

Between test runs, put the cell back where it started, or move one object, without reloading the scene.
Send these commands to the world component from the DoCommand box on its card on the **CONTROL** tab, or with `do_command` from your code.

To return to the starting poses:

```json
{ "command": "reset" }
```

To move one prop, with its position in meters:

```json
{
  "command": "set_prop_pose",
  "prop": "pick_block",
  "position": [0.3, 0.05, 0.02],
  "orientation_wxyz": [1, 0, 0, 0]
}
```

{{< tabs >}}
{{% tab name="MuJoCo" %}}

`reset` sends arms home and returns every prop that isn't fixed to its spawn pose.
`set_prop_pose` stops the prop moving, and rejects a fixed prop.
`park_props`, with a list of prop names in `props`, returns only those props to their spawn poses.
Obstacles never move.

{{% /tab %}}
{{% tab name="Isaac Sim" %}}

`reset` resets the simulation and returns each arm to its `initial_joint_positions_deg`.
To return props to their spawn poses, send `park_props` with a list of prop names in `props`.
`set_prop_pose` stops the prop moving.

{{% /tab %}}
{{< /tabs >}}

The prop is at its new pose in a camera image.
`get_prop_pose`, with the prop's name in `prop`, returns where it is now.

## Troubleshooting {#troubleshooting}

{{% expand "Scene changes don't show up" %}}

The simulation didn't load the change.
In Isaac Sim, world, prop, and spawn changes need a module restart; in MuJoCo, a file edited on disk does.
Follow [Reload the scene after you edit it](#reload-the-scene-after-you-edit-it).
Check the machine's **LOGS** tab for a warning that the change needs a restart, or for an error loading a file.

{{% /expand %}}

{{% expand "The arm starts inside the table or knocks objects over" %}}

The arm's start pose, all joints at zero for an arm with no home pose, puts it in the way.
Give the arm a home pose that's clear of the scene, as in [Use your own robot model](#use-your-own-robot-model), or move the table and props away from the arm.

{{% /expand %}}

{{% expand "Moving one object launches another" %}}

`set_prop_pose` put the prop where another prop already is, and the physics engine pushed them apart.
Move the prop that's in the way first, with `set_prop_pose` or `park_props`, and then move the one you want.

{{% /expand %}}

## What's next {#whats-next}

- [Move a simulated machine to real hardware](/simulate/move-to-real-hardware/): run the code that works against your scene on the real robot.
- [How simulation works](/simulate/how-simulation-works/): learn how the world, props, and frame system fit together, and how MuJoCo and Isaac Sim differ.
- [Configure workspace obstacles](/motion-planning/obstacles/configure-workspace-obstacles/): add obstacles the motion planner avoids on a real machine.
