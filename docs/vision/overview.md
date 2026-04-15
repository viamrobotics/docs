---
linkTitle: "Overview"
title: "Computer vision"
weight: 1
layout: "docs"
type: "docs"
description: "Run detection, classification, and 3D segmentation on camera feeds with Viam's vision service. Use ML models, heuristic color detection, or point cloud segmenters, and close the loop with retraining."
date: "2026-04-14"
---

Computer vision on Viam turns camera frames into structured results your code can act on: bounding boxes, class labels, or 3D point cloud objects. Three built-in vision service models cover the common tasks, and the [registry](https://app.viam.com/registry) has more for specialized cases.

## What the vision service does

The vision service exposes a single API. Your code calls the same methods whether the underlying detector is an ML model, a color heuristic, or a 3D segmenter. The implementation you pick decides what the service recognizes; the code you write does not change.

Available methods:

- [`GetDetections`](/reference/apis/services/vision/#getdetections) and [`GetDetectionsFromCamera`](/reference/apis/services/vision/#getdetectionsfromcamera) return 2D bounding boxes with labels and confidence.
- [`GetClassifications`](/reference/apis/services/vision/#getclassifications) and [`GetClassificationsFromCamera`](/reference/apis/services/vision/#getclassificationsfromcamera) return top-N label-confidence pairs for the whole image.
- [`GetObjectPointClouds`](/reference/apis/services/vision/#getobjectpointclouds) returns 3D point cloud objects, each with a label.
- [`CaptureAllFromCamera`](/reference/apis/services/vision/#captureallfromcamera) returns an image, its detections, classifications, and point clouds in a single round trip. Use this when you need more than one kind of result.
- [`GetProperties`](/reference/apis/services/vision/#getproperties) reports which result types the service supports at runtime.

## Pick a built-in model

| Goal                                               | Model                                                                                      | When to use it                                                                                                  |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| Detect or classify objects with a trained ML model | [`mlmodel`](/reference/services/vision/mlmodel/)                                           | General-purpose path: wraps a TFLite, ONNX, TensorFlow, or PyTorch model deployed through the ML model service. |
| Find regions of a specific hue                     | [`color_detector`](/reference/services/vision/color_detector/)                             | The target stands out by color, no training data is available, or the task is too simple for ML.                |
| Project 2D detections into 3D point cloud objects  | [`viam:vision:detections-to-segments`](/reference/services/vision/detections-to-segments/) | You need 3D positions of detected objects (for example, to pick them up). Requires a depth camera.              |

For more specialized tasks (small-object detection, face recognition, hand pose estimation, specific model architectures), browse the [registry](https://app.viam.com/registry).

## Detection vs classification vs segmentation

These three task types answer different questions.

**Detection** asks _where_ objects are in an image. A detector returns one bounding box per object, each with a label and confidence score. Use detection when you need object locations. Stopping a robot when a person enters a zone or guiding an arm to pick up a cup both need detection.

**Classification** asks _what_ the image contains. A classifier returns a small number of labels with confidence scores for the whole image or a region of it. Use classification when you just need to categorize the scene. "Is this picture of a cat or a dog?" and "is the conveyor belt clear or blocked?" are classification questions.

**3D segmentation** asks _where in 3D space_ objects are. A 3D segmenter returns a point cloud per object with coordinates in the camera frame. Use it when a robot needs physical positions. Planning an arm motion to an object or feeding obstacle positions into a navigation stack both need 3D segmentation.

## Verify that it works

After configuring a vision service, the fastest way to confirm it is producing results is the vision control card in the Viam app:

1. Open your machine in the Viam app.
2. Navigate to the **CONTROL** tab and click your vision service.
3. In the **Camera** dropdown, select the camera whose feed you want the vision service to run on. Detections or classifications appear as an overlay on the live camera feed at up to 20 frames per second. The overlay refreshes automatically.

The control card calls `CaptureAllFromCamera` under the hood, so what you see on screen matches what your code receives. If the overlay is empty, check `GetProperties` to confirm the service registered in the role you expected, then lower the confidence threshold and try again.

## Close the loop with retraining

Accuracy almost always drops when a model moves from the lab to production. The [training-to-production gap](https://medium.com/sciforce/why-your-computer-vision-model-struggles-in-the-real-world-3a6a999cdf8f) is the single most common reason a vision system fails after launch. Viam provides the pieces to close that loop on production machines:

1. Capture failing images from deployed machines with [data capture](/data-ai/capture-data/capture-sync/).
2. Label the new images in the [**DATA** tab](https://app.viam.com/data/view) and update a dataset.
3. Retrain the model with [managed training](/data-ai/train/train/) or a custom script.
4. Deploy the new model version through the ML model service and push it to your fleet.

This capture, label, train, deploy, monitor cycle is often called CVOps (computer-vision operations). Viam's data, training, fleet, and vision sections are the tools. The vision section is where your code meets the model.

## Where to go next

### Starting from scratch

- [How the vision service works](/vision/how-it-works/): the two-service architecture behind every vision pipeline
- [Configure a vision pipeline](/vision/configure/): end-to-end setup of an ML model service plus vision service

### Deploy a model

- [Deploy a model from the registry](/vision/deploy-from-registry/): pick a pre-trained model and run it on a machine
- [Deploy a custom ML model](/vision/deploy-custom-model/): bring your own trained model
- [Detect by color](/vision/detect-by-color/): no ML needed

### Use the results

- [Detect objects](/vision/detect/): 2D bounding boxes in code
- [Classify images](/vision/classify/): whole-image labels
- [Segment 3D objects](/vision/segment-3d/): point cloud objects with 3D coordinates
- [Track objects across frames](/vision/track/): persistent IDs across video frames
- [Measure depth](/vision/measure-depth/): distance readings from a depth camera
- [Act on detections](/vision/act-on-detections/): trigger machine behavior from vision results
- [Alert on detections](/vision/alert-on-detections/): send notifications on detections

### Operate in production

- [Tune detection quality](/vision/tune/): match symptoms to the right `mlmodel` attribute
- [Retrain when accuracy drops](/vision/retrain/): the CVOps loop for model maintenance
- [Roll out a new model to a fleet](/vision/roll-out-to-fleet/): staged model rollouts
- [Run batch inference](/vision/batch-inference/): run a model against stored images with `viam infer`

### Reference

- [Vision service API](/reference/apis/services/vision/)
- [ML model service API](/reference/apis/services/ml/)
- [`mlmodel` configuration](/reference/services/vision/mlmodel/)
- [`color_detector` configuration](/reference/services/vision/color_detector/)
- [`detections-to-segments` configuration](/reference/services/vision/detections-to-segments/)
