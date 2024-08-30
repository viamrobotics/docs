---
title: "Upload a Model to the Registry"
linkTitle: "Upload Model"
weight: 50
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/upload-model/
  - /manage/ml/upload-model/
  - /ml/upload-model/
description: "Upload a Machine Learning model to the Viam registry to use it with the ML Model service."
no_service: true
draft: true
# SME: Steven B.
---

## Upload a new model or new version

On the [**DATA** tab](https://app.viam.com/data/view) in the Viam app, navigate to the **MODELS** subtab.
Click **Upload model**.

{{<imgproc src="/services/ml/add-new-model.png" resize="400x" alt="Upload model menu on the DATA tab of the Viam app.">}}

Select if you want to upload a **New model** or a **New version** of a previously published model.

{{< tabs >}}
{{% tab name="New model" %}}

Select **Public** to upload the model publicly to the [Viam registry](https://app.viam.com/registry).
This makes the model usable by any external organization.
See [ML models in the registry](/registry/#ml-models) for more information.

Select **Private** to only publish the model for internal use within this {{< glossary_tooltip term_id="organization" text="organization" >}}.
Select **Next steps** to continue.

{{<imgproc src="/services/ml/upload-model.png" resize="900x" alt="Upload model menu on the DATA tab of the Viam app." style="max-width: 600px">}}

1. Select the **Model framework** or the type of model.
   TensorFlow Lite, TensorFlow, PyTorch, and ONNX model frameworks are currently supported.
2. Upload the files required for your model framework:
   - For a TensorFlow Lite or ONNX model framework, upload a `.txt` label file containing the label names you provided in training, with one name per line.
   - For a TensorFlow model framework, upload the model in the [SavedModel format](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/saved_model/README.md#the-savedmodel-format).
3. Specify a name for the model.
4. Specify the **Task type**.
5. Add a short description.
   This will help other users to understand how to use your model.

Select **Upload model**.
The model is now visible on the **MODELS** subtab of the **DATA** tab in the [Viam app](https://app.viam.com) and available to [deploy on your machine](/services/ml/deploy/).
Also, if you selected **Public**, it should be publicly visible in the [Viam registry](https://app.viam.com/registry).

{{% /tab %}}
{{% tab name="New version" %}}

{{<imgproc src="/services/ml/select-existing-model.png" resize="400x" alt="Select from your existing models.">}}

1. Select the model you would like to update from your existing models.
1. Click **Next steps** to continue.
1. Select the **Model framework** or the type of model.
   TensorFlow Lite, TensorFlow, PyTorch, and ONNX model frameworks are currently supported.
1. Upload the files required for your model framework:
   - For a TensorFlow Lite or ONNX model framework, upload a `.txt` label file containing the label names you provided in training, with one name per line.
   - For a TensorFlow model framework, upload the model in the [SavedModel format](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/saved_model/README.md#the-savedmodel-format).
1. Click **Upload model**.

Your model is now updated.

{{% alert title="Note" color="note" %}}

If you [deploy a model](/services/ml/) to a machine, Viam automatically assumes that this is the `latest` version of the model and that you would always like to deploy the `latest` version of the model to the machine.
If you upload a new version of that model, Viam will automatically deploy the new version to the machine and replace the old version.

If you do not want Viam to automatically deploy the `latest` version of the model, you can change the `packages` configuration in the [JSON machine configuration](/configure/#the-configure-tab).

You can get the version number from a specific model version by navigating to the [models page](https://app.viam.com/data/models), finding the model's row, clicking on the right-side menu marked with **_..._** and selecting **Copy package JSON**. For example: `2024-02-28T13-36-51`.
The model package config looks like this:

```json
{
  "package": "<model_id>/<model_name>",
  "version": "YYYY-MM-DDThh-mm-ss",
  "name": "<model_name>",
  "type": "ml_model"
}
```

{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

## Make an existing model public in the registry

To add a model that you've trained to the [Viam registry](https://app.viam.com/registry) so that other users can deploy it onto their robots:

1. On the [**DATA** tab](https://app.viam.com/data/view) in the Viam app, navigate to the **MODELS** subtab.
   You'll see a list of all ML models you have access to.
2. Open the menu on the right side of an ML model's row.

{{<imgproc src="/services/ml/model-list.png" resize="1000x" alt="List of models displayed on MODELS subtab of DATA tab.">}}

3. Then, click **Make public in Registry**.

{{<imgproc src="/services/ml/publish-model.png" resize="600x" alt="Publish model to registry action card.">}}

4. Add a short description.
   This will help other users to understand how to use your model.
5. Then, click **Publish model**.
   Your model is now publicly visible in the [Viam registry](https://app.viam.com/registry).

## Next steps

{{< cards >}}
{{% manualcard link="/services/ml/deploy/" %}}

<h4>Deploy your model</h4>

Create an ML model service to deploy your machine learning model to your machine.

{{% /manualcard %}}
{{% manualcard link="/services/vision/mlmodel/"%}}

<h4>Create a detector with your model</h4>

Configure your `mlmodel detector`.

{{% /manualcard %}}
{{% manualcard link="/services/vision/mlmodel/"%}}

<h4>Create a classifier with your model</h4>

Configure your `mlmodel classifier`.

{{% /manualcard %}}

{{< /cards >}}
