---
linkTitle: "Inspect point clouds"
title: "Inspect point clouds"
weight: 30
layout: "docs"
type: "docs"
description: "View live camera point clouds and imported PCD files in the 3D scene."
---

Depth cameras produce point clouds: sets of 3D points representing the surfaces visible to the camera.
The 3D scene tab can display these point clouds in the context of your frame system, so you can verify that the camera is producing good data and that the data aligns with your workspace geometry.

## Prerequisites

- A machine with a depth camera configured and producing point cloud data.
- The camera must support the `GetPointCloud` method (check the camera's `supports_pcd` property).

## View live point clouds

### 1. Open the 3D scene tab

Navigate to your machine in the [Viam app](https://app.viam.com) and click the **3D scene** tab.
Your machine must be online for live point cloud data.

### 2. Enable point cloud display

Open the settings panel (gear icon) and go to the **Pointclouds** tab.
You will see a list of cameras on your machine that support point clouds.
Enable the toggle for each camera you want to display.

You can also configure:

- **Point size**: how large each point renders in the scene. Increase this if points are hard to see; decrease it for denser clouds.
- **Default color**: the color used for points that do not have color data from the camera.

### 3. Interpret the point cloud

The point cloud renders in the scene positioned according to the camera's frame in your frame system.
If the frame configuration is correct, the point cloud should align with physical objects in your workspace:

- Flat surfaces (tables, walls) appear as planes of points.
- Objects appear as clusters of points at the expected distances from the camera.
- The floor should appear at the expected height relative to the world frame.

If the point cloud appears shifted, rotated, or in an unexpected location, the camera's frame offset or orientation is likely wrong.
See [Calibrate frame offsets](/motion-planning/3d-scene/calibrate-frame-offsets/).

### 4. Check point cloud quality

Look for common depth camera issues:

- **Gaps or holes**: areas where the camera cannot measure depth (reflective surfaces, transparent objects, surfaces at extreme angles).
- **Noise at edges**: depth values that jump between foreground and background at object boundaries.
- **Range limitations**: points missing beyond the camera's maximum depth range.
- **Sparse data**: too few points to be useful. Check the camera's resolution and depth mode settings.

## Import point cloud files

You can load saved point cloud data into the scene by dragging and dropping PCD or PLY files onto the 3D viewport.
Imported point clouds appear at the world frame origin.

This is useful for:

- Comparing a saved SLAM map against your current frame system.
- Loading a point cloud capture from a different session for offline analysis.
- Viewing point clouds exported from external tools.

## Select and export points

The lasso tool lets you select a region of points from any point cloud in the scene and export them.

1. Activate the lasso tool from the toolbar.
2. Hold Shift and drag to draw a freeform selection boundary around the points you want.
3. The selected points are highlighted.
4. Export the selection as a PCD file.

This is useful for isolating a specific region of a point cloud for further analysis or for creating a cropped point cloud to use in a different workflow.
