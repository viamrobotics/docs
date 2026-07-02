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
**Widgets**, and toggle the camera on under **Camera widgets**. A floating panel then shows
the live feed with its current frame rate, for example `20.0fps`.

A resolution dropdown on the widget sets the feed size: **Default**, `1280x720`, `640x360`,
`320x180`, `160x90`, or `80x44`. A lower resolution costs less bandwidth, which helps when you
watch several cameras at once or work over a slow connection.

## Point clouds from depth cameras

A depth camera also reports the distance to points in front of it, which the scene renders as
a point cloud. For how point clouds render, display, and compare, see
[Point clouds](/visualization/perception/point-clouds/).

## Camera frames

A camera appears in the scene as a coordinate frame, and its point cloud renders at that
frame. If a camera's point cloud lands in the wrong place, check the camera's frame
configuration rather than the camera itself.
