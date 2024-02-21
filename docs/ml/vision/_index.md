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
    {{< imgproc alt="A white dog with a bounding box around it labeled 'Dog: 0.71'" src="/ml/vision/dog-detector.png" resize="300x" declaredimensions=true >}}
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

- [GetDetections()](#getdetections)
- [GetDetectionsFromCamera()](#getdetectionsfromcamera)

## Classifications

_2D Image Classification_ is the process of taking a 2D image from a camera and deciding which class label, out of many, best describes the given image.
Any camera that can return 2D images can use 2D image classification.

The class labels used for classification vary and depend on the machine learning model and how it was trained.

The returned classifications consist of the image's class label and confidence score.

- `class_name` (string): specifies the label of the found object.
- `confidence` (float): specifies the confidence of the assigned label.
  Between `0.0` and `1.0`, inclusive.

**Supported API methods:**

- [GetClassifications()](#getclassifications)
- [GetClassificationsFromCamera()](#getclassificationsfromcamera)

## Segmentations

_3D Object Segmentation_ is the process of separating and returning a list of the identified "objects" from a 3D scene.
The "objects" are usually a list of point clouds with associated metadata, like the label, the 3D bounding box, and center coordinates of the object.

3D object segmentation is useful for obstacle detection.
See our guide [Navigate with a Rover Base](/tutorials/services/navigate-with-rover-base/#next-steps-automate-obstacle-detection) for an example of automating obstacle avoidance with 3D object segmentation for obstacle detection.

Any camera that can return 3D pointclouds can use 3D object segmentation.

**Supported API methods:**

- [GetObjectPointClouds()](#getobjectpointclouds)

## Supported models

To use a vision service with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your use case.

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
Model | Description <a name="model-table"></a>
----- | -----------
[`mlmodel`](./mlmodel/) | A detector or classifier that uses a `tensorflow-lite` model available on the machine’s hard drive to draw bounding boxes around objects or returns a class label and confidence score.
[`color_detector`](./color_detector/) | A heuristic detector that draws boxes around objects according to their hue (does not detect black, gray, and white).
[`obstacles_pointcloud`](./obstacles_pointcloud/) | A segmenter that identifies well-separated objects above a flat plane.
[`detector_3d_segmenter`](./detector_3d_segmenter/) | A segmenter that takes 2D bounding boxes from an object detector and projects the pixels in the bounding box to points in 3D space.
[`obstacles_depth`](./obstacles_depth/) | A segmenter for depth cameras that returns the perceived obstacles as a set of 3-dimensional bounding boxes, each with a Pose as a vector.
[`obstacles_distance`](./obstacles_distance/) | A segmenter that takes point clouds from a camera input and returns the average single closest point to the camera as a perceived obstacle.

### Modular Resources

{{<modular-resources api="rdk:service:vision" type="vision">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Used with

{{< cards >}}
{{< relatedcard link="/ml/deploy/" alt_title="Machine Learning" >}}
{{< /cards >}}

## API

Different vision service models support different methods:

{{< readfile "/static/include/services/apis/vision.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with a [camera](/components/camera/) and a vision service [detector](/ml/vision/#detections), [classifier](/ml/vision/#classifications) or [segmenter](/ml/vision/#segmentations), as applicable, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your machine.

{{% /alert %}}

### GetDetections

Get a list of detections from a given image using a configured [detector](#detections).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `image` [(RawImage)](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.RawImage): The image in which to look for detections.
- `extra` (Mapping[str, Any]) (_optional_): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(List[Detection])](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Detection): A list of 2D bounding boxes, their labels, and the confidence score of the labels around the detected objects, and confidence scores of those detections.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections).

```python {class="line-numbers linkable-line-numbers" data-line="11"}
# Grab camera from the machine
cam1 = Camera.from_robot(robot, "cam1")

# Get the detector you configured on your machine
my_detector = VisionClient.from_robot(robot, "my_detector")

# Get an image from the camera
img = await cam1.get_image()

# Get detections from that image
detections = await my_detector.get_detections(img)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `img` [(Image)](https://pkg.go.dev/image#Image): The image in which to look for detections.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]objectdetection.Detection)](https://pkg.go.dev/go.viam.com/rdk/vision/objectdetection#Detection): A list of 2D bounding boxes around the detected objects, and confidence scores of those detections.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision).

```go {class="line-numbers linkable-line-numbers" data-line="22"}
// Grab the camera from the machine
cameraName := "cam1"
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// Grab the detector you configured on your machine
visService, err := vision.from_robot(robot=robot, name='my_detector')
if err != nil {
    logger.Fatalf("Cannot get vision service: %v", err)
}

// Get the stream from a camera
camStream, err := myCam.Stream(context.Background())

// Get an image from the camera stream
img, release, err := camStream.Next(context.Background())
defer release()

// Get the detections from the image
detections, err := visService.Detections(context.Background(), img, nil)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(detections) > 0 {
    logger.Info(detections[0])
}
```

{{% /tab %}}
{{< /tabs >}}

### GetDetectionsFromCamera

Get a list of detections from the next image from a specified camera using a configured [detector](./#detections).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `camera_name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The name of the camera from which to get an image to run detections on.
- `extra` (Mapping[str, Any]) (_optional_): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(List[Detection])](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Detection): A list of 2D bounding boxes, their labels, and the confidence score of the labels around the detected objects, and confidence scores of those detections.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections_from_camera).

```python {class="line-numbers linkable-line-numbers" data-line="8"}
camera_name = "cam1"

# Grab the detector you configured on your machine
my_detector = VisionClient.from_robot(robot, "my_detector")

# Get detections from the next image from the camera
detections = await my_detector.get_detections_from_camera(camera_name)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cameraName` [(string)](https://pkg.go.dev/builtin#string): The name of the camera from which to get an image to run detections on.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]objectdetection.Detection)](https://pkg.go.dev/go.viam.com/rdk/vision/objectdetection#Detection): A list of bounding boxes around the detected objects, and confidence scores of those detections.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision).

```go {class="line-numbers linkable-line-numbers" data-line="15"}
// Grab the camera from the machine
cameraName := "cam1"
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// Grab the detector you configured on your machine
visService, err := vision.from_robot(robot=robot, name='my_detector')
if err != nil {
    logger.Fatalf("Cannot get vision service: %v", err)
}

// Get detections from the camera output
detections, err := visService.DetectionsFromCamera(context.Background(), myCam, nil)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(detections) > 0 {
    logger.Info(detections[0])
}
```

{{% /tab %}}
{{< /tabs >}}

### GetClassifications

Get a list of classifications from a given image using a configured [classifier](#classifications).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `image` [(RawImage)](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.RawImage): The image in which to look for classifications.
- `count` [(int)](https://docs.python.org/3/library/functions.html#int): The number of classifications to return.
  For example, if you specify `3` you will get the top three classifications with the greatest confidence scores.
- `extra` (Mapping[str, Any]) (_optional_): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(List[Classification])](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Classification): A list of classification labels, and the confidence scores of those classifications.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_classifications).

```python {class="line-numbers linkable-line-numbers" data-line="11"}
# Grab camera from the machine
cam1 = Camera.from_robot(robot, "cam1")

# Get the classifier you configured on your machine
my_classifier = VisionClient.from_robot(robot, "my_classifier")

# Get an image from the camera
img = await cam1.get_image()

# Get the 2 classifications with the highest confidence scores
classifications = await my_classifier.get_classifications(img, 2)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `img` [(Image)](https://pkg.go.dev/image#Image): The image in which to look for classifications.
- `n` [(int)](https://pkg.go.dev/builtin#int): The number of classifications to return.
  For example, if you specify `3` you will get the top three classifications with the greatest confidence scores.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(classification.Classification)](https://pkg.go.dev/go.viam.com/rdk/vision/classification#Classifications): A list of classification labels, and the confidence scores of those classifications.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision).

```go {class="line-numbers linkable-line-numbers" data-line="22"}
// Grab the camera from the machine
cameraName := "cam1"
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// Grab the classifier you configured on your machine
visService, err := vision.from_robot(robot=robot, name='my_classifier')
if err != nil {
    logger.Fatalf("Cannot get vision service: %v", err)
}

// Get the stream from a camera
camStream, err := myCam.Stream(context.Background())

// Get an image from the camera stream
img, release, err := camStream.Next(context.Background())
defer release()

// Get the 2 classifications with the highest confidence scores from the image
classifications, err := visService.Classifications(context.Background(), img, 2, nil)
if err != nil {
    logger.Fatalf("Could not get classifications: %v", err)
}
if len(classifications) > 0 {
    logger.Info(classifications[0])
}
```

{{% /tab %}}
{{< /tabs >}}

### GetClassificationsFromCamera

Get a list of classifications from the next image from a specified camera using a configured [classifier](#classifications).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `camera_name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The name of the camera from which to get an image to run the classifier on.
- `count` [(int)](https://docs.python.org/3/library/functions.html#int): The number of classifications to return.
  For example, if you specify `3` you will get the top three classifications with the greatest confidence scores.
- `extra` (Mapping[str, Any]) (_optional_): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(List[Classification])](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Classification): A list of classification labels, and the confidence scores of those classifications.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_classifications_from_camera).

```python {class="line-numbers linkable-line-numbers" data-line="8"}
camera_name = "cam1"

# Grab the classifier you configured on your machine
my_classifier = VisionClient.from_robot(robot, "my_classifier")

# Get the 2 classifications with the highest confidence scores from the next
# image from the camera
classifications = await my_classifier.get_classifications_from_camera(
    camera_name, 2)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cameraName` [(string)](https://pkg.go.dev/builtin#string): The name of the camera from which to get an image to run the classifier on.
- `n` [(int)](https://pkg.go.dev/builtin#int): The number of classifications to return.
  For example, if you specify `3` you will get the top three classifications with the greatest confidence scores.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]objection.Classification)](https://pkg.go.dev/go.viam.com/rdk/vision/classification#Classifications): A list of classification labels, and the confidence scores of those classifications.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision).

```go {class="line-numbers linkable-line-numbers" data-line="15"}
// Grab the camera from the machine
cameraName := "cam1"
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// Grab the classifier you configured on your machine
visService, err := vision.from_robot(robot=robot, name='my_classifier')
if err != nil {
    logger.Fatalf("Cannot get vision service: %v", err)
}

// Get the 2 classifications with the highest confidence scores from the camera output
classifications, err := visService.ClassificationsFromCamera(context.Background(), myCam, 2, nil)
if err != nil {
    logger.Fatalf("Could not get classifications: %v", err)
}
if len(classifications) > 0 {
    logger.Info(classifications[0])
}
```

{{% /tab %}}
{{< /tabs >}}

### GetObjectPointClouds

Get a list of 3D point cloud objects and associated metadata in the latest picture from a 3D camera (using a specified [segmenter](#segmentations)).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `camera_name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The name of the 3D camera from which to get point cloud data.
- `extra` (Mapping[str, Any]) (_optional_): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(List[PointCloudObject])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PointCloudObject): A list of point clouds and associated metadata like the center coordinates of each point cloud.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_object_point_clouds).

```python {class="line-numbers linkable-line-numbers" data-line="8"}
# Grab the 3D camera from the machine
cam1 = Camera.from_robot(robot, "cam1")

# Grab the object segmenter you configured on your machine
my_segmenter = VisionClient.from_robot(robot, "my_segmenter")

# Get the objects from the camera output
objects = await my_segmenter.get_object_point_clouds(cam1)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cameraName` [(string)](https://pkg.go.dev/builtin#string): The name of the 3D camera from which to get point cloud data.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]objection.Classification)](https://pkg.go.dev/go.viam.com/rdk/vision#Object): A list of point clouds and associated metadata like the center coordinates of each point cloud.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision).

```go {class="line-numbers linkable-line-numbers" data-line="15"}
// Grab the camera from the machine
cameraName := "cam1"
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// Grab the segmenter you configured on your machine
visService, err := vision.from_robot(robot=robot, name='my_segmenter')
if err != nil {
    logger.Fatalf("Cannot get vision service: %v", err)
}

// Get the objects from the camera output
objects, err := visService.ObjectPointClouds(context.Background(), myCam, nil)
if err != nil {
    logger.Fatalf("Could not get point clouds: %v", err)
}
if len(objects) > 0 {
    logger.Info(objects[0])
}
```

{{% /tab %}}
{{< /tabs >}}

## DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own vision service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.do_command).

```python {class="line-numbers linkable-line-numbers"}
# Access your vision service
vision_svc = VisionClient.from_robot(robot, "my_vision_svc")

my_command = {
  "command": "dosomething",
  "someparameter": 52
}

await vision_svc.do_command(my_command)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map\[string\]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
// Access your vision service
visService, err := vision.from_robot(robot=robot, name="my_vision_svc")
if err != nil {
  logger.Fatal(err)
}

resp, err := visService.DoCommand(ctx, map[string]interface{}{"command": "dosomething", "someparameter": 52})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
vision_svc = VisionClient.from_robot(robot, "my_vision_svc")

await vision_svc.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
visService, err := vision.FromRobot(robot, "my_vision_svc")

err := visService.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
