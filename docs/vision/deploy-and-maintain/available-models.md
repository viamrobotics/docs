---
linkTitle: "What's in the registry"
title: "What's in the Viam registry for vision"
weight: 5
layout: "docs"
type: "docs"
description: "Three kinds of registry entries feed a vision pipeline: ML model service implementations, vision service models, and public ML models. How to pick among them."
date: "2026-04-14"
---

The [Viam registry](https://app.viam.com/registry) has three kinds of entries you reach for when building a vision pipeline. Understanding what each one is makes the rest of the deploy and tune flow easier.

## Three kinds of entries

- **ML model service implementations.** There is one ML model service API (`Infer`); multiple module implementations target different frameworks (TFLite, ONNX, TensorFlow, PyTorch) and sometimes specific hardware (CPU, GPU on Jetson). When you add an ML model service to your machine, you pick one of these implementations.
- **Vision service models.** There is one vision service API (`GetDetections`, `GetClassifications`, `GetObjectPointClouds`, `CaptureAllFromCamera`, `GetProperties`); three models ship built in (`mlmodel`, `color_detector`, `viam:vision:detections-to-segments`) and registry modules add more for specialized tasks. You pick a vision service model when you configure a vision service.
- **Public ML models.** Model artifacts (weights plus metadata) published to the registry so any machine can deploy them without training. Your ML model service loads one of these.

A typical pipeline uses one of each: a camera → an ML model service implementation running a public ML model → a vision service model interpreting its output.

## How to pick

The registry mixes Viam-authored modules, partner contributions, and community work at various stages of maturity. Before picking one:

- **Read the module's README** for tensor requirements, hardware support, and example configuration. The registry card links to it.
- **Check recent commits and versions** if maturity matters. A module with a single 2023 release is a different bet than one with continuous releases this quarter.
- **Prefer framework-specific implementations over the generic `triton`** unless you actually need GPU or multi-framework flexibility. Framework-specific implementations are simpler to configure and debug.
- **Verify the model task type matches your need.** A model tagged for `object detection` will not give you classifications, and vice versa. See [Deploy an ML model from the registry, step 1](/vision/deploy-and-maintain/deploy-from-registry/#1-pick-a-model) for the task/framework/hardware matching table.

To browse or search the registry, go to [app.viam.com/registry](https://app.viam.com/registry).

## Next steps

- [Deploy an ML model from the registry](/vision/deploy-and-maintain/deploy-from-registry/): the step-by-step how-to
- [Deploy a custom ML model](/vision/deploy-and-maintain/deploy-custom-model/): for models you trained yourself or brought from elsewhere
- [Configure a vision pipeline](/vision/configure/): wire a model through an ML model service and a vision service
