---
title: "Configure a tflite_cpu ML model service"
linkTitle: "tflite_cpu"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training"]
description: "Configure a tflite_cpu ML model service to deploy TensorFlow lite models to your machine."
service_description: "Runs a TensorFlow Lite model that you have trained or uploaded on the CPU of your machine."
icon: true
images: ["/services/icons/ml.svg"]
aliases:
  - /ml/deploy/tflite_cpu/
  - /services/ml/deploy/tflite_cpu/
# SME: Khari
---

The `tflite_cpu` ML model service allows you to deploy [TensorFlow Lite](https://www.tensorflow.org/lite) ML models as long as your models adhere to the [model requirements](#model-requirements).
It is supported on any CPU and Linux, Raspbian, MacOS and Android machines.

To work with the `tflite_cpu` ML model service, an ML model is comprised of a <file>.tflite</file> model file which defines the model, and optionally a <file>.txt</file> labels file which provides the text labels for your model.
With the `tflite_cpu` ML model service, you can deploy:

- [a model from the registry](https://app.viam.com/registry)
- a [model](/services/ml/ml-models/) trained outside the Viam platform that you have uploaded
- a model available on your machine

To configure a `tflite_cpu` ML model service:

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
Select the `ML model` type, then select the `TFLite CPU` model.
Enter a name or use the suggested name for your service and click **Create**.

You can choose to configure your service with an existing model on the machine or deploy a model onto your machine:

{{< tabs >}}
{{% tab name="Deploy Model on Machine" %}}

1. To configure your service and deploy a model onto your machine, select **Deploy model on machine** for the **Deployment** field in the resulting ML model service configuration pane.

2. Click **Select model**.
   In the modal that appears, search for models from your organization or the [Registry](/registry/).

{{<imgproc src="/tutorials/data-management/mlmodel-modal.png" alt="The ML model service configuration modal." resize="500x" >}}

You can select a model to see more details about it, and then select the model to deploy it to your machine.

{{<imgproc src="/tutorials/data-management/mlmodel-service-conf.png" alt="The ML model service configuration modal with a model suggested." resize="450x" >}}

3. Also, optionally select the **Number of threads**.

4. Click **Save** at the top right of the window to save your changes.

{{% /tab %}}
{{% tab name="Path to Existing Model On Robot" %}}

1. To configure your service with an existing model on the machine, select **Path to existing model on robot** for the **Deployment** field.
2. Then specify the absolute **Model path** and any **Optional settings** such as the absolute **Label path** and the **Number of threads**.

![Create a machine learning models service with an existing model](/services/available-models.png)

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the `tflite_cpu` ML model object to the services array in your raw JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<mlmodel_name>",
    "type": "mlmodel",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "${packages.<model_name>}/<model-name>.tflite",
      "label_path": "${packages.<model_name>}/labels.txt",
      "num_threads": <number>
    }
  },
  ... // Other services
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
"packages": [
  {
    "package": "39c34811-9999-4fff-bd91-26a0e4e90644/my_fruit_model",
    "version": "YYYY-MM-DDThh-mm-ss",
    "name": "my_fruit_model",
    "type": "ml_model"
  }
], ... // < Insert "components", "modules" etc. >
"services": [
  {
    "name": "fruit_classifier",
    "type": "mlmodel",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "${packages.my_fruit_model}/my_fruit_model.tflite",
      "label_path": "${packages.my_fruit_model}/labels.txt",
      "num_threads": 1
    }
  }
]
}
```

The `"packages"` array shown above is automatically created when you deploy the model.
You do not need to edit the configuration yourself, except if you wish to specify a specific [version for your deployed model](/services/ml/ml-models/#versions).

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `"tflite_cpu"` model:

<!-- prettier-ignore -->
| Parameter | Required? | Description |
| --------- | --------- | ----------- |
| `model_path` | **Required** | The absolute path to the `.tflite model` file, as a `string`. |
| `label_path` | Optional | The absolute path to a `.txt` file that holds class labels for your TFLite model, as a `string`. This text file should contain an ordered listing of class labels. Without this file, classes will read as "1", "2", and so on. |
| `num_threads` | Optional | An integer that defines how many CPU threads to use to run inference. Default: `1`. |

{{% alert title="Note" color="note" %}}
If you **Deploy model on machine**, `model_path` and `label_path` will be automatically configured in the format `"${packages.<model_name>}/<model-name>.tflite"` and `"${packages.<model_name>}/labels.txt"` respectively.

If you take the **Path to existing model on machine** approach, your model and label paths do not have to be in the same format.
For example, they might resemble `home/models/fruit/my_fruit_model.tflite`.
{{% /alert %}}

Save the configuration.

## Model requirements

{{% alert title="Tip" color="tip" %}}
Models [trained](/how-tos/deploy-ml/) in the Viam app meet these requirements by design.
{{% /alert %}}

We strongly recommend that you package your TensorFlow Lite model with metadata in [the standard form](https://github.com/tensorflow/tflite-support/blob/560bc055c2f11772f803916cb9ca23236a80bf9d/tensorflow_lite_support/metadata/metadata_schema.fbs).

In the absence of metadata, your `tflite_cpu` model must satisfy the following requirements:

- A single input tensor representing the image of type UInt8 (expecting values from 0 to 255) or Float 32 (values from -1 to 1).
- At least 3 output tensors (the rest won’t be read) containing the bounding boxes, class labels, and confidence scores (in that order).
- Bounding box output tensor must be ordered [x x y y], where x is an x-boundary (xmin or xmax) of the bounding box and the same is true for y.
  Each value should be between 0 and 1, designating the percentage of the image at which the boundary can be found.

These requirements are satisfied by a few publicly available model architectures including EfficientDet, MobileNet, and SSD MobileNet V1.
You can use one of these architectures or build your own.

## Next steps

The ML model service only runs your model on the machine.
To use the inferences from the model, you must use an additional service such as a [vision service](/services/vision/):

{{< cards >}}

{{% manualcard link="/services/vision/mlmodel/" title="Create a visual detector or classifier" noimage="True" %}}

Use your model deployed with the ML model service by adding a vision service that can provide detections or classifications depending on your ML model.

{{% /manualcard %}}
{{% card link="/how-tos/deploy-ml/" noimage="True" %}}
{{% card link="/how-tos/detect-people/" customTitle="Detect people" noimage="true" %}}

{{< /cards >}}
