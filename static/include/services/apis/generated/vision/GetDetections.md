### GetDetections

{{< tabs >}}
{{% tab name="Python" %}}

Get a list of detections in the given image using the specified detector

**Parameters:**

- `image` [(viam.media.viam_rgba_plugin.Image.Image | viam.media.video.RawImage)](https://python.viam.dev/autoapi/viam/../gen/component/camera/v1/camera_pb2/index.html#viam.gen.component.camera.v1.camera_pb2.Image) (required): The image to get detections from
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[viam.proto.service.vision.Detection])](INSERT RETURN TYPE LINK): A list of 2D bounding boxes, their labels, and the confidence score of the labels, around the found objects in the next 2D image from the given camera, with the given detector applied to it.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections).

``` python {class="line-numbers linkable-line-numbers"}
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

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `img` [(Image)](https://pkg.go.dev/image#Image):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `objectdetection` [(Detection)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/vision/objectdetection#Detection):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `height` [(Int64)](https://pub.dev/documentation/fixnum/1.1.0/fixnum/Int64-class.html) (required):
- `image` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)> (required):
- `mimeType` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `width` [(Int64)](https://pub.dev/documentation/fixnum/1.1.0/fixnum/Int64-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/getDetections.html).

{{% /tab %}}
{{< /tabs >}}
