---
title: "Phase 4: Auto-label the training set"
linkTitle: "4. Auto-label the training set"
weight: 40
type: "docs"
layout: "docs"
slug: "auto-label-the-training-set"
description: "Use the starter model to predict boxes on the training dataset, then accept, reject and fix each prediction, and add the starter images."
capabilities: ["datasets", "ml-models"]
diataxis: workshop
date: "2026-11-06"
draft: true
workshop: "dice-vision"
phase: 4
phase_total: 10
time_estimate: "20 minutes"
prev: "/tutorials/dice-vision/train-a-starter-model/"
next: "/tutorials/dice-vision/train-a-built-in-model/"
toc_hide: true
---

At the end of this phase, `dice-train` holds about 100 labeled images: the 70 new ones, whose boxes mostly came from your starter model rather than your mouse, and your 30 starter images.
The starter model learned from only 30 images, so expect it to miss dice and misread some faces.
Your job is to review its guesses: accept the right ones, reject the wrong ones, and draw what it missed.

## Get predictions from the starter model {#get-predictions-from-the-starter-model}

1. On the **DATA** tab, click **MODELS** and check that `dice-starter-model` shows **Completed**.
   If it's still training, wait for it to finish.
1. On the **DATASETS** page, open `dice-train`.
1. Click **Run model**, then click **Get auto-predictions**.
1. Select `dice-starter-model` and its latest version.
1. Set the confidence threshold to `0.25`.
1. Click **Get predictions**.

A low threshold makes the starter model suggest a box even when it isn't sure.
You'll reject more wrong guesses, but you'll draw fewer boxes from scratch, which takes longer.

{{< checkpoint >}}
After a minute or two, the dataset page shows that predictions are ready, with a **Review predictions** button.
If it reports no predictions, run it again with a lower confidence threshold, such as `0.1`.
{{< /checkpoint >}}

## Review every prediction {#review-every-prediction}

The review screen shows each of the starter model's guesses as a dashed box on the image.
The **Predictions** panel on the right lists the same guesses by label, each with its confidence score, a check mark to accept it, and an **X** to reject it.
A box's color shows its label, not whether it's right, so check every box against the die under it.

1. On the **DATASETS** page, open `dice-train` and click **Review predictions**.
1. For each prediction in the **Predictions** panel, click the check mark to accept it or the **X** to reject it.
   Accept a box that's around one die and has the value on its top face.
   Reject a box that has the wrong value or isn't around a die.
1. Draw a box on every die that has none, as you did in [Phase 2](/tutorials/dice-vision/label-the-starter-set/#draw-a-box-on-every-die), including dice whose prediction you rejected.
1. Move to the next image and repeat until you've reviewed them all.

**Accept all** (**A**) and **Reject all** (**R**) act on every prediction in the image at once.
Use them only when every box in the image is right, or every box is wrong.

### Examples {#examples}

In this image, the starter model got two dice right, misread one, and missed one:

{{< imgproc src="/tutorials/dice-vision/review-predictions-1.png" resize="960x" declaredimensions=true class="imgzoom shadow" alt="The review screen with four dice. Dashed boxes mark a blue die predicted 6, a red die predicted 2, and a green die predicted 6. A tan die has no box. The Predictions panel lists 2 at 0.4, and 6 at 0.53 and 0.47." >}}

- **Blue die, `6` at 0.53:** the top face shows six pips. Accept.
- **Red die, `2` at 0.4:** the top face shows two pips. Accept.
- **Green die, `6` at 0.47:** the top face shows four pips; the model is reading the side faces. Reject, then draw a box labeled `4`.
- **Tan die, no box:** the model missed it. Draw a box labeled `2`.

In this image, the starter model got only one die right:

{{< imgproc src="/tutorials/dice-vision/review-predictions-2.png" resize="960x" declaredimensions=true class="imgzoom shadow" alt="The review screen with four dice clustered together, each with a dashed box. The Predictions panel lists 1 at 0.47, 2 at 0.34, 2 at 0.31, and 3 at 0.41." >}}

- **Green die, `2` at 0.34:** the top face shows two pips. Accept.
- **Tan die, `1` at 0.47:** the top face shows two pips. Reject, then draw a box labeled `2`.
- **Blue die, `3` at 0.41:** the top face shows four pips. Reject, then draw a box labeled `4`.
- **Red die, `2` at 0.31:** the top face shows three pips. Reject, then draw a box labeled `3`.

Confidence doesn't tell you which guesses are right: here the wrong `1` scores higher than the right `2`.
Check every box, whatever its score.

## Add the starter images to the training set {#add-the-starter-images-to-the-training-set}

Your 30 hand-labeled images belong in the training set too.
You add them now, after the review, so the starter model doesn't predict boxes on images you've already labeled.
Labels belong to the image, not the dataset, so they come with it.

1. On the **DATASETS** page, open `dice-starter`.
1. Select all 30 images.
1. Click **Add to dataset**, select `dice-train`, and click **Add**.

{{< checkpoint title="Milestone" >}}
A model you trained is labeling your data.
`dice-train` holds about 100 images, every image shows a box on each die, no predictions are left to review, and each label has at least 10 boxes.
If the starter images appear without boxes, open one and check that its labels show in `dice-starter`.
If the dataset still shows predictions to review, open it and finish them.
If some images still have no boxes, a training job will refuse the dataset when more than 20% of its images are unlabeled; label them or remove them from `dice-train`.
{{< /checkpoint >}}

This label, train, predict and correct loop is how real projects grow a dataset.
Each round, the model is better and you fix less.
When you add images later, you can auto-label them with your best model instead of the starter.
See [Automate annotation](/train/automate-annotation/).

In the next phase, you train a built-in model on the full training set.

{{< workshop-nav >}}
