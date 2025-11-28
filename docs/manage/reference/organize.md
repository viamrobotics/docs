---
linkTitle: "Organize your machines"
title: "Organize your machines"
weight: 60
layout: "docs"
type: "docs"
no_list: true
description: "Organize and manage access to your fleet by grouping machines into organizations and locations."
aliases:
  - /how-tos/manage-fleet/
  - /use-cases/manage-fleet/
  - /cloud/machines/
  - /fleet/robots/
  - /manage/fleet/machines/
  - /fleet/machines/
  - /cloud/locations/
  - /manage/fleet/locations/
  - /fleet/locations/
  - /cloud/organizations/
  - /manage/fleet/organizations/
  - /fleet/organizations/
---

Before you start connecting your devices to Viam, you need to decide how you want to group your machines.

On Viam, {{< glossary_tooltip term_id="machine" text="machines" >}} are grouped into _locations_, and locations are grouped into _organizations_:

- Each location can represent either a physical location or some other conceptual grouping like "Production" and "Testing".
- An organization is the highest level grouping, and often contains all the locations (and machines) of an entire company.

These groupings allow you to manage permissions; you can grant a user access to an individual machine, to all the machines in a location, or to everything in an entire organization.
You choose how to group your machines.

<p>
{{<imgproc src="/fleet/fleet.svg" class="fill aligncenter" resize="800x" style="width: 600px" declaredimensions=true alt="Two locations within an organization">}}
</p>

## Create organization

1. Log into [Viam](https://app.viam.com) in a web browser.
1. Click the dropdown in the upper-right corner of the **FLEET** page and use the **+** button to create a new organization.
1. Name the organization.
1. From the **Data region** dropdown, choose the [geographic location](/manage/manage/data-regions/) where Viam should store your application data.
1. Click **Create**.

## Create location

1. Click **FLEET** in the upper-left corner of the page and click **LOCATIONS**.
   A new location called `First Location` is automatically generated for you.

   Use the **...** menu to edit the location name to what it represents for your use case.

1. Click **Save**.

1. To create additional locations, click the **+ Add location** button on the **LOCATIONS** page.

## Create sub-locations

If needed, you can add further sub-locations to, for example, differentiate groups of machines within an office.

To add a sub-location:

1. Add a new location using the same **+ Add location** button.
1. On the location's page, click the **...** menu and click **Move**.
1. Choose a new parent for the location.
   This can be the organization the location is in or another location.

You can nest locations up to three levels deep.

## Example

If you'd like to look at an example, see [Monitor Air Quality with a Fleet of Sensors](/tutorials/control/air-quality-fleet/#organize-devices-for-third-party-usage).

## Frequently asked questions

### Can I move a machine to a different location?

Yes, organization owners and location owners can move machines between locations within their organization.

To move a machine:

1. Navigate to your machine's page.
1. Click the **...** button in the upper-right corner.
1. Select **Move to a new location**.
1. Choose the destination location from the organization tree.
1. Confirm the move.

{{< alert title="Important considerations" color="caution" >}}
Moving a machine has several important implications:

- **Machine address changes**: The machine's network address will change to `<machine-main-part-name>.<new-location-id>.viam.cloud`. You'll need to update any code that references the old address.
- **Permission changes**: Access permissions will be updated. Users with access to the current location lose access, and users with access to the new location gain access to the machine.
- **Data access**: Users in the new location cannot access historical data from when the machine was in the previous location.

{{< /alert >}}

**Requirements for moving machines:**

- You must be an organization owner, or an owner of both the current and destination locations
- The destination location must be within the same organization
- No other machine in the destination location can have the same name

### Can I move a location to a different organization?

No, it is not possible to move a location to a different organization.

You can share a location with another organization.
However, machines will continue to use the primary organization as a reference point.
This means any captured data is associated with the primary organization and the machines are only able to use private ML models and registry items from the primary owner.

### Can I rename my organization after its creation?

Yes, you can rename your organization if you are an organization owner.

{{< alert title="Caution" color="caution" >}}
If your organization owns modules or packages in the Viam Registry, the namespace for those modules and packages will be changed in the registry automatically.
You will need to update any configurations that reference your modules using the old namespace.
{{< /alert >}}

1. Click the organization name in the upper-right corner of the **FLEET** page and click on **Settings and invites**.
1. Find the **Details** section of the page.
1. Change the organization name and click on the **Rename** button.

### How do I delete an organization?

1. Delete all the locations in your organization.
1. Click the organization name in the upper-right corner of the **FLEET** page and click on **Settings and invites**.
1. At the bottom of the page click **Delete organization**.
