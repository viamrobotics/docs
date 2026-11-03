---
linkTitle: "Overview"
title: "Train ML models"
weight: 1
layout: "docs"
type: "docs"
description: "How datasets, training methods and frameworks fit together to produce models that run on your machines, from image classifiers to robot policies."
capabilities: ["ml-training", "datasets", "ml-models"]
diataxis: explanation
date: "2026-04-17"
updated: "2026-11-02"
---

Your machines capture data in the field.
Training uses that data to produce a model that runs on the machine, whether the model labels what a camera sees, controls an arm, or does something else.
Usually you start from a model that already exists and fine-tune it on your data.

Viam supports two ways to train, and an organization can use both:

- **Built-in training** takes no code.
  You pick a dataset, the labels to learn and a framework, and Viam fine-tunes a pretrained image model on your labels.
  It's the fastest path to an image classifier or object detector.
- **Custom training scripts** run your own Python code, so you choose the model, the training method and the framework.
  Use one to fine-tune a large pretrained model such as a robot policy, train on data that isn't images, or control how training works.

Either way, Viam runs the job on its own cloud GPUs, so you don't provision hardware, and the result deploys to your machines the same way.

Every model goes through the same stages, and three choices decide which pages in this section apply to you: the model's task type, how you train it, and its framework.
This page explains each of them, so you can tell which path your model takes before you start.

## How training works {#how-training-works}

Training is a loop.
A deployed model captures more data as the machine uses it, and that data trains the next version.

<img src="/train/training-flywheel.svg" alt="The training loop: capture data on your machines, build a dataset, train with built-in training or a custom script, deploy the model to a machine, and run it on the machine, which captures more data and starts the loop again. Each round trains a new model version." style="width:100%;max-width:560px;height:auto;display:block;margin:0 auto" >

**1. Capture data.**
Machines [capture data](/data/capture-sync/overview/) from their cameras and sensors and sync it to the cloud.

**2. Build a dataset.**
A [dataset](/train/create-a-dataset/) collects data from any of your organization's machines into one named collection.
What goes in it depends on the model: images you [label](/train/annotate-data/) for a vision model, or recorded demonstrations you [tag with the task](/train/annotate-data/#tag-sequences) for a robot policy.

**3. Train.**
A training job reads the dataset in the cloud and publishes the result as a new model version in your organization's registry.
[Built-in training](/train/train-a-model/) needs no code; a [custom training script](/train/custom-training-scripts/) runs your own code.

**4. Deploy.**
[Deploying](/train/deploy-a-model/) adds the model and the resource that runs it to a machine's configuration.
The machine downloads the model from the registry.

**5. Run.**
What you do with a deployed model depends on what it is.
A vision model answers through a [vision service](/vision/), which your code or other services query for classifications and detections.
Other models are used through the module that runs them.
While the model runs, the machine keeps capturing data, including the cases where the model gets it wrong.

**Retrain.**
You add data from the cases where the model struggles to the dataset, train a new version, and machines configured to use the model pick it up.
For vision models, [auto-predictions](/train/automate-annotation/) let an existing model draft labels for new images, so each round takes less hand-labeling.

## What you can train {#what-you-can-train}

### Task type {#task-type}

The task type says what the model does.
It decides what data is required, and what Viam features are available.

| Task type                       | The model                                             | Example                                                                  | The dataset holds                                                                                    | Built-in training |
| ------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- | ----------------- |
| **Single label classification** | Assigns one label to each image                       | Is this part on the line good or defective?                              | Images with exactly one tag each                                                                     | Yes               |
| **Multi label classification**  | Assigns one or more labels to each image              | Which safety gear, such as a hard hat or a vest, is this worker wearing? | Images with one or more tags each                                                                    | Yes               |
| **Object detection**            | Finds objects in an image and draws boxes around them | Where is each package on the conveyor?                                   | Images with labeled bounding boxes                                                                   | Yes               |
| **Robot policy**                | Drives a robot to do a task                           | Pick up the cup and put it in the bin.                                   | Recorded demonstrations of the task, usually camera images and joint positions, tagged with the task | No                |
| **Other**                       | Anything the other types don't describe               | Predict a motor failure from its vibration readings.                     | Whatever your training script requires                                                               | No                |

### Training method {#training-method}

Beyond whether you write code, the two ways to train differ in what they can do.

**Built-in training** starts from an image model pretrained on a large set of general images, keeps its layers fixed, and trains new layers on top of it to predict your labels.
It produces TFLite or TensorFlow models.
It only reads images: it can't train on a sequence dataset, and it rejects the **Robot policy** and **Other** task types.

A **custom training script** can train any task type, in any framework, on either kind of dataset, and can fine-tune any pretrained model your code loads.
The script runs in a container: a Viam-managed one, which comes with TensorFlow, or a [custom training container](/train/custom-containers/) your organization registers with whatever dependencies the model needs.
A custom job's task type and framework come from the training script, which declares them when it's uploaded to the registry, so every model a script trains has the same ones.
Custom jobs run on more powerful GPUs and are billed at a higher rate than built-in training.
You can write your own script or find one in the [registry](https://app.viam.com/registry?type=Training+Script).

### Framework and what runs the model {#framework}

A framework is the machine learning library a model is built with, and it sets the format of the model's files.
TFLite, TensorFlow, PyTorch and ONNX aren't specific to Viam: they're widely used formats, so a model trained in one of them anywhere, not only on Viam, can run on a Viam machine.

- **TensorFlow** and **PyTorch** are the two most common libraries for building and training models.
- **TFLite** is a compact form of a TensorFlow model, a `.tflite` file, made to run on small devices without a GPU.
- **ONNX** is an open format that many libraries can export to, so it's often how a model moves between them.
- **Registry** is Viam's own, and it isn't a file format. It means a specific module, rather than a standard service, reads the model's files and runs the model.

To run a model, a machine needs software that can read its format.
The framework decides which software that is, and that's what **Deploy** adds to the machine's configuration:

| Framework      | Runs on the machine in                                                                                                                                                 | Hardware                                             |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **TFLite**     | The [`tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu) ML model service                                                                                       | linux/amd64, linux/arm64, darwin/arm64, darwin/amd64 |
| **TensorFlow** | The [`tensorflow-cpu`](https://app.viam.com/module/viam/tensorflow-cpu) or [`triton`](https://app.viam.com/module/viam/mlmodelservice-triton-jetpack) ML model service | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64   |
| **PyTorch**    | The [`torch-cpu`](https://app.viam.com/module/viam/torch-cpu) or `triton` ML model service                                                                             | Nvidia GPU, linux/arm64, darwin/arm64                |
| **ONNX**       | The [`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu) or `triton` ML model service                                                                               | Nvidia GPU, linux/amd64, linux/arm64, darwin/arm64   |
| **Registry**   | The module the model names                                                                                                                                             | Whatever the module supports                         |

The first four load the model into an ML model service, which runs it but doesn't interpret its output.
For a classification or detection model, a vision service sits on top of the ML model service and turns that output into labels and boxes.

A **Registry** model doesn't use an ML model service unless its module provides one.
Instead, the model names the module resource that runs it, such as a module that drives an arm with a robot policy, and **Deploy** adds that resource with the model.
Like the framework, the module comes from the training script.
This is how a model whose runtime isn't a standard ML model service gets onto a machine without manual configuration.

## What's next {#whats-next}

- [Create a dataset](/train/create-a-dataset/): collect the images or demonstrations your model trains on.
- [Built-in training](/train/train-a-model/): train an image classifier or object detector without writing code.
- [Custom training](/train/custom-training-scripts/): train a robot policy or any other model with your own code.
- [Deploy a model to a machine](/train/deploy-a-model/): add a trained model and what runs it to your machine.
