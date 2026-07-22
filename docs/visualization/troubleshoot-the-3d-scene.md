---
linkTitle: "Troubleshoot the 3D scene"
title: "Troubleshoot the 3D scene"
weight: 80
layout: "docs"
type: "docs"
description: "Trace a wrong or missing element in the 3D scene to its source: the machine configuration, a module, or the connection."
---

Every element in the 3D scene comes from one of three layers: the machine's saved
configuration (frames and geometry), a module publishing at runtime (custom visuals and
point clouds), or the live connection that streams poses and data. When something looks
wrong, identify the layer first; the fix lives there, and edits to the wrong layer waste
time.

## Read the scene's own signals first

Three signals tell you what the scene is receiving before you change anything:

- **Online state.** An offline machine renders the saved frame configuration only, with
  every component at its configured pose. Live poses, point clouds, and custom visuals
  need the machine online and connected.
- **The Logs button** in the top-center toolbar shows a count of renderer errors and
  warnings. A nonzero badge means the scene received data it could not draw; open it and
  read the message before assuming data is missing.
- **Polling rates** under **Settings** > **Connection** control how often the scene
  fetches each data stream. A stream set to off explains a layer that never updates.

## A frame or geometry is in the wrong place

Frames and configured geometry come from the machine configuration, so a misplaced one
is a configuration problem. Select the entity in the **World** panel and compare its
**local position** and **parent frame** to your physical measurements. Then fix the
values in the configuration or
[edit the frame in the scene](/visualization/3d-scene/editing-frames-visually/).
For the full checklist of frame and obstacle checks, see
[Debug a motion plan](/motion-planning/debug-motion-plan/).

## A point cloud is missing

Work down the camera pipeline:

1. The camera's toggle is on under **Settings** > **Pointclouds** > **Enabled cameras**.
2. The camera supports point clouds. A camera that reports `supports_pcd=false` is
   auto-disabled in that list; check its module documentation.
3. The camera's frame is configured. A point cloud renders at its camera's frame, so a
   camera with no frame has nowhere to draw.

A point cloud that renders in the wrong place, rather than missing, is a frame problem:
see [Verify point cloud alignment](/visualization/perception/verify-point-cloud-alignment/).

## A custom visual is missing or stale

Custom visuals come from a module through a
[world state store service](/reference/apis/services/world-state-store/), so a missing or
stale one is a module problem. Check the module's output at the service boundary:

1. `ListUUIDs` returns the visual's UUID. An empty list means the module publishes
   nothing; check the module's logs and its dependencies.
2. The module emits a change event when the data changes. A visual that appears once and
   never moves usually means the poll loop stopped or emits no `TransformChange` events.
3. The UUID is stable across updates. A module that generates a fresh UUID each tick
   piles up duplicates instead of updating one visual.

The implementation side of these checks is covered in
[Publish visuals from a module](/visualization/publish-visuals-from-a-module/).

## Know what the scene can tell you

Match your conclusion to what the scene renders:

- **Machine offline**: trust the frame tree and configured geometry; treat every pose as
  the configured default, and expect point clouds, live poses, and custom visuals to be
  absent.
- **Machine online**: poses, point clouds, and custom visuals are live, subject to the
  polling rates you set.

A plan's obstacles are a separate case: `WorldState` obstacles passed to a single `Move`
call are planner input for that request and are never drawn. To see them, publish the
same geometry as a custom visual; see
[Visuals and collisions](/visualization/visuals-and-collisions/).

## What's next

- [Debug a motion plan](/motion-planning/debug-motion-plan/): the frame, obstacle, and
  reach checks for planning failures.
- [Publish visuals from a module](/visualization/publish-visuals-from-a-module/): the
  service methods and poll loop behind custom visuals.
- [The 3D scene interface](/visualization/3d-scene/the-3d-scene-interface/): every
  panel, setting, and toolbar button.
