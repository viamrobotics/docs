---
linkTitle: "Deploy a model from the registry"
title: "Deploy an ML model from the registry"
weight: 10
layout: "docs"
type: "docs"
description: "Pick a pre-trained ML model from the Viam registry, deploy it to your machine, and wire it through an ML model service so a vision service can use it."
date: "2026-04-14"
aliases:
  - /data-ai/ai/deploy/
  - /how-tos/train-deploy-ml/
  - /services/ml/
  - /registry/ml/
  - /services/ml/upload-model/
  - /services/ml/edit/
  - /ml/edit/
  - /manage/data/upload-model/
  - /manage/ml/upload-model/
  - /ml/upload-model/
  - /services/ml/ml-models/
  - /registry/ml-models/
  - /manage/ml/
  - /ml/deploy/
  - /ml/
  - /services/ml/deploy/
  - /how-tos/deploy-ml/
  - /manage/data/deploy-model/
  - /vision/deploy-from-registry/
---

The fastest way to get a working vision pipeline is to pick a pre-trained model from the Viam [registry](https://app.viam.com/registry). Select a model, pick a framework-matching ML model service, and save the config. `viam-server` downloads the model to the machine and the vision service can use it immediately.

Use this guide when a general-purpose or community-shared model already handles your task (people detection, common objects, COCO-class recognition). If you need a custom model trained on your data, see [Deploy a custom ML model](/vision/deploy-and-maintain/deploy-custom-model/).

## 1. Pick a model

Open the [Viam registry](https://app.viam.com/registry) and search or browse for models. If you are not sure which kind of registry entry to pick, see [What's in the registry for vision](/vision/deploy-and-maintain/available-models/) first. Each entry shows its framework, supported hardware, and a short description.

When picking, match the model to:

- The **task** you need (detection vs classification vs segmentation).
- The **framework** the model was trained in. The ML model service you configure must support it.
- The **hardware** on the machine. TFLite models run on almost any CPU. Larger frameworks benefit from GPUs.

### Supported frameworks and hardware {#model-framework-support}

| Framework                                          | ML model service                                                                                                                                | Hardware support                                     | Notes                                                                                            |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [TensorFlow Lite](https://www.tensorflow.org/lite) | [`tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu)                                                                                     | linux/amd64, linux/arm64, darwin/arm64, darwin/amd64 | Quantized models; broadest hardware support. Model requirements documented in the module README. |
| [ONNX](https://onnx.ai/)                           | [`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack)             | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64   | Universal format. Not hardware-specific unless you use Triton on a Jetson.                       |
| [TensorFlow](https://www.tensorflow.org/)          | [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64   | Full framework. Best for larger production models.                                               |
| [PyTorch](https://pytorch.org/)                    | [`torch-cpu`](https://app.viam.com/module/viam/torch-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack)           | Nvidia GPU, linux/arm64, darwin/arm64                | Common for open-source research models.                                                          |

{{< alert title="Note" color="note" >}}
For ML model services that support GPUs (like [Triton on Jetson](https://github.com/viamrobotics/viam-mlmodelservice-triton/)), you can configure the service to use either the CPU or the dedicated GPU at runtime.
{{< /alert >}}

## 2. Add the ML model service

The ML model service loads the model file and exposes it for inference. It does not interpret the output; that is the vision service's job.

1. Open your machine in the Viam app and go to the **CONFIGURE** tab.
2. Click the **+** icon next to your machine part and select **Configuration block**.
3. In the search field, type the ML model service name (for example, `tflite_cpu` for TFLite models) and select the matching result.
4. Click **Add component**, give it a name (for example, `my-ml-model`), and click **Add component** again to confirm.

## 3. Select the model

In the ML model service panel:

1. Click **Select model**. A dialog opens showing models from your organization and the public [registry](https://app.viam.com/registry).
2. Filter or search for the model you picked in step 1.
3. Click the model to select it.
4. In the **Version** dropdown, choose either a specific version or **Latest**:

- **A specific version** pins the machine to that version until you explicitly change it. Recommended for production.
- **Latest** automatically upgrades when a newer version of the model is published. Useful during development but risky in production.

Save the configuration. `viam-server` downloads the model package to the machine and reports the service as ready.

## 4. Add a vision service that wraps the model

The ML model service is a building block. To get detections, classifications, or point cloud objects from your code, add a vision service that wraps it.

1. Click the **+** icon and select **Configuration block**.
2. In the search field, type `vision` or `mlmodel` and select the `vision/mlmodel` result.
3. Click **Add component**, name the service (for example, `my-detector`), and click **Add component** again to confirm.
4. In the vision service panel's **ML MODEL** section, select the ML model service from step 3.
5. In the **DEFAULT CAMERA** section, pick the camera the vision service should use by default.
6. Save.

If the underlying model uses non-standard tensor names or preprocessing conventions, additional configuration is required. See the [`mlmodel` reference](/reference/services/vision/mlmodel/) for every attribute, and [Tune detection quality](/vision/object-detection/tune/) for a symptom-to-attribute map.

## 5. Verify

Open the **CONTROL** tab, click the vision service, and select the camera from the **Camera** dropdown. If the model is working, bounding boxes or classifications appear as an overlay on the live camera feed and refresh automatically. Make sure you pick the same camera your vision service is configured to use.

If you see nothing:

- Confirm the vision service registered in the expected role. Call [`GetProperties`](/reference/apis/services/vision/#getproperties) or check the vision service's **Test** panel. A detection model that registered as a classifier (or vice versa) will return empty lists.
- Lower `default_minimum_confidence` on the vision service and try again. A model may be producing detections below the default confidence threshold.
- Check `viam-server` logs for startup errors mentioning tensor names or label files.

See [Tune detection quality](/vision/object-detection/tune/) for detailed fixes.

## Update to a newer model version later

When a newer version of the model is published to the [registry](https://app.viam.com/registry):

1. Open the ML model service panel on your machine.
2. Change the **Version** dropdown to the new version.
3. Save. `viam-server` downloads the new version and restarts the service in place.

Your vision service, your application code, and your downstream triggers and modules do not need to change.

For rolling this out across many machines at once, see [Retrain when your model drifts](/vision/deploy-and-maintain/retrain/) and the [fleet deployment docs](/fleet/).

## Next steps

- [Configure a vision pipeline](/vision/configure/): the broader end-to-end setup
- [Tune detection quality](/vision/object-detection/tune/): fine-tune mlmodel vision service attributes
- [Deploy a custom ML model](/vision/deploy-and-maintain/deploy-custom-model/): bring your own trained model
- [Retrain when accuracy drops](/vision/deploy-and-maintain/retrain/): close the loop on drift
