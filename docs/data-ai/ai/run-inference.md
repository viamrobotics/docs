---
linkTitle: "Run inference"
title: "Run inference"
weight: 50
layout: "docs"
type: "docs"
modulescript: true
aliases:
  - /how-tos/detect-people/
  - /get-started/detect-people/
  - /how-tos/detect-color/
  - /services/vision/
  - /ml/vision/detection/
  - /ml/vision/classification/
  - /ml/vision/segmentation/
  - /ml/vision/
  - /get-started/quickstarts/detect-people/
description: "Run machine learning inference locally on your robot or remotely in the cloud using vision services, ML model services, or SDKs."
date: "2025-09-12"
---

Inference is the process of generating output from a machine learning (ML) model.

You can run inference [locally on a Viam machine](#machine-inference), or [remotely in the Viam cloud](#cloud-inference).

## Machine inference

When you have [deployed an ML model](/data-ai/ai/deploy/) on your machine, you can run inference on your machine [directly with the ML model service](#using-an-ml-model-service-directly) or [using a vision service](#using-a-vision-service) that interprets the inferences.

Entry-level devices such as the Raspberry Pi 4 can run small ML models, such as TensorFlow Lite (TFLite).
More powerful hardware, including the Jetson Xavier or Raspberry Pi 5 with an AI HAT+, can process larger models, including TensorFlow and ONNX.
If your hardware does not support the model you want to run, see [Cloud inference](#cloud-inference).

### Using an ML model service directly

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Visit your machine's **CONFIGURE** or **CONTROL** page.
1. Expand the **TEST** area of the ML model service panel to view the tensor output.

{{< imgproc src="/tutorials/data-management/tensor-output.png" alt="Example tensor output" resize="x1000" class="shadow imgzoom fill" >}}

{{% /tab %}}
{{% tab name="Python" %}}

The following code passes an image to an ML model service, and uses the [`Infer`](/dev/reference/apis/services/ml/#infer) method to make inferences:

{{< read-code-snippet file="/static/include/examples-generated/run-inference.snippet.run-inference.py" lang="py" class="line-numbers linkable-line-numbers" data-line="82-85" >}}

{{% /tab %}}
{{% tab name="Go" %}}

The following code passes an image to an ML model service, and uses the [`Infer`](/dev/reference/apis/services/ml/#infer) method to make inferences:

{{< read-code-snippet file="/static/include/examples-generated/run-inference.snippet.run-inference.go" lang="go" class="line-numbers linkable-line-numbers" data-line="166-171" >}}

{{% /tab %}}
{{< /tabs >}}

### Using a vision service

Vision services apply an ML model to a stream of images from a camera to:

- detect objects (using bounding boxes)
- classify (using tags)

To use a vision service:

1. Navigate to your machine's **CONFIGURE** page.
1. Click the **+** icon next to your main machine part and select **Component or service**.
1. Select a vision service.
1. Configure your vision service.
   If your vision service does not include an ML model, you need to [deploy an ML model to your machine](/data-ai/ai/deploy/) and select it when configuring your vision service.

{{% expand "Click to search available vision services" %}}

{{<resources_svc api="rdk:service:vision" type="vision">}}

{{% /expand%}}

{{% expand "Click to view example vision services" %}}

<!-- prettier-ignore -->
| Example | Description |
| ------- | ----------- |
| Detect a variety of objects | Use the [`viam:vision:mlmodel`](/operate/reference/services/vision/mlmodel/) vision service with the `EfficientDet-COCO` ML model to detect a variety of objects, including people, bicycles, and apples, in a camera feed. |
| Detect license plates | Use the [`viam-soleng:vision:openalpr`](https://app.viam.com/module/viam-soleng/viamalpr) vision service to detect license plates in images. This service includes its own ML model. |

{{% /expand%}}

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Visit your machine's **CONFIGURE** or **CONTROL** page.
1. Expand the **TEST** area of the vision service panel.

   The feed shows an overlay of detected objects or classifications on top of a live camera feed.

   {{< imgproc src="/tutorials/data-management/blue-star.png" alt="Detected blue star" resize="x200" class="shadow" >}}
   {{< imgproc src="/tutorials/filtered-camera-module/viam-figure-preview.png" alt="Detection of a viam figure with a confidence score of 0.97" resize="x200" class="shadow" >}}

{{% /tab %}}
{{% tab name="Python" %}}

The following code passes an image from a camera to a vision service and uses the [`GetClassifications`](/dev/reference/apis/services/vision/#GetClassifications) method:

{{< read-code-snippet file="/static/include/examples-generated/run-vision-service.snippet.run-vision-service.py" lang="py" class="line-numbers linkable-line-numbers" data-line="36-37" >}}

{{% /tab %}}
{{% tab name="Go" %}}

The following code passes an image from a camera to a vision service and uses the [`GetClassifications`](/dev/reference/apis/services/vision/#GetClassifications) method:

{{< read-code-snippet file="/static/include/examples-generated/run-vision-service.snippet.run-vision-service.go" lang="go" class="line-numbers linkable-line-numbers" data-line="66-69" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

The following code passes an image from a camera to a vision service and uses the [`GetClassifications`](/dev/reference/apis/services/vision/#GetClassifications) method:

{{< read-code-snippet file="/static/include/examples-generated/run-vision-service.snippet.run-vision-service.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="32-38" >}}

{{% /tab %}}
{{< /tabs >}}

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

For more information, see [`viam infer`](/dev/tools/cli/#infer).
