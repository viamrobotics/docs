---
linkTitle: "Deploy ML models"
title: "Deploy ML models across your fleet"
weight: 32
layout: "docs"
type: "docs"
description: "Roll out trained ML models to machines using fragments and the Viam registry."
---

Deploy a trained ML model to one machine or an entire fleet using the same fragment-based workflow you use for modules. When you retrain and upload a new model version, machines configured to track that version update automatically.

## Prerequisites

- A trained ML model in the Viam registry. See [Train a model](/train/train-a-model/) to create one.
- At least one machine with a camera configured. See [Add a camera](/hardware/common-components/add-a-camera/).
- A [fragment](/fleet/reuse-configuration/) for your fleet configuration (or create one in the steps below).

## How model deployment works

ML models in Viam are deployed as registry packages, the same way modules are. A machine needs two services to run a model:

1. **ML model service** -- loads the model file and runs inference.
2. **Vision service** -- connects the ML model service to a camera and returns detections or classifications.

You configure both services in a fragment, apply the fragment to your machines, and every machine downloads the model and starts running inference.

When you upload a new version of the model, machines update automatically (unless you pin to a specific version).

## 1. Create a fragment with your ML model

1. Go to [app.viam.com/fragments](https://app.viam.com/fragments).
1. Click **Create fragment** and give it a name.
1. Click the **+** button to add resources.
1. Search for `tflite` and add the **tflite_cpu** ML model service (or the appropriate model service for your model framework).
1. In the ML model service configuration, under **Deployment**, select **Deploy model on machine**.
1. Click **Select model** and choose your trained model from the registry.
1. Add a **vision** service. Search for `mlmodel` and add the **mlmodel** vision service.
1. Configure the vision service to use the ML model service you just added.
1. Click **Save**.

## 2. Choose a version strategy

In the fragment configuration, each module and ML model package has a version field.

- **Track latest**: leave the version set to the default. When you upload a new model version, machines update automatically on their next config sync.
- **Pin to a specific version**: set the version to a specific string (for example, `2026-03-15T10-30-00`) to prevent automatic updates.
- **Use fragment tags for staged rollouts**: create a `stable` tag on your fragment, deploy `stable` to production machines, and a `development` tag for test machines. When the new model is validated on development machines, move the `stable` tag to the new fragment revision.

For more on version strategies, see [Update software](/fleet/update-software/).

{{< alert title="Tip" color="tip" >}}
Configure a [maintenance window](/fleet/update-software/) to control when model updates are applied, so machines are not interrupted during operation.
{{< /alert >}}

## 3. Apply the fragment to your machines

Apply the fragment to machines individually or through provisioning:

- **Manual**: on each machine's **CONFIGURE** tab, click **+**, select **Insert fragment**, and choose your fragment.
- **Provisioning**: include the fragment ID in your `viam-defaults.json` file so new machines apply it automatically on first boot. See [Provision devices](/fleet/provision-devices/).
- **CLI**: use `viam machines part fragments add --part=<part-id> --fragment=<fragment-id>`.

## 4. Verify the deployment

After applying the fragment, verify that the model is running on your machines:

1. Navigate to a machine's **CONTROL** tab in the Viam app.
1. Find the vision service card and test it with a live camera feed.
1. Check the machine's **LOGS** tab for any errors from the ML model or vision service.

## Update a model across the fleet

When you retrain and upload a new model version:

1. If you are tracking the latest version, machines update automatically on their next config sync (or within the maintenance window if configured).
1. If you are using fragment tags, update the fragment configuration with the new model version, then move the `stable` tag to the new revision.
1. If you pinned to a specific version, update the version string in the fragment.

To monitor which model version each machine is running, use the fleet dashboard or check machine status programmatically. See [Update software](/fleet/update-software/) for details.

## Related pages

- [Train a model](/train/train-a-model/) for creating ML models from captured data
- [Deploy a model to a machine](/train/deploy-a-model/) for single-machine model deployment
- [Configure computer vision](/vision/configure/) for setting up vision pipelines
- [Reuse configuration](/fleet/reuse-configuration/) for fragment details
- [Update software](/fleet/update-software/) for version management and maintenance windows
