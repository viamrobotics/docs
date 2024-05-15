---
title: "Train a Model"
linkTitle: "Train Model"
weight: 40
type: "docs"
tags: ["data management", "ml", "model training"]
images: ["/app/ml/train-model.gif"]
videos: ["/app/ml/train-model.webm","/app/ml/train-model.mp4"]
videoAlt: "Add a bounding box around the dog in an image."
aliases:
  - /app/data/train-model/
description: "Train an image classification model on labeled image data."
aliases:
  - /manage/app/ml/train-model/
# SME: Tahiya + Alexa Greenberg
---

You can add classification tags or bounding boxes to [images collected](/app/data/capture/) by machines, add them to a dataset, and use the annotated data to train a **Single Label Classification Model**, **Multi Label Classification Model** or **Object Detection Model** within Viam.

When training machine learning models, it is important to supply a variety of different data about the subject.
In the case of image classification, it is important to provide images of the object being identified in different situations, such as from different angles or in different lighting situations.
The more varied the provided data set, the more accurate the resulting model becomes.

## Train a model

After [creating a dataset](/app/data/dataset/), navigate to the **DATA** tab and the **DATASETS** subtab.
Then click on the dataset you want to train a model from and click on the **Train model** button on your dataset's page.

On the **Train a model** menu:

1. Enter a name or use the suggested name for your new model.
1. Select a **Model Type** and one or more labels to train on:
   - **Single Label Classification**: The resulting model predicts one of the selected labels or `UNKNOWN` per image.
     If you are only using one label, ensure that the dataset you are training on also contains unlabeled images.
   - **Multi Label Classification**: The resulting model predicts one or more of the selected labels per image.
   - **Object Detection**: The resulting model predicts either no detected objects or any number of object labels alongside their locations per image.
1. Click **TRAIN MODEL**

{{<gif webm_src="/app/ml/train-model.webm" mp4_src="/app/ml/train-model.mp4" alt="Train a model UI">}}

The model now starts training and you can follow its process in the **Training** section of the **Models** page.

Once the model has finished training, it becomes visible in the **Models** section of the page.

![The trained model](/app/ml/petfeeder-model.png)

{{< alert title="Note" color="note" >}}

Your [dataset](/app/data/dataset/) is not versioned.
You can add or remove data from it at any time.
Existing models will not change if you change the dataset they were trained on.
To iterate on your model and train on the a changed dataset, [train a new version of your model](#train-a-new-version-of-a-model).

{{< /alert >}}

### Train a new version of a model

If you [deploy a model](/ml/) to a machine, Viam automatically assumes that this is the `latest` version of the model and that you would always like to deploy the `latest` version of the model to the machine.
If you train a new version of that model, Viam will automatically deploy the new version to the machine and replace the old version.

{{< alert title="Important" color="note" >}}
The previous model remains unchanged when you are training a new version of a model and is not used as input.
If you are training a new model, you need to again go to your dataset's page and click on the **Train Model** button.
{{< /alert >}}

If you do not want Viam to automatically deploy the `latest` version of the model, you can change `packages` configuration in the [JSON machine configuration](/machine/configure/#the-configure-tab).

You can get the version number from a specific model version by navigating to the [models page](https://app.viam.com/app/data/models) finding the model's row, clicking on the right-side menu marked with **_..._** and selecting **Copy package JSON**. For example: `2024-02-28T13-36-51`.
The model package config looks like this:

```json
{
  "package": "<model_id>/<model_name>",
  "version": "YYYY-MM-DDThh-mm-ss",
  "name": "<model_name>",
  "type": "ml_model"
}
```

## Delete a model

You can delete a model from the [models page](https://app.viam.com/app/data/models) in the Viam app:

- To delete a trained model, click the **_..._** icon to the right of the model name under the **Models** section of the page, and select **Delete**.

  ![Delete a trained model](/app/ml/delete-trained-model.png)

- To delete a model that has failed training, click the trash can icon to the right of the model name under the **Training** section of the page.

  ![Delete a failed model](/app/ml/delete-failed-model.png)

## Next steps

{{< cards >}}
{{% manualcard link="/app/ml/" %}}

<h4>Deploy your model</h4>

Create an ML model service to deploy your machine learning model to your machine.

{{% /manualcard %}}
{{% manualcard link="/machine/services/vision/mlmodel/"%}}

<h4>Create a detector with your model</h4>

Configure an `mlmodel detector`.

{{% /manualcard %}}
{{% manualcard link="/machine/services/vision/mlmodel/"%}}

<h4>Create a classifier with your model</h4>

Configure your `mlmodel classifier`.

{{% /manualcard %}}

{{< /cards >}}
