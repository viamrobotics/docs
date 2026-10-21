---
title: "Vision service API"
linkTitle: "Vision"
weight: 80
type: "docs"
description: "Give commands to get 2D detections, classifications, 3D detections, or point cloud objects, depending on the model the vision service is using."
capabilities: ["sdks", "vision-service"]
diataxis: reference
aliases:
  - /appendix/apis/services/vision/
  - /services/vision/segmentation/
icon: true
images: ["/services/icons/vision.svg"]
tags: ["vision", "computer vision", "CV", "services"]
date: "2026-04-14"
---

The vision service enables your machine to use its on-board [cameras](/hardware/) to intelligently see and interpret the world around it.
While the camera component lets you access what your machine's camera sees, the vision service allows you to interpret your image data.

The vision service {{< glossary_tooltip term_id="api" text="API" >}} allows you to get detections, classifications, 3D detections, or point cloud objects, depending on the model the vision service is using.

The vision service supports the following kinds of operations:

- [Detections](#detections)
- [Classifications](#classifications)
- [3D detections and segmentation](#3d-detections-and-segmentation)

## Detections

<div class="td-max-width-on-larger-screens">
  <div class="alignright" >
    {{< imgproc alt="A white dog with a bounding box around it labeled 'Dog: 0.71'" src="/services/vision/dog-detector.png" resize="300x" declaredimensions=true >}}
  </div>
</div>

_2D Object Detection_ is the process of taking a 2D image from a camera and identifying and drawing a box around the distinct "objects" of interest in the scene.
Any camera that can return 2D images can use 2D object detection.

You can use different types of detectors, both based on heuristics and machine learning, for any object you may need to identify.

The returned detections consist of the bounding box around the identified object, as well as its label and confidence score:

- `x_min`, `y_min`, `x_max`, `y_max` (int): specify the bounding box around the object using a rectangular area specified by two points: the top left point (`(x_min, y_min)`) and the bottom right point (`(x_max, y_max)`). The origin (0, 0) occupies the top left pixel of the image; X values increase as you move right, Y values increase as you move down.
- `class_name` (string): specifies the label of the found object.
- `confidence` (float): specifies the confidence of the assigned label.
  Between `0.0` and `1.0`, inclusive.

**Supported API methods:**

- [GetDetections()](/reference/apis/services/vision/#getdetections)
- [GetDetectionsFromCamera()](/reference/apis/services/vision/#getdetectionsfromcamera)

## Classifications

_2D Image Classification_ is the process of taking a 2D image from a camera and deciding which class label, out of many, best describes the given image.
Any camera that can return 2D images can use 2D image classification.

The class labels used for classification vary and depend on the machine learning model and how it was trained.

The returned classifications consist of the image's class label and confidence score.

- `class_name` (string): specifies the label of the found object.
- `confidence` (float): specifies the confidence of the assigned label.
  Between `0.0` and `1.0`, inclusive.

**Supported API methods:**

- [GetClassifications()](/reference/apis/services/vision/#getclassifications)
- [GetClassificationsFromCamera()](/reference/apis/services/vision/#getclassificationsfromcamera)

## 3D detections and segmentation

_3D detection_ is the process of finding the distinct "objects" in a 3D scene and returning where they are in space.
Any camera that can return 3D point clouds can use it.

`GetDetections3D` is the recommended method.
It returns each object as a tree of named transforms that carries the object's shapes and class hypotheses.
Because the result is already a set of transforms, you can pass it directly into a frame system or a motion `WorldState`.

`GetObjectPointClouds` is the older format.
It returns one flat geometry and one merged point cloud per object, along with a label.
It is useful for obstacle detection when you need the raw points of each object.

Not every vision service model supports `GetDetections3D`.
Call `GetProperties` to see which result types a model supports.

{{% alert title="Tip" color="tip" %}}
3D operations require [frame system](/motion-planning/frame-system/) configuration to properly relate camera coordinates to your machine's spatial reference frames.
This enables the vision service to provide meaningful 3D coordinates and spatial relationships.
{{% /alert %}}

**Supported API methods:**

- [GetDetections3D()](/reference/apis/services/vision/#getdetections3d): recommended. Returns each object as a tree of named transforms carrying its shapes, plus class hypotheses.
- [GetObjectPointClouds()](/reference/apis/services/vision/#getobjectpointclouds): the older format. Returns one geometry and one point cloud per object.

The [vision service](/vision/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/vision-table.md" >}}

## API

{{< readfile "/static/include/services/apis/generated/vision.md" >}}
