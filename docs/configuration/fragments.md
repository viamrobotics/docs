---
title: "Fragments"
linkTitle: "Fragments"
weight: 40
type: "docs"
no_list: true
description: "Fragments are a way of sharing and managing identical configuration files (or parts of config files) across multiple robots."
tags: ["manage", "fragments"]
---

{{% alert title="Note" color="note" %}}

Fragments are an experimental feature.
Stability is not guaranteed.

{{% /alert %}}

Fragments are a way of sharing and managing identical configuration files (or parts of config files) across multiple robots.
For example, if you have multiple robots with the same hardware, wired the same way, you can create and share a fragment and add it to any number of robots.
When changes are made to the fragment, those changes are automatically carried to all robots that include the fragment in their config.

You can add a fragment to a robot's config and also add other configuration outside the fragment.
For example, if you have multiple identical rovers but one has an arm attached, you can add the rover configuration fragment (including the motors and base components), and then configure the arm on just that one rover.

To add a fragment to a robot:

- Go to the **FRAGMENTS** sub-tab of your robot's **CONFIG** tab on the [Viam app](https://app.viam.com).
- Look through the list of available fragments and click **ADD** next to any fragments you want to add to your robot.
- Click **Save Config** at the bottom of the screen.

{{% alert title="Note" color="note" %}}

The components or other resources included in the fragment will *not* appear in the **COMPONENTS** sub-tab or in the `components` section of your config.
You will simply see the fragment ID in the `fragments` section of your config, but all the resources *will* appear on the **CONTROL** tab when your robot comes on line, and they will be accessible from SDK code as regular resources of your robot.

{{% /alert %}}

To create a fragment, go to [app.viam.com/fragments](https://app.viam.com/fragments).

For an example of adding a fragment to a robot, see the [Viam Rover fragment tutorial](/try-viam/rover-resources/rover-tutorial-fragments/).
