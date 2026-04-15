---
linkTitle: "Calibrate frame offsets"
title: "Calibrate frame offsets"
weight: 20
layout: "docs"
type: "docs"
description: "Verify and adjust the spatial relationship between components using the 3D scene and measurement tool."
---

When you configure a camera mounted on an arm or a sensor attached to a base, the frame system needs the exact translation and orientation between the two components.
Small errors in these offsets cause the arm to reach for objects in the wrong place or the point cloud to misalign with the physical workspace.
The 3D scene tab lets you visually verify these offsets and use the measurement tool to check distances.

## Prerequisites

- A machine with at least two components that have frames configured (for example, an arm and a camera).
- Physical measurements of the distances between components.

## Verify frame offsets

### 1. Open the 3D scene tab

Navigate to your machine in the [Viam app](https://app.viam.com) and click the **3D scene** tab.

### 2. Select each component and check its position

Click a component in the tree view.
The details panel shows:

- **Local position**: the translation from the parent frame, in mm. This is what you configured.
- **World position**: the absolute position in the world frame, computed from the chain of parent transforms.

Compare the local position values to your physical measurements.
If the camera is 50 mm to the right and 100 mm above the arm's wrist joint, the local position should reflect that.

### 3. Use the measurement tool

The measurement tool calculates the distance between two points in the scene.

1. Activate the measurement tool from the toolbar.
2. Click a point on the first component (for example, the arm's end effector frame origin).
3. Click a point on the second component (for example, the camera frame origin).

The tool displays the distance in mm.
Compare this to your physical measurement.
If the values disagree, adjust the translation in the frame configuration.

You can constrain the measurement to a single axis (X, Y, or Z) to isolate which component of the offset is wrong.

### 4. Check orientation alignment

Select a component and look at its coordinate axes in the 3D view.
The axes should match the physical orientation of the component:

- A camera's Z axis (blue) typically points forward along the optical axis.
- An arm's coordinate system follows the manufacturer's convention.

If the axes are rotated relative to what you expect, adjust the orientation values in the frame configuration.
The details panel shows the orientation as an orientation vector (x, y, z, theta in degrees).

### 5. Verify with a point cloud

If the component is a depth camera, enable its point cloud in the settings panel.
The point cloud should align with the physical objects in your workspace.

If the point cloud appears shifted or rotated relative to where objects actually are, the camera's frame offset or orientation is wrong.
See [Verify point cloud alignment](/motion-planning/3d-scene/verify-point-cloud-alignment/) for more on working with point clouds.

## Iterative adjustment

Frame calibration is often iterative:

1. Measure physically.
2. Enter the values in the frame configuration.
3. Check the result in the 3D scene.
4. Adjust and repeat until the scene matches reality.

For high-precision applications, use the camera calibration procedure to compute intrinsic parameters before adjusting frame offsets.
See [Calibrate a camera for motion planning](/motion-planning/frame-system/camera-calibration/).
