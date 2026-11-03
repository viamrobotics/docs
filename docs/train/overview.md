---
linkTitle: "Overview"
title: "Train ML models"
weight: 1
layout: "docs"
type: "docs"
description: "What kinds of models you can train with Viam, how training works, and when to use built-in training or a custom training script."
capabilities: ["ml-training", "datasets", "ml-models"]
diataxis: explanation
date: "2026-04-17"
updated: "2026-11-02"
---

Your machines capture data in the field.
Training uses that data to produce a model that runs on the machine, whether the model labels what a camera sees, controls an arm, or does something else.
Usually you start from a model that already exists and fine-tune it on your data.

Viam supports two ways to train: built-in training, which takes no code, and custom training scripts, which run your own Python code.
Either way, Viam runs the job on its own cloud GPUs, so you don't provision hardware, and the result deploys to your machines the same way.

This page covers the types of models you can train, the stages every model goes through, and how to choose between built-in and custom training.

## Types of models {#types-of-models}

<span id="what-you-can-train"></span><span id="task-type"></span>Every model has a task type, which says what the model does and decides what data it trains on.

| Task type                       | The model                                             | Example                                                                  | Training           |
| ------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------ | ------------------ |
| **Single label classification** | Assigns one label to each image                       | Is this part on the line good or defective?                              | Built-in or custom |
| **Multi label classification**  | Assigns one or more labels to each image              | Which safety gear, such as a hard hat or a vest, is this worker wearing? | Built-in or custom |
| **Object detection**            | Finds objects in an image and draws boxes around them | Where is each package on the conveyor?                                   | Built-in or custom |
| **Robot policy**                | Drives a robot to do a task                           | Pick up the cup and put it in the bin.                                   | Custom only        |
| **Other**                       | Anything the other types don't describe               | Predict a motor failure from its vibration readings.                     | Custom only        |

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

## Built-in or custom training {#training-method}

Use built-in training when all of these are true:

- You're training an image classifier or object detector.
- Your dataset is labeled images, not a [sequence dataset](/train/create-a-dataset/).
- Your machine can run a TFLite or TensorFlow model. TFLite runs on Linux and macOS on both ARM and x86; to check your hardware, see [What runs the model](/train/deploy-a-model/#what-runs-the-model).
- You don't need to choose the model architecture or control preprocessing, augmentation or hyperparameters.

For anything else, such as a robot policy, a model trained on sensor readings, or a PyTorch or ONNX model, use a custom training script.

A custom training script doesn't mean writing code from scratch.
You can [find a training script](/train/custom-training-scripts/#find-an-existing-training-script) in the registry that already trains the model you need, and run it on your dataset.

### How they differ {#how-they-differ}

|                  | Built-in training                                                                                          | Custom training script                                                                                                                                                                |
| ---------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task types       | Single label classification, multi label classification, object detection                                  | Any, including robot policy and **Other**                                                                                                                                             |
| Training data    | The images in a binary dataset; other files are skipped                                                    | A binary or sequence dataset, read however your script needs                                                                                                                          |
| Code             | None: you pick a dataset, the labels to learn and a framework                                              | A Python script you write or find in the registry, run in a Viam-managed container with TensorFlow or a [custom training container](/train/custom-containers/) with your dependencies |
| Model            | A pretrained image model with its layers kept fixed, plus new layers trained on top to predict your labels | Any model your code builds or loads, including large pretrained models such as robot policies                                                                                         |
| Control          | The labels and the framework                                                                               | Everything: architecture, preprocessing, augmentation, hyperparameters                                                                                                                |
| Framework        | TFLite or TensorFlow                                                                                       | Any, declared by the script: TFLite, TensorFlow, PyTorch, ONNX, or **Registry** for a model a module runs                                                                             |
| Compute and cost | Viam cloud GPUs                                                                                            | More powerful Viam cloud GPUs, billed at a higher rate                                                                                                                                |
| Dataset minimums | [80% labeled, at least 10 examples per label](/train/train-a-model/#prerequisites)                         | Whatever your script requires                                                                                                                                                         |

<span id="framework"></span>The framework is the format of the model's files, and it decides what runs the model on your machine: an ML model service for TFLite, TensorFlow, PyTorch and ONNX, or the module the model names for **Registry**.
Check that a service for your framework supports your machine's hardware before you train; see [What runs the model](/train/deploy-a-model/#what-runs-the-model).

A custom job's task type and framework come from the training script, which declares them when it's uploaded to the registry, so every model a script trains has the same ones.

## What's next {#whats-next}

- [Create a dataset](/train/create-a-dataset/): collect the images or demonstrations your model trains on.
- [Built-in training](/train/train-a-model/): train an image classifier or object detector without writing code.
- [Custom training](/train/custom-training-scripts/): train a robot policy or any other model with your own code.
- [Deploy a model to a machine](/train/deploy-a-model/): add a trained model and what runs it to your machine.
