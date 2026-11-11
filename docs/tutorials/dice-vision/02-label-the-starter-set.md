---
title: "Phase 2: Label the starter set"
linkTitle: "2. Label the starter set"
weight: 20
type: "docs"
layout: "docs"
slug: "label-the-starter-set"
description: "Draw a bounding box around every die in the starter dataset and label each box with the die's value."
capabilities: ["datasets"]
diataxis: workshop
date: "2026-11-06"
workshop: "dice-vision"
phase: 2
phase_total: 10
time_estimate: "20 minutes"
prev: "/tutorials/dice-vision/capture-a-starter-set/"
next: "/tutorials/dice-vision/train-a-starter-model/"
toc_hide: true
---

At the end of this phase, every die in `dice-starter` has a box around it labeled with its value, at least 10 times for each face.
That's the minimum a training job accepts, and it's what the starter model in [Phase 3](/tutorials/dice-vision/train-a-starter-model/) learns from.
This is the only time you label a whole dataset by hand, so it's worth being careful: about 100 boxes, one die at a time.

## Draw a box on every die {#draw-a-box-on-every-die}

Use the labels `1`, `2`, `3`, `4`, `5` and `6`, for the number of pips on the top face.

1. On the **DATASETS** page, open `dice-starter` and click the first image.
1. In the side panel, click the **Actions** tab, then click **Annotate**.
1. Select or create the label for the first die's top face, for example `4`.
1. Hold **Cmd** (macOS) or **Ctrl** (Linux) and drag a rectangle tightly around the die.
1. Repeat for every die in the image, then move to the next image.

For more on the annotation tools, see [Annotate images](/train/annotate-data/).

Follow these rules on every image, here and in later phases:

- Box the whole die, edge to edge, with as little background as possible.
- Label the face pointing at the camera, not a side face.

Your boxes should look like these, with each one tight around a die, including dice that touch:

{{< imgproc src="/tutorials/dice-vision/annotated-examples.jpg" resize="1200x" declaredimensions=true class="imgzoom shadow" alt="Three images from a labeled starter dataset, with a tight box around every die and each box labeled with the die's top face: four dice spread apart, three dice in a diagonal line, and four dice touching in a cluster." >}}

{{< checkpoint >}}
Every image in `dice-starter` shows a labeled box on each die.
If you find a die with no box, go back and box it; otherwise the model learns that a die can be background.
{{< /checkpoint >}}

## Check the label counts {#check-the-label-counts}

1. On the **DATASETS** page, open `dice-starter`.
1. In the dataset's side panel, find **Bounding box labels**.
   Each row shows how many images use the label and, in parentheses, how many boxes have it.

{{< imgproc src="/tutorials/dice-vision/dice-starter-labels.webp" resize="1200x" declaredimensions=true class="imgzoom shadow" alt="The dice-starter dataset page with 30 images. The side panel's Bounding box labels list shows labels 1 to 6, each with at least 10 boxes, from 3 with 17 images and 23 labels down to 4 with 10 images and 13 labels." >}}

The **Unlabeled** count under **Classifications and tags** counts images with no classification tag.
This workshop uses bounding boxes, not tags, so that count stays at 30.
It doesn't affect training: when you train an object detection model, the 20% unlabeled limit counts only images with no box for any label you train on, and classification tags don't count.

{{< checkpoint >}}
Each label, `1` through `6`, has at least 10 boxes, and **Bounding box labels** shows no **Unlabeled** row.
If you see a label you didn't mean to create, such as `l` or `six`, relabel its boxes and delete it.
If a face has fewer, go back to the **Test** section of the `camera` card on the **CONFIGURE** tab, add a few images where that face is on top, and label them.
A training job won't start with fewer than 10 boxes for any label you train on.
{{< /checkpoint >}}

In the next phase, you train a starter model on these 30 images, and capture the rest of your training images while it trains.

{{< workshop-nav >}}
