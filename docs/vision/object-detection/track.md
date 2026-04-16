---
linkTitle: "Track objects"
title: "Track objects across frames"
weight: 40
layout: "docs"
type: "docs"
description: "Track detected objects across consecutive video frames with persistent IDs using the object-tracker module."
date: "2025-01-30"
aliases:
  - /build/vision-detection/track-objects-across-frames/
  - /vision-detection/track-objects-across-frames/
  - /vision/track/
---

Object detection operates on single frames. It tells you what is in the image right now, but nothing about what was in the previous frame. When you run detections at 5 frames per second, you get 5 independent lists of bounding boxes with no way to tell whether a detection in frame 2 corresponds to the same object as in frame 1.

The [`viam:object-tracker` module](https://app.viam.com/module/viam/object-tracker) solves this problem. It wraps an existing detector and camera, matches detections across consecutive frames, and assigns each tracked object a stable ID. With track IDs you can answer questions like "how many cars have passed through this intersection?" and "how long has this person been standing here?"

## How it works

The object tracker sits between your detector and your application code:

1. Your **camera** provides the image stream.
2. Your **detector** (a vision service) runs on each frame and returns detections.
3. The **object tracker** matches new detections to existing tracks using the [Hungarian algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm). Unmatched detections become new tracks. Tracks with no matching detection for several frames are removed.

Each tracked object gets a persistent class name in the format:

```text
<class>_<N>_<YYYYMMDD>_<HHMMSS>
```

For example, the first person detected becomes `person_0_20250413_143052`. The `person_0` portion is the stable track ID. The timestamp records when the object was first detected.

## Prerequisites

- A configured [camera](/hardware/common-components/add-a-camera/)
- A configured vision service detector (see [Configure a vision pipeline](/vision/configure/))

## Configure the object tracker

### 1. Add the object-tracker vision service

1. Click **+** and select **Configuration block**.
2. In the search field, type `object-tracker` and select the `viam:vision:object-tracker` result (the card shows the module name and model name; the badge says `VISION`).
3. Click **Add component**, name the service (for example, `my-tracker`), and click **Add component** again to confirm. The module is installed automatically.

### 2. Configure attributes

Set the required attributes:

```json
{
  "camera_name": "my-camera",
  "detector_name": "my-detector"
}
```

| Attribute               | Type   | Required | Default | Description                                                                                     |
| ----------------------- | ------ | -------- | ------- | ----------------------------------------------------------------------------------------------- |
| `camera_name`           | string | **Yes**  | None    | Name of the configured camera component.                                                        |
| `detector_name`         | string | **Yes**  | None    | Name of the configured vision detector service.                                                 |
| `min_confidence`        | float  | No       | 0.2     | Minimum confidence threshold for detections (0 to 1).                                           |
| `max_frequency_hz`      | float  | No       | 10      | Maximum rate at which the tracker processes frames.                                             |
| `chosen_labels`         | object | No       | None    | Map of class names to confidence thresholds. Only detections matching these labels are tracked. |
| `trigger_cool_down_s`   | float  | No       | 5       | Seconds before a trigger resets after firing.                                                   |
| `buffer_size`           | int    | No       | 30      | Number of frames to buffer lost detections before removing a track (1 to 256).                  |
| `min_track_persistence` | int    | No       | 1       | Number of consecutive frames a track must appear in before it is returned in detection results. |

Click **Save**.

**Full example configuration:**

```json
{
  "camera_name": "my-camera",
  "detector_name": "my-detector",
  "min_confidence": 0.5,
  "max_frequency_hz": 10,
  "chosen_labels": {
    "person": 0.7,
    "dog": 0.3
  },
  "buffer_size": 30,
  "min_track_persistence": 3
}
```

## Use the tracker

The object tracker exposes the standard vision service API. Call `GetDetectionsFromCamera` or `GetDetections` to get tracked detections with persistent IDs.

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

    tracker = VisionClient.from_robot(robot, "my-tracker")

    while True:
        detections = await tracker.get_detections_from_camera("my-camera")

        for d in detections:
            # class_name contains the track ID, for example "person_0_20250413_143052"
            print(f"{d.class_name}: {d.confidence:.2f} "
                  f"at ({d.x_min},{d.y_min})-({d.x_max},{d.y_max})")

        await asyncio.sleep(0.2)

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
    "time"

    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/services/vision"
    "go.viam.com/utils/rpc"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("tracker")

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

    tracker, err := vision.FromProvider(machine, "my-tracker")
    if err != nil {
        logger.Fatal(err)
    }

    for {
        detections, err := tracker.DetectionsFromCamera(ctx, "my-camera", nil)
        if err != nil {
            logger.Error(err)
            time.Sleep(time.Second)
            continue
        }

        for _, d := range detections {
            // Label() contains the track ID, for example "person_0_20250413_143052"
            fmt.Printf("%s: %.2f at (%d,%d)-(%d,%d)\n",
                d.Label(), d.Score(),
                d.BoundingBox().Min.X, d.BoundingBox().Min.Y,
                d.BoundingBox().Max.X, d.BoundingBox().Max.Y)
        }

        time.Sleep(200 * time.Millisecond)
    }
}
```

{{% /tab %}}
{{< /tabs >}}

### Count entries and exits

Use `GetClassificationsFromCamera` to detect when new objects enter the scene. The tracker returns a `new-object-detected` classification when a fresh object appears.

### Extract the track ID

Parse the class name to extract a stable track ID for grouping detections over time:

{{< tabs >}}
{{% tab name="Python" %}}

```python
def get_track_id(class_name: str) -> str:
    """Extract stable track ID from tracker class name.

    'person_0_20250413_143052' -> 'person_0'
    """
    parts = class_name.split("_")
    if len(parts) >= 2:
        return f"{parts[0]}_{parts[1]}"
    return class_name
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func getTrackID(className string) string {
    parts := strings.SplitN(className, "_", 3)
    if len(parts) >= 2 {
        return parts[0] + "_" + parts[1]
    }
    return className
}
```

{{% /tab %}}
{{< /tabs >}}

## Tune tracking parameters

- **`min_confidence`**: raise this to reduce noisy detections that create spurious tracks. Start at 0.5 for most use cases.
- **`buffer_size`**: controls how long a lost track is kept before being removed. Increase for scenes with frequent occlusion (objects passing behind other objects). Decrease for faster exit detection.
- **`min_track_persistence`**: increase to filter out brief false detections. A value of 3 means an object must be detected in 3 consecutive frames before the tracker reports it.
- **`max_frequency_hz`**: lower this on resource-constrained devices to reduce CPU usage.
- **`chosen_labels`**: use this to track only specific classes. For example, to track only people with high confidence: `{"person": 0.7}`.

## Troubleshooting

{{< expand "Tracks keep switching IDs" >}}

- Increase `min_confidence` to reduce noisy detections that confuse the matching algorithm.
- If objects are close together and frequently swap IDs, increase `min_track_persistence` so only stable tracks are reported.

{{< /expand >}}

{{< expand "Tracks are lost too quickly" >}}

- Increase `buffer_size`. If your detection model occasionally misses an object for a few frames, a higher value keeps the track alive through the gap.
- Check your detection confidence threshold. If it is too high, the model may intermittently fail to detect objects, causing track loss.

{{< /expand >}}

{{< expand "Too many tracks for the same object" >}}

- Increase `min_track_persistence` so brief, unstable detections are not reported.
- If the underlying detector produces inconsistent bounding boxes, the tracker may fail to match them across frames. Try a different or better-trained model.

{{< /expand >}}

{{< expand "No detections returned" >}}

- Verify the underlying detector works by testing it directly. On the **CONTROL** tab, check that detections appear from the detector vision service before adding the tracker.
- Verify `camera_name` and `detector_name` in the tracker configuration match the names of your configured camera and detector exactly.

{{< /expand >}}

## What's next

- [Detect objects](/vision/object-detection/detect/): learn about the detection API the tracker builds on.
- [Act on detections](/vision/object-detection/act-on-detections/): build modules that respond to detection or classification results.
- [Alert on detections](/vision/object-detection/alert-on-detections/): send alerts when tracked objects enter or exit a scene.
