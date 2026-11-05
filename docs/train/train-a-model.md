---
linkTitle: "Built-in training"
title: "Train a vision model with built-in training"
weight: 20
layout: "docs"
type: "docs"
description: "Train an image classification or object detection model from a labeled image dataset with built-in training."
capabilities: ["ml-training"]
diataxis: how-to
date: "2025-01-30"
updated: "2026-10-29"
aliases:
  - /build/train/train-a-model/
  - /data-ai/ai/train/
---

Train an image classification or object detection model from a dataset of labeled images, with no training code.
Viam runs the job on cloud GPUs and saves the trained model in your organization's registry.
<span id="upload-your-training-script"></span><span id="click-for-more-information-on-parsing-command-line-inputs"></span>To train any other kind of model, such as a robot policy or a PyTorch model, use a [custom training script](/train/custom-training-scripts/); to choose between the two, see [Built-in or custom training](/train/overview/#training-method).

## Prerequisites {#prerequisites}

- A dataset of labeled images: tags for classification, or bounding boxes for object detection.
  To make one, see [Create a dataset](/train/create-a-dataset/) and [Annotate data](/train/annotate-data/).
  For tips on making it a good one, see [Prepare a dataset for training](/train/create-a-dataset/#prepare-a-dataset-for-training).

Built-in training rejects a job if the dataset doesn't meet these minimums:

| Requirement        | Minimum                                                             |
| ------------------ | ------------------------------------------------------------------- |
| Labeled images     | 80% of the dataset                                                  |
| Examples per label | 10 images (classification) or 10 bounding boxes (object detection)  |
| Total images       | 15 (object detection only; classification has no total-image floor) |

Built-in training uses only the images in a dataset and skips any other files, such as video or audio.
It can't train on a [sequence dataset](/train/create-a-dataset/).

## Choose a framework {#choose-a-framework}

The framework sets which software runs the model on your machine.
Built-in training produces either one:

|                        | TFLite                                                                                        | TensorFlow                                                                                                                                                          |
| ---------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Choose it when         | You aren't sure, or the model runs on a small computer such as a Raspberry Pi                 | Your machine has an NVIDIA GPU you want the model to use                                                                                                            |
| Runs on the machine in | [`tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu), on the CPU of almost any machine | [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu), or [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) on an NVIDIA GPU |
| Resources              | Made for devices with little memory and compute                                               | Needs more memory and compute, and takes longer to train                                                                                                            |

For the platforms each service supports, see [What runs the model](/train/deploy-a-model/#what-runs-the-model).

## 1. Start a training job {#start-a-training-job}

{{< tabs >}}
{{% tab name="Viam app" %}}

1. In the Viam app, go to **DATA** > **DATASETS** and click the dataset you want to train on.
1. Click **Train model**.
1. Select **New model**.
   To retrain a model you already have, select **New version** and pick the model instead.
1. Select **Built-in (TensorFlow Lite)** or **Built-in (TensorFlow)**.
1. Enter a **Name** for the model, such as `part-inspector`.
   The name identifies the model in your organization's registry.
1. Select the task type: **Single label classification**, **Multi label classification**, or **Object detection**.
   It must match how you labeled the dataset.
1. Select the labels to train on.
   Multi label classification needs at least two. Leave out labels with too few examples or that you don't want the model to learn.
1. Click **Train model**.

{{% /tab %}}
{{% tab name="CLI" %}}

```sh {class="command-line" data-prompt="$"}
viam train submit managed \
  --dataset-id=<dataset-id> \
  --model-org-id=<org-id> \
  --model-name=part-inspector \
  --model-type=single_label_classification \
  --model-framework=tflite \
  --model-labels=good-part,defective-part
```

Set `--model-type` to `single_label_classification`, `multi_label_classification`, or `object_detection`, and `--model-framework` to `tflite` or `tensorflow`.
`--model-version` is optional and defaults to the current timestamp.
If `--model-name` is already a model in your organization, the job adds a new version of it.

{{% /tab %}}
{{% tab name="Python" %}}

The SDKs can't choose a framework: a job submitted from code always trains a TFLite model.

```python
from viam.proto.app.mltraining import ModelType

# viam_client is a connected ViamClient
ml_training_client = viam_client.ml_training_client

job_id = await ml_training_client.submit_training_job(
    org_id="<org-id>",
    dataset_id="<dataset-id>",
    model_name="part-inspector",
    model_version="1",
    model_type=ModelType.MODEL_TYPE_SINGLE_LABEL_CLASSIFICATION,
    tags=["good-part", "defective-part"],
)
print(f"Training job: {job_id}")
```

{{% /tab %}}
{{% tab name="Go" %}}

The SDKs can't choose a framework: a job submitted from code always trains a TFLite model.

```go
// viamClient is a connected *app.ViamClient
mlTrainingClient := viamClient.MLTrainingClient()

jobID, err := mlTrainingClient.SubmitTrainingJob(
    ctx,
    app.SubmitTrainingJobArgs{
        DatasetID:      "<dataset-id>",
        OrganizationID: "<org-id>",
        ModelName:      "part-inspector",
        ModelVersion:   "1",
    },
    app.ModelTypeSingleLabelClassification,
    []string{"good-part", "defective-part"},
)
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Training job: %s\n", jobID)
```

{{% /tab %}}
{{< /tabs >}}

The job starts, and you get its job ID.
Training is billed by usage; see [pricing](https://www.viam.com/product/pricing).

## 2. Monitor the training job {#monitor-the-training-job}

A job's status is **Pending** while it waits to start, then **In Progress**, and ends as **Completed**, **Failed**, or **Canceled**.
You get an email when it finishes.

{{< tabs >}}
{{% tab name="Viam app" %}}

1. In the Viam app, go to **DATA** > **MODELS** and expand **Active Training**.
   It lists your organization's training jobs with their status.
1. Click a job ID to see its details and logs.

{{% /tab %}}
{{% tab name="CLI" %}}

Check one job, and read its logs:

```sh {class="command-line" data-prompt="$"}
viam train get --job-id=<job-id>
viam train logs --job-id=<job-id>
```

List your organization's training jobs:

```sh {class="command-line" data-prompt="$"}
viam train list --org-id=<org-id> --job-status=unspecified
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
job = await ml_training_client.get_training_job(id="<job-id>")
print(f"Status: {job.status}")

# List your organization's training jobs
for job in await ml_training_client.list_training_jobs(org_id="<org-id>"):
    print(f"{job.id}: {job.status}, model {job.model_name}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
job, err := mlTrainingClient.GetTrainingJob(ctx, "<job-id>")
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Status: %v\n", job.Status)

// List your organization's training jobs
jobs, err := mlTrainingClient.ListTrainingJobs(ctx, "<org-id>", app.TrainingStatusUnspecified)
if err != nil {
    logger.Fatal(err)
}
for _, j := range jobs {
    fmt.Printf("%s: %v, model %s\n", j.ID, j.Status, j.ModelName)
}
```

{{% /tab %}}
{{< /tabs >}}

Training logs are kept for 7 days after the job finishes.
Copy them before then if you need them longer.

## 3. Verify the trained model {#verify-the-trained-model}

<span id="test-the-model"></span><span id="evaluate-against-a-test-dataset"></span><span id="test-on-a-machine"></span>When the job's status is **Completed**, the model is in your organization's registry.
In the Viam app, go to **DATA** > **MODELS** and click the model's name to open its details page, which lists its versions.

Built-in training holds back part of the dataset to validate the model, but it doesn't report loss curves or test results.
To see how the model does on images it hasn't seen, [evaluate it on a labeled test dataset](/train/evaluate-a-model/) before you deploy it.

## Troubleshooting {#troubleshooting}

{{< expand "The training job fails" >}}

- **Check the training logs.** The error message usually says what went wrong.
- **The dataset is too small.** Check it against the minimums in [Prerequisites](#prerequisites).
- **Fewer than two labels are selected for multi label classification.** Multi label classification needs at least two labels.
- **Bounding boxes are out of range.** For object detection, box coordinates must be between 0.0 and 1.0, with `x_min` less than `x_max`.

{{< /expand >}}

{{< expand "The model gives low confidence scores" >}}

- **Add more training images.** Low confidence usually means the model hasn't seen enough varied examples of each label.
- **Balance the labels.** If one label dominates the dataset, the model may give low confidence to the others.
- **Check image quality.** Blurry, dark, or low-resolution images make it harder for the model to learn.
- **Lower the confidence threshold.** If the model is right but scores around 0.4 to 0.6, your threshold may be too high.

{{< /expand >}}

{{< expand "Training takes a long time" >}}

- **Large datasets take longer.** A dataset with thousands of images can take an hour or more.
- **TensorFlow takes longer than TFLite.** If training time matters, use TFLite.
- **The job is waiting to start.** A job stays **Pending** while the training infrastructure is busy; jobs run in order.

{{< /expand >}}

## What's next {#whats-next}

- [Evaluate a model](/train/evaluate-a-model/): measure the model's precision and recall on a labeled test dataset.
- [Deploy a model to a machine](/train/deploy-a-model/): add the model, an ML model service, and a vision service to your machine.
- [Detect objects (2D)](/vision/object-detection/detect/): use an object detection model to find objects in camera images.
- [Classify images](/vision/classify/): use a classification model to sort what your camera sees.
- [Automate annotation](/train/automate-annotation/): label new images faster with your trained model.
