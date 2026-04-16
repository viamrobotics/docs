---
linkTitle: "Train a model"
title: "Train a model"
weight: 20
layout: "docs"
type: "docs"
description: "Train a classification or object detection model from a labeled dataset."
date: "2025-01-30"
aliases:
  - /build/train/train-a-model/
  - /data-ai/ai/train/
---

Submit a training job from your labeled dataset. Viam runs the job on
GPU-backed cloud infrastructure -- no framework installation or GPU
provisioning needed on your part. Training is part of the Viam platform;
see [pricing](https://www.viam.com/product/pricing) for plan details.
Training logs are available for 7 days after the job completes.

For background on model frameworks (TFLite and TensorFlow), task types, and
how deployment works, see the [overview](/train/overview/).

Managed training uses a fixed internal train/validation split and does not
currently expose loss curves or a separate test-dataset option. To evaluate
a trained model, see [Test your model](#4-test-your-model) below.

## 1. Start a training job from the web UI

1. Go to [app.viam.com](https://app.viam.com).
2. Click the **DATA** tab in the top navigation.
3. Click the **DATASETS** subtab.
4. Click the dataset you want to train on.
5. Click **Train model**.
6. Select the model framework:
   - **TFLite** for edge devices (recommended for most use cases)
   - **TF** for general-purpose models requiring more compute
7. Enter a name for your model. Use a descriptive name like
   `part-inspector-v1` or `package-detector-v1`. This name identifies the model
   in your organization's registry.
8. Select the task type:
   - **Single Label Classification** if each image has one tag
   - **Multi Label Classification** if images have multiple tags
   - **Object Detection** if you used bounding box annotations
9. Select which labels to include in training. You can exclude labels that have
   too few examples or that you do not want the model to learn.
10. Click **Train model**.

The training job starts. You will see a confirmation message with the job ID.

## 2. Start a training job from the CLI

If you prefer the command line, use the Viam CLI:

```bash
viam train submit managed \
  --dataset-id=YOUR-DATASET-ID \
  --model-org-id=YOUR-ORG-ID \
  --model-name=part-inspector-v1 \
  --model-type=single_label_classification \
  --model-framework=tflite \
  --model-labels=good-part,defective-part
```

**Required flags:**

| Flag                | Description                       | Accepted values                                                                 |
| ------------------- | --------------------------------- | ------------------------------------------------------------------------------- |
| `--dataset-id`      | Dataset to train on               | Your dataset ID                                                                 |
| `--model-org-id`    | Organization to save the model in | Your organization ID                                                            |
| `--model-name`      | Name for the trained model        | Any string                                                                      |
| `--model-type`      | Task type                         | `single_label_classification`, `multi_label_classification`, `object_detection` |
| `--model-framework` | Model framework                   | `tflite`, `tensorflow`                                                          |
| `--model-labels`    | Labels to train on                | Comma-separated list of labels from your dataset                                |

`--model-version` is optional and defaults to the current timestamp.

The command returns a training job ID that you can use to check status.

## 3. Monitor training progress

**Web UI:**

1. In the Viam app, click the **DATA** tab.
2. Click the **MODELS** subtab, then expand **Active Training**.
3. You will see a list of training jobs with their status:
   - **Pending** -- the job is queued
   - **In Progress** -- training is running
   - **Completed** -- the model is ready
   - **Failed** -- something went wrong
   - **Canceled** -- the job was canceled before completing
4. Click a job ID to view detailed logs.

**CLI:**

Check the status of a training job:

```bash
viam train get --job-id=YOUR-JOB-ID
```

View training logs:

```bash
viam train logs --job-id=YOUR-JOB-ID
```

Training logs expire after 7 days. If you need to retain logs for longer,
copy them before they expire.

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def main():
    viam_client = await connect()
    ml_training_client = viam_client.ml_training_client

    job = await ml_training_client.get_training_job(
        id="YOUR-TRAINING-JOB-ID",
    )
    print(f"Status: {job.status}")
    print(f"Model name: {job.model_name}")
    print(f"Created: {job.created_on}")

    viam_client.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
job, err := mlTrainingClient.GetTrainingJob(ctx, "YOUR-TRAINING-JOB-ID")
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Status: %s\n", job.Status)
fmt.Printf("Model name: %s\n", job.ModelName)
fmt.Printf("Created: %s\n", job.CreatedOn)
```

{{% /tab %}}
{{< /tabs >}}

## 4. Test your model

You can evaluate a trained model two ways: offline against a held-out test
dataset, or live on a machine.

### Test offline against a test dataset

Run the model against images it has not seen using auto-predictions. This
lets you evaluate performance without configuring a machine.

1. [Create a test dataset](/train/create-a-dataset/) with images that were
   not used for training.
2. Go to the dataset's page and click **Get auto-predictions**.
3. Select your trained model and a confidence threshold.
4. Click **Get predictions**, then **Review predictions** once they finish.
5. For each prediction, **Accept (A)** or **Reject (R)**.

The accept/reject tally tells you how the model performs on unseen data.

### Test live on a machine

Deploy the model to a machine with a camera to see its predictions on live or
captured data.

1. [Deploy the model](/train/deploy-a-model/) to a machine with a camera.
2. [Configure a vision service](/vision/configure/) that uses the model.
3. On the machine's **CONTROL** tab, open the vision service panel to see live classifications or detections.
4. Evaluate the results against a variety of conditions:
   - Images that clearly belong to each class (should get high confidence)
   - Ambiguous images (helps you understand the model's decision boundary)
   - Images from conditions not in the training set (reveals generalization gaps)

## 5. Deploy and iterate

When training completes, the model is stored in your organization's registry.
See [Deploy a model to a machine](/train/deploy-a-model/) to configure the
module, ML model service, and vision service on your machine.

After deploying, improve your model by collecting targeted data where it
struggles (edge cases, counterexamples, varied conditions), using
[auto-annotation](/train/automate-annotation/) to label efficiently, and
retraining. If your machine is configured to use the model, the new version
deploys automatically.

To review past training jobs:

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def main():
    viam_client = await connect()
    ml_training_client = viam_client.ml_training_client

    jobs = await ml_training_client.list_training_jobs(
        org_id=ORG_ID,
    )
    for job in jobs:
        print(f"Job: {job.id}, Status: {job.status}, "
              f"Model: {job.model_name}, Created: {job.created_on}")

    viam_client.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
jobs, err := mlTrainingClient.ListTrainingJobs(
    ctx, orgID, app.TrainingStatusUnspecified)
if err != nil {
    logger.Fatal(err)
}
for _, job := range jobs {
    fmt.Printf("Job: %s, Status: %d, Model: %s, Created: %s\n",
        job.ID, job.Status, job.ModelName, job.CreatedOn)
}
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Training job fails" >}}

- **Check the training logs.** In the **MODELS** tab, expand **Active Training**
  and click the failed job ID to view logs. The error message usually indicates
  the problem.
- **Dataset too small.** Training requires at least 15 images with at least 80%
  labeled. Check your dataset in the **DATASETS** tab.
- **No labels selected.** You must select at least two labels. A model cannot
  learn to classify if there is only one category.
- **Bounding box format issue.** For object detection, verify that bounding box
  coordinates are normalized between 0.0 and 1.0, and `x_min` is less than
  `x_max`.

{{< /expand >}}

{{< expand "Low confidence scores" >}}

- **Add more training data.** Low confidence usually means the model has not seen
  enough examples. More diverse images of each class will help.
- **Check label balance.** If one label dominates the dataset, the model may
  assign low confidence to minority labels. Balance the dataset and retrain.
- **Verify image quality.** Blurry, dark, or low-resolution images make it
  harder for the model to learn distinctive features.
- **Lower the confidence threshold.** If the model is correct but with scores
  around 0.4-0.6, your threshold may be set too high.

{{< /expand >}}

{{< expand "Training takes too long" >}}

- **Large datasets take longer.** A dataset with thousands of images may take an
  hour or more. This is normal.
- **TF models take longer than TFLite.** If training time is a concern, switch
  to TFLite.
- **Training is queued.** If the status stays at "Pending", the training
  infrastructure may be busy. Jobs are processed in order.

{{< /expand >}}

## What's next

- [Deploy a model to a machine](/train/deploy-a-model/) -- configure the module,
  ML model service, and vision service to run your model.
- [Add computer vision](/vision/configure/) -- the full guide to configuring
  vision services and cloud inference.
- [Detect objects (2D)](/vision/object-detection/detect/) -- use your
  object detection model to find and locate objects in camera images.
- [Classify images](/vision/classify/) -- use your
  classification model to categorize images from your machine's camera.
