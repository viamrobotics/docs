### GetDetectionsFromCamera

Get a list of detections from the next image from a specified camera using a configured [detector](/dev/reference/apis/services/vision/#detections).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `camera_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the camera to use for detection.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.service.vision.Detection]](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Detection)): A list of 2D bounding boxes, their labels, and the
confidence score of the labels, around the found objects in the next 2D image
from the given camera, with the given detector applied to it.

**Raises:**

- (ViamError): Raised if given an image without a specified width and height.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_detector = VisionClient.from_robot(robot=machine, "my_detector")

# Get detections for the next image from the specified camera
detections = await my_detector.get_detections_from_camera("my_camera")
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
myDetectorService, err := vision.FromProvider(machine, "my_detector")
if err != nil {
  logger.Error(err)
  return
}

// Get detections from the camera output
detections, err := myDetectorService.DetectionsFromCamera(context.Background(), "my_camera", nil)
if err != nil {
  logger.Fatalf("Could not get detections: %v", err)
}
if len(detections) > 0 {
  logger.Info(detections[0])
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `cameraName` (string) (required): The name of the camera to use for detection.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[visionApi](https://ts.viam.dev/modules/visionApi.html).[Detection](https://ts.viam.dev/classes/visionApi.Detection.html)[]>): * The list of Detections.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const vision = new VIAM.VisionClient(machine, 'my_vision');
const detections = await vision.getDetectionsFromCamera('my_camera');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/VisionClient.html#getdetectionsfromcamera).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `cameraName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[Detection](https://flutter.viam.dev/viam_protos.service.vision/Detection-class.html)\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var detections = await myVisionService.detectionsFromCamera('myWebcam');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/detectionsFromCamera.html).

{{% /tab %}}
{{< /tabs >}}

### GetDetections

Get a list of detections from a given image using a configured [detector](/dev/reference/apis/services/vision/#detections).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `image` ([viam.media.video.ViamImage](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.ViamImage)) (required): The image to get detections for.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.service.vision.Detection]](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Detection)): A list of 2D bounding boxes, their labels, and the
confidence score of the labels, around the found objects in the next 2D image
from the given camera, with the given detector applied to it.

**Raises:**

- (ViamError): Raised if given an image without a specified width and height.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=machine, "my_camera")
my_detector = VisionClient.from_robot(robot=machine, "my_detector")

# Get an image from the camera
img = await my_camera.get_image()

# Get detections for that image
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
 // add "go.viam.com/rdk/utils" to imports to use this code snippet

  myCam, err := camera.FromProvider(machine, "my_camera")
  if err != nil {
    logger.Error(err)
    return
  }
  // Get an image from the camera decoded as an image.Image
  img, err = camera.DecodeImageFromCamera(context.Background(), utils.MimeTypeJPEG, nil, myCam)

  myDetectorService, err := vision.FromProvider(machine, "my_detector")
  if err != nil {
    logger.Error(err)
    return
  }
  // Get the detections from the image
  detections, err := myDetectorService.Detections(context.Background(), img, nil)
  if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
  }
  if len(detections) > 0 {
    logger.Info(detections[0])
  }
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `image` (Uint8Array) (required): The image from which to get detections.
- `width` (number) (required): The width of the image.
- `height` (number) (required): The height of the image.
- `mimeType` ([MimeType](https://ts.viam.dev/types/MimeType.html)) (required): The MimeType of the image.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[visionApi](https://ts.viam.dev/modules/visionApi.html).[Detection](https://ts.viam.dev/classes/visionApi.Detection.html)[]>): * The list of Detections.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const camera = new VIAM.CameraClient(machine, 'my_camera');
const vision = new VIAM.VisionClient(machine, 'my_vision');

const mimeType = 'image/jpeg';
const image = await camera.getImage(mimeType);
const detections = await vision.getDetections(
  image,
  600,
  600,
  mimeType
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/VisionClient.html#getdetections).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `image` [ViamImage](https://flutter.viam.dev/viam_sdk/ViamImage-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[Detection](https://flutter.viam.dev/viam_protos.service.vision/Detection-class.html)\>\>

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

Get a list of classifications from the next image from a specified camera using a configured [classifier](/dev/reference/apis/services/vision/#classifications).

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
my_classifier = VisionClient.from_robot(robot=machine, "my_classifier")

# Get the 2 classifications with the highest confidence scores for the next image from the camera
classifications = await my_classifier.get_classifications_from_camera(
    "my_camera", 2)
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
myClassifierService, err := vision.FromProvider(machine, "my_classifier")
if err != nil {
  logger.Error(err)
  return
}
// Get the 2 classifications with the highest confidence scores from the camera output
classifications, err := myClassifierService.ClassificationsFromCamera(context.Background(), "my_camera", 2, nil)
if err != nil {
  logger.Fatalf("Could not get classifications: %v", err)
}
if len(classifications) > 0 {
  logger.Info(classifications[0])
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `cameraName` (string) (required): The name of the camera to use for classification.
- `count` (number) (required): The number of Classifications requested.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[visionApi](https://ts.viam.dev/modules/visionApi.html).[Classification](https://ts.viam.dev/classes/visionApi.Classification.html)[]>): * The list of Classifications.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const vision = new VIAM.VisionClient(machine, 'my_vision');
const classifications = await vision.getClassificationsFromCamera(
  'my_camera',
  10
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/VisionClient.html#getclassificationsfromcamera).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `cameraName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `count` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[Classification](https://flutter.viam.dev/viam_protos.service.vision/Classification-class.html)\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var classifications = await myVisionService.classificationsFromCamera('myWebcam', 2);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/classificationsFromCamera.html).

{{% /tab %}}
{{< /tabs >}}

### GetClassifications

Get a list of classifications from a given image using a configured [classifier](/dev/reference/apis/services/vision/#classifications).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `image` ([viam.media.video.ViamImage](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.ViamImage)) (required): The image to get detections for.
- `count` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The number of classifications desired.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.service.vision.Classification]](https://python.viam.dev/autoapi/viam/proto/service/vision/index.html#viam.proto.service.vision.Classification)): The list of Classifications.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=machine, "my_camera")
my_classifier = VisionClient.from_robot(robot=machine, "my_classifier")

# Get an image from the camera
img = await my_camera.get_image()

# Get the 2 classifications with the highest confidence scores for the image
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
 // add "go.viam.com/rdk/utils" to imports to use this code snippet

  myCam, err := camera.FromProvider(machine, "my_camera")
  if err != nil {
    logger.Error(err)
    return
  }
  // Get an image from the camera decoded as an image.Image
  img, err = camera.DecodeImageFromCamera(context.Background(), utils.MimeTypeJPEG, nil, myCam)

  myClassifierService, err := vision.FromProvider(machine, "my_classifier")
  if err != nil {
    logger.Error(err)
    return
  }
  // Get the 2 classifications with the highest confidence scores from the image
  classifications, err := myClassifierService.Classifications(context.Background(), img, 2, nil)
  if err != nil {
    logger.Fatalf("Could not get classifications: %v", err)
  }
  if len(classifications) > 0 {
    logger.Info(classifications[0])
  }
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `image` (Uint8Array) (required): The image from which to get classifications.
- `width` (number) (required): The width of the image.
- `height` (number) (required): The height of the image.
- `mimeType` ([MimeType](https://ts.viam.dev/types/MimeType.html)) (required): The MimeType of the image.
- `count` (number) (required): The number of Classifications requested.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[visionApi](https://ts.viam.dev/modules/visionApi.html).[Classification](https://ts.viam.dev/classes/visionApi.Classification.html)[]>): * The list of Classifications.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const camera = new VIAM.CameraClient(machine, 'my_camera');
const vision = new VIAM.VisionClient(machine, 'my_vision');

const mimeType = 'image/jpeg';
const image = await camera.getImage(mimeType);
const classifications = await vision.getClassifications(
  image,
  600,
  600,
  mimeType,
  10
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/VisionClient.html#getclassifications).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `image` [ViamImage](https://flutter.viam.dev/viam_sdk/ViamImage-class.html) (required)
- `count` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[Classification](https://flutter.viam.dev/viam_protos.service.vision/Classification-class.html)\>\>

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

Get a list of 3D point cloud objects and associated metadata in the latest picture from a 3D camera (using a specified [segmenter](/dev/reference/apis/services/vision/#segmentations)).

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

my_segmenter = VisionClient.from_robot(robot=machine, "my_segmenter")
# Get the objects from the camera output
objects = await my_segmenter.get_object_point_clouds("my_camera")
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
mySegmenterService, err := vision.FromProvider(machine, "my_segmenter")
if err != nil {
  logger.Error(err)
  return
}
// Get the objects from the camera output
objects, err := mySegmenterService.GetObjectPointClouds(context.Background(), "my_camera", nil)
if err != nil {
  logger.Fatalf("Could not get point clouds: %v", err)
}
if len(objects) > 0 {
  logger.Info(objects[0])
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `cameraName` (string) (required): The name of the camera.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[commonApi](https://ts.viam.dev/modules/commonApi.html).[PointCloudObject](https://ts.viam.dev/classes/commonApi.PointCloudObject.html)[]>): * The list of PointCloudObjects.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const vision = new VIAM.VisionClient(machine, 'my_vision');
const pointCloudObjects =
  await vision.getObjectPointClouds('my_camera');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/VisionClient.html#getobjectpointclouds).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `cameraName` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[PointCloudObject](https://flutter.viam.dev/viam_protos.common.common/PointCloudObject-class.html)\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var ptCloud = await myVisionService.objectPointClouds('myCamera');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/objectPointClouds.html).

{{% /tab %}}
{{< /tabs >}}

### CaptureAllFromCamera

Get the next image, detections, classifications, and objects all together, given a camera name.
Used for visualization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `camera_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the camera to use for detection.
- `return_image` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Ask the vision service to return the camera’s latest image.
- `return_classifications` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Ask the vision service to return its latest classifications.
- `return_detections` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Ask the vision service to return its latest detections.
- `return_object_point_clouds` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): Ask the vision service to return its latest 3D segmentations.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.services.vision.vision.CaptureAllResult](https://python.viam.dev/autoapi/viam/services/vision/vision/index.html#viam.services.vision.vision.CaptureAllResult)): A class that stores all potential returns from the vision service.
It can return the image from the camera along with its associated detections, classifications,
and objects, as well as any extra info the model may provide.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_detector = VisionClient.from_robot(machine, "my_detector")

# Get the captured data for a camera
result = await my_detector.capture_all_from_camera(
    "my_camera",
    return_image=True,
    return_detections=True,
)
image = result.image
detections = result.detections
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.capture_all_from_camera).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cameraName` [(string)](https://pkg.go.dev/builtin#string): The name of the camera to use for detection.
- `opts` [(viscapture.CaptureOptions)](https://pkg.go.dev/go.viam.com/rdk/vision/viscapture#CaptureOptions): Additional options to provide if desired.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(viscapture.VisCapture)](https://pkg.go.dev/go.viam.com/rdk/vision/viscapture#VisCapture): A class that stores all potential returns from the vision service. It can return the image from the camera along with its associated detections, classifications, and objects, as well as any extra info the model may provide.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// The data to capture and return from the camera
captOpts := viscapture.CaptureOptions{
  ReturnImage: true,
  ReturnDetections: true,
}
// Get the captured data for a camera
capture, err := visService.CaptureAllFromCamera(context.Background(), "my_camera", captOpts, nil)
if err != nil {
  logger.Fatalf("Could not get capture data from vision service: %v", err)
}
image := capture.Image
detections := capture.Detections
classifications := capture.Classifications
objects := capture.Objects
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `cameraName` (string) (required): The name of the camera to use for classification,
  detection, and segmentation.
- `__namedParameters` (CaptureAllOptions) (required)
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise< { classifications: [visionApi](https://ts.viam.dev/modules/visionApi.html).[Classification](https://ts.viam.dev/classes/visionApi.Classification.html)[]; detections: [visionApi](https://ts.viam.dev/modules/visionApi.html).[Detection](https://ts.viam.dev/classes/visionApi.Detection.html)[]; extra: undefined | [Struct](https://ts.viam.dev/classes/Struct.html); image: undefined | [Image](https://ts.viam.dev/classes/cameraApi.Image.html); objectPointClouds: [commonApi](https://ts.viam.dev/modules/commonApi.html).[PointCloudObject](https://ts.viam.dev/classes/commonApi.PointCloudObject.html)[]; },>): * The requested image, classifications, detections, and 3d point
cloud objects.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const vision = new VIAM.VisionClient(machine, 'my_vision');
const captureAll = await vision.captureAllFromCamera('my_camera', {
  returnImage: true,
  returnClassifications: true,
  returnDetections: true,
  returnObjectPointClouds: true,
});
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/VisionClient.html#captureallfromcamera).

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
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own vision service and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_vision_svc = VisionClient.from_robot(robot=machine, "my_vision_svc")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

await my_vision_svc.do_command(command=my_command)
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
myVisionSvc, err := vision.FromRobot(machine, "my_vision_svc")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myVisionSvc.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `command` ([Struct](https://ts.viam.dev/classes/Struct.html)) (required): The command to execute.
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[JsonValue](https://ts.viam.dev/types/JsonValue.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
import { Struct } from '@viamrobotics/sdk';

const result = await resource.doCommand(
  Struct.fromJson({
    myCommand: { key: 'value' },
  })
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/VisionClient.html#docommand).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example using doCommand with an arm component
const command = {'cmd': 'test', 'data1': 500};
var result = myArm.doCommand(command);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this instance of the vision service.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_vision_svc_name = VisionClient.get_resource_name("my_vision_svc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myVisionSvc, err := vision.FromRobot(machine, "my_vision_svc")

err = myVisionSvc.Name()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (string): The name of the resource.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
vision.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/VisionClient.html#name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
final myVisionServiceResourceName = myVisionService.getResourceName("my_vision_service");
```

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
my_detector = VisionClient.from_robot(robot=machine, "my_detector")
properties = await my_detector.get_properties()
detections_supported = properties.detections_supported
classifications_supported = properties.classifications_supported
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
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise< { classificationsSupported: boolean; detectionsSupported: boolean; objectPointCloudsSupported: boolean; },>): * The properties of the vision service.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const vision = new VIAM.VisionClient(machine, 'my_vision');
const properties = await vision.getProperties();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/VisionClient.html#getproperties).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[VisionProperties](https://flutter.viam.dev/viam_sdk/VisionProperties.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var properties = await myVisionService.properties();
properties.detections_supported
properties.classifications_supported
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/VisionClient/properties.html).

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
my_vision_svc = VisionClient.from_robot(robot=machine, name="my_vision_svc")
await my_vision_svc.close()
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
myVisionSvc, err := vision.FromRobot(machine, "my_vision_svc")

err = myVisionSvc.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
