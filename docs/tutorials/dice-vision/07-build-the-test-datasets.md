---
title: "Phase 7: Build the test datasets"
linkTitle: "7. Build the test datasets"
weight: 70
type: "docs"
layout: "docs"
slug: "build-the-test-datasets"
description: "Capture and label a clean test dataset and a hard test dataset that neither model trained on."
capabilities: ["datasets"]
diataxis: workshop
date: "2026-11-06"
draft: true
workshop: "dice-vision"
phase: 7
phase_total: 10
time_estimate: "25 minutes"
prev: "/tutorials/dice-vision/train-a-yolo-model/"
next: "/tutorials/dice-vision/evaluate-both-models/"
toc_hide: true
---

At the end of this phase, you have two labeled test datasets that neither model has seen: `dice-test-clean`, taken the same way as your training images, and `dice-test-hard`, taken in conditions the models never trained on.
A model can score well on the images it learned from and still fail on new ones, so you score models only on images they didn't train on.
The labels in these datasets are the answer key, so they need to be right.

## Capture and label the clean test dataset {#capture-and-label-the-clean-test-dataset}

1. Create a dataset named `dice-test-clean`.
1. Add about 20 images to it from the **TEST** section of the `camera` card on the **CONFIGURE** tab, with the same dice, camera height and light as your training images.
1. Add three images of the empty background, with no dice.
1. Open `dice-test-clean`, click **Run model**, then **Get auto-predictions**, and get predictions from `dice-starter-model` at a confidence threshold of `0.25`, as in [Phase 4](/tutorials/dice-vision/auto-label-the-training-set/#get-predictions-from-the-starter-model).
1. Review every prediction, and draw a box on every die that has none.

Check every box here, not just the ones that look wrong.
These labels are the answer key for [Phase 8](/tutorials/dice-vision/evaluate-both-models/), so a wrong label makes a model that reads the die correctly look wrong.

{{< checkpoint >}}
`dice-test-clean` shows about 23 images, every die in the 20 dice images has a correct box, and the three empty images have none.
If you find a box with the wrong value, delete it and draw a new one.
{{< /checkpoint >}}

## Capture and label the hard test dataset {#capture-and-label-the-hard-test-dataset}

This dataset shows how each model copes with conditions it didn't train on, which is where models usually differ most.

1. Create a dataset named `dice-test-hard`.
1. Add about 20 images, mixing these conditions:

   - The camera raised to about 45 cm, so the dice look smaller.
   - Three to five dice pushed together so they touch.
   - A different background, such as a sheet of colored or patterned paper under the dice.
   - Dimmer light, such as one lamp turned off.

   {{< imgproc src="/tutorials/dice-vision/hard-examples.jpg" resize="1000x" declaredimensions=true class="imgzoom shadow" alt="Four hard test images: dice small and far away on a white desk from a raised, shallower camera; five touching dice on a black mat printed with white robot-part drawings; four dice spread out on bright pink paper; and four dice, three of them touching, on blue paper." >}}

1. Add three images of the empty background.
1. Label every die, either by hand as in [Phase 2](/tutorials/dice-vision/label-the-starter-set/#draw-a-box-on-every-die), or with auto-predictions from `dice-starter-model` as in [Phase 4](/tutorials/dice-vision/auto-label-the-training-set/#get-predictions-from-the-starter-model).
   The starter model never trained on these conditions, so expect to fix more of its boxes, and check every one.
1. Put the camera back at its original height and angle.
   In Phases 9 and 10 the model reads live rolls, and it reads them best from the position it was trained on.

{{< checkpoint >}}
`dice-test-hard` shows about 23 images, every die in the 20 dice images has a correct box, and the three empty images have none.
If you can't tell a die's value yourself, remove that image from the dataset rather than leaving the die unboxed; an unboxed die counts against any model that finds it.
{{< /checkpoint >}}

The empty images let the evaluation count false positives: boxes a model draws where there's no die.

In the next phase, you score both models on both test datasets and pick the one Yahtzee will use.

{{< workshop-nav >}}
