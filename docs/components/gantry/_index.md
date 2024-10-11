---
title: "Gantry Component"
linkTitle: "Gantry"
childTitleEndOverwrite: "Gantry Component"
no_list: true
weight: 50
type: "docs"
description: "A mechanical system of linear rails that can precisely position an attached device."
tags: ["gantry", "components"]
icon: true
images: ["/icons/components/gantry.svg"]
modulescript: true
aliases:
  - "/components/gantry/"
hide_children: true
# SME: Rand
---

<div class="td-max-width-on-larger-screens text-center">
<img src="gantry-illustration.png" style="width:300px" alt="Example of what a multi-axis robot gantry looks like as a black and white illustration of an XX YY mechanical gantry." class="alignright imgzoom">
</div>

The gantry component provides an API for coordinated control of one or more linear actuators.

If you have a physical gantry, that is a mechanical system of linear actuators used to hold and position an [end effector](https://en.wikipedia.org/wiki/Robot_end_effector), use a gantry component.

A 3D printer is an example of a three-axis gantry where each linear actuator can move the print head along one axis.

Gantry components can only be controlled in terms of linear motion (you cannot rotate them).
Each gantry can only move in one axis within the limits of the length of the linear rail.

## Available models

To use a gantry, you need to add it to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your gantry.

The following list shows the available gantry models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:gantry" type="gantry" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component in `viam-micro-server`.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The [gantry API](/appendix/apis/components/gantry/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/gantry-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{< /cards >}}

You can also use the gantry component with the following services:

- [Motion service](/services/slam/): To move machines or components of machines
- [Frame system service](/services/navigation/): To configure the positions of your components
