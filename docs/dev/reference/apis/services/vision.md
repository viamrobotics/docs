---
title: "Vision service API"
linkTitle: "Vision"
weight: 20
type: "docs"
tags: ["vision", "computer vision", "CV", "services"]
description: "Give commands to get detections, classifications, or point cloud objects, depending on the ML model the vision service is using."
aliases:
    - /services/vision/
    - /ml/vision/detection/
    - /ml/vision/classification/
    - /ml/vision/segmentation/
    - /services/vision/segmentation/
    - /ml/vision/
    - /appendix/apis/services/vision/
icon: true
images: ["/services/icons/vision.svg"]
tags: ["vision", "computer vision", "CV", "services"]
date: "2022-01-01"
aliases:
   - /appendix/apis/services/vision/
# updated: ""  # When the content was last entirely checked
---

The vision service enables your machine to use its on-board [cameras](/operate/reference/components/camera/) to intelligently see and interpret the world around it.
While the camera component lets you access what your machine's camera sees, the vision service allows you to interpret your image data.

The vision service API allows you to get detections, classifications, or point cloud objects, depending on the ML model the vision service is using.

The vision service supports the following kinds of operations:

- [Detections](#detections)
- [Classifications](#classifications)
- [Segmentations](#segmentations)

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

- `x_min`, `y_min`, `x_max`, `y_max` (int): specify the bounding box around the object.
- `class_name` (string): specifies the label of the found object.
- `confidence` (float): specifies the confidence of the assigned label.
  Between `0.0` and `1.0`, inclusive.

**Supported API methods:**

- [GetDetections()](/dev/reference/apis/services/vision/#getdetections)
- [GetDetectionsFromCamera()](/dev/reference/apis/services/vision/#getdetectionsfromcamera)

## Classifications

_2D Image Classification_ is the process of taking a 2D image from a camera and deciding which class label, out of many, best describes the given image.
Any camera that can return 2D images can use 2D image classification.

The class labels used for classification vary and depend on the machine learning model and how it was trained.

The returned classifications consist of the image's class label and confidence score.

- `class_name` (string): specifies the label of the found object.
- `confidence` (float): specifies the confidence of the assigned label.
  Between `0.0` and `1.0`, inclusive.

**Supported API methods:**

- [GetClassifications()](/dev/reference/apis/services/vision/#getclassifications)
- [GetClassificationsFromCamera()](/dev/reference/apis/services/vision/#getclassificationsfromcamera)

## Segmentations

_3D Object Segmentation_ is the process of separating and returning a list of the identified "objects" from a 3D scene.
The "objects" are usually a list of point clouds with associated metadata, like the label, the 3D bounding box, and center coordinates of the object.

3D object segmentation is useful for obstacle detection.
See our guide [Navigate with a Rover Base](/tutorials/services/navigate-with-rover-base/#next-steps-automate-obstacle-detection) for an example of automating obstacle avoidance with 3D object segmentation for obstacle detection.

Any camera that can return 3D pointclouds can use 3D object segmentation.

**Supported API methods:**

- [GetObjectPointClouds()](/dev/reference/apis/services/vision/#getobjectpointclouds)

The [vision service](/operate/reference/services/vision/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/vision-table.md" >}}

## Establish a connection

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on the [Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code.

{{% snippet "show-secret.md" %}}

When executed, this sample code creates a connection to your machine as a client.

The following examples assume that you have a machine configured with a [camera](/operate/reference/components/camera/) and a vision service [detector](/operate/reference/services/vision/#detections), [classifier](/operate/reference/services/vision/#classifications) or [segmenter](/operate/reference/services/vision/#segmentations).

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.vision import VisionClient
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/services/vision"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

{{< readfile "/static/include/services/apis/generated/vision.md" >}}
