---
title: "Browse ML Models"
linkTitle: "ML Models"
weight: 20
type: "docs"
tags: ["extending viam", "machine learning", "vision"]
description: "Browse existing machine learning models to use on your device."
no_list: true
modulescript: true
---

Viam provides the ability to train, upload, and deploy [machine learning models](/services/ml/ml-models/) within the platform.
See [Machine Learning](/services/ml/) for more information.

The Viam registry hosts trained ML models that users have made public, which you can use to deploy classifiers or detectors for your use case onto your robot instead of training your own.
You can also upload your own model to the registry.

You can search the available ML models from the Viam registry here:

{{<mlmodels>}}

To use an existing model from the registry, [deploy the ML model to your robot](/services/ml/deploy/) and use a [vision service](/services/vision/) to make detections or classifications on-machine.
