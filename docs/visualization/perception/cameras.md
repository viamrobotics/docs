---
linkTitle: "Cameras"
title: "Cameras in the 3D scene"
weight: 20
layout: "docs"
type: "docs"
description: "View a camera's live feed alongside the 3D scene, and relate it to the camera's frame and point cloud."
---

A camera contributes to the 3D scene in more than one way: its frame positions it in space,
its live feed shows what it currently sees, and a depth camera also produces a point cloud.

## See a camera's live feed

To watch a camera's feed next to the 3D view, open the **Settings** panel (gear icon), select
**Widgets**, and toggle the camera on under **Camera widgets**. For the widget's resolution
and frame-rate controls, see [3D scene widgets](/visualization/3d-scene/3d-scene-widgets/).
To view the scene from the camera's own perspective, open its
[frame POV](/visualization/3d-scene/3d-scene-widgets/#frame-pov).

## Point clouds from depth cameras

A depth camera also reports the distance to points in front of it, which the scene renders as
a point cloud. For how point clouds render, display, and compare, see
[Point clouds](/visualization/perception/point-clouds/).

## Camera frames

A camera appears in the scene as a coordinate frame, and its point cloud renders at that
frame. If a camera's point cloud appears in the wrong place, check the camera's frame
configuration rather than the camera itself.
