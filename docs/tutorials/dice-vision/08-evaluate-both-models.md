---
title: "Phase 8: Evaluate both models and pick a winner"
linkTitle: "8. Evaluate both models"
weight: 80
type: "docs"
layout: "docs"
slug: "evaluate-both-models"
description: "Evaluate both trained models on the clean and hard test datasets, compare precision and recall, and pick a model and confidence threshold."
capabilities: ["ml-models", "datasets"]
diataxis: workshop
date: "2026-11-06"
workshop: "dice-vision"
phase: 8
phase_total: 10
time_estimate: "20 minutes"
prev: "/tutorials/dice-vision/build-the-test-datasets/"
next: "/tutorials/dice-vision/deploy-the-winning-model/"
toc_hide: true
---

At the end of this phase, you have four evaluations, one for each model on each test dataset, and you've picked the model and confidence threshold your Yahtzee scorer will use.
Scoring both models on the same images with the same thresholds turns "which model is better?" from a guess into a measurement.
Evaluation runs in the cloud, so nothing needs to be deployed yet.

## Run the four evaluations {#run-the-four-evaluations}

1. On the **DATA** tab, click **MODELS** and check that `dice-tflite` and `dice-yolo` both show **Completed**.
1. On the **DATASETS** page, open `dice-test-clean`.
1. Click **Run model**, then click **Evaluate model performance**.
1. Under **Model**, select `dice-tflite`, and under **Version**, select its latest version.
1. Set **Confidence threshold** to `0.5` and **IoU threshold** to `0.5`.
1. Click **Next**, check the settings, and click **Run evaluation**.
1. Repeat for `dice-yolo` on `dice-test-clean`, then for both models on `dice-test-hard`, with the same thresholds each time.

The IoU threshold sets how closely a predicted box must overlap the box you drew to count as a match.
At `0.5`, the two boxes must overlap by at least half.

Like auto-predictions in [Phase 4](/tutorials/dice-vision/auto-label-the-training-set/#get-predictions-from-the-starter-model), an evaluation runs the model once on each image and is billed as compute time.
These four evaluations run a model about 92 times, and the threshold evaluation later in this phase adds about 23 more.

{{< checkpoint >}}
On each test dataset's **Evaluations** page, two evaluations are listed, one per model, each showing **Precision** and **Recall**.
If you don't see an evaluation, check that you clicked **Run evaluation** at the end of the dialog.
If an evaluation fails, check that the test dataset has labeled images and that the model's latest version finished training.
{{< /checkpoint >}}

## Compare the results {#compare-the-results}

### Read an evaluation {#read-an-evaluation}

Each test dataset's **Evaluations** page lists that dataset's evaluations, one row per run, with the model, its overall **Precision** and **Recall**, and how many images it scored.

- **Precision** is the share of the model's boxes that were right. Low precision means it reads dice that aren't there or reads the wrong value.
- **Recall** is the share of the real dice the model found with the right value. Low recall means it misses dice or misreads them.

Click a row to expand its **Per-class breakdown**, which scores each label on its own:

- **Labels** is how many boxes with that label are in the test dataset.
- **Precision** and **Recall** mean the same as above, for that label only.
- **F1** combines precision and recall into one score. It's high only when both are high.

Each bar is green at 85% and above, yellow from 70%, and red below 70%.

{{< imgproc src="/tutorials/dice-vision/evaluation-per-class.png" resize="960x" declaredimensions=true class="imgzoom shadow" alt="Two per-class breakdowns from one test dataset's Evaluations page. In the first, most recall bars are red: label 5 has 100% precision and 7.1% recall, and label 4 is 0% for everything. In the second, for a YOLO model at 96.0% precision and 90.9% recall overall, every bar is green except label 2's recall at 71.4% and label 1's precision at 83.3%." >}}

In this example, two models were scored on the same 20 images:

- In the first breakdown, label `5` has 100% precision but 7.1% recall. Every time the model said `5`, it was right, but it found only 1 of the 14 fives. Label `4` is 0% across the board: the model never read a 4 correctly. Low recall alone doesn't tell you whether the model missed the other 13 fives or read them as another value; a five read as a `6` would lower the precision of label `6`, not `5`.
- In the second breakdown, every label scores at least 70%. The weakest is recall for label `2`, at 71.4%: the model missed or misread 4 of the 14 twos.

### Fill in the comparison {#fill-in-the-comparison}

Before you look at the numbers, write down a prediction: which model will drop more from `dice-test-clean` to `dice-test-hard`, and why?
Check it against your results when the table is filled in.

Each **Evaluations** page shows only one test dataset, so to compare both models on both datasets, write down the four overall results in a table like this one:

| Model         | Test dataset      | Precision | Recall |
| ------------- | ----------------- | --------- | ------ |
| `dice-tflite` | `dice-test-clean` |           |        |
| `dice-yolo`   | `dice-test-clean` |           |        |
| `dice-tflite` | `dice-test-hard`  |           |        |
| `dice-yolo`   | `dice-test-hard`  |           |        |

For Yahtzee, both matter: a missed die and a misread die both give a wrong score.
Look at three things:

1. Which model scores higher on `dice-test-clean`.
1. How much each model drops from `dice-test-clean` to `dice-test-hard`. A small drop means the model copes with conditions it didn't train on.
1. The **Per-class breakdown** for each model. A face with low recall is one the model often misses or misreads. The breakdown doesn't show which face the model mistook a die for, only that it got that face wrong.

Pick the model with the higher recall on `dice-test-hard`, unless its precision on `dice-test-hard` is more than 5 points lower than the other model's.
The rest of this workshop calls it the winning model.

{{< checkpoint >}}
Your table has four rows filled in, you've picked a winning model, and you've checked your prediction.
If both models have the same recall on `dice-test-hard`, pick the one with the higher precision there.
If both models score close to 100% on both test datasets, your hard test dataset isn't hard enough to separate them; either model works for Yahtzee.
{{< /checkpoint >}}

## Pick a confidence threshold {#pick-a-confidence-threshold}

A model gives each box a confidence score.
A lower threshold keeps more boxes, so recall goes up and precision usually goes down.

1. Run one more evaluation of the winning model on `dice-test-hard`, with **Confidence threshold** set to `0.25` and **IoU threshold** at `0.5`.
1. Compare it with the `0.5` result.
1. Pick the threshold with the higher recall, unless its precision is more than 5 points lower.

{{< checkpoint title="Milestone" >}}
You have a measured answer to which model reads dice better, and the threshold to run it at.
If the two thresholds give the same results, use `0.5`.
{{< /checkpoint >}}

## Refine your model {#refine-your-model}

If even the winning model misreads too many dice, the evaluation tells you where it's weak, and that tells you what to change.
Most fixes add training images and train a new version of the model:

- **One face scores low in the per-class breakdown.** The model hasn't seen that face often enough. Capture 10 to 20 more training images with that face on top.
- **The model does well on `dice-test-clean` but poorly on `dice-test-hard`.** It hasn't learned to cope with conditions outside its training images. Capture training images in the conditions it struggles with, such as touching dice or a different background. The old hard test images still score the model fairly, but they no longer show how it copes with conditions it never trained on, so capture a few new hard images in a condition you didn't add.
- **The model misses dice everywhere, with low recall on most labels.** It needs more to learn from. Capture more training images of every kind, or, for `dice-yolo`, train with more epochs.

To retrain:

1. Add the new images to `dice-train` from the **Test** section of the `camera` card, as in [Phase 3](/tutorials/dice-vision/train-a-starter-model/#capture-the-rest-of-the-training-set).
1. Label them with auto-predictions from your winning model, as in [Phase 4](/tutorials/dice-vision/auto-label-the-training-set/). It's more accurate than the starter model, so you fix fewer boxes.
1. On the **DATASETS** page, open `dice-train` and click **Train model**.
1. Select **New version**, select the model under **Existing model**, and train as before.
1. When the new version finishes, run its evaluations on the same test datasets with the same thresholds, and compare them with the old ones.

Never add test images to `dice-train`.
A model scored on images it trained on looks better than it really is.

Choosing has a similar, smaller effect.
Once you've used the test datasets to pick a model and a threshold, their scores overstate how well that model reads rolls it's never seen, and each round of retraining against them adds to that.
If you retrain more than once or twice, capture fresh test datasets for your final comparison.

In the next phase, you deploy the winning model to your machine and see it read dice live.

{{< workshop-nav >}}
