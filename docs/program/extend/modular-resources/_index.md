---
title: "Create custom components and services as modular resources"
linkTitle: "Modular Resources"
description: "Use the Viam module system to implement custom resources that can be included in any Viam-powered robot."
image: "/tutorials/img/intermode/rover_outside.png"
weight: 10
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
---

The Viam module system allows you to integrate custom [resources](/appendix/glossary/#term-resource) ([components](/components) and [services](/services)) into any robot running on Viam.

<!-- ## Modular Resources

You can use the Viam module system to build a custom [component](/components) or [service](/services), which can then be included in any Viam-powered robot.
Once configured, modular resources behave identically to built-in RDK resources.

The Viam platform manages:

- Starting and stopping the module binary (lifecycle)
- Dependency management (modular resources may depend on other resources - both RDK built-in and other modular resources)
- Securely exposing the modular resource's interface (protobuf-described API) alongside Viam RDK built-in APIs
- Robot reconfiguration for any configured modular resource instances

For more detail, see [Modular Resources](/program/extend/modular-resources/).

## Custom Components as Remotes

You can also implement custom components by programming custom components with the SDK of your choice, registering them on a server, adding the server as a remote part of your robot, and adding a process to your robot that runs the server.

For more detail, see [Custom Components as Remotes](/program/extend/sdk-as-server/). -->

With modular resources, you can:

- Create new models of built-in component or service types
- Create brand new resource types

`viam-server` treats modular resources configured on your robot like resources that are already built-in to the [Robot Development Kit (RDK)](/program/rdk).
This means that functionality that the [RDK](/program/rdk/) provides for built-in resources is also automatically provided for user-created modular resources.
Two key concepts exist across all Viam resources, built-in and modular, to facilitate this: [*APIs*](#apis) and [*models*](#models).

## Key Concepts

### APIs

Every Viam [resource](/appendix/glossary/#term-resource) exposes an [Application Programming Interface (API)](https://www.ibm.com/topics/api).
This API describes the interface for the particular component or service type.
Viam APIs are uniquely namespaced, with each resource type represented as a *colon-delimited-triplet*.
For example:

- The API of built-in component type [camera](/components/camera) is __rdk:component:camera__, and exposes methods such as `GetImage()`.
- The API of built-in service type [vision](/services/vision) is __rdk:service:vision__, and exposes methods such as `GetDetectionsFromCamera()`.

Each API is described through <a href="https://developers.google.com/protocol-buffers" target="_blank">protocol buffers</a>.
Viam SDKs [expose these APIs](/internals/robot-to-robot-comms/).

{{% alert title="Note" color="note" %}}
You can see built-in Viam resource APIs in the <a href="https://github.com/viamrobotics/api" target="_blank">Viam GitHub</a>.
{{% /alert %}}

### Models

A model is an implementation of a resource type that implements all or some of the API methods of a resource type's API.

Models allow you to control any number of versions of a given resource with a consistent interface.
This is powerful, because you have all the same methods for interfacing with different models of the same component type.

For example, some DC motors can be controlled with GPIO, which you can interface with in different ways depending on the attached controlling hardware.
Other DC motors are controlled with various serial protocols.
This is simplified with Viam, as any motor model that implements the *rdk:component:motor* API can be powered with the `SetPower()` method.

Models are also represented by *colon-delimited-triplets*.
For example:

- The __rdk:builtin:gpio__ model of the __rdk:component:motor__ API provides RDK support for [GPIO-controlled DC motors](/components/motor/gpio/).
- The __rdk:builtin:DMC4000__ model of the same __rdk:component:motor__ API provides RDK support for the [DMC4000](/components/motor/dmc4000/) motor.

A common use-case for modular resources is to create a new model using an existing Viam API.
However, you can also create and expose new API types using modular resources.

## Use a Modular Resource with Your Robot

Add a modular resource to your robot configuration in five steps:

1. Code a module in Go or Python that implements a new resource and registers the component in the Viam RDK's [global registry of robotic parts](https://github.com/viamrobotics/rdk/blob/main/registry/registry.go).
2. Create a binary executable file that runs your module.
3. Save the module binary in a location where it can be accessed by the RDK.
4. Add a *module*, which is built from the module binary, to the configuration of your robot.
5. Add a new component or service referencing the custom resource provided by the configured *module* to the configuration of your robot.

<!-- 3. Ensure that the module binary can be accessed by the RDK (see [Make the modular resource available to RDK](#make-the-modular-resource-available-to-rdk))
4. Add a *module* to your robot configuration
5. Add a *component* or *service* that references a component or service resource provided by the configured module -->

### Code Your Module

### Create Your Executable Module Binary

### Make Your Module Binary Available to the RDK

In order for the RDK to manage a modular resource, the modular resource must be exposed by a module that is able to be run by the RDK.
Therefore, you must ensure that any modular resource is made available with a module binary executable in a location that the RDK can access.
For example, if you are running the RDK on an Raspberry Pi you'll need to have an executable module on the Pi's filesystem.

{{% alert title="Modules vs modular resources" color="tip" %}}
Modules are binary executables that can be managed by the RDK through [module configuration](#add-a-module-to-your-robot-configuration).

A configured module can make one or more modular resources available for configuration as a component and/or service instances.
{{% /alert %}}

### Configure Your Module

The Viam module system introduces a new optional top-level configuration block to robot configurations called *modules*.
This allows you to instruct RDK to load modules as well as register and [manage](#modular-resource-management-with-the-rdk) any modular resources made available by the module that you'd like to use with your robot.
The RDK loads modules in the order you specify in the modules list.

The following properties are available for modules:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
`name` | string | **Required** | Name of the module you are registering |
`executable_path` | string | **Required** | The filesystem path to the module executable on the robot part |

### Configure Your Modular Resource

Once you have configured a module as part of your robot configuration, you can instantiate any number of instances of a modular resource made available by that module with the component or service configuration.
All standard properties such as *attributes* and *depends_on* are supported for modular resources.

To correctly reference a registered modular resource, you must configure the *namespace*, *type*, *name* and *model* properties:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `namespace` | string | **Required** | The namespace of the [API](#apis) (the first part of the [API](#apis) triplet) |
| `type` | string | **Required** | The subtype of the [API](#apis) (the third part of the [API](#apis) triplet) |
| `name` | string | **Required** | What you want to name this instance of your modular resource. |
| `model` | string | **Required** | The [full triplet](#models) of the modular resource |

The following is an example configuration for a motor modular resource implementation.
It registers a custom model __viam-contributor:motor:super-custom__ to use with the Viam [motor API](/components/motor#api):

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

## More Information

### Modular Resource Management

#### Dependency Management

Modular resources may depend on other built-in resources or other modular resources, and vice versa.
The Viam RDK handles dependency management.

#### Startup

RDK ensures that any configured modules are loaded automatically on startup, and that configured modular resource instances are started alongside configured built-in resources instances.

#### Reconfiguration

When you change the configuration of a Viam robot, the behavior of modular resource instances versus built-in resource instances is equivalent.
This means you can add, modify, and remove a modular resource instance from a running robot as normal.

#### Shutdown

During robot shutdown, the RDK handles modular resource instances similarly to built-in resource instances - it signals them for shutdown in topological (dependency) order.

### Modular Resources as Remotes

[Remote](/manage/parts-and-remotes/) parts may load their own modules and provide modular resources, just as the main part can.
This means that you can compose a robot of any number of parts running in different compute locations, each containing both built-in and custom resources.

### Limitations

Custom models of the [arm](/components/arm) component type are not yet supported, as kinematic information is not currently exposed through the arm API.
Support will be added soon.
