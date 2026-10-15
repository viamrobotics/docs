---
linkTitle: "Controls and settings"
title: "3D scene controls and settings"
weight: 90
layout: "docs"
type: "docs"
description: "Navigation, where to find keyboard shortcuts, Details panel fields and the configuration they map to, and importable files for the 3D scene."
capabilities: ["scene-3d"]
diataxis: reference
---

Look up 3D scene controls and settings here. For what the scene shows and what each mode is for, see [3D scene](/visualization/3d-scene/).

## Navigation

| Action                                 | Mouse             |
| -------------------------------------- | ----------------- |
| Orbit (rotate the view around a point) | Left-click drag   |
| Pan (slide the view without rotating)  | Right-click drag  |
| Zoom                                   | Scroll wheel      |
| Select an entity                       | Left-click        |
| Deselect                               | Click empty space |

On a trackpad, a two-finger swipe zooms, and pan needs a right-click held while dragging.

## Keyboard shortcuts

The scene has keyboard shortcuts for moving the camera, focusing on, hiding, and isolating entities, switching transform tools, and undoing, redoing, and saving Build mode edits. For the full, current list, open **Settings** > **Keybindings** in the scene.

Keyboard navigation pauses while you type in a field or hold `⌘` (or `Ctrl`).

## Details panel fields

The Details panel shows the selected entity's pose and geometry on its **Details** tab, and how it draws on its **Appearance** tab. Fields that correspond to frame configuration are editable in [Build mode](/visualization/3d-scene/build-mode/) for configurable frames, and read-only otherwise. In [Move mode](/visualization/3d-scene/move-mode/), the panel becomes the move controls instead.

| Field                                                       | Meaning                                                                        | Frame configuration                                                                                                                          |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **world position** (mm)                                     | The entity's position in the world frame                                       | None. Computed from the local pose and the parent chain                                                                                      |
| **world orientation**                                       | The entity's orientation in the world frame, as an orientation vector          | None. Computed                                                                                                                               |
| **parent frame**                                            | The frame this entity is attached to                                           | `frame.parent`                                                                                                                               |
| **local position** (mm)                                     | Position relative to the parent frame                                          | `frame.translation`                                                                                                                          |
| **local orientation**                                       | Orientation relative to the parent frame, entered as **OV (deg)** or **Euler** | `frame.orientation`, stored as an orientation vector in degrees whichever form you enter                                                     |
| **geometry**                                                | The collision geometry: `None`, `Box`, `Sphere`, or `Capsule`                  | `frame.geometry.type`                                                                                                                        |
| **dimensions** (mm)                                         | `x`, `y`, `z` for a box; `r` for a sphere; `r` and `l` for a capsule           | `frame.geometry` `x`, `y`, `z`, `r`, `l`                                                                                                     |
| **Appearance** tab: color, opacity, visibility, axes helper | How the entity draws in the scene                                              | In build mode, the component's `visualizer` field; **Reset appearance** removes it. In monitor mode, none: changes last only for the session |

The panel header can open a [frame POV widget](/visualization/3d-scene/3d-scene-widgets/#frame-pov) and copy the entity's pose and geometry as JSON. To center the camera on the selected entity, use the scene's focus control or its keyboard shortcut.

## Settings

**Settings** controls how the scene fetches and draws data, such as refresh rates, point cloud display, and which vision services render. Pages that rely on a particular setting name it where it matters. Toggle the rest to see what they do.

## Import files

Drag a file onto the viewport to add it to the scene:

| File type                | Loads as                                                                                                                                                                                                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `.pcd`                   | A point cloud                                                                                                                                                                                                                                                                  |
| `.ply`                   | A triangle mesh. A `.ply` file that holds only points draws as triangles, not points, so convert point clouds to `.pcd` first.                                                                                                                                                 |
| `.json`, `.pb`, `.pb.gz` | A scene snapshot. The file name must start with `visualization_snapshot`, or the scene rejects it as an unsupported file type. A snapshot can also set the camera's starting view. See [Viam Visualization](/visualization/viam-visualization/#save-and-load-scene-snapshots). |

Imported files are placed relative to the world frame.

To remove an imported file, select it and use **Remove from scene** in the Details panel header.
