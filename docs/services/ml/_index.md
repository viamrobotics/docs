---
title: "ML Model Service"
linkTitle: "ML Model"
weight: 30
type: "docs"
tags: ["data management", "ml", "model training"]
aliases:
  - /manage/data/deploy-model/
  - /services/ml/
  - /ml/deploy/
  - /services/ml/deploy/
  - /manage/ml/
  - /ml/
description: "Deploy machine learning models to a machine and use the vision service to detect or classify images or to create point clouds of identified objects."
modulescript: true
hide_children: true
icon: true
no_list: true
images: ["/platform/ml.svg"]
date: "2024-09-03"
# updated: ""  # When the content was last entirely checked
# SME: Aaron Casas
---

Machine learning (ML) provides your machines with the ability to adjust their behavior based on models that recognize patterns or make predictions.

Common use cases include:

- Object detection, which enables machines to detect people, animals, plants, or other objects with bounding boxes, and to perform actions when they are detected.
- Object classification, which enables machines to separate people, animals, plants, or other objects into predefined categories based on their characteristics, and to perform different actions based on the classes of objects.
- Speech recognition, natural language processing, and speech synthesis, which enable machines to verbally communicate with us.

The Machine Learning (ML) model service allows you to deploy [machine learning models](/registry/ml-models/) to your machine.
The service works with models trained inside and outside the Viam app:

- You can [train](/how-tos/train-deploy-ml/) models on data from your machines.
- You can upload externally trained models on the [**MODELS** tab](https://app.viam.com/data/models) in the **DATA** section of the Viam app.
- You can use [ML models](https://app.viam.com/registry?type=ML+Model) from the [Viam Registry](https://app.viam.com/registry).
- You can use a [model](/registry/ml-models/) trained outside the Viam platform whose files are on your machine.

## Configuration

You must deploy an ML model service to use machine learning models on your machines.
Once you have deployed the ML model service, you can select an [ML model](#machine-learning-models-from-registry).

After deploying your model, you need to configure an additional service to use the deployed model.
For example, you can configure an [`mlmodel` vision service](/services/vision/) to visualize the predictions your model makes.
For other use cases, consider [creating custom functionality with a module](/how-tos/create-module/).

{{<resources_svc api="rdk:service:mlmodel" type="ML model">}}

{{< alert title="Add support for other models" color="tip" >}}
ML models must be designed in particular shapes to work with the `mlmodel` [classification](/services/vision/mlmodel/) or [detection](/services/vision/mlmodel/) model of Viam's [vision service](/services/vision/).
See [ML Model Design](/registry/advanced/mlmodel-design/) to design modular ML model service with models that work with vision.
{{< /alert >}}

{{< alert title="Note" color="note" >}}
For some models of the ML model service, like the [Triton ML model service](https://github.com/viamrobotics/viam-mlmodelservice-triton/tree/main/) for Jetson boards, you can configure the service to use either the available CPU or a dedicated GPU.
{{< /alert >}}

## Machine learning models from registry

You can search the machine learning models that are available to deploy on this service from the registry here:

{{<mlmodels>}}

## API

The [ML model service API](/appendix/apis/services/ml/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/mlmodel-table.md" >}}

## Next steps

The ML model service only runs your model on the machine.
To use the inferences from the model, you must use an additional service such as a [vision service](/services/vision/):

{{< cards >}}
{{% manualcard link="/services/vision/mlmodel/" title="Create a visual detector or classifier" noimage="True" %}}

Use your model deployed with the ML model service by adding a vision service that can provide detections or classifications depending on your ML model.

{{% /manualcard %}}
{{% card link="/how-tos/train-deploy-ml/" noimage="True" %}}
{{% card link="/how-tos/detect-people/" customTitle="Detect people" noimage="true" %}}

{{< /cards >}}
