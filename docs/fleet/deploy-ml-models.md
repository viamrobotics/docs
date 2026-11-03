---
linkTitle: "Deploy ML models"
title: "Deploy ML models across your fleet"
weight: 32
layout: "docs"
type: "docs"
description: "Roll out trained ML models to machines using fragments and the Viam registry."
capabilities: ["fleet-deployment"]
diataxis: how-to
aliases:
  - /vision/deploy-and-maintain/roll-out-to-fleet/
  - /vision/roll-out-to-fleet/
---

Deploy a trained ML model to one machine or your entire fleet using the same fragment workflow you use for modules. When you retrain and upload a new model version, machines that track the model's latest version update automatically, and machines pinned to a version update when you change the pin.

## When to use this

Use this page when you have a trained model in the Viam registry and want to deploy it to multiple machines. If you are deploying to a single machine for the first time, start with [deploy a model to a machine](/train/deploy-a-model/).

## Prerequisites

- A trained ML model in the Viam registry. See [train a model](/train/train-a-model/).
- For a classification or detection model, machines with a camera configured. See [add a camera](/hardware/common-components/add-a-camera/).
- A [fragment](/fleet/reuse-configuration/) for your fleet. If you don't have one yet, [create one](/fleet/reuse-configuration/#create-a-fragment) first.

## How model deployment works

ML models are deployed as registry packages, the same way modules are. A classification or detection model needs two services on the machine:

1. **ML model service**: loads the model file and runs inference.
2. **Vision service**: connects the ML model service to a camera and returns detections or classifications.

Other models need only the resource that runs them: an ML model service, or for a **Registry** model, the module resource the model names. See [Framework and what runs the model](/train/overview/#framework).

You configure these resources in a fragment, apply the fragment to your machines, and every machine downloads the model and starts running it.

## 1. Add the model to a fragment

1. Navigate to your fragment at [app.viam.com/fragments](https://app.viam.com/fragments).
1. Click **+** and add an ML model service (for example, search for `tflite` and add **tflite_cpu**).
1. In the ML model service card, under **Deployment**, select **Deploy model on machine**.
1. Click **Select model** and choose your trained model from the registry.
1. For a classification or detection model, click **+** again and add a vision service. Search for `mlmodel` and add the **mlmodel** vision service, then configure it to use the ML model service you just added.
1. Click **Save**.

For a **Registry** model, add the module resource the model names and the model package instead, as in [Deploy a Registry model manually](/train/deploy-a-model/#deploy-a-registry-model-manually).

In the fragment's JSON, the model is an entry in `packages`, and the resource that runs it points into that package:

```json
{
  "packages": [
    {
      "name": "my-model",
      "package": "<org-id>/my-model",
      "version": "2026-04-14T16-38-25",
      "type": "ml_model"
    }
  ],
  "services": [
    {
      "name": "my-ml-model",
      "api": "rdk:service:mlmodel",
      "model": "tflite_cpu",
      "attributes": {
        "package_reference": "<org-id>/my-model",
        "model_path": "${packages.ml_model.my-model}/my-model.tflite",
        "label_path": "${packages.ml_model.my-model}/labels.txt"
      }
    }
  ]
}
```

The service attributes stay the same across model versions. The version is set only on the package.

## 2. Choose a version strategy

Each ML model package has a version field in the fragment configuration. For what each choice does on a single machine, see [Choose a model version](/train/deploy-a-model/#choose-a-model-version).

- **Track latest**: leave the version at the default, **Latest**. When you upload a retrained model, machines update automatically on their next config sync. Simpler, but any new version reaches every machine at once.
- **Pin to a specific version**: set the version string to prevent automatic updates until you are ready. Safer for production.
- **Use fragment tags**: create `stable` and `development` tags on the fragment. Test new models on development machines before promoting to production. See [reuse configuration](/fleet/reuse-configuration/#version-and-tag-fragments-for-staged-rollouts) for the tag workflow.

To control the timing of updates, configure a maintenance window so models are not swapped while a machine is actively processing. See [manage versions](/fleet/manage-versions/).

## 3. Apply the fragment to machines

Apply the fragment to your machines through the Viam app, provisioning, or CLI. See [deploy software](/fleet/deploy-software/#3-apply-the-fragment-to-machines) for the steps.

## 4. Verify the deployment

1. Navigate to a machine's **CONTROL** tab.
1. For a classification or detection model, find the vision service card and test it with a live camera feed to confirm detections or classifications appear.
1. Check the **LOGS** tab for errors from the resource that runs the model. A model-load error after an update usually means the new version doesn't match what that resource expects, such as different tensor names or preprocessing.

## Update or roll back a model across the fleet

Before you update the fleet, test the new version on one machine. See [Update or roll back a deployed model](/train/deploy-a-model/#update-a-deployed-model).

When you retrain and upload a new model version:

- **Tracking latest**: machines update on their next config sync (or within the maintenance window).
- **Using fragment tags**: update the fragment configuration with the new model version, save to create a new revision, then move the `stable` tag to the new revision.
- **Pinned to a version**: update the version string in the fragment and save.

After each stage of a rollout, check the updated machines before you move on. For a vision model, a rise in low-confidence detections suggests the new version does worse than the old one on real camera input.

Rolling back follows the same pattern in reverse: change the version pin or move the tag back to a previous revision. Viam does not automatically roll back if a new model performs worse, so you change the pin or tag manually.

## Related pages

- [Train a model](/train/train-a-model/) for creating ML models
- [Deploy a model to a machine](/train/deploy-a-model/) for single-machine deployment
- [Configure computer vision](/vision/configure/) for vision pipeline details
- [Reuse configuration](/fleet/reuse-configuration/) for fragment management
- [Manage versions](/fleet/manage-versions/) for version pinning and maintenance windows
