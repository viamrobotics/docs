---
title: "Deploy an ML Model with the ML Model Service"
linkTitle: "ML Model Service"
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

The Machine Learning (ML) model service allows you to deploy [machine learning models](/services/ml/ml-models/) to your machine.
You can deploy:

- a model you [trained](/how-tos/deploy-ml/)
- a model from [the registry](https://app.viam.com/registry) that another user has shared publicly
- a model trained outside the Viam platform that you have uploaded to the [**MODELS** tab](https://app.viam.com/data/models) in the **DATA** section of the Viam app
- a model trained outside the Viam platform that's already available on your machine

After deploying your model, you need to configure an additional service to use the deployed model.
For example, you can configure an [`mlmodel` vision service](/services/vision/) to visualize the predictions your model makes.

## Available ML model service models

You must deploy an ML model service to use machine learning models on your machines.
Once you have deployed the ML model service, you can select an [ML model](#machine-learning-models-from-registry).

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

## Machine learning models from registry

You can search the machine learning models that are available to deploy on this service from the registry here:

{{<mlmodels>}}

## API

{{< alert title="Viam Python SDK Support" color="note" >}}

To use the ML model service from the [Viam Python SDK](https://python.viam.dev/), install the Python SDK using the `mlmodel` extra:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[mlmodel]'
```

{{< /alert >}}

The MLModel service supports the following methods:

{{< readfile "/static/include/services/apis/generated/mlmodel-table.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with an `MLModel` service, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **CONNECT** tab's **Code sample** page on the [Viam app](https://app.viam.com) for sample code to connect to your machine.

{{% /alert %}}

{{< readfile "/static/include/services/apis/generated/mlmodel.md" >}}

## Next steps

The ML model service only runs your model on the machine.
To use the inferences from the model, you must use an additional service such as a [vision service](/services/vision/) or a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}}:

{{< cards >}}

{{% manualcard link="/services/vision/mlmodel/" img="/services/icons/ml.svg" alt="Machine Learning" %}}
**Create a visual detector or classifier**

Use your model deployed with the ML model service by adding a vision service that can provide detections or classifications depending on your ML model.

{{% /manualcard %}}

{{% card link="/registry/examples/tflite-module/" customTitle="Example: TensorFlow Lite Modular Service" %}}

{{< /cards >}}
