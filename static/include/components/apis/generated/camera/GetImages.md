### GetImages

{{< tabs >}}
{{% tab name="Python" %}}

Get simultaneous images from different imagers, along with associated metadata. This should not be used for getting a time series of images from the same imager.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(Tuple[List[viam.media.video.NamedImage], viam.proto.common.ResponseMetadata])](INSERT RETURN TYPE LINK):  A tuple containing two values; the first [0] a list of images returned from thecamera system, and the second [1] the metadata associated with this response.   

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_images).

``` python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=robot, name="my_camera")

images, metadata = await my_camera.get_images()
img0 = images[0].image
timestamp = metadata.captured_at

```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):

**Returns:**

- [(NamedImage)](<INSERT PARAM TYPE LINK>)
- `resource`[(ResponseMetadata)](https://pkg.go.dev/go.viam.com/rdk@v0.26.0/resource#resource):
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.component.camera/CameraServiceClient/getImages.html).

{{% /tab %}}
{{< /tabs >}}
