---
linkTitle: "Evaluate a model"
title: "Evaluate a model on a labeled dataset"
weight: 27
layout: "docs"
type: "docs"
description: "Measure how accurately a classification or detection model labels images by running it against a dataset you labeled."
capabilities: ["ml-models", "datasets"]
diataxis: how-to
date: "2026-11-04"
---

Find out how well a classification or detection model does before you deploy it.
An evaluation runs the model on a dataset of images you labeled and compares its predictions with your labels.
For each label, it reports how many of the model's predictions were right and how many of your labels the model found.

{{< alert title="What evaluation doesn't support" color="note" >}}
You can't evaluate:

- robot policies, or models with the **Other** task type
- PyTorch models, or models in the **Registry** framework
- files other than JPEG and PNG images; the evaluation skips any other files in the dataset

Evaluation is available only in the Viam app, not from the CLI or the SDKs.
It doesn't report mean average precision (mAP) for detection models.
{{< /alert >}}

## Prerequisites {#prerequisites}

- A single label classification, multi label classification, or object detection model in your organization's registry, in the TensorFlow, TensorFlow Lite, or ONNX framework.
  [Train one with built-in training](/train/train-a-model/), [train one with a custom training script](/train/custom-training-scripts/), or [upload one](/vision/deploy-and-maintain/deploy-custom-model/).
- JPEG or PNG images like the ones the model will see on your machines, that weren't used to train the model.
  See [Capture and sync data](/data/capture-sync/capture-and-sync-data/).

## How evaluation works {#how-evaluation-works}

The evaluation treats your labels as the right answers.
It runs the model on each image, keeps the predictions at or above a confidence threshold you set, and compares them with the image's labels:

- A prediction that matches a label on the image is correct.
- A prediction of a label the image doesn't have is a false alarm.
- A label on the image that the model didn't predict is a miss.

For a detection model, a predicted box matches a labeled box only if they overlap enough.
Overlap is measured as intersection over union (IoU): the area the two boxes share, divided by the total area they cover.
It runs from 0, for boxes that don't touch, to 1, for identical boxes.

Only the labels the model can predict are scored.
The Viam app calls these the model's classes.
An image with no labels shows none of them, so any prediction on it is a false alarm.
An image whose labels are all ones the model can't predict is skipped.

An evaluation only reads the dataset.
Unlike [auto-predictions](/train/automate-annotation/), it doesn't add labels or predictions to your images.
Each image the model runs on is billed as one cloud inference.

## 1. Create a test dataset {#create-a-test-dataset}

The test dataset is separate from the dataset you trained the model on.
If you evaluate on the training images, the results show how well the model remembers them, not how it does on new ones.
An image can belong to more than one dataset, so don't add the test images to the training dataset too.

1. [Create a dataset](/train/create-a-dataset/) and add the test images.
   Include images without any of the objects the model looks for, so the results show what the model flags by mistake.
   Include the conditions the model meets on your machines, such as different lighting, angles, and backgrounds, and images that are hard to tell apart.
1. [Label every image](/train/annotate-data/) with each of the model's labels that applies to it.
   Use tags or classifications for a classification model, and bounding boxes for a detection model.
   A label you leave off turns the model's correct prediction into a false alarm.

You can draft the labels with [auto-predictions](/train/automate-annotation/) and review each one, but use a different model from the one you're evaluating.
Labels drafted by the same model agree with its own predictions, so its scores come out higher than they should.

## 2. Start an evaluation {#start-an-evaluation}

1. In the Viam app, go to **DATA** > **DATASETS** and click your test dataset.
1. Click **Run model**, then **Evaluate model performance**.
   You can also click **Evaluations** in the dataset's sidebar, then **New evaluation**.
1. Select the model and a version, then click **Next**.
1. Set the **Confidence threshold**, the minimum score a prediction needs to count.
   The default is 0.5.
   Use the threshold you plan to run the model with on your machines.
1. For an object detection model, set the **IoU (Intersection over Union) threshold**, the minimum overlap for a predicted box to match a labeled box.
   The default is 0.5.
   Raise it if your application needs boxes that fit the object closely.
1. Click **Next**, check the settings, and click **Run evaluation**.

You can't change the thresholds after the job starts.
To compare thresholds, run one evaluation for each.

The Viam app opens the dataset's **Evaluations** page, where the job shows as **Running**.
To stop it, click the cancel button on its row.

## 3. Verify the results {#verify-the-results}

When the job's status changes to **Completed**, its row on the **Evaluations** page shows:

- **Precision**: of the model's predictions, the percentage that were correct.
  Low precision means many false alarms.
- **Recall**: of the labels in the dataset, the percentage the model found.
  Low recall means many misses.
- The number of images evaluated, which leaves out the images the evaluation skipped.

These overall values average the scores of every label that both the model and the dataset use, with each label counting equally, however many images it's on.
A green dot next to a value means 85% or higher, yellow means 70% to 85%, and red means below 70%.

Click the arrow at the start of the row to open the **Per-class breakdown**.
For each label, it shows how many times the dataset uses the label, its precision and recall, and its F1 score, with the most-used labels first.
The F1 score combines precision and recall into one number, which is high only when both are high.
An overall score can look good while one label does badly, so check each label you depend on.
A label used only a few times gives a less reliable score; add more images of it to the test dataset before you trust it.

To improve a weak label, add training images where the model struggles, label them, and [train a new version](/train/train-a-model/).
Then evaluate the new version on the same test dataset with the same thresholds, so the results compare directly.

## Troubleshooting {#troubleshooting}

{{< expand "The model I want to evaluate is unavailable" >}}

The model is a kind that evaluation doesn't support; see the note at the top of this page.
The model picker shows the reason next to each model it can't run.

{{< /expand >}}

{{< expand "Evaluate model performance is unavailable" >}}

The dataset has no images.
Add images to it, then try again.

{{< /expand >}}

{{< expand "The job fails" >}}

Point to the icon next to **Failed** to see the error.

- **"This model has no labels.txt file, so its predictions cannot be scored."** The evaluation reads the labels the model can predict from the `labels.txt` file in its package.
  Upload a version of the model that includes one.
- **"The inference service is unavailable right now."** Start the evaluation again in a few minutes.

{{< /expand >}}

{{< expand "The per-class breakdown says no per-class metrics" >}}

None of the dataset's labels match the labels the model can predict.
Check that they're spelled exactly the same, including capitalization, and that the label type matches the model: bounding boxes for a detection model, tags or classifications for a classification model.

{{< /expand >}}

## What's next {#whats-next}

- [Deploy a model to a machine](/train/deploy-a-model/): run the model on your machine once it does well enough.
- [Annotate data](/train/annotate-data/): label more training images of the labels the model struggles with.
- [Automate annotation](/train/automate-annotation/): have a model draft labels for new training images, so each round takes less hand-labeling.
- [Retrain a model](/vision/deploy-and-maintain/retrain/): keep a deployed model accurate as conditions change.
