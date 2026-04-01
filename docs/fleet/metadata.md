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

1. Navigate to the resource you want to add metadata to (machine part, machine, location, or organization).
1. Click the **...** (actions) menu.
1. Select **Custom part metadata**, **Custom machine metadata**, **Custom location metadata**, or **Custom organization metadata** depending on the level.
1. Edit the JSON object in the editor that appears.
1. Click **Save**.

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

The CLI `metadata read` command aggregates metadata across levels. Pass `--organization-id`, `--location-id`, `--machine-id`, or `--machine-part-id` to read specific levels.

## Verify metadata

After adding metadata:

- **Viam app**: click the **...** menu and select the custom metadata option. The JSON object should show your data.
- **CLI**: run `viam metadata read --machine-id=<machine-id>`.
- **SDK**: call the corresponding `Get` method to retrieve and confirm the metadata.

## Related pages

- [Manage your fleet with the CLI](/cli/manage-your-fleet/) for CLI fleet operations
