---
title: "Manage a fleet of machines"
linkTitle: "Manage a fleet of machines"
weight: 70
type: "docs"
tags: ["fleet management", "app", "services"]
no_list: true
description: "Use Viam's fleet management capabilities to share and manage access to your machines."
images: ["/platform/fleet.svg"]
imageAlt: "Fleet management"
aliases:
  - /use-cases/manage-fleet/
languages: []
viamresources: []
level: "Beginner"
date: "2024-02-27"
updated: "2024-09-02"
cost: "0"
---

You can use Viam's cloud-based fleet management tools to monitor and manage access to your fleet of {{< glossary_tooltip term_id="smart-machine" text="smart machines" >}}.
Use these tools as you create and scale a new fleet of smart machines, or integrate Viam to manage and add functionality like data management to your existing fleet.

For example, you might have 30 robots in one warehouse and 500 in another.
You can monitor and teleoperate all of the robots from one online dashboard, and grant permission to other users to do the same.
You can grant users different levels of access to individual machines or to groups of machines.

{{% alert title="In this page" color="info" %}}

1. [Organize your machines](#organize-your-machines): Learn about organizations and locations
1. [Manage access with role-based access control](#manage-access-with-role-based-access-control)
1. [Monitoring and debugging](/how-tos/manage-fleet/#monitoring-and-debugging)

{{% /alert %}}

## Prerequisites

{{% expand "A Viam account" %}}

Go to the [Viam app](https://app.viam.com) and sign up with Google, GitHub, Apple, or an email address.

{{% /expand%}}

## Organize your machines

Before you start connecting your devices to the Viam app, you need to decide how you want to group your devices.

In the Viam app, {{< glossary_tooltip term_id="machine" text="machines" >}} are grouped into _locations_, and locations are grouped into _organizations_:

- Each location can represent either a physical location or some other conceptual grouping.
- An organization is the highest level grouping, and often contains all the locations (and machines) of an entire company.

These groupings allow you to manage permissions; you can grant a user access to an individual machine, to all the machines in a location, or to everything in an entire organization.
You choose how to group your machines.

{{<imgproc src="/fleet/fleet.svg" class="fill aligncenter" resize="800x" style="max-width: 600px" declaredimensions=true alt="Two locations within an organization">}}

If you'd like to look at an example, see [Monitor Air Quality with a Fleet of Sensors](/tutorials/control/air-quality-fleet/#example).

{{< table >}}
{{% tablestep link="/cloud/organizations/" %}}
**1. Create organizations**

1. Log into [Viam app](https://app.viam.com) in a web browser.
1. Click the dropdown in the upper-right corner of the **FLEET** page and use the **+** button to create a new organization.
   Name the organization and click **Create**.
1. Create additional organizations as needed.

{{% /tablestep %}}
{{% tablestep link="/cloud/locations/" %}}
**2. Create locations**

1. Click **FLEET** in the upper-left corner of the page.
   A new location called `First Location` is automatically generated for you.

   Click the pencil icon next to the location name and give it a name for what it represents for your use case.
   Then click **Save**.

1. Create additional locations as needed using **New location** interface, on the left of the **FLEET** page.

{{% /tablestep %}}
{{% tablestep link="/cloud/locations/" %}}
**3. Create sub-locations**

If needed, you can add further sub-locations to, for example, differentiate groups of machines within an office.

To add a sub-location:

1. Add a new location using the same **New location** interface.

1. At the bottom of the location’s page, use the New Parent Location dropdown to choose a parent location.
   Click **Change**.

   {{<imgproc class="aligncenter" src="/tutorials/air-quality-fleet/locations-done.png" resize="x900" declaredimensions=true alt="The New York Office fleet page. The left Locations navigation panel lists Antonia's Home and RobotsRUs, with New York Office and Oregon Office nested inside RobotsRUs." >}}

You can nest locations up to three levels deep.

{{% /tablestep %}}
{{< /table >}}

## Manage Access with Role-Based Access Control

To collaborate with others on your machines, you need to invite them to your organizations, locations, or machines:

{{< table >}}
{{% tablestep link="/cloud/rbac/" %}}
**1. Invite users and assign permissions**

If you have the **Owner** role, you can invite new users to an organization or a location to [share access](/cloud/#use-viam-for-collaboration) to the machines within it.
Assign each user a role (owner or operator) to manage permissions.

{{<imgproc src="/fleet/app-usage/limit-access.png" resize="1000x" style="max-width: 600px" class="aligncenter" declaredimensions=true alt="Limit user access">}}

Users with owner access to a location or organization, can collaborate on the [machines](/cloud/machines/) within it.

{{% /tablestep %}}
{{% tablestep link="/installation/" %}}
**2. Use API keys**

You (and anyone with owner access) can create API keys for programmatic access to machines, locations, or organizations.

Click on the organization dropdown in the top navigation bar and click on **Settings** to create and manage API keys.

{{<imgproc src="/cloud/rbac.png" resize="700x" declaredimensions=true alt="Organization page" class="aligncenter">}}

{{% /tablestep %}}
{{< /table >}}

## Monitoring and debugging

Viam allows you to access each machine, check its logs, check recent changes, and roll back changes if needed.

{{< table >}}
{{% tablestep link="/cloud/machines/#logs" %}}
**1. Monitor your fleet's logs**

Using the [Viam app](https://app.viam.com), you can monitor the status of each machine from its [**LOGS** tab](/cloud/machines/#logs).

{{<gif webm_src="/fleet/log-filtering.webm" mp4_src="/fleet/log-filtering.mp4" alt="Filter logs by term of log level in the UI" max-width="800px">}}

You can also access machine logs using [`viam machines logs`](/cli/#machines-alias-robots), the [Machines API](/appendix/apis/robot/), or the [Viam mobile app](/cloud/machines/#logs).

{{% /tablestep %}}
{{% tablestep link="/fleet/control/" %}}
**2. Test your machines remotely**

Using the [Viam app](https://app.viam.com), you can remotely operate machines from the [**CONTROL** tab](/fleet/control/).

{{<gif webm_src="/fleet/control.webm" mp4_src="/fleet/control.mp4" alt="Using the control tab" max-width="800px">}}

You can also operate machine using the [`viam machines part run`](/cli/#machines-alias-robots) CLI command or [Viam's APIs](/appendix/apis/), or the [Viam mobile app](/fleet/control/#control-interface-in-the-viam-mobile-app).

{{% /tablestep %}}
{{% tablestep link="/configure/#configuration-history" %}}
**3. Use configuration version history**

The Viam app keeps a record of your configuration changes, allowing you to revert to earlier configurations if needed. To see the history of the configuration of a machine part, click on **History** on the component or machine menu on the CONFIGURE tab.

{{<imgproc src="build/configure/history.png" resize="800x" declaredimensions=true alt="Configuration history for a machine part">}}

{{% /tablestep %}}
{{< /table >}}

## Next steps

If you haven't configured your machines yet, start there and explore provisioning.

{{< cards >}}
{{% card link="/how-tos/one-to-many/" %}}
{{% card link="/how-tos/provision-setup/" %}}
{{< /cards >}}

With your machines set up on Viam, you can now manage data across all your machines, as well as use machine learning, SLAM, and other platform capabilities:

{{< cards >}}
{{% card link="/how-tos/collect-sensor-data/" %}}
{{% card link="/how-tos/deploy-ml/" %}}
{{% card link="/how-tos/navigate/" %}}
{{< /cards >}}
