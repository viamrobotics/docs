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
date: "2024-10-21"
# SME: James
---

The input controller API provides an API for configuring callbacks for events, allowing you to configure input devices to control your machines.

If you have a keyboard, mouse, elevator button panel, light power switch, joystick, gamepad, or video game controllers with which you want to control a robotic base, use an input controller component.

This component supports devices like gamepads and joysticks that contain one or more [`Control`s](/dev/reference/apis/components/input-controller/#control-field) representing the individual axes and buttons on the device.
To use the controller's inputs, you must [register callback functions](/dev/reference/apis/components/input-controller/#registercontrolcallback) to the [`Control`s](/dev/reference/apis/components/input-controller/#control-field) with the [`input` API](/dev/reference/apis/components/input-controller/).

The callback functions can then handle the [Events](/dev/reference/apis/components/input-controller/#getevents) that are sent when the `Control` is activated or moved.
For example, when a specific button is pushed, the callback function registered to it can move another component, or print a specific output.

The [base remote control service](/operate/reference/services/base-rc/) implements an input controller as a remote control for a base.

## Configuration

To use an input controller to control your machine's actions, you need to add it to your machine's configuration.

Go to your machine's **CONFIGURE** page, and add a model that supports your input controller.

The following list shows the available input controller models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:input_controller" type="input_controller" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component compatible with the Micro-RDK.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The [input controller API](/dev/reference/apis/components/input-controller/) supports the following methods:

{{< readfile "/static/include/components/apis/generated/input_controller-table.md" >}}

## Troubleshooting

If your input controller is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
1. Review your input controller model's documentation to ensure you have configured all required attributes.
1. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the input controller there.
1. Disconnect and reconnect your input controller.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

For general configuration, development, and usage info, see:

{{< cards >}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{% card link="/tutorials/control/gamepad/" noimage="true" %}}
{{< /cards >}}
