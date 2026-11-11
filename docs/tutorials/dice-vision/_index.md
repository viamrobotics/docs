---
title: "Train a dice reader and score Yahtzee"
linkTitle: "Dice vision workshop"
weight: 70
type: "docs"
layout: "docs"
description: "Train two object detection models to read dice from a webcam, evaluate them on held-out data, and score Yahtzee rolls with the winner."
capabilities:
  [
    "datasets",
    "ml-training",
    "ml-models",
    "vision-service",
    "hw-camera",
    "inline-modules",
  ]
diataxis: overview
date: "2026-11-06"
authors: ["Eliza Farley"]
level: "Intermediate"
languages: ["python"]
viamresources: ["camera", "mlmodel", "vision"]
platformarea: ["ml", "data"]
cost: "80"
images: ["/tutorials/dice-vision/hero-yahtzee-roll.jpg"]
imageAlt: "A webcam on a purple post at the back of a white desk, facing eight translucent colored dice rolled out in front of it."
tags: ["workshop", "ml", "vision", "training"]
workshop: "dice-vision"
workshop_overview: true
time_estimate: "185 minutes"
hardware:
  - "A USB webcam, such as a Logitech C920"
  - "Five or more dice"
  - "Mac or Linux computer"
no_list: true
---

In this workshop you teach a webcam to read dice, then use what it sees to score Yahtzee.
You capture and label your own images, train two detection models two different ways, measure which one reads dice better, and build a Yahtzee scorer on the winner that runs on your machine.

{{< imgproc src="/tutorials/dice-vision/hero-yahtzee-roll.jpg" resize="1200x" declaredimensions=true alt="A webcam on a purple post at the back of a white desk, facing eight translucent colored dice rolled out in front of it." >}}

Dice are a good first vision project.
They're cheap and the same everywhere, a pretrained model can't read them, and there's never any doubt about what a die shows.

You'll learn how to:

- Add images from a camera to a dataset
- Label images, and use a starter model to label more of them for you
- Train an object detection model with built-in training
- Train a YOLO model with a training script from the registry
- Evaluate models on held-out test datasets and compare the results
- Choose a confidence threshold from evaluation results
- Deploy a model with the ML model and vision services
- Build an inline module that scores rolls from your model's detections

## Requirements {#requirements}

### Hardware {#hardware}

- A USB webcam connected to your computer, such as a [Logitech C920](https://www.logitech.com/en-us/products/webcams/c920-pro-hd-webcam.960-000764.html).
  Any webcam that `viam-server` can stream from works.
- Five or more dice whose pips stand out clearly from the die, such as white pips on colored dice.
  Any color works; the model learns the colors you train it on.
- A way to hold the webcam about 30 cm above your workspace, and later about 45 cm.
  A stand, a clamp, a 3D-printed post or tape all work.
- A plain background to roll on, such as a dice tray or a sheet of plain paper.
- A Mac or Linux computer that runs `viam-server`.

### Software {#software}

- A Viam account and a machine running `viam-server` on your computer. See [Set up your first machine](/set-up-a-machine/first-machine/).

### What you should know first {#what-you-should-know-first}

- How components, services and machines fit together: [Viam platform overview](/overview/).
- What training, datasets and models are in Viam: [Train ML models](/train/overview/).

### Check your setup {#check-your-setup}

Everything in this workshop happens in the Viam app, including the code in [Phase 10](/tutorials/dice-vision/score-a-yahtzee-roll/), so you don't need to install anything on your computer besides `viam-server`.

Open your machine's page in the [Viam app](https://app.viam.com) and check that it shows **Live**.
If it shows **Offline**, check that `viam-server` is running on your computer.

## Phases {#phases}

The phase times are hands-on time.
Each training job also runs for some time in the cloud, and the phases tell you what to do while you wait.

| Phase                                                                                      | What you end with                                                                                                                                 | Time             |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| 1. [Capture a starter set from your webcam](/tutorials/dice-vision/capture-a-starter-set/) | The webcam streams in the `camera` card's **Test** section and 30 images of dice are in a dataset.                                                | About 20 minutes |
| 2. [Label the starter set](/tutorials/dice-vision/label-the-starter-set/)                  | Every die in the starter set has a box and a value.                                                                                               | About 20 minutes |
| 3. [Train a starter and capture more](/tutorials/dice-vision/train-a-starter-model/)       | A starter model trains while you capture about 70 more images.                                                                                    | About 20 minutes |
| 4. [Auto-label the training set](/tutorials/dice-vision/auto-label-the-training-set/)      | The starter model labels your training set, you correct it, and you add your starter images. **Milestone:** a model you trained labels your data. | About 20 minutes |
| 5. [Train a built-in model](/tutorials/dice-vision/train-a-built-in-model/)                | A TFLite detection model trains on the full training set.                                                                                         | About 10 minutes |
| 6. [Train a YOLO model from the registry](/tutorials/dice-vision/train-a-yolo-model/)      | A YOLO model trains on the same dataset.                                                                                                          | About 15 minutes |
| 7. [Build the test datasets](/tutorials/dice-vision/build-the-test-datasets/)              | A clean and a hard test dataset, labeled and checked.                                                                                             | About 25 minutes |
| 8. [Evaluate both models and pick a winner](/tutorials/dice-vision/evaluate-both-models/)  | Four evaluations and a chosen model and threshold. **Milestone:** a measured answer to which model reads dice better.                             | About 20 minutes |
| 9. [Deploy the winning model](/tutorials/dice-vision/deploy-the-winning-model/)            | The winning model draws boxes on the live camera feed.                                                                                            | About 15 minutes |
| 10. [Score a Yahtzee roll](/tutorials/dice-vision/score-a-yahtzee-roll/)                   | An inline module reads a roll and returns its score. **Milestone:** an application built on your own model.                                       | About 20 minutes |

When you finish, the [wrap-up](/tutorials/dice-vision/wrap-up/) suggests where to go next.
