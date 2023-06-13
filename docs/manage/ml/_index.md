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

Viam natively supports [TensorFlow Lite](https://www.tensorflow.org/lite) ML models, but you can use other models as well as long as your models adhere to the [model requirements](/services/ml/#tflite_cpu-limitations).

To make use of ML models with your robot, you can use the built-in ML model service to train image classification models for object detection and classification or create a [modular resource](/program/extend/modular-resources/) to integrate it with your robot.

### Object detection and classification

Once you have [created the ML model service](/services/ml/#create-an-ml-model-service) for your robot, you can [train image classification models](train-model/) to enable it to detect people, animals, plants or other objects with bounding boxes and perform actions when they are detected.

![Gif of a dog being labeled](/tutorials/img/pet-treat-dispenser/app-data-images.png)

When training machine learning models, it is important to supply a variety of different data about the subject. In the case of object detection, it is important to provide images of the object in different situations, such as from different angles or in different lighting situations. The more varied the provided data set, the more accurate the resulting model becomes.

You can also [upload and use existing models](upload-model/).

To capture and synchronize data to the platform, see [Data Management Service](../../services/data/).
To view or export captured data, see [Data Management](../data/).

## Next Steps

{{< cards >}}
  {{% card link="/manage/ml/train-model" size="small" %}}
  {{% card link="/manage/ml/upload-model" size="small" %}}
  {{% card link="/services/ml" size="small" custom="Deploy Model" %}}
  {{% card link="/tutorials/projects/pet-treat-dispenser/" size="small" custom="Tutorial: Smart Pet Feeder" %}}
{{< /cards >}}
