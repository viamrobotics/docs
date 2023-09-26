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
Common use cases include object detection, image classification, natural language processing, and speech recognition and synthesis, but your robot can make use of machine learning with nearly any kind of data.

Viam natively supports [TensorFlow Lite](https://www.tensorflow.org/lite) ML models as long as your models adhere to the [model requirements](/services/ml/#tflite_cpu-limitations).

You can [train your own image classification models](/manage/ml/train-model/) or [add an existing model](/manage/ml/upload-model/) for object detection and classification within the platform using data from the [data management service](../../services/data/).
Object detection and classification models are commonly used to enable robots to detect people, animals, plants, or other objects with bounding boxes, and to perform actions when they are detected.

To make use of ML models with your robot, you can use the built-in [ML model service](/services/ml/) to deploy and run the model.

Once you have [deployed the ML model service](/services/ml/#create-an-ml-model-service) to your robot, you can then add another service to make use of the model.

- For object detection and classification, you can use the [vision service](/services/vision/), which provides both [mlmodel detector](/services/vision/detection/#configure-an-mlmodel-detector) and [mlmodel classifier](/services/vision/classification/#configure-an-mlmodel-classifier) models.
- For other usage, you can create a [modular resource](/extend/modular-resources/) to integrate it with your robot.
  For an example, see [this tutorial](/extend/modular-resources/examples/tflite-module/) which adds a modular-resource-based service that uses TensorFlow Lite to classify audio samples.

The video below shows the training process for an object detection model using a bounding box:

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/CP14LR0Pq64">}}

## Next Steps

{{< cards >}}
{{% card link="/manage/ml/train-model" %}}
{{% card link="/manage/ml/upload-model" %}}
{{% card link="/services/ml" customTitle="Deploy Model" %}}
{{% card link="/tutorials/projects/pet-treat-dispenser/" customTitle="Tutorial: Smart Pet Feeder" %}}
{{% card link="/extend/modular-resources/examples/tflite-module/" %}}
{{< /cards >}}
