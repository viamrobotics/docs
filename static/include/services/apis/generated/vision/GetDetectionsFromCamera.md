### GetDetectionsFromCamera

{{< tabs >}}
{{% tab name="Python" %}}

Get a list of detections in the next image given a camera and a detector

**Parameters:**

- `camera_name` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The name of the camera to use for detection
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(List[viam.proto.service.vision.Detection])](INSERT RETURN TYPE LINK): A list of 2D bounding boxes, their labels, and the confidence score of the labels, around the found objects in the next 2D image from the given camera, with the given detector applied to it.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections_from_camera).

``` python {class="line-numbers linkable-line-numbers"}
camera_name = "cam1"

# Grab the detector you configured on your machine
my_detector = VisionClient.from_robot(robot, "my_detector")

# Get detections from the next image from the camera
detections = await my_detector.get_detections_from_camera(camera_name)

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `cameraName`[(string)](<INSERT PARAM TYPE LINK>)
- `extra` [(map[string]interface\{\})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `objectdetection`[(Detection)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/vision/objectdetection#objectdetection):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/vision#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `cameraName` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `extra` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.vision/VisionServiceClient/getDetectionsFromCamera.html).

{{% /tab %}}
{{< /tabs >}}
