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

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/use-cases/signup.png" class="fill alignright" resize="600x" style="max-width: 350px" declaredimensions=true alt="Viam app signup screen">}}
**1. Create an account**

Go to the [Viam app](https://app.viam.com) and sign up with Google, GitHub, Apple, or an email address.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/fleet/fleet.svg" class="fill alignleft" resize="600x" style="max-width: 400px" declaredimensions=true alt="Two locations within an organization">}}
**2. Create organizations and locations**

Use [organizations](/fleet/organizations/), and [locations](/fleet/locations/) within them, to organize your machines into groups and manage user access.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/fleet/app-usage/limit-access.png" class="fill alignright" resize="600x" style="max-width: 350px" declaredimensions=true alt="Limit user access">}}
**3. Invite other users and assign permissions**

Invite other users to an organization or a location to [share access](/fleet/#use-viam-for-collaboration) to the machines within it.
Assign each user a role (owner or operator) to manage permissions.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/fleet/app-usage/create-machine.png" class="fill alignleft" resize="600x" style="max-width: 450px" declaredimensions=true alt="Create a new machine in the Viam app">}}
**4. Connect machines to the cloud**

Users with access to a location can create and collaborate on the [machines](/fleet/machines/) within it.
When you [install `viam-server`](/get-started/installation/) on each machine, unique keys are generated to securely connect it to the Viam app.
Use the config builder interface to configure {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} for new or existing smart machines.
You can use {{< glossary_tooltip term_id="fragment" text="fragments" >}} to streamline the process of configuring multiple similar machines.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/use-cases/last-online.png" class="fill alignright" resize="600x" style="max-width: 100px" declaredimensions=true alt="Machine last online status indicator in the Viam app.">}}
**5. Monitor your fleet**

Using the [Viam app](https://app.viam.com), you can:

- Monitor the status of each machine from its [**Logs** tab](/fleet/machines/#logs).
- View any data captured by your fleet from the [**Data** tab](/data/).
- Operate machines remotely from the [**Control** tab](/fleet/machines/#control).

Use [modules](/registry/) to deploy code to your fleet and manage versioning.

{{< /tablestep >}}
{{< /table >}}

## Next steps

{{< cards >}}
{{% card link="/fleet/" %}}
{{% card link="/fleet/cli/" %}}
{{% card link="/fleet/rbac/" %}}

<!-- markdownlint-disable MD034 -->

{{% manualcard link="https://www.viam.com/post/integrate-your-ros2-robot-with-viam/" target="_blank" %}}

<h4>Integrate your ROS2 robot with Viam</h4>

Read a blog post on the ROS integration process.

{{% /manualcard %}}
{{< /cards >}}
