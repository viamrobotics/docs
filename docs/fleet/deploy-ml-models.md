---
linkTitle: "Deploy ML models"
title: "Deploy ML models across your fleet"
weight: 32
layout: "docs"
type: "docs"
description: "Roll out trained ML models to machines using fragments and the Viam registry."
---

Deploy a trained ML model to one machine or your entire fleet using the same fragment workflow you use for modules. When you retrain and upload a new model version, machines configured to track that version update automatically.

## When to use this

Use this page when you have a trained model in the Viam registry and want to deploy it to multiple machines. If you are deploying to a single machine for the first time, start with [deploy a model to a machine](/train/deploy-a-model/).

## Prerequisites

- A trained ML model in the Viam registry. See [train a model](/train/train-a-model/).
- At least one machine with a camera configured. See [add a camera](/hardware/common-components/add-a-camera/).
- A [fragment](/fleet/reuse-configuration/) for your fleet, or create one below.

## How model deployment works

ML models are deployed as registry packages, the same way modules are. A machine needs two services to run a model:

1. **ML model service**: loads the model file and runs inference.
2. **Vision service**: connects the ML model service to a camera and returns detections or classifications.

You configure both services in a fragment, apply the fragment to your machines, and every machine downloads the model and starts running inference.

## 1. Add the model and vision service to a fragment

1. Navigate to your fragment at [app.viam.com/fragments](https://app.viam.com/fragments).
1. Click **+** and add an ML model service (for example, search for `tflite` and add **tflite_cpu**).
1. In the ML model service card, under **Deployment**, select **Deploy model on machine**.
1. Click **Select model** and choose your trained model from the registry.
1. Click **+** again and add a vision service. Search for `mlmodel` and add the **mlmodel** vision service.
1. Configure the vision service to use the ML model service you just added.
1. Click **Save**.

## 2. Choose a version strategy

Each ML model package has a version field in the fragment configuration.

- **Track latest**: leave the version at the default. When you upload a retrained model, machines update automatically on their next config sync.
- **Pin to a specific version**: set the version string to prevent automatic updates until you are ready.
- **Use fragment tags**: create `stable` and `development` tags on the fragment. Test new models on development machines before promoting to production. See [reuse configuration](/fleet/reuse-configuration/#version-and-tag-fragments-for-staged-rollouts) for the tag workflow.

To control the timing of updates, configure a maintenance window so models are not swapped while a machine is actively processing. See [manage versions](/fleet/manage-versions/).

## 3. Apply the fragment to machines

Apply the fragment to your machines through the Viam app, provisioning, or CLI. See [deploy software](/fleet/deploy-software/#3-apply-the-fragment-to-machines) for the steps.

## 4. Verify the deployment

1. Navigate to a machine's **CONTROL** tab.
1. Find the vision service card and test it with a live camera feed to confirm detections or classifications appear.
1. Check the **LOGS** tab for errors from the ML model service or vision service.

## Update a model across the fleet

When you retrain and upload a new model version:

- **Tracking latest**: machines update on their next config sync (or within the maintenance window).
- **Using fragment tags**: update the fragment configuration with the new model version, save to create a new revision, then move the `stable` tag to the new revision.
- **Pinned to a version**: update the version string in the fragment and save.

## Related pages

- [Train a model](/train/train-a-model/) for creating ML models
- [Deploy a model to a machine](/train/deploy-a-model/) for single-machine deployment
- [Configure computer vision](/vision/configure/) for vision pipeline details
- [Reuse configuration](/fleet/reuse-configuration/) for fragment management
- [Manage versions](/fleet/manage-versions/) for version pinning and maintenance windows
