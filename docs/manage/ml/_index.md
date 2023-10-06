---
title: "Machine Learning"
linkTitle: "Machine Learning"
weight: 40
type: "docs"
tags: ["data management", "data", "services"]
no_list: true
description: "Use Viam's built-in machine learning capabilities to train image classification models and deploy these models to your robots."
# SME: Aaron Casas
---

Viam includes a built-in [machine learning (ML) service](/services/ml/) which provides your robot with the ability to learn from data and adjust its behavior based on insights gathered from that data.
Common use cases include:

- Object detection and classification which enable smart machines to detect people, animals, plants, or other objects with bounding boxes, and to perform actions when they are detected.
- Speech recognition, natural language processing, and speech synthesis, which enable smart machines to verbally communicate with us.

However, your robot can make use of machine learning with nearly any kind of data.

Viam natively supports [TensorFlow Lite](https://www.tensorflow.org/lite) ML models as long as your models adhere to the [model requirements](/services/ml/#tflite_cpu-limitations).

## Use machine learning with your smart machine

{{< cards >}}
{{% manualcard %}}

<h4>Train or upload an ML model</h4>

You can [add an existing model](/manage/ml/upload-model/) or [train your own models](/manage/ml/train-model/) for object detection and classification using data from the [data management service](../../services/data/).

{{% /manualcard %}}
{{% manualcard %}}

<h4>Deploy your ML model</h4>

To make use of ML models with your smart machine, use the built-in [ML model service](/services/ml/) to deploy and run the model.

{{% /manualcard %}}
{{% manualcard %}}

<h4>Configure a service</h4>

For object detection and classification, you can use the [vision service](/services/vision/), which provides an [ml model detector](/services/vision/detection/#configure-an-mlmodel-detector) and an [ml model classifier](/services/vision/classification/#configure-an-mlmodel-classifier) model.

For other usage, you can use a [modular resource](/extend/modular-resources/) to integrate it with your robot.

{{% /manualcard %}}
{{% manualcard %}}

<h4>Test your detector or classifier</h4>

Test your [`mlmodel detector`](/services/vision/detection/#test-your-detector) or [`mlmodel classifier`](/services/vision/classification/#test-your-classifier).

{{% /manualcard %}}

{{< /cards >}}

## Tutorials

{{< cards >}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Smart Pet Feeder" %}}
{{% card link="/extend/modular-resources/examples/tflite-module/" %}}
{{< /cards >}}
