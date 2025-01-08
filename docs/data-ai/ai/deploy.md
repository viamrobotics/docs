---
linkTitle: "Deploy model"
title: "Deploy a model"
weight: 40
layout: "docs"
type: "docs"
modulescript: true
description: "The Machine Learning (ML) model service allows you to deploy machine learning models to your machine."
aliases:
  - /how-tos/train-deploy-ml/
  - /services/ml/
  - /registry/ml/
  - /services/ml/upload-model/
  - /services/ml/edit/
  - /ml/edit/
  - /manage/data/upload-model/
  - /manage/ml/upload-model/
  - /ml/upload-model/
  - /services/ml/ml-models/
  - /registry/ml-models/
---

The Machine Learning (ML) model service allows you to deploy [machine learning models](/data-ai/ai/deploy/#deploy-your-ml-model) to your machine.
The service works with models trained inside and outside the Viam app:

- You can [train TFlite](/data-ai/ai/train-tflite/) or [other models](/data-ai/ai/train/) on data from your machines.
- You can upload externally trained models on the [**MODELS** tab](https://app.viam.com/data/models) in the **DATA** section of the Viam app.
- You can use [ML models](https://app.viam.com/registry?type=ML+Model) from the [Viam Registry](https://app.viam.com/registry).
- You can use a [model](/data-ai/ai/deploy/#deploy-your-ml-model) trained outside the Viam platform whose files are on your machine.

## Deploy your ML model

Navigate to the **CONFIGURE** tab of one of your machine in the [Viam app](https://app.viam.com).
Add an ML model service that supports the ML model you trained or the one you want to use from the registry.

{{<resources_svc api="rdk:service:mlmodel" type="ML model">}}

### Model framework support

Viam currently supports the following frameworks:

<!-- prettier-ignore -->
| Model Framework | ML Model Service | Hardware Support | Description |
| --------------- | --------------- | ------------------- | ----------- |
| [TensorFlow Lite](https://www.tensorflow.org/lite) | [`tflite_cpu`](https://github.com/viam-modules/mlmodel-tflite) | linux/amd64, linux/arm64, darwin/arm64, darwin/amd64 | Quantized version of TensorFlow that has reduced compatibility for models but supports more hardware. Uploaded models must adhere to the [model requirements.](https://github.com/viam-modules/mlmodel-tflite) |
| [ONNX](https://onnx.ai/) | [`onnx-cpu`](https://github.com/viam-labs/onnx-cpu), [`triton`](https://github.com/viamrobotics/viam-mlmodelservice-triton) |  Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64 | Universal format that is not optimized for hardware inference but runs on a wide variety of machines. |
| [TensorFlow](https://www.tensorflow.org/) | [`tensorflow-cpu`](https://github.com/viam-modules/tensorflow-cpu), [`triton`](https://github.com/viamrobotics/viam-mlmodelservice-triton) | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64 | A full framework that is made for more production-ready systems. |
| [PyTorch](https://pytorch.org/) | [`torch-cpu`](https://github.com/viam-modules/torch), [`triton`](https://github.com/viamrobotics/viam-mlmodelservice-triton) | Nvidia GPU, linux/arm64, darwin/arm64 | A full framework that was built primarily for research. Because of this, it is much faster to do iterative development with (model doesn’t have to be predefined) but it is not as “production ready” as TensorFlow. It is the most common framework for OSS models because it is the go-to framework for ML researchers. |

{{< alert title="Note" color="note" >}}
For some models of the ML model service, like the [Triton ML model service](https://github.com/viamrobotics/viam-mlmodelservice-triton/) for Jetson boards, you can configure the service to use either the available CPU or a dedicated GPU.
{{< /alert >}}

For example,use the `ML model / TFLite CPU` service for TFlite ML models.
If you used the built-in training, this is the ML model service you need to use.
If you used a custom training script, you may need a different ML model service.

To deploy a model, click **Select model** and select the model from your organization or the registry.
Save your config.

### Machine learning models from registry

You can search the machine learning models that are available to deploy on this service from the registry here:

{{<mlmodels>}}

## Next steps

On its own the ML model service only runs the model.
After deploying your model, you need to configure an additional service to use the deployed model.
For example, you can configure an [`mlmodel` vision service](/operate/reference/services/vision/) to visualize the inferences your model makes.
Follow our docs to [run inference](/data-ai/ai/run-inference/) to add an `mlmodel` vision service and see inferences.

For other use cases, consider [creating custom functionality with a module](/operate/get-started/other-hardware/).

{{< alert title="Add support for other models" color="tip" >}}
ML models must be designed in particular shapes to work with the `mlmodel` [classification](/operate/reference/services/vision/mlmodel/) or [detection](/operate/reference/services/vision/mlmodel/) model of Viam's [vision service](/operate/reference/services/vision/).
See [ML Model Design](/data-ai/reference/mlmodel-design/) to design a modular ML model service with models that work with vision.
{{< /alert >}}
