---
linkTitle: "Camera calibration"
title: "Calibrate a camera for motion planning"
weight: 50
layout: "docs"
type: "docs"
description: "Compute camera intrinsic and distortion parameters for accurate 2D-to-3D projection."
aliases:
  - /work-cell-layout/calibrate-camera-to-robot/
  - /build/work-cell-layout/calibrate-camera-to-robot/
  - /motion-planning/camera-calibration/
---

A camera captures 2D images, but your robot operates in 3D space. Converting
a pixel coordinate to a real-world position, for example to tell the arm
where an object is, requires the camera's intrinsic parameters. These
parameters describe how the camera projects 3D space onto its 2D sensor. They
include the focal length, the principal point (the optical center), and the
lens distortion characteristics.

Without accurate intrinsics, every 2D-to-3D conversion will be wrong. Detected
objects will appear shifted, depth estimates will be inaccurate, and the arm will
miss its targets.

## Concepts

### Camera intrinsic parameters

| Parameter   | Description                                               |
| ----------- | --------------------------------------------------------- |
| `fx`        | Focal length in the x direction (pixels)                  |
| `fy`        | Focal length in the y direction (pixels)                  |
| `ppx`       | Principal point x coordinate (pixels), the optical center |
| `ppy`       | Principal point y coordinate (pixels), the optical center |
| `width_px`  | Image width in pixels                                     |
| `height_px` | Image height in pixels                                    |

### Distortion parameters

| Parameter | Description                              |
| --------- | ---------------------------------------- |
| `rk1`     | First radial distortion coefficient      |
| `rk2`     | Second radial distortion coefficient     |
| `rk3`     | Third radial distortion coefficient      |
| `tp1`     | First tangential distortion coefficient  |
| `tp2`     | Second tangential distortion coefficient |

Radial distortion causes barrel or pincushion effects. Tangential distortion
occurs when the lens is not perfectly parallel to the sensor.

### Eye-in-hand vs eye-to-hand

- **Eye-in-hand**: the camera is mounted on the arm, so its frame parent is
  the arm and the camera moves with the arm.
- **Eye-to-hand**: the camera is on a fixed mount, so its frame parent is the
  world frame and the camera stays stationary.

The calibration process is the same for both. Only the frame configuration
differs.

## Steps

### 1. Print a calibration target

Print a standard chessboard calibration pattern (at least 8x6 inner corners). The [Viam-labs calibration repository](https://github.com/viam-labs/camera-calibration) provides a
ready-to-print [A4 8x6 25 mm checkerboard](https://github.com/viam-labs/camera-calibration/blob/main/Checkerboard-A4-25mm-8x6.pdf).
Mount the print on a flat, rigid surface (foam board or a clipboard works well).
Measure the square size with a ruler to confirm your printer did not scale the pattern.

### 2. Capture calibration images

Open the camera on the **CONTROL** tab in the Viam app. Confirm the
camera's status badge reads **Ready**; if the card shows **Resource is
configuring...**, wait until configuration completes. In the camera's
Test view, use the refresh-interval dropdown in the top controls row
to select **Live** so the stream updates in real time. For each
chessboard pose, click **Export screenshot** to save a JPEG to your
computer. Collect 10-15 images covering a range of positions and
angles.

Guidelines:

- Cover the entire field of view (center, corners, edges).
- Vary the distance across your working range.
- Tilt the chessboard 15-30 degrees in different directions.
- Keep the full chessboard visible in every image.
- Avoid shadows, glare, and motion blur.

### 3. Run the calibration script

Download [`cameraCalib.py`](https://github.com/viam-labs/camera-calibration/blob/main/cameraCalib.py)
from the [camera-calibration repository](https://github.com/viam-labs/camera-calibration),
then run it:

```sh
pip3 install numpy opencv-python
python3 cameraCalib.py YOUR_PICTURES_DIRECTORY
```

A successful calibration produces output like:

```json
{
  "intrinsic_parameters": {
    "fx": 939.27,
    "fy": 940.29,
    "ppx": 320.61,
    "ppy": 239.14,
    "width_px": 640,
    "height_px": 480
  },
  "distortion_parameters": {
    "rk1": 0.0465,
    "rk2": 0.8003,
    "rk3": -5.408,
    "tp1": -0.000009,
    "tp2": -0.002829
  }
}
```

Check the reprojection error in the script's output. A value under 1.0 pixel
is good; a value above 2.0 indicates poor calibration, so retake the images.

### 4. Add parameters to camera config

```json
{
  "name": "my-camera",
  "api": "rdk:component:camera",
  "model": "webcam",
  "attributes": {
    "video_path": "video0",
    "width_px": 640,
    "height_px": 480,
    "intrinsic_parameters": {
      "fx": 939.27,
      "fy": 940.29,
      "ppx": 320.61,
      "ppy": 239.14,
      "width_px": 640,
      "height_px": 480
    },
    "distortion_parameters": {
      "rk1": 0.0465,
      "rk2": 0.8003,
      "rk3": -5.408,
      "tp1": -0.000009,
      "tp2": -0.002829
    }
  }
}
```

### 5. Configure the camera frame

**Eye-in-hand (camera mounted on the arm):**

```json
{
  "parent": "my-arm",
  "translation": { "x": 50, "y": 0, "z": 80 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 1, "z": 0, "th": -30 }
  }
}
```

**Eye-to-hand (camera on a fixed mount):**

```json
{
  "parent": "world",
  "translation": { "x": 500, "y": 300, "z": 800 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 180 }
  }
}
```

### 6. Verify calibration accuracy

Check the calibration against a known position before trusting it. Place an
object where you can measure its real-world position, then use `TransformPose`
to convert the detected position from camera frame to world frame and compare
the two.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import PoseInFrame, Pose

detected_in_camera = PoseInFrame(
    reference_frame="my-camera",
    pose=Pose(x=50, y=30, z=400)
)

detected_in_world = await machine.transform_pose(detected_in_camera, "world")
print("Detected position in world frame:")
print(f"  x={detected_in_world.pose.x:.1f} mm")
print(f"  y={detected_in_world.pose.y:.1f} mm")
print(f"  z={detected_in_world.pose.z:.1f} mm")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
detectedInCamera := referenceframe.NewPoseInFrame("my-camera",
    spatialmath.NewPoseFromPoint(r3.Vector{X: 50, Y: 30, Z: 400}))

detectedInWorld, err := machine.TransformPose(ctx, detectedInCamera, "world", nil)
if err != nil {
    logger.Fatal(err)
}

pt := detectedInWorld.Pose().Point()
fmt.Printf("Detected position in world frame:\n")
fmt.Printf("  x=%.1f mm\n", pt.X)
fmt.Printf("  y=%.1f mm\n", pt.Y)
fmt.Printf("  z=%.1f mm\n", pt.Z)
```

{{% /tab %}}
{{< /tabs >}}

If the computed position is within 10-20 mm of the measured position at a
working distance of 500-1000 mm, your calibration is good.

For a visual sanity check, open the [3D SCENE tab](/motion-planning/3d-scene/).
The camera frame should sit in the correct position and orientation relative
to the arm, and any visible obstacles should appear in plausible locations.
See [Calibrate frame offsets](/motion-planning/3d-scene/calibrate-frame-offsets/)
for the full workflow.

## Troubleshooting

{{< expand "Calibration script fails to find chessboard corners" >}}

- Verify the chessboard is fully visible in every image.
- Check lighting. Shadows and glare prevent corner detection.
- Ensure the chessboard is flat, not curled.
- Verify the expected pattern size matches your chessboard.

{{< /expand >}}

{{< expand "3D positions are consistently offset" >}}

- Check the camera frame translation. Measure the physical offset and update.
- Check the camera frame orientation. A tilted camera needs the tilt reflected.
- Verify the parent frame is correct (arm vs world).

{{< /expand >}}

{{< expand "Accuracy varies with distance" >}}

- Depth errors grow with distance for all depth cameras.
- Re-run calibration with more images at your target working distance.
- Check the camera's specified depth range.

{{< /expand >}}

## What's next

- [Define your frame system](/motion-planning/frame-system/): configure
  component frames for spatial reasoning.
- [Define obstacles](/motion-planning/obstacles/): add collision geometry using
  calibrated camera data.
- [Move an arm to a target pose](/motion-planning/move-an-arm/move-to-pose/):
  use calibrated positions to plan arm movements.
