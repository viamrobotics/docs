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

A robotic _gantry_ is a mechanical system of linear actuators used to hold and position an [end effector](https://en.wikipedia.org/wiki/Robot_end_effector).
A 3D printer is an example of a three-axis gantry where each linear actuator can move the print head along one axis.
The linear rail design makes gantries a common and reliable system for simple positioning and placement tasks.

This component abstracts the hardware of a gantry to give you an easy interface for coordinated control of linear actuators, even many at once [(multi-axis)](multi-axis/).

<div class="td-max-width-on-larger-screens text-center">
{{<imgproc src="/components/gantry/gantry-illustration.png" resize="300x" declaredimensions=true alt="Example of what a multi-axis robot gantry looks like as a black and white illustration of an XX YY mechanical gantry.">}}
</div>

Gantry components can only be controlled in terms of linear motion (you cannot rotate them).
Each gantry can only move in one axis within the limits of the length of the linear rail.

Most machines with a gantry need at least the following hardware:

- A [board](/components/board/) or [controller](/components/input-controller/) component that can detect changes in voltage on GPIO pins
- A [motor](/components/motor/) that can move linear rails
  - Encoded motor: See [DC motor with encoder](/components/motor/encoded-motor/) and [encoder component](/components/encoder/).
  - Stepper motor: See [Stepper motor](/components/motor/gpiostepper/).
    Requires setting limit switches in the config of the gantry, or setting offsets in the config of the stepper motor.
- Limit switches, to attach to the ends of the gantry's axis

## Related services

{{< cards >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/motion/" >}}
{{< /cards >}}

## Supported models

{{<resources api="rdk:component:gantry" type="gantry">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Control your gantry with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a gantry called `"my_gantry"` configured as a component of your machine.
If your gantry has a different name, change the `name` in the code.

Be sure to import the gantry package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.gantry import Gantry
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/gantry"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The gantry component supports the following methods:

{{< readfile /static/include/components/apis/generated/gantry-table.md" >}}

{{< readfile /static/include/components/apis/generated/gantry.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
