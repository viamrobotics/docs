---
linkTitle: "3D scene"
title: "Visualizing with the 3D scene"
weight: 5
layout: "docs"
type: "docs"
description: "What the 3D scene renders, where each element comes from, and how built-in configuration content differs from custom visuals a module publishes at runtime."
aliases:
  - /visualization/visualizing-with-the-3d-scene/
  - /visualization/3d-scene-tools/
  - /motion-planning/3d-scene/
---

The **3D SCENE** tab renders your machine in an interactive 3D view: the frames of every
component, the geometry attached to them, point clouds from depth cameras, and any custom
visuals a module publishes while the machine runs. It turns configuration you would
otherwise read as JSON numbers into a picture you can inspect, so you can confirm a gripper
sits where the arm expects it or watch a motion plan against the obstacles around it.

This page describes what the scene shows, where each element comes from, and how the scene
stays current. For the tab's panels, navigation, and settings, see
[The 3D scene interface](/visualization/3d-scene/the-3d-scene-interface/).

## What the scene renders

The scene draws four kinds of element, each with its own appearance:

- **Component frames** render as sets of red, green, and blue coordinate axes, one per
  component, positioned by each frame's translation and orientation.
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

## What's next

{{< cards >}}
{{% card link="/visualization/3d-scene/the-3d-scene-interface/" noimage="true" %}}
{{% card link="/visualization/3d-scene/measuring-between-frames/" noimage="true" %}}
{{% card link="/visualization/3d-scene/editing-frames-visually/" noimage="true" %}}
{{% card link="/visualization/3d-scene/3d-scene-widgets/" noimage="true" %}}
{{% card link="/visualization/visuals-and-collisions/" noimage="true" %}}
{{% card link="/visualization/publish-visuals-from-a-module/" noimage="true" %}}
{{< /cards >}}
