---
linkTitle: "Monitor mode"
title: "Monitor mode"
weight: 10
layout: "docs"
type: "docs"
description: "Watch your machine's live state in the 3D scene and read any frame's pose."
capabilities: ["scene-3d", "motion-planning"]
diataxis: explanation
---

Monitor mode shows your machine as it is: its frames, its configured geometry, and, when the machine is online, live poses, point clouds, and custom visuals. Nothing in Monitor mode changes your machine or its configuration, so it's the safe place to look around.

## Live and configured state

What the scene shows depends on whether the machine is online:

- **Online**: component poses, point clouds, and custom visuals update as the machine runs.
- **Offline**: the scene shows only the saved configuration, with every component at its configured pose. Point clouds and custom visuals are absent.

The scene fetches each kind of live data at its own rate, which you set under **Settings** > **Connection**. A data stream set to off never updates, so check these rates when part of the scene seems frozen. For other reasons a scene can look wrong, see [Troubleshoot the 3D scene](/visualization/troubleshoot-the-3d-scene/).

## Read a frame's pose

Select any entity, in the viewport or in the **World** panel, to see its pose in the Details panel: its **world position** and **world orientation**, its **parent frame**, and its **local position** and **local orientation** relative to that parent. In Monitor mode these fields are read-only. To change them, use [Build mode](/visualization/3d-scene/build-mode/).

To read where an arm's end effector is, expand the arm in the **World** panel and select its last link or the frame attached to it, such as a gripper. For the meaning of each field, see [3D scene controls and settings](/visualization/3d-scene/controls-and-settings/#details-panel-fields).

## What's next

- [Move mode](/visualization/3d-scene/move-mode/): plan and run a move from the scene.
- [Replay mode](/visualization/3d-scene/replay-mode/): step through saved motion plans.
- [Visualize a motion plan](/motion-planning/visualize-a-motion-plan/): publish a plan as custom visuals to keep it live while the machine runs.
- [Troubleshoot the 3D scene](/visualization/troubleshoot-the-3d-scene/): trace a wrong or missing element to its source.
