---
title: "Deploy an ML Model with the ML Model Service"
linkTitle: "Deploy Model"
weight: 60
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/deploy-model/
  - /services/ml/
  - /ml/deploy/
description: "Deploy machine learning models to a machine and use the vision service to detect or classify images or to create point clouds of identified objects."
modulescript: true
hide_children: true
icon: true
no_list: true
images: ["/services/icons/ml.svg"]
# SME: Aaron Casas
---

The Machine Learning (ML) model service allows you to deploy machine learning models to your machine.
This can mean deploying:

- a model you [trained](/services/ml/train-model/)
- a model from [the registry](https://app.viam.com/registry) that another user has shared publicly
- a model trained outside the Viam platform that you have [uploaded](/services/ml/upload-model/) to the registry privately or publicly
- a model trained outside the Viam platform that's already available on your machine

After deploying your model, you need to configure an additional service to use the deployed model.
For example, you can configure an [`mlmodel` vision service](/services/vision/) and a [`transform` camera](/components/camera/transform/) to visualize the predictions your model makes.

## Supported models

{{<resources_svc api="rdk:service:mlmodel" type="ML model">}}

{{< alert title="Add support for other models" color="tip" >}}
If none of the existing models of the ML model service fit your use case, you can create a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} to add support for it.

ML models must be designed in particular shapes to work with the `mlmodel` [classification](/services/vision/mlmodel/) or [detection](/services/vision/mlmodel/) model of Viam's [vision service](/services/vision/).
Follow [these instructions](/registry/advanced/mlmodel-design/) to design your modular ML model service with models that work with vision.
{{< /alert >}}

{{< alert title="Note" color="note" >}}
For some models of the ML model service, like the [Triton ML model service](https://github.com/viamrobotics/viam-mlmodelservice-triton/tree/main/) for Jetson boards, you can configure the service to use either the available CPU or a dedicated GPU.
{{< /alert >}}

## Used with

{{< cards >}}
{{< relatedcard link="/services/vision/">}}
{{< relatedcard link="/components/board/">}}
{{< relatedcard link="/components/camera/">}}
{{< /cards >}}

## Models from registry

You can search the machine learning models that are available to deploy on this service from the registry here:

<div id="searchboxML"></div>
<p>
<div id="searchstatsML"></div></p>
<div class="mr-model" id="">
  <div class="modellistheader">
    <div class="name">Model</div>
    <div>Description</div>
  </div>
<div id="hitsML" class="modellist">
</div>
<div id="paginationML"></div>
</div>

## Versioning for deployed models

If you upload or train a new version of a model, Viam automatically deploys the `latest` version of the model to the machine.
If you do not want Viam to automatically deploy the `latest` version of the model, you can edit the `"packages"` array in the [JSON configuration](/build/configure/#the-configure-tab) of your machine.
This array is automatically created when you deploy the model and is not embedded in your service configuration.

You can get the version number from a specific model version by navigating to the [models page](https://app.viam.com/data/models) finding the model's row, clicking on the right-side menu marked with **_..._** and selecting **Copy package JSON**. For example: `2024-02-28T13-36-51`.
The model package config looks like this:

```json
"packages": [
  {
    "package": "<model_id>/<model_name>",
    "version": "YYYY-MM-DDThh-mm-ss",
    "name": "<model_name>",
    "type": "ml_model"
  }
]
```

## API

The MLModel service supports the following methods:

{{< readfile "/static/include/services/apis/generated/mlmodel-table.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with an `MLModel` service, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **CONNECT** tab's **Code sample** page on the [Viam app](https://app.viam.com) for boilerplate code to connect to your machine.

{{% /alert %}}

{{< readfile "/static/include/services/apis/generated/mlmodel.md" >}}

## Use the ML model service with the Viam Python SDK

To use the ML model service from the [Viam Python SDK](https://python.viam.dev/), install the Python SDK using the `mlmodel` extra:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[mlmodel]'
```

You can also run this command on an existing Python SDK install to add support for the ML model service.

See the [Python documentation](https://python.viam.dev/autoapi/viam/services/mlmodel/mlmodel/index.html#viam.services.mlmodel.mlmodel.MLModel) for more information about the `MLModel` service in Python.

See [Program a machine](/build/program/) for more information about using an SDK to control your machine.

## Next steps

To use your model with your machine, add a [vision service](/services/vision/) or a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}:

{{< cards >}}

{{% manualcard link="/services/vision/mlmodel/"%}}

<h4>Create a detector with your model</h4>

Configure an `mlmodel detector`.

{{% /manualcard %}}
{{% manualcard link="/services/vision/mlmodel/"%}}

<h4>Create a classifier with your model</h4>

Configure your `mlmodel classifier`.

{{% /manualcard %}}

{{% card link="/registry/examples/tflite-module/" customTitle="Example: TensorFlow Lite Modular Service" %}}

{{< /cards >}}
