---
linkTitle: "Edit frames visually"
title: "Edit frames visually"
weight: 50
layout: "docs"
type: "docs"
description: "Add, edit, and attach geometry to frames directly in the 3D scene instead of editing JSON configuration."
---

The 3D scene tab can serve as a configuration tool: you can add frames to components, reposition them by editing coordinates in the Details panel, change parent frames, and attach or modify geometry, all without editing JSON directly.
Changes you make in the 3D scene are written back to your machine's configuration. The app surfaces an unsaved-changes banner on the CONFIGURE tab, and you save from there with **Save** or `⌘/Ctrl+S`.

## Prerequisites

- A machine with at least one component configured.

## Add a frame to a component

1. Open the 3D scene tab.
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

Changes flow back to the machine configuration. The CONFIGURE tab shows an unsaved-changes banner with a **Save** button; click it (or press `⌘/Ctrl+S` on the CONFIGURE tab) to persist the edits.

If you navigate away without saving, your changes are lost.

To delete a frame, remove it from the component's configuration on the CONFIGURE tab (there is no **Delete frame** button in the embedded 3D scene tab).

## When to use visual editing

Visual frame editing is most useful when:

- You are setting up a new frame system and want to see the result as you go, rather than configuring JSON and then checking the 3D scene.
- You need to make small adjustments to frame positions and want immediate visual feedback.
- You are adding geometry to components and want to see whether the shapes cover the physical objects correctly.

For bulk configuration changes, complex orientation values, or frames that reference components on different machine parts, editing the JSON configuration directly may be more efficient.
