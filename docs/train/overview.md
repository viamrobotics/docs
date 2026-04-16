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

## Scale labeling with auto-predictions

Once you have a working model, you do not have to label every new image by
hand. Use [auto-predictions](/train/automate-annotation/) to have an existing
model draft tags or bounding boxes for a dataset, then review the suggestions.

A typical active-learning loop:

1. Hand-label a starter dataset (20-50 images per class).
2. Train an initial model.
3. Capture more images from your machines.
4. Run auto-predictions against the new images using your initial model.
5. Accept or reject each prediction to produce verified labels.
6. Retrain with the expanded dataset.

This turns a small labeling effort into a growing, self-improving dataset.

## Supported frameworks and hardware

Viam's managed training handles TFLite and TensorFlow directly. For PyTorch,
ONNX, or other frameworks, write a [custom training script](/train/custom-training-scripts/).

| Framework                                          | How to train                      | ML model service                                                                                                                                | Hardware                                             |
| -------------------------------------------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| [TensorFlow Lite](https://www.tensorflow.org/lite) | Managed training                  | [`tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu)                                                                                     | linux/amd64, linux/arm64, darwin/arm64, darwin/amd64 |
| [TensorFlow](https://www.tensorflow.org/)          | Managed training or custom script | [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64   |
| [PyTorch](https://pytorch.org/)                    | Custom script                     | [`torch-cpu`](https://app.viam.com/module/viam/torch-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack)           | Nvidia GPU, linux/arm64, darwin/arm64                |
| [ONNX](https://onnx.ai/)                           | Custom script                     | [`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu), [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack)             | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64   |

**TFLite** produces compact models optimized for edge devices without a GPU,
and is the right choice for most Viam use cases. **TensorFlow** produces
larger models that require more compute. Use **PyTorch** or **ONNX** when you
are importing an existing model or need framework-specific features not
available in TensorFlow.

Custom training scripts currently run in TensorFlow-based containers. You can
install additional Python dependencies through `setup.py`. See
[custom training scripts](/train/custom-training-scripts/) for details.

## Task types

The task type determines what the model learns to do. It must match how you
labeled your dataset.

{{<imgproc src="/train/task-types.png" resize="x400" declaredimensions=true alt="Three task type cards from the Viam training wizard: single label classification, multi label classification, and object detection." class="shadow imgzoom" >}}

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
