---
title: "Upload a Model"
linkTitle: "Upload Model"
weight: 50
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
    - /manage/ml/upload-model
description: "Upload an image classification model to Viam."
# SME: Aaron Casas
---

On the [**DATA** tab](https://app.viam.com/data/view) in the Viam app, navigate to the **MODELS** sub-tab.

![Add new model](../img/add-new-model.png)

To add a new model:

1. Specify a **Name** for the model.
2. Add a `.tflite` model file.
3. Add a `.txt` label file.
4. Click **CREATE MODEL**.

The model now starts training and you can follow its process in the **Training** section of the page.

Once the model has finished training, it becomes visible in the **Models** section of the page.

![The trained model](../img/stars-model.png)

## Next Steps

To deploy your model to your robot, see [deploy model](../deploy-model).
