---
linkTitle: "Controls and settings"
title: "3D scene controls and settings"
weight: 90
layout: "docs"
type: "docs"
description: "Navigation and keyboard shortcuts, Details panel fields and the configuration they map to, settings, and importable files for the 3D scene."
capabilities: ["scene-3d"]
diataxis: reference
---

Look up 3D scene controls and settings here. For what the scene shows and what each mode is for, see [3D scene](/visualization/3d-scene/).

## Navigation

| Action                   | Mouse             | Keyboard              |
| ------------------------ | ----------------- | --------------------- |
| Orbit (rotate view)      | Left-click drag   | Arrow keys            |
| Pan                      | Right-click drag  |                       |
| Zoom                     | Scroll wheel      | `R` (in) / `F` (out)  |
| Strafe camera            |                   | `W`/`A`/`S`/`D`       |
| Select entity            | Left-click        |                       |
| Deselect                 | Click empty space |                       |
| Exit object view         |                   | `Escape`              |
| Toggle camera mode       |                   | `C`                   |
| Toggle entity visibility |                   | `H` (selected entity) |

Holding `⌘` (or `Ctrl`) disables keyboard navigation, which is useful when you are typing a value in the Details panel. `H` affects only the selected entity, so select an entity, in the viewport or its row in the **World** panel, before pressing it.

## Details panel fields

The Details panel shows the selected entity's pose and geometry on its **Details** tab, and how it draws on its **Appearance** tab. Fields that correspond to frame configuration are editable in [Build mode](/visualization/3d-scene/build-mode/) for configurable frames, and read-only otherwise. In [Move mode](/visualization/3d-scene/move-mode/), the panel becomes the move controls instead.

| Field                                           | Meaning                                                                        | Frame configuration                                                                      |
| ----------------------------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **world position** (mm)                         | The entity's position in the world frame                                       | None. Computed from the local pose and the parent chain                                  |
| **world orientation**                           | The entity's orientation in the world frame, as an orientation vector          | None. Computed                                                                           |
| **parent frame**                                | The frame this entity is attached to                                           | `frame.parent`                                                                           |
| **local position** (mm)                         | Position relative to the parent frame                                          | `frame.translation`                                                                      |
| **local orientation**                           | Orientation relative to the parent frame, entered as **OV (deg)** or **Euler** | `frame.orientation`, stored as an orientation vector in degrees whichever form you enter |
| **geometry**                                    | The collision geometry: `None`, `Box`, `Sphere`, or `Capsule`                  | `frame.geometry.type`                                                                    |
| **dimensions** (mm)                             | `x`, `y`, `z` for a box; `r` for a sphere; `r` and `l` for a capsule           | `frame.geometry` `x`, `y`, `z`, `r`, `l`                                                 |
| **Appearance** tab: color, opacity, axes helper | How the entity draws in the scene                                              | None. These change the rendering only, not the configuration                             |

The panel header can center the camera on the entity, open a [frame POV widget](/visualization/3d-scene/3d-scene-widgets/#frame-pov), and copy the entity's pose and geometry as JSON.

## Settings

Open **Settings** to change how the scene fetches and draws data. The settings other pages refer to:

- **Connection**: how often the scene fetches each data stream, such as poses, point clouds, and vision service results. A stream set to off never updates.
- **Scene**: the grid, object labels, hover tooltips, line thickness, and how arm models render (**Arm Models**).
- **Pointclouds**: the default point size and color, and which cameras' point clouds draw (**Enabled cameras**). Cameras that don't support point clouds are turned off.
- **Vision**: which vision services' results draw in the scene.

## Import files

Drag a file onto the viewport to add it to the scene:

| File type | Loads as                                                                                                                                                             |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.pcd`    | A point cloud                                                                                                                                                        |
| `.ply`    | A point cloud                                                                                                                                                        |
| `.json`   | A scene snapshot. The file name must start with `visualization_snapshot`. See [Viam Visualization](/visualization/viam-visualization/#save-and-load-scene-snapshots) |

To remove an imported file, select it and use **Remove from scene** in the Details panel header.
