---
linkTitle: "Roll out to a fleet"
title: "Roll out a new model to a fleet"
weight: 80
layout: "docs"
type: "docs"
description: "Update a vision model across many machines at once using fragments and model version pinning. Short guide with links to the full fleet and deployment docs."
date: "2026-04-14"
---

This page covers the vision-specific pieces of rolling a new model to a fleet. The mechanics of fragments, staged rollout, and machine tagging live in the [fleet section](/fleet/).

A vision model rollout has three moving parts:

1. **The model version.** The ML model service on each machine either pins a specific version or tracks "latest".
2. **The configuration source.** Shared config lives in a [fragment](/fleet/fragments/) so you update one place and every machine picks up the change.
3. **The rollout order.** Machines update as soon as the new config reaches them; you can stage rollout by updating groups in sequence instead of all at once.

## Before rolling out

Before updating any production machine:

1. Train and publish the new model version. See [Retrain when your model drifts](/vision/retrain/).
2. Deploy the new version on one test machine. Verify detections look correct through the Control tab. See [Deploy an ML model from the registry](/vision/deploy-from-registry/).
3. Confirm the fleet's shared configuration uses a fragment or is otherwise centrally managed. Machines configured one-off are updated one at a time; you cannot stage a rollout across them without per-machine changes.

## Pin the new version in a fragment

If your fleet shares a [fragment](/fleet/fragments/), update the ML model service's `model_version` attribute in the fragment:

```json
{
  "name": "my-ml-model",
  "api": "rdk:service:mlmodel",
  "model": "tflite_cpu",
  "attributes": {
    "model_path": "${packages.my-model}/model.tflite",
    "label_path": "${packages.my-model}/labels.txt",
    "model_version": "2025-04-14T16-38-25"
  }
}
```

Save the fragment. Every machine using it picks up the change on its next config sync (within seconds under normal operation).

Tracking "latest" is simpler but less safe for production. Any new version published to the [registry](https://app.viam.com/registry) auto-deploys. Pin specific versions when you want to control when rollouts happen.

## Stage the rollout

To roll out to a subset of machines first:

1. Split the fleet into groups using machine tags or location.
2. Apply the updated fragment to the first group only (for example, a "canary" location).
3. Wait the period you need to catch problems (hours to days depending on your monitoring cadence).
4. Apply the fragment to the remaining groups.

See the [fleet section](/fleet/) for the fragment-per-group and tag-based rollout patterns.

## Monitor the rollout

After each stage:

- Check the machine's detections through the Control tab or a saved dashboard.
- Watch for a spike in low-confidence detections (which suggests the new model is worse than the old one on the production distribution).
- Watch `viam-server` logs for model-load errors that indicate the new version is incompatible with preprocessing or tensor name assumptions.

If the new model looks wrong, roll back by pinning the previous version in the fragment. Machines converge to the previous version on the next config sync.

## Related

- [Retrain when your model drifts](/vision/retrain/): produce the new model version in the first place
- [Deploy an ML model from the registry](/vision/deploy-from-registry/): deploy a model to a single machine
- [Fleet deployment](/fleet/): the full fragment and staged-rollout mechanics
