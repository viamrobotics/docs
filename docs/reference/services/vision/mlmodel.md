---
title: "Configure an mlmodel detector or classifier"
linkTitle: "mlmodel"
weight: 10
type: "docs"
description: "Configure the mlmodel vision service to turn a deployed ML model into a detector, classifier, or 3D segmenter."
service_description: "A detector, classifier, or 3D segmenter that wraps a deployed ML model."
tags: ["vision", "computer vision", "CV", "services", "detection"]
images: ["/services/vision/dog-detector.png"]
date: "2026-04-14"
aliases:
  - /operate/reference/services/vision/mlmodel/
  - /services/vision/detection/
  - /services/vision/classification/
  - /ml/vision/mlmodel/
  - /services/vision/mlmodel/
  - /data-ai/services/vision/mlmodel/
---

The `mlmodel` vision service wraps a deployed ML model and exposes it through the standard [vision service API](/reference/apis/services/vision/). At startup, the service reads the model's tensor metadata and decides which of three roles the model can fulfill: classifier, detector, or 3D segmenter. It registers every role the model supports.

## Prerequisites {#prerequisites}

Before configuring an `mlmodel` vision service, you need:

{{< cards >}}
{{% manualcard %}}

<h4>1. A trained or uploaded ML model</h4>

Add an existing model from the [registry](https://app.viam.com/registry) or [train one from your data](/data-ai/train/train/). The model must be TensorFlow Lite, TensorFlow, ONNX, or PyTorch.

{{% /manualcard %}}
{{% manualcard %}}

<h4>2. An ML model service running on your machine</h4>

Configure an [ML model service](/data-ai/ai/deploy/) with an implementation that matches your model format (for example, `tflite_cpu`, `onnx-cpu`, `tensorflow-cpu`, or `torch-cpu`).

{{% /manualcard %}}
{{< /cards >}}

## Configure

{{< tabs >}}
{{% tab name="Builder" %}}

1. Navigate to the **CONFIGURE** tab of your machine's page.
2. Click the **+** icon next to your machine part in the left-hand menu and select **Configuration block**.
3. In the search field, type `vision` or `mlmodel` and select the `vision / mlmodel` result.
4. Enter a name for your service and click **Add component**.
5. In the **ML MODEL** section, select the ML model service your model is deployed on.
6. In the **DEFAULT CAMERA** section, select the camera the service should use by default for calls such as `GetDetectionsFromCamera`.
7. Adjust other attributes in the attributes table as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<service_name>",
    "api": "rdk:service:vision",
    "model": "mlmodel",
    "attributes": {
      "mlmodel_name": "<mlmodel-service-name>",
      "camera_name": "<camera-name>"
    }
  }
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

{{< tabs >}}
{{% tab name="Detector" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "person_detector",
    "api": "rdk:service:vision",
    "model": "mlmodel",
    "attributes": {
      "mlmodel_name": "my_mlmodel_service",
      "camera_name": "camera-1",
      "default_minimum_confidence": 0.6
    }
  }
]
```

{{% /tab %}}
{{% tab name="Classifier" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "fruit_classifier",
    "api": "rdk:service:vision",
    "model": "mlmodel",
    "attributes": {
      "mlmodel_name": "fruit_classifier",
      "camera_name": "camera-1"
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

## Attributes

<!-- prettier-ignore -->
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------- |
| `mlmodel_name` | string | **Required** | The name of the [ML model service](/data-ai/ai/deploy/) the vision service wraps. |
| `camera_name` | string | Optional | The default camera to use for calls such as `GetDetectionsFromCamera`, `GetClassificationsFromCamera`, and `GetObjectPointClouds`. |
| `default_minimum_confidence` | number | Optional | Minimum confidence score (between `0.0` and `1.0`) applied to all output labels. Detections and classifications below this are filtered out. If unset, no filtering is applied. <br> Example: `0.6` |
| `label_confidences` | object | Optional | Per-label confidence thresholds. Keys are label names and values are minimum confidence. When set, `label_confidences` overrides `default_minimum_confidence` for listed labels and other labels are filtered out. <br> Example: `{"DOG": 0.8, "CARROT": 0.3}` |
| `label_path` | string | Optional | Path to a labels file. Overrides the label file specified in the ML model service. The file is one label per line; line number (zero-indexed) is the class ID. |
| `remap_input_names` | object | Optional | Map model input tensor names to the names the vision service expects. The service expects `image` for the input tensor. See [Tensor name requirements](#tensor-name-requirements). |
| `remap_output_names` | object | Optional | Map model output tensor names to the names the vision service expects (`location`, `category`, `score` for detectors; `probability` for classifiers). See [Tensor name requirements](#tensor-name-requirements). |
| `xmin_ymin_xmax_ymax_order` | array of int | Optional | Four-entry permutation indicating the order in which the model outputs bounding box coordinates. Use `[0, 1, 2, 3]` when the model outputs `[xmin, ymin, xmax, ymax]`. Use `[1, 0, 3, 2]` when the model outputs `[ymin, xmin, ymax, xmax]`. Common source of shifted or mirrored detections when using custom YOLO variants. |
| `input_image_mean_value` | array of float | Optional | Per-channel mean values subtracted from each pixel before inference. Requires at least 3 values, one per color channel. Set this only when the model was trained with non-default input normalization. If unset, no mean subtraction is applied. <br> Example: `[127.5, 127.5, 127.5]` |
| `input_image_std_dev` | array of float | Optional | Per-channel standard deviation values. Each pixel is divided by this after mean subtraction. Requires at least 3 values, all non-zero. Set this only when the model was trained with non-default input normalization. If unset, no division is applied. <br> Example: `[127.5, 127.5, 127.5]` |
| `input_image_bgr` | bool | Optional | Set to `true` if the model expects BGR channel order instead of RGB. If detections have wrong colors or all labels appear at once, try flipping this. <br> Default: `false` |

## Tensor name requirements

The vision service expects specific tensor names from the wrapped ML model:

| Service role | Input tensor | Output tensors                  |
| ------------ | ------------ | ------------------------------- |
| Detector     | `image`      | `location`, `category`, `score` |
| Classifier   | `image`      | `probability`                   |

If your model uses different tensor names, set `remap_input_names` and `remap_output_names` to bridge them:

{{< tabs >}}
{{% tab name="Detector remap" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "api": "rdk:service:vision",
  "model": "mlmodel",
  "attributes": {
    "mlmodel_name": "my_model",
    "remap_input_names": {
      "my_model_input_tensor1": "image"
    },
    "remap_output_names": {
      "my_model_output_tensor1": "category",
      "my_model_output_tensor2": "location",
      "my_model_output_tensor3": "score"
    },
    "camera_name": "camera-1"
  },
  "name": "my-vision-service"
}
```

{{% /tab %}}
{{% tab name="Classifier remap" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "api": "rdk:service:vision",
  "model": "mlmodel",
  "attributes": {
    "mlmodel_name": "my_model",
    "remap_input_names": {
      "my_model_input_tensor1": "image"
    },
    "remap_output_names": {
      "my_model_output_tensor1": "probability"
    },
    "camera_name": "camera-1"
  },
  "name": "my-vision-service"
}
```

{{% /tab %}}
{{< /tabs >}}

If a Viam-trained model already uses these names, you can skip `remap_input_names` and `remap_output_names` entirely.

## Test your detector or classifier

Test an `mlmodel` vision service from the [Control tab](/manage/troubleshoot/teleoperate/default-interface/#web-ui), with images in the cloud, or with code.

### Live camera footage

1. Open your machine in the Viam app and click the vision service's **Test** area, or navigate to the **CONTROL** tab and select the vision service.
2. Select your camera and click **Refresh**. Detections above `default_minimum_confidence` appear as bounding boxes on the live image.

{{< imgproc src="/services/vision/detections.png" alt="A vision service test panel showing bounding boxes on a live camera feed" resize="450x" declaredimensions=true >}}

If you want a continuous overlay in the Control tab, configure a [transform camera](/operate/reference/components/camera/transform/):

{{< tabs >}}
{{% tab name="Detections overlay" %}}

```json {class="line-numbers linkable-line-numbers"}
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

{{% /tab %}}
{{% tab name="Classifications overlay" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "pipeline": [
    {
      "type": "classifications",
      "attributes": {
        "confidence_threshold": 0.5,
        "classifier_name": "<vision-service-name>",
        "max_classifications": 5,
        "valid_labels": ["<label>"]
      }
    }
  ],
  "source": "<camera-name>"
}
```

{{% /tab %}}
{{< /tabs >}}

### Images in the cloud

If you have images stored in the [Viam Cloud](/data-ai/capture-data/capture-sync/), you can run your classifier against them:

1. Navigate to the [**DATA** tab](https://app.viam.com/data/view) and click the **Images** subtab.
2. Click an image to open the side menu and select the **Actions** tab.
3. In the **Run model** section, select your model, specify a confidence threshold, and click **Run model**.

### Code

The following examples get detections or classifications from a camera. Replace `"camera-1"` with the name of the camera you configured.

{{< tabs >}}
{{% tab name="Detections" %}}

{{< tabs >}}
{{< tab name="Python" >}}

```python {class="line-numbers linkable-line-numbers"}
from viam.components.camera import Camera
from viam.services.vision import VisionClient

robot = await connect()
camera_name = "camera-1"

cam = Camera.from_robot(robot, camera_name)
my_detector = VisionClient.from_robot(robot, "my_detector")

# Get detections from the camera in one call
detections = await my_detector.get_detections_from_camera(camera_name)

# Or capture an image first, then run detections on it
images, _ = await cam.get_images()
img = images[0]
detections_from_image = await my_detector.get_detections(img)

await robot.close()
```

{{< /tab >}}
{{< tab name="Go" >}}

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

myDetector, err := vision.FromProvider(machine, "my_detector")
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
  logger.Fatalf("could not decode image from camera: %v", err)
}
detectionsFromImage, err := myDetector.Detections(context.Background(), img, nil)
if err != nil {
  logger.Fatalf("could not get detections: %v", err)
}
if len(detectionsFromImage) > 0 {
  logger.Info(detectionsFromImage[0])
}
```

{{< /tab >}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Classifications" %}}

{{< tabs >}}
{{< tab name="Python" >}}

```python {class="line-numbers linkable-line-numbers"}
from viam.components.camera import Camera
from viam.services.vision import VisionClient

robot = await connect()
camera_name = "camera-1"
cam = Camera.from_robot(robot, camera_name)
my_classifier = VisionClient.from_robot(robot, "my_classifier")

# Get the top 2 classifications from the camera in one call
classifications = await my_classifier.get_classifications_from_camera(
    camera_name, 2)

# Or capture an image first, then run classifications on it
images, _ = await cam.get_images()
img = images[0]
classifications_from_image = await my_classifier.get_classifications(img, 2)

await robot.close()
```

{{< /tab >}}
{{< tab name="Go" >}}

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

myClassifier, err := vision.FromProvider(machine, "my_classifier")
if err != nil {
  logger.Fatalf("cannot get vision service: %v", err)
}

// Get top 2 classifications from the camera in one call
classifications, err := myClassifier.ClassificationsFromCamera(context.Background(), cameraName, 2, nil)
if err != nil {
  logger.Fatalf("could not get classifications: %v", err)
}
if len(classifications) > 0 {
  logger.Info(classifications[0])
}

// Or capture an image first, then run classifications on it
img, err := camera.DecodeImageFromCamera(context.Background(), myCam, nil, nil)
if err != nil {
  logger.Fatalf("could not decode image from camera: %v", err)
}
classificationsFromImage, err := myClassifier.Classifications(context.Background(), img, 2, nil)
if err != nil {
  logger.Fatalf("could not get classifications: %v", err)
}
if len(classificationsFromImage) > 0 {
  logger.Info(classificationsFromImage[0])
}
```

{{< /tab >}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Tip" color="tip" %}}
To fetch an image, detections, classifications, and point cloud objects in one round trip, use [`CaptureAllFromCamera`](/reference/apis/services/vision/#captureallfromcamera). This is more efficient than separate calls and guarantees all results correspond to the same frame.
{{% /alert %}}

## Troubleshoot

{{< expand "Detections appear shifted or mirrored" >}}

The model's output bounding box coordinate order does not match the vision service's expected order. Set `xmin_ymin_xmax_ymax_order` to a permutation that matches your model. For example, a YOLO variant that outputs `[ymin, xmin, ymax, xmax]` needs `[1, 0, 3, 2]`.

{{< /expand >}}

{{< expand "Detections have wrong labels or fire constantly" >}}

Input preprocessing probably does not match the model. Check:

- `input_image_bgr`: set to `true` if the model was trained on BGR images.
- `input_image_mean_value` and `input_image_std_dev`: set these if the model expects normalized input.
- `label_path`: verify the labels file matches the model's output classes in order.

{{< /expand >}}

{{< expand "Model is loaded but zero detections ever" >}}

- Confirm `mlmodel_name` matches the ML model service name exactly (case-sensitive).
- Verify the model's input tensor is named `image` or that `remap_input_names` bridges it.
- For detectors, confirm the model outputs `location`, `category`, and `score` tensors (or use `remap_output_names`).
- Lower `default_minimum_confidence` temporarily to see whether low-confidence detections are being filtered out.

{{< /expand >}}

{{< expand "Some labels trigger too often, others not at all" >}}

Use `label_confidences` to set different thresholds per label. For example, set `"PERSON": 0.8` to suppress false-positive person detections while keeping other labels at a lower threshold.

{{< /expand >}}

{{< expand "Service fails to start" >}}

Check `viam-server` logs. Most common causes:

- `mlmodel_name` does not match any configured ML model service name.
- `label_path` points to a file that does not exist on the machine.
- `input_image_mean_value` or `input_image_std_dev` has fewer than 3 entries, or `input_image_std_dev` contains a zero.

{{< /expand >}}

## Next steps

{{< cards >}}
{{% card link="/vision/configure/" %}}
{{% card link="/vision/detect/" %}}
{{% card link="/vision/classify/" %}}
{{< /cards >}}
