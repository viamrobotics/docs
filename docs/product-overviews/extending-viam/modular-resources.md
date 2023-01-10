---
title: "Create custom components and services as modular resources"
linkTitle: "Modular Resources"
weight: 10
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
---

The Viam module system allows you to integrate custom resources ([components](/components) and [services](/services)) into any robot running on Viam.
Once configured, custom resources behave the same as built-in RDK resources.

## Viam resource basics

With modular resources you can:

- Create new models of existing (RDK built-in) component or service types
- Create brand new resource types

Modular resources that are configured and composed into a Viam robot behave identically to built-in resources.
This means that functionality that the Viam [RDK](/product-overviews/rdk/) provides for built-in resources is also automatically provided for user-created resources.

Two key concepts exist across all Viam resources (built-in and modular) to facilitate this: *APIs* and *models*

### APIs

Every Viam component and service type exposes an *API*.
This API describes the interface for the particular component or service type.
For example, the API of built-in component type [camera](/components/camera) exposes methods such as *GetImage*, and the API of built-in service type [vision](/services/vision) exposes methods such as *GetDetectionsFromCamera*.

Each API corresponds with a Viam resource and is described through [protocol buffers](https://developers.google.com/protocol-buffers).
You can see built-in Viam resource APIs in the [Viam API GitHub repository](https://github.com/viamrobotics/api).

[Viam SDKs](/product-overviews/sdk-as-client/) that expose these APIs are available in various programming languages and allow you to control your robots [securely from anywhere](deeper-dive/robot-to-robot-comms/).

Viam APIs are uniquely namespaced, with each resource type represented as a *colon-delimited-triplet*.  
For example, the built-in component type *camera*'s namespace is __rdk:component:camera__.
The built-in service type *vision*'s namespace is __rdk:service:vision__

### Models

A model is an implementation of a resource type that implements all or some of the API methods of a resource type API.
Models allow any number of versions of a given resource to be controlled with a consistent interface.
This is powerful, because you only need to learn and code against one interface which remains the same for different models of the same component type.

For example, some DC motors can be controlled with GPIO and PWM, which you can interface with in different ways depending on the attached controlling hardware.
Other DC motors are controlled with various serial protocols.
This is simplified with Viam, as any motor model that implements the *rdk:component:motor* API can be powered with the *SetPower* method.

Viam represents models with *colon-delimited-triplets*.
For example, the __rdk:builtin:gpio__ model of the __rdk:component:motor__ API provides RDK support for GPIO-controlled DC motors and the __rdk:builtin:DMC4000__ model of the same __rdk:component:motor__ API provides support for the DMC 4000 motor.

A common use-case for modular resources is to create a new model of an existing Viam API (resource type).
However, you can also create and expose new API types using modular resources.

## Modular Resource Management with the RDK

### Dependency Management

Modular resources may depend on other built-in resources or other modular resources, and vice versa.
The Viam RDK handles dependency management.

### Startup

RDK ensures that any configured modules are loaded automatically on startup, and that configured modular resource instances are started alongside configured built-in resources instances.

### Reconfiguration

When you reconfigure a Viam robot (meaning, when you change its configuration), the behavior of modular resource instances versus built-in resource instances is equivalent.
This means you can add, modify, and remove a modular resource instance from a running robot as normal.

### Shutdown

During robot shutdown, the RDK handles modular resource instances similarly to built-in resource instances - it signals them for shutdown in topological (dependency) order.

## Modular resources examples

Detailed, working examples of various types of modular resources are [included with the RDK](https://github.com/viamrobotics/rdk/tree/main/examples/customresources).

The easiest way to get started is to:

1. Include one of the provided examples in your Viam robot config (see [Using a modular resource with your robot](#use-a-modular-resource-with-your-robot))
2. Control the custom resource on the Viam app's [__CONTROL__ tab](/getting-started/app-usage/#control)
3. Control the custom resource programmatically with a [Viam SDK](/product-overviews/sdk-as-client/)
4. Experiment by changing the resource's behavior.

## Use a modular resource with your robot

Add a modular resource to your robot configuration in three steps:

1. Ensure that the module binary can be accessed by the RDK (see [Make the modular resource available to RDK](#make-the-modular-resource-available-to-rdk))
2. Add a *module* to your robot configuration
3. Add a *component* or *service* that references a component or service resource provided by the configured module

### Make the modular resource available to RDK

In order for the RDK to manage a modular resource, the modular resource must be exposed by a module that is able to be run by the RDK.
Therefore, you must ensure that any modular resource(s) are made available via a module binary executable in a location that the RDK can access.
For example, if you are running the RDK on an Raspberry Pi you'll need to have an executable module on the Pi's filesystem.


{{% alert title="Modules vs modular resources" color="tip" %}}  
Modules are binary executables that can be managed by RDK through [module configuration](#add-a-module-to-your-robot-configuration).

A configured module can make one or more modular resources available for configuration as component and/or service instances.
{{% /alert %}}

### Add a module to your robot configuration

The Viam module system introduces a new optional top-level configuration block to robot configurations called *modules*.
This allows you to instruct RDK to load modules as well as register and [manage](#modular-resource-management-with-the-rdk) any modular resources made available by the module that you'd like to use with your robot.
The RDK loads modules in the order you specify in the modules list.

#### Required attributes - module

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
`name` | string | --        | Name of the module you are registering
`executable_path` | string | --         | The filesystem path to the module executable on the robot part

### Configure a component instance for a modular resource

Once you have configured a module as part of your robot configuration, you can instantiate any number of instances of a modular resource made availabkle by that module with the component or service configuration.
All standard properties such as *attributes* and *depends_on* are supported for modular resources.
In order to correctly reference a registered modular resource, you must configure the *namespace*, *type*, *name* and *model* properties.

#### Required attributes - modular component

Name | Type | Default Value | Description
-------------- | ---- | ------------- | ---------------
`namespace` | string | --        | The namespace of the [API](#apis) (the first part of the [API](#apis) triplet)
`type` | string | --         | The subtype of the [API](#apis) (the third part of the [API](#apis) triplet)
`name` | string | --         | A unique name for this configured instance of the modular resource
`model` | string | --         | The [full triplet](#models) of the modular resource

## Configuration example - custom motor

The following example configuration illustrates how you can configure a robot that uses a custom motor implementation.
This example motor implementation uses the standard (built-in) Viam motor API, but registers and uses a custom model __viam-contributor:motor:super-custom__

``` json
{
  "modules": [
    {
      "name": "super-motor",
      "executable_path": "/home/me/super-custom-motor/run.sh"
    }
  ],
    "components": [
        {
            "type": "board",
            "name": "main-board",
            "model": "pi"
        },
        {
        "type": "motor",
        "name": "super-motor-1",
        "model": "viam-contributor:motor:super-custom",
        "namespace": "rdk",
        "attributes": {},
        "depends_on": [ "main-board" ]
        }
    ]
}
```

## Modular resources as remotes

[Remote](/getting-started/high-level-overview/#remote) parts may load their own modules and provide modular resources, just as the main part can.
This means that you can compose a robot of any number of parts running in different compute locations, each containing both built-in and custom resources.

## Limitations

Currently, modular resources are supported only with the Viam [Go SDK](https://pkg.go.dev/go.viam.com/rdk).
We're working to add support to all of our SDKs, but in the meantime you can add custom components by using the Viam SDK of your choice to [create a custom component implementation server](/product-overviews/extending-viam/sdk-as-server/).

Custom models of the [arm](/components/arm) component type are not yet supported (as kinematic information is not currently exposed via the arm API), but support will be added soon.
