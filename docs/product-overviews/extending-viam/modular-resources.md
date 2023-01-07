---
title: "Building custom components and services as modular resources"
linkTitle: "Modular Resources"
weight: 99
type: "docs"
description: "How modular resources can be used to extend RDK functionality."
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
---

The Viam module system allows a user to build a custom [component](/components) or [service](/services) that can be seamlessly included into any Viam-powered robot.

Note: Viam components and services are collectively referred to as *resources*

## Viam resource basics

Modular resources can be used to create new versions (models) of existing (RDK built-in) component or service types.  They can also be used to create brand new resource types.  

Modular resources that are configured and composed into a Viam robot behave identically to built-in resources from a user perspective.
This means that functionality that is provided by the Viam [RDK](/product-overviews/rdk/) for built-in resources is automatically provided for user-created resources, as well.

Two key concepts exist to facilitate this: *APIs* and *models*

### APIs ###
All Viam component and service types expose their own *API*.
This API describes the interface that the particular component or service type exposes.
For example, the API of built-in component type [camera](/components/camera) exposes the *GetImage* method, while the API of built-in service type [vision](/services/vision) exposes the *GetDetectionsFromCamera* method.

Each API that corresponds with a Viam resource is described and exposed via [protocol buffers](https://developers.google.com/protocol-buffers).
Built-in Viam resource APIs can be seen in the [Viam API github repository](https://github.com/viamrobotics/api).

Viam APIs are uniquely namespaced, which is represented as a *colon-delimited-triplet*.  
For example, the built-in component type *camera*'s namespace is __rdk:component:camera__.
The built-in service type *vision*'s namespace is __rdk:service:vision__

Viam API interfaces are made available in various programming languages via [Viam SDKs](/product-overviews/sdk-as-client/) and allow you to control your robots [securely from anywhere](deeper-dive/robot-to-robot-comms/).

### Models ###

A model is an implementation of a given given resource type.  A model may implement all or some of the API methods provided by a given resource type API.
Models allow any number of versions of a given resource to be controlled with a consistent interface.

This is powerful, as normally a software engineer may need to learn and code against multiple interfaces for different models of the same component type.

For example, some DC motors can be controlled via GPIO and PWM, which can be interfaced with in different ways depending on the controlling hardware they are attached to.  
Other DC motors are controlled via various serial protocols.
This simplified with Viam, as any motor model that implements the *rdk:component:motor* API can be powered with the *SetPower* method.

Models in Viam are represented by their own *colon-delimited-triplet*. 
For example, RDK support for GPIO-powered motors is provided by the __rdk:builtin:gpio__ model of the API __rdk:component:motor__, while DMC 4000 motor support is provided by the __rdk:builtin:DMC4000__ model of the same __rdk:component:motor__ API.

A common use-case for modular resources is to create a new model of an existing Viam API.  However, new API types can also be created and exposed via modular resources.

## Modular resource management by RDK

### Dependency Management

### Startup

RDK ensures that any configured custom resources are started alongside configured-built in resources.  This includes ensuring that any models and subtypes are registered.The module manager (modmanager) integrates with the robot and resource manager. During startup, a dedicated GRPC module service is started,
listening on a unix socket in a temporary directory (ex: /tmp/viam-modules-893893/parent.sock) and then individual modules are executed.
These are each passed dedicated socket address of their own in the same directory, and based on the module name.
(ex: /tmp/viam-modules-893893/acme.sock) The parent then queries this address with Ready() and waits for confirmation. The ready response
also includes a HandlerMap that defines which protocols and models the module provides support for. The parent then registers these
subtypes and models, with creator functions that call the manager's AddResource() method. Once all modules are started, normal robot
loading continues.

### Reconfiguration

### Shutdown

## Building a modular resource

Detailed, working examples of various types of modular resources are [included with RDK](https://github.com/viamrobotics/rdk/tree/main/examples/customresources).

The easiest way to get started is to:
1. Try configuring one of these examples with a Viam robot (see [Using a modular resource with your robot](#using-a-modular-resource-with-your-robot))
2. Interface with the custom resource via the Viam app's [control page](/getting-started/app-usage/#control)
3. Interface with the custom resource via a [Viam SDK](/product-overviews/sdk-as-client/)
4. Experiment by changing its behavior.

## Using a modular resource with your robot

### Including modular resources as a remote

Modular resources can be included as a [remote](/getting-started/high-level-overview/#remote) part of any configured Viam robot.
This means that a robot can be composed of any number of parts running in different compute locations, each containing both built-in and custom resources.

## Limitations

Currently, modular resources are supported only via the Viam [Go SDK](https://pkg.go.dev/go.viam.com/rdk).
We're working to add support to all of our SDKs, but in the meantime you can add custom components by using the Viam SDK of your choice to [create a server component implementation](/product-overviews/extending-viam/sdk-as-server/).

Custom models of the [arm](/components/arm) component type are not yet supported (as kinematic information is not currently exposed via the arm API), but support will be added soon.
