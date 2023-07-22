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

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured with a [camera](/components/camera/) and a Vision Service [detector](/services/vision/detection/), [classifier](/services/vision/classification/) or [segmenter](/services/vision/segmentation/), as applicable, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### GetDetections

Get a list of detections from a given image using a detector.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `image` [(RawImage)](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.RawImage): The image in which to look for detections.
- `extra` (Mapping[str, Any]) (*optional*): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(List[Detection])](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Detectionn): A list of 2D bounding boxes, their labels, and the confidence score of the labels around the detected objects, and confidence scores of those detections.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections).

```python {class="line-numbers linkable-line-numbers" data-line="11"}
# Grab camera from the robot
cam1 = Camera.from_robot(robot, "cam1")

# Get the detector you configured on your robot
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
// Grab the camera from the robot
cameraName := "cam1"
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// Grab the detector you configured on your robot
visService, err := vision.from_robot(robot=robot, name='my_detector')
if err != nil {
    logger.Fatalf("Cannot get Vision Service: %v", err)
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

Get a list of detections from the next image from a specified camera using a detector.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `camera_name` [(string)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The name of the camera from which to get an image to run detections on.
- `extra` (Mapping[str, Any]) (*optional*): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(List[Detection])](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Detectionn): A list of 2D bounding boxes, their labels, and the confidence score of the labels around the detected objects, and confidence scores of those detections.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections_from_camera).


```python {class="line-numbers linkable-line-numbers" data-line="8"}
# Grab the camera from the robot
cam1 = Camera.from_robot(robot, "cam1")

# Grab the detector you configured on your robot
my_detector = VisionClient.from_robot(robot, "my_detector")

# Get detections from the next image from the camera
detections = await my_detector.get_detections_from_camera(cam1)
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
// Grab the camera from the robot
cameraName := "cam1"
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// Grab the detector you configured on your robot
visService, err := vision.from_robot(robot=robot, name='my_detector')
if err != nil {
    logger.Fatalf("Cannot get Vision Service: %v", err)
}

// Get detections from the camera output
detections, err := visService.DetectionsFromCamera(context.Background(), myCam, nil)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(directDetections) > 0 {
    logger.Info(detections[0])
}
```

{{% /tab %}}
{{< /tabs >}}