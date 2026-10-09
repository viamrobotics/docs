---
linkTitle: "Point clouds"
title: "Point clouds in the 3D scene"
weight: 10
layout: "docs"
type: "docs"
description: "How depth-camera point clouds render in the 3D scene, how to adjust their display, and how to load and compare external point clouds."
capabilities: ["scene-3d"]
diataxis: explanation
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

For a full alignment walkthrough, see
[Verify point cloud alignment](/visualization/perception/verify-point-cloud-alignment/).

## Link two point clouds with HoverLink

To compare two point clouds that should align, such as a registered scan and a transformed
copy, or ground-truth points and predicted points, link them with **HoverLink**. Hovering a
point in one then highlights the matching point in the other, and the hover tooltip shows
both points' positions.

1. Select a point cloud or arrows entity, such as an imported `.pcd` or `.ply` file.
2. In the Details panel, click **Add Relationship** and choose **HoverLink**.
3. Pick the other entity, and set the **Index mapping**. The default, `index`, matches point
   N in one cloud to point N in the other. Other expressions over `index` map between
   datasets whose points aren't in the same order.
4. Click **Add**.

Existing links appear under **Relationships** in the Details panel, where you can remove them.
