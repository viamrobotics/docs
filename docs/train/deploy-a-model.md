---
linkTitle: "Deploy a model"
title: "Deploy a model to a machine"
weight: 25
layout: "docs"
type: "docs"
description: "Add an ML model service and vision service to run a trained model on your machine."
---

Configure your machine to load a trained model from the registry and apply it
to live camera frames. You need an ML model service to load the model and a
vision service to run it against camera input.

{{< alert title="Tip" color="tip" >}}
For the full guide to configuring vision services and cloud inference, see [Configure computer vision](/vision/configure/).
{{< /alert >}}

## 1. Add the ML model service

1. Navigate to your machine's **CONFIGURE** tab.
2. Click **+** and select **Configuration block**.
3. Search for `tflite` and find the **tflite_cpu** block (by **viam**,
   badge: **MLMODEL**).
4. Click the block, then click **Add component**.
5. Enter a name for the service (for example, `my-ml-model`) and click
   **Add component**. The supporting `viam:tflite_cpu` module is installed
   automatically.
6. In the service configuration card, under **Deployment**, leave
   **Deploy model on machine** selected.
7. Click **Select model**. In the dialog, browse **My models** or
   **Registry** to find your trained model.
8. Select the model, choose a version (or leave it on **Latest**), and click
   **Choose**. The model path and label path are set automatically.
9. Click **Save** in the top right.

## 2. Add the vision service

1. Click **+** and select **Configuration block**.
2. Search for `mlmodel` and find the **mlmodel** block (type: **VISION**,
   built-in).
3. Click the block, then click **Add component**.
4. Enter a name for the service (for example, `my-detector`) and click
   **Add component**.
5. In the **ML Model** dropdown, select the ML model service you added in
   step 1 (for example, `my-ml-model`).
6. Optionally, select a **Default Camera** and adjust the
   **Minimum confidence threshold** (default: 0.5).
7. Click **Save**.

## 3. Verify

1. Navigate to the **CONTROL** tab.
2. Find your vision service and click **Test**.
3. Select a camera to run the model against.
4. You should see live classifications or detections overlaid on the camera
   feed.

## Use the model in code

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.services.vision import VisionClient

# Get the vision service (assumes you have a robot connection)
vision = VisionClient.from_robot(robot, "my-detector")

# For classification
classifications = await vision.get_classifications(
    image=my_image,
    count=5,
)
for c in classifications:
    print(f"  {c.class_name}: {c.confidence:.2f}")

# For object detection
detections = await vision.get_detections(image=my_image)
for d in detections:
    print(f"  {d.class_name}: {d.confidence:.2f} "
          f"at ({d.x_min}, {d.y_min}) to ({d.x_max}, {d.y_max})")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import "go.viam.com/rdk/services/vision"

// Get the vision service (assumes you have a robot connection)
visionSvc, err := vision.FromProvider(robot, "my-detector")
if err != nil {
    logger.Fatal(err)
}

// For classification
classifications, err := visionSvc.Classifications(ctx, myImage, 5, nil)
if err != nil {
    logger.Fatal(err)
}
for _, c := range classifications {
    fmt.Printf("  %s: %.2f\n", c.Label(), c.Score())
}

// For object detection
detections, err := visionSvc.Detections(ctx, myImage, nil)
if err != nil {
    logger.Fatal(err)
}
for _, d := range detections {
    box := d.BoundingBox()
    fmt.Printf("  %s: %.2f at (%d, %d) to (%d, %d)\n",
        d.Label(), d.Score(),
        box.Min.X, box.Min.Y, box.Max.X, box.Max.Y)
}
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Model not appearing on the machine" >}}

- **Check the ML model service configuration.** Open the service card in the
  **CONFIGURE** tab and verify a model is selected. If you see the
  **Select model** button, no model has been chosen yet.
- **Restart viam-server.** In some cases, the machine may need to restart to
  pick up a new model version.
- **Check machine connectivity.** The machine must be online and connected to
  the cloud to download model updates.

{{< /expand >}}

{{< expand "Vision service returns no results" >}}

- **Check the ML Model dropdown.** The vision service's **ML Model** dropdown
  must reference your ML model service by name. If it shows
  **No models available**, add an ML model service first.
- **Check the camera.** Verify that the camera is working in the **CONTROL** tab
  before testing the vision service.
- **Lower the confidence threshold.** The model may be producing results below
  your current threshold. Adjust the **Minimum confidence threshold** slider.

{{< /expand >}}

## What's next

- [Add computer vision](/vision/configure/) -- the full guide to configuring
  vision services and cloud inference.
- [Detect objects (2D)](/vision/detect/) -- use your
  object detection model to find and locate objects in camera images.
- [Classify images](/vision/classify/) -- use your
  classification model to categorize images from your machine's camera.
