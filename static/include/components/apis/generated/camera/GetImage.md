### GetImage

{{< tabs >}}
{{% tab name="Python" %}}

Get the next image from the camera as an Image or RawImage. Be sure to close the image when finished.

**Parameters:**

- `mime_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) (required): The desired mime type of the image. This does not guarantee output type
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(PIL.Image.Image | viam.components.camera.RawImage)](INSERT RETURN TYPE LINK): The frame

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_image).

``` python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=robot, name="my_camera")

# Assume "frame" has a mime_type of "image/vnd.viam.dep"
frame = await my_camera.get_image(mime_type = CameraMimeType.VIAM_RAW_DEPTH)

# Convert "frame" to a standard 2D image representation.
# Remove the 1st 3x8 bytes and reshape the raw bytes to List[List[Int]].
standard_frame = frame.bytes_to_depth_array()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `gostream` [(ErrorHandler)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/gostream#ErrorHandler):

**Returns:**

- `gostream` [(VideoStream)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/gostream#VideoStream):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `mimeType` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.camera/CameraServiceClient/getImage.html).

{{% /tab %}}
{{< /tabs >}}
