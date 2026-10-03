---
linkTitle: "3D scene"
title: "Visualizing with the 3D scene"
weight: 5
layout: "docs"
type: "docs"
description: "What the 3D scene renders, where each element comes from, and how built-in configuration content differs from custom visuals a module publishes at runtime."
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
around it.

This page describes what the scene shows, where each element comes from, how the scene
stays current, and the three modes you work in. To jump to a task, see
[Start from what you want to do](#start-from-what-you-want-to-do).

## Visualization, not simulation

The 3D scene shows your machine; it doesn't simulate physics. Everything it draws comes from
your machine's configuration or from live data, so what you see is what the machine reports.

Two things let you try motion without risking hardware:

- [Move mode](/visualization/3d-scene/move-mode/) previews a planned move in the scene
  before anything moves, so you can see the motion before you run it.
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

Every element in the scene traces back to one source. The **World panel** lists every entity
in a tree rooted at the world frame, so you can select anything on screen and follow it back
to the component or module that produced it.

| Element in the scene | Comes from                                                  |
| -------------------- | ----------------------------------------------------------- |
| Component frame      | The frame system, from each component's frame configuration |
| Attached geometry    | A component's `frame.geometry` in configuration             |
| Point cloud          | A depth camera, streamed live when the machine is online    |
| Custom visual        | A module, published through a world state store service     |

The first three appear because they are part of the machine's configuration, and the scene
reads that configuration whenever you open the tab. Custom visuals appear only when a module
publishes them.

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

## Modes

The scene has three modes. The mode decides what you can do and which tools appear.

| Mode                                             | What it's for                                                                                      |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| [Monitor](/visualization/3d-scene/monitor-mode/) | Watch the machine's live state, read any frame's pose, and replay saved motion plans. The default. |
| [Build](/visualization/3d-scene/build-mode/)     | Edit frames and geometry, then save them to the machine's configuration.                           |
| [Move](/visualization/3d-scene/move-mode/)       | Plan a move to a target pose, preview it, and run it on the machine.                               |

In every mode, the **World** panel lists every entity in the scene, and selecting one shows
its details. [3D scene widgets](/visualization/3d-scene/3d-scene-widgets/) let you drive
components and read their values without leaving the scene. For navigation, shortcuts, and
settings, see [3D scene controls and settings](/visualization/3d-scene/controls-and-settings/).

## Start from what you want to do

| I want to…                                                         | Start here                                                                              |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| See whether the scene matches my real machine                      | [Measuring between frames](/visualization/3d-scene/measuring-between-frames/)           |
| Enter frame offsets or add collision geometry without editing JSON | [Editing frames visually](/visualization/3d-scene/editing-frames-visually/)             |
| Try a move safely before it runs                                   | [Move mode](/visualization/3d-scene/move-mode/)                                         |
| Drive a component or watch its readings without leaving the scene  | [3D scene widgets](/visualization/3d-scene/3d-scene-widgets/)                           |
| See what the motion planner saw when a plan failed or surprised me | [Replay a saved plan](/visualization/3d-scene/monitor-mode/#replay-a-saved-plan)        |
| Understand why the planner ignores something I can see             | [Visuals and collisions](/visualization/visuals-and-collisions/)                        |
| Check that a depth camera's point cloud lines up with the world    | [Verify point cloud alignment](/visualization/perception/verify-point-cloud-alignment/) |
| Tune a 3D segmenter against the live view                          | [Vision services in the 3D scene](/visualization/perception/vision-services/)           |
| See what a camera or end effector sees from its mount              | [Frame POV](/visualization/3d-scene/3d-scene-widgets/#frame-pov)                        |
| Draw my module's own visuals in the scene                          | [Publish visuals from a module](/visualization/publish-visuals-from-a-module/)          |
| Preview spatial data from a Go script without deploying            | [Viam Visualization](/visualization/viam-visualization/)                                |
| Fix something that looks wrong                                     | [Troubleshoot the 3D scene](/visualization/troubleshoot-the-3d-scene/)                  |
