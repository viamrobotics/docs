---
title: "Vision Service"
linkTitle: "Vision"
weight: 90
type: "docs"
description: "The Vision Service enables your robot to use its on-board cameras to intelligently see and interpret the world around it."
icon: "/services/icons/vision.svg"
tags: ["vision", "computer vision", "CV", "services"]
no_list: true
# SMEs: Bijan, Khari
---

The Vision Service enables your robot to use its on-board [cameras](/components/camera/) to intelligently see and interpret the world around it.
While the camera component lets you access what your robot's camera sees, the Vision Service allows you to interpret your image data.
The Vision Service is a default service on the robot, and can be initialized without attributes.

Currently, the Vision Service supports the following models:

{{< cards >}}
  {{% card link="/services/vision/detection/" %}}
  {{% card link="/services/vision/classification/" %}}
  {{% card link="services/vision/segmentation" %}}
{{< /cards >}}

## API

The Vision Service supports the following methods:

Method Name | Description
----------- | -----------
[`GetDetections`](#getdetections) | Get detections from an image.
[`GetDetectionsFromCamera`](#getdetectionsfromcamera) | Get detections from the next image from a camera.
[`GetClassifications`](#getclassifications) | Get classifications from an image.
[`GetClassificationsFromCamera`](#getclassificationsfromcamera) | Get classifications from the next image from a camera.
[`GetObjectPointClouds`](#getobjectpointclouds) | Get a list of point cloud objects from a 3D camera.


### GetDetections

{{< tabs >}}
{{% tab name="Python" %}}



```python {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `img` [(Image)](https://pkg.go.dev/image#Image): The image in which to look for detections
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]objectdetection.Detection)](https://pkg.go.dev/go.viam.com/rdk/vision/objectdetection#Detection): A list of bounding boxes around the detected objects, and confidence scores of those detections.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision).

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}