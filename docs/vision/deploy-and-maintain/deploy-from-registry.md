---
linkTitle: "Deploy a model from the registry"
title: "Deploy an ML model from the registry"
weight: 10
layout: "docs"
type: "docs"
description: "Pick a pre-trained ML model from the Viam registry, deploy it to your machine, and verify that a vision service can use it."
capabilities: ["ml-models", "vision-service"]
diataxis: how-to
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

The fastest way to get a working vision pipeline is to pick a pre-trained model from the Viam [registry](https://app.viam.com/registry). Pick a model and deploy it to your machine. `viam-server` downloads the model to the machine and the vision service can use it immediately.

Use this guide when a general-purpose or community-shared model already handles your task (people detection, common objects, COCO-class recognition). If you need a custom model trained on your data, see [Deploy a custom ML model](/vision/deploy-and-maintain/deploy-custom-model/).

## 1. Pick a model

Open the [Viam registry](https://app.viam.com/registry) and search or browse for models. If you are not sure which kind of registry entry to pick, see [What's in the registry for vision](/vision/deploy-and-maintain/available-models/) first. Each entry shows its framework, supported hardware, and a short description.

When picking, match the model to:

- The **task** you need (detection vs classification vs segmentation).
- The **framework** the model was trained in. The ML model service you configure must support it.
- The **hardware** on the machine. TFLite models run on almost any CPU. Larger frameworks benefit from GPUs.

### Supported frameworks and hardware {#model-framework-support}

For which ML model service runs each framework, and on what hardware, see [What runs the model](/train/deploy-a-model/#what-runs-the-model).

## 2. Deploy the model

Deploy the model from its page or from your machine's **CONFIGURE** tab: see [Deploy a model to a machine](/train/deploy-a-model/#deploy-the-model). Deploying adds an ML model service, which loads the model file and exposes it for inference. It does not interpret the output; that is the vision service's job.

When you select a version, pin a specific version in production; see [Choose a model version](/train/deploy-a-model/#choose-a-model-version).

## 3. Check the vision service

The ML model service is a building block. To get detections, classifications, or point cloud objects from your code, you need a vision service that wraps it.

For a classification or detection model, the deployment adds a `vision/mlmodel` service unless you turn **Include Vision service** off. To add or change one yourself, including its default camera, see [Configure a vision pipeline](/vision/configure/#3-add-a-vision-service). In the vision service panel, the **ML MODEL** section selects the ML model service and the **DEFAULT CAMERA** section selects the camera the service uses by default.

If the underlying model uses non-standard tensor names or preprocessing conventions, additional configuration is required. See the [`mlmodel` reference](/reference/services/vision/mlmodel/) for every attribute, and [Tune detection quality](/vision/object-detection/tune/) for a symptom-to-attribute map.

## 4. Verify

Open the **CONTROL** tab, click the vision service, and select the camera from the **Camera** dropdown. If the model is working, bounding boxes or classifications appear as an overlay on the live camera feed and refresh automatically. Make sure you pick the same camera your vision service is configured to use.

If you see nothing:

- Confirm the vision service registered in the expected role. Call [`GetProperties`](/reference/apis/services/vision/#getproperties) or check the vision service's **Test** panel. A detection model that registered as a classifier (or vice versa) will return empty lists.
- Lower `default_minimum_confidence` on the vision service and try again. A model may be producing detections below the default confidence threshold.
- Check `viam-server` logs for startup errors mentioning tensor names or label files.

See [Tune detection quality](/vision/object-detection/tune/) for detailed fixes.

## Update to a newer model version later

To move a machine to a newer version of the model, or roll back, see [Update or roll back a deployed model](/train/deploy-a-model/#update-a-deployed-model). Your vision service, your application code, and your downstream triggers and modules do not need to change. To update many machines at once, see [Deploy ML models across your fleet](/fleet/deploy-ml-models/).

## Next steps

- [Configure a vision pipeline](/vision/configure/): the broader end-to-end setup
- [Tune detection quality](/vision/object-detection/tune/): fine-tune mlmodel vision service attributes
- [Deploy a custom ML model](/vision/deploy-and-maintain/deploy-custom-model/): bring your own trained model
- [Retrain a model](/train/retrain-a-model/): close the loop on drift
