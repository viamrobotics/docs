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

You can tag [images collected](../../../services/data/configure-data-capture/) by robots and use the labeled data to train a **Single Label** or **Multi Label** image classification model within Viam.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/CP14LR0Pq64">}}

## Label a dataset

To label a dataset, go to the [**DATA** tab](https://app.viam.com/data/view) in the Viam app.

![Add new model menu](../img/add-new-model.png)

On the **Images** subtab, you can filter available images, using the **Filtering** menu and select the attributes that match where, how, and when the data was collected.

{{< alert title="Important" color="note" >}}
Datasets are views, not materialized.
If the underlying data matching the filter changes because data is deleted or more data is added, the dataset will also change.

Therefore the data you are viewing may change as you label and train on the dataset.
{{< /alert >}}

If you would like to create a model that identifies an image of a star in a set of images, tag each image with a star with a `star` tag.

You can also optionally tag images without a star with a `notstar` tag.
This allows you to filter down the data in your dataset further by adding the explicit tags as a filter, for example `star` and `notstar`.

To tag an image, click on the image.
More information about the image will open up to the right side, including **Tags**.

![Information view of an image](../img/image-info.png)

Click on the **Tags** dropdown and create a new tag or select an existing tag to apply it to the image.

![Image tag menu](../img/image-tag.png)

Repeat this with all images in your dataset.

## Train a model

When you've tagged all the images click on the **TRAIN MODEL** button in the top right corner.

![Train model button](../img/train-model.png)

A **Training** side menu opens.
The model that you configure to be training will train on all images part of the current filter.

1. Select **New Model**.
2. Specify a **Model Name**.
3. Select a **Classification Type**:
    - **Single Label**: predicts one label per image
    - **Multi Label**: predicts multiple labels per image
4. Select one or more tags to train on.
    The selected tags will be the possible tags the model predicts for a given image.
     - If you selected **Single Label**, the model will predict one of these labels or `UNKNOWN`.
     - If you selected **Multi Label**, the model can predict one or more labels for each image.
4. Click **TRAIN MODEL**

![Train model menu](../img/train-model-menu.png)

The model now starts training and you can follow its process in the **Training** section of the **Models** page.

Once the model has finished training, it becomes visible in the **Models** section of the page.

![The trained model](../img/stars-model.png)

### Train a new version of a model

If you [deploy a model](../../../services/ml/) to a robot, Viam automatically assumes that this is the `latest` version of the model and that you would always like to deploy the `latest` version of the model to the robot.
If you train a new version of that model, Viam will automatically deploy the new version to the robot and replace the old version.

{{< alert title="Note" color="note" >}}
The previous model remains unchanged when you are training a new version of a model and is not used as input.
If you are training a new model, you need to again select the images to train on because the model will be built from scratch.
{{< /alert >}}

If you do not want Viam to automatically deploy the `latest` version of the model, you can change `packages` configuration in the [Raw JSON robot configuration](../../configuration/#the-config-tab).

You can get the version number from a specific model version by clicking on **COPY** on the model on the model page.
The model package config looks like this:

```json
{"package":"<model_id>/allblack","version":"1234567891011","name":"<model_name>"}
```

## Next Steps

To deploy your model to your robot, see [deploy model](../../../services/ml/).
