---
title: "Camera Component"
linkTitle: "Camera"
childTitleEndOverwrite: "Camera Component"
weight: 40
type: "docs"
description: "A camera captures 2D or 3D images and sends them to the computer controlling the machine."
no_list: true
tags: ["camera", "components"]
icon: true
images: ["/icons/components/camera.svg"]
modulescript: true
aliases:
  - "/tutorials/configure-a-camera"
  - "/components/camera/"
# SMEs: Bijan, vision team
---

A camera component is a source of 2D and/or 3D images.
You can use the component to configure a webcam, lidar, time-of-flight sensor, or another type of camera.

The API for camera components allows you to:

- Request single images or a stream in 2D color, or display z-depth.

- Request a point cloud.
  Each 3D point cloud image consists of a set of coordinates (x,y,z) representing depth in mm.

The configuration of your camera component depends on your camera model.
You can use different models to:

- Configure physical cameras that generate images or point clouds.
- Combine streams from multiple cameras into one.
- Transform and process images.

## Related services

{{< cards >}}
{{< relatedcard link="/data/" >}}
{{< relatedcard link="/ml/vision/" >}}
{{< relatedcard link="/mobility/frame-system/" >}}
{{< relatedcard link="/mobility/slam/" >}}
{{< relatedcard link="/ml/deploy/" alt_title="Machine Learning" >}}
{{< /cards >}}

## Supported models

To use your camera with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your camera.

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`ffmpeg`](ffmpeg/) | Uses a camera, a video file, or a stream as a camera. |
| [`image_file`](image-file/) | Gets color and depth images frames from a file path. |
| [`velodyne`](velodyne/) | Uses velodyne lidar. |
| [`webcam`](webcam/) | A standard camera that streams camera data. |
| [`rtsp`](rtsp/) | A streaming camera with an MJPEG track. |
| [`fake`](fake/) | A camera model for testing. |
| [`single_stream`](single-stream/) | A HTTP client camera that streams image data from an HTTP endpoint. |
| [`dual_stream`](dual-stream/) | A HTTP client camera that combines the streams of two camera servers to create colorful point clouds. |
| [`join_color_depth`](join-color-depth/) | Joins the outputs of a color and depth camera already registered in your config to create a third "camera" that outputs the combined and aligned image. |
| [`align_color_depth_extrinsics`](align-color-depth-extrinsics/) | Uses the intrinsics of the color and depth camera, as well as the extrinsic pose between them, to align two images. |
| [`align_color_depth_homography`](align-color-depth-homography/) | Uses a homography matrix to align the color and depth images. |
| [`join_pointclouds`](join-pointclouds/) | Combines the point clouds from multiple camera sources and projects them to be from the point of view of target_frame. |
| [`transform`](transform/) | A pipeline for applying transformations to an input image source. |
| [`ultrasonic`](ultrasonic/) | The [HC-S204](https://www.sparkfun.com/products/15569) ultrasonic distance sensor. |

### Modular resources

{{<modular-resources api="rdk:component:camera" type="camera">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Control your camera with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a camera called `"my_camera"` configured as a component of your machine.
If your camera has a different name, change the `name` in the code.

Be sure to import the camera package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.camera import Camera
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/camera"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The camera component supports the following methods:

{{< readfile "/static/include/components/apis/camera.md" >}}

### GetImage

Returns an image from the camera.
You can request a specific MIME type but the returned MIME type is not guaranteed.
If the server does not know how to return the specified MIME type, the server returns the image in another format instead.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `mime_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The requested MIME type of the image.
  The returned MIME type is not guaranteed to match the image output type:
  If the requested MIME type has `+lazy` appended to it or the requested MIME type is not supported for decoding/encoding, `GetImage` returns a [`RawImage`](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.RawImage) instead.

**Returns:**

- ([PIL.Image](https://pillow.readthedocs.io/en/stable/reference/Image.html) or [RawImage](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.RawImage)): The requested frame.

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=robot, name="my_camera")

frame = await my_camera.get_image(mime_type="image/jpeg")
```

<br>

If the `mime_type` of your image is `image/vnd.viam.dep`, pass the returned image data to the Viam Python SDK's [`RawImage.bytes_to_depth_array()`](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.RawImage.bytes_to_depth_array) method to decode the raw image data to a standard 2D image representation.

For example:

```python {class="line-numbers linkable-line-numbers"}
# Assume "frame" has a mime_type of "image/vnd.viam.dep"
frame = await my_camera.get_image()

# Convert "frame" to a standard 2D image representation.
# Remove the 1st 3x8 bytes and reshape the raw bytes to List[List[Int]].
standard_frame = frame.bytes_to_depth_array()
```

{{% alert title="Tip" color="tip" %}}

Be sure to close the image when finished.

{{% /alert %}}

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.get_image).

{{% /tab %}}
{{% tab name="Go" %}}

{{% alert title="Info" color="info" %}}

Unlike most Viam [component APIs](/build/program/apis/#component-apis), the methods of the Go camera client do not map exactly to the names of the other SDK's camera methods.
To get an image in the Go SDK, you first need to construct a `Stream` and then you can get the next image from that stream.

{{% /alert %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `errHandlers` [(ErrorHandler)](https://pkg.go.dev/github.com/viamrobotics/gostream#ErrorHandler): A handler for errors allowing for logic based on consecutively retrieved errors).

**Returns:**

- [(gostream.VideoStream)](https://pkg.go.dev/github.com/viamrobotics/gostream): A `VideoStream` that streams video until closed.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(robot, "my_camera")

// gets the stream from a camera
stream, err := myCamera.Stream(context.Background())

// gets an image from the camera stream
img, release, err := stream.Next(context.Background())
defer release()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#Camera).

{{% /tab %}}
{{< /tabs >}}

### GetImages

{{% alert title="Usage" color="note" %}}
Intended specifically for use with cameras that support simultaneous depth and color image streams, like the [Intel RealSense](https://app.viam.com/module/viam/realsense) or the [Luxonis OAK-D](https://app.viam.com/module/viam/oak-d).
If your camera does not have multiple imagers, this method will work without capturing multiple images simultaneously.
{{% /alert %}}

Get simultaneous images from different imagers, along with associated metadata.
The multiple images returned from `GetImages()` do not represent a time series of images.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- [(List[NamedImage])](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.NamedImage): The list of images returned from the camera system.
- [(ResponseMetadata)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResponseMetadata): The metadata timestamp with this response.

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=robot, name="my_camera")

images, metadata = await my_camera.get_images()
img0 = images[0].image
timestamp = metadata.captured_at
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.get_images).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [([]camera.NamedImage)](https://pkg.go.dev/go.viam.com/rdk/components/camera#NamedImage): The list of images returned from the camera system, with the name of the imager associated with the image.
- [(resource.ResponseMetadata)](https://pkg.go.dev/go.viam.com/rdk/resource#ResponseMetadata): The metadata, which holds the timestamp of when the data was captured.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(robot, "my_camera")

images, metadata, err := myCamera.Images(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#Camera).

{{% /tab %}}
{{< /tabs >}}

### GetPointCloud

Get a point cloud from the camera as bytes with a MIME type describing the structure of the data.
The consumer of this call should decode the bytes into the format suggested by the MIME type.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- [(Tuple[bytes,str])](https://docs.python.org/3/library/stdtypes.html#bytes): The pointcloud data as bytes paired with a string representing the MIME type of the pointcloud (for example, PCD).

To deserialize the returned information into a numpy array, use the Open3D library:

```python {class="line-numbers linkable-line-numbers"}
import numpy as np
import open3d as o3d

my_camera = Camera.from_robot(robot=robot, name="my_camera")

data, _ = await my_camera.get_point_cloud()

# write the point cloud into a temporary file
with open("/tmp/pointcloud_data.pcd", "wb") as f:
    f.write(data)
pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
points = np.asarray(pcd.points)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.get_point_cloud).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(pointcloud.PointCloud)](https://pkg.go.dev/go.viam.com/rdk/pointcloud#PointCloud): A general purpose container of points.
  It does not dictate whether or not the cloud is sparse or dense.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(robot, "my_camera")

pointCloud, err := myCamera.NextPointCloud(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#Camera).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get the camera intrinsic parameters and camera distortion, as well as whether the camera supports returning point clouds.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- [(Properties)](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.Properties): The properties of the camera.

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=robot, name="my_camera")

properties = await my_camera.get_properties()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(Properties)](https://pkg.go.dev/go.viam.com/rdk/components/camera#Properties): Properties of the particular implementation of a camera.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(robot, "my_camera")

// gets the properties from a camera
properties, err := myCamera.Properties(context.Background())

```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#Camera).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the camera in its current configuration, in the [frame](/mobility/frame-system/) of the camera.
The [motion](/mobility/motion/) and [navigation](/mobility/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[Geometry])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry): The geometries associated with the camera, in any order.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.get_geometries).

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=robot, name="my_camera")

geometries = await my_camera.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

{{% /tab %}}

<!-- Go tab

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [`[]spatialmath.Geometry`](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): The geometries associated with the camera, in any order.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Shaped).

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(robot, "my_camera")

geometries, err := myCamera.Geometries(context.Background(), nil)

if len(geometries) > 0 {
    // Get the center of the first geometry
    elem := geometries[0]
    fmt.Println("Pose of the first geometry's center point:", elem.center)
}
```

 -->

{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For native models, model-specific commands are covered with each model's documentation.
If you are implementing your own camera and adding features that have no native API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot, "my_camera")

command = {"cmd": "test", "data1": 500}
result = my_camera.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(robot, "my_camera")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myCamera.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Code](https://pkg.go.dev/go.viam.com/rdk/components/camera).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot, "my_camera")

await my_camera.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/client/index.html#viam.components.camera.client.CameraClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myCamera, err := camera.FromRobot(robot, "my_camera")

err := myCamera.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## Next steps

{{< cards >}}
{{% card link="/ml/vision" %}}
{{% card link="/tutorials/services/try-viam-color-detection" %}}
{{% card link="/tutorials/services/color-detection-scuttle" %}}
{{< /cards >}}

<br>

{{< snippet "social.md" >}}
