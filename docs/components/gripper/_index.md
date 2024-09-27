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

If you have a physical robotic grasping device that can open and close, use a _gripper_ component.

The gripper component is often used with the following services:

- [motion service](/services/slam/): to move machines or components of machines
- [frame system service](/services/navigation/): to configure the positions of your components

## Available models

To use a robotic gripper, you have to add it to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your gripper.

The following list shows you the available gripper models.
For additional configuration information, click on the model name:

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

To get started using your gripper, see the [gripper API](/appendix/apis/components/gripper/), which supports the following methods:

{{< readfile "/static/include/components/apis/generated/gripper-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
  {{% card link="/how-tos/configure/" noimage="true" %}}
  {{% card link="/how-tos/develop-app/" noimage="true" %}}
  {{% card link="/tutorials/services/plan-motion-with-arm-gripper" noimage="true" %}}
{{< /cards >}}