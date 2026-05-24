### GetImages

{{% alert title="Usage" color="note" %}}

You can use the [`rgb-d-overlay` module](https://app.viam.com/module/viam/rgb-d-overlay) to view and compare the camera streams returned by this method.
See the [module readme](https://github.com/viam-labs/rgb-d-overlay) for further instructions.
{{% /alert %}}

`GetImages` is used for getting simultaneous images from different imagers from 3D cameras along with associated metadata, and single images from non-3D cameras, for example webcams, RTSP cameras, etc. in the image list in the response.
Multiple images returned from `GetImages()` do not represent a time series of images.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `filter_source_names` (Sequence[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]) (optional): The filter_source_names parameter can be used to filter only the images from the specified source names. When unspecified, all images are returned.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[Sequence[[video.NamedImage](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.NamedImage)], [common.ResponseMetadata](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResponseMetadata)]): :   A tuple containing two values; the first [0] a list of images
    returned from the camera system, and the second [1] the metadata associated with this response.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=machine, name="my_camera")

images, metadata = await my_camera.get_images()
first_image = images[0]
timestamp = metadata.captured_at
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_images).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `filterSourceNames` [([]string)](https://pkg.go.dev/builtin#string)
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]NamedImage)](https://pkg.go.dev/go.viam.com/rdk/components/camera#NamedImage): The list of images returned from the camera system, with the name of the imager associated with the image.
- [(resource.ResponseMetadata)](https://pkg.go.dev/go.viam.com/rdk/resource#ResponseMetadata): The metadata, which holds the timestamp of when the data was captured.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromProvider(machine, "my_camera")

images, metadata, err := myCamera.Images(context.Background(), nil, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#ImagesSource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `filterSourceNames` (string) (optional): A list of source names to filter the images by.
  If empty or undefined, all images will be returned.
- `extra` (None) (optional): Extra parameters to pass to the camera.
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise< { images: { image: Uint8Array; mimeType: string; sourceName: string }[]; metadata: ResponseMetadata; }, >)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const camera = new VIAM.CameraClient(machine, 'my_camera');
const images = await camera.getImages();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/CameraClient.html#getimages).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `filterSourceNames` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html)>? (optional)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[GetImagesResult](https://flutter.viam.dev/viam_sdk/GetImagesResult-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
const camera = new VIAM.CameraClient(machine, 'my_camera');
const images = await camera.getImages();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Camera/getImages.html).

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

- (Tuple[[bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects), [str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)]): :   A tuple containing two values; the first [0] the pointcloud data,
    and the second [1] the mimetype of the pointcloud (for example, PCD).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
import numpy as np
import open3d as o3d

my_camera = Camera.from_robot(robot=machine, name="my_camera")

data, _ = await my_camera.get_point_cloud()

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
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(pointcloud.PointCloud)](https://pkg.go.dev/go.viam.com/rdk/pointcloud#PointCloud): A general purpose container of points. It does not dictate whether or not the cloud is sparse or dense.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromProvider(machine, "my_camera")

// gets the next point cloud from a camera
pointCloud, err := myCamera.NextPointCloud(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#PointCloudSource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<Uint8Array>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const camera = new VIAM.CameraClient(machine, 'my_camera');
const pointCloud = await camera.getPointCloud();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/CameraClient.html#getpointcloud).

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

- ([viam.components.camera.Camera.Properties](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.Properties)): :   The properties of the camera, including intrinsic parameters, distortion parameters,
    supported mime types, and optionally extrinsic parameters (position relative to a reference frame).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=machine, name="my_camera")

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

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#Camera).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[cameraApi](https://ts.viam.dev/modules/cameraApi.html).[GetPropertiesResponse](https://ts.viam.dev/classes/cameraApi.GetPropertiesResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const camera = new VIAM.CameraClient(machine, 'my_camera');
const properties = await camera.getProperties();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/CameraClient.html#getproperties).

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
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own camera and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/reference/sdks/docommand/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): :   Result of the executed command.

**Raises:**

- (NotImplementedError): Raised if the Resource does not support arbitrary commands.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=machine, name="my_camera")
command = {"cmd": "test", "data1": 500}
result = await my_camera.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.do_command).

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
myCamera, err := camera.FromProvider(machine, "my_camera")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myCamera.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `command` ([Struct](https://ts.viam.dev/classes/Struct.html)) (required): The command to execute. Accepts either a [Struct](https://ts.viam.dev/classes/Struct.html) or
  a plain object, which will be converted automatically.
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[JsonValue](https://ts.viam.dev/types/JsonValue.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
// Plain object (recommended)
const result = await resource.doCommand({
  myCommand: { key: 'value' },
});

// Struct (still supported)
import { Struct } from '@viamrobotics/sdk';

const result = await resource.doCommand(
  Struct.fromJson({ myCommand: { key: 'value' } })
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/CameraClient.html#docommand).

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

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Resource/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the camera in its current configuration, in the [frame](/reference/services/frame-system/) of the camera.
The [motion](/reference/services/motion/) and [navigation](/reference/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([Sequence[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry)): :   The geometries associated with the Component.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=machine, name="my_camera")
geometries = await my_camera.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_geometries).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]spatialmath.Geometry)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): The geometries associated with this resource, in any order.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using Geometries with an camera component.
myCamera, err := camera.FromProvider(machine, "my_camera")

geometries, err := myCamera.Geometries(context.Background(), nil)

if len(geometries) > 0 {
   // Get the center of the first geometry
   elem := geometries[0]
   fmt.Println("Pose of the first geometry's center point:", elem.Pose())
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Shaped).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[commonApi](https://ts.viam.dev/modules/commonApi.html).[Geometry](https://ts.viam.dev/classes/commonApi.Geometry.html)[]>)

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/CameraClient.html#getgeometries).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this camera.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): :   The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_camera_name = Camera.get_resource_name("my_camera")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromProvider(machine, "my_camera")

err = myCamera.Name()
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
camera.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/CameraClient.html#name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
final myCameraResourceName = myCamera.getResourceName("my_camera");
```

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
my_camera = Camera.from_robot(robot=machine, name="my_camera")
await my_camera.close()
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
myCamera, err := camera.FromProvider(machine, "my_camera")

err = myCamera.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
