---
linkTitle: "Edit frames visually"
title: "Edit frames visually"
weight: 50
layout: "docs"
type: "docs"
description: "Add, edit, and delete frames and geometries directly in the 3D scene instead of editing JSON configuration."
---

{{< alert title="Preview feature" color="note" >}}
Visual frame editing is currently behind a feature flag and may not be enabled for your organization.
The interface and behavior described here may change before general availability.
{{< /alert >}}

When visual frame editing is enabled, the 3D scene tab becomes a configuration tool: you can add frames to components, reposition them by editing coordinates in the details panel, change parent frames, and attach or modify geometry, all without editing JSON directly.
Changes you make in the 3D scene are written back to your machine's configuration and saved when you click **Save** in the app.

## Prerequisites

- Visual frame editing enabled for your organization (feature flag: `ENABLE_EDIT_FRAME_IN_VIZ_TAB`).
- A machine with at least one component configured.

## Add a frame to a component

Components that do not yet have a frame configured appear in the **Add frames** panel.

1. Open the 3D scene tab.
2. Look for the **Add frames** panel. It lists components that do not have frames.
3. Select a component from the dropdown.
4. Click **Add frame**.

The component appears in the scene at the world frame origin with default values (zero translation, identity orientation, no geometry).
You can then reposition it using the details panel.

## Edit a frame's position and orientation

1. Select the component in the tree view or by clicking it in the 3D viewport.
2. In the details panel, the **local position** and **local orientation** fields are editable input fields (rather than read-only values).
3. Edit the position values (x, y, z in mm) to set the translation relative to the parent frame.
4. Edit the orientation values (x, y, z, theta in degrees) to set the orientation as an orientation vector.

Changes appear immediately in the 3D viewport as you type.
The values you enter here correspond directly to the `translation` and `orientation` fields in the frame JSON configuration.

## Change a frame's parent

1. Select the component.
2. In the details panel, the **parent frame** field is a dropdown instead of a read-only label.
3. Select the new parent frame from the dropdown.

The component moves in the scene to reflect its new position relative to the new parent.
All children of this frame move with it.

## Add or change geometry

1. Select the component.
2. In the details panel, find the **geometry** section.
3. Click one of the geometry type buttons: **None**, **Box**, **Sphere**, or **Capsule**.
4. If you selected a geometry type, dimension fields appear:
   - **Box**: x, y, z dimensions in mm.
   - **Sphere**: radius (r) in mm.
   - **Capsule**: radius (r) and length (l) in mm.
5. Enter the dimensions. The geometry renders in the scene as you type.

To remove a geometry, click **None**.

## Delete a frame

1. Select the component.
2. In the details panel, click **Delete frame** at the bottom of the actions section.

This removes the frame configuration from the component.
The component disappears from the 3D scene but remains in your machine configuration (it just no longer has a spatial position in the frame system).

## Save your changes

Changes made in the 3D scene are held locally until you save.
The app shows an unsaved changes indicator when you have pending edits.
Click **Save** in the machine configuration header to write all changes to your machine's configuration.

If you navigate away without saving, your changes are lost.

## When to use visual editing

Visual frame editing is most useful when:

- You are setting up a new frame system and want to see the result as you go, rather than configuring JSON and then checking the 3D scene.
- You need to make small adjustments to frame positions and want immediate visual feedback.
- You are adding geometry to components and want to see whether the shapes cover the physical objects correctly.

For bulk configuration changes, complex orientation values, or frames that reference components on different machine parts, editing the JSON configuration directly may be more efficient.
