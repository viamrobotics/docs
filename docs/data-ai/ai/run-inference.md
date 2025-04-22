---
linkTitle: "Run inference"
title: "Run inference on a model"
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

After deploying an ml model, you need to configure an additional service to use the inferences the deployed model makes.
You can run inference on an ML model with a vision service or use an SDK to further process inferences.

## Use a vision service

Vision services work to provide computer vision.
They use an ML model and apply it to the stream of images from your camera.

{{<resources_svc api="rdk:service:vision" type="vision">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

Note that many of these services have built in ML models, and thus do not need to be run alongside an ML model service.

One vision service you can use to run inference on a camera stream if you have an ML model service configured is the `mlmodel` service.

### Configure an mlmodel vision service

Add the `vision / ML model` service to your machine.
Then, from the **Select model** dropdown, select the name of the ML model service you configured when [deploying](/data-ai/ai/deploy/) your model (for example, `mlmodel-1`).

**Save** your changes.

### Test your changes

You can test a deployed vision service by clicking on the **Test** area of its configuration panel or from the [**CONTROL** page](/manage/troubleshoot/teleoperate/default-interface/#viam-app).

The camera stream shows when the vision service identifies something.
Try pointing the camera at a scene similar to your training data.

{{< imgproc src="/tutorials/data-management/blue-star.png" alt="Detected blue star" resize="x200" class="shadow" >}}
{{< imgproc src="/tutorials/filtered-camera-module/viam-figure-preview.png" alt="Detection of a viam figure with a confidence score of 0.97" resize="x200" class="shadow" >}}

{{% expand "Want to limit the number of shown classifications or detections? Click here." %}}

If you are seeing a lot of classifications or detections, you can set a minimum confidence threshold.

Start by setting the value to 0.8.
This reduces your output by filtering out anything below a threshold of 80% confidence.
You can adjust this attribute as necessary.

Click the **Save** button in the top right corner of the page to save your configuration, then close and reopen the **TEST** panel of the vision service configuration panel.
Now if you reopen the panel, you will only see classifications or detections with a confidence value higher than the `default_minimum_confidence` attribute.

{{< /expand>}}

For more detailed information, including optional attribute configuration, see the [`mlmodel` docs](/operate/reference/services/vision/mlmodel/).

## Use an SDK

You can also run inference using a Viam SDK.
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

After adding a vision service, you can use a vision service API method with a classifier or a detector to get inferences programmatically.
For more information, see the ML Model and Vision APIs:

{{< cards >}}
{{< card link="/dev/reference/apis/services/ml/" customTitle="ML Model API" noimage="True" >}}
{{% card link="/dev/reference/apis/services/vision/" customTitle="Vision service API" noimage="True" %}}
{{< /cards >}}
