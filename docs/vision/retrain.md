---
linkTitle: "Retrain when accuracy drops"
title: "Retrain when your model drifts"
weight: 75
layout: "docs"
type: "docs"
description: "Close the loop when a vision model's accuracy drops in production: capture the failing images, label them, retrain, and redeploy a new model version to one or many machines."
date: "2026-04-14"
---

Every vision model loses accuracy over time. Lighting shifts, new object variations appear, someone moves a camera, a new SKU shows up on the line. The [training-to-production gap](https://medium.com/sciforce/why-your-computer-vision-model-struggles-in-the-real-world-3a6a999cdf8f) is the single most common reason a vision system fails after launch. The fix is never a one-time deployment. It is a loop.

Viam's data, training, and fleet tools are the pieces of that loop. This guide walks through the end-to-end cycle from production machine back to production machine.

## The cycle

```text
   Production ───► Capture failing ───► Label ───► Train ───► Deploy ───► Production
   detections       images from the     new         a new      new version    (again, with
   start drifting   machine              data        model      to the fleet   the new model)
         ▲                                                                          │
         └──────────────────────────────── monitor ─────────────────────────────────┘
```

You do not have to complete every step in a single sitting, and you do not have to do it manually every time. Scheduled data capture and training jobs can automate most of the loop once you have configured it.

## 1. Detect that your model needs retraining

Signs that a model needs new training data:

- Detections are missing on objects you know are in the frame.
- False positives on classes the model was never trained on.
- The label distribution in production does not match the training set (for example, a model trained in daylight is running at night).
- Confidence scores have drifted downward even on correct detections.

A simple approach: log detection results alongside camera frames for a day, then review a sample. Any class with precision or recall below your target threshold is a candidate for retraining.

## 2. Capture failing images

The image that made your model fail is the single most valuable training example you can add. Use the [data management service](/data-ai/capture-data/capture-sync/) to save camera frames to the Viam Cloud so they become available for labeling.

Two capture strategies, depending on volume:

- **Time-based capture** saves a frame every N seconds. Good for building a broad dataset across a day or week. Adjust the interval to control storage cost.
- **Conditional capture** saves frames only when a trigger condition fires (for example, "when the vision service returns a confidence below 0.6"). This keeps only the hard cases, which is what you need for retraining.

Both strategies are configured on the data management service. The images sync to the [**DATA** tab](https://app.viam.com/data/view) where you label them in the next step.

## 3. Label the new images

Open the [**DATA** tab](https://app.viam.com/data/view) in the Viam app and filter to your captured images. For each image, draw bounding boxes and apply class labels. See [Annotate images](/train/annotate-images/) for the UI walkthrough.

If you have a lot of images, use [automatic annotation](/train/automate-annotation/) to generate initial labels from an existing model, then review and correct them. Correction is usually faster than labeling from scratch.

Add the newly labeled images to an existing dataset or [create a new one](/train/create-a-dataset/). Using the same dataset as the original training keeps a single lineage: the next training job sees both the old and new images.

## 4. Train a new model version

With the updated dataset, start a new training job. See [Train a model](/train/train-a-model/) for the full flow. Key choices:

- **Same architecture, same hyperparameters** if you are just correcting drift or adding examples. Retraining with a known-good setup is predictable and easy to compare.
- **New architecture** if the task has changed (for example, you are adding a new class that the previous model could not detect). Expect to tune more.
- **Same or new model name.** If you train under the same model name, the new version replaces the last version when deployed. If you train under a new name, both versions exist and you can promote one to production while keeping the old one as a fallback.

Viam runs training jobs on cloud infrastructure. You do not need to provision a GPU machine locally. Logs stay available for seven days after the job completes.

## 5. Deploy the new version

### Test on one machine first

Pick a non-critical machine (or a local test machine). In its ML model service panel:

1. In the **Version** dropdown, select the new model version.
2. Save the configuration.

The `viam-server` on that machine downloads the new model and restarts the ML model service. No application restart is needed.

Let the new version run for a few minutes against real camera input. Watch the vision service's Control tab overlay. Confirm:

- Detections appear on the objects you labeled.
- The confidence scores are reasonable.
- No new false positives appeared on unrelated objects.

### Roll out to the fleet

Once the new version passes single-machine validation, promote it. If the machines in your fleet share a [fragment](/fleet/fragments/), update the fragment's ML model service to reference the new version. Every machine using the fragment reconfigures in place.

For [staged rollout](/fleet/), update machines in groups. One approach: use machine tags to select a canary group, roll out to canaries, wait, then roll out to the rest.

### Pin the model version, or track "latest"

In the ML model service configuration, you can either:

- **Pin a specific version** (for example, `2026-04-10T12:00:00`). The machine will keep running this version until you explicitly change it.
- **Track "latest"**. The machine runs whichever version is newest in the [registry](https://app.viam.com/registry), updating automatically when new versions land.

Pinning is safer for production fleets. "Latest" is useful during active development when you are iterating quickly and want every training run to flow through immediately.

## 6. Monitor and repeat

Accuracy monitoring is not automatic on Viam today. There is no dashboard that reports "your model's precision has dropped 5% this week." Practical approaches:

- **Log confidence scores** from your detector to a time-series store and watch for trends.
- **Sample review**: capture a periodic snapshot of production detections and review them against ground truth.
- **Alert on low confidence**: configure a [trigger](/vision/alert-on-detections/) that fires when detections below a threshold exceed a rate, so you know to pull more training data.

When drift shows up again, the cycle repeats. The first retraining cycle is the slowest; subsequent cycles reuse the same dataset, labeling workflow, and deployment procedure.

## Next steps

- [Data capture and sync](/data-ai/capture-data/capture-sync/): set up production image capture
- [Annotate images](/train/annotate-images/): label captured data
- [Train a model](/train/train-a-model/): produce a new model version
- [Deploy a model](/data-ai/ai/deploy/): wire the new version into the ML model service
- [Act on detections](/vision/act-on-detections/) and [alert on detections](/vision/alert-on-detections/): use the new version in production logic
