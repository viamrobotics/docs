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

The _input controller_ component represents devices, such as keyboards and mice, elevator button panels, light power switches, joysticks, and gamepads, or, video game controllers.

This component supports devices like gamepads and joysticks that contain one or more [`Control`s](/appendix/apis/components/input-controller/#control-field) representing the individual axes and buttons on the device.
To use the controller's inputs, you must [register callback functions](/appendix/apis/components/input-controller/#registercontrolcallback) to the [`Control`s](/appendix/apis/components/input-controller/#control-field) with the [`input` API](/appendix/apis/components/input-controller/).

The callback functions can then handle the [Events](/appendix/apis/components/input-controller/#getevents) that are sent when the `Control` is activated or moved.
For example, when a specific button is pushed, the callback function registered to it can move another component, or print a specific output.

## Available models

To use an input controller to control your machine's actions, you have to add it as well as any components you are trying to control, to your machine's configuration.

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

## Related services

{{< cards >}}
{{< relatedcard link="/services/base-rc/" >}}
{{< /cards >}}

## API

To get started using your input controller, see the [input controller API](/appendix/apis/components/input-controller/), which supports the following methods:

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