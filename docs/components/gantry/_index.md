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
<img src="/components/gantry/gantry-illustration.png" style="max-width:300px" alt="Example of what a multi-axis robot gantry looks like as a black and white illustration of an XX YY mechanical gantry." class="alignright imgzoom">
</div>

A _gantry_ component represents a mechanical system of linear actuators used to hold and position an [end effector](https://en.wikipedia.org/wiki/Robot_end_effector).
A 3D printer is an example of a three-axis gantry where each linear actuator can move the print head along one axis.
The linear rail design makes gantries a common and reliable system for simple positioning and placement tasks.

This component abstracts the hardware of a gantry to give you an easy interface for coordinated control of linear actuators, even many at once [(multi-axis)](multi-axis/).

Gantry components can only be controlled in terms of linear motion (you cannot rotate them).
Each gantry can only move in one axis within the limits of the length of the linear rail.

## Available models

To use a gantry, you have to add it, and any dependencies, such as a [board](/components/board/), [input controller](/components/input-controller/), or a [motor](/components/motor/), to your machine's configuration.
Go to your machine's **CONFIGURE** page, and add a model that supports your gantry.

The following list shows you the available gantry models.
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

## Related services

{{< cards >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/motion/" >}}
{{< /cards >}}

## API

The gantry component supports the following methods:

{{< readfile "/static/include/components/apis/generated/gantry-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
