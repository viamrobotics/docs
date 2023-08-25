---
title: "Key Concepts of Modular Resource APIs"
linkTitle: "Concepts"
weight: 10
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "The key concepts behind how Viam's resource APIs and models are uniquely namespaced and modular resource management with the RDK."
no_list: true
---

`viam-server` [manages](#management) modular {{< glossary_tooltip term_id="resource" text="resources" >}} configured on your robot the same way it manages resources that are already built into the Robot Development Kit [(RDK)](/internals/rdk/).
Two key concepts exist across all Viam resources, both built-in and modular, that make this flexible management possible: uniquely namespaced resource [*APIs*](#apis) and [*models*](#models).

If you create your [own module](/extend/modular-resources/create/), you must register any new APIs and models you define in your model with Viam's model registry in the appropriate namespaces to [configure](/extend/modular-resources/configure/) the modular resource on your robot.

## APIs

{{% alert title="Modules vs. modular resources" color="tip" %}}

A configured *module* can make one or more *modular resources* available for configuration.

{{% /alert %}}

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} subtype exposes an [application programming interface (API)](https://en.wikipedia.org/wiki/API).
This can be understood as a description of how you can interact with that resource.
Each API is described through [protocol buffers](https://developers.google.com/protocol-buffers).
Viam SDKs [expose these APIs](/internals/robot-to-robot-comms/).

### Namespace

Each Viam resource's API is uniquely namespaced as a colon-delimited-triplet in the form of `namespace:type:subtype`.

For example:

- The API of built-in component [camera](/components/camera/) is `rdk:component:camera`, which exposes methods such as `GetImage()`.
- The API of built-in service [vision](/services/vision/) is `rdk:service:vision`, which exposes methods such as `GetDetectionsFromCamera()`.

{{% alert title="Tip" color="tip" %}}
You can see built-in Viam resource APIs in the [Viam GitHub](https://github.com/viamrobotics/api).
{{% /alert %}}

## Models

A *model* describes a specific implementation of a resource that implements (speaks) its API.
Models allow you to control different instances of resource {{< glossary_tooltip term_id="api-namespace-triplet" text="subtypes" >}} with a consistent interface.

For example:

Some DC motors use just [GPIO](/components/board/), while other DC motors use serial protocols like [SPI bus](/components/board/#spis).
Regardless, you can power any motor model that implements the `rdk:component:motor` API with the `SetPower()` method.

### Namespace

Models are uniquely namespaced as colon-delimited-triplets in the form of `namespace:family:name`.

For example:

- The `rdk:builtin:gpio` model of the `rdk:component:motor` API provides RDK support for [GPIO-controlled DC motors](/components/motor/gpio/).
- The `rdk:builtin:DMC4000` model of the same `rdk:component:motor` API provides RDK support for the [DMC4000](/components/motor/dmc4000/) motor.

{{% alert title="Important" color="note" %}}
If you are creating a custom module and uploading that module to the Viam Registry, the namespace of your model **must** match the namespace of your organization.
{{% /alert %}}

## Management

The Robot Development Kit (RDK) `viam-server` provides automatically manages modular resources to function like built-in resources:

### Dependency Management

Modular resources may depend on other built-in resources or other modular resources, and vice versa.
The Viam RDK handles dependency management.

### Start-up

The RDK ensures that any configured modules are loaded automatically on start-up, and that configured modular resource instances are started alongside configured built-in resource instances.

### Reconfiguration

When you change the configuration of a Viam robot, the behavior of modular resource instances versus built-in resource instances is equivalent.
This means you can add, modify, and remove a modular resource instance from a running robot as normal.

### Data management

Data capture for individual components is supported on [certain component subtypes](/services/data/configure-data-capture/#configure-data-capture-for-individual-components).
If your modular resource is a model of one of these subtypes, you can configure data capture on it just as you would on a built-in resource.

### Shutdown

During robot shutdown, the RDK handles modular resource instances similarly to built-in resource instances - it signals them for shutdown in topological (dependency) order.

### Modular resources as remotes

[Remote](/manage/parts-and-remotes/) parts may load their own modules and provide modular resources, just as the main part can.
This means that you can compose a robot of any number of parts running in different compute locations, each containing both built-in and custom resources.
