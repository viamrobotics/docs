---
linkTitle: "Models for vision"
title: "Use an ML model with the vision service"
weight: 60
layout: "docs"
type: "docs"
description: "Pick a classification or detection model for a vision service, check that its tensors match what the service expects, and find where to deploy, update, and retrain it."
capabilities: ["ml-models", "vision-service"]
diataxis: how-to
aliases:
  - /vision/deploy-and-maintain/
  - /vision/deploy-and-maintain/available-models/
  - /vision/deploy-and-maintain/deploy-from-registry/
  - /vision/deploy-from-registry/
  - /vision/deploy-custom-model/
---

The `mlmodel` vision service wraps a classification or detection model that an ML model service runs.
This page covers what is specific to vision: which model to pick, and what the vision service expects from the model's tensors.

Uploading, deploying, versioning, and retraining work the same way for every model, so those steps are in [Train and deploy ML models](/train/overview/).
For a model that a vision service doesn't use, such as a robot policy, go straight to [Upload a model](/train/upload-a-model/) and [Deploy a model to a machine](/train/deploy-a-model/).

## 1. Pick a model

A vision service can use a model from any of three sources:

- **The Viam [registry](https://app.viam.com/registry).**
  The fastest way to get a working vision pipeline is a pre-trained model.
  Use one when a general-purpose or community-shared model already handles your task, such as people detection or common objects.
- **Training on Viam.**
  Train a model on your own data with [built-in training](/train/train-a-model/) or a [custom training script](/train/custom-training-scripts/).
- **Somewhere else.**
  Use a model you trained outside Viam, for example locally, in another cloud, or in a notebook, or one you found on GitHub or Hugging Face.

Whichever source you use, match the model to:

- The **task** you need.
  A model tagged for object detection will not give you classifications, and a classification model will not give you detections.
- The **framework** the model was trained in.
  The ML model service you configure must support it.
- The **hardware** on the machine.
  TFLite models run on almost any CPU.
  Larger frameworks benefit from GPUs.

For which ML model service runs each framework, and on what hardware, see [What runs the model](/train/deploy-a-model/#what-runs-the-model).

### What the registry holds for vision {#registry-entries}

The registry has three kinds of entries you reach for when building a vision pipeline:

- **ML model service implementations.**
  The ML model service has one API method, `Infer`, but the registry offers multiple module implementations of that service.
  Each implementation targets a specific framework: TFLite, ONNX, TensorFlow, or PyTorch.
  Some also target specific hardware, such as a GPU on a Jetson.
  When you add an ML model service to your machine, you pick one implementation.
- **Vision service models.**
  The vision service has one API that covers detection, classification, and 3D segmentation (see the [full API reference](/reference/apis/services/vision/)).
  Multiple models implement that API.
  Three ship built into Viam: `mlmodel`, `color_detector`, and `viam:vision:detections-to-segments`.
  Registry modules add more for specialized tasks.
  You pick a vision service model when you configure a vision service.
- **Public ML models.**
  Model artifacts (the weights plus metadata) published to the registry so any machine can deploy them without training.
  Your ML model service loads one of these.

A typical pipeline uses one of each: a camera → an ML model service implementation running a public ML model → a vision service model interpreting its output.

The registry mixes Viam-authored modules, partner contributions, and community work at various stages of maturity.
Before picking an entry:

- **Read the module's README** for tensor requirements, hardware support, and example configuration.
  The registry card links to it.
- **Check recent commits and versions** if maturity matters.
  A module with a single old release is a different bet than one with continuous releases this quarter.
- **Prefer framework-specific implementations over the generic `triton`** unless you need a GPU or multi-framework flexibility.
  Framework-specific implementations are simpler to configure and debug.

## 2. Check the model's tensors {#tensor-requirements}

The `mlmodel` vision service expects specific tensor conventions from the model it wraps.
If the model does not match, the vision service fails to come up as a detector or classifier, or it comes up but produces garbled output.
Models trained on Viam already use the expected names, so skip this step for them.

**Detector models must expose:**

- Input tensor named `image` with shape `[batch, height, width, channels]`.
  The service feeds one image at a time.
- Output tensors named `location`, `category`, and `score`.
  Each is per-detection.

**Classifier models must expose:**

- Input tensor named `image` with the same shape.
- Output tensor named `probability`, one value per class.

**Preprocessing assumptions:**

- Input pixel values are uint8 in `[0, 255]` by default.
- Input channel order is RGB by default.
- Bounding boxes are `[xmin, ymin, xmax, ymax]` normalized to `[0, 1]`.

### Convert the model or bridge the difference {#convert-or-bridge}

If your model disagrees with any of these conventions, you generally do not have to retrain or modify it.
Set vision service attributes to bridge the gap:

- **Non-standard tensor names**: `remap_input_names` and `remap_output_names`.
  See [Tensor names do not match](/vision/object-detection/tune/#tensor-names-do-not-match).
- **Non-standard preprocessing**, such as `[-1, 1]` or `[0, 1]` normalization or BGR channel order: `input_image_mean_value`, `input_image_std_dev`, and `input_image_bgr`.
  See [Wrong labels or every label fires](/vision/object-detection/tune/#wrong-labels-or-every-label-fires).
- **Non-standard bounding box coordinate order**: `xmin_ymin_xmax_ymax_order`.
  See [Bounding boxes appear shifted or mirrored](/vision/object-detection/tune/#bounding-boxes-appear-shifted-or-mirrored).
- **Class-specific confidence tuning**: `label_confidences`.

The [`mlmodel` reference](/reference/services/vision/mlmodel/) lists every attribute.

Convert the model itself only when its format is unsupported (for example, exporting from Keras HDF5 to TFLite) or when the tensor types are incompatible with the chosen ML model service.
[Upload a model](/train/upload-a-model/#check-the-format) lists the supported formats.

## 3. Deploy the model

1. Make sure the model is in your organization or the registry.
   A registry model, or a model you trained on Viam, already is.
   For any other model, [upload it](/train/upload-a-model/).
1. Follow [Deploy a model to a machine](/train/deploy-a-model/#deploy-the-model).
   Deploying adds an ML model service, which loads the model file and exposes it for inference.
   It does not interpret the output; that is the vision service's job.
   When you deploy from the model's page, keep **Include Vision service** on so the deployment adds a `vision/mlmodel` service that uses the model and an existing camera.
1. When you select a version, pin a specific version in production.
   See [Choose a model version](/train/deploy-a-model/#choose-a-model-version).

If the model file lives on the machine's disk and you do not want to upload it, see [Run a model file stored on the machine](/train/deploy-a-model/#local-model-file).

## 4. Check the vision service and verify

If the deployment didn't add a vision service, add one yourself: see [Configure a vision pipeline](/vision/configure/#3-add-a-vision-service).
The service's `mlmodel_name` is the name of the ML model service, and `camera_name` is the default camera.

Then [verify with the control card](/vision/configure/#6-verify-with-the-control-card): bounding boxes or classifications appear as an overlay on the live camera feed.

If you see nothing:

- Confirm the vision service registered in the expected role.
  Call [`GetProperties`](/reference/apis/services/vision/#getproperties).
  A detection model that registered as a classifier (or a classifier that registered as a detector) returns empty lists.
- Lower `default_minimum_confidence` on the vision service and try again.
  A model may be producing detections below the default confidence threshold.
- Check `viam-server` logs for startup errors mentioning tensor names or label files.

If results look wrong (shifted boxes, wrong labels, or zero detections), go through [Tune detection quality](/vision/object-detection/tune/).
Every common failure mode maps to a specific attribute on the vision service.

## Maintain the model

Your vision service, your application code, and your downstream triggers and modules do not need to change when the model's version changes.

- [Update or roll back a deployed model](/train/deploy-a-model/#update-a-deployed-model): move one machine to a newer version, or back to an earlier one.
- [Deploy ML models across your fleet](/fleet/deploy-ml-models/): update many machines at once.
- [Retrain a model](/train/retrain-a-model/): capture the cases the model gets wrong and train a new version.
- [Run batch inference](/train/batch-inference/): run a model against stored images before you deploy it to live machines.

## Next steps

- [Configure a vision pipeline](/vision/configure/): the end-to-end setup of the ML model service and vision service
- [Tune detection quality](/vision/object-detection/tune/): fix specific detection failure modes
- [Detect objects](/vision/object-detection/detect/): use detections in code
