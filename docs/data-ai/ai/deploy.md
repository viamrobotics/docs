---
linkTitle: "Deploy model"
title: "Deploy a model"
weight: 40
layout: "docs"
type: "docs"
no_list: true
description: "Deploy an ML model to your machine."
---

To use an ML model on your machine, you need to deploy the model with an ML model service.
The ML model service will run the model.

## Deploy your ML model

Navigate to the **CONFIGURE** tab of one of your machine in the [Viam app](https://app.viam.com).
Add an ML model service that supports the ML model you trained or the one you want to use from the registry.
For example use the `ML model / TFLite CPU` service for TFlite ML models.
If you used the built-in training, this is the ML model service you need to use.
If you used a custom training script, you may need a different [ML model service](/services/ml/).

To deploy a model, click **Select model** and select the model from your organization or the registry.
Save your config.

On its own the ML model service only runs the model.
To use it to make inferences on a camera stream, you need to use it alongside a vision service.
Follow our docs to [run inference](/data-ai/ai/run-inference/) to add a vision service and make inferences.
