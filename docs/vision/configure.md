---
linkTitle: "Configure a vision pipeline"
title: "Configure a vision pipeline"
weight: 10
layout: "docs"
type: "docs"
description: "Wire up an ML model service and a vision service so your machine's camera can produce detections, classifications, or 3D point cloud objects."
capabilities: ["vision-service", "ml-models"]
diataxis: how-to
date: "2026-04-14"
aliases:
  - /vision/deploy-and-maintain/
  - /vision/deploy-and-maintain/available-models/
  - /vision/deploy-and-maintain/deploy-from-registry/
  - /vision/deploy-from-registry/
  - /vision/models/
  - /build/vision-detection/add-computer-vision/
  - /vision-detection/add-computer-vision/
---

You have a camera on your machine, and you have an ML model. The model could have come from the [registry](https://app.viam.com/registry), from the [Train and deploy ML models section](/train/) through [built-in training](/train/train-a-model/) or a [custom training script](/train/custom-training-scripts/), or from elsewhere entirely: GitHub, Hugging Face, or your own training run outside Viam. This how-to wires the pieces together: an ML model service loads the model, and a vision service turns the model's output into detections, classifications, or 3D point cloud objects.

Downstream how-tos ([detect](/vision/object-detection/detect/), [classify](/vision/classify/), [track](/vision/object-detection/track/), [measure depth](/vision/3d-vision/measure-depth/)) assume the pipeline described here is running.

## What you are configuring, in one paragraph

Viam splits ML inference into two services. The **ML model service** loads the model file and runs tensors through it. The **vision service** turns those tensors into structured detections and classifications and ties them to a specific camera. Your application code talks to the vision service; the ML model service is a building block underneath.

```text
    Camera ─── image ───► Vision service ─── tensor ───► ML model service
                               │                             │
                               ▼                             ▼
                       Detections,                      Raw output
                       classifications,                 tensor
                       point cloud objects    ◄──────────────┘
                       (what your code uses)
```

Three resources (camera, vision service, ML model service) plus the model file itself. The steps below add each piece. For the longer explanation and when the split matters, see [How a vision service works](/vision/how-it-works/).

## 1. Add an ML model service

The ML model service matches your model file's framework. For most tasks, `tflite_cpu` is the right starting point: it runs on almost any CPU and keeps hardware costs down. When you need GPU acceleration (larger models, higher frame rates, Nvidia Jetson hardware), use [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) instead. [What runs the model](/train/deploy-a-model/#what-runs-the-model) lists which services support which frameworks and hardware.

1. Navigate to the **CONFIGURE** tab of your machine in the Viam app.
2. Click the **+** icon next to your machine part and select **Blocks**.
3. In the search field, type `tflite_cpu` (or the service matching your model format) and select the matching result.
4. Click **Add to machine**, name the service `my-ml-model`, and click **Add to machine** again to confirm.

## 2. Configure the ML model service

Point the service at your model file. The Builder flow populates the config for you; the JSON tab shows what you end up with (or what to write manually, for example for a local model file).

Two things matter here:

- **The model file itself** (`model_path` in the JSON): the weights the service loads.
- **The label file** (`label_path`): a plain text file that maps the numeric class IDs the model outputs to human-readable names. A detector that outputs class `3` doesn't mean anything on its own; the label file translates that to `dog` or whatever class 3 was at training time. Registry models ship with this file; for local models you provide your own.

Both paths resolve to whatever you give them: a package reference like `${packages.ml_model.my-model}/labels.txt` for registry models, or an absolute path on the machine for local files. You can inspect a registry model's bundled `labels.txt` by looking in `${packages.ml_model.my-model}/` after first deploy, or by opening the model's detail view on [app.viam.com/models](https://app.viam.com/models).

{{< tabs >}}
{{% tab name="Builder" %}}

1. Click your new ML model service card on the **CONFIGURE** tab.
2. Click **Select model**. A dialog titled "Select a model" opens.
3. Use the **My models** and **Registry** tabs to switch between models in your organization and public models in the [Viam Registry](https://app.viam.com/registry). Use the search field and the **Task type**, **Framework**, and **Visibility** filters to narrow the list.
4. Click a model card to open its details view. Pick a **Version** from the dropdown: **Latest** (auto-updates when a newer version is published) or a specific timestamp version (recommended for production). See [Choose a model version](/train/deploy-a-model/#choose-a-model-version).
5. Click **Choose**. The dialog closes and the service panel now shows the selected model as a pill with its version and author.

Behind the scenes the builder adds a `packages` entry for the model and sets `model_path` and `label_path` on the service attributes to point into the package.

{{% /tab %}}
{{% tab name="JSON — registry model" %}}

```json
{
  "packages": [
    {
      "name": "my-model",
      "package": "<org-id>/my-model",
      "version": "latest",
      "type": "ml_model"
    }
  ],
  "services": [
    {
      "name": "my-ml-model",
      "api": "rdk:service:mlmodel",
      "model": "tflite_cpu",
      "attributes": {
        "package_reference": "<org-id>/my-model",
        "model_path": "${packages.ml_model.my-model}/my-model.tflite",
        "label_path": "${packages.ml_model.my-model}/labels.txt"
      }
    }
  ]
}
```

`${packages.ml_model.my-model}` resolves to the directory where the [registry](https://app.viam.com/registry) package was downloaded. Replace `my-model` with the name of your deployed model package and `<org-id>` with the UUID of the organization that owns it. `package_reference` is the same `<org-id>/my-model` identifier. The file name inside the placeholder (`my-model.tflite`, `labels.txt`) matches the actual file names inside the package; the Builder flow in the previous tab fills these in automatically based on what the registry model contains.

{{% /tab %}}
{{% tab name="JSON — local model file" %}}

```json
{
  "name": "my-ml-model",
  "api": "rdk:service:mlmodel",
  "model": "tflite_cpu",
  "attributes": {
    "model_path": "/path/to/your/model.tflite",
    "label_path": "/path/to/your/labels.txt"
  }
}
```

For local models, `label_path` is optional but recommended. The file is plain text, one label per line, in class-ID order (line 0 is class 0, line 1 is class 1, and so on).

{{% /tab %}}
{{< /tabs >}}

For more on the deployment flow, see [Deploy a model to a machine](/train/deploy-a-model/). To update a deployed model or roll it out across a fleet, see [Update or roll back a deployed model](/train/deploy-a-model/#update-a-deployed-model) and [Deploy ML models across your fleet](/fleet/deploy-ml-models/).

## 3. Check the model's tensors {#tensor-requirements}

The `mlmodel` vision service expects specific tensor conventions from the model it wraps.
If the model does not match, the vision service fails to come up as a detector or classifier, or it comes up but produces garbled output.
Models trained on Viam already use the expected names, so skip this step for them.
For a registry model, the module's README lists its tensor requirements.

**Detector models must expose:**

- Input tensor named `image` with shape `[batch, height, width, channels]`.
  The service feeds one image at a time.
- Output tensors named `location`, `category`, and `score`.
  Each is per-detection.

**Classifier models must expose:**

- Input tensor named `image` with the same shape.
- Output tensor named `probability`, one value per class.

**Preprocessing assumptions:**

- Input pixel values are uint8 in `[0, 255]` by default.
- Input channel order is RGB by default.
- Bounding boxes are `[xmin, ymin, xmax, ymax]` normalized to `[0, 1]`.

### Convert the model or bridge the difference {#convert-or-bridge}

If your model disagrees with any of these conventions, you generally do not have to retrain or modify it.
Set vision service attributes (in [step 5](#5-configure-the-vision-service)) to bridge the gap:

- **Non-standard tensor names**: `remap_input_names` and `remap_output_names`.
  See [Tensor names do not match](/vision/object-detection/tune/#tensor-names-do-not-match).
- **Non-standard preprocessing**, such as `[-1, 1]` or `[0, 1]` normalization or BGR channel order: `input_image_mean_value`, `input_image_std_dev`, and `input_image_bgr`.
  See [Wrong labels or every label fires](/vision/object-detection/tune/#wrong-labels-or-every-label-fires).
- **Non-standard bounding box coordinate order**: `xmin_ymin_xmax_ymax_order`.
  See [Bounding boxes appear shifted or mirrored](/vision/object-detection/tune/#bounding-boxes-appear-shifted-or-mirrored).
- **Class-specific confidence tuning**: `label_confidences`.

The [`mlmodel` reference](/reference/services/vision/mlmodel/) lists every attribute.

Convert the model itself only when its format is unsupported (for example, exporting from Keras HDF5 to TFLite) or when the tensor types are incompatible with the chosen ML model service.
[Upload a model](/train/upload-a-model/#check-the-format) lists the supported formats.

## 4. Add a vision service

If you deployed the model from its page with **Include Vision service** on, the deployment already added a `vision/mlmodel` service. Skip to [step 6](#6-save) after checking that its `mlmodel_name` and `camera_name` match your resources.

1. Click the **+** icon and select **Blocks**.
2. In the search field, type `vision` or `mlmodel` and select the `vision/mlmodel` result.
3. Click **Add to machine**, name the service `my-detector`, and click **Add to machine** again to confirm.

## 5. Configure the vision service

```json
{
  "name": "my-detector",
  "api": "rdk:service:vision",
  "model": "mlmodel",
  "attributes": {
    "mlmodel_name": "my-ml-model",
    "camera_name": "my-camera"
  }
}
```

`mlmodel_name` must match the name of the ML model service from step 1. `camera_name` is the default camera used by `GetDetectionsFromCamera`, `GetClassificationsFromCamera`, and `GetObjectPointClouds` when no camera name is passed in the call.

For the full list of `mlmodel` vision service attributes (confidence thresholds, per-label thresholds, tensor remapping, input normalization), see the [mlmodel reference](/reference/services/vision/mlmodel/). If your detections come out shifted, mirrored, or with unexpected labels, see [Tune detection quality](/vision/object-detection/tune/) to find the attribute that fixes your symptom.

## 6. Save

Click **Save** in the upper right. `viam-server` reconfigures in place and initializes both services.

## 7. Verify with the control card

The fastest check is the Viam app's live overlay:

1. Go to the **CONTROL** tab.
2. Find your vision service in the component list and open it.
3. In the **Camera** dropdown, select the camera whose feed you want the vision service to run on. Detections appear as an overlay on the live camera feed.
4. The overlay refreshes automatically once per second. To adjust, use the dropdown next to the Camera selector (**Live**, **Refresh every second**, **Refresh every 5 seconds**, or **Manual refresh**).

Bounding boxes or classification labels should appear within a second or two. If you are using a COCO-class general-purpose model, point the camera at a person, a cup, or a keyboard.

If the camera feed appears but no detections are shown:

- Confirm the vision service registered in the expected role by calling [`GetProperties`](/reference/apis/services/vision/#getproperties), as described below. A detection model that registered as a classifier (or a classifier that registered as a detector) returns empty lists.
- Lower `default_minimum_confidence` on the vision service and try again. The model may be producing detections below the default confidence threshold.
- Check `viam-server` logs for startup errors mentioning tensor names or label files. See [Check the model's tensors](#tensor-requirements).

If results look wrong (shifted boxes, wrong labels, or zero detections), see [Tune detection quality](/vision/object-detection/tune/).

From code, you can confirm which roles the vision service registered by calling [`GetProperties`](/reference/apis/services/vision/#getproperties). The response includes three booleans reporting whether detections, classifications, and 3D point clouds are supported at runtime. If a default camera is configured, the response also includes its name.

## 8. Complete configuration

With both services saved, a minimal end-to-end configuration (camera + ML model service + vision service) looks like this:

```json
{
  "components": [
    {
      "name": "my-camera",
      "api": "rdk:component:camera",
      "model": "webcam",
      "attributes": {}
    }
  ],
  "packages": [
    {
      "name": "my-model",
      "package": "<org-id>/my-model",
      "version": "latest",
      "type": "ml_model"
    }
  ],
  "services": [
    {
      "name": "my-ml-model",
      "api": "rdk:service:mlmodel",
      "model": "tflite_cpu",
      "attributes": {
        "package_reference": "<org-id>/my-model",
        "model_path": "${packages.ml_model.my-model}/my-model.tflite",
        "label_path": "${packages.ml_model.my-model}/labels.txt"
      }
    },
    {
      "name": "my-detector",
      "api": "rdk:service:vision",
      "model": "mlmodel",
      "attributes": {
        "mlmodel_name": "my-ml-model",
        "camera_name": "my-camera"
      }
    }
  ]
}
```

`viam-server` resolves the dependencies between the camera, ML model service, and vision service automatically, so order within the file does not matter.

## Try it from code

Verify end-to-end by pulling a detection from your own code.

Install the SDK if you have not already:

Install the Viam Python SDK in a virtual environment by following [Install the Python SDK](/reference/sdks/python/python-venv/).

{{< tabs >}}
{{% tab name="Python" %}}

Save as `vision_test.py`:

```python
import asyncio

from viam.robot.client import RobotClient
from viam.services.vision import VisionClient


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID",
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    detector = VisionClient.from_robot(robot, "my-detector")
    detections = await detector.get_detections_from_camera("my-camera")

    print(f"Found {len(detections)} detections:")
    for d in detections:
        print(f"  {d.class_name}: {d.confidence:.2f}")

    await robot.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python vision_test.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir vision-test && cd vision-test
go mod init vision-test
go get go.viam.com/rdk
```

Save as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/services/vision"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("vision-test")

    machine, err := client.New(ctx, "YOUR-MACHINE-ADDRESS", logger,
        client.WithDialOptions(client.WithEntityCredentials(
            "YOUR-API-KEY-ID",
            client.Credentials{
                Type:    client.CredentialsTypeAPIKey,
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

    fmt.Printf("Found %d detections:\n", len(detections))
    for _, d := range detections {
        fmt.Printf("  %s: %.2f\n", d.Label(), d.Score())
    }
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

You should see a list of detected objects with their confidence scores. If the list is empty, point the camera at something your model was trained to recognize.

Get the placeholder values from the Viam app:

1. Open your machine's **CONNECT** tab.
2. Select **SDK code sample**.
3. Click the **Include API key** switch. The snippet on the page regenerates with your machine's real API key, API key ID, and machine address in place of the `<API-KEY>`, `<API-KEY-ID>`, and `<MACHINE-ADDRESS>` placeholders. Click the copy icon on the snippet to copy the whole thing.
4. To view or copy API keys separately, open the **API keys** sidebar item on the same tab.

## What's next

- [Detect objects](/vision/object-detection/detect/): use detection results in code
- [Classify images](/vision/classify/): use classification results in code
- [Tune detection quality](/vision/object-detection/tune/): fix mis-configured or miscalibrated detectors
- [Update or roll back a deployed model](/train/deploy-a-model/#update-a-deployed-model): move a machine to a new model version without changing the vision service
- [Run batch inference](/train/batch-inference/): run a model against stored images instead of live frames
- [Retrain when accuracy drops](/train/retrain-a-model/): close the loop when your model drifts
