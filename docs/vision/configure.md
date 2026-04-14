---
linkTitle: "Configure a vision pipeline"
title: "Configure a vision pipeline"
weight: 10
layout: "docs"
type: "docs"
modulescript: true
description: "Deploy an ML model and configure a vision service to give your machine the ability to detect or classify objects."
date: "2025-01-30"
aliases:
  - /build/vision-detection/add-computer-vision/
  - /vision-detection/add-computer-vision/
---

You have a trained machine learning model and a camera, and you want your machine to understand what it sees.
This how-to configures both an ML model service and a vision service so that downstream how-to guides --[Detect Objects](/vision/detect/), [Classify Images](/vision/classify/), [Track Objects](/vision/track/) --have a working vision pipeline to build on.

## Concepts

### The two-service architecture

Most robotics platforms handle ML inference as a monolithic block: one configuration entry that loads a model and runs it against a camera. Viam splits this into two services for a reason.

The **ML model service** handles the mechanics of model loading: reading the file, allocating memory, preparing the inference runtime. The **vision service** handles the semantics: what does "run a detection" mean, how do you map model outputs to bounding boxes, how do you associate results with camera frames.

This separation means:

- You can update your model (retrain, swap architectures) without changing your vision service configuration.
- You can run the same model against multiple cameras by creating multiple vision services that reference the same ML model service.
- Different model formats (TFLite, ONNX, TensorFlow, PyTorch) are handled by different ML model service implementations, but the vision service API stays the same.

### Supported frameworks and hardware

Viam currently supports the following frameworks:

<!-- prettier-ignore -->
| Model Framework | ML Model Service | Hardware Support | Description |
| --------------- | --------------- | ------------------- | ----------- |
| [TensorFlow Lite](https://www.tensorflow.org/lite) | [`tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu) | linux/amd64, linux/arm64, darwin/arm64, darwin/amd64 | Quantized version of TensorFlow that has reduced compatibility for models but supports more hardware. Uploaded models must adhere to the [model requirements](https://app.viam.com/module/viam/tflite_cpu). |
| [ONNX](https://onnx.ai/) | [`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64 | Universal format that is not optimized for hardware-specific inference but runs on a wide variety of machines. |
| [TensorFlow](https://www.tensorflow.org/) | [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64 | A full framework designed for more production-ready systems. |
| [PyTorch](https://pytorch.org/) | [`torch-cpu`](https://app.viam.com/module/viam/torch-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) | Nvidia GPU, linux/arm64, darwin/arm64 | A full framework that was built primarily for research. Because of this, it is much faster to do iterative development with (the model doesn't have to be predefined) but it is not as "production ready" as TensorFlow. It is the most common framework for open-source models because it is the go-to framework for ML researchers. |

{{< alert title="Note" color="note" >}}
For some ML model services, like the [Triton ML model service](https://github.com/viamrobotics/viam-mlmodelservice-triton/) for Jetson boards, you can configure the service to use either the available CPU or a dedicated GPU.
{{< /alert >}}

Entry-level devices such as the Raspberry Pi 4 can run small ML models, such as TensorFlow Lite (TFLite).
More powerful hardware, including the Jetson Xavier or Raspberry Pi 5 with an AI HAT+, can process larger models, including TensorFlow and ONNX.
If your hardware does not support the model you want to run, see [Cloud inference](#cloud-inference).

### ML model service

The ML model service loads a model file and exposes it for inference. The most common implementation is `tflite_cpu`, which runs TensorFlow Lite models on the CPU. Other implementations support ONNX, TensorFlow SavedModel, and PyTorch.

When you deploy a model from the Viam registry, the model files are downloaded to your machine and referenced with the `${packages.model-name}` variable. You can also point directly to a local file path if you have a model file on disk.

The `tflite_cpu` implementation runs entirely on the CPU, so it works on any hardware --no GPU required. For Raspberry Pi, Jetson Nano, and other edge machines, this is the standard approach. Performance depends on the model size: a MobileNet-based detector typically runs at 5-10 frames per second on a Raspberry Pi 4.

### Vision service

The vision service connects an ML model to a camera and provides high-level APIs for detection and classification. The `mlmodel` implementation takes detections or classifications from the ML model and returns them as structured data: bounding boxes with labels and confidence scores for detections, or label-confidence pairs for classifications.

The vision service is what your code interacts with. You never call the ML model service directly from application code. This means switching from a detection model to a classification model requires only a configuration change to the ML model service, not a rewrite of your application.

The vision service also handles the image capture pipeline. When you call `GetDetectionsFromCamera`, the vision service captures a frame from the specified camera, converts it to the format expected by the model, runs inference, and returns structured results. You do not need to manage image capture and model input formatting yourself.

### Labels and label files

ML models output numeric class IDs, not human-readable names. A detection model might output class ID `3`, which means nothing to you. The **label file** maps these IDs to names: class 3 might be "dog", class 7 might be "car".

The label file is a plain text file with one label per line. The line number (zero-indexed) corresponds to the class ID. For example:

```text
background
person
bicycle
car
motorcycle
```

In this file, class ID 0 is "background", class ID 1 is "person", and so on. When you configure the ML model service with a `label_path`, detections and classifications will use these human-readable names instead of numeric IDs.

If you do not provide a label file, detections will report numeric class IDs as their labels.

### Model sources

The service works with models from various sources:

- You can [train TensorFlow or TensorFlow Lite](/train/train-a-model/) or [other model frameworks](/train/custom-training-scripts/) on data from your machines.
- You can use [ML models](https://app.viam.com/registry?type=ML+Model) from the [registry](https://app.viam.com/registry).
- You can upload externally trained models from a model file on the [**MODELS** tab](https://app.viam.com/models).
- You can use models trained outside the Viam platform whose files are on your machine.
  See the documentation for the ML model service you're using (pick one that supports your model framework) for instructions on this.

{{< alert title="Add support for other models" color="tip" >}}
ML models must be designed in particular shapes to work with the `mlmodel` [classification](/vision/configure/) or [detection](/vision/configure/) models of Viam's [vision service](/vision/configure/).
See [ML Model Design](/reference/) to design a modular ML model service with models that work with vision.
{{< /alert >}}

## Steps

### 1. Add an ML model service

1. Go to [app.viam.com](https://app.viam.com) and navigate to your machine.
2. Confirm it shows as **Live**.
3. Click the **+** button.
4. Select **Configuration block**.
5. Search for **tflite_cpu** (or the appropriate implementation for your
   model format). For help choosing, see [Supported frameworks and hardware](#supported-frameworks-and-hardware).
6. Click **Add component**, name it `my-ml-model`, and click **Add component**
   again to confirm.

### 2. Configure the ML model service

After creating the service, configure it to point to your model file.

**If you deployed a model from the Viam registry:**

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

The `${packages.my-model}` variable resolves to the directory where the registry package was downloaded. Replace `my-model` with the name of your deployed model package.

**If you have a local model file:**

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

The `model_path` is the path to the model file on the machine where `viam-server` is running. The `label_path` is optional but recommended --it maps numeric class IDs to human-readable names.

#### Deploy a specific version of an ML model

When you add a model to the ML model service in the app interface, it automatically uses the latest version.
In the ML model service panel, you can change the version in the version dropdown.
Save your config to use your specified version of the ML model.

### 3. Add a vision service

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for **vision / mlmodel** (`vision:mlmodel`). You can also search for
   **computer vision**.
4. Click **Add component**, name it `my-detector`, and click **Add component**
   again to confirm.

### 4. Configure the vision service

Link the vision service to your ML model service:

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

The `mlmodel_name` must match the name you gave your ML model service in step 1. This is how the vision service knows which model to use for inference.

For the full list of `mlmodel` vision service configuration attributes, see [Configure an mlmodel Detector or Classifier](/vision/configure/).

### 5. Save the configuration

Click **Save** in the upper right. `viam-server` reloads automatically and initializes both services. You do not need to restart anything.

You can verify which capabilities your vision service supports by calling [`GetProperties`](/reference/apis/services/vision/#getproperties). This returns whether the service supports detections, classifications, and 3D object point clouds.

### 6. Test from the CONTROL tab

1. Go to the **CONTROL** tab in the Viam app.
2. Find your camera in the component list and open it.
3. Enable the camera stream.
4. In the vision service overlay dropdown, select your vision service (`my-detector`).
5. You should see bounding boxes drawn on the camera feed if your model is detecting objects in the current frame.

If the camera feed appears but no detections are shown, point the camera at an object your model was trained to recognize. If you are using a general-purpose COCO model, try pointing the camera at a person, a cup, or a keyboard.

### 7. Verify the full configuration

Your machine configuration should now include both services. The relevant sections look like this:

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

The ML model service must be listed before or alongside the vision service. The vision service depends on the ML model service, and `viam-server` resolves dependencies automatically regardless of order in the configuration file.

### mlmodel vision service attributes

The `mlmodel_name` attribute is the only required field. The remaining attributes let you fine-tune how the vision service interprets model output:

| Attribute                    | Type           | Required     | Description                                                                                                                                                                             |
| ---------------------------- | -------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mlmodel_name`               | string         | **Required** | Name of the ML model service to use.                                                                                                                                                    |
| `default_minimum_confidence` | float          | Optional     | Minimum confidence threshold (0.0-1.0) for all labels. Detections and classifications below this are filtered out.                                                                      |
| `label_confidences`          | object         | Optional     | Per-label confidence thresholds. Keys are label names, values are minimum confidence (0.0-1.0). Overrides `default_minimum_confidence` for specific labels.                             |
| `label_path`                 | string         | Optional     | Path to a labels file. Overrides the label file specified in the ML model service.                                                                                                      |
| `camera_name`                | string         | Optional     | Default camera to use when calling methods that take a camera name.                                                                                                                     |
| `remap_input_names`          | object         | Optional     | Map model input tensor names to the names the vision service expects. Use when the model's input names do not match the standard convention.                                            |
| `remap_output_names`         | object         | Optional     | Map model output tensor names to the names the vision service expects (for example, `location`, `category`, `score`). Use when the model's output names differ from the expected names. |
| `xmin_ymin_xmax_ymax_order`  | array of int   | Optional     | Specifies the order of bounding box coordinates in the model's output tensor as indices `[xmin, ymin, xmax, ymax]`. Use when the model outputs coordinates in a non-standard order.     |
| `input_image_mean_value`     | array of float | Optional     | Per-channel mean values for input image normalization (for example, `[127.5, 127.5, 127.5]`). Subtracted from each pixel before inference.                                              |
| `input_image_std_dev`        | array of float | Optional     | Per-channel standard deviation values for input normalization (for example, `[127.5, 127.5, 127.5]`). Each pixel is divided by this after mean subtraction.                             |
| `input_image_bgr`            | bool           | Optional     | Set to `true` if the model expects BGR channel order instead of RGB. Default: `false`.                                                                                                  |

For most pre-trained models from the Viam registry, only `mlmodel_name` is needed. The advanced attributes are useful when working with custom models that have non-standard input/output formats.

### Using an ML model service directly

You can also use the ML model service directly to run raw tensor inference, without a vision service.
This is useful for non-vision ML models or when you need to interpret the raw model output yourself.

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Visit your machine's **CONFIGURE** or **CONTROL** page.
1. Expand the **TEST** area of the ML model service panel to view the tensor output.

{{< imgproc src="/tutorials/data-management/tensor-output.png" alt="Example tensor output" resize="x1000" class="shadow imgzoom fill" >}}

{{% /tab %}}
{{% tab name="Python" %}}

The following code passes an image to an ML model service, and uses the [`Infer`](/reference/apis/services/ml/#infer) method to make inferences:

{{< read-code-snippet file="/static/include/examples-generated/run-inference.snippet.run-inference.py" lang="py" class="line-numbers linkable-line-numbers" data-line="82-85" >}}

{{% /tab %}}
{{% tab name="Go" %}}

The following code passes an image to an ML model service, and uses the [`Infer`](/reference/apis/services/ml/#infer) method to make inferences:

{{< read-code-snippet file="/static/include/examples-generated/run-inference.snippet.run-inference.go" lang="go" class="line-numbers linkable-line-numbers" data-line="161-164" >}}

{{% /tab %}}
{{< /tabs >}}

## Available services and models

### Available ML model services

{{<resources_svc api="rdk:service:mlmodel" type="ML model">}}

### Available vision services

{{% expand "Click to search available vision services" %}}

{{<resources_svc api="rdk:service:vision" type="vision">}}

{{% /expand%}}

{{% expand "Click to view example vision services" %}}

<!-- prettier-ignore -->
| Example | Description |
| ------- | ----------- |
| Detect a variety of objects | Use the [`viam:vision:mlmodel`](/vision/configure/) vision service with the `EfficientDet-COCO` ML model to detect a variety of objects, including people, bicycles, and apples, in a camera feed. |
| Detect license plates | Use the [`viam-soleng:vision:openalpr`](https://app.viam.com/module/viam-soleng/viamalpr) vision service to detect license plates in images. This service includes its own ML model. |

{{% /expand%}}

### Available machine learning models

You can use these publicly available machine learning models:

{{<mlmodels>}}

## Try It

Verify the full pipeline is working by running a quick detection from code.

Install the SDK if you haven't already:

```bash
pip install viam-sdk
```

{{< tabs >}}
{{% tab name="Python" %}}

Save this as `vision_test.py`:

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

Save this as `main.go`:

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

You should see a list of detected objects with their confidence scores. If the list is empty, point the camera at objects your model recognizes.

Replace the placeholder values in both examples:

1. In the Viam app, go to your machine's **CONNECT** tab.
2. Select **API keys** and copy your API key and API key ID.
3. Copy the machine address from the same tab.

To confirm the full pipeline is working end-to-end:

1. Run the Python or Go script.
2. Point the camera at an object your model recognizes.
3. Verify the script prints at least one detection with a confidence score above 0.5.
4. Move the object out of frame and run the script again. Verify that no detections (or only low-confidence detections) are returned.

If both tests pass, your vision pipeline is configured correctly and ready for use by downstream how-to guides.

## Cloud inference

Cloud inference enables you to run machine learning models in the Viam cloud, instead of on a local machine.
Cloud inference provides more computing power than edge devices, enabling you to run more computationally-intensive models or achieve faster inference times.

You can run cloud inference using any TensorFlow and TensorFlow Lite model in the Viam registry, including unlisted models owned by or shared with you.

To run cloud inference, you must pass the following:

- the binary data ID and organization of the data you want to run inference on
- the name, version, and organization of the model you want to use for inference

You can obtain the binary data ID from the [**DATA** tab](https://app.viam.com/data/view) and the organization ID by running the CLI command `viam org list`.
You can find the model information on the [**MODELS** tab](https://app.viam.com/models).

```sh {class="command-line" data-prompt="$" data-output="2-18"}
viam infer --binary-data-id <binary-data-id> --model-name <model-name> --model-org-id <org-id-that-owns-model> --model-version "2025-04-14T16-38-25" --org-id <org-id-that-executes-inference>
Inference Response:
Output Tensors:
  Tensor Name: num_detections
    Shape: [1]
    Values: [1.0000]
  Tensor Name: classes
    Shape: [32 1]
    Values: [...]
  Tensor Name: boxes
    Shape: [32 1 4]
    Values: [...]
  Tensor Name: confidence
    Shape: [32 1]
    Values: [...]
Annotations:
Bounding Box Format: [x_min, y_min, x_max, y_max]
  No annotations.
```

The command returns a list of detected classes or bounding boxes depending on the output of the ML model you specified, as well as a list of confidence values for those classes or boxes.
The bounding box output uses proportional coordinates between 0 and 1, with the origin `(0, 0)` in the top left of the image and `(1, 1)` in the bottom right.

For more information, see [`viam infer`](/cli/#infer).

## Troubleshooting

{{< expand "Vision service fails to start" >}}

- Check the `viam-server` logs for error messages. The most common cause is a mismatch between the `mlmodel_name` in the vision service config and the name of the ML model service.
- Verify both services are saved in the configuration.

{{< /expand >}}

{{< expand "ML model service fails to load the model" >}}

- Verify the `model_path` points to a file that exists on the machine. If using `${packages.my-model}`, confirm the model package is deployed to the machine through the ML model service configuration panel.
- Check that the model file format matches the ML model implementation. A `.tflite` file requires `tflite_cpu`, not `onnx_cpu`.
- On resource-constrained machines, large models may fail to load due to insufficient memory. Check system memory usage.

{{< /expand >}}

{{< expand "Detections are empty even though the camera works" >}}

- Verify the model is trained to detect the objects in the camera's field of view. A model trained on dogs will not detect cats.
- Check the confidence threshold. Some models produce low-confidence detections that may be filtered out by default. Try lowering the threshold if your vision service configuration supports it.
- Ensure the camera resolution and image format are compatible with the model's expected input. Most TFLite models expect RGB images.

{{< /expand >}}

{{< expand "Detections are inaccurate or noisy" >}}

- The model may need more training data. See [Train a Model](/train/train-a-model/) for improving model quality.
- Lighting conditions affect detection quality significantly. Test under the same lighting conditions the model was trained for.
- If using a general-purpose model, expect lower accuracy than a model trained specifically for your use case.

{{< /expand >}}

{{< expand "\"Model not found\" error in code" >}}

- The service name in your code must match the name in the Viam app configuration exactly. Names are case-sensitive.
- Verify the machine is online and `viam-server` is running.
- Check that you are connecting to the correct machine address.

{{< /expand >}}

{{< expand "Multiple vision services on the same model" >}}

If you configured two vision services that reference the same ML model service, and one works while the other does not, check the `mlmodel_name` attribute in both. A common mistake is pointing both vision services at each other instead of at the ML model service.

{{< /expand >}}

{{< expand "Model loads but inference is very slow" >}}

- On a Raspberry Pi 4, a typical TFLite model runs inference in 100-500ms per frame. This is normal for CPU-based inference.
- Larger models take longer. If you need faster inference, use a smaller model architecture (MobileNet is faster than EfficientDet) or reduce the input image resolution.
- Check CPU usage on the machine. If other processes are consuming CPU, inference will be slower. Use `top` or `htop` to monitor.

{{< /expand >}}

{{< expand "Label file format errors" >}}

- The label file must be plain text with one label per line. No headers, no commas, no quotes.
- The number of labels must match the number of output classes in the model. If your model outputs 80 classes but your label file has 79 lines, the last class will have no name.
- Encoding must be UTF-8. Non-ASCII characters in labels may cause issues on some systems.

{{< /expand >}}

## What's Next

- [Detect Objects](/vision/detect/) --use the vision service to get bounding boxes, filter by confidence, and process detection results in code.
- [Classify Images](/vision/classify/) --use the vision service for whole-image classification instead of per-object detection.
- [Act on Detections](/vision/act-on-detections/) --create modules that act on detection or classification results.
- [Alert on Detections](/vision/alert-on-detections/) --send alerts when specific objects are detected.
- [Train a Model](/train/train-a-model/) --train a custom model on your own data for better accuracy on your specific use case.
