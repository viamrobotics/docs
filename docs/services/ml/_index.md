---
title: "ML Model Service"
linkTitle: "ML Model"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/deploy-model/
description: "Deploy Machine Learning models to a robot."
icon: "/services/icons/ml.svg"
# SME: Aaron Casas
---

The ML Model service allows you to deploy machine learning models to your robots.

## Create an ML model service

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the [robot page on the Viam app](https://app.viam.com/robots).
Click on the robot you wish to add the ML Model Service to.
Select the **Config** tab, and click on **Services**.

Scroll to the **Create Service** section.

1. Select `mlmodel` as the **Type**.
2. Enter a name as the **Name**.
3. Select `tflite_cpu` as the **Model**.
4. Click **Create Service**.

{{< imgproc src="/services/ml-models-service.png" alt="Create a machine learning models service" resize="1000x" declaredimensions=true >}}

You can choose to configure your service with an existing model on the robot or deploy a model onto your robot:

{{< tabs >}}
{{% tab name="Existing Model" %}}

To configure your service with an existing model on the robot, select **Path to Existing Model On Robot** for the **Deployment** field.

Then specify the absolute **Model Path** and any **Optional Settings** such as the absolute **Label Path** and the **Number of threads**.

{{< imgproc src="/services/available-models.png" alt="Create a machine learning models service with an existing model" resize="1000x" declaredimensions=true >}}

{{% /tab %}}
{{% tab name="Deploy Model" %}}

To configure your service and deploy a model onto your robot, select **Deploy Model On Robot** for the **Deployment** field.

Then select the **Models** and any **Optional Settings** such as the **Number of threads**.

{{< imgproc src="/services/deploy-model.png" alt="Create a machine learning models service with a model to be deployed" resize="1000x" declaredimensions=true >}}

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the `tflite_cpu` ML model object to the services array in your raw JSON configuration:

``` json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<mlmodel_name>",
    "type": "mlmodel",
    "model": "tflite_cpu",
    "attributes": {
      "model_path": "${packages.<model-name>}/<model-name>.tflite",
      "label_path": "${packages.<model-name>}/labels.txt",
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
      "model_path": "${packages.<model-name>}/<model-name>.tflite",
      "label_path": "${packages.<model-name>}/labels.txt",
      "num_threads": 1
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `"tflite_cpu"` model:

| Parameter | Inclusion | Description |
| --------- | --------- | ----------- |
| `model_path` | _Required_ | The absolute path to the `.tflite model` file, as a `string`. |
| `label_path` | _Optional_ | The absolute path to a `.txt` file that holds class labels for your TFLite model, as a `string`. The SDK expects this text file to contain an ordered listing of the class labels. Without this file, classes will read as "1", "2", and so on. |
| `num_threads` | _Optional_ | An integer that defines how many CPU threads to use to run inference. Default: `1`. |

Save the configuration and your model will be added to your robot at <file>$HOME/.viam/packages/\<model-name\>/\<file-name\></file>.

{{< alert title="Info" color="info" >}}
If you upload or train a new version of a model, Viam automatically deploys the `latest` version of the model to the robot.
If you do not want Viam to automatically deploy the `latest` version of the model, you can change the  `packages` configuration in the [Raw JSON robot configuration](../../manage/configuration/#the-config-tab).
{{< /alert >}}

You can get the version number from a specific model version by clicking on **COPY** on the model on the models tab of the **DATA** page.
The model package config looks like this:

```json
{"package":"<model_id>/allblack","version":"1234567891011","name":"<model_name>"}
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

## Next Steps

To make use of your new model, follow the instructions to create:

- a [`mlmodel` detector](../vision/detection/#configure-a-mlmodel-detector) or
- a [`mlmodel` classifier](../vision/classification/#configure-a-mlmodel-classifier)
