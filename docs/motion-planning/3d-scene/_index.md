---
linkTitle: "3D scene"
title: "3D scene"
weight: 50
layout: "docs"
type: "docs"
no_list: true
description: "Visualize your machine's frame system, geometries, and point clouds in an interactive 3D view."
---

The **3D scene** tab on your machine's page in the [Viam app](https://app.viam.com) renders your machine's frame system as an interactive 3D visualization.
You can inspect how components are positioned relative to each other, verify that obstacle geometry covers your workspace correctly, view live point clouds from depth cameras, and measure distances between points in the scene.

The 3D scene tab reads your machine's configuration and, when the machine is online, connects to it for live data.
Everything you see in the scene maps directly to your frame system configuration: each component's frame appears as a set of coordinate axes positioned according to its translation and orientation relative to its parent frame.

## The interface

The 3D scene tab has four main areas:

**3D viewport** (center): The main rendering area.
You can orbit, pan, and zoom to view your frame system from any angle.
Components appear as labeled coordinate axes, with attached geometries rendered as translucent shapes.
Point clouds from cameras render as colored point sets.
An XY grid provides spatial reference.

**World panel** (floating, upper-left): A hierarchical list of every entity in the scene, titled **World**.
The panel is always visible (it has no close button) but is draggable and resizable.
The root node `World` mirrors your machine's world frame.
Each row shows an expand caret, the entity name, and an eye toggle (click the eye, or select the row and press `H`, to hide or show that entity).
Click a row to select the entity; its details appear in the Details panel.

**Details panel** (floating, upper-right): Shows the selected entity's spatial properties.
The panel is draggable and anchors to the top-right of the viewport by default.
It includes:

- **world position** (mm) and **world orientation** (deg, as an orientation vector `x / y / z / th`): the entity's absolute pose in the world frame. Read-only.
- **parent frame**: which frame this entity is a child of. Editable when the entity is a configurable frame.
- **local position** (mm) and **local orientation** (deg): pose relative to the parent frame. Editable for configurable frames; these correspond to the `translation` and `orientation` in your frame configuration.
- **geometry**: four buttons (`None` / `Box` / `Sphere` / `Capsule`) plus **dimensions** (`x / y / z` for Box, `r / l` for Capsule, `r` for Sphere, all in mm).

The panel header includes a **Zoom to object** button (centers the camera on the selected entity) and a copy-to-clipboard button next to the `Details` heading that exports the entity's pose and geometry as JSON.
Entities that can be removed (for example, dropped PCD files) also show a **Remove from scene** button in the header.

**Dashboard toolbar** (top-center): Visible buttons, left to right:

- **Orthographic / Perspective** toggle — switch between an orthographic view (no foreshortening) and a perspective view. Keyboard: `C`.
- **Add frames** — opens a floating panel listing components that do not yet have a frame; click a component and then **Add frame** (singular) to attach a default frame to it. See [Edit frames visually](/motion-planning/3d-scene/edit-frames/).
- **Measurement** (ruler icon) — activate to measure distance between two points you pick in the viewport. Click the icon again to clear.
- **Measurement settings** (sliders icon next to the ruler) — toggle `x`, `y`, or `z` under **Enabled axes** to constrain the second point to the enabled axes of the first.
- **Logs** — shows a count badge for errors/warnings from the scene renderer.
- **Settings** (gear icon) — opens the Settings panel.

## Navigation controls

| Action                   | Mouse             | Keyboard             |
| ------------------------ | ----------------- | -------------------- |
| Orbit (rotate view)      | Left-click drag   | Arrow keys           |
| Pan                      | Right-click drag  |                      |
| Zoom                     | Scroll wheel      | `R` (in) / `F` (out) |
| Strafe camera            |                   | `W`/`A`/`S`/`D`      |
| Select entity            | Left-click        |                      |
| Deselect                 | Click empty space | `Escape`             |
| Toggle camera mode       |                   | `C`                  |
| Toggle entity visibility |                   | `H`                  |

Holding `⌘` (or `Ctrl`) disables keyboard navigation, which is useful when you are editing a value in the Details panel.

## Settings

Click the gear icon to open the settings panel.
Settings are organized into tabs:

- **Connection**: polling rates for the scene's data streams.
- **Scene**: toggle the grid, **Object labels**, hover detail tooltips, arm-model rendering (`Arm Models`), and line thickness.
- **Pointclouds**: set default point size and color, and enable or disable point cloud display per camera under **Enabled cameras**.
- **Vision**: enable or disable vision-service point-cloud entities.
- **Widgets**: show or hide the **Arm positions** widget and per-camera **Camera widgets** (a live camera feed floating alongside the 3D view).
- **Stats**: performance counters.
- **Weblabs**: feature-flag overrides (usually empty).
- **VR / AR**: only visible when the browser supports WebXR.

## File import

You can drag and drop `.pcd`, `.ply`, or `.json` (scene snapshot) files directly onto the 3D viewport to load external data into the scene.
This is useful for loading saved SLAM maps or point cloud captures for comparison with your live frame system.

## How-to guides

{{< cards >}}
{{% card link="/motion-planning/3d-scene/debug-motion-plan/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/calibrate-frame-offsets/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/verify-point-cloud-alignment/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/set-up-obstacle-avoidance/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/edit-frames/" noimage="true" %}}
{{< /cards >}}
