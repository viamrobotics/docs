---
linkTitle: "Verify point cloud alignment"
title: "Verify point cloud alignment"
weight: 30
layout: "docs"
type: "docs"
description: "Display a depth camera's point cloud in the 3D scene to verify that the data aligns with your frame system and workspace geometry."
aliases:
  - /motion-planning/3d-scene/inspect-point-clouds/
---

Depth cameras produce point clouds: sets of 3D points that represent the surfaces the camera sees. The **3D SCENE** tab renders those points in your frame system, so you can check two things at once: the camera is producing usable data, and the data lines up with the rest of the workspace.

Misalignment usually means one of two things: the camera's frame offset is wrong, or the camera itself has a problem. Finding that out now, before a motion plan runs or an ML detector ships, costs minutes; finding it out later costs a day of debugging a downstream pipeline.

## Prerequisites

- A machine with a depth camera configured and producing point cloud data.
- The camera must support the `GetPointCloud` method (check the camera's `supports_pcd` property).
- A frame configured for the camera with translation and orientation values that reflect its physical mounting position.

## Steps

### 1. Open the 3D SCENE tab

Navigate to your machine in the [Viam app](https://app.viam.com) and click the **3D SCENE** tab.
Your machine must be online for live point cloud data.

### 2. Enable point cloud display

Open the settings panel (gear icon) and go to the **Pointclouds** tab.

Under **Enabled cameras**, you see a list of every camera on your machine. Cameras that report `supports_pcd=false` from `GetProperties` are auto-toggled off and cannot stream point clouds through this tab. If a camera you expect to stream is missing from the list, confirm its module supports PCD; if it is there but off, toggle it on.

You can also configure:

- **Default point size**: how large each point renders in the scene. Increase this if points are hard to see; decrease it for denser clouds.
- **Default point color**: the color used for points that do not have color data from the camera.

### 3. Check spatial alignment

The point cloud sits wherever the camera's frame puts it. If the frame configuration is right, three things line up:

- Flat surfaces (tables, walls) appear as planes at the correct height and position relative to other components.
- Objects appear as clusters at the expected distances from the camera.
- The floor appears at the expected height relative to the world frame.

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

## What's next

The motion planner does not consume raw point clouds directly: a vision
service with a 3D segmenter (such as the
[`obstacles_pointcloud` module](https://app.viam.com/module/viam/obstacles-pointcloud))
turns point clouds into bounded 3D objects, and you feed those to the
planner.

- [Pick an object](/motion-planning/pick-and-place/pick-an-object/):
  uses `GetObjectPointClouds` to localize the target the arm should
  grasp on a single `Move` call.
- [Define obstacles](/motion-planning/obstacles/): the geometry types
  the motion planner accepts, including the
  [`WorldState.obstacles`](/motion-planning/obstacles/#3-define-obstacles-programmatically-with-worldstate)
  pattern for per-call dynamic obstacles.
- [ObstacleDetector](/motion-planning/reference/motion-configuration/#obstacledetector):
  configures the motion service to poll a vision service during
  `MoveOnMap` and `MoveOnGlobe`, so detections trigger replans without
  re-issuing `Move`.
