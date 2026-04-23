---
linkTitle: "Measure depth"
title: "Measure depth"
weight: 20
layout: "docs"
type: "docs"
description: "Retrieve point clouds and depth images from a depth camera, read depth at specific pixels, and measure distance to detected objects."
date: "2025-01-30"
aliases:
  - /build/vision-detection/measure-depth/
  - /vision-detection/measure-depth/
  - /vision-detection/localize-objects-in-3d/
  - /build/vision-detection/localize-objects-in-3d/
  - /vision/measure-depth/
---

A standard camera gives you a flat 2D image. You can see that there is a box on the table, but you cannot tell whether the box is 30 centimeters away or 3 meters away. This how-to shows you how to get depth data from your perception sensor (a depth camera, LiDAR, or ToF sensor) and extract useful distance measurements for robotics tasks that involve physical interaction.

## Concepts

### What depth cameras provide

Depth cameras capture both color (RGB) and distance information. There are several technologies:

| Technology           | How it works                                       | Common examples                    |
| -------------------- | -------------------------------------------------- | ---------------------------------- |
| Structured light     | Projects a known pattern and measures distortion   | Intel RealSense D400 series        |
| Time of flight (ToF) | Measures how long light takes to bounce back       | Intel RealSense L515, Azure Kinect |
| Stereo vision        | Uses two cameras to calculate depth from disparity | Oak-D, ZED cameras                 |

All of these produce the same type of output in Viam: a point cloud or a depth map that you access through the standard camera API.

### Point clouds

A point cloud is a collection of 3D points, each with an (x, y, z) position measured in millimeters from a frame defined by the sensor (the optical center for most depth cameras; check your sensor's datasheet for LiDAR and ToF units). Some point clouds also include color information for each point.

The coordinate system typically follows this convention:

- **X** increases to the right
- **Y** increases downward
- **Z** increases away from the sensor (depth)

A typical indoor scene captured by a depth camera contains tens of thousands to hundreds of thousands of points, depending on the camera resolution and range.

### Depth maps vs point clouds

A **depth map** is a 2D image where each pixel's value is the distance from the camera to the surface. It is essentially a grayscale image where brighter pixels are farther away (or vice versa, depending on the encoding).

A **point cloud** is the 3D representation: each pixel in the depth map is projected into 3D space using the camera's intrinsic parameters. The point cloud contains explicit (x, y, z) coordinates.

Viam provides point clouds through the `GetPointCloud` API. If you need a depth map instead, capture it through `GetImages` and filter the returned list for the image whose MIME type is `image/vnd.viam.dep` (the raw depth format).

### Camera intrinsic parameters

Intrinsic parameters describe the internal geometry of the camera: focal length, principal point, and lens distortion. These parameters are required to accurately project 2D pixel coordinates into 3D space.

When you configure a depth camera in Viam, the intrinsic parameters are typically loaded automatically from the camera hardware. If your camera does not provide them, you can specify them manually in the camera configuration. Without correct intrinsic parameters, 3D projections will be inaccurate.

### 3D object localization

If you need 3D positions for detected objects (for example, to guide a robot arm to pick up a cup), combine 2D detections with depth data. The workflow is:

1. Run a 2D detector to get bounding boxes.
2. For each bounding box, extract the corresponding depth pixels.
3. Project those depth pixels into 3D space using the camera's intrinsic parameters.

The result is a 3D point cloud for each detected object, with coordinates in the camera's frame (x right, y down, z forward, in millimeters). To use these positions with other robot components, transform them through the [frame system](/motion-planning/frame-system/).

Step 5 of this guide shows how to combine detections with depth data to measure distance. For full 3D point clouds, use the vision service's [`GetObjectPointClouds`](/reference/apis/services/vision/#getobjectpointclouds) method if your vision service supports it.

## Steps

### 1. Verify your depth camera is configured

Go to [app.viam.com](https://app.viam.com), navigate to your machine, and verify your depth camera appears in the component list. Open the test panel and confirm it is producing images.

Common depth-capable cameras and the modules that wrap them:

- Intel RealSense D400 series, through the [RealSense module](https://github.com/viamrobotics/viam-camera-realsense)
- Luxonis OAK-D series, through the [OAK camera module](https://github.com/viamrobotics/viam-camera-oak)
- Orbbec cameras, through the [Orbbec module](https://github.com/viam-modules/orbbec)
- The `fake` camera model, for development without hardware (returns synthetic but structurally correct point clouds)

For other depth cameras, search for `camera` in the [Viam registry](https://app.viam.com/registry).

Check that the depth stream is enabled in the camera's configuration, and confirm the camera reports `supports_pcd: true` through [`GetProperties`](/reference/apis/components/camera/#getproperties). Without depth support, none of the steps below will work.

### 2. Get a point cloud

Use the camera API to retrieve a point cloud from your depth camera.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.camera import Camera


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    camera = Camera.from_robot(robot, "my-depth-camera")

    # get_point_cloud returns (point_cloud_bytes, mime_type).
    # The MIME type (for example, "pointcloud/pcd") is not needed here.
    point_cloud, mime_type = await camera.get_point_cloud()

    print("Point cloud retrieved")
    print(f"MIME type: {mime_type}, payload type: {type(point_cloud)}")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/components/camera"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/utils/rpc"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("depth")

    machine, err := client.New(ctx, "YOUR-MACHINE-ADDRESS", logger,
        client.WithDialOptions(rpc.WithEntityCredentials(
            "YOUR-API-KEY-ID",
            rpc.Credentials{
                Type:    rpc.CredentialsTypeAPIKey,
                Payload: "YOUR-API-KEY",
            })),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer machine.Close(ctx)

    cam, err := camera.FromProvider(machine, "my-depth-camera")
    if err != nil {
        logger.Fatal(err)
    }

    pc, err := cam.NextPointCloud(ctx, nil)
    if err != nil {
        logger.Fatal(err)
    }

    fmt.Printf("Point cloud retrieved with %d points\n", pc.Size())
}
```

{{% /tab %}}
{{< /tabs >}}

### 3. Get a depth image

Instead of a full point cloud, you can capture a depth image. This is a 2D representation where each pixel value is the depth in millimeters.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.camera import Camera

camera = Camera.from_robot(robot, "my-depth-camera")

# Get images from the depth camera
images, _ = await camera.get_images()

# Each item is a NamedImage. Inspect `name` and `mime_type` to find the depth stream.
for img in images:
    print(f"Name: {img.name}, MIME: {img.mime_type}, size: {img.width}x{img.height}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
cam, err := camera.FromProvider(machine, "my-depth-camera")
if err != nil {
    logger.Fatal(err)
}

// Get images including the depth frame
images, _, err := cam.Images(ctx, nil, nil)
if err != nil {
    logger.Fatal(err)
}

for _, img := range images {
    fmt.Printf("Source: %s\n", img.SourceName)
}
```

{{% /tab %}}
{{< /tabs >}}

### 4. Read depth at a specific pixel

Given a depth image, you can look up the distance at any pixel coordinate. This is useful when you know where an object is in the 2D image (from a detection) and want to know how far away it is.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import numpy as np
from viam.components.camera import Camera
from viam.media.video import CameraMimeType


camera = Camera.from_robot(robot, "my-depth-camera")

# Get images from the depth camera
images, _ = await camera.get_images()

# Find the depth image by MIME type, then decode bytes to a 2D depth array.
depth_image = next(
    (img for img in images if img.mime_type == CameraMimeType.VIAM_RAW_DEPTH),
    None,
)
if depth_image is None:
    raise RuntimeError("No depth stream in camera output")

# bytes_to_depth_array returns a 2D list of uint16 values in millimeters.
depth_array = np.array(depth_image.bytes_to_depth_array(), dtype=np.uint16)

# Read depth at a specific pixel (center of image)
center_x = depth_array.shape[1] // 2
center_y = depth_array.shape[0] // 2
depth_mm = int(depth_array[center_y, center_x])

print(f"Depth at center ({center_x}, {center_y}): {depth_mm} mm")
print(f"That is {depth_mm / 1000:.2f} meters")

# Read depth at a specific coordinate
target_x, target_y = 320, 240
depth_at_target = int(depth_array[target_y, target_x])
print(f"Depth at ({target_x}, {target_y}): {depth_at_target} mm")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "fmt"
    "image"
)

cam, err := camera.FromProvider(machine, "my-depth-camera")
if err != nil {
    logger.Fatal(err)
}

images, _, err := cam.Images(ctx, nil, nil)
if err != nil {
    logger.Fatal(err)
}

// Access the depth image (check SourceName to identify the depth stream)
depthImg, err := images[1].Image(ctx)
if err != nil {
    logger.Fatal(err)
}
bounds := depthImg.Bounds()
centerX := (bounds.Min.X + bounds.Max.X) / 2
centerY := (bounds.Min.Y + bounds.Max.Y) / 2

// Read the depth value at center
r, _, _, _ := depthImg.At(centerX, centerY).RGBA()
depthMM := int(r)

fmt.Printf("Depth at center (%d, %d): %d mm\n", centerX, centerY, depthMM)
fmt.Printf("That is %.2f meters\n", float64(depthMM)/1000.0)
```

{{% /tab %}}
{{< /tabs >}}

### 5. Measure distance to detected objects

Combine 2D detections with depth data to measure the distance to each detected object. Use the center of the bounding box as the depth sample point.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.camera import Camera
from viam.media.video import CameraMimeType
from viam.services.vision import VisionClient
import numpy as np


camera = Camera.from_robot(robot, "my-depth-camera")
detector = VisionClient.from_robot(robot, "my-detector")

# Get detections
detections = await detector.get_detections_from_camera("my-depth-camera")

# Get images and decode the depth stream.
images, _ = await camera.get_images()
depth_image = next(
    (img for img in images if img.mime_type == CameraMimeType.VIAM_RAW_DEPTH),
    None,
)
if depth_image is None:
    raise RuntimeError("No depth stream in camera output")
depth_array = np.array(depth_image.bytes_to_depth_array(), dtype=np.uint16)

for d in detections:
    if d.confidence < 0.5:
        continue

    # Use the center of the bounding box
    center_x = (d.x_min + d.x_max) // 2
    center_y = (d.y_min + d.y_max) // 2

    # Clamp to image bounds
    center_x = max(0, min(center_x, depth_array.shape[1] - 1))
    center_y = max(0, min(center_y, depth_array.shape[0] - 1))

    depth_mm = depth_array[center_y, center_x]

    # Sample a small region around center for more robust measurement
    region = depth_array[
        max(0, center_y - 5):min(depth_array.shape[0], center_y + 5),
        max(0, center_x - 5):min(depth_array.shape[1], center_x + 5)
    ]
    # Filter out zero (invalid) depth values
    valid_depths = region[region > 0]
    if len(valid_depths) > 0:
        median_depth = np.median(valid_depths)
    else:
        median_depth = depth_mm

    print(f"{d.class_name}: {d.confidence:.2f}, "
          f"distance: {median_depth:.0f} mm ({median_depth/1000:.2f} m)")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "fmt"
    "sort"

    "go.viam.com/rdk/components/camera"
    "go.viam.com/rdk/services/vision"
)

cam, err := camera.FromProvider(machine, "my-depth-camera")
if err != nil {
    logger.Fatal(err)
}

detector, err := vision.FromProvider(machine, "my-detector")
if err != nil {
    logger.Fatal(err)
}

detections, err := detector.DetectionsFromCamera(ctx, "my-depth-camera", nil)
if err != nil {
    logger.Fatal(err)
}

images, _, err := cam.Images(ctx, nil, nil)
if err != nil {
    logger.Fatal(err)
}

// Access the depth image (check SourceName to identify the depth stream)
depthImg, err := images[1].Image(ctx)
if err != nil {
    logger.Fatal(err)
}
bounds := depthImg.Bounds()

for _, d := range detections {
    if d.Score() < 0.5 {
        continue
    }

    bb := d.BoundingBox()
    centerX := (bb.Min.X + bb.Max.X) / 2
    centerY := (bb.Min.Y + bb.Max.Y) / 2

    // Clamp to image bounds
    if centerX < bounds.Min.X {
        centerX = bounds.Min.X
    }
    if centerX >= bounds.Max.X {
        centerX = bounds.Max.X - 1
    }
    if centerY < bounds.Min.Y {
        centerY = bounds.Min.Y
    }
    if centerY >= bounds.Max.Y {
        centerY = bounds.Max.Y - 1
    }

    // Sample center pixel depth
    r, _, _, _ := depthImg.At(centerX, centerY).RGBA()
    depthMM := int(r)

    fmt.Printf("%s: %.2f, distance: %d mm (%.2f m)\n",
        d.Label(), d.Score(), depthMM, float64(depthMM)/1000.0)
}
```

{{% /tab %}}
{{< /tabs >}}

### 6. Convert depth + pixel coordinates to a 3D position

A distance reading tells you how far something is, but not where it is in space. To plan a motion to a detected object you need a 3D position (x, y, z) in a frame another component can use.

Two steps: unproject the pixel to a point in the **camera frame**, then transform that point into whichever frame the consuming component (arm base, robot base, map) expects.

**Unproject pixel + depth to camera frame:**

Given the pixel `(u, v)` where your detection centered, a depth reading `d` in millimeters, and the camera's intrinsics `fx`, `fy`, `ppx`, `ppy`:

```python
x_camera = (u - ppx) * d / fx
y_camera = (v - ppy) * d / fy
z_camera = d
```

The result is a point in millimeters, in the camera's frame (x right, y down, z forward).

**Transform to a shared frame:**

Call `transform_pose` on your `RobotClient` to convert the camera-frame pose into whatever frame your application uses: the arm base, the robot base, the world. `transform_pose` reads the [frame system](/motion-planning/frame-system/) configuration, which records where the camera is mounted relative to other components:

```python
from viam.proto.common import Pose, PoseInFrame

camera_pose = PoseInFrame(
    reference_frame="my-depth-camera",
    pose=Pose(x=x_camera, y=y_camera, z=z_camera, o_x=0, o_y=0, o_z=1, theta=0),
)
arm_pose = await robot.transform_pose(camera_pose, "my-arm")
print(f"Object at arm-frame position: ({arm_pose.pose.x:.0f}, {arm_pose.pose.y:.0f}, {arm_pose.pose.z:.0f}) mm")
```

For this to work, your machine configuration must declare frames for the camera and the target component. See [Frame system](/motion-planning/frame-system/) for the full setup.

If your vision service model supports it, [`GetObjectPointClouds`](/reference/apis/services/vision/#getobjectpointclouds) returns the 3D center for each detected object directly, skipping the manual unprojection. See [Segment 3D objects](/vision/3d-vision/segment-3d/).

### 7. Use a fake camera for testing

If you do not have a depth camera, configure a `fake` camera that generates simulated point cloud data. This lets you develop and test your depth-related code without hardware.

```json
{
  "name": "my-depth-camera",
  "api": "rdk:component:camera",
  "model": "fake",
  "attributes": {}
}
```

The fake camera generates both color images and simulated point cloud data. The depth values are synthetic but structurally correct, so your code will work the same way with real hardware.

### 8. Configure camera intrinsic parameters

Intrinsic parameters apply to camera-based depth sensors that capture depth as a 2D map and then project it into 3D using the camera's internal geometry. This covers structured light cameras like the Intel RealSense D400 series and stereo cameras like the OAK-D. Sensors that return 3D points directly, such as the Intel RealSense L515 and solid-state lidars, don't use intrinsics the same way. Check your sensor's datasheet if you're not sure.

If your camera does not automatically provide intrinsic parameters, you can set them manually in the configuration.

```json
{
  "name": "my-depth-camera",
  "api": "rdk:component:camera",
  "model": "webcam",
  "attributes": {
    "intrinsic_parameters": {
      "fx": 615.0,
      "fy": 615.0,
      "ppx": 320.0,
      "ppy": 240.0,
      "width_px": 640,
      "height_px": 480
    },
    "distortion_parameters": {
      "rk1": 0.0,
      "rk2": 0.0,
      "rk3": 0.0,
      "tp1": 0.0,
      "tp2": 0.0
    }
  }
}
```

| Parameter               | Description                                      |
| ----------------------- | ------------------------------------------------ |
| `fx`, `fy`              | Focal length in pixels (horizontal and vertical) |
| `ppx`, `ppy`            | Principal point (optical center) in pixels       |
| `width_px`, `height_px` | Image dimensions                                 |
| `rk1`, `rk2`, `rk3`     | Radial distortion coefficients                   |
| `tp1`, `tp2`            | Tangential distortion coefficients               |

Most depth cameras (Intel RealSense, Oak-D) provide these automatically. You only need to set them manually for cameras without built-in calibration data.

**Intrinsics vs extrinsics.** Intrinsics describe the camera's internal geometry (how pixels map to rays). Extrinsics describe where the camera is mounted relative to other things on the machine (the arm base, the robot base). Viam handles extrinsics through the [frame system](/motion-planning/frame-system/), not through camera attributes. Step 6 above uses extrinsics (through `TransformPose`) to move a 3D point from the camera frame into another component's frame.

{{< alert title="Tip" color="tip" >}}
To fetch an image, detections, and point cloud objects together in one call (rather than separate `get_images` and detector calls), use [`CaptureAllFromCamera`](/reference/apis/services/vision/#captureallfromcamera). All three results come from the same captured frame, so they stay in sync:

```python
from viam.services.vision import VisionClient

detector = VisionClient.from_robot(robot, "my-detector")

result = await detector.capture_all_from_camera(
    "my-depth-camera",
    return_image=True,
    return_detections=True,
    return_object_point_clouds=True,
)

image = result.image
detections = result.detections
point_clouds = result.objects  # list of 3D objects, one per detection
```

This matters for fused results: if you call `get_images()` and `get_detections_from_camera()` separately on a running stream, the detections come from a later frame than the image. `CaptureAllFromCamera` avoids the race.
{{< /alert >}}

## Try it

1. Run the point cloud script from step 2 and verify you get data back.
2. Run the depth-at-pixel script from step 4. Point the camera at objects at different distances and verify the measurements are reasonable.
3. If you have a detector configured, run the combined detection + depth script from step 5. Walk toward and away from the camera and observe how the distance measurement changes.
4. Compare the depth reading at the center of the image with a physical measurement (use a tape measure). Depth cameras are typically accurate to within a few centimeters at ranges under 5 meters.

## Troubleshooting

{{< expand "Point cloud is empty or has very few points" >}}

- Depth cameras have a minimum and maximum range. Objects too close (under ~20 cm) or too far (over ~10 m for structured light cameras) produce no depth data.
- Reflective surfaces (mirrors, shiny metal) and transparent surfaces (glass, clear plastic) are invisible to most depth cameras. Move these objects out of the scene.
- Check the camera's USB connection. Depth cameras require USB 3.0 for full resolution. A USB 2.0 connection may work but with reduced depth resolution.

{{< /expand >}}

{{< expand "Depth values are zero at some pixels" >}}

- Zero typically means "no data": the camera could not determine the depth at that pixel. This is common at object edges, on featureless surfaces (blank walls), and at extreme distances.
- When measuring distance to an object, sample multiple pixels around the target and take the median of non-zero values, as shown in step 5.

{{< /expand >}}

{{< expand "Depth measurements are inaccurate" >}}

- Verify the camera's intrinsic parameters are correct. Incorrect focal length values cause systematic depth errors.
- Depth accuracy degrades with distance. Most consumer depth cameras are accurate to 1-2% at ranges under 4 meters but much less accurate beyond that.
- Ensure the camera has been running for at least 30 seconds before measuring. Some depth cameras need time to warm up and stabilize.

{{< /expand >}}

{{< expand "\"GetPointCloud not supported\" error" >}}

- Not all camera models support point clouds. The camera must be a depth camera or have depth functionality enabled.
- If using a module (such as the RealSense module), verify the module is installed and the camera is configured to output depth data.
- The `fake` camera model supports point clouds for testing purposes.

{{< /expand >}}

## What's next

- [Detect objects](/vision/object-detection/detect/): get 2D detections to combine with depth measurements.
- [Act on detections](/vision/object-detection/act-on-detections/): drive machine behavior from detections plus depth (for example, move a robot arm to a 3D object position).
- [Frame system](/motion-planning/frame-system/): set up coordinate frame transforms so 3D positions are usable by other components.
