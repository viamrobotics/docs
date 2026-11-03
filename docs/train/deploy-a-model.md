---
linkTitle: "Deploy a model"
title: "Deploy a model to a machine"
weight: 30
layout: "docs"
type: "docs"
description: "Add a trained model and the resource that runs it to your machine's configuration, from the model's page or the CONFIGURE tab."
capabilities: ["ml-models", "vision-service"]
diataxis: how-to
---

Configure your machine to load a trained model from the registry.
What runs the model depends on its framework.

{{< alert title="Tip" color="tip" >}}
For the full guide to configuring vision services and cloud inference, see [Configure computer vision](/vision/configure/).
{{< /alert >}}

## What runs the model {#what-runs-the-model}

A model's framework is the machine learning library it was built with, and it sets the format of the model's files.
TFLite, TensorFlow, PyTorch and ONNX are widely used formats, so a model trained in one of them anywhere, not only on Viam, can run on a Viam machine.
**Registry** is Viam's own, and it isn't a file format: it means a specific module reads the model's files and runs the model.

To run a model, a machine needs software that can read its format:

| Framework      | Runs on the machine in                                                                                                                                                 | Hardware                                             |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **TFLite**     | The [`tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu) ML model service                                                                                       | linux/amd64, linux/arm64, darwin/arm64, darwin/amd64 |
| **TensorFlow** | The [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu) or [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) ML model service | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64   |
| **PyTorch**    | The [`torch-cpu`](https://app.viam.com/module/viam/torch-cpu) or `triton` ML model service                                                                             | Nvidia GPU, linux/arm64, darwin/arm64                |
| **ONNX**       | The [`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu) or `triton` ML model service                                                                               | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64   |
| **Registry**   | The module resource the model names                                                                                                                                    | Whatever the module supports                         |

The first four load the model into an ML model service, which runs it but doesn't interpret its output.
For a classification or detection model, a vision service sits on top of the ML model service and turns that output into labels and boxes.
The steps for the vision service on this page apply only to those models.

A **Registry** model doesn't use an ML model service unless its module provides one.
Instead, the model names the module resource that runs it, such as a module that drives an arm with a robot policy, and deploying adds that resource with the model.
The training script sets the module when it's uploaded to the registry.

## Deploy from the model details page

The fastest way to deploy a model is from the model's page in the Viam app:

1. Navigate to **Models** and click the model you want to deploy.
1. Click **Deploy** in the model header to open the deploy dialog, which walks you through a few steps.
1. Select a model version, location, machine, and machine part, then click **Continue**.
1. Name the resource that runs the model, then click **Continue**.
   For most frameworks, this is the ML model service.
   For a **Registry** model, the dialog has one name for each module resource the model names, and the next click deploys them.
1. For a model that runs in an ML model service, the dialog offers a vision service next.
   **Include Vision service** is on by default for classification and detection models, and uses an existing camera on your machine.
   Turn it off for any other model.
1. Click **Deploy** to add the resources to the machine's configuration.

After deploying, check the resource on the machine's **CONTROL** tab.

<!-- When "Run a robot policy" (DOCS-5063 N3) exists, link it here for Registry robot policy models. -->

## Deploy from the machine's configure tab

These steps work for any model that runs in an ML model service: a TFLite, TensorFlow, PyTorch or ONNX model of any task type.
Step 2, the vision service, applies only to classification and detection models.
For a **Registry** model, such as a robot policy, see [Deploy a Registry model manually](#deploy-a-registry-model-manually).

### 1. Add the ML model service

The ML model service loads the model.
Pick the service that matches your trained model's framework and your machine's hardware, from the table in [What runs the model](#what-runs-the-model).

1. Navigate to your machine's **CONFIGURE** tab.
2. Click **+** and select **Blocks**.
3. Search for the ML model service matching your framework (for example,
   `tflite_cpu`) and select the matching result.
4. Click the block, then click **Add to machine**.
5. Enter a name for the service (for example, `my-ml-model`) and click
   **Add to machine**. The supporting module is installed automatically.
6. In the service configuration card, under **Deployment**, leave
   **Deploy model on machine** selected.
7. Click **Select model**. In the dialog, browse **My models** or
   **Registry** to find your trained model.
8. Select the model, choose a version (or leave it on **Latest**), and click
   **Choose**. The model path and label path are set automatically.
9. Click **Save** in the top right.

### 2. Add the vision service

Skip this step if your model isn't a classification or detection model.

1. Click **+** and select **Blocks**.
2. Search for `mlmodel` and find the **mlmodel** block (type: **VISION**,
   built-in).
3. Click the block, then click **Add to machine**.
4. Enter a name for the service (for example, `my-detector`) and click
   **Add to machine**.
5. In the **ML Model** dropdown, select the ML model service you added in
   step 1 (for example, `my-ml-model`).
6. Optionally, select a **Default Camera** and adjust the
   **Minimum confidence threshold** (default: 0.5).
7. Click **Save**.

### 3. Verify

For a classification or detection model:

1. In the vision service's configuration card, click **Test**.
2. Select a camera to run the model against.
3. You should see live classifications or detections overlaid on the camera
   feed.

For any other model, call the ML model service's `metadata` from code to check that it loaded the model.
See [Use the model in code](#other-models-in-an-ml-model-service).

### Deploy a Registry model manually

A **Registry** model runs in a module resource instead of an ML model service, so the steps above don't apply.
[Deploying from the model details page](#deploy-from-the-model-details-page) is simpler, because the deploy dialog adds the module, the resource and the model together.
To configure it by hand instead:

1. On the machine's **CONFIGURE** tab, click **+** and add the module resource the model names.
   The training script set this resource when it was uploaded to the registry.
   It can be a component or a service of any API.
2. Switch to **JSON** mode and add the model to `packages`.
3. In the resource's attributes, set `model_path` to the package directory, `${packages.ml_model.<package-name>}`.
   This is what the deploy dialog writes.
   The module's documentation in the registry lists any other attributes the resource needs.
4. Click **Save**.

```json
{
  "packages": [
    {
      "name": "my-policy",
      "package": "<org-id>/my-policy",
      "version": "latest",
      "type": "ml_model"
    }
  ],
  "services": [
    {
      "name": "my-policy-runner",
      "api": "<resource-api>",
      "model": "<namespace>:<module-name>:<model-name>",
      "attributes": {
        "model_path": "${packages.ml_model.my-policy}"
      }
    }
  ]
}
```

If the module resource is a component, it goes under `components` instead of `services`.

## Use the model in code

How you call a deployed model depends on what runs it.

### Classification and detection models

A classification or detection model answers through the vision service:

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

### Robot policies and other Registry models

A **Registry** model, such as a robot policy, runs in the module resource it names.
It doesn't answer through a vision service, and it uses an ML model service only if its module provides one.
Call the module resource's API, which depends on the module.
Check the module's documentation in the registry for which API it implements and how to run the policy.

<!-- When "Run a robot policy" (DOCS-5063 N3) exists, link it here. -->

### Other models in an ML model service

A model with the **Other** task type that runs in an ML model service has no vision service.
Call the ML model service directly: `metadata` returns the model's input and output tensors, and `infer` runs the model on input tensors you pass.

```python
from viam.services.mlmodel import MLModelClient

# Get the ML model service (assumes you have a robot connection)
mlmodel = MLModelClient.from_robot(robot, "my-model")

metadata = await mlmodel.metadata()
for tensor in metadata.input_info:
    print(f"  input {tensor.name}: {tensor.data_type} {list(tensor.shape)}")

# my_input is a NumPy array that matches the input tensor's shape and type
outputs = await mlmodel.infer({metadata.input_info[0].name: my_input})
```

See the [ML model service API](/reference/apis/services/ml/) for each method.

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
- [Detect objects (2D)](/vision/object-detection/detect/) -- use your
  object detection model to find and locate objects in camera images.
- [Classify images](/vision/classify/) -- use your
  classification model to categorize images from your machine's camera.
