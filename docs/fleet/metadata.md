---
linkTitle: "Add custom metadata"
title: "Add custom metadata"
weight: 50
layout: "docs"
type: "docs"
description: "Attach custom key-value data to machine parts, machines, locations, and organizations."
---

Attach custom metadata as a JSON object to any level of your fleet hierarchy: machine parts, machines, locations, or organizations. Use metadata to store deployment details, maintenance notes, device serial numbers, or any other data you need to track alongside your machines.

## Add metadata in the Viam app

1. Navigate to the machine part, machine, or location you want to add metadata to.
1. Click the **...** (actions) menu.
1. Select **Custom part metadata**, **Custom machine metadata**, or **Custom location metadata** depending on the level.
1. Edit the JSON object in the editor that appears.
1. Click **Save**.

Organization-level metadata is available through the SDK and CLI but not through the Viam app UI.

Metadata is stored as an arbitrary JSON object with no required schema. You define the structure.

Example:

```json
{
  "serial_number": "SN-2026-0042",
  "deployment_date": "2026-03-15",
  "facility": "Building A, Line 3",
  "firmware_batch": "v2.1.0-rc3"
}
```

## Add metadata with the SDK

Use the fleet management API to read and update metadata programmatically at each level:

| Level        | Get method                | Update method                |
| ------------ | ------------------------- | ---------------------------- |
| Machine part | `GetRobotPartMetadata`    | `UpdateRobotPartMetadata`    |
| Machine      | `GetRobotMetadata`        | `UpdateRobotMetadata`        |
| Location     | `GetLocationMetadata`     | `UpdateLocationMetadata`     |
| Organization | `GetOrganizationMetadata` | `UpdateOrganizationMetadata` |

## Add metadata with the CLI

Read metadata for a machine and its parts:

```sh {class="command-line" data-prompt="$"}
viam metadata read --machine-id=<machine-id>
```

The CLI `metadata read` command aggregates metadata across levels. Pass `--org-id`, `--location-id`, `--machine-id`, or `--part-id` to read specific levels.

## Verify metadata

After adding metadata:

- **Viam app**: click the **...** menu and select the custom metadata option. The JSON object should show your data.
- **CLI**: run `viam metadata read --machine-id=<machine-id>`.
- **SDK**: call the corresponding `Get` method to retrieve and confirm the metadata.

## Limitations

- Metadata cannot be deployed through fragments. Each machine's metadata must be set individually through the UI, SDK, or CLI.
- To set metadata on many machines at once, use the SDK in a script that iterates over your machines.

## Related pages

- [Manage your fleet with the CLI](/cli/manage-your-fleet/) for CLI fleet operations
- [Automate with scripts](/cli/automate-with-scripts/) for scripting fleet operations
