---
title: "ML Models"
linkTitle: "ML Models"
weight: 20
type: "docs"
tags: ["data management", "ml", "model training"]
images: ["/services/ml/train-model.gif"]
videos: ["/services/ml/train-model.webm","/services/ml/train-model.mp4"]
videoAlt: "Add a bounding box around the dog in an image."
aliases:
  - /data/train-model/
description: "The Viam Registry provides ML models that can recognize patterns in your data. You can use them on your machines to interpret the machine's surroundings."
aliases:
  - /services/ml/upload-model/
  - /services/ml/edit/
  - /ml/edit/
  - /manage/data/upload-model/
  - /manage/ml/upload-model/
  - /ml/upload-model/
  - /services/ml/ml-models/
date: "2024-10-20"
modulescript: true
# SME: Tahiya + Alexa Greenberg
---

The Viam Registry provides Machine Learning (ML) models that can recognize patterns in your data.

{{< alert title="In this page" color="note" >}}
{{% toc %}}
{{< /alert >}}

## ML models in the registry

{{<mlmodels>}}

## Usage

To use an ML model with a machine, you have to deploy it using the [ML model service](/services/ml/).
Services like the [vision service](/services/vision/mlmodel/) can then use the ML model service to provide your machine with information about its surroundings.

{{< alert title="Add support for other models" color="tip" >}}
ML models must be designed in particular shapes to work with the `mlmodel` [classification](/services/vision/mlmodel/) or [detection](/services/vision/mlmodel/) model of Viam's [vision service](/services/vision/).
See [ML Model Design](/registry/advanced/mlmodel-design/) to design modular ML model service with models that work with vision.
{{< /alert >}}

## Versions

When you deploy a model to a machine, Viam automatically deploys the `latest` version of the model to the machine.
This also means that as new version of the ML model become available, the machine will automatically get the latest version.

If you do not want Viam to automatically deploy the `latest` version of the model, you can change the `packages` configuration in the [JSON machine configuration](/configure/#the-configure-tab) to use a specific version:

```json
{
  "package": "<model_id>/<model_name>",
  "version": "YYYY-MM-DDThh-mm-ss",
  "name": "<model_name>",
  "type": "ml_model"
}
```

For models you have uploaded or traines, you can get the version number from a specific model version by navigating to the [models page](https://app.viam.com/data/models) finding the model's row, clicking on the right-side menu marked with **_..._** and selecting **Copy package JSON**. For example: `2024-02-28T13-36-51`.

## Model framework support

Viam currently supports the following frameworks:

<!-- prettier-ignore -->
| Model Framework | ML Model Service | Hardware Support | System Architecture | Description |
| --------------- | --------------- | ---------------- | ------------------- | ----------- |
| [TensorFlow Lite](https://www.tensorflow.org/lite) | [`tflite_cpu`](https://github.com/viam-modules/mlmodel-tflite) | Any CPU <br> Nvidia GPU | Linux, Raspbian, MacOS, Android | Quantized version of TensorFlow that has reduced compatibility for models but supports more hardware. Uploaded models must adhere to the [model requirements.](https://github.com/viam-modules/mlmodel-tflite) |
| [ONNX](https://onnx.ai/) | [`onnx_cpu`](https://github.com/viam-labs/onnx-cpu) | Any CPU <br> Nvidia GPU | Android, MacOS, Linux arm-64 | Universal format that is not optimized for hardware inference but runs on a wide variety of machines. |
| [TensorFlow](https://www.tensorflow.org/) | [`triton`](https://github.com/viamrobotics/viam-mlmodelservice-triton) | Nvidia GPU | Linux (Jetson) | A full framework that is made for more production-ready systems. |
| [PyTorch](https://pytorch.org/) | [`triton`](https://github.com/viamrobotics/viam-mlmodelservice-triton) | Nvidia GPU | Linux (Jetson) | A full framework that was built primarily for research. Because of this, it is much faster to do iterative development with (model doesn’t have to be predefined) but it is not as “production ready” as TensorFlow. It is the most common framework for OSS models because it is the go-to framework for ML researchers. |

## Next steps

Use the ML model service to deploy a model to your machine or learn how to train and deploy models:

{{< cards >}}
{{% card link="/services/ml/" customTitle="ML model service" %}}
{{% card link="/how-tos/train-deploy-ml/" %}}
{{< /cards >}}

To see machine learning in actions, follow one of these tutorials:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai/" customDescription="Add object detection, speech recognition, natural language processing, and speech synthesis capabilities to a machine." %}}
{{< /cards >}}
