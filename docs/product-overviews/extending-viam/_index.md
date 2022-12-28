---
title: "Extending Viam with custom components and services"
linkTitle: "Extending Viam"
weight: 20
simple_list: true
type: docs
description: "Using modular resources, SDKs, and remotes to extend Viam"
---


Viam's [Robot Development Kit (RDK)](/product-overviews/rdk/) provides support for a variety of resources:
- Standard hardware [components](/components) and component models.
- High-level functionality exposed as [services](/services).

Many robots can be composed of these resources out-of-the-box.

However, sometimes you may encounter a hardware component that is not natively supported by Viam's SDK.
In other cases, you may want to add new functionality to a component or expose a custom service securely through the Viam API and corresponding SDKs.

Here, we'll walk you through how extend Viam in these and other ways via the creation and usage of custom resources.

## Modular resources

TODO: Update language in this section

The module system allows a user to build an external binary, either in Golang, using this package and any others from the RDK ecosystem,
or in any other language, provided it can properly support protobuf/grpc. 
The path to the binary (the module) and a name for it must
be given in the Modules section of the robot config. 
The normal viam-server (rdk) process will then start this binary, and query it via
GRPC for what protocols (protobuf described APIs) and models it supports. 
Then, any components or services that match will be handled
seamlessly by the module, including reconfiguration, shutdown, and dependency management. 
Modular components may depend on others from
either the parent (aka built-in resources) or other modules, and vice versa.
Modular resources should behave identically to built-in
resources from a user perspective.


## Using modular resources as a remote

TODO: Explain (with examples) when you may want to run a modular resource as a remote.

## Using a Viam SDK as a server to create a custom component

Currently, modular resources are supported only via the Viam [Go SDK](https://pkg.go.dev/go.viam.com/rdk).
We're working to add support to all of our SDKs, but in the meantime you can add custom components by using the Viam SDK of your choice to create a server component implementation.

This method is covered in detail [here](/product-overviews/extending-viam/sdk-as-server/)


## See Also