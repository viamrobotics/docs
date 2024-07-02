---
title: "Motion Service"
linkTitle: "Motion"
weight: 20
type: "docs"
description: "The motion service enables your machine to plan and move its components relative to itself, other machines, and the world."
tags: ["motion", "motion planning", "services"]
icon: true
images: ["/services/icons/motion.svg"]
no_list: true
aliases:
  - "/services/motion/"
  - "/mobility/motion/"
no_service: true
# SME: Motion team
---

The motion service enables your machine to plan and move itself or its components relative to itself, other machines, and the world.
The motion service:

1. Gathers the current positions of the machine’s components as defined with the [frame system](../frame-system/).
2. Plans the necessary motions to move a component to a given destination while obeying any [constraints you configure](constraints/).

The motion service can:

- use motion [planning algorithms](algorithms/) locally on your machine to plan coordinated motion across many components.
- pass movement requests through to individual components which have implemented their own motion planning.

## Used with

{{< cards >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/components/movement-sensor/" required="yes">}}
{{< relatedcard link="/components/base/" >}}
{{< relatedcard link="/components/arm/" >}}
{{< relatedcard link="/components/gripper/" >}}
{{< /cards >}}

{{% snippet "required-legend.md" %}}

## Configuration

You need to configure frames for your machine's components with the [frame system](../frame-system/).
This defines the spatial context within which the motion service operates.

The motion service itself is enabled on the machine by default, so you do not need to do any extra configuration in the [Viam app](https://app.viam.com/) to enable it.

{{% alert title="Tip" color="tip" %}}

Because the motion service is enabled by default, you don't give it a `"name"` while configuring it.
Use the name `"builtin"` to access the built-in motion service in your code with methods like [`FromRobot()`](/appendix/apis/#fromrobot) that require a `ResourceName`.

{{% /alert %}}

## API

The motion service supports the following methods:

{{< readfile "/static/include/services/apis/generated/motion-table.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a machine configured with a gripper, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **CONNECT** tab on the [Viam app](https://app.viam.com) and select the **Code sample** page for boilerplate code to connect to your machine.

{{% /alert %}}

{{% alert title="Important" color="note" %}}

When using Viam component APIs, you generally pass the component name of type `string` as an argument to the methods.
When using the motion service, you pass an argument of type `ResourceName` instead of the string name.
For examples showing how to construct the `ResourceName`, see the code samples below or [this tutorial](/tutorials/services/plan-motion-with-arm-gripper/#get-the-resourcename).

{{% /alert %}}

{{< readfile "/static/include/services/apis/generated/motion.md" >}}

## Test the motion service

You can test motion on your machine from the [**CONTROL** tab](/fleet/control/).

![Motion card on the Control tab](/services/motion/motion-rc-card.png)

Enter x and y coordinates to move your machine to, then click the **Move** button to issue a `MoveOnMap()` request.

{{< alert title="Info" color="info" >}}

The `plan_deviation_m` for `MoveOnMap()` on calls issued from the **CONTROL** tab is 0.5 m.

{{< /alert >}}

## Next steps

The following tutorials contain complete example code for interacting with a robot arm through the arm component API, and with the motion service API, respectively:

{{< cards >}}
{{% card link="/tutorials/services/accessing-and-moving-robot-arm" %}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper" %}}
{{< /cards >}}
