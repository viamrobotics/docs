---
title: "Key Concepts of Modular Resource APIs"
linkTitle: "Concepts"
weight: 10
type: "docs"
tags:
  [
    "server",
    "rdk",
    "extending viam",
    "modular resources",
    "components",
    "services",
  ]
description: "The key concepts behind how Viam's resource APIs and models are uniquely namespaced and modular resource management with the RDK."
no_list: true
aliases:
  - "/program/extend/modular-resources/key-concepts/"
---

Viam's [Robot Development Kit (RDK)](/internals/rdk/) provides built-in support for a variety of {{< glossary_tooltip term_id="resource" text="resources" >}}:

- Various types of hardware [components](/components/).
- High-level functionality exposed as [services](/services/).

However, if you want to work with a new hardware component that is not already supported by Viam, or want to introduce a new software service or service model to support additional functionality on your smart machine, you can extend Viam by adding a _modular resource_ to your smart machine.

Modular resources are defined in _modules_, which are easy to create and add to your robot.
A module can provide one or more modular resource models, and can be added to any smart machine running on Viam.

## Modules

A _module_ provides one or more [_modular resources_](#resources), and is a flexible way to extend the functionality of your Viam robot.
Modules run alongside `viam-server` as a separate process, communicating with `viam-server` over a UNIX socket.
A module provides definitions for one or more pairs of [APIs](#valid-apis-to-implement-in-your-model) and [models](#models).

When the module initializes, it registers those pairs on your robot, making the functionality defined by that pair available for use.

## Resources

A resource is a [component](/components/) or [service](/services/).
Each component or service is typed by a proto API, such as the [component proto definitions](https://github.com/viamrobotics/api/tree/main/proto/viam/component).

Any resource on your robot needs to implement either one of the [existing Viam APIs](#valid-apis-to-implement-in-your-model), or a [custom interface](/modular-resources/advanced/#new-api-subtypes).

A _modular resource_ is a resource that is provided by a [module](#modules), and not built into the RDK.
A modular resource runs in the module process.
This differs from built-in resources, which run as part of `viam-server`.

## Models

A _model_ describes a specific implementation of a [resource](#resources) that implements (speaks) its [API](/program/apis/).
Models allow you to control hardware or software of a similar category, such as motors, with a consistent set of methods as an interface, even if the underlying implementation differs.

For example, some DC motors communicate using [GPIO](/components/board/), while other DC motors use serial protocols like the [SPI bus](/components/board/#spis).
Regardless, you can power any motor model that implements the `rdk:component:motor` API with the `SetPower()` method.

Models are uniquely namespaced as colon-delimited-triplets in the form `namespace:family:name`.
See [Naming your model](/modular-resources/key-concepts/#naming-your-model) for more information.

Models are either:

- Built into the RDK, and included when you [install `viam-server`](/installation/) or when you use one of the [Viam SDKs](/program/apis/).
- Provided in [custom modules](#modules) available for download from the [Viam registry](https://app.viam.com/registry), and are written by either Viam or community users.
  Custom modules can also be [local](/modular-resources/configure/#local-modules).

### Built-in models

Viam provides many built-in models that implement API capabilities, each using `rdk` as the `namespace`, and `builtin` as the `family`.
These models run within `viam-server`.

For example:

- The `rdk:builtin:gpio` model of the `rdk:component:motor` API provides RDK support for [GPIO-controlled DC motors](/components/motor/gpio/).
- The `rdk:builtin:DMC4000` model of the same `rdk:component:motor` API provides RDK support for the [DMC4000](/components/motor/dmc4000/) motor.

### Custom models

The [Viam registry](https://app.viam.com/registry) makes available both Viam-provided and community-written modules for download and use on your robot.
You can also run modules [locally](/modular-resources/configure/#local-modules).
These models run outside `viam-server` as a separate process.

#### Valid APIs to implement in your model

When implementing a custom [model](#models) of an existing [component](/components/), valid [APIs](/program/apis/) always have the following parameters:

- `namespace`: `rdk`
- `type`: `component`
- `subtype`: any one of [these component proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/component), for example `motor`

When implementing a custom [model](#models) of an existing [service](/services/), valid [APIs](/program/apis/) always have the following parameters:

- `namespace`: `rdk`
- `type`: `service`
- `subtype`: any one of [these service proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/service), for example `navigation`

#### Naming your model

If you are [creating a custom module](/modular-resources/create/) and [uploading that module](/modular-resources/upload/) to the Viam registry, ensure your model name meets the following requirements:

- The namespace of your model **must** match the [namespace of your organization](/manage/fleet/organizations/#create-a-namespace-for-your-organization).
  For example, if your organization uses the `acme` namespace, your models must all begin with `acme`, like `acme:demo:mybase`.
- Your model triplet must be all-lowercase.
- Your model triplet may only use alphanumeric (`a-z` and `0-9`), hyphen (`-`), and underscore (`_`) characters.

In addition, you should chose a name for the `family` of your model based on the whether your module implements a single model, or multiple models:

- If your module provides a single model, the `family` should match the `subtype` of whichever API your model implements.
  For example, the Intel Realsense module `realsense`, available from the [Viam registry](https://app.viam.com/module/viam/realsense), implements the `camera` component API, so it is named as follows:

  ```json {class="line-numbers linkable-line-numbers"}
  {
    "api": "rdk:component:camera",
    "model": "viam:camera:realsense"
  }
  ```

- If your module provides multiple models, the `family` should describe the common functionality provided across all the models of that module.
  For example, the ODrive module `odrive`, available from the [Viam registry](https://app.viam.com/module/viam/odrive), implements several `motor` component APIs, so it is named as follows:

  ```json {class="line-numbers linkable-line-numbers"}
  {
    "api": "rdk:component:motor",
    "model": "viam:odrive:serial"
  },
  {
    "api": "rdk:component:motor",
    "model": "viam:odrive:canbus"
  }
  ```

The `viam` namespace is reserved for models provided by Viam.

## Management

The Robot Development Kit (RDK) `viam-server` provides automatically manages modular resources to function like built-in resources:

### Logging

You can configure your module to write log messages to the Viam app.
Log messages written to the app appear under the **Logs** tab for the smart machine running the module.
See [Configure logging](/modular-resources/create/#configure-logging) for more information.

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
