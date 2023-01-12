---
title: "Use SDKs to extend Viam"
linkTitle: "Custom Resources with SDKs"
weight: 99
type: "docs"
tags: ["server", "sdk"]
---

Viam's Robot Development Kit ([RDK](/product-overviews/rdk/)) provides a variety of components and services out of the box.
If the components you are working with are not supported, you can use Viam [modular resources](/product-overviews/modular-resources) to add support for custom resources which form a seamless extension of the Viam platform.

Currently, [modular resource](/product-overviews/modular-resources) development is supported only with the [RDK (Golang SDK)](https://pkg.go.dev/go.viam.com/rdk).
However, you can leverage any Viam [SDK](product-overviews/sdk-as-client/) to create a custom component implementation by using an SDK as a server.

## What is a server component implementation?

The Viam server component implementation allows you to create custom components that interface with the `viam-server` using Viam's SDKs.
A server component is a subclass of a [component](https://python.viam.dev/autoapi/viam/components/component_base/index.html#module-viam.components.component_base) that allows you to register the new component with the `viam-server` as a [*remote*](/appendix/glossary/#remote_anchor) after you spin up an SDK server (which can have one or many custom components).

In other words, a server component implementation is a way for you to connect to, control, and monitor any unsupported robots, sensors, or components using any of Viam's clients, including our SDKs and the Viam app.

## Why use the SDK to create a custom server component implementation?

While the main Viam RDK is written in Golang, you can create custom components using the Viam SDKs (like Python) and connect them to a robot as a remote component.
This allows you to extend the functionality of a robot, or even create an entire robot exclusively.
Once you have created and registered your server component with the `viam-server`, you will be able to control and monitor your from the Viam SDK and from the [Viam app](https://app.viam.com/).

For example, let's say that you have built a custom robotic arm that is not supported by [Viam's arm component from our SDK](https://python.viam.dev/autoapi/viam/components/arm/index.html#module-viam.components.arm), and you want to integrate it with Viam.
You will need to create a server component and register the new arm in order to use it with the Viam SDK.
Once your new arm is registered, you will be able to use it remotely with Viam.

{{% alert title="Tip" color="tip" %}}  
Here is an example of [how to create a new arm server component in the Python SDK documentation](https://python.viam.dev/examples/example.html#subclass-a-component).
{{% /alert %}}

## What is required to create a custom component?

The steps required in creating a custom component and connecting it to the RDK are

1. Subclass a component and implement desired functions

2. Create an `rpc.server.Server` instance and register the custom component

3. Start the Server and register the running server as a remote

You can view the complete tutorial on how to create a custom component in Python in the [Viam Python documentation](https://python.viam.dev/examples/example.html#create-custom-components).

You can view more component implementation examples in <file>components.py</file>, found in the <a href="https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/server/v1/components.py" target="_blank">Viam Python SDK repo</a>[^compsamp].

[^compsamp]:<file>components.py</file>: <a href="https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/server/v1/components.py" target="_blank">ht<span></span>tps://github.com/viamrobotics/viam-python-sdk/blob/main/examples/server/v1/components.py</a>
