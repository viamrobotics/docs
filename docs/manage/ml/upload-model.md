---
title: "Upload a Model"
linkTitle: "Upload Model"
weight: 50
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/upload-model/
description: "Upload an image classification model to Viam."
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

#### Naming your model: namespace:repo-name:name

If you are [creating a custom module](/modular-resources/create/) and want to [upload that module](/modular-resources/upload/) to the Viam registry, ensure your model name meets the following requirements:

- The namespace of your model **must** match the [namespace of your organization](/manage/fleet/organizations/#create-a-namespace-for-your-organization).
  For example, if your organization uses the `acme` namespace, your models must all begin with `acme`, like `acme:demo:mybase`.
- Your model triplet must be all-lowercase.
- Your model triplet may only use alphanumeric (`a-z` and `0-9`), hyphen (`-`), and underscore (`_`) characters.

For the middle segment of your model triplet `repo-name`, use the name of the git repository where you store your module's code.
The `repo-name` should describe the common functionality provided across the model or models of that module.

For example:

- The `rand:yahboom:arm` model and the `rand:yahboom:gripper` model uses the repository name [yahboom](https://github.com/viam-labs/yahboom).
  The models implement the `rdk:component:arm` and the `rdk:component:gripper` API to support the Yahboom DOFBOT arm and gripper, respectively.
- The `viam-labs:audioout:pygame` model uses the repository name [audioout](https://github.com/viam-labs/audioout)
  It implements the custom API `viam-labs:service:audioout`.

The `viam` namespace is reserved for models provided by Viam.

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

Create an ML model service to deploy your machine learning model to your smart machine.

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
