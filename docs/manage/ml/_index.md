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

You can [add existing models](/manage/ml/upload-model/) or [train image classification models](/manage/ml/train-model/) for object detection and classification within the platform using data from the [Data Management Service](../../services/data/).
Training detection and classification models enables robots to detect people, animals, plants or other objects with bounding boxes and perform actions when they are detected.

To make use of ML models with your robot, you can use the built-in [ML model service](/services/ml/) to deploy and run the model.

### Object detection and classification

Once you have [deployed the ML model service](/services/ml/#create-an-ml-model-service) for your robot, you can then add another service to make use of the model.

* For object detection and classification you can use the [Vision Service](/services/vision) [mlmodel detector](https://docs.viam.com/services/vision/detection/#configure-a-mlmodel-detector) or [mlmodel classifier](https://docs.viam.com/services/vision/classification/#configure-a-mlmodel-classifier).
* For other usage, you can create a [modular resource](/program/extend/modular-resources/) to integrate it with your robot.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/CP14LR0Pq64">}}

## Next Steps

{{< cards >}}
  {{% card link="/manage/ml/train-model" size="small" %}}
  {{% card link="/manage/ml/upload-model" size="small" %}}
  {{% card link="/services/ml" size="small" custom="Deploy Model" %}}
  {{% card link="/tutorials/projects/pet-treat-dispenser/" size="small" custom="Tutorial: Smart Pet Feeder" %}}
{{< /cards >}}
