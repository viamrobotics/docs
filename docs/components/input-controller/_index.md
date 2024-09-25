---
title: "Input Controller Component"
linkTitle: "Input Controller"
weight: 60
type: "docs"
no_list: true
description: "An input controller, like a gamepad or joystick, is a device humans use to control a machine's actions."
tags: ["input controller", "components"]
icon: true
images: ["/icons/components/controller.svg"]
modulescript: true
aliases:
  - "/components/input-controller/"
hide_children: true
# SME: James
---

You are likely already familiar with human-interface devices, like keyboards and mice, elevator button panels, light power switches, joysticks, and gamepads, or, video game controllers, from your daily life.

Configuring an _input_ component allows you to use devices like these with your machine, enabling you to control your machine's actions by interacting with the device.

This component currently supports devices like gamepads and joysticks that contain one or more [Controls](#control-field) representing the individual axes and buttons on the device.
To use the controller's inputs, you must [register callback functions](/components/input-controller/#registercontrolcallback) to the [Controls](#control-field) with the `input` API.

The callback functions can then handle the [Events](/components/input-controller/#getevents) that are sent when the Control is activated or moved.
For example, when a specific button is pushed, the callback function registered to it can move another component, or print a specific output.

Most machines with an input controller need at least the following hardware:

- A computer capable of running `viam-server`.
- A power supply cable or batteries for the input device and the machine.
- A component that you can direct the input to control, like an [arm](/components/arm/) or [motor](/components/motor/).

## Related services

{{< cards >}}
{{< relatedcard link="/services/base-rc/" >}}
{{< /cards >}}

## Available models

To use your input controller component, check whether one of the following models supports it.

For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:input_controller" type="input_controller" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component in `viam-micro-server`.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The input controller component supports the following methods:

{{< readfile "/static/include/components/apis/generated/input_controller-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/configure/configure-rover" %}}
{{% card link="/tutorials/control/gamepad" %}}
{{< /cards >}}
