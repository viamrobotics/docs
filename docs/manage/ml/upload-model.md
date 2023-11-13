---
title: "Upload a Model"
linkTitle: "Upload Model"
weight: 50
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/upload-model/
description: "Upload a Machine Learning model to Viam to use it with the ML Model service."
# SME: Aaron Casas
---

On the [**DATA** tab](https://app.viam.com/data/view) in the Viam app, navigate to the **Models** subtab.

![Add new model](/manage/ml/add-new-model.png)

To add a new model:

1. Specify a **Name** for the model.
2. Add a `.tflite` model file.
3. Add a `.txt` label file.
4. Click **CREATE MODEL**.

The model now starts training and you can follow its process in the **Training** section of the page.

Once the model has finished training, it becomes visible in the **Models** section of the page.

![The trained model](/manage/ml/stars-model.png)

### Upload a new version of a model

If you [deploy a model](/services/ml/) to a robot, Viam automatically assumes that this is the `latest` version of the model and that you would always like to deploy the `latest` version of the model to the robot.
If you upload a new version of that model, Viam will automatically deploy the new version to the robot and replace the old version.

If you do not want Viam to automatically deploy the `latest` version of the model, you can change the `packages` configuration in the [Raw JSON robot configuration](/manage/configuration/#the-config-tab).

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

Configure your `mlmodel detector`.

{{% /manualcard %}}
{{% manualcard link="/services/vision/classification/#configure-an-mlmodel-classifier"%}}

<h4>Create a classifier with your model</h4>

Configure your `mlmodel classifier`.

{{% /manualcard %}}

{{< /cards >}}
