---
linkTitle: "Visualization"
title: "Visualization"
weight: 165
layout: "docs"
type: "docs"
no_list: true
description: "See your machine in 3D: frames, geometries, point clouds, and custom visuals your modules publish."
---

Spatial configuration is invisible in JSON. A frame translation of
`{x: 50, y: 0, z: 110}` tells you nothing about whether the gripper actually
sits where the arm needs it, and a list of obstacle geometries tells you nothing
about whether they cover the real workspace. Visualization renders these in 3D
so you can see the spatial model your machine is actually working with, catch
misconfigurations before they cause a failure, and watch live data in context.

This section covers the **3D SCENE** tab in the Viam app, the transforms and
metadata that make up a custom visual, how a module publishes visuals, and the
standalone Viam Visualization app for previewing spatial data outside the app.

## What the 3D scene renders

The **3D SCENE** tab on your machine's page renders an interactive 3D view of
your machine. It draws four kinds of content, each from a different source:

- **Component frames**, from the [frame system](#the-frame-system). Each
  configured component appears as a set of coordinate axes at its computed
  position.
- **Geometries**, from the components' `frame.geometry` configuration and from
  obstacles. These render as translucent shapes the motion planner uses for
  collision checking.
- **Point clouds**, from depth cameras, rendered as colored point sets.
- **Custom visuals**, from a [world state store service](/visualization/publish-visuals-from-a-module/).
  A module publishes these at runtime, and the scene streams them in as they
  change.

The scene reads your saved configuration, and when the machine is online it
connects for live data, so frames move to their current poses and point clouds
update as the cameras report them.

## The frame system

Everything in the scene is positioned by the **frame system**: the single
coordinate tree that records where every component sits relative to every other.

Each component has a frame with a parent, a translation, and an orientation.
A component's frame is defined relative to its parent's frame, not to the world
directly, so the frames form a tree rooted at the fixed **world frame**. A
gripper's frame is a child of the arm's, the arm's is a child of the world, and
so on. Because the tree is connected, the frame system can compute the transform
between any two frames: it walks the path between them, composing each frame's
local transform along the way. When the arm's joints move, every frame below it
in the tree moves with it automatically.

This is what makes the scene meaningful. A point cloud from a wrist camera and an
obstacle defined in world coordinates can be drawn in the same view because the
frame system relates both back to the world frame. The same machinery lets the
motion planner reason about where the gripper is while the arm moves, and lets a
custom visual attach itself to a moving component.

For configuring frames in detail (parent, translation, orientation, geometry),
see the [frame system documentation](/motion-planning/frame-system/).

## Built-in content versus custom visuals

Two kinds of content reach the scene by two different routes, and the difference
determines where you change them:

- **Built-in content** (component frames and configured geometry) comes from
  your machine **configuration**. You change it by editing the frame system and
  obstacle config. The scene reads it directly.
- **Custom visuals** come from a **module** that implements a world state store
  service and publishes transforms at runtime. You change them in **code**, not
  config, and the scene streams them in as the module adds, updates, and removes
  them.

If a frame or geometry looks wrong, fix the configuration. If a custom visual
looks wrong, the module that publishes it is where to look.

## Topics

{{< cards >}}
{{% card link="/visualization/visuals-and-collisions/" noimage="true" %}}
{{% card link="/visualization/publish-visuals-from-a-module/" noimage="true" %}}
{{% card link="/visualization/drawing-library/" noimage="true" %}}
{{< /cards >}}

## Use the 3D scene with motion planning

{{< cards >}}
{{% card link="/motion-planning/3d-scene/set-up-obstacle-avoidance/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/debug-motion-plan/" noimage="true" %}}
{{< /cards >}}
