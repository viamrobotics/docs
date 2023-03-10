---
title: "Use SDKs to extend Viam"
linkTitle: "Custom Resources with SDKs"
weight: 99
type: "docs"
tags: ["server", "sdk"]
---

Viam's Robot Development Kit ([RDK](/program/rdk/)) provides a variety of components and services out of the box.
If the components you are working with are not supported, you can use Viam [modular resources](/program/extend/) to add support for custom resources which form a seamless extension of the Viam platform.

Currently, [modular resource](/program/extend/) development is supported only with the [RDK (Go SDK)](https://pkg.go.dev/go.viam.com/rdk).
However, you can leverage any Viam [SDK](/program/extend/sdk-as-server) to create a custom component implementation by using an SDK as a server.

## What is a custom component implementation?

Implementing a custom component allows you to create a new component type (or a new model of an existing type, such as a new `arm` model) that interfaces with `viam-server` using Viam's SDKs.
A custom component is a subclass of a [component](https://python.viam.dev/autoapi/viam/components/component_base/index.html#module-viam.components.component_base) that allows you to register the new component with the `viam-server` as a [*remote*](/appendix/glossary/#remote_anchor) after you spin up an SDK server (which can have one or many custom components).

In other words, a custom component implementation is a way for you to integrate unsupported components into a robot running on the Viam platform.

## Why use the SDK to create a custom component implementation?

While the main Viam RDK is written in Go, you can create custom components using the Viam SDKs (like Python) and connect them to a robot as a remote component.
This allows you to use hardware that is not natively supported by Viam, without having to use Go if you prefer not to.
Once you have created and registered your custom component with `viam-server`, you will be able to control and monitor your component from the Viam SDK and from the [Viam app](https://app.viam.com/).

## What is required to create a custom component?

For example, let's say that you have a robotic arm that is not one of the models supported by [Viam's arm component](/components/arm/), and you want to integrate it with Viam.
You will need to create a custom component and register the new arm model in order to use it with the Viam SDK.
Once your new arm is registered, you will be able to use it remotely with Viam.

{{% alert title="Tip" color="tip" %}}
Here is an example of [how to create a custom arm component in the Python SDK documentation](https://python.viam.dev/examples/example.html#subclass-a-component).
{{% /alert %}}

To create a custom component and connect it to the RDK:

1. Subclass a component and implement desired functions
    - If you are using the Python SDK, you must define all functions.
      For functions you do not want to implement, put `pass` or `raise NotImplementedError()` in the function.
    Otherwise, the class won't instantiate.
    - If you are using the Go SDK, you must define all functions but you can leave the ones you do not wish to implement empty.
2. Create an `rpc.server.Server` instance and register the custom component.
3. Start the server and register the running server as a remote.

You can view the complete tutorial on how to create a custom component using Python in the [Viam Python documentation](https://python.viam.dev/examples/example.html#create-custom-components).

Find more component implementation examples in [<file>components.py</file> in the Viam Python SDK repo](https://github.com/viamrobotics/viam-python-sdk/blob/main/examples/server/v1/components.py).

For a full walk-through of a different example, see the [Custom Quadruped Base tutorial](/tutorials/custom-base-dog/).
