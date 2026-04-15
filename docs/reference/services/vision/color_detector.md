---
title: "Configure a color_detector"
linkTitle: "color_detector"
weight: 20
type: "docs"
description: "Configure the color_detector vision service to find regions of a specific hue in camera images — no ML model required."
service_description: "A heuristic detector that draws boxes around regions of a specified hue."
tags: ["vision", "computer vision", "CV", "services", "detection"]
images: ["/services/vision/dog-detector.png"]
date: "2026-04-14"
aliases:
  - /operate/reference/services/vision/color_detector/
  - /services/vision/color_detector/
  - /ml/vision/color_detector/
  - /data-ai/services/vision/color_detector/
  - /tutorials/services/basic-color-detection/
  - /tutorials/services/try-viam-color-detection/
  - /tutorials/try-viam-color-detection/
  - /tutorials/viam-rover/try-viam-color-detection/
---

The `color_detector` vision service is a heuristic detector that draws boxes around connected regions of a specified hue. It runs entirely on the machine with no ML model. Use it for any task where the target stands out by color: red objects on a conveyor, green plants against soil, a blue marker against a wall.

The detector cannot detect black, white, or perfect grays (pixels whose red, green, and blue values are equal). It only detects hues on the color wheel.

{{% alert title="Tip" color="tip" %}}
Object colors vary dramatically with lighting. Verify your target color value under actual lighting conditions. Tools like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia) can extract a hex color from a screenshot of the camera feed. If the color is not reliably detected, increase `hue_tolerance_pct`.
{{% /alert %}}

## Configure

{{< tabs >}}
{{% tab name="Builder" %}}

1. Navigate to the **CONFIGURE** tab of your machine's page.
2. Click the **+** icon next to your machine part and select **Configuration block**.
3. In the search field, type `color detector` and select the `vision / color_detector` result.
4. Enter a name and click **Add component**.
5. Choose a color and a hue tolerance, then set a segment size in pixels.
6. Select a default camera.

{{< imgproc src="/services/vision/color-detector-panel.png" alt="Color detector panel showing color picker, hue tolerance, and segment size fields" resize="500x" declaredimensions=true >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<service_name>",
    "api": "rdk:service:vision",
    "model": "color_detector",
    "attributes": {
      "detect_color": "#RRGGBB",
      "hue_tolerance_pct": <number>,
      "segment_size_px": <integer>,
      "saturation_cutoff_pct": <number>,
      "value_cutoff_pct": <number>,
      "label": "<label>",
      "camera_name": "<camera-name>"
    }
  }
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "blue_square",
    "api": "rdk:service:vision",
    "model": "color_detector",
    "attributes": {
      "detect_color": "#1C4599",
      "hue_tolerance_pct": 0.07,
      "segment_size_px": 100,
      "value_cutoff_pct": 0.15,
      "label": "blue",
      "camera_name": "camera-1"
    }
  },
  {
    "name": "green_triangle",
    "api": "rdk:service:vision",
    "model": "color_detector",
    "attributes": {
      "detect_color": "#62963F",
      "hue_tolerance_pct": 0.05,
      "segment_size_px": 200,
      "value_cutoff_pct": 0.20,
      "label": "green",
      "camera_name": "camera-1"
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------- |
| `detect_color` | string | **Required** | The target color in hex format (`#RRGGBB`). Must not be black, white, or any grayscale value. |
| `hue_tolerance_pct` | float | **Required** | How much hue variation to accept, between `0.0` (exact match) and `1.0` (any color). Start at `0.05` and increase if detection is unreliable. Values outside `(0.0, 1.0]` fail at startup. |
| `segment_size_px` | int | **Required** | Minimum pixel area of a connected color region for it to count as a detection. Filters out small noise blobs. |
| `saturation_cutoff_pct` | float | Optional | Pixels with HSV saturation below this are treated as gray and ignored. Must be in `[0.0, 1.0]`. <br> Default: `0.2` |
| `value_cutoff_pct` | float | Optional | Pixels with HSV value (brightness) below this are treated as black and ignored. Must be in `[0.0, 1.0]`. <br> Default: `0.3` |
| `label` | string | Optional | Label applied to detected bounding boxes. If unset, detections have no label. |
| `camera_name` | string | Optional | Default camera for calls such as `GetDetectionsFromCamera`. Must name a configured camera. |

{{% alert title="Info" color="info" %}}
`hue_tolerance_pct`, `saturation_cutoff_pct`, and `value_cutoff_pct` describe cutoff thresholds using the HSV color model. They do not specify the absolute saturation or brightness of the target color. `hue_tolerance_pct` controls how strictly the detector matches your `detect_color`; the saturation and value cutoffs filter out pixels that are too gray or too dark before matching.
{{% /alert %}}

## Test your detector

### Live camera footage

1. Open your machine in the Viam app and either click the vision service's **Test** area or navigate to the **CONTROL** tab and select the vision service.
2. In the **Camera** dropdown, select the camera whose feed you want the detector to run on. Detections appear as bounding boxes on the live camera feed and refresh automatically.

{{< imgproc src="/services/vision/detections.png" alt="Live camera feed with bounding boxes drawn around detected regions" resize="450x" declaredimensions=true >}}

For a continuous overlay, configure a [transform camera](/operate/reference/components/camera/transform/):

```json
{
  "pipeline": [
    {
      "type": "detections",
      "attributes": {
        "confidence_threshold": 0.5,
        "detector_name": "<vision-service-name>",
        "valid_labels": ["<label>"]
      }
    }
  ],
  "source": "<camera-name>"
}
```

### Code

```python {class="line-numbers linkable-line-numbers"}
from viam.components.camera import Camera
from viam.services.vision import VisionClient

robot = await connect()
camera_name = "camera-1"

cam = Camera.from_robot(robot, camera_name)
my_detector = VisionClient.from_robot(robot, "blue_square")

# Get detections from the camera in one call
detections = await my_detector.get_detections_from_camera(camera_name)

# Or capture an image first, then run detections on it
images, _ = await cam.get_images()
img = images[0]
detections_from_image = await my_detector.get_detections(img)

await robot.close()
```

```go {class="line-numbers linkable-line-numbers"}
import (
  "go.viam.com/rdk/components/camera"
  "go.viam.com/rdk/services/vision"
)

cameraName := "camera-1"
myCam, err := camera.FromProvider(machine, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

myDetector, err := vision.FromProvider(machine, "blue_square")
if err != nil {
  logger.Fatalf("cannot get vision service: %v", err)
}

// Get detections from the camera in one call
detections, err := myDetector.DetectionsFromCamera(context.Background(), cameraName, nil)
if err != nil {
  logger.Fatalf("could not get detections: %v", err)
}
if len(detections) > 0 {
  logger.Info(detections[0])
}

// Or capture an image first, then run detections on it
img, err := camera.DecodeImageFromCamera(context.Background(), myCam, nil, nil)
if err != nil {
  logger.Fatalf("could not decode image: %v", err)
}
detectionsFromImage, err := myDetector.Detections(context.Background(), img, nil)
if err != nil {
  logger.Fatalf("could not get detections: %v", err)
}
if len(detectionsFromImage) > 0 {
  logger.Info(detectionsFromImage[0])
}
```

## Troubleshoot

{{< expand "Service fails to start with \"saturation of 0\" error" >}}

Your `detect_color` is black, white, or a perfect gray. The detector can only match hues on the color wheel. Pick a saturated color and try again.

{{< /expand >}}

{{< expand "Service fails to start with \"too unsaturated\" error" >}}

Your `detect_color` has saturation below the saturation cutoff. Either pick a more saturated color, or lower `saturation_cutoff_pct`.

{{< /expand >}}

{{< expand "Service fails to start with hue_tolerance_pct error" >}}

`hue_tolerance_pct` must be strictly greater than `0.0` and at most `1.0`. A value of `0` is not allowed because it would require a pixel-perfect hue match that camera noise makes effectively impossible.

{{< /expand >}}

{{< expand "Detector runs but returns no detections" >}}

- Check the color under actual lighting conditions. Use a color picker on a live camera screenshot to find the real hex value — the color on the object often looks different through the camera.
- Increase `hue_tolerance_pct` (try `0.10` to `0.15`) if the color is close but not exact.
- Lower `segment_size_px` if the color region in the image is small.
- If the lighting is dim, lower `value_cutoff_pct` (for example, `0.10`).

{{< /expand >}}

{{< expand "Detector returns too many false positives" >}}

- Decrease `hue_tolerance_pct` to require a closer match.
- Raise `saturation_cutoff_pct` to ignore washed-out regions.
- Increase `segment_size_px` to ignore small noise blobs.

{{< /expand >}}

## Next steps

{{< cards >}}
{{% card link="/vision/detect/" %}}
{{% card link="/vision/configure/" %}}
{{% card link="/reference/services/vision/mlmodel/" %}}
{{< /cards >}}
