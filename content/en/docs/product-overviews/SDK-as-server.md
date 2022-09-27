---
title: "Using Our SDKs for a Server Component Implementation"
linkTitle: "SDKs as Server"
weight: 99
type: "docs"
description: "An introduction to Viam's SDKs and how to use them to drive hardware not natively supported in the RDK."
---

Viam's Software Development Kits (SDKs) provide a wide array of components to customize. (You can browse through the [^API Reference][API Reference](https://python.viam.dev/autoapi/viam/components/index.html) to see all of them.) But if you want to use a component that is not natively supported by Viam's SDK, then you will need to create a server component implementation in order to use your custom component.

## What is a server component implementation?

The Viam server component implementation allows you to create custom components that interface with the `viam-server` using Viam's SDKs. A server component is a subclass of a [component](https://python.viam.dev/autoapi/viam/components/component_base/index.html?highlight=component#module-viam.components.component_base), that allows you to register the new component with the `viam-server` as a remote after you spin up an SDK server (which can have one or many custom components).

In other words, a server component is a way for you to connect to, control, and monitor any unsupported robots, sensors, or components using any of Viam's clients, including our SDKs and the Viam App.

## Why use the SDK to create a custom server component implementation?

While the main Viam RDK is written in Golang, you can create custom components using the Viam SDKs (like Python) and connect them to a robot as a `remote` component. This allows you to extend the functionality of a robot, or even create an entire robot exclusively. Once you have created and registered your server component with the `viam-server`, you will be able to control and monitor your from the Viam SDK and from the [Viam App](https://app.viam.com/).

For example, let's say that you have built a custom robotic arm that is not supported by [Viam's arm component from our SDK](https://python.viam.dev/autoapi/viam/components/arm/index.html?highlight=arm#module-viam.components.arm), and you want to integrate it with Viam. You will need to create a server component and register the new arm in order to use it with the Viam SDK. Once your new arm is registered, you will be able to use it remotely with Viam.

!!! tip
    Here is an example of [how to create a new arm server component in the Python SDK documentation](https://python.viam.dev/autoapi/viam/components/arm/index.html?highlight=arm#module-viam.components.arm).

## What is required to create a custom component?

The steps required in creating a custom component and connecting it to the RDK are

1.  Subclass a component and implement desired functions

2.  Create an `rpc.server.Server` instance and register the custom component

3.  Start the Server and register the running server as a remote

You can view the complete tutorial on how to create a custom component in Python in the [Viam Python documentation](https://python.viam.dev/examples/example.html#create-custom-components).

You can view more component implementation examples in the [Viam Python SDK repo](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/server/v1/components.py).

[You can find the API reference here.](https://python.viam.dev/autoapi/viam/components/index.html)
