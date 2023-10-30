---
title: "ML Model Service"
linkTitle: "ML Model"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/deploy-model/
description: "Deploy Machine Learning models to a smart machine."
icon: "/services/icons/ml.svg"
# SME: Aaron Casas
---

Once you have [trained](/manage/ml/train-model/) or [uploaded](/manage/ml/upload-model/) your model, the Machine Learning (ML) model service allows you to deploy machine learning models to your smart machine.

You can use the following built-in model:

{{< alert title="Note" color="note" >}}
For some models, like the [Triton MLModel](/modular-resources/examples/triton/) for Jetson boards, you can configure the service to use the available CPU or GPU.
{{< /alert >}}

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`"tflite_cpu"` model](#create-an-ml-model-service) | Runs a tensorflow lite model that you have [trained](/manage/ml/train-model/) or [uploaded](/manage/ml/upload-model/). |

### Modular Resources

{{<modular-resources api="rdk:service:mlmodel" type="mlmodel">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Create an ML model service

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to your robot's **Config** tab on the [Viam app](https://app.viam.com/robots).
Click the **Services** subtab and click **Create service** in the lower-left corner.
Select the `ML Model` type, then select the `TFLite CPU` model.
Enter a name for your service and click **Create**.

You can choose to configure your service with an existing model on the smart machine or deploy a model onto your smart machine:

{{< tabs >}}
{{% tab name="Existing Model" %}}

To configure your service with an existing model on the robot, select **Path to Existing Model On Robot** for the **Deployment** field.

Then specify the absolute **Model Path** and any **Optional Settings** such as the absolute **Label Path** and the **Number of threads**.

![Create a machine learning models service with an existing model](/services/available-models.png)

{{% /tab %}}
{{% tab name="Deploy Model" %}}

To configure your service and deploy a model onto your robot, select **Deploy Model On Robot** for the **Deployment** field.

Then select the **Models** and any **Optional Settings** such as the **Number of threads**.

![Create a machine learning models service with a model to be deployed](/services/deploy-model.png)

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
      "model_path": "${packages.ml_model.<model_name>}/<model-name>.tflite",
      "label_path": "${packages.ml_model.<model_name>}/labels.txt",
      "num_threads": <number>
    }
  },
  ... // Other services
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "fruit_classifier",
    "type": "mlmodel",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "${packages.ml_model.my_fruit_model}/my_fruit_model.tflite",
      "label_path": "${packages.ml_model.my_fruit_model}/labels.txt",
      "num_threads": 1
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `"tflite_cpu"` model:

<!-- prettier-ignore -->
| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `model_path` | **Required** | The absolute path to the `.tflite model` file, as a `string`. |
| `label_path` | Optional | The absolute path to a `.txt` file that holds class labels for your TFLite model, as a `string`. The SDK expects this text file to contain an ordered listing of the class labels. Without this file, classes will read as "1", "2", and so on. |
| `num_threads` | Optional | An integer that defines how many CPU threads to use to run inference. Default: `1`. |

Save the configuration and your model will be added to your robot at <file>$HOME/.viam/packages/\<model-name\>/\<file-name\></file>.

{{< alert title="Info" color="info" >}}
If you upload or train a new version of a model, Viam automatically deploys the `latest` version of the model to the robot.
If you do not want Viam to automatically deploy the `latest` version of the model, you can change the `packages` configuration in the [Raw JSON robot configuration](../../manage/configuration/#the-config-tab).
{{< /alert >}}

You can get the version number from a specific model version by clicking on **COPY** on the model on the models tab of the **DATA** page.
The model package config looks like this:

```json
{
  "package": "<model_id>/allblack",
  "version": "YYYYMMDDHHMMSS",
  "name": "<model_name>",
  "type": "ml_model"
}
```

### `tflite_cpu` Limitations

We strongly recommend that you package your `.tflite_cpu` model with metadata in [the standard form](https://github.com/tensorflow/tflite-support/blob/560bc055c2f11772f803916cb9ca23236a80bf9d/tensorflow_lite_support/metadata/metadata_schema.fbs).

In the absence of metadata, your `.tflite_cpu` model must satisfy the following requirements:

- A single input tensor representing the image of type UInt8 (expecting values from 0 to 255) or Float 32 (values from -1 to 1).
- At least 3 output tensors (the rest won’t be read) containing the bounding boxes, class labels, and confidence scores (in that order).
- Bounding box output tensor must be ordered [x x y y], where x is an x-boundary (xmin or xmax) of the bounding box and the same is true for y.
  Each value should be between 0 and 1, designating the percentage of the image at which the boundary can be found.

These requirements are satisfied by a few publicly available model architectures including EfficientDet, MobileNet, and SSD MobileNet V1.
You can use one of these architectures or build your own.

## Use the ML model service with the Viam Python SDK

To use the ML model service from the [Viam Python SDK](https://python.viam.dev/), you must install both the Python SDK itself and the `mlmodel` extra:

```sh
pip install viam-sdk
pip install 'viam-sdk[mlmodel]'
```

See the [Python documentation](https://python.viam.dev/autoapi/viam/services/mlmodel/mlmodel/index.html#viam.services.mlmodel.mlmodel.MLModel) for more information about the `MLModel` service in Python

See [program your smart machine](/program/) for more information.

## Next Steps

To make use of your model with your smart machine, add a [vision service](/services/vision/) or a [modular resource](/modular-resources/):

{{< cards >}}

{{% manualcard link="/services/vision/detection/#configure-an-mlmodel-detector"%}}

<h4>Create a detector with your model</h4>

Configure an `mlmodel detector`.

{{% /manualcard %}}
{{% manualcard link="/services/vision/classification/#configure-an-mlmodel-classifier"%}}

<h4>Create a classifier with your model</h4>

Configure your `mlmodel classifier`.

{{% /manualcard %}}

{{% card link="/modular-resources/examples/tflite-module/" customTitle="Example: TensorFlow Lite Modular Service" %}}

{{< /cards >}}
