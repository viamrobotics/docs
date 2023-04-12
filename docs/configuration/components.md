---
title: "Components"
linkTitle: "Components"
weight: 10
type: "docs"
no_list: true
description: "Components are the hardware of your robot."
tags: ["manage", "components"]
---

Components represent the pieces of hardware on your robot that you want to control with Viam.

You must configure each component with a name, a model, a type, attributes, and dependencies:

- `name`: Serves as an identifier when accessing the resource from your code, as well as when configuring other resources that are dependent on that resource.
You can choose any unique name for a component.

- `type`: The broad component category, such as `motor`, `arm` or `camera`.
  Components of a given type have a common API.

- `model`: Indicates the more specific category of hardware.
Components of the same model are supported using the same low-level code.

- `attributes`: A struct to define things like how the component is wired to the robot, its dimensions, and other specifications; attributes vary widely between models.
  See the [component documentation](/components/) for a given component type and model for more details.

- `depends_on`: Any components that a given component relies upon, and that must be initialized on boot before this component is initialized.
  Many built-in components have convenient implicit dependencies, in which case `depends_on` can be left blank.
  For example, a [`gpio` motor](/components/motor/gpio/) depends on the `board` to which it is wired, but it has a dedicated `board` attribute and `viam-server` will automatically initialize that board before it looks for the motor.

Find specific information on how to configure each supported component type in its respective [documentation](/components/).

{{% alert title="Tip" color="tip" %}}

When you configure a component on the **CONFIG** tab, it will also appear on the **CONTROL** tab which gives you an interface to test and interact with it.
Meanwhile the **CODE SAMPLE** tab will also update to include code for some basic interaction with that component using the Viam [SDKs](/program/sdk-as-client/).

{{% /alert %}}
