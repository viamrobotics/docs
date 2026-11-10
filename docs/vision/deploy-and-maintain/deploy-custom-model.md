---
linkTitle: "Deploy a custom model"
title: "Deploy a custom ML model"
weight: 20
layout: "docs"
type: "docs"
description: "Use a classification or detection model you trained or brought from elsewhere with the vision service: match its tensors, deploy it, and verify it."
capabilities: ["ml-models", "vision-service"]
diataxis: how-to
date: "2026-04-14"
aliases:
  - /vision/deploy-custom-model/
---

Use this guide when you have a classification or detection model that is not already in the Viam [registry](https://app.viam.com/registry), and you want a vision service to use it. That covers three cases:

- You trained the model on Viam data using [built-in training](/train/train-a-model/) or a [custom training script](/train/custom-training-scripts/).
- You trained it entirely outside Viam (local, another cloud, a notebook).
- You found it elsewhere (GitHub, Hugging Face) and want to run it on your machines.

If you just want to pick a ready-made model from the [registry](https://app.viam.com/registry), see [Deploy an ML model from the registry](/vision/deploy-and-maintain/deploy-from-registry/) instead. For a model that a vision service doesn't use, such as a robot policy, see [Upload a model](/train/upload-a-model/) and [Deploy a model to a machine](/train/deploy-a-model/).

## 1. Meet the tensor shape and name requirements

The `mlmodel` vision service expects specific tensor conventions from the model it wraps. If the model does not match, the vision service fails to come up as a detector or classifier, or it comes up but produces garbled output.

**Detector models must expose:**

- Input tensor named `image` with shape `[batch, height, width, channels]`. The service feeds one image at a time.
- Output tensors named `location`, `category`, and `score`. Each is per-detection.

**Classifier models must expose:**

- Input tensor named `image` with the same shape.
- Output tensor named `probability`, one value per class.

**Preprocessing assumptions:**

- Input pixel values are uint8 in `[0, 255]` by default. If your model expects `[-1, 1]` or `[0, 1]` normalization, use [`input_image_mean_value` and `input_image_std_dev`](/vision/object-detection/tune/#wrong-labels-or-every-label-fires) on the vision service.
- Input channel order is RGB by default. If your model expects BGR, set [`input_image_bgr: true`](/vision/object-detection/tune/#wrong-labels-or-every-label-fires).
- Bounding boxes are `[xmin, ymin, xmax, ymax]` normalized to `[0, 1]`. If your model outputs a different order, use [`xmin_ymin_xmax_ymax_order`](/vision/object-detection/tune/#bounding-boxes-appear-shifted-or-mirrored).

If your model disagrees with any of these assumptions, retraining is not required. Set the matching vision service attributes to bridge the gap. See [Tune detection quality](/vision/object-detection/tune/).

**Tensor names:** if your model does not use the exact names above, you can remap them on the vision service without retouching the model. See [Tune detection quality](/vision/object-detection/tune/#tensor-names-do-not-match).

## 2. Add the model to your organization

<span id="3-add-the-model-to-your-organization"></span><span id="deploy-a-registry-framework-model"></span>A model you trained on Viam is already in your organization. For any other model, [upload it](/train/upload-a-model/). The upload page lists the supported model formats and what to convert if yours isn't one of them.

## 3. Deploy the model to a machine

Follow [Deploy a model to a machine](/train/deploy-a-model/). When you deploy from the model's page, keep **Include Vision service** on so the deployment adds a `vision/mlmodel` service that uses the model and an existing camera.

If the model file lives on the machine's disk and you do not want to upload it, see [Run a model file stored on the machine](/train/deploy-a-model/#local-model-file).

## 4. Check the vision service

If the deployment didn't add a vision service, add one yourself: see [Configure a vision pipeline](/vision/configure/#3-add-a-vision-service). The service's `mlmodel_name` is the name of the ML model service, and `camera_name` is the default camera.

If the model does not produce detections right away, its input preprocessing or output tensor layout is probably non-standard. See [Tune detection quality](/vision/object-detection/tune/).

## 5. Verify

1. Open the **CONTROL** tab.
2. Click the vision service.
3. In the **Camera** dropdown, select the camera whose feed you want the vision service to run on. Detections appear as bounding boxes on the live camera feed and refresh automatically.

If results look wrong (shifted boxes, wrong labels, or zero detections), go through [Tune detection quality](/vision/object-detection/tune/). Every common failure mode maps to a specific attribute on the vision service.

## When to convert vs when to bridge

You generally do not have to modify the model itself. The vision service can bridge:

- **Non-standard tensor names** through `remap_input_names` and `remap_output_names`.
- **Non-standard preprocessing** through `input_image_mean_value`, `input_image_std_dev`, `input_image_bgr`.
- **Non-standard bounding box coordinate order** through `xmin_ymin_xmax_ymax_order`.
- **Class-specific confidence tuning** through `label_confidences`.

Convert the model itself only when its format is unsupported (for example, exporting from Keras HDF5 to TFLite) or when the tensor types are incompatible with the chosen ML model service.

## Next steps

- [Tune detection quality](/vision/object-detection/tune/): fix specific detection failure modes
- [mlmodel reference](/reference/services/vision/mlmodel/): full attribute reference
- [Detect objects](/vision/object-detection/detect/): use detections in code
- [Retrain a model](/train/retrain-a-model/): maintain quality in production
