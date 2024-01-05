---
title: "Manage a fleet of machines"
linkTitle: "Manage a fleet of machines"
weight: 70
type: "docs"
tags: ["fleet management", "app", "services"]
no_list: true
description: "Use Viam's fleet management capabilities to share and manage access to your machines."
image: "/fleet/locations.png"
imageAlt: "Fleet management"
images: ["/fleet/locations.png"]
---

You can use Viam's cloud-based fleet management tools to monitor and manage access to your fleet of {{< glossary_tooltip term_id="smart-machine" text="smart machines" >}}.
Use these tools as you create and scale a new fleet of smart machines, or integrate Viam to manage and add functionality like data management to your existing fleet.

For example, you might have 30 robots in one warehouse and 500 in another.
You can monitor and teleoperate all of the robots from one online dashboard, and grant permission to other users to do the same.
You can grant users different levels of access to individual machines or to groups of machines.

<table>
  <tr>
    <th>{{<imgproc src="/use-cases/signup.png" class="fill alignright" resize="600x" style="max-width: 350px" declaredimensions=true alt="Viam app signup screen">}}
      <b>1. Create an account</b>
      <p>Go to the <a href="https://app.viam.com">Viam app</a> and sign up with Google, GitHub, Apple, or an email address.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/fleet/locations.png" class="fill alignleft" resize="600x" style="max-width: 400px" declaredimensions=true alt="Two locations within an organization">}}
      <b>2. Create organizations and locations</b>
      <p>Use <a href="/fleet/organizations/">organizations</a>, and <a href="/fleet/locations/">locations</a> within them, to organize your machines into groups and manage user access.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/fleet/app-usage/limit-access.png" class="fill alignright" resize="600x" style="max-width: 350px" declaredimensions=true alt="Limit user access">}}
      <b>3. Invite other users and assign permissions</b>
      <p>Invite other users to an organization or a location to <a href="/fleet/#use-viam-for-collaboration">share access</a> to the machines within it. Assign each user a role (owner or operator) to manage permissions.</p>
    </th>
  </tr>
  <tr>
    <td>{{<imgproc src="/fleet/app-usage/create-machine.png" class="fill alignleft" resize="600x" style="max-width: 450px" declaredimensions=true alt="Create a new machine in the Viam app">}}
      <b>4. Connect machines to the cloud</b>
      <p>Users with access to a location can create and collaborate on the <a href="/fleet/machines/">machines</a> within it. When you <a href="/get-started/installation/">install <code>viam-server</code></a> on each machine, unique keys are generated to securely connect it to the Viam app. Use the config builder interface to configure {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}} for new or existing smart machines. You can use {{< glossary_tooltip term_id="fragment" text="fragments" >}} to streamline the process of configuring multiple similar machines.</p>
    </td>
  </tr>
  <tr>
    <td>{{<imgproc src="/use-cases/last-online.png" class="fill alignright" resize="600x" style="max-width: 100px" declaredimensions=true alt="Machine last online status indicator in the Viam app.">}}
      <b>5. Monitor your fleet</b>
      <p>View the status and logs from each machine in the <a href="https://app.viam.com">Viam app</a>, gather machine sensor <a href="/data/">data</a>, and operate machines remotely from the <a href="/fleet/machines/#control"><strong>Control</strong> tab</a>. Use <a href="/registry/">modules</a> to deploy code to your fleet and manage versioning.</p>
    </td>
  </tr>
</table>

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
