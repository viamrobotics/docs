---
title: "Camera Component"
linkTitle: "Camera"
childTitleEndOverwrite: "Camera Component"
weight: 40
type: "docs"
description: "A camera captures 2D or 3D images and sends them to the computer controlling the robot."
no_list: true
tags: ["camera", "components"]
icon: "/icons/components/camera.svg"
images: ["/icons/components/camera.svg"]
aliases:
  - "/tutorials/configure-a-camera"
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

## Configuration

For configuration information, click on one of the supported camera models:

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

Viam also provides the following camera models as [modular resources](/extend/modular-resources/):

| Model | Description |
| ----- | ----------- |
| [`viam:lidar:rplidar`](/extend/modular-resources/examples/rplidar/) | A LIDAR scanning device like the [RPlidar A1](https://www.slamtec.com/en/Lidar/A1). |
| [`viam:camera:csi`](/extend/modular-resources/examples/csi/) | Camera Serial Interface (CSI) cameras, like [these cameras from E-con Systems](https://www.e-consystems.com/nvidia-jetson-agx-orin-cameras.asp) or [this camera from Seed Technologies](https://www.digikey.com/en/products/detail/seeed-technology-co.,-ltd/114992263/12396924). |

## Control your camera with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have a camera called `"my_camera"` configured as a component of your robot.
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

- `mime_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The MIME type of the image.
  The returned MIME type is not guaranteed to match the image output type.

**Returns:**

- ([PIL.Image](https://pillow.readthedocs.io/en/stable/reference/Image.html) or [RawImage](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.RawImage)): The requested frame.

```python {class="line-numbers linkable-line-numbers"}
my_camera = Camera.from_robot(robot=robot, name="my_camera")

frame = await my_camera.get_image()
```

<br>

If the `mime_type` of your image is `image/vnd.viam.dep`, pass the returned image data to the Viam Python SDK's [`RawImage.bytes_to_depth_array()`](https://python.viam.dev/autoapi/viam/media/video/index.html#viam.media.video.RawImage.bytes_to_depth_array) method to decode the raw image data to a standard 2D image representation.

For example:

```python {class="line-numbers linkable-line-numbers"}
# Assume "frame" has a mime_type of "image/vnd.viam.dep"
frame = await my_cam.get_image()

# Convert "frame" to a standard 2D image representation.
# Remove the 1st 3x8 bytes and reshape the raw bytes to List[List[Int]].
standard_frame frame.bytes_to_depth_array()
```

{{% alert title="Tip" color="tip" %}}

Be sure to close the image when finished.

{{% /alert %}}

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.get_image).

{{% /tab %}}
{{% tab name="Go" %}}

{{% alert title="Info" color="info" %}}

Unlike most Viam [component APIs](/program/apis/#component-apis), the methods of the Go camera client do not map exactly to the names of the other SDK's camera methods.
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

Get simultaneous images from different imagers, along with associated metadata.
The multiple images returned from GetImages do not represent a time series of images.

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

my_camera= Camera.from_robot(robot=robot, name="my_camera")

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
my_camera= Camera.from_robot(robot=robot, name="my_camera")

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
my_camera= Camera.from_robot(robot, "my_camera")

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

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
  {{% card link="/services/vision" %}}
  {{% card link="/tutorials/services/try-viam-color-detection" %}}
  {{% card link="/tutorials/services/color-detection-scuttle" %}}
{{< /cards >}}
