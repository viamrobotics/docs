---
linkTitle: "Perception"
title: "Perception in the 3D scene"
weight: 60
layout: "docs"
type: "docs"
no_list: true
description: "View and compare live perception data in the 3D scene: depth-camera point clouds, vision-service entities, and a sensor's own point of view."
---

The 3D scene renders live perception data alongside your frame system, so you see what your
machine senses in the same space as the components that sense it. Cameras are what it draws
today, and a camera contributes in more than one way: its frame positions it in space, a
depth camera's point cloud renders at that frame, a vision service can add entities of its
own, and the camera's live feed and
[point of view](/visualization/3d-scene/3d-scene-widgets/) are available as widgets.

When perception data lands in the wrong place in the scene, the sensing component's frame
configuration is the usual cause, not the component. For configuring and tuning the vision
services themselves, see [Computer vision](/vision/).

{{< cards >}}
{{% card link="/visualization/perception/point-clouds/" noimage="true" %}}
{{% card link="/visualization/perception/vision-services/" noimage="true" %}}
{{% card link="/visualization/perception/verify-point-cloud-alignment/" noimage="true" %}}
{{< /cards >}}
