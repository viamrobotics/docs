---
title: "Phase 3: Train a starter and capture more"
linkTitle: "3. Train a starter model"
weight: 30
type: "docs"
layout: "docs"
slug: "train-a-starter-model"
description: "Start a built-in training job on the starter dataset, then capture about 70 more images into the training dataset while it runs."
capabilities: ["ml-training", "datasets"]
diataxis: workshop
date: "2026-11-06"
draft: true
workshop: "dice-vision"
phase: 3
phase_total: 10
time_estimate: "20 minutes"
prev: "/tutorials/dice-vision/label-the-starter-set/"
next: "/tutorials/dice-vision/auto-label-the-training-set/"
toc_hide: true
---

At the end of this phase, a starter model is training in the cloud and a dataset named `dice-train` holds about 70 new, unlabeled images.
The starter model won't be very good, since it learns from only 30 images.
That's fine, because its only job is to give you a head start on labeling.
In [Phase 4](/tutorials/dice-vision/auto-label-the-training-set/) it draws a first guess at every box in the 70 new images, and you fix its mistakes, which is much faster than drawing all of those boxes by hand.

## Start the starter training job {#start-the-starter-training-job}

1. On the **DATASETS** page, open `dice-starter`.
1. Click **Train model**.
1. Select **TFLite** as the framework.
1. Name the model `dice-starter-model`.
1. Select **Object Detection** as the task type.
1. Select all six labels, `1` through `6`.
1. Click **Train model**.

{{< checkpoint >}}
On the **DATA** tab, click **MODELS** and expand **Active Training**.
The `dice-starter-model` job shows **Preparing**, **Waiting for GPU** or **Training**.
If the job fails to start with a message about too few annotations, a label has fewer than 10 boxes; add and label more images for it, as in [Phase 2](/tutorials/dice-vision/label-the-starter-set/#check-the-label-counts).
{{< /checkpoint >}}

The job runs in the cloud, so you don't need to wait for it.
A small job like this one usually finishes within 20 minutes, but it can take longer when cloud compute is busy.
Keep going with the next section.

## Capture the rest of the training set {#capture-the-rest-of-the-training-set}

Thirty images are enough for a rough starter model, but not for a model you can rely on.
The models you train in Phases 5 and 6 learn from a training set of about 100 images: the 30 starter images plus about 70 new ones.
You capture the new images now, while the starter model trains, and leave them unlabeled; in [Phase 4](/tutorials/dice-vision/auto-label-the-training-set/) the starter model labels them for you, and then you add the 30 starter images.
They go in a new dataset, `dice-train`, so `dice-starter` stays fully labeled.

1. On the **DATA** tab, click **DATASETS**, then click **Create dataset**.
1. Name it `dice-train`, leave **Data type** set to **Binary Data**, and click **Create dataset**.
1. On the **CONFIGURE** tab, open the **TEST** section of the `camera` card.
1. Roll, click **Add to dataset**, select `dice-train`, and confirm.
1. Repeat until you've added about 70 images.

Vary the rolls as you did in [Phase 1](/tutorials/dice-vision/capture-a-starter-set/): one to five dice, different positions, some touching.
Keep the camera at the same height and angle.
Other conditions, such as a different height or dim light, are for the hard test dataset in [Phase 7](/tutorials/dice-vision/build-the-test-datasets/), where they show how well each model handles scenes it hasn't seen.

{{< checkpoint >}}
`dice-train` on the **DATASETS** page shows about 70 images.
If the count is lower, check that you selected `dice-train`, not `dice-starter`, each time.
If an image shows no dice or a blurry roll, remove it from the dataset.
{{< /checkpoint >}}

## Troubleshooting {#troubleshooting}

{{% expand "The training job shows Failed" %}}
On the **MODELS** tab, expand **Active Training**, click the job, and read its logs.
The most common cause is a label with fewer than 10 boxes.
See [Train a model](/train/train-a-model/#troubleshooting) for other causes.
{{% /expand %}}

In the next phase, once the starter model finishes training, you use it to label the 70 new images.

{{< workshop-nav >}}
