---
title: "Gripper Component"
linkTitle: "Gripper"
childTitleEndOverwrite: "Gripper Component"
weight: 60
type: "docs"
description: "A gripper is a robotic grasping device that can open and close."
tags: ["gripper", "components"]
icon: true
images: ["/icons/components/gripper.svg"]
no_list: true
modulescript: true
aliases:
  - "/components/gripper/"
hide_children: true
# SMEs: Bucket Team
---

A _gripper_ is a robotic grasping device that can open and close, often attached to the end of an [arm](../arm/) or to a [gantry](../gantry/).

## Related services

{{< cards >}}
{{< relatedcard link="/services/data/" >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/motion/" >}}
{{< /cards >}}

## Available models

To use your gripper component, check whether one of the following models supports it.

For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:gripper" type="gripper" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component in `viam-micro-server`.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The gripper component supports the following methods:

{{< readfile "/static/include/components/apis/generated/gripper-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next steps

{{< cards >}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper" %}}
{{< /cards >}}
