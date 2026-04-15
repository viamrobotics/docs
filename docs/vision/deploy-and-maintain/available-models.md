---
linkTitle: "Browse available models"
title: "Browse available models and services"
weight: 5
layout: "docs"
type: "docs"
modulescript: true
description: "Browse ML model services (TFLite, ONNX, TensorFlow, PyTorch, and GPU variants), vision services, and public ML models available in the Viam registry."
date: "2026-04-14"
---

Three things show up in the [Viam registry](https://app.viam.com/registry) that a vision pipeline can use:

- **ML model services** load and run model files. Each service implementation targets a specific framework (TFLite, ONNX, TensorFlow, PyTorch) and sometimes a specific hardware path (CPU, GPU on Jetson).
- **Vision services** interpret model output into detections, classifications, or 3D segments, or detect by heuristics rather than ML. This includes the three built-in models (`mlmodel`, `color_detector`, `viam:vision:detections-to-segments`) and module-provided models for specialized tasks.
- **Public ML models** are model artifacts (weights plus metadata) published to the registry so any machine can deploy them without training.

## How to use this page

The lists below come directly from the registry at page load. They include both well-maintained Viam-authored modules and community contributions at various stages of maturity. Before picking one:

- **Read the module's README** for the tensor requirements, hardware support, and example configuration. The registry card includes a link.
- **Check recent commits and versions** if maturity matters for your use case. A module with a single 2023 release is a different bet than one with continuous releases this quarter.
- **Prefer framework-specific services over the generic `triton`** unless you actually need GPU or multi-framework flexibility. Framework-specific services are simpler to configure and debug.
- **Verify the model task type matches your need.** A model tagged for `object detection` will not give you classifications, and vice versa. See [Deploy an ML model from the registry, step 1](/vision/deploy-and-maintain/deploy-from-registry/#1-pick-a-model) for the task/framework/hardware matching table.

## Available ML model services

{{< resources_svc api="rdk:service:mlmodel" type="ML model" >}}

## Available vision services

{{% expand "Click to see available vision services" %}}

{{< resources_svc api="rdk:service:vision" type="vision" >}}

{{% /expand %}}

## Public machine learning models

{{< mlmodels >}}

## Next steps

- [Configure a vision pipeline](/vision/configure/): wire a model through an ML model service + vision service
- [Deploy an ML model from the registry](/vision/deploy-and-maintain/deploy-from-registry/): the step-by-step how-to
- [Deploy a custom ML model](/vision/deploy-and-maintain/deploy-custom-model/): for models you trained yourself or brought from elsewhere
