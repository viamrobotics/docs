---
linkTitle: "Classify images"
title: "Classify images"
weight: 30
layout: "docs"
type: "docs"
description: "Use a vision service to classify images by label and confidence, make decisions based on classification, and monitor scenes continuously."
date: "2025-01-30"
aliases:
  - /build/vision-detection/classify-objects/
  - /vision-detection/classify-objects/
---

Detection tells you where objects are in an image. Classification tells you what the entire image (or a region of it) contains. If you need to answer "is this a picture of a cat or a dog?" rather than "where are the cats and dogs in this picture?", classification is the right tool. This how-to shows you how to get classifications from your vision service and use them in application logic.

## Concepts

### What a classification contains

A classification is a label paired with a confidence score. Unlike detections, classifications do not include spatial information: there are no bounding box coordinates. Each classification describes the image as a whole.

| Field        | Type            | Description                                                          |
| ------------ | --------------- | -------------------------------------------------------------------- |
| `class_name` | String          | The label assigned by the model (for example, "cat", "dog", "empty") |
| `confidence` | Float (0.0-1.0) | How confident the model is in this label                             |

A single classification call returns multiple results ranked by confidence. The `count` parameter controls how many top results to return.

### Single-label vs multi-label classification

**Single-label classification** assumes the image belongs to exactly one category. The confidences across all classes sum to approximately 1.0, so a cat score of `0.85` leaves `0.15` of confidence spread across the remaining classes. Most classification models work this way.

**Multi-label classification** allows the image to belong to multiple categories simultaneously. An image could be classified as both "outdoor: 0.92" and "sunny: 0.88" at the same time. The confidences are independent and do not sum to 1.0.

The API is the same for both. The difference is in how the model was trained and how you interpret the results.

### The count parameter

The `count` parameter tells the vision service how many top classifications to return. If `count=3`, you get the three highest-confidence labels. This is useful for:

- Understanding what else the model considered (was it confused between two classes?)
- Multi-label classification where you want all relevant labels
- Debugging model performance by seeing the runner-up predictions

### Classification vs detection: when to use which

| Use classification when              | Use detection when                 |
| ------------------------------------ | ---------------------------------- |
| You care about the whole scene       | You care about individual objects  |
| You need a yes/no or category answer | You need object locations          |
| There is one dominant subject        | There are multiple objects to find |
| You want to sort or categorize       | You want to count or track         |

You can use both on the same camera. Run a classifier for scene-level understanding and a detector for object-level detail.

## Steps

### 1. Get classifications from a camera

The simplest approach lets the vision service capture an image and classify it in one call.

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

    classifier = VisionClient.from_robot(robot, "my-classifier")

    # Get top 3 classifications from the camera
    classifications = await classifier.get_classifications_from_camera(
        "my-camera", count=3
    )

    for c in classifications:
        print(f"{c.class_name}: {c.confidence:.2f}")

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
    logger := logging.NewLogger("classify")

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

    classifier, err := vision.FromProvider(machine, "my-classifier")
    if err != nil {
        logger.Fatal(err)
    }

    // Get top 3 classifications from the camera
    classifications, err := classifier.ClassificationsFromCamera(
        ctx, "my-camera", 3, nil,
    )
    if err != nil {
        logger.Fatal(err)
    }

    for _, c := range classifications {
        fmt.Printf("%s: %.2f\n", c.Label(), c.Score())
    }
}
```

{{% /tab %}}
{{< /tabs >}}

### 2. Get classifications from an existing image

If you have an image from a previous capture or a file, classify it directly.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.camera import Camera
from viam.services.vision import VisionClient

camera = Camera.from_robot(robot, "my-camera")
classifier = VisionClient.from_robot(robot, "my-classifier")

# Capture images from the camera
images, _ = await camera.get_images()

# Classify the first image
classifications = await classifier.get_classifications(images[0], count=5)

for c in classifications:
    print(f"{c.class_name}: {c.confidence:.2f}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
cam, err := camera.FromProvider(machine, "my-camera")
if err != nil {
    logger.Fatal(err)
}

classifier, err := vision.FromProvider(machine, "my-classifier")
if err != nil {
    logger.Fatal(err)
}

images, _, err := cam.Images(ctx, nil, nil)
if err != nil {
    logger.Fatal(err)
}
img, err := images[0].Image(ctx)
if err != nil {
    logger.Fatal(err)
}

classifications, err := classifier.Classifications(ctx, img, 5, nil)
if err != nil {
    logger.Fatal(err)
}

for _, c := range classifications {
    fmt.Printf("%s: %.2f\n", c.Label(), c.Score())
}
```

{{% /tab %}}
{{< /tabs >}}

### 3. Make decisions based on classification

Classification is most useful when it drives application logic. Use the top classification to branch your program's behavior.

{{< tabs >}}
{{% tab name="Python" %}}

```python
classifications = await classifier.get_classifications_from_camera(
    "my-camera", count=1
)

if not classifications:
    print("No classification result")
elif classifications[0].confidence < 0.5:
    print(f"Uncertain: {classifications[0].class_name} "
          f"({classifications[0].confidence:.2f})")
else:
    label = classifications[0].class_name
    confidence = classifications[0].confidence
    print(f"Classified as: {label} ({confidence:.2f})")

    if label == "defective":
        print("Triggering rejection mechanism")
        # Add your action here
    elif label == "good":
        print("Part passes inspection")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
classifications, err := classifier.ClassificationsFromCamera(
    ctx, "my-camera", 1, nil,
)
if err != nil {
    logger.Fatal(err)
}

if len(classifications) == 0 {
    fmt.Println("No classification result")
} else if classifications[0].Score() < 0.5 {
    fmt.Printf("Uncertain: %s (%.2f)\n",
        classifications[0].Label(), classifications[0].Score())
} else {
    label := classifications[0].Label()
    confidence := classifications[0].Score()
    fmt.Printf("Classified as: %s (%.2f)\n", label, confidence)

    switch label {
    case "defective":
        fmt.Println("Triggering rejection mechanism")
        // Add your action here
    case "good":
        fmt.Println("Part passes inspection")
    }
}
```

{{% /tab %}}
{{< /tabs >}}

### 4. Monitor classifications continuously

Run classifications in a loop to monitor a scene over time. Track when the classification changes.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
import time

classifier = VisionClient.from_robot(robot, "my-classifier")
previous_label = ""

while True:
    classifications = await classifier.get_classifications_from_camera(
        "my-camera", count=1
    )

    if classifications and classifications[0].confidence >= 0.6:
        current_label = classifications[0].class_name
        confidence = classifications[0].confidence

        if current_label != previous_label:
            print(f"Scene changed: {previous_label or 'unknown'} "
                  f"-> {current_label} ({confidence:.2f})")
            previous_label = current_label
    else:
        if previous_label:
            print(f"Scene uncertain (was: {previous_label})")

    await asyncio.sleep(0.5)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
classifier, err := vision.FromProvider(machine, "my-classifier")
if err != nil {
    logger.Fatal(err)
}

previousLabel := ""

for {
    classifications, err := classifier.ClassificationsFromCamera(
        ctx, "my-camera", 1, nil,
    )
    if err != nil {
        logger.Error(err)
        time.Sleep(time.Second)
        continue
    }

    if len(classifications) > 0 && classifications[0].Score() >= 0.6 {
        currentLabel := classifications[0].Label()
        confidence := classifications[0].Score()

        if currentLabel != previousLabel {
            if previousLabel == "" {
                fmt.Printf("Scene changed: unknown -> %s (%.2f)\n",
                    currentLabel, confidence)
            } else {
                fmt.Printf("Scene changed: %s -> %s (%.2f)\n",
                    previousLabel, currentLabel, confidence)
            }
            previousLabel = currentLabel
        }
    } else if previousLabel != "" {
        fmt.Printf("Scene uncertain (was: %s)\n", previousLabel)
    }

    time.Sleep(500 * time.Millisecond)
}
```

{{% /tab %}}
{{< /tabs >}}

### 5. Use the transform camera to overlay classifications

You can add a `transform` camera that overlays classification results directly on the camera feed. This is useful for debugging and monitoring without writing code.

Add a transform camera to your configuration:

```json
{
  "name": "classified-feed",
  "api": "rdk:component:camera",
  "model": "transform",
  "attributes": {
    "source": "my-camera",
    "pipeline": [
      {
        "type": "classifications",
        "attributes": {
          "classifier_name": "my-classifier",
          "confidence_threshold": 0.5,
          "max_classifications": 3
        }
      }
    ]
  }
}
```

After saving, view the `classified-feed` camera in the CONTROL tab. You will see classification labels overlaid on the camera image.

{{< alert title="Tip" color="tip" >}}
If you need the image and its classifications together in one call, use [`CaptureAllFromCamera`](/reference/apis/services/vision/#captureallfromcamera). This is more efficient than separate calls and ensures the classifications correspond exactly to the returned image. See [Detect objects, step 7](/vision/detect/#7-get-everything-in-one-call-with-captureallfromcamera) for a full example.
{{< /alert >}}

## Try it

1. Run the classification script from step 1. Point the camera at different scenes and observe how the top label changes.
2. Increase the `count` parameter to 5 or 10 and observe how confidence distributes across labels.
3. Implement the decision logic from step 3 with labels relevant to your model.
4. Set up the transform camera from step 5 and watch classifications update in real time from the CONTROL tab.

## Troubleshooting

{{< expand "No classifications returned" >}}

- Verify the vision service is running and the ML model service loaded successfully. Check the `viam-server` logs for errors.
- Ensure the `count` parameter is at least 1. A `count` of 0 returns no results.
- Some vision services configured for detection do not support classification. Check that your model was trained for classification.

{{< /expand >}}

{{< expand "All classifications have very low confidence" >}}

- The model may not have been trained on the type of image you are showing it. A model trained on close-up product photos will perform poorly on wide-angle room views.
- Lighting and image quality affect classification confidence. Test under conditions similar to the training data.
- If all classes show roughly equal confidence (for example, five classes each at ~0.2), the model is essentially guessing. The input image likely does not match anything in the training set.

{{< /expand >}}

{{< expand "Classification is inconsistent between frames" >}}

- Small changes in lighting, angle, or camera noise can shift classification results. If you need stable results, average classifications over several frames or require a minimum confidence threshold before acting on a result.
- The monitoring loop in step 4 already handles this by only reacting when the top label changes and exceeds the confidence threshold.

{{< /expand >}}

{{< expand "Transform camera shows no overlay" >}}

- Verify the `classifier_name` in the transform camera configuration matches the name of your vision service exactly.
- Check that the `source` camera name is correct.
- Try lowering the `confidence_threshold` in the transform configuration.

{{< /expand >}}

## What's next

- [Detect objects](/vision/detect/): get per-object bounding boxes instead of whole-image labels.
- [Track objects across frames](/vision/track/): maintain object identities across consecutive frames.
- [Alert on detections](/vision/alert-on-detections/): send email or webhook notifications when specific objects or labels are detected.
