---
title: "Extend Viam with custom components and services"
linkTitle: "Extending Viam"
weight: 60
simple_list: true
type: docs
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Using modular resources and SDKs to extend Viam"
---


Viam's [Robot Development Kit (RDK)](/product-overviews/rdk/) provides support for a variety of resources:

- Standard hardware [components](/components) and component models.
- High-level functionality exposed as [services](/services).

Many robots can be composed of these resources out-of-the-box.
However, sometimes you may encounter a hardware component that is not natively supported by Viam's RDK.
In other cases, you may want to add new functionality to a component or expose a custom service securely through the Viam API and corresponding SDKs.

Viam can be extended in these and other ways with the creation and usage of custom resources.

## Modular resources

The Viam module system allows a user to build a custom [component](/components) or [service](/services) that can be seamlessly included into any Viam-powered robot.
Once configured, modular resources behave identically to built-in resources.

The Viam platform manages:

- Starting and stopping the resource binary (lifecycle)
- Dependency management (modular resources may depend on other resources - both RDK built-in and other modular resources)
- Securely exposing the modular resource's interface (protobuf-described API) alongside Viam RDK built-in APIs
- Robot reconfiguration for any configured modular resource instances

For more detail, see the [modular resources documentation](/product-overviews/extending-viam/modular-resources/).

## Using a Viam SDK as a server to create a custom component

Currently, modular resources are supported only with the Viam [Go SDK](https://pkg.go.dev/go.viam.com/rdk).
If you are not using the Go SDK, you can add custom components using the Viam [SDKs](product-overviews/sdk-as-client/) of your choice to create a [server component implementation](/product-overviews/extending-viam/sdk-as-server/).

## See Also
