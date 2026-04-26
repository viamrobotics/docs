---
linkTitle: "Reuse configuration"
title: "Reuse configuration with fragments"
weight: 10
layout: "docs"
type: "docs"
description: "Create reusable configuration templates and apply them across multiple machines."
aliases:
  - /fleet/fragments/
  - /manage/fleet/reuse-configuration/
---

As a fleet grows, machines tend to drift into unique, undocumented configurations (often called "snowflake robots") because each one was set up by hand. Fragments solve this: a fragment is a reusable configuration template that you apply to many machines, and when you update the fragment, every machine that uses it receives the change.

## Prerequisites

- A Viam account with an organization. See [get started](/set-up-a-machine/) if you have not set up your first machine yet.
- At least one machine connected to Viam.

## When to use fragments

Use fragments when you have multiple machines that share the same configuration, either entirely or with small per-machine differences. Common examples:

- A fleet of identical robots that all need the same camera, motor, and control logic
- Machines in different locations that share most configuration but have different WiFi credentials or sensor thresholds
- A standard module deployment that you want to roll out to all machines in an organization

If every machine has a unique configuration with nothing in common, direct per-machine configuration may be simpler.

## Create a fragment

1. Navigate to [app.viam.com/fragments](https://app.viam.com/fragments) and click **Create fragment**.
1. Enter a name for the fragment.
1. Set the visibility:
   - **Private**: only your organization can see and use this fragment.
   - **Public**: any Viam user can see and use this fragment. Requires a public namespace for your organization.
   - **Unlisted**: anyone with a direct link can see and use it, but it does not appear in search results.
1. Click **Save**.

The fragment editor works just like the machine configuration editor. You can use the visual **Builder** to add resources, or switch to the **JSON** view to edit the configuration directly.

### Add resources to the fragment

In the fragment editor sidebar, click **+** to add:

- Components and services (cameras, motors, sensors, vision services, and so on)
- Control code modules
- Nested fragments (fragments can include other fragments, up to 5 levels deep)
- Maintenance windows
- Jobs
- Triggers

Nested fragments let you compose configuration libraries. For example, a `base-robot` fragment can include separate `motor-pair` and `camera-array` fragments, so you can swap out the camera array without rewriting the base.

Click **Save** after adding and configuring your resources.

## Apply a fragment to a machine

### In the Viam app

1. Navigate to your machine's **CONFIGURE** tab.
1. Click **+** and select **Configuration block**.
1. Search for your fragment by name and select it.
1. Click **Add fragment**.
1. Click **Add fragment** again to confirm.
1. Click **Save** in the upper right corner.

The fragment's resources now appear on the machine's configuration page. The machine downloads and applies the configuration on its next sync.

### With the CLI

```sh {class="command-line" data-prompt="$"}
viam machines part fragments add --part=<part-id> --fragment=<fragment-id>
```

To find your part ID, run `viam machines part list --machine=<machine-id>`. To find your fragment ID, copy it from the fragment's page in the Viam app (it appears in the URL and under the fragment name).

If you omit `--fragment`, the CLI prompts you to pick a fragment interactively from the ones available to your organization.

To apply a fragment across many machines, see [Automate with scripts](/cli/automate-with-scripts/).

### Avoid resource name conflicts with a prefix

If a machine already has a resource with the same name as one in the fragment, or if you apply the same fragment twice, you need a prefix to avoid name collisions.

When you insert a fragment that would cause a conflict, the UI prompts you for a prefix. The prefix is prepended to every resource name from the fragment. For example, a component named `camera-1` in a fragment with prefix `front` becomes `front-camera-1`.

## Customize fragments with variables

Fragments support variable substitution for values that differ between machines. Define a variable in the fragment's JSON configuration using the `$variable` syntax, then set the value when applying the fragment to each machine.

In the fragment's JSON editor, replace a value with a variable object:

```json
{
  "components": [
    {
      "name": {
        "$variable": {
          "name": "sensor-name"
        }
      },
      "model": "viam:sensor:ultrasonic",
      "type": "sensor",
      "attributes": {
        "trigger_pin": {
          "$variable": {
            "name": "trigger-pin"
          }
        },
        "echo_int_pin": {
          "$variable": {
            "name": "echo-pin"
          }
        }
      }
    }
  ]
}
```

When you apply this fragment to a machine, set the variable values in the fragment card's **Variables** section. Any variables you don't set use the placeholder value as a default.

## Override specific settings

Sometimes you need to change a single value from a fragment without creating a new fragment. Use fragment overrides (called "fragment mods" in JSON) to modify, add, or remove specific fields.

In the machine's **CONFIGURE** tab, find the fragment card and click the field you want to change. Modified fields are highlighted to show they differ from the fragment's default.

In JSON mode, overrides use the `fragment_mods` array with [MongoDB update operator syntax](https://www.mongodb.com/docs/manual/reference/operator/update/), which may look unfamiliar if you have not used MongoDB:

```json
{
  "fragment_mods": [
    {
      "fragment_id": "abcd1234-5678-efgh-ijkl-mnopqrstuvwx",
      "mods": [
        {
          "$set": {
            "components.motor1.attributes.max_rpm": 200
          }
        }
      ]
    }
  ]
}
```

Supported operators: `$set` (change or add a value), `$unset` (remove a value).

## Version and tag fragments for staged rollouts

Every time you save a fragment, Viam creates a new revision. You can pin machines to a specific revision or use tags to control rollouts.

### Create a tag

1. Navigate to your fragment's page.
1. Click **Versions** in the navigation bar.
1. Click **Add Tag**.
1. Enter a tag name (lowercase alphanumeric, hyphens, and underscores; cannot start with a digit or "v"; maximum 60 characters).
1. Select the revision to assign the tag to.
1. Click **Add tag**.

### Pin a machine to a tag or revision

On the machine's **CONFIGURE** tab, find the fragment card and look for the **Update version** section:

- **Latest version**: the machine always uses the newest fragment revision. This is the default.
- **Pin to version**: the machine stays on a specific revision number and never updates automatically.
- **Pin to tag**: the machine uses whichever revision the tag currently points to. When you move the tag to a new revision, the machine updates.

### Staged rollout workflow

1. Create two tags on your fragment: `stable` and `development`.
2. Point `stable` at your current production revision.
3. Pin your production machines to the `stable` tag.
4. Make changes to the fragment. The new revision is created automatically on save.
5. Point `development` at the new revision.
6. Pin a few test machines to `development` and verify the changes work.
7. Once you have confirmed the changes work on your test machines, move `stable` to the new revision. All production machines update.

## Find which machines use a fragment

Before changing or removing a fragment, you usually want to know which machines use it. Viam exposes this through `GetFragmentUsage` (returns a count of machines per revision) and `ListMachineSummaries` (returns the full list of machines and their resolved fragments). Neither is yet wrapped as a high-level method on the Python SDK's `AppClient`. To use them today, call the gRPC stubs from the proto bindings directly, or use any other gRPC client.

## Set default fragments for an organization

You can configure default fragments at the organization level so that every new machine in the organization automatically uses them. Default fragments are applied when a machine is created, whether manually or through provisioning.

To configure default fragments:

- **In the Viam app**: go to your organization's **Settings** page and configure default fragments there.
- **Through the API**: use the fleet management API's `UpdateOrganization` method with the `default_fragments` field.

## JSON reference: fragment imports

In JSON mode on a machine's **CONFIGURE** tab, fragments are listed in the `fragments` array. Each entry supports:

| Field       | Type   | Description                                                                                |
| ----------- | ------ | ------------------------------------------------------------------------------------------ |
| `id`        | string | The fragment ID. Required.                                                                 |
| `version`   | string | Pin to a specific revision number or tag name. Omit to track the latest revision.          |
| `prefix`    | string | A string prepended to all resource names from this fragment. Use to avoid name collisions. |
| `variables` | object | A map of variable names to values, overriding the defaults defined in the fragment.        |

Example:

```json
{
  "fragments": [
    {
      "id": "abcd1234-5678-efgh-ijkl-mnopqrstuvwx",
      "version": "stable",
      "prefix": "front",
      "variables": {
        "sensor_name": "front-ultrasonic",
        "trigger_pin": "15",
        "echo_pin": "16"
      }
    }
  ]
}
```

## Verify the configuration

After applying a fragment to a machine:

1. On the machine's **CONFIGURE** tab, confirm the fragment's resources appear in the resource list.
1. Click **Save** if you haven't already.
1. Go to the **CONTROL** tab and verify the fragment's components respond (for example, test a camera feed or read sensor values).
1. Check the **LOGS** tab for any configuration errors.

To see the fully resolved configuration with all fragments expanded, click **...** (actions menu) on the machine page and select **View debug configuration**.

## Limitations

- Fragments can be nested up to 5 levels deep. Deeper nesting produces an error.
- Circular fragment references (fragment A includes fragment B which includes fragment A) are detected and rejected.
- You cannot add the same fragment to a machine twice without using a prefix.
- Fragment overrides use MongoDB update operator syntax, which may be unfamiliar. The visual editor handles common overrides without requiring JSON.

## Related pages

- [Deploy software](/fleet/deploy-software/) for deploying modules through fragments
- [Deploy ML models](/fleet/deploy-ml-models/) for deploying trained models through fragments
- [Manage versions](/fleet/manage-versions/) for version pinning and maintenance windows
- [Provision devices](/fleet/provision-devices/) for applying fragments to new devices automatically
