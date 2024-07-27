---
title: "Machine Learning"
linkTitle: "Machine Learning"
weight: 450
type: "docs"
tags: ["data management", "data", "services"]
no_list: true
description: "Use Viam's built-in machine learning capabilities to train image classification models and deploy these models to your machines."
images: ["/platform/ml.svg"]
aliases:
  - /manage/ml/
  - /ml/
# SME: Aaron Casas
---

{{<imgproc src="/services/ml/training.png" class="alignright" resize="400x" declaredimensions=true alt="ML training">}}

Machine learning (ML) provides your machines with the ability to adjust their behavior based on models that recognize patterns or make predictions.

Common use cases include:

- Object detection, which enables machines to detect people, animals, plants, or other objects with bounding boxes, and to perform actions when they are detected.
- Object classification, which enables machines to separate people, animals, plants, or other objects into predefined categories based on their characteristics, and to perform different actions based on the classes of objects.
- Speech recognition, natural language processing, and speech synthesis, which enable machines to verbally communicate with us.

For other use cases, consider [creating custom functionality with a module](/registry/create/).

Viam provides two services that enable machine learning capabilities: the [ML model](/services/ml/deploy/) service and the [Computer Vision](/services/vision/) service.

The ML model service deploys and runs a machine learning model, such as a TensorFlow or ONNX model, on your machine and makes its output accessible to other services.
For example, the [Computer Vision](/services/vision/mlmodel/) `mlmodel` service, which can detect or classify objects, is built to work with the inferences from an ML model service.
As a detector, the service uses these inferences to interpret image data from images on your computer or a [camera](/components/camera/), drawing bounding boxes around objects.
As a classifier, the service returns class labels and confidence score based off the [inferences](/services/ml/deploy/#infer) the underlying ML model makes from image data.

## Use machine learning with your machine

{{< cards >}}
{{< card link="/get-started/quickstarts/collect-data/" customTitle="Step 1: Collect data in 2 minutes" customDescription="Gather images from your machine." >}}
{{< card link="/use-cases/deploy-ml/" customTitle="Step 2: Label a dataset and train a model on it." >}}
{{< card link="/services/vision/mlmodel/" customTitle="Step 3: Deploy your model with the vision service." >}}
{{< /cards >}}

## Example tutorials

{{< cards >}}
{{% card link="/tutorials/services/data-mlmodel-tutorial/" %}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai/" customDescription="Add object detection, speech recognition, natural language processing, and speech synthesis capabilities to a machine." %}}
{{< /cards >}}

## Model support

You have four options when choosing a model to deploy onto an [ML model](/services/ml/deploy/) deployment service.
You can:

- [train a model on the Viam app](/services/ml/train-model/) and deploy it
- deploy a pre-trained model another user has published from [the registry](https://app.viam.com/registry)
- [upload](/services/ml/upload-model/) a model trained outside the Viam platform to the registry privately or publicly and deploy it
- deploy a model trained outside the Viam platform that's already available on your machine

The model you use must be supported on the Viam platform.
Viam supports the following model frameworks:

- [TensorFlow Lite](https://www.tensorflow.org/lite) (as long as your models adhere to the [model requirements](/services/ml/deploy/tflite_cpu/#model-requirements)): with the [`tflite_cpu` ML model service](/services/ml/deploy/)
- [TensorFlow](https://www.tensorflow.org/): with the [`triton` ML model service](https://github.com/viamrobotics/viam-mlmodelservice-triton)
- [PyTorch](https://pytorch.org/): with the [`triton` ML model service](https://github.com/viamrobotics/viam-mlmodelservice-triton)
- [ONNX](https://onnx.ai/): with the [`onnx_cpu` ML model service](https://github.com/viam-labs/onnx-cpu)

For more information, see [Model framework support](/services/ml/upload-model/#model-framework-support).
