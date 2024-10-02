---
title: "Motion Service"
linkTitle: "Motion"
weight: 40
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

1. Gathers the current positions of the machine’s components as defined with the [frame system](/services/frame-system/).
2. Plans the necessary motions to move a component to a given destination while obeying any [constraints you configure](constraints/).

The motion service can:

- use motion [planning algorithms](algorithms/) locally on your machine to plan coordinated motion across many components.
- pass movement requests through to individual components which have implemented their own motion planning.

## Configuration

You need to configure frames for your machine's components with the [frame system](/services/frame-system/).
This defines the spatial context within which the motion service operates.

The motion service itself is enabled on the machine by default, so you do not need to do any extra configuration in the [Viam app](https://app.viam.com/) to enable it.

## API

The [motion service API](/appendix/apis/services/motion/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/motion-table.md" >}}

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
