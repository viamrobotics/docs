---
title: "Phase 9: Deploy the winning model"
linkTitle: "9. Deploy the winning model"
weight: 90
type: "docs"
layout: "docs"
slug: "deploy-the-winning-model"
description: "Deploy the winning model to your machine with an ML model service and a vision service, and check its detections on the live camera feed."
capabilities: ["ml-models", "vision-service"]
diataxis: workshop
date: "2026-11-06"
draft: true
workshop: "dice-vision"
phase: 9
phase_total: 10
time_estimate: "15 minutes"
prev: "/tutorials/dice-vision/evaluate-both-models/"
next: "/tutorials/dice-vision/score-a-yahtzee-roll/"
toc_hide: true
---

At the end of this phase, the winning model runs on your machine and draws a labeled box on each die in the live camera feed.

## What deploying does {#what-deploying-does}

Until now, your models have lived in the Viam cloud.
Training and evaluation both ran there, on images already saved in your datasets.
Deploying puts the model on your machine, so it runs on live camera images as they come in, without sending them to the cloud.

In practice, deploying adds two services to your machine's configuration.
When you save, `viam-server` downloads the model file and the module that runs it, and starts both services:

- The **ML model service**, `dice-model`, loads the model file and runs it.
  It's the [`tflite_cpu`](https://app.viam.com/module/viam/tflite_cpu) service from the registry for `dice-tflite`, or [`onnx-cpu`](https://app.viam.com/module/viam/onnx-cpu) for `dice-yolo`.
  It takes numbers in, the pixels of an image, and gives numbers back: box coordinates, label numbers and scores.
  It doesn't know anything about cameras or dice.
- The **vision service**, `dice-detector`, is the part that understands images.
  It's the built-in [`mlmodel`](/reference/services/vision/mlmodel/) vision service, which ships with `viam-server`.
  It gets a frame from `camera`, prepares it for the model, sends it to `dice-model`, and turns the numbers that come back into detections: a box, a label and a confidence for each die.
  It also drops boxes below the confidence threshold you set.

The vision service is what your code talks to.
In [Phase 10](/tutorials/dice-vision/score-a-yahtzee-roll/), your Yahtzee module asks `dice-detector` for the detections in the latest camera frame and gets back a list of dice, without handling the model at all.
Because the two services are separate, you could later swap in a retrained model, or the other one, without changing your code.
For more, see [How a vision service works](/vision/how-it-works/).

## Deploy the model {#deploy-the-model}

1. In the Viam app, go to **Models** and click the winning model, `dice-tflite` or `dice-yolo`.
1. Click **Deploy**.
1. Select the latest version, your location, your machine and its part, then click **Continue**.
1. Name the ML model service `dice-model`, then click **Continue**.
1. Name the vision service `dice-detector`, and check that it uses `camera`.
1. Click **Deploy**.

The deploy dialog picks the ML model service that matches the model's framework and installs its module on your machine.

{{< checkpoint >}}
On the **CONFIGURE** tab, the machine shows two new services, `dice-model` and `dice-detector`, and neither shows an error.
If the services don't appear, check that you clicked **Deploy** at the end of the dialog.
If `dice-model` shows an error, wait a minute for its module to finish installing, then check the machine's **LOGS** tab.
{{< /checkpoint >}}

## Set the confidence threshold {#set-the-confidence-threshold}

1. On the **CONFIGURE** tab, open the `dice-detector` card.
1. Set **Minimum confidence threshold** to the threshold you picked in [Phase 8](/tutorials/dice-vision/evaluate-both-models/#pick-a-confidence-threshold).
1. Click **Save**.

The vision service drops any box below this threshold.
A YOLO model from the registry script always returns its 100 best guesses, most of them near zero confidence, so without a threshold the feed fills with stray boxes.

{{< checkpoint >}}
The `dice-detector` card shows your threshold, for example `0.5`.
If the setting doesn't save, check the **LOGS** tab for a configuration error.
{{< /checkpoint >}}

## Check live detections {#check-live-detections}

1. Roll five dice onto the background.
1. In the `dice-detector` card, click **Test** and select `camera`.

{{< checkpoint >}}
The camera feed shows a box around each die, labeled with its value and a confidence score, and the values match the dice.
If not, see [Troubleshooting](#troubleshooting).
{{< /checkpoint >}}

## Troubleshooting {#troubleshooting}

{{% expand "You see no boxes at all" %}}
Check that `dice-model` and `dice-detector` show no errors on the **CONFIGURE** tab.
If either shows an error, check the machine's **LOGS** tab for the cause.
If neither does, check that the threshold in the `dice-detector` card is the one you picked in [Phase 8](/tutorials/dice-vision/evaluate-both-models/#pick-a-confidence-threshold), not a higher one.
{{% /expand %}}

{{% expand "Some dice have no box" %}}
The model isn't confident enough about those dice to pass the threshold.
Lower the threshold in the `dice-detector` card a little, and click **Save**.
{{% /expand %}}

{{% expand "Dice get the wrong value" %}}
The model reads dice best in the conditions it trained on.
Check that the scene matches your `dice-train` images:

- The camera is at the same height and angle.
- The light is the same.
- The dice roll on the same background.
- You're using the same dice.

If the scene matches and the model still misreads dice, it needs more training.
See [Refine your model](/tutorials/dice-vision/evaluate-both-models/#refine-your-model).
{{% /expand %}}

In the next phase, you write an inline module that reads a roll from `dice-detector` and scores it.

{{< workshop-nav >}}
