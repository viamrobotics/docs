---
linkTitle: "Evaluate model"
title: "Evaluate a model on a labeled dataset"
weight: 52
layout: "docs"
type: "docs"
description: "Evaluate the performance of your ML model against a labeled dataset to measure precision, recall, and F1 score before deploying."
date: "2026-04-06"
---

You can evaluate your model's performance by running it against a labeled dataset.
Evaluation computes precision, recall, and F1 score to measure how well your model performs before deployment.

## Prerequisites

{{%/* expand "A trained ML model in the registry" */%}}

Train a model using one of these methods:

- [Train a TensorFlow or TensorFlow Lite model](/data-ai/train/train-tf-tflite/)
- [Train other models](/data-ai/train/train/)

{{%/* /expand */%}}

{{%/* expand "A labeled dataset" */%}}

Follow the instructions to [create a dataset](/data-ai/train/create-dataset/) and [annotate images](/data-ai/train/annotate-images/).

The dataset must contain labeled images that correspond to the model's output classes.
Only labels that overlap between your dataset and the model's output classes are used for evaluation.
Images without labels are skipped.

{{%/* /expand */%}}

## Evaluate a model

Navigate to the [**DATASETS** tab](https://app.viam.com/datasets) of the **DATA** page.
Select the dataset you want to use for evaluation.
Click **Evaluations** in the dataset navigation to open the evaluations page.

To start a new evaluation:

1. Click **New evaluation**.
2. Read the evaluation tips and click **Continue**.
3. Select the ML model you want to evaluate from the registry.
4. Configure the evaluation thresholds:
   - **Confidence threshold**: The minimum confidence score (0-1) for a prediction to count. The default is 0.5.
   - **IoU threshold** (object detection models only): The minimum intersection-over-union score (0-1) for a predicted bounding box to match a ground-truth box. The default is 0.5.
5. Click **Start evaluation**.

The evaluation job runs inference on each image in your dataset and compares predictions against your ground-truth labels.

## View evaluation results

After the evaluation completes, view the results in the evaluations table.
The table shows:

- **Model**: The registry item name and version
- **Type**: The model type (classification or object detection)
- **Precision**: The percentage of model predictions that were correct
- **Recall**: The percentage of ground-truth labels that the model detected
- **Images**: The number of images evaluated vs. processed

Click **Details** on any evaluation to see:

- **Aggregate metrics**: Overall precision, recall, and F1 score (macro average across all classes)
- **Per-class metrics**: Precision, recall, and F1 score for each label
- **Dataset coverage**: How many images were processed and how many had ground-truth labels
- **Unevaluated classes**: Model output classes that had no matching labels in the dataset

## Understanding the metrics

**Precision** measures how accurate the model's positive predictions are.
A precision of 90% means that when the model predicts a label, it's correct 90% of the time.

**Recall** measures how completely the model finds all positive cases.
A recall of 80% means the model detects 80% of the actual instances of each label.

**F1 score** is the harmonic mean of precision and recall, providing a single metric that balances both.

For object detection models, a prediction is correct when the predicted bounding box has sufficient overlap with the ground-truth box (measured by IoU) and the label matches.

## Manage evaluation jobs

Evaluation jobs have the following statuses:

- **Provisioning**: The job is being set up
- **In progress**: The job is running inference on images
- **Completed**: The job finished successfully
- **Failed**: The job encountered an error
- **Cancelled**: The job was stopped by the user

To cancel a running evaluation, click **Cancel** next to the job in the evaluations table.

## Billing

Evaluation jobs use cloud inference to run your model on each image.
Standard cloud inference billing applies.

## Next steps

After evaluating your model and reviewing its performance:

- [Deploy the model](/data-ai/ai/deploy/) to your machine
- [Run inference](/data-ai/ai/run-inference/) using the vision service
