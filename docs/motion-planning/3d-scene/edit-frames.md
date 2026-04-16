---
linkTitle: "Edit frames visually"
title: "Edit frames visually"
weight: 50
layout: "docs"
type: "docs"
description: "Add, edit, and attach geometry to frames directly in the 3D scene instead of editing JSON configuration."
---

The **3D SCENE** tab can serve as a configuration editor: you can add, move, re-parent, and reshape frames without writing JSON.

Visual editing is most useful while you are still figuring out where things go. Typing coordinates into JSON and reloading the 3D view to check them is slow; editing in the viewport and seeing the result immediately is faster. The trade-off is that the visual editor writes the same JSON fields through a smaller surface area, so it is less suited to bulk changes or cross-machine-part frames. Changes flow back to the machine configuration, and the app surfaces an unsaved-changes banner on the CONFIGURE tab where you save them with **Save** or `⌘/Ctrl+S`.

## Prerequisites

- A machine with at least one component configured.

## Add a frame to a component

1. Open the **3D SCENE** tab.
2. Click the **Add frames** button (axis-arrow icon) in the top-center toolbar. A floating panel opens listing components that do not yet have a frame.
3. Select a component from the dropdown.
4. Click **Add frame** (singular) inside the panel.

The component appears in the scene at the world frame origin with default values (zero translation, identity orientation, no geometry).
You can then reposition it using the Details panel.

## Edit a frame's position and orientation

1. Select the component in the **World** panel on the upper-left, or by clicking it in the 3D viewport.
2. The Details panel (upper-right) shows the entity's current values. There is no edit-mode toggle; for any configurable frame, the **local position** and **local orientation** fields are editable inputs.
3. Edit the position values (`x`, `y`, `z` in mm) to set the translation relative to the parent frame.
4. Edit the orientation values (`x`, `y`, `z`, `th` in degrees) to set the orientation as an orientation vector.

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
2. In the Details panel, find the **geometry** row (four buttons: `None`, `Box`, `Sphere`, `Capsule`).
3. Click a geometry type.
4. **Dimensions** fields appear below:
   - **Box**: `x`, `y`, `z` in mm.
   - **Sphere**: `r` (radius) in mm.
   - **Capsule**: `r` (radius) and `l` (length) in mm.
5. Enter the dimensions. The geometry renders in the scene as you type.

To remove a geometry, click **None**.

## Save your changes

Edits are held locally until you save. The CONFIGURE tab shows an unsaved-changes banner with a **Save** button; click it (or press `⌘/Ctrl+S` on the CONFIGURE tab) to commit them. If you navigate away first, the edits are lost.

To delete a frame, remove it from the component's configuration on the CONFIGURE tab (there is no **Delete frame** button in the embedded **3D SCENE** tab).

## When to edit JSON instead

Visual editing covers most cases, but a few are faster in JSON:

- **Bulk changes** (renaming many frames, regenerating a layout) — JSON
  edits are easier in a text editor.
- **Frames that reference components on a different machine part** —
  the visual editor's parent dropdown only shows local frames.
- **Complex orientations** (rotations expressed in `axis_angles` or
  `quaternion` rather than `ov_degrees`) — the visual editor surfaces
  only the orientation vector form.
