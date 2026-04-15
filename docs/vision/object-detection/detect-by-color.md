---
linkTitle: "Detect by color"
title: "Detect objects by color"
weight: 20
layout: "docs"
type: "docs"
description: "Configure the color_detector vision service to find regions of a specific hue. No ML model, no training data, runs anywhere."
date: "2026-04-14"
aliases:
  - /vision/detect-by-color/
---

Use the `color_detector` vision service when you need to detect objects that stand out by color. It runs a heuristic hue-match on every frame with no ML model, no training data, and negligible compute cost.

Typical use cases: detecting colored markers, sorting parts by color on a conveyor, finding a red stop button, spotting a green plant against soil. If the target objects share a distinct hue and the background does not, color detection is the simplest possible vision pipeline.

## When to use color detection vs ML detection

Pick **color detection** when:

- The target has a specific, saturated hue.
- Lighting conditions are controlled or predictable.
- You do not have labeled training data (or it is not worth collecting).
- You need zero cold-start time and low compute.

Pick **ML detection** when:

- The target varies in color or texture (for example, "detect any person").
- Lighting changes significantly across sessions.
- Multiple distinct object classes matter.
- You have labeled training data or can use a pre-trained model from the [registry](https://app.viam.com/registry).

You can also combine them: a color detector for a known marker alongside an ML detector for people and obstacles.

## Limits of color detection

The `color_detector` model runs a heuristic on HSV color values. It cannot detect:

- **Black, white, or perfect grays.** Pixels where red, green, and blue values are equal have no hue and are rejected.
- **Objects defined by shape instead of color.** A red ball and a red stop sign both look the same.
- **Colors that shift significantly with lighting.** A red object looks orange under warm light and purple under UV. Retune hue tolerance for each lighting condition, or use ML detection instead.

## 1. Pick a target color

Get the actual hex color of your target as the camera sees it, not the color you think it is. Lighting, white balance, and the camera sensor all shift color values.

The practical approach:

1. Configure the camera on your machine and navigate to its **Test** panel in the Viam app.
2. Take a screenshot of the camera feed with the target object clearly visible.
3. Use a pixel-level color picker on the screenshot (browser extensions like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia) work well).
4. Sample three or four pixels on different parts of the object. Note the hex values.
5. Pick one as your `detect_color`. If the values vary, you will need a wider `hue_tolerance_pct` in step 3.

## 2. Add the color_detector vision service

1. Open the **CONFIGURE** tab in the Viam app.
2. Click the **+** icon and select **Configuration block**.
3. In the search field, type `color detector` and select the `vision/color_detector` result.
4. Click **Add component**, name the service (for example, `red_detector`), and click **Add component** again to confirm.

## 3. Configure the detector

```json
{
  "name": "red_detector",
  "api": "rdk:service:vision",
  "model": "color_detector",
  "attributes": {
    "detect_color": "#C43131",
    "hue_tolerance_pct": 0.07,
    "segment_size_px": 200,
    "label": "red",
    "camera_name": "camera-1"
  }
}
```

- `detect_color`: the hex color from step 1. Must be a saturated hue (not black, white, or gray).
- `hue_tolerance_pct`: how wide a hue band to accept, between `0.0` (exact) and `1.0` (any color). Start with `0.05` and raise if detection is unreliable.
- `segment_size_px`: minimum pixel area of a connected color region. Filters out small noise blobs. Start with `100` and raise if you get too many false positives on small specks.
- `label`: the label applied to detected boxes. Optional but recommended for multi-detector pipelines.
- `camera_name`: the camera this detector should use by default.

See the [color_detector reference](/reference/services/vision/color_detector/) for every attribute including the optional `saturation_cutoff_pct` and `value_cutoff_pct`.

Save the configuration.

## 4. Verify in the Control tab

1. Navigate to the **CONTROL** tab.
2. Click your vision service.
3. In the **Camera** dropdown, select the camera whose feed you want the detector to run on. Bounding boxes appear as an overlay on the live camera feed and refresh automatically.

Point the camera at the target color. Bounding boxes should appear around regions of that hue. If you see:

- **No boxes:** the color under the actual lighting differs from `detect_color`. Sample a live screenshot, update `detect_color`, or raise `hue_tolerance_pct`.
- **Too many boxes on small specks:** raise `segment_size_px`.
- **Boxes on washed-out regions:** raise `saturation_cutoff_pct` (default `0.2`).
- **Boxes on dark regions that look black:** raise `value_cutoff_pct` (default `0.3`).

Tuning is quick: each change takes a `viam-server` reload (a few seconds) to apply.

## 5. Use detections in code

Color detections come through the same vision service API as ML detections. Any code that works with `GetDetections` works with a color detector.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio

from viam.robot.client import RobotClient
from viam.services.vision import VisionClient


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID",
    )
    return await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)


async def main():
    machine = await connect()
    detector = VisionClient.from_robot(machine, "red_detector")

    detections = await detector.get_detections_from_camera("camera-1")

    for d in detections:
        print(f"{d.class_name}: confidence {d.confidence:.2f}, "
              f"box ({d.x_min}, {d.y_min}) to ({d.x_max}, {d.y_max})")

    await machine.close()


if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
  "context"

  "go.viam.com/rdk/logging"
  "go.viam.com/rdk/robot/client"
  "go.viam.com/rdk/services/vision"
  "go.viam.com/utils/rpc"
)

func main() {
  ctx := context.Background()
  logger := logging.NewLogger("detector")

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

  detector, err := vision.FromProvider(machine, "red_detector")
  if err != nil {
    logger.Fatal(err)
  }

  detections, err := detector.DetectionsFromCamera(ctx, "camera-1", nil)
  if err != nil {
    logger.Fatal(err)
  }

  for _, d := range detections {
    bb := d.BoundingBox()
    logger.Infof("%s: score %.2f, box (%d,%d)-(%d,%d)",
      d.Label(), d.Score(), bb.Min.X, bb.Min.Y, bb.Max.X, bb.Max.Y)
  }
}
```

{{% /tab %}}
{{< /tabs >}}

## Use multiple color detectors

You can configure multiple `color_detector` services against the same camera, each tuned for a different color. This is the simplest way to tag parts by color: one detector per color, each with its own `label`.

```json
"services": [
  {
    "name": "red_parts",
    "api": "rdk:service:vision",
    "model": "color_detector",
    "attributes": {
      "detect_color": "#C43131",
      "hue_tolerance_pct": 0.07,
      "segment_size_px": 150,
      "label": "red",
      "camera_name": "camera-1"
    }
  },
  {
    "name": "blue_parts",
    "api": "rdk:service:vision",
    "model": "color_detector",
    "attributes": {
      "detect_color": "#1C4599",
      "hue_tolerance_pct": 0.07,
      "segment_size_px": 150,
      "label": "blue",
      "camera_name": "camera-1"
    }
  }
]
```

Your code queries each detector in sequence. For higher throughput, call them concurrently.

## Troubleshooting

{{< expand "Service fails to start" >}}

- **"saturation of 0" error:** `detect_color` is black, white, or a perfect gray. Pick a saturated color.
- **"too unsaturated" error:** `detect_color` has saturation below `saturation_cutoff_pct`. Pick a more saturated color or lower the cutoff.
- **"hue_tolerance_pct must be greater than 0.0":** the value was omitted or set to zero. Set it to a value between `0.01` and `1.0`.

{{< /expand >}}

{{< expand "Color looks right to me but the detector sees nothing" >}}

What your eye sees and what the camera records are often different:

- White balance settings on the camera can shift all hues.
- Low lighting makes everything look less saturated.
- Some cameras apply aggressive noise reduction that washes out edges.

Sample the actual on-screen color from a live camera screenshot and use that hex value. Adjust `hue_tolerance_pct` up if you still do not get detections.

{{< /expand >}}

{{< expand "Works in testing, fails in production" >}}

Color detection is sensitive to lighting changes. A system that works under controlled lab lighting often fails under sunlight, under fluorescent lights (which flicker at 50 or 60 Hz and can beat against camera frame rates), or under mixed light.

Fixes, in order of preference:

1. Add consistent artificial lighting so the target color does not shift.
2. Switch to an [ML-based detector](/vision/deploy-and-maintain/deploy-from-registry/) trained on images from the actual production environment.

{{< /expand >}}

## Next steps

- [color_detector reference](/reference/services/vision/color_detector/): every attribute
- [Detect objects](/vision/object-detection/detect/): write code that uses detection results
- [Deploy an ML model](/vision/deploy-and-maintain/deploy-from-registry/): when color detection is too fragile
