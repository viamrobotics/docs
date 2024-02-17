---
title: "Use Fragments to Configure a Fleet of Machines"
linkTitle: "Configure a Fleet"
weight: 40
type: "docs"
description: Use fragments to configure many machines at the same time.
tags: ["fleet management", "cloud", "app"]
---

If you have multiple identical or similar machines, use a _fragment_ to configure all of the machines at the same time.

Fragments are a way of sharing and managing [machine configurations](/build/configure/) across multiple machines.
When you or one of your collaborators changes the fragment, the Viam app automatically applies the changes to all machines that include the fragment in their config.

If there are differences between your machines, you can use a fragment to quickly configure the {{< glossary_tooltip term_id="resource" text="resources" >}} that are the same between machines.
You can then configure the differing resources separately, outside of the fragment.
For example, if you have multiple identical rovers but one has an arm attached, you can add the rover configuration fragment (including the motors and base components), and then configure the arm on just that one rover.

See [Fragments](/build/configure/#fragments) for more information.

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
