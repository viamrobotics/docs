### GetImage

Return an image from the camera.
You can request a specific MIME type but the returned MIME type is not guaranteed.
If the server does not know how to return the specified MIME type, the server returns the image in another format instead.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `mime_type` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The desired mime type of the image. This does not guarantee output type.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.media.video.ViamImage](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.ViamImage)): The frame.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=robot, name="my_camera")

# Assume "frame" has a mime_type of "image/vnd.viam.dep"
frame = await my_camera.get_image(mime_type = CameraMimeType.VIAM_RAW_DEPTH)

# Convert "frame" to a standard 2D image representation.
# Remove the 1st 3x8 bytes and reshape the raw bytes to List[List[Int]].
standard_frame = frame.bytes_to_depth_array()
```

If the `mime_type` of your image is `image/vnd.viam.dep`, pass the returned image data to the Viam Python SDK's [`ViamImage.bytes_to_depth_array()`](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.ViamImage.bytes_to_depth_array) method to decode the raw image data to a standard 2D image representation.

In addition, the Python SDK provides the helper functions `viam_to_pil_image` and `pil_to_viam_image` to decode the `ViamImage` into a [`PIL Image`](https://omz-software.com/pythonista/docs/ios/Image.html) and vice versa.

For example:

```python {class="line-numbers linkable-line-numbers"}
# from viam.media.utils.pil import pil_to_viam_image, viam_to_pil_image
# < ADD ABOVE IMPORT TO BEGINNING OF PROGRAM >

# Get the ViamImage from your camera.
frame = await my_camera.get_image()

# Convert "frame" to a PIL Image representation.
pil_frame = viam_to_pil_image(frame)

# Use methods from the PIL Image class to get size.
x, y = pil_frame.size[0], pil_frame.size[1]
# Crop image to get only the left two fifths of the original image.
cropped_pil_frame = pil_frame.crop((0, 0, x / 2.5, y))

# Convert back to ViamImage.
cropped_frame = pil_to_viam_image(cropped_pil_frame)
```

{{% alert title="Tip" color="tip" %}}

Be sure to close the image when finished.

{{% /alert %}}

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_image).

{{% /tab %}}
{{% tab name="Go" %}}

{{% alert title="Info" color="info" %}}

Unlike most Viam [component APIs](/appendix/apis/#component-apis), the methods of the Go camera client do not map exactly to the names of the other SDK's camera methods.
To get an image in the Go SDK, you first need to construct a `Stream` and then you can get the next image from that stream.

{{% /alert %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `errHandlers` [(...gostream.ErrorHandler)](https://pkg.go.dev/go.viam.com/rdk/gostream#ErrorHandler): A handler for errors allowing for logic based on consecutively retrieved errors.

**Returns:**

- [(gostream.VideoStream)](https://pkg.go.dev/go.viam.com/rdk/gostream#VideoStream): A `VideoStream` that streams video until closed.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(machine, "my_camera")

// gets the stream from a camera
stream, err := myCamera.Stream(context.Background())

// gets an image from the camera stream
img, release, err := stream.Next(context.Background())
defer release()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `mimeType` [MimeType](https://flutter.viam.dev/viam_sdk/MimeType-class.html)? (optional)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[ViamImage](https://flutter.viam.dev/viam_sdk/ViamImage-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var nextImage = await myCamera.image();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Camera/image.html).

{{% /tab %}}
{{< /tabs >}}

### GetImages

{{% alert title="Usage" color="note" %}}
Intended specifically for use with cameras that support simultaneous depth and color image streams, like the [Intel RealSense](https://app.viam.com/module/viam/realsense) or the [Luxonis OAK-D](https://app.viam.com/module/viam/oak-d).
If your camera does not have multiple imagers, this method will work without capturing multiple images simultaneously.

You can use the [`rgb-d-overlay` module](https://app.viam.com/module/viam/rgb-d-overlay) to view and compare the camera streams returned by this method.
See the [module readme](https://github.com/viam-labs/rgb-d-overlay) for further instructions.
{{% /alert %}}

Get simultaneous images from different imagers, along with associated metadata.
The multiple images returned from `GetImages()` do not represent a time series of images.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[List[[video.NamedImage](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.NamedImage)], [common.ResponseMetadata](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResponseMetadata)]): A tuple containing two values; the first [0] a list of images returned from the camera system, and the second [1] the metadata associated with this response.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=robot, name="my_camera")

images, metadata = await my_camera.get_images()
img0 = images[0].image
timestamp = metadata.captured_at
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_images).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [([]NamedImage)](https://pkg.go.dev/go.viam.com/rdk/components/camera#NamedImage): The list of images returned from the camera system, with the name of the imager associated with the image.
- [(resource.ResponseMetadata)](https://pkg.go.dev/go.viam.com/rdk/resource#ResponseMetadata): The metadata, which holds the timestamp of when the data was captured.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(machine, "my_camera")

images, metadata, err := myCamera.Images(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

{{% /tab %}}
{{< /tabs >}}

### GetPointCloud

Get a point cloud from the camera as bytes with a MIME type describing the structure of the data.
The consumer of this call should decode the bytes into the format suggested by the MIME type.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[[bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): A tuple containing two values; the first [0] the pointcloud data, and the second [1] the mimetype of the pointcloud (for example, PCD).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
import numpy as np
import open3d as o3d

data, _ = await camera.get_point_cloud()

# write the point cloud into a temporary file
with open("/tmp/pointcloud_data.pcd", "wb") as f:
    f.write(data)
pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
points = np.asarray(pcd.points)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_point_cloud).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(pointcloud.PointCloud)](https://pkg.go.dev/go.viam.com/rdk/pointcloud#PointCloud): A general purpose container of points. It does not dictate whether or not the cloud is sparse or dense.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(machine, "my_camera")

// gets the properties from a camera
properties, err := myCamera.Properties(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[ViamImage](https://flutter.viam.dev/viam_sdk/ViamImage-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var nextPointCloud = await myCamera.pointCloud();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Camera/pointCloud.html).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get the camera intrinsic parameters and camera distortion, as well as whether the camera supports returning point clouds.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (viam.components.camera.Camera.Properties): The properties of the camera.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=robot, name="my_camera")

properties = await my_camera.get_properties()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(Properties)](https://pkg.go.dev/go.viam.com/rdk/components/camera#Properties): Properties of the particular implementation of a camera.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[CameraProperties](https://flutter.viam.dev/viam_sdk/CameraProperties.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var cameraProperties = await myCamera.properties();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Camera/properties.html).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For native models, model-specific commands are covered with each model's documentation.
If you are implementing your own camera and adding features that have no native API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Raises:**

- (NotImplementedError): Raised if the Resource does not support arbitrary commands.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
command = {"cmd": "test", "data1": 500}
result = component.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.do_command).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example using doCommand with an arm component
const command = {'cmd': 'test', 'data1': 500};
var result = myArm.doCommand(command);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Resource/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the camera in its current configuration, in the [frame](/services/frame-system/) of the camera.
The [motion](/services/motion/) and [navigation](/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry)): The geometries associated with the Component.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
geometries = await component.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_geometries).

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

- [Camera](https://flutter.viam.dev/viam_sdk/Camera-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Camera/fromRobot.html).

{{% /tab %}}
{{< /tabs >}}

### Name

Get the `ResourceName` for this camera with the given name.

{{< tabs >}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Camera/getResourceName.html).

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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(machine, "my_camera")

err = myCamera.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#VideoSource).

{{% /tab %}}
{{< /tabs >}}
