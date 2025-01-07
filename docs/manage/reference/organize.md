---
linkTitle: "Organize your machines"
title: "Organize your machines"
weight: 60
layout: "docs"
type: "docs"
no_list: true
description: "Organize and manage access to your fleet by grouping machines into organizations and locations."
aliases:
  - /fleet/account/
  - /cloud/account/
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

Before you start connecting your devices to the Viam app, you need to decide how you want to group your machines.

In the Viam app, {{< glossary_tooltip term_id="machine" text="machines" >}} are grouped into _locations_, and locations are grouped into _organizations_:

- Each location can represent either a physical location or some other conceptual grouping like "Production" and "Testing".
- An organization is the highest level grouping, and often contains all the locations (and machines) of an entire company.

These groupings allow you to manage permissions; you can grant a user access to an individual machine, to all the machines in a location, or to everything in an entire organization.
You choose how to group your machines.
You cannot move machines to other locations once created.

<p>
{{<imgproc src="/fleet/fleet.svg" class="fill aligncenter" resize="800x" style="width: 600px" declaredimensions=true alt="Two locations within an organization">}}
</p>

## Create organizations and locations

{{< table >}}
{{% tablestep link="/dev/reference/glossary/#organization" %}}
**1. Create organizations**

1. Log into [Viam app](https://app.viam.com) in a web browser.
1. Click the dropdown in the upper-right corner of the **FLEET** page and use the **+** button to create a new organization.
   Name the organization and click **Create**.
1. Create additional organizations as needed.

{{% /tablestep %}}
{{% tablestep %}}
**2. Create locations**

1. Click **FLEET** in the upper-left corner of the page and click **LOCATIONS**.
   A new location called `First Location` is automatically generated for you.

   Use the **...** menu to edit the location name to what it represents for your use case.
   Then click **Save**.

1. Create additional locations as needed using the **Add location** button, on the left of the **LOCATIONS** page.

{{% /tablestep %}}
{{% tablestep %}}
**3. Create sub-locations**

If needed, you can add further sub-locations to, for example, differentiate groups of machines within an office.

To add a sub-location:

1. Add a new location using the same **Add location** button.

1. At the bottom of the location’s page, use the **New parent location** dropdown to choose a parent location.
   Click **Change**.

   {{<imgproc class="aligncenter" src="/tutorials/air-quality-fleet/locations-done.png" resize="x900" declaredimensions=true alt="The New York Office fleet page. The left Locations navigation panel lists Antonia's Home and RobotsRUs, with New York Office and Oregon Office nested inside RobotsRUs." >}}

You can nest locations up to three levels deep.

{{% /tablestep %}}
{{< /table >}}

## Example

If you'd like to look at an example, see [Monitor Air Quality with a Fleet of Sensors](/tutorials/control/air-quality-fleet/#example).
