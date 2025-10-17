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
  - /manage/ml/
  - /how-tos/train-deploy-ml/
  - /ml/deploy/
  - /ml/
  - /services/ml/deploy/
  - /how-tos/deploy-ml/
  - /manage/data/deploy-model/
date: "2025-10-09"
---

Use a machine learning (ML) model service to deploy an ML model to your machine.

## What is an ML model service?

An ML model service is a Viam service that runs machine learning models on your machine. The service works with models trained on Viam or elsewhere, and supports various frameworks including TensorFlow Lite, ONNX, TensorFlow, and PyTorch.

## Supported frameworks and hardware

Viam currently supports the following frameworks:

<!-- prettier-ignore -->
| Model Framework | ML Model Service | Hardware Support | Description |
| --------------- | --------------- | ------------------- | ----------- |
| [TensorFlow Lite](https://www.tensorflow.org/lite) | [`tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu) | linux/amd64, linux/arm64, darwin/arm64, darwin/amd64 | Quantized version of TensorFlow that has reduced compatibility for models but supports more hardware. Uploaded models must adhere to the [model requirements](https://app.viam.com/module/viam/tflite_cpu). |
| [ONNX](https://onnx.ai/) | [`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) |  Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64 | Universal format that is not optimized for hardware-specific inference but runs on a wide variety of machines. |
| [TensorFlow](https://www.tensorflow.org/) | [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64 | A full framework designed for more production-ready systems. |
| [PyTorch](https://pytorch.org/) | [`torch-cpu`](https://app.viam.com/module/viam/torch-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) | Nvidia GPU, linux/arm64, darwin/arm64 | A full framework that was built primarily for research. Because of this, it is much faster to do iterative development with (the model doesn't have to be predefined) but it is not as "production ready" as TensorFlow. It is the most common framework for open-source models because it is the go-to framework for ML researchers. |

{{< alert title="Note" color="note" >}}
For some ML model services, like the [Triton ML model service](https://github.com/viamrobotics/viam-mlmodelservice-triton/) for Jetson boards, you can configure the service to use either the available CPU or a dedicated GPU.
{{< /alert >}}

## Deploy your ML model

1. Navigate to the **CONFIGURE** tab of one of your machines.
2. Add an ML model service that supports the ML model you want to use.
   - For example, use the `ML model / TFLite CPU` service for TFlite ML models that you trained with Viam's built-in training.
3. Click **Select model** and select a model from your organization or the registry.
4. Save your config.
5. Use the **Test** panel to test your model.

### Available ML model services

{{<resources_svc api="rdk:service:mlmodel" type="ML model">}}

## Available machine learning models

You can use these publicly available machine learning models:

{{<mlmodels>}}

### Model sources

The service works with models from various sources:

- You can [train TensorFlow or TensorFlow Lite](/data-ai/train/train-tf-tflite/) or [other model frameworks](/data-ai/train/train/) on data from your machines.
- You can use [ML models](https://app.viam.com/registry?type=ML+Model) from the [registry](https://app.viam.com/registry).
- You can upload externally trained models from a model file on the [**MODELS** tab](https://app.viam.com/models).
- You can use models trained outside the Viam platform whose files are on your machine.
  See the documentation for the ML model service you're using (pick one that supports your model framework) for instructions on this.

{{< alert title="Add support for other models" color="tip" >}}
ML models must be designed in particular shapes to work with the `mlmodel` [classification](/operate/reference/services/vision/mlmodel/) or [detection](/operate/reference/services/vision/mlmodel/) models of Viam's [vision service](/operate/reference/services/vision/).
See [ML Model Design](/data-ai/reference/mlmodel-design/) to design a modular ML model service with models that work with vision.
{{< /alert >}}

### Deploy a specific version of an ML model

When you add a model to the ML model service in the app interface, it automatically uses the latest version.
In the ML model service panel, you can change the version in the version dropdown.
Save your config to use your specified version of the ML model.

## Next steps

On its own, the ML model service only runs the model.
After deploying your model, you need to configure an additional service to use the deployed model.
For example, you can configure an [`mlmodel` vision service](/operate/reference/services/vision/) to visualize the inferences your model makes.
Follow our docs to [run inference](/data-ai/ai/run-inference/) to add an `mlmodel` vision service and see inferences.

For other use cases, consider [creating custom functionality with a module](/operate/modules/support-hardware/).
