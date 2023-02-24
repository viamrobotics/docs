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

## Configuration

The configuration of your camera component depends on your camera model.
You can use different models to:

- Configure physical cameras that generate images or point clouds.
- Combine streams from multiple cameras into one.
- Transform and process images.

For configuration information, click on one of the following models:

| Model | Description |
| ----- | ----------- |
| [`ffmpeg`](ffmpeg) | Uses a camera, a video file, or a stream as a camera. |
| [`image_file`](image-file) | Gets color and depth images frames from a file path. |
| [`velodyne`](velodyne) | Uses velodyne lidar. |
| [`webcam`](webcam) | A standard camera that streams camera data. |
| [`fake`](fake) | A camera model for testing. |
| [`single_stream`](single-stream) | A HTTP server camera that streams image data from an HTTP endpoint. |
| [`dual_stream`](dual-stream) | A HTTP server camera that combines the streams of two camera servers to create colorful point clouds. |
| [`join_color_depth`](join-color-depth) | Joins the outputs of a color and depth camera already registered in your config to create a third "camera" that outputs the combined and aligned image. |
| [`align_color_depth_extrinsics`](align-color-depth-extrinsics) | Uses the intrinsics of the color and depth camera, as well as the extrinsic pose between them, to align two images. |
| [`align_color_depth_homography`](align-color-depth-homography) | Uses a homography matrix to align the color and depth images. |
| [`join_pointclouds`](join-pointclouds) | Combines the point clouds from multiple camera sources and projects them to be from the point of view of target_frame. |
| [`transform`](transform) | A pipeline for applying transformations to an input image source. |

## Control your camera with Viam's client SDK libraries

Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and the [Getting Started with the Viam App guide](/manage/app-usage/) for app-specific guidance.

{{< readfile "/static/include/components/camera-sample.md" >}}

## API

The camera component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [GetImage](#getimage) | Returns an image from the camera encoded in the format specified by the MIME type. |
| [GetPointCloud](#getpointcloud) | Returns a point cloud from the camera. |
| [GetProperties](#getproperties) | Returns the camera intrinsic and camera distortion parameters, as well as whether the camera supports returning point clouds. |

### GetImage

Returns an image from the camera encoded in the format specified by the MIME type.

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

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next Steps

<div class="container text-center">
  <div class="row">
        <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
          <a href="calibrate/">
            <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">
                Calibrate a Camera
            </h4>
          </a>
          <p style="text-align: left;"> Calibrate a camera and extract the intrinsic and distortion parameters. </p>
        </div>
        <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
          <a href="transform/">
            <h4 style="text-align: left; margin-left: 0px; margin-top: 1em;">
                Transform a Camera
            </h4>
          </a>
          <p style="text-align: left;"> Instructions for transforming a webcam. </p>
        </div>
      <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
          <a href="../../services/vision">
              <br>
              <h4 style="text-align: left; margin-left: 0px;">Vision Service</h4>
              <p style="text-align: left;">The vision service enables your robot to use its on-board cameras to intelligently see and interpret the world around it.</p>
          <a>
      </div>
    </div>
  <div class="row">
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="/tutorials/viam-rover/try-viam-color-detection/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Detect color with a Viam Rover</h4>
            <p style="text-align: left;">Use the vision service in the Viam app to detect a color.</p>
        </a>
    </div>
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="/tutorials/scuttlebot/color-detection-scuttle/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Colored Object Follower</h4>
            <p style="text-align: left;">Instructions for detecting and following a colored object with a SCUTTLE Robot on Viam software.</p>
        </a>
    </div>
  </div>
</div>
