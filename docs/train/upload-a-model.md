---
linkTitle: "Upload a model"
title: "Upload a model"
weight: 29
layout: "docs"
type: "docs"
description: "Add a model you trained outside Viam, or found elsewhere, to your organization so you can deploy it to your machines."
capabilities: ["ml-models"]
diataxis: how-to
aliases:
  - /vision/deploy-and-maintain/deploy-custom-model/
  - /vision/deploy-custom-model/
  - /services/ml/upload-model/
  - /manage/data/upload-model/
  - /manage/ml/upload-model/
  - /ml/upload-model/
---

Upload a model when you have model files that aren't in the Viam [registry](https://app.viam.com/registry):

- You trained the model outside Viam, for example locally, in another cloud, or in a notebook.
- You found the model elsewhere, such as on GitHub or Hugging Face, and want to run it on a Viam machine.

A model you train on Viam, with [built-in training](/train/train-a-model/) or a [custom training script](/train/custom-training-scripts/), is added to your organization by the training job, so you don't upload it.

## Prerequisites

- The model's files, in a format Viam supports. See [step 1](#check-the-format).

## 1. Check the model's format {#check-the-format}

The ML model services run four model formats.
Your model must be in one of them:

- **TensorFlow Lite** (`.tflite`): runs in [`tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu).
  It has the broadest hardware support, and quantized models run on almost any CPU.
- **ONNX** (`.onnx`): runs in [`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu) or, for a GPU on a Jetson, [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack).
- **TensorFlow SavedModel**: runs in [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu).
- **PyTorch** (`.pt`): runs in [`torch-cpu`](https://app.viam.com/module/viam/torch-cpu).

For the hardware each service supports, see [What runs the model](/train/deploy-a-model/#what-runs-the-model).

If your training workflow produces a different format, such as Keras HDF5, convert the model to one of these formats first.
TensorFlow Lite and ONNX are the most common targets because their runtimes are the lightest.

<span id="deploy-a-registry-framework-model"></span>Use the **Registry** framework instead only if a module's instructions tell you to upload your model with it.
That module loads the model itself, so it decides the format.

If a vision service will use the model, also check that the model's tensors match what the vision service expects.
See [Check the model's tensors](/vision/configure/#tensor-requirements).

## 2. Upload the model {#upload-the-model}

<span id="3-add-the-model-to-your-organization"></span>Models belong to an organization.
You upload each version of a model once.

1. In the Viam app, go to the [**MODELS** tab](https://app.viam.com/models).
1. Click **Upload**.
1. Choose **New model**, or **New version** to add a version to a model you've already uploaded.
   Under **Visibility**, choose **Private** for internal use or **Public** to publish the model to the [registry](https://app.viam.com/registry).
   Click **Next steps**.
1. Fill in the upload form:
   - **Model framework**: select the framework that matches your model file: TFLite, TensorFlow, PyTorch, or ONNX.
     Select **Registry** only if a module's instructions tell you to.
   - **Module resources to deploy** (**Registry** framework only): with **Search the registry** selected, click **Select Modular Resource** to pick one or more component or service models from the registry.
     To enter a model by name instead, select **Type the model name**, type the model triple in the format `namespace:module-name:model-name`, and click **Add**.
     Deploying the model adds each of these resources to the machine.
   - Under **Upload files**, click **Choose model file** and pick your `.tflite`, `.onnx`, `.pt`, or framework-specific file.
     Click **Choose label file** and pick a `.txt` file with one label on each line.
     The label file is optional but recommended; a label's line number, starting from zero, is its class ID.
     For the **Registry** framework, click **Upload files** and pick the files the module loads at runtime, such as model weights and configuration files.
     Which files those are depends on the module, so check the module's documentation in the registry.
     Viam stores them together as one package, and the module reads them from the directory that `model_path` points to.
   - **Model name**: a short identifier made of letters, numbers, and hyphens.
     You refer to the model by this name when you deploy it.
     For the **Registry** framework, it's also the package name in `model_path`.
     Registry item names are unique within an organization, so the upload fails if another registry item in your organization, such as a module or training script, already uses the name.
   - **Task type**: select what the model predicts:
     - **Single label classification**: one label for each image.
     - **Multi label classification**: any number of labels for each image.
     - **Object detection**: labels for objects in an image, and where each object is.
     - **Robot policy**: actions for a robot to take, computed from inputs such as camera images and joint states.
       For example, a model that controls an arm.
     - **Other**: none of these.
   - **Description**: one sentence that describes the model.
1. Click **Upload model**.

## 3. Verify the upload

The model is listed on the [**MODELS** tab](https://app.viam.com/models), and its details page lists the version you uploaded.
You can change a model between **Private** and **Public** later in the model's settings.

## What's next

- [Deploy a model to a machine](/train/deploy-a-model/): add the model and the resource that runs it to a machine.
- [Evaluate a model](/train/evaluate-a-model/): for a classification or object detection model, measure its precision and recall on a labeled test dataset.
- [Configure a vision pipeline](/vision/configure/): use the model with a vision service, and check that its tensors match.
