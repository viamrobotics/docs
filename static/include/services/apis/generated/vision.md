### GetDetectionsFromCamera

Get a list of detections from the next image from a specified camera using a configured [detector](./#detections).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `camera_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the camera to use for detection.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.service.vision.Detection]](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Detection)): A list of 2D bounding boxes, their labels, and the confidence score of the labels, around the found objects in the next 2D image from the given camera, with the given detector applied to it.

**Raises:**

- (ViamError): Raised if given an image without a specified width and height.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
camera_name = "cam1"

# Grab the detector you configured on your machine
my_detector = VisionClient.from_robot(robot, "my_detector")

# Get detections from the next image from the camera
detections = await my_detector.get_detections_from_camera(camera_name)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections_from_camera).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cameraName` [(string)](https://pkg.go.dev/builtin#string): The name of the camera from which to get an image to run detections on.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]objectdetection.Detection)](https://pkg.go.dev/go.viam.com/rdk/vision/objectdetection#Detection): A list of bounding boxes around the detected objects, and confidence scores of those detections.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get detections from the camera output
detections, err := visService.DetectionsFromCamera(context.Background(), myCam, nil)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(detections) > 0 {
    logger.Info(detections[0])
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `cameraName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Detection](https://flutter.viam.dev/viam_protos.service.vision/Detection-class.html)>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var detections = await myVisionService.detectionsFromCamera('myWebcam');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/detectionsFromCamera.html).

{{% /tab %}}
{{< /tabs >}}

### GetDetections

Get a list of detections from a given image using a configured [detector](#detections).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `image` ([viam.media.video.ViamImage](https://python.viam.dev/autoapi/viam/gen/component/camera/v1/camera_pb2/index.html#viam.gen.component.camera.v1.camera_pb2.Image)) (required): The image to get detections from.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.service.vision.Detection]](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Detection)): A list of 2D bounding boxes, their labels, and the confidence score of the labels, around the found objects in the next 2D image from the given camera, with the given detector applied to it.

**Raises:**

- (ViamError): Raised if given an image without a specified width and height.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Grab camera from the machine
cam1 = Camera.from_robot(robot, "cam1")

# Get the detector you configured on your machine
my_detector = VisionClient.from_robot(robot, "my_detector")

# Get an image from the camera
img = await cam1.get_image()

# Get detections from that image
detections = await my_detector.get_detections(img)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `img` [(image.Image)](https://pkg.go.dev/image#Image): The image in which to look for detections.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]objectdetection.Detection)](https://pkg.go.dev/go.viam.com/rdk/vision/objectdetection#Detection): A list of 2D bounding boxes around the detected objects, and confidence scores of those detections.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
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

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `image` [ViamImage](https://flutter.viam.dev/viam_sdk/ViamImage-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Detection](https://flutter.viam.dev/viam_protos.service.vision/Detection-class.html)>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var latestImage = await myWebcam.image();
var detections = await myVisionService.detections(latestImage);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/detections.html).

{{% /tab %}}
{{< /tabs >}}

### GetClassificationsFromCamera

Get a list of classifications from the next image from a specified camera using a configured [classifier](#classifications).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `camera_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the camera to use for detection.
- `count` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The number of classifications desired.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.service.vision.Classification]](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Classification)): The list of Classifications.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
camera_name = "cam1"

# Grab the classifier you configured on your machine
my_classifier = VisionClient.from_robot(robot, "my_classifier")

# Get the 2 classifications with the highest confidence scores from the next image from the camera
classifications = await my_classifier.get_classifications_from_camera(
    camera_name, 2)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_classifications_from_camera).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cameraName` [(string)](https://pkg.go.dev/builtin#string): The name of the camera from which to get an image to run the classifier on.
- `n` [(int)](https://pkg.go.dev/builtin#int): The number of classifications to return. For example, if you specify `3` you will get the top three classifications with the greatest confidence scores.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(classification.Classifications)](https://pkg.go.dev/go.viam.com/rdk/vision/classification#Classifications): A list of classification labels, and the confidence scores of those classifications.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the 2 classifications with the highest confidence scores from the camera output
classifications, err := visService.ClassificationsFromCamera(context.Background(), myCam, 2, nil)
if err != nil {
    logger.Fatalf("Could not get classifications: %v", err)
}
if len(classifications) > 0 {
    logger.Info(classifications[0])
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `cameraName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `count` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Classification](https://flutter.viam.dev/viam_protos.service.vision/Classification-class.html)>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var classifications = await myVisionService.classificationsFromCamera('myWebcam', 2);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/classificationsFromCamera.html).

{{% /tab %}}
{{< /tabs >}}

### GetClassifications

Get a list of classifications from a given image using a configured [classifier](#classifications).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `image` ([viam.media.video.ViamImage](https://python.viam.dev/autoapi/viam/gen/component/camera/v1/camera_pb2/index.html#viam.gen.component.camera.v1.camera_pb2.Image)) (required): The image to get detections from.
- `count` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The number of classifications desired.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.service.vision.Classification]](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Classification)): The list of Classifications.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Grab camera from the machine
cam1 = Camera.from_robot(robot, "cam1")

# Get the classifier you configured on your machine
my_classifier = VisionClient.from_robot(robot, "my_classifier")

# Get an image from the camera
img = await cam1.get_image()

# Get the 2 classifications with the highest confidence scores
classifications = await my_classifier.get_classifications(img, 2)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_classifications).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `img` [(image.Image)](https://pkg.go.dev/image#Image): The image in which to look for classifications.
- `n` [(int)](https://pkg.go.dev/builtin#int): The number of classifications to return. For example, if you specify `3` you will get the top three classifications with the greatest confidence scores.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(classification.Classifications)](https://pkg.go.dev/go.viam.com/rdk/vision/classification#Classifications): A list of classification labels, and the confidence scores of those classifications.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the stream from a camera
camStream, err := myCam.Stream(context.Background())
if err!=nil {
    logger.Error(err)
    return
}

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

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `image` [ViamImage](https://flutter.viam.dev/viam_sdk/ViamImage-class.html) (required)
- `count` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Classification](https://flutter.viam.dev/viam_protos.service.vision/Classification-class.html)>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var latestImage = await myWebcam.image();
var classifications = await myVisionService.classifications(latestImage, 2);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/classifications.html).

{{% /tab %}}
{{< /tabs >}}

### GetObjectPointClouds

Get a list of 3D point cloud objects and associated metadata in the latest picture from a 3D camera (using a specified [segmenter](#segmentations)).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `camera_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the camera.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.common.PointCloudObject]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PointCloudObject)): The pointcloud objects with metadata.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
import numpy as np
import open3d as o3d

# Grab the 3D camera from the machine
cam1 = Camera.from_robot(robot, "cam1")
# Grab the object segmenter you configured on your machine
my_segmenter = VisionClient.from_robot(robot, "my_segmenter")
# Get the objects from the camera output
objects = await my_segmenter.get_object_point_clouds(cam1)
# write the first object point cloud into a temporary file
with open("/tmp/pointcloud_data.pcd", "wb") as f:
    f.write(objects[0].point_cloud)
pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
points = np.asarray(pcd.points)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_object_point_clouds).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cameraName` [(string)](https://pkg.go.dev/builtin#string): The name of the 3D camera from which to get point cloud data.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]*viz.Object)](https://pkg.go.dev/go.viam.com/rdk/vision#Object): A list of point clouds and associated metadata like the center coordinates of each point cloud.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the objects from the camera output
objects, err := visService.GetObjectPointClouds(context.Background(), "cam1", nil)
if err != nil {
    logger.Fatalf("Could not get point clouds: %v", err)
}
if len(objects) > 0 {
    logger.Info(objects[0])
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `cameraName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[PointCloudObject](https://flutter.viam.dev/viam_protos.common.common/PointCloudObject-class.html)>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var ptCloud = await myVisionService.objectPointClouds('myCamera');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/objectPointClouds.html).

{{% /tab %}}
{{< /tabs >}}

### Reconfigure

Reconfigure this resource.
Reconfigure must reconfigure the resource atomically and in place.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `deps` [(Dependencies)](https://pkg.go.dev/go.viam.com/rdk/resource#Dependencies): The resource dependencies.
- `conf` [(Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config): The resource configuration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own vision service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
service = SERVICE.from_robot(robot, "builtin")  # replace SERVICE with the appropriate class

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

# Can be used with any resource, using the motion service as an example
await service.do_command(command=my_command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using DoCommand with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myArm.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example using doCommand with an arm component
const command = {'cmd': 'test', 'data1': 500};
var result = myArm.doCommand(command);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### FromRobot

Get the resource from the provided robot with the given name.

{{< tabs >}}
{{% tab name="Flutter" %}}

**Parameters:**

- `robot` [RobotClient](https://flutter.viam.dev/viam_sdk/RobotClient-class.html) (required)
- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [VisionClient](https://flutter.viam.dev/viam_sdk/VisionClient-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/fromRobot.html).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this instance of the Vision service with the given name.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Can be used with any resource, using an arm as an example
my_arm_name = my_arm.get_resource_name("my_arm")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_resource_name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/getResourceName.html).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Fetch information about which vision methods a given vision service supports.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([Vision.Properties](https://python.viam.dev/autoapi/viam/components/audio_input/audio_input/index.html#viam.components.audio_input.audio_input.AudioInput.Properties)): The properties of the vision service.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Grab the detector you configured on your machine
my_detector = VisionClient.from_robot(robot, "my_detector")
properties = await my_detector.get_properties()
properties.detections_supported      # returns True
properties.classifications_supported # returns False
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*Properties)](https://pkg.go.dev/go.viam.com/rdk/services/vision#Properties)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await component.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using Close with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

err = myArm.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
