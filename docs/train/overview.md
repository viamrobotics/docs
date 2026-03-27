---
linkTitle: "Overview"
title: "Train ML models"
weight: 1
layout: "docs"
type: "docs"
description: "Create datasets from captured images and train ML models for classification or object detection."
---

Your machines capture images in the field. ML model training turns those images
into models that can classify what a camera sees or detect specific objects in
real time. Viam handles the training infrastructure so you can focus on your
data and your use case.

## The training workflow

Training an ML model follows a repeating cycle:

1. **Create a dataset.** Collect images from your machines into a named,
   organization-level collection. You can pull images from multiple machines
   across different locations into a single dataset.

2. **Label your images.** Tag images for classification (the whole image gets a
   label) or draw bounding boxes for object detection (each object in the image
   gets a labeled rectangle). You can label manually or use an existing model to
   auto-annotate and review predictions.

3. **Train a model.** Submit a training job and Viam runs it on cloud
   infrastructure. No GPU provisioning, no framework installation. Training
   times range from minutes to an hour depending on dataset size. When training
   completes, the model is stored in your organization's registry.

4. **Deploy to your machine.** Configure the `tflite_cpu` module and an ML
   model service on your machine. Add a vision service to apply the model to
   live camera frames. The machine pulls the model from the registry
   automatically.

5. **Iterate.** Deploy the model, collect data on its failures, auto-annotate
   new images with the current model, review the predictions, retrain, and
   redeploy. Each cycle tightens the feedback loop and improves accuracy. In ML
   this is called active learning.

## Managed training or custom scripts

Viam offers two paths for training:

**Managed training** handles everything. You select a dataset, pick a framework
and task type, and start the job. Use this for standard classification and
object detection with TFLite or TensorFlow. Most users start here.

**Custom training scripts** let you bring your own Python training code. Use
any framework (PyTorch, ONNX, or anything installable with pip), write custom
preprocessing, train on non-image data, or implement transfer learning. Viam
runs your script in the same cloud infrastructure, and the output model is
published to the registry just like a managed training job.

## Model frameworks

**TensorFlow Lite (TFLite)** produces compact models optimized for edge
devices. TFLite models run directly on single-board computers like the
Raspberry Pi without requiring a GPU. This is the right choice for most Viam
use cases: quality inspection, object detection on a camera feed, simple
classification.

**TensorFlow (TF)** produces larger models that require more compute resources.
Use TF when you are running on hardware with a capable CPU or GPU and need
additional model capacity.

Custom training scripts can use any framework, including PyTorch and ONNX.

## Task types

The task type determines what the model learns to do. It must match how you
labeled your dataset.

- **Single label classification** assigns exactly one label to each image. Your
  dataset should have tags with exactly one tag per image.
- **Multi label classification** assigns one or more labels to each image. Your
  dataset should have tags, and images may have multiple tags.
- **Object detection** finds objects in an image and draws bounding boxes around
  them with labels. Your dataset should have bounding box annotations.

## Automatic deployment

When training completes, the model is stored in your organization's registry.
If a machine is already configured to use that model, Viam automatically
deploys the new version. The machine pulls the latest version the next time it
checks for updates. No manual download or restart is needed.

## Dataset versioning

Each time you train a model from a dataset, Viam snapshots the dataset's
contents at that point. You can continue adding images and labels to a dataset
after training without affecting previously trained models.

{{< cards >}}
{{% card link="/train/create-a-dataset/" %}}
{{% card link="/train/annotate-images/" %}}
{{% card link="/train/automate-annotation/" %}}
{{% card link="/train/train-a-model/" %}}
{{% card link="/train/deploy-a-model/" %}}
{{% card link="/train/custom-training-scripts/" %}}
{{< /cards >}}
