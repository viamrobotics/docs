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

Input controllers provide an API for configuring callbacks for events, allowing you to configure input devices to control your machines.

If you have a keyboards, mice, elevator button panels, light power switches, joysticks, and gamepads, or, video game controllers with which you want to control a robotic base, use an _input controller_ component.

This component supports devices like gamepads and joysticks that contain one or more [`Control`s](/appendix/apis/components/input-controller/#control-field) representing the individual axes and buttons on the device.
To use the controller's inputs, you must [register callback functions](/appendix/apis/components/input-controller/#registercontrolcallback) to the [`Control`s](/appendix/apis/components/input-controller/#control-field) with the [`input` API](/appendix/apis/components/input-controller/).

The callback functions can then handle the [Events](/appendix/apis/components/input-controller/#getevents) that are sent when the `Control` is activated or moved.
For example, when a specific button is pushed, the callback function registered to it can move another component, or print a specific output.

The [base remote control service](/services/base-rc/) implements an input controller as a remote control for a base.

## Available models

To use an input controller to control your machine's actions, you need to add it to your machine's configuration.

Go to your machine's **CONFIGURE** page, and add a model that supports your input controller.

The following list shows you the available input controller models.
For additional configuration information, click on the model name:

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

The [input controller API](/appendix/apis/components/input-controller/), which supports the following methods:

{{< readfile "/static/include/components/apis/generated/input_controller-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/how-tos/configure/" noimage="true" %}}
{{% card link="/how-tos/develop-app/" noimage="true" %}}
{{% card link="/tutorials/control/gamepad/" noimage="true" %}}
{{< /cards >}}
