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
---

You can use Viam's cloud-based fleet management tools to monitor and manage access to your fleet of {{< glossary_tooltip term_id="smart-machine" text="smart machines" >}}.
Use these tools as you create and scale a new fleet of smart machines, or integrate Viam to manage and add functionality like data management to your existing fleet.

For example, you might have 30 robots in one warehouse and 500 in another.
You can monitor and teleoperate all of the robots from one online dashboard, and grant permission to other users to do the same.
You can grant users different levels of access to individual machines or to groups of machines.

If you'd like to follow a more detailed tutorial, see [Monitor Air Quality with a Fleet of Sensors](/tutorials/control/air-quality-fleet/).

{{< table >}}
{{% tablestep %}}
**1. Create an account**

Go to the [Viam app](https://app.viam.com) and sign up with Google, GitHub, Apple, or an email address.

{{% /tablestep %}}
{{% tablestep link="/cloud/" %}}
**2. Create organizations and locations**

Use [organizations](/cloud/organizations/), and [locations](/cloud/locations/) within them, to organize your machines into groups and manage user access.

{{<imgproc src="/fleet/fleet.svg" class="fill aligncenter" resize="800x" style="max-width: 600px" declaredimensions=true alt="Two locations within an organization">}}

{{% /tablestep %}}
{{% tablestep link="/cloud/rbac/" %}}
**3. Invite other users and assign permissions**

Invite other users to an organization or a location to [share access](/fleet/#use-viam-for-collaboration) to the machines within it.
Assign each user a role (owner or operator) to manage permissions.

{{<imgproc src="/fleet/app-usage/limit-access.png" resize="1000x" style="max-width: 600px" class="aligncenter" declaredimensions=true alt="Limit user access">}}

{{% /tablestep %}}
{{% tablestep link="/get-started/installation/" %}}
**4. Connect machines to the cloud**

Users with access to a location can create and collaborate on the [machines](/cloud/machines/) within it.
When you [install `viam-server`](/installation/) on each machine, unique keys are generated to securely connect it to the Viam app.
Use the config builder interface to configure {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} for new or existing smart machines.
You can use {{< glossary_tooltip term_id="fragment" text="fragments" >}} to streamline the process of configuring multiple similar machines.

{{<imgproc src="/fleet/app-usage/create-machine.png" class="fill aligncenter" resize="800x" style="max-width: 600px" declaredimensions=true alt="Create a new machine in the Viam app">}}

{{% /tablestep %}}
{{% tablestep %}}
**5. Monitor your fleet**

Using the [Viam app](https://app.viam.com), you can:

- Monitor the status of each machine from its [**LOGS** tab](/cloud/machines/#logs).
- View any data captured by your fleet from the [**Data** tab](/services/data/).
- Operate machines remotely from the [**CONTROL** tab](/fleet/control/).

{{% /tablestep %}}
{{< /table >}}

## Next steps

{{< cards >}}
{{% card link="/fleet/" %}}
{{% card link="/cli/" %}}
{{% card link="/cloud/rbac/" %}}

<!-- markdownlint-disable MD034 -->

{{% manualcard link="https://www.viam.com/post/integrate-your-ros2-robot-with-viam/" target="_blank" %}}

<h4>Integrate your ROS2 robot with Viam</h4>

Read a blog post on the ROS integration process.

{{% /manualcard %}}
{{< /cards >}}
