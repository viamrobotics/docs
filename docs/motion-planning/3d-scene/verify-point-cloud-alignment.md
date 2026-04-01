---
linkTitle: "Verify point cloud alignment"
title: "Verify point cloud alignment"
weight: 30
layout: "docs"
type: "docs"
description: "Display a depth camera's point cloud in the 3D scene to verify that the data aligns with your frame system and workspace geometry."
---

Depth cameras produce point clouds: sets of 3D points representing the surfaces visible to the camera.
The 3D scene tab can display these point clouds in the context of your frame system, so you can verify that the camera is producing good data and that the data aligns with your workspace geometry.

If the point cloud does not align with the physical objects in your workspace, either the camera's frame offset is wrong or the camera itself has a problem.
Catching this early prevents issues with vision pipelines, object detection, SLAM, and motion planning that depend on accurate spatial data.

## Prerequisites

- A machine with a depth camera configured and producing point cloud data.
- The camera must support the `GetPointCloud` method (check the camera's `supports_pcd` property).
- A frame configured for the camera with translation and orientation values that reflect its physical mounting position.

## Steps

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

### 3. Check spatial alignment

The point cloud renders in the scene positioned according to the camera's frame in your frame system.
If the frame configuration is correct, the point cloud should align with physical objects in your workspace:

- Flat surfaces (tables, walls) appear as planes of points at the correct height and position relative to other components.
- Objects appear as clusters of points at the expected distances from the camera.
- The floor should appear at the expected height relative to the world frame.

If the point cloud appears shifted, rotated, or in an unexpected location, the camera's frame offset or orientation is likely wrong.
See [Calibrate frame offsets](/motion-planning/3d-scene/calibrate-frame-offsets/).

### 4. Check data quality

If the point cloud is in the right place but the data looks wrong, look for common depth camera issues:

- **Gaps or holes**: areas where the camera cannot measure depth (reflective surfaces, transparent objects, surfaces at extreme angles).
- **Noise at edges**: depth values that jump between foreground and background at object boundaries.
- **Range limitations**: points missing beyond the camera's maximum depth range.
- **Sparse data**: too few points to be useful. Check the camera's resolution and depth mode settings.

Data quality problems are camera issues, not frame system issues.
Adjust the camera's configuration, mounting angle, or lighting conditions to address them.
