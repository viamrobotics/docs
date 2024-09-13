---
title: "ML Models"
linkTitle: "ML Models"
weight: 40
type: "docs"
tags: ["data management", "ml", "model training"]
images: ["/services/ml/train-model.gif"]
videos: ["/services/ml/train-model.webm","/services/ml/train-model.mp4"]
videoAlt: "Add a bounding box around the dog in an image."
aliases:
  - /data/train-model/
description: "Machine learning models are mathematical models that can recognize patterns. You can use them on your machines to interpret the machine's surroundings."
aliases:
  - /services/ml/upload-model/
  - /services/ml/edit/
  - /ml/edit/
  - /manage/data/upload-model/
  - /manage/ml/upload-model/
  - /ml/upload-model/
no_service: true
modulescript: true
# SME: Tahiya + Alexa Greenberg
---

Machine Learning (ML) models are mathematical models that can recognize patterns.

The [ML model service](/services/ml/deploy/) runs ML models on your machines.
Services like the [vision service](/services/vision/mlmodel/) can then use the ML model services to provide your machine with information about its surroundings.
The ML model service works with models trained inside and outside the Viam app:

- You can upload externally trained models on the [**MODELS** tab](https://app.viam.com/data/models) in the **DATA** section of the Viam app.
- You can [train](/how-tos/deploy-ml/) models on data from your machines.
- You can use [ML models](https://app.viam.com/registry?type=ML+Model) from the Viam Registry.
- You can use a [model](/services/ml/ml-models/) trained outside the Viam platform that's already available on your machine.

## Available machine learning models in the registry

You can search the machine learning models that are available to deploy on this service from the registry here:

<div id="searchboxML"></div>
<p>
<div id="searchstatsML"></div></p>
<div class="mr-model" id="">
  <div class="modellistheader">
    <div class="name">Model</div>
    <div class="type">Type</div>
    <div class="framework">Framework</div>
    <div>Description</div>
  </div>
<div id="hitsML" class="modellist">
</div>
<div id="paginationML"></div>
</div>

## Model framework support

Viam currently supports the following frameworks:

<!-- prettier-ignore -->
| Model Framework | ML Model Service | Hardware Support | System Architecture | Description |
| --------------- | --------------- | ---------------- | ------------------- | ----------- |
| [TensorFlow Lite](https://www.tensorflow.org/lite) | [`tflite_cpu`](/services/ml/deploy/) | Any CPU <br> Nvidia GPU | Linux, Raspbian, MacOS, Android | Quantized version of TensorFlow that has reduced compatibility for models but supports more hardware. Uploaded models must adhere to the [model requirements](/services/ml/deploy/tflite_cpu/#model-requirements). |
| [ONNX](https://onnx.ai/) | [`onnx_cpu`](https://github.com/viam-labs/onnx-cpu) | Any CPU <br> Nvidia GPU | Android, MacOS, Linux arm-64 | Universal format that is not optimized for hardware inference but runs on a wide variety of machines. |
| [TensorFlow](https://www.tensorflow.org/) | [`triton`](https://github.com/viamrobotics/viam-mlmodelservice-triton) | Nvidia GPU | Linux (Jetson) | A full framework that is made for more production-ready systems. |
| [PyTorch](https://pytorch.org/) | [`triton`](https://github.com/viamrobotics/viam-mlmodelservice-triton) | Nvidia GPU | Linux (Jetson) | A full framework that was built primarily for research. Because of this, it is much faster to do iterative development with (model doesn’t have to be predefined) but it is not as “production ready” as TensorFlow. It is the most common framework for OSS models because it is the go-to framework for ML researchers. |

## Versions

If you [deploy a model](/services/ml/) to a machine, Viam automatically assumes that this is the `latest` version of the model and that you would always like to deploy the `latest` version of the model to the machine.
If you train a new version of that model, Viam will automatically deploy the new version to the machine and replace the old version.

If you do not want Viam to automatically deploy the `latest` version of the model, you can change `packages` configuration in the [JSON machine configuration](/configure/#the-configure-tab).
The model package config looks like this:

```json
{
  "package": "<model_id>/<model_name>",
  "version": "YYYY-MM-DDThh-mm-ss",
  "name": "<model_name>",
  "type": "ml_model"
}
```

You can get the version number from a specific model version by navigating to the [models page](https://app.viam.com/data/models) finding the model's row, clicking on the right-side menu marked with **_..._** and selecting **Copy package JSON**. For example: `2024-02-28T13-36-51`.

{{< alert title="Note" color="note" >}}
When you [train](/how-tos/deploy-ml/) a new version of a model, the previous model remains unchanged and is not used as input.
{{< /alert >}}

If you need to make changes to a model, you can edit or delete it on its page which you can access from the [**MODELS** tab](https://app.viam.com/data/models).

## Next steps

Use the ML model service to deploy a machine learning model to your machine:

{{< cards >}}
{{% card link="/services/ml/deploy/" %}}
{{% card link="/how-tos/deploy-ml/" %}}
{{< /cards >}}

Follow one of these tutorials to see ML models in action:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai/" customDescription="Add object detection, speech recognition, natural language processing, and speech synthesis capabilities to a machine." %}}
{{< /cards >}}
