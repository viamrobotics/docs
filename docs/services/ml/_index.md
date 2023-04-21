---
title: "ML Model Service"
linkTitle: "ML Model"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/deploy-model/
description: "Deploy Machine Learning models to a robot."
# SME: Aaron Casas
---

The ML Models service allows you to deploy machine learning models to your robots.

## Create an ML model service

Navigate to your robot's [**config** tab](https://app.viam.com/robot) and click on the **Services** subtab.

Scroll to the bottom and create a new service with the **Type** `mlmodel` and the **Model** `tflite_cpu`.

![Create a machine learning models service](../img/ml-models-service.png)

You can choose to configure your service with an existing model on the robot or deploy a model onto your robot:

{{< tabs >}}
{{% tab name="Existing Model" %}}

To configure your service with an existing model on the robot, select **Path to Existing Model On Robot** for the **Deployment** field.

Then specify the **Model Path** and any **Optional Settings** such as the **Label Path** and the **Number of threads**.

![Create a machine learning models service with an existing model](../img/available-models.png)

{{% /tab %}}
{{% tab name="Deploy Model" %}}

To configure your service and deploy a model onto your robot, select **Deploy Model On Robot** for the **Deployment** field.

Then select the **Models** and any **Optional Settings** such as the **Number of threads**.

![Create a machine learning models service with a model to be deployed](../img/deploy-model.png)

{{% /tab %}}
{{< /tabs >}}

Save the configuration and your model will be added to your robot at <file>$HOME/.viam/packages/\<model-name\>/\<file-name\></file>.

{{< alert title="Note" color="note" >}}
If you upload or train a new version of a model, Viam automatically deploys the `latest` version of the model to the robot.
If you do not want Viam to automatically deploy the `latest` version of the model, you can change the  `packages` configuration in the [Raw JSON robot configuration](../../manage/configuration/#the-config-tab).
{{< /alert >}}

You can get the version number from a specific model version by clicking on **COPY** on the model on the models tab of the **DATA** page.
The model package config looks like this:

```json
{"package":"<model_id>/allblack","version":"1234567891011","name":"<model_name>"}
```

## Next Steps

To make use of your new model, follow the instructions to create a detector or a classifier:

- A [`tflite_cpu` detector](../vision/detection/#configure-a-tflite_cpu-detector)
- A [`tflite_cpu` classifier](../vision/classification/#configure-a-tflite_cpu-classifier)
