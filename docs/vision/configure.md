---
linkTitle: "Configure a vision pipeline"
title: "Configure a vision pipeline"
weight: 10
layout: "docs"
type: "docs"
modulescript: true
description: "Wire up an ML model service and a vision service so your machine's camera can produce detections, classifications, or 3D point cloud objects."
date: "2026-04-14"
aliases:
  - /build/vision-detection/add-computer-vision/
  - /vision-detection/add-computer-vision/
---

You have a camera on your machine and a trained ML model. This how-to wires them up: an ML model service loads the model and a vision service turns the model's output into detections, classifications, or 3D point cloud objects.

Downstream how-tos ([detect](/vision/detect/), [classify](/vision/classify/), [track](/vision/track/), [measure depth](/vision/measure-depth/)) assume the pipeline described here is running.

## What you are configuring, in one paragraph

Viam splits ML inference into two services. The **ML model service** loads the model file and runs tensors through it. The **vision service** turns those tensors into structured detections and classifications and ties them to a specific camera. Your application code talks to the vision service; the ML model service is a building block underneath. For the longer explanation and when the split matters, see [How the vision service works](/vision/how-it-works/).

## 1. Add an ML model service

The ML model service matches your model file's framework. For most tasks, `tflite_cpu` is the right starting point.

1. Navigate to the **CONFIGURE** tab of your machine in the Viam app.
2. Click the **+** icon next to your machine part and select **Configuration block**.
3. In the search field, type `tflite_cpu` (or the service matching your model format) and select the matching result. For other frameworks, see the [framework table](/vision/deploy-from-registry/#model-framework-support).
4. Click **Add component**, name the service `my-ml-model`, and click **Add component** again to confirm.

## 2. Configure the ML model service

Point the service at your model file.

**Registry model:**

```json
{
  "name": "my-ml-model",
  "api": "rdk:service:mlmodel",
  "model": "tflite_cpu",
  "attributes": {
    "model_path": "${packages.my-model}/model.tflite",
    "label_path": "${packages.my-model}/labels.txt"
  }
}
```

`${packages.my-model}` resolves to the directory where the [registry](https://app.viam.com/registry) package was downloaded. Replace `my-model` with the name of your deployed model package.

**Local model file:**

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

`label_path` is optional but recommended: it maps numeric class IDs (the raw output of the model) to human-readable names.

For more on the deployment flow, see [Deploy a model from the registry](/vision/deploy-from-registry/) or [Deploy a custom ML model](/vision/deploy-custom-model/).

## 3. Add a vision service

1. Click the **+** icon and select **Configuration block**.
2. In the search field, type `vision` or `mlmodel` and select the `vision/mlmodel` result.
3. Click **Add component**, name the service `my-detector`, and click **Add component** again to confirm.

## 4. Configure the vision service

```json
{
  "name": "my-detector",
  "api": "rdk:service:vision",
  "model": "mlmodel",
  "attributes": {
    "mlmodel_name": "my-ml-model"
  }
}
```

`mlmodel_name` must match the name of the ML model service from step 1.

For the full list of `mlmodel` vision service attributes (confidence thresholds, per-label thresholds, tensor remapping, input normalization), see the [mlmodel reference](/reference/services/vision/mlmodel/). If your detections come out shifted, mirrored, or with unexpected labels, see [Tune detection quality](/vision/tune/) to find the attribute that fixes your symptom.

## 5. Save and verify

Click **Save** in the upper right. `viam-server` reconfigures in place and initializes both services.

You can check which capabilities the service registered by calling [`GetProperties`](/reference/apis/services/vision/#getproperties) from code. The response is three booleans reporting whether detections, classifications, and 3D point clouds are supported at runtime.

## 6. Verify with the control card

The fastest check is the Viam app's live overlay:

1. Go to the **CONTROL** tab.
2. Find your vision service in the component list and open it.
3. In the **Camera** dropdown, select the camera whose feed you want the vision service to run on. Detections appear as an overlay on the live camera feed and refresh automatically.

Bounding boxes or classification labels should appear on the live camera feed within a second or two. If you are using a COCO-class general-purpose model, point the camera at a person, a cup, or a keyboard.

If the camera feed appears but no detections are shown, see [Tune detection quality](/vision/tune/).

## 7. Complete configuration

With both services saved, the relevant part of your machine configuration looks like this:

```json
{
  "services": [
    {
      "name": "my-ml-model",
      "api": "rdk:service:mlmodel",
      "model": "tflite_cpu",
      "attributes": {
        "model_path": "${packages.my-model}/model.tflite",
        "label_path": "${packages.my-model}/labels.txt"
      }
    },
    {
      "name": "my-detector",
      "api": "rdk:service:vision",
      "model": "mlmodel",
      "attributes": {
        "mlmodel_name": "my-ml-model"
      }
    }
  ]
}
```

`viam-server` resolves the dependency between the two services automatically, so order within the file does not matter.

## Try it from code

Verify end-to-end by pulling a detection from your own code.

Install the SDK if you have not already:

```bash
pip install viam-sdk
```

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
    "go.viam.com/utils/rpc"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("vision-test")

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

## Available ML model services and vision models

### Available ML model services

{{< resources_svc api="rdk:service:mlmodel" type="ML model" >}}

### Available vision services

{{% expand "Click to see available vision services" %}}

{{< resources_svc api="rdk:service:vision" type="vision" >}}

{{% /expand %}}

### Public machine learning models

{{< mlmodels >}}

## What's next

- [Deploy a model from the registry](/vision/deploy-from-registry/): expand on model-picking guidance
- [Detect objects](/vision/detect/): use detection results in code
- [Classify images](/vision/classify/): use classification results in code
- [Tune detection quality](/vision/tune/): fix mis-configured or miscalibrated detectors
- [Run batch inference](/vision/batch-inference/): run a model against stored images instead of live frames
- [Retrain when accuracy drops](/vision/retrain/): close the loop when your model drifts
