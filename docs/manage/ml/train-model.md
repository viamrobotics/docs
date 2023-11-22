---
title: "Train a Model"
linkTitle: "Train Model"
weight: 40
type: "docs"
tags: ["data management", "ml", "model training"]
images: ["/manage/ml/train-model.gif"]
webmSrc: "/manage/ml/train-model.webm"
mp4Src: "/manage/ml/train-model.mp4"
videoAlt: "Add a bounding box around the dog in an image."
aliases:
  - /manage/data/train-model/
description: "Train an image classification model on labeled image data."
# SME: Tahiya + Alexa Greenberg
---

You can add classification tags or bounding boxes to [images collected](/services/data/configure-data-capture/) by robots, add them to a dataset, and use the annotated data to train a **Single Label Classification Model**, **Multi Label Classification Model** or **Object Detection Model** within Viam.

When training machine learning models, it is important to supply a variety of different data about the subject.
In the case of image classification, it is important to provide images of the object being identified in different situations, such as from different angles or in different lighting situations.
The more varied the provided data set, the more accurate the resulting model becomes.

## Train a model

After [creating a dataset](/manage/data/dataset/), navigate to the **DATA** tab and the **DATASETS** subtab.
Then click on the dataset you want to train a model from and click on the **Train model** button on your dataset's page.

On the **Train a model** menu:

1. Enter a name for your new model.
1. Select a **Model Type** and one or more labels to train on:
   - **Single Label Classification**: The resulting model predicts one of the selected labels or `UNKNOWN` per image.
     If you are only using one label, ensure that the dataset you are training on also contains unlabeled images.
   - **Multi Label Classification**: The resulting model predicts one or more of the selected labels per image.
   - **Object Detection**: The resulting model predicts either no detected objects or any number of object labels alongside their locations per image.
1. Click **TRAIN MODEL**

{{<gif webm_src="/manage/ml/train-model.webm" mp4_src="/manage/ml/train-model.mp4" alt="Train a model UI">}}

The model now starts training and you can follow its process in the **Training** section of the **Models** page.

Once the model has finished training, it becomes visible in the **Models** section of the page.

![The trained model](/manage/ml/stars-model.png)

{{< alert title="Note" color="note" >}}

Your [dataset](/manage/data/dataset/) is not versioned.
You can add or remove data from it at any time.
Existing models will not change if you change the dataset they were trained on.
To iterate on your model and train on the a changed dataset, [train a new version of your model](#train-a-new-version-of-a-model).

{{< /alert >}}

### Train a new version of a model

If you [deploy a model](/services/ml/) to a robot, Viam automatically assumes that this is the `latest` version of the model and that you would always like to deploy the `latest` version of the model to the robot.
If you train a new version of that model, Viam will automatically deploy the new version to the robot and replace the old version.

{{< alert title="Important" color="note" >}}
The previous model remains unchanged when you are training a new version of a model and is not used as input.
If you are training a new model, you need to again go to your dataset's page and click on the **Train Model** button.
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
