---
title: "Use Fragments to Configure a Fleet of Machines"
linkTitle: "Configure a Fleet"
weight: 40
type: "docs"
description: Use fragments to configure many machines at the same time.
tags: ["fleet management", "cloud", "app"]
---

If you have multiple machines with similar configurations, you can use a _fragment_ to configure all of the machines at the same time.
Fragments are a way of sharing and managing [machine configurations](/build/configure/) across multiple machines.

If there are differences between your machines, you can use a fragment to quickly configure the {{< glossary_tooltip term_id="resource" text="resources" >}} that are the same between machines.
You can then configure the differing resources separately, outside of the fragment.
For example, if you have multiple similar rovers but one has an arm attached, you can add the rover configuration fragment (including the motors and base components), and then configure the arm on just that one rover.

When you or one of your collaborators edit a fragment that you've already deployed to one or more machines, the Viam app updates the configuration on each deployed machine that uses that fragment.

{{< alert title="Alert" color="alert" >}}
Be cautious when making changes to fragments that have been deployed to production machines.
We recommend that you create a duplicate fragment, make your desired change to that second fragment, and then deploy that fragment to a test machine that is configured identically to your production machines.

Once you are confident that your configuration change works as expected, you can safely make the same change to the fragment in use on your production fleet, and the Viam app will deploy that change to all machines using that fragment.
{{< /alert >}}

If you attempt to delete a fragment that is currently deployed to a machine, you will receive an error message advising that the fragment is in use, but you can still delete the fragment if desired.
You can see the number of machines using your fragment from the [fragments page](https://app.viam.com/fragments) in the Viam app.

Fragments are private to each organization by default (except for the `viam-dev` organization).
If you would like to make your fragment available to users outside your organization, please reach out to us to request that we make your fragment public.
You must be an [organization owner](/fleet/rbac/#permissions) in order to create fragments.

A fragment can define one, several, or all resources on a machine.
You can add multiple fragments to a single machine, or can add additional resources to a machine that has already been configured with a fragment.

## Create a fragment

Before you create a fragment, you'll need a JSON configuration file.
The easiest way to create a config file is to [configure](/build/configure/) one of your machines on its **CONFIG** tab in the [Viam app](https://app.viam.com).
Configure all resources that you want to have for all your machines.
If there are any additional resources that you do not want to share with all machines, do not configure them until after you've created the fragment.
When you've finished configuring the resources, go to the **JSON** tab and copy the entire JSON config.
Now you're ready to share that config by creating a fragment.

To create your own private fragment, go to [app.viam.com/fragments](https://app.viam.com/fragments) or click on **Fragments** in the left navigation bar on the [FLEET page](https://app.viam.com/robots).

1. Enter a name for your new fragment and click **Add fragment**.
2. Paste the copied JSON configuration in the config field.
3. Click **SAVE FRAGMENT**.

![Fragment creation view](/fleet/fragment-view.png)

## Add a fragment to a machine

To add a fragment to a machine:

- Go to the **Fragments** subtab of your machine's **Config** tab on the [Viam app](https://app.viam.com).
- Look through the list of available fragments and click **Add** next to any fragments you want to add to your machine.
- Click **Save Config** at the bottom of the screen.

![The fragments subtab](/fleet/fragments-tab.png)

The components and services included in the fragment appear inside a read-only fragment section in the **Components** and **Services** subtabs.

![A fragment in the components subtab](/fleet/fragment-components.png)

In the `Raw JSON` configuration, you will see the fragment ID in the `fragments` section:

```json
{
  "components": [],
  "fragments": ["3e8e0e1c-f515-4eac-8307-b6c9de7cfb84"]
}
```

For an example of adding a fragment to a machine, see the [Add a Rover Fragment to your Machine](/get-started/try-viam/rover-resources/rover-tutorial-fragments/).

## Modify the config of a machine that uses a fragment

When you modify a fragment, those changes are pushed to all machines that use that fragment.
If you need to modify the config of just one machine that uses a fragment you can do the following:

1. Go to the **Fragments** subtab of the **Config** tab.
2. Click **Remove** next to the fragment.
3. Select and copy the contents of the fragment in the box on the right side of the **Fragments** subtab.
4. Toggle to **Raw JSON** mode.
5. Paste the raw fragment contents into the **Raw JSON** config field.
6. Click **Save config**.
7. Now, you can edit the config either in **Raw JSON** mode or in **Builder** mode.

## Next steps

Viam provides several [pre-made fragments](https://app.viam.com/fragments) you can use as a template for writing your own fragments.

For an example of a fragment that configures multiple components and services, see the [Viam Rover fragment](https://app.viam.com/fragment?id=3e8e0e1c-f515-4eac-8307-b6c9de7cfb84).
