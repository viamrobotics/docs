---
title: "Machine Learning"
linkTitle: "Machine Learning"
weight: 30
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

<p>
{{<imgproc src="/services/ml/training.png" class="alignright" resize="400x" declaredimensions=true alt="ML training">}}
</p>

Machine learning (ML) provides your machines with the ability to adjust their behavior based on models that recognize patterns or make predictions.

Common use cases include:

- Object detection, which enables machines to detect people, animals, plants, or other objects with bounding boxes, and to perform actions when they are detected.
- Object classification, which enables machines to separate people, animals, plants, or other objects into predefined categories based on their characteristics, and to perform different actions based on the classes of objects.
- Speech recognition, natural language processing, and speech synthesis, which enable machines to verbally communicate with us.

Viam provides two services that together enable visual machine learning capabilities: the [ML model](/services/ml/deploy/) service and the [Computer Vision](/services/vision/) service.
For other use cases, consider [creating custom functionality with a module](/how-tos/create-module/).

## Machine learning models

Machine Learning (ML) models are mathematical models that can recognize patterns.
Currently Viam supports TensorFlow Lite, TensorFlow, ONNX, and PyTorch.

- You can upload externally trained models on the [**MODELS** tab](https://app.viam.com/data/models) in the **DATA** section of the Viam app.
- You can [train](/how-tos/deploy-ml/) models on data from your machines using different training scripts.
- You can use [ML models from the Viam Registry](https://app.viam.com/registry?type=ML+Model).
- You can use a [model](/services/ml/ml-models/) trained outside the Viam platform that's already available on your machine.

For more information, see [ML Models](/services/ml/ml-models/) and [Training Scripts](/services/ml/training-scripts/).

{{< cards >}}
{{% card link="/services/ml/ml-models/" %}}
{{% card link="/services/ml/training-scripts/" %}}
{{< /cards >}}

## ML Model service

The ML model service deploys and runs a machine learning model, such as a TensorFlow or ONNX model, on your machine and makes its output accessible to other services.
For example, the [Computer Vision](/services/vision/mlmodel/) `mlmodel` service, which can detect or classify objects, is built to work with the inferences from an ML model service.
As a detector, the service uses these inferences to interpret image data from images on your computer or a [camera](/components/camera/), drawing bounding boxes around objects.
As a classifier, the service returns class labels and confidence score based off the [inferences](/services/ml/deploy/#infer) the underlying ML model makes from image data.

## Next steps

For comprehensive guides on using data capture and synchronization together with the ML model service, see:

{{< cards >}}
{{% card link="/how-tos/image-data/" %}}
{{% card link="/how-tos/deploy-ml/" %}}
{{< /cards >}}

You can also follow one of these tutorials to see ML models in action:

{{< cards >}}
{{% card link="/tutorials/projects/helmet/" %}}
{{% card link="/tutorials/services/color-detection-scuttle/" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai/" customDescription="Add object detection, speech recognition, natural language processing, and speech synthesis capabilities to a machine." %}}
{{< /cards >}}
