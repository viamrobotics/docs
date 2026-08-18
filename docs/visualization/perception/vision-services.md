---
linkTitle: "Vision services"
title: "Vision services in the 3D scene"
weight: 30
layout: "docs"
type: "docs"
description: "Render a vision service's segmented objects in the 3D scene and tune detection parameters against the live view."
---

A vision service with a 3D segmenter returns the objects it finds as point clouds, one
per object, through `GetObjectPointClouds`. The 3D scene polls each vision service on
your machine and renders those objects in place, so you see what the detector found in
the same space as the camera, the arm, and the workspace geometry.

## Prerequisites

- A vision service configured with a 3D segmenter, such as the
  [`obstacles_pointcloud` module](https://app.viam.com/module/viam/obstacles-pointcloud).
- A depth camera that supports point clouds, with its frame configured.

## Display a vision service's objects

Open the **3D SCENE** tab on your machine's page. When the machine is online, the scene
calls each vision service's `GetObjectPointClouds` and draws the returned objects as
point-cloud entities. Each object renders at the pose the service reports, placed in the
scene by the camera's frame.

To control which services render, open the **Settings** panel (gear icon) and select
**Vision**: each vision service has its own toggle. The polling rate lives under
**Connection**, with the scene's other data-stream rates; slow it down when a busy scene
lags, or turn it off while you work on something else.

## Read an object's placement

An object's position in the scene combines two sources: the segmenter's output (the
object's points and pose relative to the camera) and the camera's frame configuration
(where the camera sits in the frame system). When an object renders in the wrong place,
this split tells you where to look:

- **Every object is offset the same way**: the camera's frame configuration is wrong.
  Verify it with [Measuring between frames](/visualization/3d-scene/measuring-between-frames/)
  and [Verify point cloud alignment](/visualization/perception/verify-point-cloud-alignment/).
- **One object is wrong or split in two**: the segmenter's parameters group the points
  incorrectly. Tune the service configuration.

## Tune a detector against the live view

The scene gives you a visual feedback loop for segmenter parameters:

1. Place representative objects in the camera's view.
2. Watch the rendered objects in the 3D scene next to the raw point cloud (enable the
   camera under **Settings** > **Pointclouds**).
3. Adjust the vision service's configuration, for example the minimum points per object
   or the plane-removal threshold, and save.
4. Compare the new segmentation against the physical objects, then repeat.

Segmentation quality shows up directly: an over-aggressive threshold drops small
objects, and a loose one merges neighbors into one blob.

## When no objects appear

Work through these checks in order:

1. The vision service's toggle is on under **Settings** > **Vision**.
2. The vision polling rate under **Settings** > **Connection** is not off.
3. The service returns objects at all: call `GetObjectPointClouds` from the
   [vision service API](/reference/apis/services/vision/) and check the count.
4. The camera behind the service supports point clouds: cameras that report
   `supports_pcd=false` produce nothing for a 3D segmenter to segment.

## What's next

- [Point clouds](/visualization/perception/point-clouds/): how raw depth-camera data
  renders and displays.
- [Verify point cloud alignment](/visualization/perception/verify-point-cloud-alignment/):
  confirm the camera's frame before you tune a detector.
- [Publish visuals from a module](/visualization/publish-visuals-from-a-module/): draw
  custom annotations the built-in vision layer does not cover.
