---
title: "Creating custom components and services as modular resources"
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

### APIs

All Viam component and service types expose their own *API*.
This API describes the interface that the particular component or service type exposes.
For example, the API of built-in component type [camera](/components/camera) exposes the *GetImage* method, while the API of built-in service type [vision](/services/vision) exposes the *GetDetectionsFromCamera* method.

Each API that corresponds with a Viam resource is described and exposed via [protocol buffers](https://developers.google.com/protocol-buffers).
Built-in Viam resource APIs can be seen in the [Viam API github repository](https://github.com/viamrobotics/api).

Viam APIs are uniquely namespaced, which is represented as a *colon-delimited-triplet*.  
For example, the built-in component type *camera*'s namespace is __rdk:component:camera__.
The built-in service type *vision*'s namespace is __rdk:service:vision__

Viam API interfaces are made available in various programming languages via [Viam SDKs](/product-overviews/sdk-as-client/) and allow you to control your robots [securely from anywhere](deeper-dive/robot-to-robot-comms/).

### Models

A model is an implementation of a given given resource type.  A model may implement all or some of the API methods provided by a given resource type API.
Models allow any number of versions of a given resource to be controlled with a consistent interface.

This is powerful, as normally a software engineer may need to learn and code against multiple interfaces for different models of the same component type.

For example, some DC motors can be controlled via GPIO and PWM, which can be interfaced with in different ways depending on the controlling hardware they are attached to.
Other DC motors are controlled via various serial protocols.
This simplified with Viam, as any motor model that implements the *rdk:component:motor* API can be powered with the *SetPower* method.

Models in Viam are represented by their own *colon-delimited-triplet*.
For example, RDK support for GPIO-powered motors is provided by the __rdk:builtin:gpio__ model of the __rdk:component:motor__ API, while DMC 4000 motor support is provided by the __rdk:builtin:DMC4000__ model of the same __rdk:component:motor__ API.

A common use-case for modular resources is to create a new model of an existing Viam API.  However, new API types can also be created and exposed via modular resources.

## Modular resource management by RDK

### Dependency Management

The Viam RDK handles dependency management, and modular resources may depend on other built-in resources or other modular resources, and vice versa.

### Startup

RDK ensures that any configured custom resources are started alongside configured-built in resources.
This includes ensuring that any custom APIs and models are registered.
Once all modules are registered and started, normal robot loading continues.

### Reconfiguration

When a Viam robot is reconfigured (meaning, its configuration is modified), the behavior of modular resources vs built-in resources should be equivalent to the end-user.
Therefore, modular resource instances can be added, modified, and removed from a running robot as normal.

### Shutdown

During robot shutdown, modular resources are handled similarly to built-in resources, in that they are signaled for shutdown in topological (dependency) order.

## Building a modular resource

Detailed, working examples of various types of modular resources are [included with RDK](https://github.com/viamrobotics/rdk/tree/main/examples/customresources).

The easiest way to get started is to:

1. Try configuring one of these examples with a Viam robot config (see [Using a modular resource with your robot](#using-a-modular-resource-with-your-robot))
2. Interface with the custom resource via the Viam app's [control page](/getting-started/app-usage/#control)
3. Interface with the custom resource via a [Viam SDK](/product-overviews/sdk-as-client/)
4. Experiment by changing its behavior.

## Using a modular resource with your robot

Adding a modular resource to your robot configuration requires two steps:

1. Add a *module* to your configuration
2. Add a *component* or *service* that references the configured module

### Adding a module to your robot configuration

Modular resources introduce a new top-level configuration block to robot configuration called *modules*.
This allows any modular resources you'd like to use with your robot to be registered and [managed](#modular-resource-management-by-rdk) by RDK.
Modules are loaded in the order they are specified in the modules list.

#### Required attributes - module

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
`name` | string | --        | Name of the module you are registering
`executable_path` | string | --         | The filesystem path to the module executable on the robot part

### Configuring a component instance for a modular resource

Once a module is configured as part of your robot configuration, you can then instantiate any number of instances of that resource via component or service configuration.
For modules, all standard properties such as *attributes* and *depends_on* are supported for modular resources.
In order to correctly reference a registered modular resource, the *namespace*, *type*, *name* and *model* properties must be configured.

#### Required attributes - modular component

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
`namespace` | string | --        | The namespace of the [API](#apis), i.e. the first part of the [API](#apis) triplet
`type` | string | --         | The type of the [API](#apis), i.e. the second part of the [API](#apis) triplet
`name` | string | --         | The name of the [API](#apis), i.e. the third part of the [API](#apis) triplet
`model` | string | --         | The full triplet of the [model](#models) of the modular resource

## Configuration example - custom motor

The following example configuration illustrates how one might configure a robot that uses a custom motor implementation.
This example motor implementation uses the standard (built-in) Viam motor API, but creates a custom model __viam-contributor:motor:super-custom__

``` json
{
  "modules": [
    {
      "name": "my-motor",
      "executable_path": "/home/me/super-custom-motor/run.sh"
    }
  ],
    "components": [
        {
        "type": "component",
        "name": "motor",
        "model": "viam-contributor:motor:super-custom",
        "namespace": "rdk",
        "attributes": {},
        "depends_on": []
        }
    ]
}
```

## Including modular resources as a remote

Modular resources can be included as a [remote](/getting-started/high-level-overview/#remote) part of any configured Viam robot.
This means that a robot can be composed of any number of parts running in different compute locations, each containing both built-in and custom resources.

## Limitations

Currently, modular resources are supported only via the Viam [Go SDK](https://pkg.go.dev/go.viam.com/rdk).
We're working to add support to all of our SDKs, but in the meantime you can add custom components by using the Viam SDK of your choice to [create a server component implementation](/product-overviews/extending-viam/sdk-as-server/).

Custom models of the [arm](/components/arm) component type are not yet supported (as kinematic information is not currently exposed via the arm API), but support will be added soon.
