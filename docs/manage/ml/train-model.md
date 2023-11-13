---
title: "Train a Model"
linkTitle: "Train Model"
weight: 40
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/train-model/
description: "Train an image classification model on labeled image data."
# SME: Aaron Casas
---

You can label or add bounding boxes to [images collected](/services/data/configure-data-capture/) by robots and use the annotated data to train a **Single Label Classification Model**, **Multi Label Classification Model** or **Object Detection Model** within Viam.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/CP14LR0Pq64">}}

When training machine learning models, it is important to supply a variety of different data about the subject.
In the case of image classification, it is important to provide images of the object being identified in different situations, such as from different angles or in different lighting situations.
The more varied the provided data set, the more accurate the resulting model becomes.

## Train a model

After [annotating your images](/manage/data/label/), click on the **TRAIN MODEL** button in the top right corner.

![Train model button](/manage/ml/train-model.png)

A **Training** side menu opens.
The model will train on all images that are part of the current filter.

{{< alert title="Info" color="info" >}}
Filtered datasets are views and not materialized.
That means the data you are viewing may change as you label and train on the dataset.
If the underlying data matching the filter changes because data is deleted or more data is added, the dataset will also change.
{{< /alert >}}

1. Select **New Model**.
2. Specify a **Model Name**.
3. Select a **Model Type** and one or more labels to train on:
   - **Single Label Classification**: The resulting model predicts one of the selected labels or `UNKNOWN` per image.
     If you are only using one label, ensure that the dataset you are training on also contains unlabeled images.
   - **Multi Label Classification**: The resulting model predicts one or more of the selected labels per image.
   - **Object Detection**: The resulting model predicts either no detected objects or any number of object labels alongside their locations per image.
4. Click **TRAIN MODEL**

![Train model menu](/manage/ml/train-model-menu.png)

The model now starts training and you can follow its process in the **Training** section of the **Models** page.

Once the model has finished training, it becomes visible in the **Models** section of the page.

![The trained model](/manage/ml/stars-model.png)

### Train a new version of a model

If you [deploy a model](/services/ml/) to a robot, Viam automatically assumes that this is the `latest` version of the model and that you would always like to deploy the `latest` version of the model to the robot.
If you train a new version of that model, Viam will automatically deploy the new version to the robot and replace the old version.

{{< alert title="Important" color="note" >}}
The previous model remains unchanged when you are training a new version of a model and is not used as input.
If you are training a new model, you need to again select the images to train on because the model will be built from scratch.
{{< /alert >}}

If you do not want Viam to automatically deploy the `latest` version of the model, you can change `packages` configuration in the [Raw JSON robot configuration](/manage/configuration/#the-config-tab).

You can get the version number from a specific model version by clicking on **COPY** on the model on the model page.
The model package config looks like this:

```json
{
  "package": "<model_id>/allblack",
  "version": "YYYYMMDDHHMMSS",
  "name": "<model_name>"
}
```

## Next Steps

{{< cards >}}
{{% manualcard link="/services/ml/" %}}

<h4>Deploy your model</h4>

Create an ML model service to deploy your machine learning model to your machine.

{{% /manualcard %}}
{{% manualcard link="/services/vision/detection/#configure-an-mlmodel-detector"%}}

<h4>Create a detector with your model</h4>

Configure an `mlmodel detector`.

{{% /manualcard %}}
{{% manualcard link="/services/vision/classification/#configure-an-mlmodel-classifier"%}}

<h4>Create a classifier with your model</h4>

Configure your `mlmodel classifier`.

{{% /manualcard %}}

{{< /cards >}}
