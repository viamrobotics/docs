### GetClassifications

{{< tabs >}}
{{% tab name="Python" %}}

Get a list of classifications in the given image using the specified classifier

**Parameters:**

- `image` [(viam.media.viam_rgba_plugin.Image.Image | viam.media.video.RawImage)](https://python.viam.dev/autoapi/viam/../gen/component/camera/v1/camera_pb2/index.html#viam.gen.component.camera.v1.camera_pb2.Image) (required): The image to get detections from
- `count` [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): The number of classifications desired
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[viam.proto.service.vision.Classification])](INSERT RETURN TYPE LINK): The list of Classifications

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_classifications).

``` python {class="line-numbers linkable-line-numbers"}
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

- `ctx`[(Context)](https://pkg.go.dev/context#Context):
- `img`[(Image)](https://pkg.go.dev/image#Image):
- `n`[(int)](https://pkg.go.dev/builtin#int):
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.
- [())](<INSERT PARAM TYPE LINK>):

**Returns:**

- `classification`[(Classifications)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/vision/classification#Classifications):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `height` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html) (required):
- `image` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)> (required):
- `mimeType` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `n` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `width` [(int)](https://api.flutter.dev/flutter/dart-core/int-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/getClassifications.html).

{{% /tab %}}
{{< /tabs >}}
