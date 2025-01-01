---
linkTitle: "Move an arm"
title: "Move an arm"
weight: 50
layout: "docs"
type: "docs"
no_list: true
description: "Move an arm with joint positions or automated motion planning."
---

You have two options for moving a robotic [arm](/operate/reference/components/arm/):

- Use direct joint position commands and simple linear commands with the [arm API](/dev/reference/apis/components/arm/)
- Use automated complex motion planning with the [motion planning service API](/dev/reference/apis/services/motion/)

{{< cards >}}
{{% card link="/dev/reference/apis/components/arm/" %}}
{{% card link="/dev/reference/apis/services/motion/" %}}
{{< /cards >}}

## Tutorials and example usage

{{< cards >}}
{{% card link="/operate/mobility/move-arm/move-robot-arm/" %}}
{{% card link="/operate/mobility/move-arm/plan-motion-with-arm-gripper/" %}}
{{% card link="/operate/mobility/move-arm/constrain-motion/" %}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{< /cards >}}
