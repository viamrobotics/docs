---
linkTitle: "Deploy software"
title: "Deploy software to machines"
weight: 30
layout: "docs"
type: "docs"
description: "Deploy modules and control logic to your fleet using fragments and the Viam registry."
---

Deploy modules (hardware drivers, control logic, or other custom code) to one machine or an entire fleet. You configure the module in a fragment, apply the fragment to your machines, and the machines download the module from the Viam registry automatically.

## Prerequisites

- A module uploaded to the Viam registry. See [deploy a module](/build-modules/deploy-a-module/) for how to upload.
- A [fragment](/fleet/reuse-configuration/) for your fleet configuration, or create one in the steps below.

## 1. Add the module to a fragment

1. Navigate to your fragment's page at [app.viam.com/fragments](https://app.viam.com/fragments).
1. Click **+** and select **Component or service** or **Control code**, depending on what the module provides.
1. Search for your module in the registry and add it.
1. Configure the module's attributes as needed.
1. Click **Save**.

## 2. Set the version strategy

Each module in the fragment has a version field. On the fragment card for the module, find the **Update version** section:

- **Latest version**: the machine downloads the newest version when it syncs. This is the default.
- **Pin to version**: the machine stays on a specific version and does not update automatically.
- **Pin to tag**: the machine uses whichever version the fragment tag points to.

{{% alert title="Caution" color="caution" %}}
For any version type other than pinning to a specific version, the module updates as soon as a matching version is available, which restarts the module. If the module cannot be safely interrupted, pin to a specific version and update manually.
{{% /alert %}}

To control when updates are applied, configure a maintenance window. See [manage versions](/fleet/manage-versions/) for details.

## 3. Apply the fragment to machines

**Through the Viam app:**

1. Navigate to each machine's **CONFIGURE** tab.
1. Click **+** and select **Insert fragment**.
1. Search for your fragment and select it.
1. Click **Insert fragment**, then **Save**.

**Through provisioning:**

Include the fragment ID in your `viam-defaults.json` file. New machines apply the fragment automatically on first boot. See [provision devices](/fleet/provision-devices/).

**Through the CLI:**

```sh {class="command-line" data-prompt="$"}
viam machines part fragments add --part=<part-id> --fragment=<fragment-id>
```

## 4. Verify the deployment

1. Navigate to a machine's **CONFIGURE** tab and confirm the module appears in the resource list.
1. Go to the **CONTROL** tab and test the deployed components or services.
1. Check the **LOGS** tab for any errors from the module.

On the fleet dashboard at [app.viam.com/fleet/machines](https://app.viam.com/fleet/machines), confirm your machines are online and showing the expected viam-server version.

## Related pages

- [Reuse configuration](/fleet/reuse-configuration/) for creating and managing fragments
- [Deploy ML models](/fleet/deploy-ml-models/) for deploying trained ML models
- [Manage versions](/fleet/manage-versions/) for version pinning and maintenance windows
- [Build and deploy modules](/build-modules/) for writing and uploading modules
