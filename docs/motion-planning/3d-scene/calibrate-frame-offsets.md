---
linkTitle: "Calibrate frame offsets"
title: "Calibrate frame offsets"
weight: 20
layout: "docs"
type: "docs"
description: "Verify and adjust the spatial relationship between components using the 3D scene and measurement tool."
---

When you configure a camera on an arm, or a sensor on a base, the frame system needs the exact translation and orientation between the two components. A 15 mm error in a camera offset places a detected object 15 mm off; the arm then reaches for the wrong spot, or the point cloud sits behind the table instead of on it. The 3D scene tab lets you verify offsets visually and measure distances directly, so you can catch these errors before they produce bad motion.

## Prerequisites

- A machine with at least two components that have frames configured (for example, an arm and a camera).
- Physical measurements of the distances between components.

## Verify frame offsets

### 1. Open the 3D scene tab

Navigate to your machine in the [Viam app](https://app.viam.com) and click the **3D SCENE** tab.

### 2. Select each component and check its position

Click a component in the **World** panel.
The Details panel shows:

- **local position** (mm): the translation from the parent frame. This is what you configured.
- **world position** (mm): the absolute position in the world frame, computed from the chain of parent transforms.

Compare the local position values to your physical measurements.
If the camera is 50 mm to the right and 100 mm above the arm's wrist joint, the local position should reflect that.

### 3. Use the measurement tool

The measurement tool shows the distance between two points you click, so you can check configured offsets against physical measurements.

1. Click the **ruler** button in the top-center toolbar. Activating it disables entity selection until you exit the tool.
2. Click a point on the first component, for example the arm's end-effector frame origin.
3. Click a point on the second component, for example the camera frame origin.

The distance appears between the two points, displayed in meters to three decimals (for example, `0.245m` means 245 mm). Click a third time to clear the measurement. Click the ruler button again to exit the tool and re-enable entity selection.

To constrain the measurement to a subset of axes, open the **measurement settings** popover (the sliders icon next to the ruler). Under **Enabled axes**, toggle `x`, `y`, or `z` off; disabled axes are held fixed to the first point, so the distance is measured only along the axes that remain enabled.

### 4. Check orientation alignment

Select a component and compare its coordinate axes in 3D to the physical component:

- A camera's Z axis (blue) should point forward along the optical axis.
- An arm's axes should follow the manufacturer's convention.

If the axes are rotated relative to what you expect, adjust the orientation vector in the frame configuration. The Details panel displays it as (`x`, `y`, `z`, `th` in degrees).

### 5. Verify with a point cloud

If the component is a depth camera, enable its point cloud at **Settings → Pointclouds → Enabled cameras**.
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
