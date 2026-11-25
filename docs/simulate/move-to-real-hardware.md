---
title: "Move a simulated machine to real hardware"
linkTitle: "Move to real hardware"
weight: 60
type: "docs"
layout: "docs"
description: "Swap a simulated machine's components for real hardware while keeping the names, frames, and code that already work."
capabilities: ["simulation", "machine-config", "frame-system"]
diataxis: how-to
date: "2026-11-24"
---

Run the code you wrote against a simulated machine on your real robot, without rewriting it.
You copy the simulated machine's config to the real machine, swap each simulated model for its hardware model, and keep every resource name and frame your code depends on.
To learn why only the models change, see [What's different from real hardware](/simulate/how-simulation-works/#whats-different-from-real-hardware).

## Prerequisites {#prerequisites}

- A simulated machine and code that works against it.
  See [Run a MuJoCo simulation on your computer](/simulate/mujoco/) or [Run an Isaac Sim simulation](/simulate/isaac-sim/).
- The computer connected to your robot, running `viam-server` as its own Viam machine.
  Use a different machine from the simulated one, so the two configs stay separate.
  See [Set up your first machine](/set-up-a-machine/first-machine/).
- The robot's arm, gripper, and cameras connected to that computer and powered on.

## 1. Copy the config and keep the resource names {#copy-the-config-and-keep-the-resource-names}

Your code finds each component and service by its name, so the real machine needs the same names as the simulated one.

1. On the simulated machine's **CONFIGURE** tab, click **JSON**.
2. Copy the `components` and `services` arrays.
3. On the real machine's **CONFIGURE** tab, click **JSON**, and paste them in place of its own `components` and `services` arrays.
4. Don't click **Save** yet.
   Saving now would start the simulator module on the real machine's computer.

If the simulated machine's config has a `fragments` array, the copy doesn't include the fragment's resources, only a reference to the fragment.
Either copy the resources you need from the fragment's own **JSON** view, or keep the shared parts, such as your services, in the fragment and apply it to both machines.
See [Reuse configuration with fragments](/fleet/reuse-configuration/).

## 2. Replace each simulated model with its hardware model {#replace-each-simulated-model-with-its-hardware-model}

For each simulated component, change its `model` and `attributes` to the hardware model's.
Keep its `name`, `api`, and `frame`.

| Simulated as                                   | Hardware model from                                                                                                                                                                       |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A UFactory Lite6 arm (`asset` `lite6`)         | The `viam:ufactory` module. See [Add an arm](/hardware/common-components/add-an-arm/).                                                                                                    |
| A Universal Robots arm, such as `asset` `ur5e` | The `viam:universal-robots` module. See [Add an arm](/hardware/common-components/add-an-arm/).                                                                                            |
| The Lite6's gripper (`asset` `lite6_gripper`)  | The `viam:ufactory` module's xArm Lite gripper. See [Add a gripper](/hardware/common-components/add-a-gripper/).                                                                          |
| A Robotiq 2F-85 gripper                        | The `viam:robotiq` module. See [Add a gripper](/hardware/common-components/add-a-gripper/).                                                                                               |
| A camera                                       | Your camera's model, such as `webcam` for a USB camera or the `viam:realsense` module for an Intel RealSense depth camera. See [Add a camera](/hardware/common-components/add-a-camera/). |

For any other component, find its hardware model under [Common components](/hardware/common-components/).

1. In the real machine's JSON, set each component's `model` to its hardware model.
2. Replace its `attributes` with the hardware model's attributes, as the page for that component describes.
   Simulated attributes such as `world`, `asset`, and `mount` don't apply to hardware.
3. In the `modules` array, remove the simulator's module entry, `viam-labs_mujoco-sim` or `viam-labs_isaac-sim`.
4. Add an entry to `modules` for each hardware module your components use:

   ```json
   {
     "type": "registry",
     "name": "<namespace>_<module-name>",
     "module_id": "<namespace>:<module-name>",
     "version": "latest"
   }
   ```

If your code asks a camera for an image by source name, check that the real camera serves the same names.
A simulated depth camera serves images named `color` and `depth`, as the RealSense module does.

## 3. Remove the world and turn props you plan around into obstacles {#remove-the-world-and-turn-props-you-plan-around-into-obstacles}

The world component and the objects in its scene exist only in the simulation.
On the real machine, the motion planner avoids only the obstacles you configure, so anything it planned around in simulation needs an obstacle component.

1. Remove the world component, usually `sim-world`.
2. Remove any other component or service whose model comes from the simulator module and has no hardware counterpart, such as a MuJoCo `world_state` store.
3. For each MuJoCo `obstacle` component, change `model` to `rdk:builtin:obstacle`, and move the shape from its frame's `geometry` into a `geometries` list in its `attributes`:

   ```json
   {
     "name": "table",
     "api": "rdk:component:generic",
     "model": "rdk:builtin:obstacle",
     "frame": {
       "parent": "world",
       "translation": { "x": 400, "y": 0, "z": 0 }
     },
     "attributes": {
       "geometries": [
         {
           "type": "box",
           "x": 600,
           "y": 800,
           "z": 20,
           "translation": { "x": 0, "y": 0, "z": -10 }
         }
       ]
     }
   }
   ```

4. For each prop in the world's `props` that the arm must plan around, such as a fixture or a bin, add an obstacle component in the same way.
   Leave out props the robot picks up; those are real objects now.
5. Click **Save**.

For obstacle shapes, meshes, and the `erh:vmodutils` obstacle models, see [Configure workspace obstacles](/motion-planning/obstacles/configure-workspace-obstacles/).

## 4. Measure and update the frames {#measure-and-update-the-frames}

The simulated frames describe where you placed things in the simulated scene, not where they are in your cell.
Measure each component's real position, and update its frame to match, so the motion planner sees the arm, cameras, and obstacles where they are.

- **Arm:** its base's position and orientation relative to the world origin you choose.
- **Gripper:** the offset from the arm's end to the real gripper's tool point.
- **Cameras:** the position and orientation of each camera.
  A simulated camera aimed with the `target` attribute has no orientation in its frame, so add the measured orientation to the frame.
  For accurate images, [calibrate the camera](/motion-planning/frame-system/camera-calibration/).
- **Obstacles:** the position and size of each table, wall, and fixture.

For how to measure and configure each frame, see [Configure an arm, gripper, and wrist camera](/motion-planning/frame-system/arm-gripper-camera/) or [Configure an arm with a fixed camera](/motion-planning/frame-system/arm-fixed-camera/).
Save the config, then open the **3D SCENE** tab and check that each component and obstacle appears where it is in your cell.

## 5. Point your code at the real machine {#point-your-code-at-the-real-machine}

Your code connects to a machine by its address and an API key, so these are the only values to change.

1. On the real machine's **CONNECT** tab, select **SDK code sample**.
2. Copy the machine address and the API key and API key ID from the sample.
3. Replace the simulated machine's address and credentials in your code with these values.

If your code reads the address and credentials from environment variables, set the variables instead and leave the code unchanged.

## 6. Test your code on the real machine {#test-your-code-on-the-real-machine}

A real arm can damage itself, the cell, or people if a frame or obstacle is wrong, so start slowly.

1. Clear the workspace of people and anything you don't want the arm to touch, and keep the robot's emergency stop within reach.
2. Set the arm's speed attribute low, such as `speed_degs_per_sec` of 15 to 30 for the UFactory module.
   See [Add an arm](/hardware/common-components/add-an-arm/) for your arm's attributes.
3. On the **CONTROL** tab, move one joint of the arm a few degrees from its card, and check that the real arm moves the same way it moves on the **3D SCENE** tab.
4. Run your code.

The real arm makes the same moves it made in simulation.
If a move goes somewhere unexpected, stop the arm and recheck that component's frame.
Once the moves are right, raise the speed in steps.

## What's next {#whats-next}

- [How simulation works](/simulate/how-simulation-works/): what differs between a simulated machine and real hardware.
- [Simulate a machine you already have](/simulate/simulate-an-existing-machine/): go the other way, and make a simulated copy of the real machine to test new code against.
- [Configure workspace obstacles](/motion-planning/obstacles/configure-workspace-obstacles/): add the rest of your cell's fixed geometry so the motion planner avoids it.
- [Reuse configuration with fragments](/fleet/reuse-configuration/): keep the config the simulated and real machines share in one place.
