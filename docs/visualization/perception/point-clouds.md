---
linkTitle: "Point Clouds"
title: "Point clouds in the 3D scene"
weight: 10
layout: "docs"
type: "docs"
description: "How depth-camera point clouds render in the 3D scene, how to adjust their display, and how to load and compare external point clouds."
---

A depth camera reports the distance to points in front of it. The 3D scene renders that data
as a colored point set, placed in the scene by the camera's frame, so you can see what the
camera perceives in the same space as the rest of your machine.

## Live point clouds

When your machine is online, the scene streams point clouds from your depth cameras and
draws each as a set of points at the camera's frame. Because each point cloud sits at its
camera's frame, a point cloud that appears in the wrong place usually points to a wrong camera
frame, not wrong perception.

Vision services can also contribute point-cloud entities, such as the points behind a
detection. These render the same way.

## Adjust how point clouds display

Open the **Settings** panel (gear icon) in the 3D scene tab to control point-cloud rendering:

- **Point size and color**: set the default size and color the scene draws points at.
- **Enabled cameras**: turn each camera's point cloud on or off, so you can focus on one
  camera at a time.
- **Vision**: enable or disable vision-service point-cloud entities.

## Load and compare external point clouds

To inspect a saved capture, drag a `.pcd` or `.ply` file onto the viewport. The scene loads
it as a point cloud you can view alongside your live data, which is useful for comparing a
saved SLAM map or scan against the current frame system.

To compare two point clouds that should align, such as a scan and a transformed copy, link
them with **HoverLink**: select one point cloud, add a HoverLink relationship to the other,
and hovering a point in one highlights the matching point in the other. For a full alignment
walkthrough, see
[Verify point cloud alignment](/visualization/perception/verify-point-cloud-alignment/).
