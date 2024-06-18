---
title: "Use Computer Vision with the Vision Service"
linkTitle: "Computer Vision"
weight: 90
type: "docs"
description: "The vision service enables your machine to use its on-board cameras to intelligently see and interpret the world around it."
icon: true
images: ["/services/icons/vision.svg"]
tags: ["vision", "computer vision", "CV", "services"]
no_list: true
modulescript: true
aliases:
  - "/services/vision/"
  - "/ml/vision/detection/"
  - "/ml/vision/classification/"
  - "/ml/vision/segmentation/"
  - "/services/vision/segmentation/"
  - /ml/vision/
# SMEs: Bijan, Khari
---

The vision service enables your machine to use its on-board [cameras](/components/camera/) to intelligently see and interpret the world around it.
While the camera component lets you access what your machine's camera sees, the vision service allows you to interpret your image data.

Currently, the vision service supports the following kinds of operations:

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

- [GetDetections()](/services/vision/#getdetections)
- [GetDetectionsFromCamera()](/services/vision/#getdetectionsfromcamera)

## Classifications

_2D Image Classification_ is the process of taking a 2D image from a camera and deciding which class label, out of many, best describes the given image.
Any camera that can return 2D images can use 2D image classification.

The class labels used for classification vary and depend on the machine learning model and how it was trained.

The returned classifications consist of the image's class label and confidence score.

- `class_name` (string): specifies the label of the found object.
- `confidence` (float): specifies the confidence of the assigned label.
  Between `0.0` and `1.0`, inclusive.

**Supported API methods:**

- [GetClassifications()](/services/vision/#getclassifications)
- [GetClassificationsFromCamera()](/services/vision/#getclassificationsfromcamera)

## Segmentations

_3D Object Segmentation_ is the process of separating and returning a list of the identified "objects" from a 3D scene.
The "objects" are usually a list of point clouds with associated metadata, like the label, the 3D bounding box, and center coordinates of the object.

3D object segmentation is useful for obstacle detection.
See our guide [Navigate with a Rover Base](/tutorials/services/navigate-with-rover-base/#next-steps-automate-obstacle-detection) for an example of automating obstacle avoidance with 3D object segmentation for obstacle detection.

Any camera that can return 3D pointclouds can use 3D object segmentation.

**Supported API methods:**

- [GetObjectPointClouds()](/services/vision/#getobjectpointclouds)

## Supported models

To use a vision service with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your use case.

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
| Model | Description <a name="model-table"></a> |
| ----- | -------------------------------------- |
| [`mlmodel`](./mlmodel/) | A detector or classifier that uses a model available on the machine’s hard drive to draw bounding boxes around objects or returns a class label and confidence score. |
| [`color_detector`](./color_detector/) | A heuristic detector that draws boxes around objects according to their hue (does not detect black, gray, and white). |
| [`obstacles_pointcloud`](./obstacles_pointcloud/) | A segmenter that identifies well-separated objects above a flat plane. |
| [`detector_3d_segmenter`](./detector_3d_segmenter/) | A segmenter that takes 2D bounding boxes from an object detector and projects the pixels in the bounding box to points in 3D space. |
| [`obstacles_depth`](./obstacles_depth/) | A segmenter for depth cameras that returns the perceived obstacles as a set of 3-dimensional bounding boxes, each with a Pose as a vector. |
| [`obstacles_distance`](./obstacles_distance/) | A segmenter that takes point clouds from a camera input and returns the average single closest point to the camera as a perceived obstacle. |

### Modular resources

{{<modular-resources api="rdk:service:vision" type="vision">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Used with

{{< cards >}}
{{< relatedcard link="/services/ml/deploy/" alt_title="Machine Learning" >}}
{{< /cards >}}

## API

Different vision service models support different methods:

{{< readfile "/static/include/services/apis/generated/vision-table.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with a [camera](/components/camera/) and a vision service [detector](/services/vision/#detections), [classifier](/services/vision/#classifications) or [segmenter](/services/vision/#segmentations), as applicable, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your machine.

{{% /alert %}}

{{< readfile "/static/include/services/apis/generated/vision.md" >}}
