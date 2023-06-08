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

Machine learning is an approach to programming where you provide an algorithm with a large data set, and train it to discover patterns in that data on its own.
The more data you provide to it, the better it becomes at identifying patterns across that data set, and the more accurate it becomes at guessing characteristics of any new data provided.

For example, say you have a collection of pictures of your cat.
As you train your algorithm on just a few pictures, it might not be able to determine that a picture of your cat's face and a picture of your cat sleeping are the same cat.
As you train the algorithm on more and more pictures, it might be able to recognize your cat from any angle, or to differentiate between multiple different cats.

You can use Viam's built-in machine learning capabilities to [train image classification models](train-model/) and [deploy these models to your robots](../../services/ml/).
You can also [upload and use existing models](upload-model/).

To capture and synchronize data to the platform, see [Data Management Service](../../services/data/).
To view or export captured data, see [Data Management](../data/).

## Next Steps

{{< cards >}}
  {{% card link="/manage/ml/train-model" size="small" %}}
  {{% card link="/manage/ml/upload-model" size="small" %}}
  {{% card link="/services/ml" size="small" custom="Deploy Model" %}}
{{< /cards >}}
