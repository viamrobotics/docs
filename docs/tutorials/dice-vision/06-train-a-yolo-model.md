---
title: "Phase 6: Train a YOLO model from the registry"
linkTitle: "6. Train a YOLO model"
weight: 60
type: "docs"
layout: "docs"
slug: "train-a-yolo-model"
description: "Train a YOLO object detection model on the training dataset with the yolo-onnx-training script from the Viam registry."
capabilities: ["ml-training", "module-registry"]
diataxis: workshop
date: "2026-11-06"
draft: true
workshop: "dice-vision"
phase: 6
phase_total: 10
time_estimate: "15 minutes"
prev: "/tutorials/dice-vision/train-a-built-in-model/"
next: "/tutorials/dice-vision/build-the-test-datasets/"
toc_hide: true
---

At the end of this phase, a second model is training on `dice-train`, this time with a custom training script that fine-tunes a YOLO model.
Both models train on exactly the same data, so in [Phase 8](/tutorials/dice-vision/evaluate-both-models/) you can compare them fairly.

## Built-in and custom training {#built-in-and-custom-training}

Training a model takes two things: a dataset, and code that teaches the model from it.
In [Phase 5](/tutorials/dice-vision/train-a-built-in-model/), Viam supplied the code.
Built-in training picks the model and how it learns, and you choose only the dataset and the labels.

A custom training script is a Python program that does the training instead.
You can write your own, or use one that someone else has published to the [Viam registry](https://app.viam.com/registry).
Viam runs the script in the cloud on your dataset and saves the model it produces, just as it does for built-in training.

Custom scripts let you train models that built-in training doesn't offer, such as YOLO.
Custom training jobs run on more powerful GPUs and are billed at a higher rate than built-in training; see [pricing](https://www.viam.com/product/pricing).
For more, see [Built-in or custom training](/train/overview/#training-method).

## Why YOLO {#why-yolo}

[YOLO](https://docs.ultralytics.com/), short for "You Only Look Once", is a widely used family of object detection models from Ultralytics.
It finds every object in an image in a single pass, which makes it fast enough to run on a live camera feed, and it handles many small objects in one frame, like a handful of dice.

You don't train YOLO from nothing.
The script starts from a YOLO model that's already been trained on a large dataset of everyday objects, so it already knows how to find edges, corners and shapes.
Training it on your images, called fine-tuning, teaches it what dice and their faces look like.
That's why about 100 images is enough.

This workshop trains a YOLO model alongside the built-in one because they're different kinds of model.
Comparing them on the same test images in [Phase 8](/tutorials/dice-vision/evaluate-both-models/) shows whether the extra setup and cost of a custom model pays off for reading dice.

## See what the script does {#see-what-the-script-does}

The `yolo-onnx-training` script, published by `devrel` from the [viam-devrel/yolo-training](https://github.com/viam-devrel/yolo-training) repository, runs these steps in the cloud:

1. Downloads `dice-train` and converts it to the folder layout YOLO expects.
1. Sets aside part of the images as its own validation set, which it uses to check how well the model is learning.
1. Fine-tunes a small pretrained YOLO model on your dice.
1. Exports an ONNX model, with a `labels.txt` file, in the shape that Viam's model evaluation and ML model service read.

## Choose how long it trains {#choose-how-long-it-trains}

The script takes its settings as arguments, which you enter in the training form.
This workshop sets one of them, `num_epochs`.

An epoch is one full pass through the training images.
In each epoch, the model looks at every image, compares its guesses with your boxes, and adjusts itself to make better guesses next time.
One pass isn't enough to learn much, so training runs many epochs, and the model improves a little each time.

More epochs give the model more chances to learn, but the job takes longer.
Past a point, the model also starts memorizing your training images instead of learning what dice look like in general, and it gets worse at reading new images.
The script guards against this: after each epoch it scores the model on its validation images, keeps the version that scored best, and stops early if the model hasn't improved for half of the epochs you set.

If you don't set `num_epochs`, the script runs up to 200 epochs.
This workshop uses 100 to keep the job shorter.
For the script's other arguments, see its [README](https://github.com/viam-devrel/yolo-training#readme).

## Start the YOLO training job {#start-the-yolo-training-job}

1. On the **DATASETS** page, open `dice-train`.
1. Click **Train model**.
1. Select **Train on a custom training script**.
1. In the **Training script** field, search for `yolo-onnx-training` and select the one by `devrel`.
   The latest version is selected for you.
1. Name the model `dice-yolo`.
1. In the **Container version** dropdown, select `tf:2.21`.
   The container is the software environment the script runs in, and this script is tested with `tf:2.21`.
1. In the **Arguments** section, click **Add argument**, enter `num_epochs` as the name, and enter `100` as the value.
1. Click **Train model**.

{{< checkpoint >}}
On the **DATA** tab, click **MODELS** and expand **Active Training**.
Both `dice-tflite` and `dice-yolo` are listed, each showing **Preparing**, **Waiting for GPU**, **Training** or **Completed**.
If you don't see `dice-yolo`, check that you clicked **Train model** at the end of the form.
If `dice-yolo` shows **Failed**, click the job and read its logs; a log that mentions a container or Python package usually means the wrong container version is selected; train again with `tf:2.21`.
{{< /checkpoint >}}

Both jobs run in the cloud, so you don't need to wait for them.
Move on to the next phase while your models train.

In the next phase, you capture and label two test datasets that neither model has seen.

{{< workshop-nav >}}
