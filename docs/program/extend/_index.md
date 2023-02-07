---
title: "Extend Viam with custom components and services"
linkTitle: "Extend Viam"
weight: 60
simple_list: true
type: docs
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Using modular resources and SDKs to extend Viam."
---


Viam's [Robot Development Kit (RDK)](/program/rdk/) provides built-in support for a variety of resources:

- Various hardware [components](/components) and component models.
- High-level functionality exposed as [services](/services).

Many robots can be composed entirely of these resources.
However, sometimes you may have a hardware component that Viam's RDK does not natively support.
In other cases, you may want to add new functionality to a component or expose a custom service securely through the Viam API and corresponding SDKs.

You can extend Viam in these and other ways by creating and using custom resources.

## Modular resources

You can use the Viam module system to build a custom [component](/components) or [service](/services).
The new component or service can then be included in any Viam-powered robot.
Once configured, modular resources behave identically to built-in RDK resources.

The Viam platform manages:

- Starting and stopping the module binary (lifecycle)
- Dependency management (modular resources may depend on other resources - both RDK built-in and other modular resources)
- Securely exposing the modular resource's interface (protobuf-described API) alongside Viam RDK built-in APIs
- Robot reconfiguration for any configured modular resource instances

For more detail, see the [modular resources documentation](/program/extend/modular-resources/).

## Use a Viam SDK as a server to create a custom component

Currently, modular resources are supported only with the Viam [Go SDK](https://pkg.go.dev/go.viam.com/rdk).
If you are not using the Go SDK, you can add custom components using the Viam SDK of your choice to create a [server component implementation](/program/extend/sdk-as-server/).

## See also

<div class="container text-center">
  <div class="row">
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="/tutorials/controlling-an-intermode-rover-canbus/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Modular Resource Example</h4>
            <p style="text-align: left;">This tutorial uses modular resources to control a custom base with CAN bus.</p>
        <a>
    </div>
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="/tutorials/custom-base-dog/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Python SDK Custom Resource Example</h4>
            <p style="text-align: left;">This tutorial uses the Viam Python SDK to control a robot dog.</p>
        </a>
    </div>
  </div>
</div>
