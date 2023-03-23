---
title: "Deploy a Model"
linkTitle: "Deploy Model"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training"]
description: "Deploy an image classification model to a robot."
# SME: Aaron Casas
---

On the [**DATA** tab](https://app.viam.com/data/view) in the Viam app, navigate to the **MODELS** sub-tab.

![The trained model](../img/stars-model.png)

Click the **COPY** button to copy the model information.
The model information looks like this:

```json
{
    "package": "a1b23cde-fgh4-56i-j78k-l90123m45n6o/stars-model",
    "version": "1234567891011",
    "name": "stars-model"
}
```

Next, navigate to your robot's [**CONFIG** tab](https://app.viam.com/robot) and click on the **SERVICES** subtab.

Scroll to the bottom and create a new service with the **Type** `ml_models`.

![Create a machine learning models service](../img/ml-models-service.png)

The created ML Models panel lists all available models.

![Create a machine learning models service](../img/available-models.png)

To add a model to your robot, select it and click on the move right button.

![Create a machine learning models service](../img/added-model.png)

Finally, save the configuration and your model will be added to your robot at <file>/root/.viam/packages/<model-name></file>.

To make use of your new model, use the Vision Service and [add a classifier](../../vision/#classification) with the `model_path`.

Then you can test your classifier [similar to the steps in this tutorial](/tutorials/viam-rover/try-viam-color-detection/) or access the detections from the classifier [with code](/services/vision/#getting-started-with-vision-services-and-the-viam-sdk).
