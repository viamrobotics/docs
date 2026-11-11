---
title: "Wrap-up and next steps"
linkTitle: "Wrap-up"
weight: 110
type: "docs"
layout: "docs"
slug: "wrap-up"
description: "Review the dice reader you built and find where to take your models next."
capabilities: ["ml-training", "ml-models", "datasets"]
diataxis: workshop
date: "2026-11-06"
workshop: "dice-vision"
prev: "/tutorials/dice-vision/score-a-yahtzee-roll/"
toc_hide: true
---

Your webcam reads dice with a model you trained on your own images, and a module running on your machine turns what it reads into Yahtzee scores.
You also know, from measurements rather than a guess, which of two models does the job better.

## What you built {#what-you-built}

- Four datasets: a hand-labeled starter set, an auto-labeled training set, and clean and hard test datasets.
- A starter model that labeled most of your training images for you.
- Two dice detectors, one from built-in training and one from a YOLO training script, scored the same way on the same test datasets.
- A deployed vision service running the winning model on your machine.
- An inline module that reads a settled roll and scores it.

## What you learned {#what-you-learned}

- Add images from a camera to a dataset.
- Label images, and use a starter model to label more of them for you.
- Train an object detection model with built-in training.
- Train a YOLO model with a training script from the registry.
- Evaluate models on held-out test datasets and compare the results.
- Choose a confidence threshold from evaluation results.
- Deploy a model with the ML model and vision services.
- Build an inline module that scores rolls from your model's detections.

## What's next {#whats-next}

- [Automate annotation](/train/automate-annotation/): auto-label new images with your best model, add images from the conditions where it struggled, retrain, and evaluate the new version on the same test datasets.
- [Custom training scripts](/train/custom-training-scripts/): write your own training script, or fork `yolo-training` and try a larger `imgsz` to help with small pips.
- [Configure a vision service](/vision/configure/): see the other kinds of vision services, such as classifiers and segmenters.
- [Miniature Palletizing with the SO-ARM101](/tutorials/so-arm101-palletizing/): give your machine an arm, and you're one step from a robot that rolls its own dice.

To keep going with the scorer, add a command to your module that keeps a scorecard across 13 rounds, so you can play a full game against your machine.

{{< workshop-nav >}}
