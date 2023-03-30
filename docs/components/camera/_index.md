---
title: "Camera Component"
linkTitle: "Camera"
weight: 40
type: "docs"
description: "A camera captures 2D or 3D images and sends them to the computer controlling the robot."
no_list: true
tags: ["camera", "components"]
icon: "img/components/camera.png"
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

For configuration information, click on one of the following models:

| Model | Description |
| ----- | ----------- |
| [`ffmpeg`](ffmpeg) | Uses a camera, a video file, or a stream as a camera. |
| [`image_file`](image-file) | Gets color and depth images frames from a file path. |
| [`velodyne`](velodyne) | Uses velodyne lidar. |
| [`webcam`](webcam) | A standard camera that streams camera data. |
| [`rtsp`](rtsp) | A streaming camera with an MJPEG track. |
| [`fake`](fake) | A camera model for testing. |
| [`single_stream`](single-stream) | A HTTP client camera that streams image data from an HTTP endpoint. |
| [`dual_stream`](dual-stream) | A HTTP client camera that combines the streams of two camera servers to create colorful point clouds. |
| [`join_color_depth`](join-color-depth) | Joins the outputs of a color and depth camera already registered in your config to create a third "camera" that outputs the combined and aligned image. |
| [`align_color_depth_extrinsics`](align-color-depth-extrinsics) | Uses the intrinsics of the color and depth camera, as well as the extrinsic pose between them, to align two images. |
| [`align_color_depth_homography`](align-color-depth-homography) | Uses a homography matrix to align the color and depth images. |
| [`join_pointclouds`](join-pointclouds) | Combines the point clouds from multiple camera sources and projects them to be from the point of view of target_frame. |
| [`transform`](transform) | A pipeline for applying transformations to an input image source. |

## Control your camera with Viam's client SDK libraries

Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries.

{{< readfile "/static/include/components/camera-sample.md" >}}

## API

The camera component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [GetImage](#getimage) | Returns an image from the camera. |
| [GetPointCloud](#getpointcloud) | Returns a point cloud from the camera. |
| [GetProperties](#getproperties) | Returns the camera intrinsic and camera distortion parameters, as well as whether the camera supports returning point clouds. |
| [DoCommand](#docommand) | Sends or receives model-specific commands. |

### GetImage

Returns an image from the camera.
You can request a specific MIME type but the returned MIME type is not guaranteed.
If the server does not know how to return the specified MIME type, the server returns the image in another format instead.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `mime_type` (`str`): The MIME type of the image.
  The returned MIME type is not guaranteed to match the image output type.

**Returns:**

- `frame` (`Image` or [`RawImage`](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.RawImage)): The requested frame.

```python {class="line-numbers linkable-line-numbers"}
my_cam = Camera.from_robot(robot=robot, name='my_camera')

frame = await my_cam.get_image()
```

Be sure to close the image when finished.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.get_image).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` ([`Context`](https://pkg.go.dev/context)): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `errHandlers` ([`ErrorHandler`](https://pkg.go.dev/github.com/edaniels/gostream#ErrorHandler)): A handler for errors allowing for logic based on consecutively retrieved errors).

**Returns:**

- `stream` ([`gostream.VideoStream`](https://pkg.go.dev/github.com/edaniels/gostream)): A `VideoStream` that streams video until closed.
- `err` ([`error`](https://pkg.go.dev/builtin#error)): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// gets the stream from a camera
stream, err := myCam.Stream(context.Background())

// gets an image from the camera stream
img, release, err := stream.Next(context.Background())
defer release()
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

- `pointcloud` (`bytes`): The pointcloud data.
- `mimetype` (`str`): The MIME type of the pointcloud (for example PCD).

To deserialize the returned information into a numpy array, use the Open3D library:

```python {class="line-numbers linkable-line-numbers"}
import numpy as np
import open3d as o3d

my_cam = Camera.from_robot(robot=robot, name='my_camera')

data, _ = await my_cam.get_point_cloud()

# write the point cloud into a temporary file
with open("/tmp/pointcloud_data.pcd", "wb") as f:
    f.write(data)
pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
points = np.asarray(pcd.points)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.get_point_cloud).

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `ctx` ([`Context`](https://pkg.go.dev/context)): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- `pointCloud` ([`pointcloud.PointCloud`](https://pkg.go.dev/go.viam.com/rdk/pointcloud#PointCloud)): A general purpose container of points.
  It does not dictate whether or not the cloud is sparse or dense.
- `err` ([`error`](https://pkg.go.dev/builtin#error)): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

pointCloud, err := myCam.NextPointCloud(context.Background())
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

- `properties` ([`Properties`](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.Properties)): The properties of the camera.

```python {class="line-numbers linkable-line-numbers"}
my_cam = Camera.from_robot(robot=robot, name='my_camera')

properties = await my_cam.get_properties()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/camera/index.html#viam.components.camera.Camera.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` ([`Context`](https://pkg.go.dev/context)): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- `properties` ([`Properties`](https://pkg.go.dev/go.viam.com/rdk/components/camera#Properties)): Properties of the particular implementation of a camera.
- `err` ([`error`](https://pkg.go.dev/builtin#error)): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// gets the properties from a camera
properties, err := myCam.Properties(context.Background())

```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/camera#Camera).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For native models, model-specific commands are covered with each model's documentation.
If you are implementing your own camera and add features that have no native API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (`Dict[str, Any]`): The command to execute.

**Returns:**

- `result` (`Dict[str, Any]`): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_cam = Camera.from_robot(robot, "camera0")

command = {"cmd": "test", "data1": 500}
result = my_cam.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/#the-do-method).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` ([`Context`](https://pkg.go.dev/context)): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` (`cmd map[string]interface{}`): The command to execute.

**Returns:**

- `result` (`cmd map[string]interface{}`): Result of the executed command.
- `error` ([`error`](https://pkg.go.dev/builtin#error)): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
  myCam, err := camera.FromRobot(robot, "my_camera")

  command := map[string]interface{}{"cmd": "test", "data1": 500}
  result, err := myCam.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/9be13108c8641b66fd4251a74ea638f47b040d62/components/camera/camera.go#L268).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
  {{% card link="/services/vision" size="small" %}}
  {{% card link="/tutorials/services/try-viam-color-detection" size="small" %}}
  {{% card link="/tutorials/services/color-detection-scuttle" size="small" %}}
{{< /cards >}}
