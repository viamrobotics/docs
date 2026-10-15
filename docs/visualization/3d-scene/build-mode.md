---
linkTitle: "Build mode"
title: "Build mode"
weight: 20
layout: "docs"
type: "docs"
description: "Edit frames and geometry in the 3D scene, add obstacles, and save the changes to your machine's configuration."
capabilities: ["scene-3d", "frame-system"]
diataxis: explanation
---

Build mode turns the 3D scene into a configuration editor. You can give components frames, move and re-parent them, attach geometry, and add obstacles, and see each change in the scene as you make it. When you save, your edits become part of the machine's configuration, the same configuration you would otherwise edit as JSON.

## What changes in Build mode

- **The Details panel becomes editable** for configurable frames: the parent frame, local position and orientation, and geometry. For what each field maps to in configuration, see [Details panel fields](/visualization/3d-scene/controls-and-settings/#details-panel-fields).
- **Transform tools appear**, so you can move, rotate, and scale a frame's geometry in the viewport instead of typing values, with optional snapping and a choice of local or world axes.
- **Appearance changes are saved.** Color, opacity, visibility, and the axes helper you set on the Details panel's **Appearance** tab are saved to the component's `visualizer` configuration, and frames inside it, such as an obstacle's shapes, follow them unless they set their own. In Monitor mode, the same changes last only for the session.
- **An editing banner appears** with **Undo** and **Redo** for stepping through your edits, and shows whether you have unsaved changes.

## Add frames and obstacles

Components that don't have a frame yet appear in the **World** panel under **Frameless components**. Select one and choose **Add frame** to place it in the scene at the world origin. You can't remove a frame from the scene; see [What Build mode doesn't cover](#what-build-mode-doesnt-cover).

To model a fixed obstacle, such as a wall or a table, use the **+** button in the **World** panel, choose **Obstacle**, and pick a type: **Simple** (a single shape), **Bounds** (walls enclosing a box-shaped space), or **Complex** (a group of shapes). It adds a generic component with the built-in `obstacle` model (`rdk:builtin:obstacle`, `viam-server` v1.12.0 or later) as an unsaved edit, with its shapes in the component's `geometries` attribute. Move it like any other frame, edit its shapes in the Details panel, then save. For step-by-step instructions, see [Add an obstacle](/visualization/3d-scene/editing-frames-visually/#add-an-obstacle). The motion planner avoids its geometry like any other obstacle in your frame system. For other ways to define obstacles, see [Define obstacles](/motion-planning/obstacles/).

## Save your edits

Edits stay local until you save. Save or discard them from the machine's header, as you would any configuration change, without leaving the tab.

## Edit frames with AI

The **LLM Scene Builder** takes a prompt describing a change to a frame or its geometry, such as "move the arm 200 mm forward and rotate it 90 degrees left" or "make wall-2 wider to reach the edge of the floor", and proposes the change as a list of fields with their old and new values. Apply the proposal to add it to your edits, then save or discard it like any other edit.

## What Build mode doesn't cover

Build mode edits a subset of frame configuration: the parent, translation, orientation, and a single geometry (or, for an obstacle, its list of shapes). Edit the JSON instead for:

- Bulk changes, such as renaming many frames.
- Orientations you want to keep as axis angles, quaternions, or Euler angles. Build mode displays any orientation, but saving any change to a frame rewrites its orientation as an orientation vector in degrees (`ov_degrees`).
- Deleting a frame. Remove it from the component's configuration on the **CONFIGURE** tab.

## What's next

- [Editing frames visually](/visualization/3d-scene/editing-frames-visually/): add a frame, set its pose, and attach geometry, step by step.
- [Measuring between frames](/visualization/3d-scene/measuring-between-frames/): check your frames against physical measurements.
- [Frame system](/motion-planning/frame-system/): how frames fit together and how the motion planner uses them.
