---
linkTitle: "Editing frames visually"
title: "Editing frames visually"
weight: 30
layout: "docs"
type: "docs"
description: "Add, edit, and attach geometry to frames directly in the 3D scene."
aliases:
  - /motion-planning/3d-scene/edit-frames/
  - /visualization/3d-scene-tools/editing-frames-visually/
---

The **3D SCENE** tab can serve as a configuration editor: you can add, move, re-parent, and reshape frames without writing JSON.

Visual editing is most useful while you are still figuring out where things go. Edits render in the viewport as you type, so you can position a frame by eye and read off the values. The trade-off is that the visual editor edits only a subset of the frame JSON (parent, translation, orientation, and a single geometry), so it is less suited to bulk changes or cross-machine-part frames. Changes flow back to the machine configuration, and you save them from the 3D scene itself with **Save** or `⌘/Ctrl+S`.

## Prerequisites

- A machine with at least one component configured.
- Permission to edit the machine's configuration. Without it, the scene stays read-only.

## Switch to build mode

The tab opens in **Monitor** mode, which watches live data and keeps every field read-only. Editing lives in **Build** mode: click **Build** (hammer icon) in the mode toggle at the top right.

Build mode pauses live updates so the poses you edit hold still, and a **Live updates paused** banner appears with **Undo** and **Redo** buttons for stepping back through your frame edits. Switch back to **Monitor** to resume live data.

## Add a frame to a component

1. Open the **3D SCENE** tab and switch to build mode.
2. Click the **Add frames** button (axis-arrow icon) in the top-center toolbar. A floating panel opens listing components that do not yet have a frame.
3. Select a component from the dropdown.
4. Click **Add frame** (singular) inside the panel.

The component appears in the scene at the world frame origin with default values (zero translation, identity orientation, no geometry).
You can then reposition it using the Details panel.

## Edit a frame's position and orientation

1. Select the component in the **World** panel on the upper-left, or by clicking it in the 3D viewport.
2. The Details panel (upper-right) shows the entity's current values. In build mode, the **local position** and **local orientation** fields of any configurable frame are editable inputs.
3. Edit the position values (`x`, `y`, `z` in mm) to set the translation relative to the parent frame.
4. Edit the orientation values. The **OV (deg)** tab takes an orientation vector (`x`, `y`, `z` unit-vector components and `th` in degrees); the **Euler** tab takes roll, pitch, and yaw. Either way, the frame JSON stores an orientation vector.

Changes appear immediately in the 3D viewport as you type.
The values you enter here correspond directly to the `translation` and `orientation` fields in the frame JSON configuration.

The **world position** and **world orientation** fields remain read-only; they are computed from the local pose plus the parent chain.

## Change a frame's parent

1. Select the component.
2. In the Details panel, click the **parent frame** dropdown.
3. Select the new parent frame from the list.

The component moves in the scene to reflect its new position relative to the new parent.
All children of this frame move with it.

## Add or change geometry

1. Select the component.
2. In the Details panel, find the **geometry** row, which has a tab per type: `None`, `Box`, `Sphere`, `Capsule`.
3. Select a geometry type.
4. **Dimensions** fields appear below:
   - **Box**: `x`, `y`, `z` in mm.
   - **Sphere**: `r` (radius) in mm.
   - **Capsule**: `r` (radius) and `l` (length) in mm.
5. Enter the dimensions. The geometry renders in the scene as you type.

To remove a geometry, click **None**.

## Save your changes

Edits are held locally until you save. The **Save** button in the machine's header shows unsaved changes and works from the 3D scene, so you do not have to leave the tab; `⌘/Ctrl+S` saves as well. If you navigate away first, the edits are lost.

To delete a frame, remove it from the component's configuration on the CONFIGURE tab (there is no **Delete frame** button in the embedded **3D SCENE** tab).

## Edit frames with AI

The **3D SCENE** tab includes an AI scene builder that lets you edit frames using natural language instead of entering values manually.
Type a prompt describing the change you want, and the AI interprets your request and applies the frame updates to the scene.

You can use natural language to:

- Move components ("move the camera 50 mm to the left")
- Rotate components ("rotate the gripper 90 degrees around the z-axis")
- Re-parent frames ("attach the sensor to the arm instead of the base")
- Add, resize, or change collision geometry ("add a 100 mm box to the sensor", "make the arm's capsule wider")

The AI edits only the frames of existing components.
It cannot add new components to or remove components from the machine configuration.

After the AI applies changes, save or discard buttons appear in the **3D SCENE** tab.

## When to edit JSON instead

Visual editing covers most cases, but a few are faster in JSON:

- **Bulk changes** (renaming many frames, regenerating a layout): JSON
  edits are easier in a text editor.
- **Frames that reference components on a different machine part**:
  the visual editor's parent dropdown only shows local frames.
- **Complex orientations** (rotations expressed in `axis_angles` or
  `quaternion` rather than `ov_degrees`): the visual editor shows
  only the orientation vector form.
