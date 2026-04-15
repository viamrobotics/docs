---
linkTitle: "Browse available models"
title: "Browse available models and services"
weight: 5
layout: "docs"
type: "docs"
modulescript: true
description: "Browse ML model service implementations, vision service models, and public ML models in the Viam registry."
date: "2026-04-14"
---

Three kinds of registry entries feed a vision pipeline:

- **ML model service implementations**. There is one ML model service API (`Infer`); multiple module implementations target different frameworks (TFLite, ONNX, TensorFlow, PyTorch) and sometimes specific hardware (CPU, GPU on Jetson).
- **Vision service models**. There is one vision service API (`GetDetections`, `GetClassifications`, `GetObjectPointClouds`, `CaptureAllFromCamera`, `GetProperties`); three models ship built in (`mlmodel`, `color_detector`, `viam:vision:detections-to-segments`) and registry modules add more for specialized tasks.
- **Public ML models**. Model artifacts (weights plus metadata) published to the registry so any machine can deploy them without training.

## How to use this page

The lists below come directly from the registry at page load. They include both well-maintained Viam-authored modules and community contributions at various stages of maturity. Before picking one:

- **Read the module's README** for the tensor requirements, hardware support, and example configuration. The registry card links to it.
- **Check recent commits and versions** if maturity matters. A module with a single 2023 release is a different bet than one with continuous releases this quarter.
- **Prefer framework-specific implementations over the generic `triton`** unless you actually need GPU or multi-framework flexibility. Framework-specific implementations are simpler to configure and debug.
- **Verify the model task type matches your need.** A model tagged for `object detection` will not give you classifications, and vice versa. See [Deploy an ML model from the registry, step 1](/vision/deploy-and-maintain/deploy-from-registry/#1-pick-a-model) for the task/framework/hardware matching table.

## Available ML model service implementations

{{< resources_svc api="rdk:service:mlmodel" type="ML model" >}}

## Available vision service models

{{% expand "Click to see available vision service models" %}}

{{< resources_svc api="rdk:service:vision" type="vision" >}}

{{% /expand %}}

## Public machine learning models

{{< mlmodels >}}

## Next steps

- [Configure a vision pipeline](/vision/configure/): wire a model through an ML model service and a vision service
- [Deploy an ML model from the registry](/vision/deploy-and-maintain/deploy-from-registry/): the step-by-step how-to
- [Deploy a custom ML model](/vision/deploy-and-maintain/deploy-custom-model/): for models you trained yourself or brought from elsewhere
