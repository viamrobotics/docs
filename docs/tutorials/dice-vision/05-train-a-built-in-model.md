---
title: "Phase 5: Train a built-in model"
linkTitle: "5. Train a built-in model"
weight: 50
type: "docs"
layout: "docs"
slug: "train-a-built-in-model"
description: "Start a built-in TFLite object detection training job on the full training dataset."
capabilities: ["ml-training"]
diataxis: workshop
date: "2026-11-06"
draft: true
workshop: "dice-vision"
phase: 5
phase_total: 10
time_estimate: "10 minutes"
prev: "/tutorials/dice-vision/auto-label-the-training-set/"
next: "/tutorials/dice-vision/train-a-yolo-model/"
toc_hide: true
---

At the end of this phase, a built-in TFLite model is training on all of `dice-train`.
It's the first of two models you'll compare.
Built-in training needs no code and runs well on small machines.
While this model trains, you can move on to [Phase 6](/tutorials/dice-vision/train-a-yolo-model/) and start the second model.

## Start the built-in training job {#start-the-built-in-training-job}

This is the same built-in TFLite training you used for the starter model in [Phase 3](/tutorials/dice-vision/train-a-starter-model/), but this time it learns from the full training set: about 100 images, all labeled and reviewed.
With more than three times as many images, expect it to be more accurate than the starter.
In [Phase 8](/tutorials/dice-vision/evaluate-both-models/) you compare it with the YOLO model from [Phase 6](/tutorials/dice-vision/train-a-yolo-model/) to see which one reads dice better.

1. On the **DATASETS** page, open `dice-train`.
1. Click **Train model**.
1. Select **TFLite** as the framework.
1. Name the model `dice-tflite`.
1. Select **Object Detection** as the task type.
1. Select all six labels, `1` through `6`.
1. Click **Train model**.

For the other options and the CLI equivalent, see [Train a model](/train/train-a-model/).

{{< checkpoint >}}
On the **DATA** tab, click **MODELS** and expand **Active Training**.
The `dice-tflite` job shows **Preparing**, **Waiting for GPU** or **Training**, and later **Completed**.
If the job won't start, the message names the problem: usually a label with fewer than 10 boxes, or more than 20% of images unlabeled.
Fix it in `dice-train` as in [Phase 4](/tutorials/dice-vision/auto-label-the-training-set/#review-every-prediction) and try again.
{{< /checkpoint >}}

In the next phase, you start a second training job on the same dataset with a YOLO training script from the registry.

{{< workshop-nav >}}
