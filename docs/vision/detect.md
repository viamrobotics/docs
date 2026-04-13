---
linkTitle: "Detect objects"
title: "Detect objects"
weight: 20
layout: "docs"
type: "docs"
description: "Retrieve 2D bounding-box detections from a vision service, filter by confidence and class, and run detections in a loop."
date: "2025-01-30"
aliases:
  - /build/vision-detection/detect-objects-2d/
  - /vision-detection/detect-objects-2d/
---

Your vision service is configured and running, but you need to do something useful with the results. This how-to shows you how to retrieve detections programmatically, filter them to reduce noise, and extract the information you need to build real applications -- counting objects, triggering actions when something appears, or feeding positions into a control loop.

## Concepts

### What a detection contains

A detection is a single recognized object in an image. Each detection includes:

| Field        | Type            | Description                                                                 |
| ------------ | --------------- | --------------------------------------------------------------------------- |
| `class_name` | String          | The label assigned by the model (for example, "person", "dog", "stop-sign") |
| `confidence` | Float (0.0-1.0) | How confident the model is in this detection                                |
| `x_min`      | Integer         | Left edge of the bounding box in pixels                                     |
| `y_min`      | Integer         | Top edge of the bounding box in pixels                                      |
| `x_max`      | Integer         | Right edge of the bounding box in pixels                                    |
| `y_max`      | Integer         | Bottom edge of the bounding box in pixels                                   |

The bounding box coordinates use the image coordinate system: (0,0) is the top-left corner, x increases to the right, y increases downward. The bounding box is axis-aligned (not rotated).

Detections also include normalized coordinates (`x_min_normalized`, `y_min_normalized`, `x_max_normalized`, `y_max_normalized`) as floats between 0.0 and 1.0, representing positions relative to image dimensions. These are useful when you need resolution-independent coordinates.

A single call to the detection API can return zero, one, or many detections. The number depends on how many objects the model finds in the frame.

### GetDetections vs GetDetectionsFromCamera

The vision service provides two methods for getting detections:

- **GetDetectionsFromCamera** takes a camera name and handles everything: it captures an image from the camera, runs it through the model, and returns detections. This is the simplest approach and the one you should use in most cases.
- **GetDetections** takes an image you already have and runs it through the model. Use this when you need to run detection on an image you captured separately, an image from a file, or an image you have preprocessed.

### Confidence thresholds

Every detection has a confidence score between 0.0 and 1.0. A score of 0.95 means the model is very confident; a score of 0.3 means it is guessing. Models often produce many low-confidence detections that are noise rather than real objects.

Choosing the right threshold depends on your application:

- **Safety-critical applications** (such as detecting people before a robot moves): use a low threshold (0.3-0.5) to avoid missing real objects, and accept some false positives.
- **Counting or logging applications**: use a higher threshold (0.7-0.9) to reduce noise and get accurate counts.
- **Start at 0.5** and adjust based on what you observe.

### The color_detector alternative

Not every detection task requires a trained ML model. Viam includes a built-in `color_detector` vision service model that detects regions of a specified color. This is useful for simple tasks like finding a red ball or detecting a blue marker. It requires no model training, no GPU, and minimal configuration.

## Steps

### 1. Get detections from a camera

The simplest way to get detections is to let the vision service capture an image and run the model in one call.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from viam.robot.client import RobotClient
from viam.services.vision import VisionClient


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    detector = VisionClient.from_robot(robot, "my-detector")

    # Get detections directly from the camera
    detections = await detector.get_detections_from_camera("my-camera")

    for d in detections:
        print(f"{d.class_name}: {d.confidence:.2f} "
              f"at ({d.x_min},{d.y_min})-({d.x_max},{d.y_max})")

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

    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/services/vision"
    "go.viam.com/utils/rpc"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("detect")

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

    detector, err := vision.FromProvider(machine, "my-detector")
    if err != nil {
        logger.Fatal(err)
    }

    detections, err := detector.DetectionsFromCamera(ctx, "my-camera", nil)
    if err != nil {
        logger.Fatal(err)
    }

    for _, d := range detections {
        fmt.Printf("%s: %.2f at (%d,%d)-(%d,%d)\n",
            d.Label(), d.Score(),
            d.BoundingBox().Min.X, d.BoundingBox().Min.Y,
            d.BoundingBox().Max.X, d.BoundingBox().Max.Y)
    }
}
```

{{% /tab %}}
{{< /tabs >}}

### 2. Get detections from an existing image

If you already have an image -- from a file, from a previous capture, or from a different camera -- you can run detection on it directly.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.camera import Camera
from viam.services.vision import VisionClient

camera = Camera.from_robot(robot, "my-camera")
detector = VisionClient.from_robot(robot, "my-detector")

# Capture images from the camera
images, _ = await camera.get_images()

# Run detection on the first image
detections = await detector.get_detections(images[0])

for d in detections:
    print(f"{d.class_name}: {d.confidence:.2f}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
cam, err := camera.FromProvider(machine, "my-camera")
if err != nil {
    logger.Fatal(err)
}

detector, err := vision.FromProvider(machine, "my-detector")
if err != nil {
    logger.Fatal(err)
}

// Capture an image first
images, _, err := cam.Images(ctx, nil, nil)
if err != nil {
    logger.Fatal(err)
}
img, err := images[0].Image(ctx)
if err != nil {
    logger.Fatal(err)
}

// Run detection on the captured image
detections, err := detector.Detections(ctx, img, nil)
if err != nil {
    logger.Fatal(err)
}

for _, d := range detections {
    fmt.Printf("%s: %.2f\n", d.Label(), d.Score())
}
```

{{% /tab %}}
{{< /tabs >}}

### 3. Filter detections by confidence

In practice, you almost always want to filter out low-confidence detections. Apply a threshold before processing results.

{{< tabs >}}
{{% tab name="Python" %}}

```python
CONFIDENCE_THRESHOLD = 0.7

detections = await detector.get_detections_from_camera("my-camera")

# Filter to only high-confidence detections
confident_detections = [
    d for d in detections
    if d.confidence >= CONFIDENCE_THRESHOLD
]

print(f"{len(confident_detections)} of {len(detections)} "
      f"detections above {CONFIDENCE_THRESHOLD} threshold")

for d in confident_detections:
    print(f"  {d.class_name}: {d.confidence:.2f}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
confidenceThreshold := 0.7

detections, err := detector.DetectionsFromCamera(ctx, "my-camera", nil)
if err != nil {
    logger.Fatal(err)
}

total := len(detections)
var confident []objectdetection.Detection
for _, d := range detections {
    if d.Score() >= confidenceThreshold {
        confident = append(confident, d)
    }
}

fmt.Printf("%d of %d detections above %.1f threshold\n",
    len(confident), total, confidenceThreshold)

for _, d := range confident {
    fmt.Printf("  %s: %.2f\n", d.Label(), d.Score())
}
```

{{% /tab %}}
{{< /tabs >}}

### 4. Filter detections by class

When your model detects multiple object types, you may only care about specific classes.

{{< tabs >}}
{{% tab name="Python" %}}

```python
TARGET_CLASSES = {"person", "dog"}

detections = await detector.get_detections_from_camera("my-camera")

targets = [
    d for d in detections
    if d.class_name in TARGET_CLASSES and d.confidence >= 0.6
]

for d in targets:
    width = d.x_max - d.x_min
    height = d.y_max - d.y_min
    print(f"{d.class_name}: {d.confidence:.2f}, "
          f"size {width}x{height} pixels")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
targetClasses := map[string]bool{"person": true, "dog": true}

detections, err := detector.DetectionsFromCamera(ctx, "my-camera", nil)
if err != nil {
    logger.Fatal(err)
}

for _, d := range detections {
    if targetClasses[d.Label()] && d.Score() >= 0.6 {
        bb := d.BoundingBox()
        width := bb.Max.X - bb.Min.X
        height := bb.Max.Y - bb.Min.Y
        fmt.Printf("%s: %.2f, size %dx%d pixels\n",
            d.Label(), d.Score(), width, height)
    }
}
```

{{% /tab %}}
{{< /tabs >}}

### 5. Run detections in a loop

Most real applications need continuous detection, not a single snapshot. Run detections in a loop with a short delay to avoid overwhelming the system.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
import time

CONFIDENCE_THRESHOLD = 0.7

detector = VisionClient.from_robot(robot, "my-detector")

while True:
    start = time.time()
    detections = await detector.get_detections_from_camera("my-camera")

    confident = [d for d in detections if d.confidence >= CONFIDENCE_THRESHOLD]
    elapsed = time.time() - start

    if confident:
        names = [f"{d.class_name}({d.confidence:.2f})" for d in confident]
        print(f"[{elapsed:.2f}s] Detected: {', '.join(names)}")
    else:
        print(f"[{elapsed:.2f}s] No detections")

    await asyncio.sleep(0.1)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
confidenceThreshold := 0.7

detector, err := vision.FromProvider(machine, "my-detector")
if err != nil {
    logger.Fatal(err)
}

for {
    start := time.Now()
    detections, err := detector.DetectionsFromCamera(ctx, "my-camera", nil)
    if err != nil {
        logger.Error(err)
        time.Sleep(time.Second)
        continue
    }

    elapsed := time.Since(start)
    var confident []objectdetection.Detection
    for _, d := range detections {
        if d.Score() >= confidenceThreshold {
            confident = append(confident, d)
        }
    }

    if len(confident) > 0 {
        for _, d := range confident {
            fmt.Printf("[%v] %s: %.2f\n", elapsed, d.Label(), d.Score())
        }
    } else {
        fmt.Printf("[%v] No detections\n", elapsed)
    }

    time.Sleep(100 * time.Millisecond)
}
```

{{% /tab %}}
{{< /tabs >}}

## Alternatives and advanced usage

### 6. Use the color_detector (no ML model needed)

For simple color-based detection, configure a vision service with the `color_detector` model instead of `mlmodel`. This requires no trained model.

```json
{
  "name": "red-detector",
  "api": "rdk:service:vision",
  "model": "color_detector",
  "attributes": {
    "detect_color": "#FF0000",
    "hue_tolerance_pct": 0.1,
    "segment_size_px": 200
  }
}
```

| Attribute               | Type   | Required     | Description                                                                                                     |
| ----------------------- | ------ | ------------ | --------------------------------------------------------------------------------------------------------------- |
| `detect_color`          | string | **Required** | Target color in hex format (for example, `"#FF0000"`). Cannot be black, white, or grayscale.                    |
| `hue_tolerance_pct`     | float  | **Required** | How much the hue can vary from the target (must be > 0.0 and <= 1.0). A value of 0.1 means 10% tolerance.       |
| `segment_size_px`       | int    | **Required** | Minimum number of pixels a detected region must contain to count as a detection.                                |
| `saturation_cutoff_pct` | float  | Optional     | Minimum saturation for a pixel to be considered a match. Default: `0.2`. Increase to reject washed-out colors.  |
| `value_cutoff_pct`      | float  | Optional     | Minimum brightness value for a pixel to be considered a match. Default: `0.3`. Increase to reject dark regions. |
| `label`                 | string | Optional     | The label to assign to detections. If omitted, detections have no class name.                                   |
| `camera_name`           | string | Optional     | Default camera to use with `GetDetectionsFromCamera` if no camera name is specified in the request.             |

The detection API works identically whether you use `mlmodel` or `color_detector`. Your code does not need to change.

### 7. Get everything in one call with CaptureAllFromCamera

If you need the image and its detections (and optionally classifications) together, use `CaptureAllFromCamera` instead of separate calls. This is more efficient when you need multiple result types and ensures the detections correspond exactly to the returned image.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.vision import VisionClient

detector = VisionClient.from_robot(robot, "my-detector")

result = await detector.capture_all_from_camera(
    "my-camera",
    return_image=True,
    return_detections=True,
    return_classifications=True
)

image = result.image            # The captured image
detections = result.detections  # Detections for that exact image
classifications = result.classifications  # Classifications too
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
captOpts := viscapture.CaptureOptions{
    ReturnImage:           true,
    ReturnDetections:      true,
    ReturnClassifications: true,
}

result, err := detector.CaptureAllFromCamera(
    context.Background(), "my-camera", captOpts, nil)
if err != nil {
    logger.Fatal(err)
}

img := result.Image
detections := result.Detections
classifications := result.Classifications
```

{{% /tab %}}
{{< /tabs >}}

This is particularly useful for data logging, visualization, or any case where you need to correlate results with the exact frame that produced them.

## Try It

1. Run the detection loop from step 5. Point your camera at objects your model recognizes and observe the output.
2. Adjust the confidence threshold and notice how it affects the number of detections. Try 0.3, 0.5, 0.7, and 0.9.
3. Add class filtering to focus on a specific object type.
4. If you do not have a trained model, configure a `color_detector` and point the camera at a brightly colored object.

## Troubleshooting

{{< expand "No detections returned" >}}

- Verify the vision service is working in the CONTROL tab first. If detections appear there but not in your code, the issue is in your code.
- Check that the camera name in your code matches the camera name in your configuration exactly.
- Lower the confidence threshold. The model may be producing detections with low confidence that are being filtered out.
- Ensure the camera is pointing at objects the model was trained to recognize.

{{< /expand >}}

{{< expand "Detections are slow" >}}

- TFLite models on a Raspberry Pi typically run at 2-10 frames per second depending on model size. This is normal.
- Reduce camera resolution to speed up inference. A 640x480 image processes faster than 1920x1080.
- Avoid calling `get_detections_from_camera` faster than the model can process. The `asyncio.sleep` or `time.Sleep` in the loop prevents this.

{{< /expand >}}

{{< expand "Bounding boxes are in the wrong position" >}}

- The bounding box coordinates are in pixel space relative to the image dimensions. If you are overlaying boxes on a resized image, scale the coordinates proportionally.
- Verify the camera orientation. If the camera is mounted upside down, the coordinates will appear inverted.

{{< /expand >}}

{{< expand "Color detector finds nothing" >}}

- Use a color picker tool to get the exact hex color of your target object under the camera's lighting conditions. Colors shift significantly under different lighting.
- Increase `hue_tolerance_pct` to allow more variation. Start at 0.2 and increase if needed.
- Decrease `segment_size_px` if the target object appears small in the frame.

{{< /expand >}}

## What's Next

- [Classify Objects](/vision/classify/) -- use whole-image classification instead of per-object bounding boxes.
- [Track Objects Across Frames](/vision/track/) -- maintain persistent identities for detected objects as they move between frames.
- [Localize Objects in 3D](/vision/measure-depth/) -- combine 2D detections with depth data to get real-world 3D positions.
