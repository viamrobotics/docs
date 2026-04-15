---
linkTitle: "3D scene"
title: "3D scene"
weight: 70
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

**Tree view** (left sidebar): A hierarchical list of every entity in the scene, matching your frame system's parent-child structure.
Click an entity to select it.
The tree shows the same hierarchy you configured: world frame at the root, with components nested under their parent frames.

**Details panel** (right, appears when you select an entity): Shows the selected entity's spatial properties:

- **World position** (mm) and **world orientation** (degrees): the entity's absolute position and orientation in the world frame.
- **Parent frame**: which frame this entity is a child of.
- **Local position** (mm) and **local orientation** (degrees): position and orientation relative to the parent frame. These correspond directly to the `translation` and `orientation` values in your frame configuration.
- **Geometry**: type (box, sphere, or capsule) and dimensions in mm, if a geometry is attached.

The details panel also has a **copy** button that exports the full pose and geometry data as JSON, and a **zoom to object** button that centers the camera on the selected entity.

**Toolbar** (top): Controls for camera mode, transform tools, and specialized tools:

- **Perspective/Orthographic toggle** (`C`): switch between perspective view (depth perception) and orthographic view (no foreshortening, useful for checking alignment).

## Navigation controls

| Action                   | Mouse             | Keyboard             |
| ------------------------ | ----------------- | -------------------- |
| Orbit (rotate view)      | Right-click drag  | Arrow keys           |
| Pan                      | Middle-click drag |                      |
| Zoom                     | Scroll wheel      | `R` (in) / `F` (out) |
| Move camera              |                   | `W`/`A`/`S`/`D`      |
| Select entity            | Left-click        |                      |
| Deselect                 | Click empty space | `Escape`             |
| Toggle camera mode       |                   | `C`                  |
| Toggle entity visibility |                   | `H`                  |

## Settings

Click the gear icon to open the settings panel.
Settings are organized into tabs:

- **Pointclouds**: set default point size and color, enable or disable point cloud display per camera.
- **Scene**: toggle the grid, axis labels, hover detail tooltips, and line thickness.
- **Widgets**: show or hide the floating camera feed and arm position widgets.

The **camera widget** displays a live camera feed from a selected robot camera alongside the 3D view.
The **arm positions widget** shows current joint angles and end-effector pose for arm components.

## File import

You can drag and drop PCD or PLY files directly onto the 3D viewport to load external point cloud data into the scene.
This is useful for loading saved SLAM maps or point cloud captures for comparison with your live frame system.

## How-to guides

{{< cards >}}
{{% card link="/motion-planning/3d-scene/debug-motion-plan/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/calibrate-frame-offsets/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/verify-point-cloud-alignment/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/set-up-obstacle-avoidance/" noimage="true" %}}
{{% card link="/motion-planning/3d-scene/edit-frames/" noimage="true" %}}
{{< /cards >}}
