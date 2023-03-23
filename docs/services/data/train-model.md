---
title: "Train a Model"
linkTitle: "Train Model"
weight: 40
type: "docs"
tags: ["data management", "ml", "model training"]
description: "Train an image classification model on labeled image data."
# SME: Aaron Casas
---

You can tag [images collected](../configure-data-capture) by robots and use the labeled data to train an image classification model within Viam.

## Label a dataset

To label a dataset, go to the [**DATA** tab](https://app.viam.com/data/view) in the Viam app.

![Add new model menu](../img/add-new-model.png)

On the **IMAGES** sub-tab, you can filter available images, using the **FILTERING** menu and select the attributes that match where, how, and when the data was collected.

If you would like to create a model that identifies an image of a star in a set of images, tag each image with `star` or `notstar` respectively.

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

1. Select **NEW MODEL**.
2. Specify a **Model Name**.
3. Select a **Classification Type**: either **Single Label** or **Multi Label**.
3. Select one or more tags to train on.
4. Click **TRAIN MODEL**

![Train model menu](../img/train-model-menu.png)

The model now starts training and you can follow its process in the **Training** section of the **MODELS** page.

Once the model has finished training, it becomes visible in the **Models** section of the page.

![The trained model](../img/stars-model.png)


## Next Steps

To deploy your model to your robot, see [deploy model](../deploy-model).
