### GetClassificationsFromCamera

{{< tabs >}}
{{% tab name="Python" %}}

Get a list of classifications in the next image given a camera and a classifier

**Parameters:**

- `camera_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The name of the camera to use for detection
- `count` [(int)](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) (required): The number of classifications desired
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(List[viam.proto.service.vision.Classification])](INSERT RETURN TYPE LINK): The list of Classifications

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_classifications_from_camera).

``` python {class="line-numbers linkable-line-numbers"}
camera_name = "cam1"

# Grab the classifier you configured on your machine
my_classifier = VisionClient.from_robot(robot, "my_classifier")

# Get the 2 classifications with the highest confidence scores from the next image from the camera
classifications = await my_classifier.get_classifications_from_camera(
    camera_name, 2)

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `cameraName`[(string)](<INSERT PARAM TYPE LINK>)
- `n`[(int)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.
- [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- `classification`[(Classifications)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/vision/classification#classification):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `cameraName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `n` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/getClassificationsFromCamera.html).

{{% /tab %}}
{{< /tabs >}}
