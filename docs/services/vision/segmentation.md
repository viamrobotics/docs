---
title: "Segmentation (or 3D object segmentation)"
linkTitle: "Segmentation"
weight: 20
type: "docs"
description: "Select an algorith that creates point clouds of identified objects in a 3D image."
tags: ["vision", "computer vision", "CV", "services", "segmentation"]
# SMEs: Bijan, Khari
---

_3D Object Segmentation_ is the process of separating and returning a list of the identified "objects" from a 3D scene.
The "objects" are a list of point clouds with associated metadata, like the label, the 3D bounding box, and center coordinates of the object.

Any camera that can return 3D pointclouds can use 3D object segmentation.

## Segmenter Types

The types of segmenters supported are:

- [**radius_clustering_segmenter**](#radius-clustering-segmenter): Radius clustering is a segmenter that identifies well separated objects above a flat plane.
- [**detector_segmenter**](#detector-segmenter): Object segmenters are automatically created from [detectors](../detection) in the Vision Service.

### Radius Clustering Segmenter

Radius clustering is a segmenter that identifies well separated objects above a flat plane.
It first identifies the biggest plane in the scene, eliminates all points below that plane, and begins clustering points above that plane based on how near they are to each other.
It is slower than other segmenters and can take up to 30s to segment a scene.

| Parameter | Description |
| --------- | ----------- |
| `min_points_in_plane` | An integer that specifies how many points there must be in a flat surface for it to count as a plane. This is to distinguish between large planes, like the floors and walls, and small planes, like the tops of bottle caps. |
| `min_points_in_segment` | An integer that sets a minimum size to the returned objects, and filters out all other found objects below that size.
| `clustering_radius_mm` | A floating point number that specifies how far apart points can be (in units of mm) in order to be considered part of the same object. A small clustering radius will more likely split different parts of a large object into distinct objects. A large clustering radius may aggregate closely spaced objects into one object. 3.0 is a decent starting value. |
| `mean_k_filtering (optional)` | An integer parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should be set to be 5-10% of the number of min_points_in_segment. Start with 5% and go up if objects are still too noisy. If you don’t want to use the filtering, set the number to 0 or less. |

### Detector Segmenter

Object segmenters are automatically created from [detectors](../detection) in the Vision Service.
Any registered detector, for example `detector1`, defined in the `register_models` field or added later to the Vision Service becomes a segmenter with `_segmenter` appended to its name, for example `detector1_segmenter`.
It begins by finding the 2D bounding boxes, and then returns the list of 3D point cloud projection of the pixels within those bounding boxes.

| Parameter | Description |
| --------- | ----------- |
| `detector_name`| The name of the detector already registered in the Vision Service that will be turned into a segmenter. |
| `confidence_threshold_pct` | A number between 0 and 1 which represents a filter on object confidence scores. Detections that score below the threshold will be filtered out in the segmenter. The default is 0.5. |
| `mean_k` | An integer parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should be set to be 5-10% of the minimum segment size. Start with 5% and go up if objects are still too noisy. If you don’t want to use the filtering, set the number to 0 or less. |
| `sigma` | A floating point parameter used in [a subroutine to eliminate the noise in the point clouds](https://pcl.readthedocs.io/projects/tutorials/en/latest/statistical_outlier.html). It should usually be set between 1.0 and 2.0. 1.25 is usually a good default. If you want the object result to be less noisy (at the risk of losing some data around its edges) set sigma to be lower. |

## Segmentation API

To learn more about the Segmentation API, see the [Python SDK docs](https://python.viam.dev/autoapi/viam/services/vision/index.html) or the [Go RDK docs](https://pkg.go.dev/go.viam.com/rdk/vision).
