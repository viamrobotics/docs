---
linkTitle: "3D scene"
title: "Visualizing with the 3D scene"
weight: 5
layout: "docs"
type: "docs"
description: "The 3D scene's Monitor, Build, and Move modes, where to start for common tasks, and where each element in the scene comes from."
capabilities: ["scene-3d"]
diataxis: explanation
aliases:
  - /visualization/visualizing-with-the-3d-scene/
  - /visualization/3d-scene-tools/
  - /motion-planning/3d-scene/
  - /visualization/3d-scene/the-3d-scene-interface/
---

The **3D SCENE** tab renders your machine in an interactive 3D view: the frames of every
component, the geometry attached to them, point clouds from depth cameras, and any custom
visuals a module publishes while the machine runs. It turns configuration you would
otherwise read as JSON numbers into a picture you can inspect, so you can confirm a gripper
sits where its frame configuration places it or watch a motion plan against the obstacles
around it. In Build and Move modes, the scene does more than show your machine: you can edit
its configuration and command it to move.

This page covers the scene's modes, where to start for common tasks, and how the scene gets
what it draws.

## Modes

The scene has three modes. The mode determines what you can do and which tools appear.

| Mode                                             | What it's for                                                                         |
| ------------------------------------------------ | ------------------------------------------------------------------------------------- |
| [Monitor](/visualization/3d-scene/monitor-mode/) | Watch the machine's live state, read any frame's pose, and replay saved motion plans. |
| [Build](/visualization/3d-scene/build-mode/)     | Edit frames and geometry, then save them to the machine's configuration.              |
| [Move](/visualization/3d-scene/move-mode/)       | Plan a move to a target pose, preview it, and run it on the machine.                  |

In every mode, the **World** panel lists every entity in the scene, and selecting one shows
its details. [3D scene widgets](/visualization/3d-scene/3d-scene-widgets/) let you drive
components and read their values without leaving the scene. For navigation, shortcuts, and
settings, see [3D scene controls and settings](/visualization/3d-scene/controls-and-settings/).

## Start from what you want to do

| I want to…                                                              | Start here                                                                                           |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| See whether the scene matches my real machine                           | [Measuring between frames](/visualization/3d-scene/measuring-between-frames/)                        |
| Find where my end effector is right now                                 | [Monitor mode: read a frame's pose](/visualization/3d-scene/monitor-mode/#read-a-frames-pose)        |
| Enter frame offsets or add collision geometry without editing JSON      | [Editing frames visually](/visualization/3d-scene/editing-frames-visually/)                          |
| Add a table or wall the planner should avoid                            | [Build mode: add frames and obstacles](/visualization/3d-scene/build-mode/#add-frames-and-obstacles) |
| Move the arm to a pose without writing code, and preview the move first | [Move mode](/visualization/3d-scene/move-mode/)                                                      |
| Drive a component or watch its readings without leaving the scene       | [3D scene widgets](/visualization/3d-scene/3d-scene-widgets/)                                        |
| See what the motion planner saw when a plan failed or surprised me      | [Replay a saved plan](/visualization/3d-scene/monitor-mode/#replay-a-saved-plan)                     |
| Understand why the planner ignores something I can see                  | [Visuals and collisions](/visualization/visuals-and-collisions/)                                     |
| Check that a depth camera's point cloud lines up with the world         | [Verify point cloud alignment](/visualization/perception/verify-point-cloud-alignment/)              |
| Tune a 3D segmenter against the live view                               | [Vision services in the 3D scene](/visualization/perception/vision-services/)                        |
| See what a camera or end effector sees from its mount                   | [Frame POV](/visualization/3d-scene/3d-scene-widgets/#frame-pov)                                     |
| Draw my module's own visuals in the scene                               | [Publish visuals from a module](/visualization/publish-visuals-from-a-module/)                       |
| Preview spatial data from a Go script without deploying                 | [Viam Visualization](/visualization/viam-visualization/)                                             |
| Fix something that looks wrong                                          | [Troubleshoot the 3D scene](/visualization/troubleshoot-the-3d-scene/)                               |

## What the scene simulates, and what it doesn't

The scene works with kinematics, not physics. It shows where things are and where a plan
would take them, and checks for collisions against the geometry you've modeled. It doesn't
model dynamics, timing, or anything in the workspace that isn't modeled.

To try motion without risking hardware:

- Preview a move in [Move mode](/visualization/3d-scene/move-mode/). The preview plays the
  planned motion before anything moves. Running the plan, with **Execute plan** or **Move**,
  moves the machine; see the caution on the Move mode page.
- Simulated and fake components report poses and accept commands without moving anything
  physical. With a fake arm, the whole scene works without hardware. See
  [Try it with a fake arm](/hardware/common-components/add-an-arm/#try-it-with-a-fake-arm).

## What the scene renders

The scene draws four kinds of element, each with its own appearance:

- **Component frames** render as sets of red, green, and blue coordinate axes (X, Y, and
  Z), one per component, positioned by each frame's translation and orientation.
- **Geometries** render as translucent shapes (a box, sphere, or capsule) at the frame they
  are attached to.
- **Point clouds** from depth cameras render as colored point sets.
- **Custom visuals** render as whatever a module draws them as: markers, arrows, lines,
  meshes, or extra geometries, published while the machine runs.

## Where each element comes from

Every element of your machine's state in the scene traces back to one source. Select an
entity in the **World** panel to follow it back to the component or module that produced it.

| Element in the scene | Comes from                                                  |
| -------------------- | ----------------------------------------------------------- |
| Component frame      | The frame system, from each component's frame configuration |
| Attached geometry    | A component's `frame.geometry` in configuration             |
| Point cloud          | A depth camera, streamed live when the machine is online    |
| Custom visual        | A module, published through a world state store service     |

Frames and geometry appear because they are part of the machine's configuration, which the
scene reads whenever you open the tab. Point clouds stream from depth cameras while the
machine is online, and custom visuals appear only while a module publishes them.

The scene also draws things that aren't your machine's reported state: a Move mode preview,
a replayed plan and its obstacles, and Build mode edits you haven't saved yet.

## Built-in content versus custom visuals

The distinction between the sources matters because it tells you _where to make a change_:

- **Built-in content** is the frame system and configured geometry. The scene shows it with
  no code. To change a frame's position or a geometry's shape, edit the component's
  configuration.
- **Custom visuals** are everything a module computes or senses at runtime: a detection, a
  planned path, a sensor's obstacle readings. The scene shows them only while the module
  publishes them. To change a custom visual, change the module's code.

If an element looks wrong, this split tells you where to look: a misplaced frame or geometry
is a configuration problem, while a missing or stale custom visual is a module problem.

## How the scene stays current

Built-in content reflects your configuration and, when the machine is online, each
component's live pose. Custom visuals stay current a different way: a module publishes them
to a [world state store service](/reference/apis/services/world-state-store/), and the scene
subscribes to that service's stream of transform changes. As the module adds, updates, and
removes transforms, the scene applies each change to the one affected visual instead of
redrawing everything, so a busy scene keeps up as the underlying data changes.

To publish your own custom visuals this way, see
[Publish visuals from a module](/visualization/publish-visuals-from-a-module/).
