---
linkTitle: "Measure depth"
title: "Measure depth"
weight: 50
layout: "docs"
type: "docs"
description: "Retrieve point clouds and depth images from a depth camera, read depth at specific pixels, and measure distance to detected objects."
date: "2025-01-30"
aliases:
  - /build/vision-detection/measure-depth/
  - /vision-detection/measure-depth/
  - /vision-detection/localize-objects-in-3d/
  - /build/vision-detection/localize-objects-in-3d/
---

A standard camera gives you a flat 2D image. You can see that there is a box on the table, but you cannot tell whether the box is 30 centimeters away or 3 meters away. This how-to shows you how to get depth data from your camera and extract useful distance measurements for robotics tasks that involve physical interaction.

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

A point cloud is a collection of 3D points, each with an (x, y, z) position measured in millimeters from the camera's optical center. Some point clouds also include color information for each point.

The coordinate system follows a standard convention:

- **X** increases to the right
- **Y** increases downward
- **Z** increases away from the camera (depth)

A typical indoor scene captured by a depth camera contains tens of thousands to hundreds of thousands of points, depending on the camera resolution and range.

### Depth maps vs point clouds

A **depth map** is a 2D image where each pixel value represents the distance from the camera to the surface at that pixel location. It is essentially a grayscale image where brighter pixels are farther away (or vice versa, depending on the encoding).

A **point cloud** is the 3D representation: each pixel in the depth map is projected into 3D space using the camera's intrinsic parameters. The point cloud contains explicit (x, y, z) coordinates.

Viam provides point clouds through the `GetPointCloud` API. If you need a depth map instead, you can capture the depth image directly using `GetImage` with the appropriate MIME type.

### Camera intrinsic parameters

Intrinsic parameters describe the internal geometry of the camera: focal length, principal point, and lens distortion. These parameters are required to accurately project 2D pixel coordinates into 3D space.

When you configure a depth camera in Viam, the intrinsic parameters are typically loaded automatically from the camera hardware. If your camera does not provide them, you can specify them manually in the camera configuration. Without correct intrinsic parameters, 3D projections will be inaccurate.

### 3D object localization

If you need 3D positions for detected objects --for example, to guide a robot arm to pick up a cup --you combine 2D detections with depth data. The workflow is:

1. Run a 2D detector to get bounding boxes.
2. For each bounding box, extract the corresponding depth pixels.
3. Project those depth pixels into 3D space using the camera's intrinsic parameters.

The result is a 3D point cloud for each detected object, with coordinates in the camera's frame (x right, y down, z forward, in millimeters). To use these positions with other robot components, transform them through the [frame system](/motion-planning/frame-system/).

Step 5 of this guide shows how to combine detections with depth data to measure distance. For full 3D point clouds, use the vision service's [`GetObjectPointClouds`](/dev/reference/apis/services/vision/#getobjectpointclouds) method if your vision service supports it.

## Steps

### 1. Verify your depth camera is configured

Go to [app.viam.com](https://app.viam.com), navigate to your machine, and verify your depth camera appears in the component list. Open the test panel and confirm it is producing images.

For Intel RealSense cameras, the `webcam` model or the `realsense` module is commonly used. Check that the depth stream is enabled in the camera configuration.

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

    # Get a point cloud
    point_cloud, _ = await camera.get_point_cloud()

    print("Point cloud retrieved")
    print(f"Type: {type(point_cloud)}")

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

# The depth image is typically the second image
# Check source_name to identify the depth stream
for img in images:
    print(f"Source: {img.source_name}, size: {img.width}x{img.height}")
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


camera = Camera.from_robot(robot, "my-depth-camera")

# Get images from the depth camera
images, _ = await camera.get_images()

# Find the depth image by checking available images
# Convert to numpy array for pixel-level access
depth_array = np.array(images[1].image)

# Read depth at a specific pixel (center of image)
center_x = depth_array.shape[1] // 2
center_y = depth_array.shape[0] // 2
depth_mm = depth_array[center_y, center_x]

print(f"Depth at center ({center_x}, {center_y}): {depth_mm} mm")
print(f"That is {depth_mm / 1000:.2f} meters")

# Read depth at a specific coordinate
target_x, target_y = 320, 240
depth_at_target = depth_array[target_y, target_x]
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
from viam.services.vision import VisionClient
import numpy as np


camera = Camera.from_robot(robot, "my-depth-camera")
detector = VisionClient.from_robot(robot, "my-detector")

# Get detections
detections = await detector.get_detections_from_camera("my-depth-camera")

# Get images including depth
images, _ = await camera.get_images()
depth_array = np.array(images[1].image)

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

### 6. Use a fake camera for testing

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

### 7. Configure camera intrinsic parameters

If your camera does not automatically provide intrinsic parameters, you can set them manually in the configuration. These parameters are needed for accurate 2D-to-3D projection.

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

{{< alert title="Tip" color="tip" >}}
If you need an image, its detections, and a point cloud together in one call, use [`CaptureAllFromCamera`](/dev/reference/apis/services/vision/#captureallfromcamera). This is more efficient than separate calls and ensures all results correspond to the same frame. See [Detect Objects, step 7](/vision/detect/#7-get-everything-in-one-call-with-captureallfromcamera) for a full example.
{{< /alert >}}

## Try It

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

- Zero typically means "no data" -- the camera could not determine the depth at that pixel. This is common at object edges, on featureless surfaces (blank walls), and at extreme distances.
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

## What's Next

- [Detect Objects (2D)](/vision/detect/) -- get 2D detections to combine with depth measurements.
- [Frame System](/motion-planning/frame-system/) -- set up coordinate frame transforms so 3D positions are usable by other components.
