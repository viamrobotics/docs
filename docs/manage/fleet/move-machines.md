---
title: "Move machines between locations"
linkTitle: "Move machines"
weight: 70
layout: "docs"
type: "docs"
description: "Move machines between locations within your organization using the web UI."
tags: ["fleet management", "machines", "locations", "organization"]
---

Organization owners and location owners can move machines between locations within their organization.
This feature allows you to reorganize your fleet as your needs change, such as moving machines from testing to production environments or relocating physical devices.

## Prerequisites

To move a machine, you must meet one of the following permission requirements:

- **Organization owner**: Can move any machine within the organization
- **Location owner**: Can move machines between locations where you have owner permissions for both the source and destination locations

Additionally:

- The destination location must be within the same organization (you cannot move machines between organizations)
- No other machine in the destination location can have the same name as the machine you're moving

## Move a machine using the web UI

1. Navigate to your machine's page in [Viam](https://app.viam.com).
1. Click the **...** (Actions) button in the upper-right corner of the page.
1. Select **Move to a new location** from the dropdown menu.
1. In the location selector modal, choose the destination location from your organization's location tree.
1. Click **Choose** to confirm your selection.
1. Review the warning modal that explains the implications of moving the machine.
1. Click **Move machine to new location** to confirm the move.

After the move is complete, you'll see a success notification and the machine's page will update to reflect the new location.

## What happens when you move a machine

Moving a machine between locations has several important effects:

### Machine address changes

The machine's network address automatically updates to reflect the new location:

- **Old address**: `<machine-main-part-name>.<old-location-id>.viam.cloud`
- **New address**: `<machine-main-part-name>.<new-location-id>.viam.cloud`

{{< alert title="Action required" color="caution" >}}
You must update any code that references the machine's address, including:

- SDK code that connects to the machine
- Remote part configurations
- Any hardcoded machine addresses in your applications

{{< /alert >}}

### Permission changes

Access permissions are updated based on the new location:

- Users who had access through the old location may lose access to the machine
- Users with access to the new location will gain access to the machine
- Machine-specific permissions remain unchanged

### Data access restrictions

Historical data access is preserved based on location permissions at the time the data was captured:

- Users in the new location cannot access historical data from when the machine was in the previous location
- This ensures data privacy and maintains proper access controls
- New data captured after the move will be accessible to users with access to the new location

### Query and data impacts

- Location-specific data queries may return different results
- Machine-specific queries will continue to work but may need updated location context
- Data visualization dashboards may need to be updated to reflect the new location

## Best practices

### Before moving a machine

1. **Document current integrations**: Make a list of all code, configurations, and integrations that reference the machine's current address.

1. **Check permissions**: Verify that the appropriate users will have access to the machine in its new location.

1. **Plan for downtime**: Consider scheduling the move during a maintenance window if the machine is critical to operations.

1. **Backup configurations**: Export the machine's configuration as a backup before making changes.

### After moving a machine

1. **Update code references**: Update all SDK code, remote part configurations, and applications that reference the old machine address.

1. **Verify connectivity**: Test that all integrations work correctly with the new machine address.

1. **Update documentation**: Update any internal documentation that references the machine's location or address.

1. **Consider API key rotation**: For enhanced security, consider rotating the machine's API keys after the move.

1. **Update monitoring**: Update any monitoring or alerting systems that reference the machine's location.

## Troubleshooting

### "Cannot move machine" error

If you receive an error when trying to move a machine, check the following:

- **Permissions**: Ensure you have owner permissions for both the source and destination locations, or are an organization owner.
- **Name conflicts**: Verify that no other machine in the destination location has the same name.
- **Organization boundaries**: Confirm that both locations are within the same organization.

### Machine not accessible after move

If you cannot access the machine after moving it:

1. **Check the new address**: Ensure you're using the updated machine address with the new location ID.
1. **Verify permissions**: Confirm that your user account has access to the new location.
1. **Update API keys**: If using API keys, ensure they have the correct permissions for the new location.

### Data queries returning unexpected results

If your data queries are returning different results after moving a machine:

1. **Update location filters**: Modify queries to use the new location ID.
1. **Check time ranges**: Historical data queries may need to account for the location change date.
1. **Review dashboard configurations**: Update any dashboards or visualizations that filter by location.

## API reference

You can also move machines programmatically using the [Fleet Management API](/dev/reference/apis/fleet/). Use the `UpdateRobot` method with the new location parameter:

```python
# Update robot location using the Fleet Management API
await app_client.update_robot(
    id="your-robot-id",
    name="your-robot-name",  # Keep the same name
    location="new-location-id"
)
```

For more information about the Fleet Management API, see the [API documentation](/dev/reference/apis/fleet/).

## Related resources

- [Organize your machines](/manage/reference/organize/)
- [Fleet Management API](/dev/reference/apis/fleet/)
- [Manage access and permissions](/manage/manage/access/)
- [API keys](/operate/control/api-keys/)