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
description: "Run inference on a model with a vision service or an SDK."
---

Inference is the process of generating output from a machine learning (ML) model.
With Viam, you can run inference to generate the following kinds of output:

- object detection (using bounding boxes)
- classification (using tags)

You can run inference locally on a Viam machine, or remotely in the Viam cloud.

## Machine inference

You can use `viam-server` to deploy and run ML models directly on your machines.

You can run inference on your machine in the following ways:

- with a vision service
- manually in application logic with an SDK

Entry-level devices such as the Raspberry Pi 4 can run small ML models, such as TensorFlow Lite (TFLite).
More powerful hardware, including the Jetson Xavier or Raspberry Pi 5 with an AI HAT+, can process larger AI models, including TensorFlow and ONNX.

{{< tabs >}}
{{% tab name="Vision service" %}}

Vision services apply an ML model to a stream of images from a camera to generate bounding boxes or classifications.

{{<resources_svc api="rdk:service:vision" type="vision">}}

{{% alert title="Tip" color="tip" %}}
Some vision services include their own ML models, and thus do not require a deployed ML model.
If your vision service does not include an ML model, you must [deploy an ML model to your machine](/data-ai/ai/deploy/) to use that service.
{{% /alert %}}

To use a vision service:

1. Visit your machine's **CONFIGURE** page.
1. Click the **+** icon next to your main machine part and select **Component or service**.
1. Type in the name of the service and select a vision service.
1. If your vision service does not include an ML model, [deploy an ML model to your machine](/data-ai/ai/deploy/) to use that service.
1. Configure the service based on your use case.
1. To view the deployed vision service, use the live detection feed.
   The feed shows an overlay of detected objects or classifications on top of a live camera feed.
   On the **CONFIGURE** or **CONTROL** pages for your machine, expand the **Test** area of the service panel to view the feed.

   {{< imgproc src="/tutorials/data-management/blue-star.png" alt="Detected blue star" resize="x200" class="shadow" >}}
   {{< imgproc src="/tutorials/filtered-camera-module/viam-figure-preview.png" alt="Detection of a viam figure with a confidence score of 0.97" resize="x200" class="shadow" >}}

For instance, you could use [`viam:vision:mlmodel`](/operate/reference/services/vision/mlmodel/) with the `EfficientDet-COCO` ML model to detect a variety of objects, including people, bicycles, and apples, in a camera feed.

Alternatively, you could use [`viam-soleng:vision:openalpr`](https://app.viam.com/module/viam-soleng/viamalpr) to detect license plates in images.
Since this service includes its own ML model, there is no need to configure a separate ML model.

After adding a vision service, you can use a vision service API method with a classifier or a detector to get inferences programmatically.
For more information, see the APIs for [ML Model](/dev/reference/apis/services/ml/) and [Vision](/dev/reference/apis/services/vision/).

{{% /tab %}}
{{% tab name="SDK" %}}

With the Viam SDK, you can pass image data to an ML model service, read the output annotations, and react to output in your own code.
Use the [`Infer`](/dev/reference/apis/services/ml/#infer) method of the ML Model API to make inferences.

For example:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import numpy as np

my_mlmodel = MLModelClient.from_robot(robot=machine, name="my_mlmodel_service")

image_data = np.zeros((1, 384, 384, 3), dtype=np.uint8)

# Create the input tensors dictionary
input_tensors = {
    "image": image_data
}

output_tensors = await my_mlmodel.infer(input_tensors)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
input_tensors := ml.Tensors{"0": tensor.New(tensor.WithShape(1, 2, 3), tensor.WithBacking([]int{1, 2, 3, 4, 5, 6}))}

output_tensors, err := myMLModel.Infer(context.Background(), input_tensors)
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

## Cloud inference

Cloud inference enables you to run machine learning models in the Viam cloud, instead of on a local machine.
Cloud inference often provides more computing power than edge devices, so you can benefit from:

- larger, more accurate models
- faster inference times

You can run cloud inference using any TensorFlow and TensorFlow Lite model in the Viam registry, including private models owned by or shared with your organization.

To run cloud inference, you must pass

- the binary data ID and organization of the data you want to run inference on
- the name, version, and organization of the model you want to use for inference

The [`viam infer`](/dev/tools/cli/#infer) CLI command runs inference in the cloud on a piece of data using the specified ML model:

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

`infer` returns a list of detected classes or bounding boxes depending on the output of the ML model you specified, as well as a list of confidence values for those classes or boxes.
This method returns bounding box output using proportional coordinates between 0 and 1, with the origin `(0, 0)` in the top left of the image and `(1, 1)` in the bottom right.
