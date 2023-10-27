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
A module can provide one or more modular resource models.

## Modules

A _module_ provides one or more [_modular resources_](#resources), and is a flexible way to extend the functionality of your Viam robot.
Modules run alongside `viam-server` as a separate process, communicating with `viam-server` over a UNIX socket.
A module provides definitions for one or more pairs of [APIs](#valid-apis-to-implement-in-your-model) and [models](#models).

When the module initializes, it registers those pairs on your robot, making the functionality defined by that pair available for use.

You can [upload your own modules to the Viam registry](/modular-resources/upload/) or can [add existing modules from the Registry](/modular-resources/configure/).

See [Creating a custom module](/modular-resources/create/) for more information.

## Resources

A resource is a [component](/components/) or [service](/services/).
Each component or service is typed by a proto API, such as the [component proto definitions](https://github.com/viamrobotics/api/tree/main/proto/viam/component).

Any resource on your robot needs to implement either one of these [existing Viam APIs](#valid-apis-to-implement-in-your-model), or a custom interface.

A _modular resource_ is a resource that is provided by a [module](#modules), and not built-in to the RDK.
A modular resource runs in the module process. This differs from built-in resources, which run as part of `viam-server`.

## Models

A _model_ describes a specific implementation of a [resource](#resources) that implements (speaks) its [API](/program/apis/).
Models allow you to control different instances of a resource with a consistent interface, even if the underlying implementation differs.

For example, some DC motors communicate using [GPIO](/components/board/), while other DC motors use serial protocols like the [SPI bus](/components/board/#spis).
Regardless, you can power any motor model that implements the `rdk:component:motor` API with the `SetPower()` method.

Models are uniquely namespaced as colon-delimited-triplets.
Modular resource model names have the form `namespace:repo-name:name`.
Built-in model names have the form `rdk:builtin:name`.
See [Naming your model](#naming-your-model-namespacerepo-namename) for more information.

Models are either:

- Built into the RDK, and included when you [install `viam-server`](/installation/) or when you use one of the [Viam SDKs](/program/apis/).
- Provided in [custom modules](#modules) available for download from the [Viam registry](https://app.viam.com/registry), and are written by either Viam or community users.

### Built-in models

Viam provides many built-in models that implement API capabilities, each using `rdk` as the `namespace`, and `builtin` as the `family`.
These models run within `viam-server`.

For example:

- The `rdk:builtin:gpio` model of the `rdk:component:motor` API provides RDK support for [GPIO-controlled DC motors](/components/motor/gpio/).
- The `rdk:builtin:DMC4000` model of the same `rdk:component:motor` API provides RDK support for the [DMC4000](/components/motor/dmc4000/) motor.

### Custom models

The [Viam registry](https://app.viam.com/registry) makes available both Viam-provided and community-written modules for download and use on your robot.
These models run outside `viam-server` as a separate process.

#### Valid APIs to implement in your model

When implementing a custom [model](#models) of an existing [component](/components/), valid [APIs](/program/apis/) are always:

- `namespace`: `rdk`
- `type`: `component`
- `subtype`: any one of [these component proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/component).

When implementing a custom [model](#models) of an existing [service](/services/), valid [APIs](/program/apis/) are always

- `namespace`: `rdk`
- `type`: `service`
- `subtype`: any one of [these service proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/service).

#### Naming your model: namespace:repo-name:name

If you are [creating a custom module](/modular-resources/create/) and [uploading that module](/modular-resources/upload/) to the Viam registry, ensure your model name meets the following requirements:

- The namespace of your model **must** match the [namespace of your organization](/manage/fleet/organizations/#create-a-namespace-for-your-organization).
  For example, if your organization uses the `acme` namespace, your models must all begin with `acme`, like `acme:demo:mybase`.
- Your model triplet must be all-lowercase.
- Your model triplet may only use alphanumeric (`a-z` and `0-9`), hyphen (`-`), and underscore (`_`) characters.

For the middle segment of your model triplet `repo-name`, use the name of the git repository where you store your module's code.
The `repo-name` should describe the common functionality provided across the model or models of that module.

For example:

- The `rand:yahboom:arm` model and the `rand:yahboom:gripper` model uses the repository name [yahboom](https://github.com/viam-labs/yahboom).
  The models implement the `rdk:component:arm` and the `rdk:component:gripper` API to support the Yahboom DOFBOT arm and gripper respectively.

  ```json {class="line-numbers linkable-line-numbers"}
  {
    "api": "rdk:component:arm",
    "model": "rand:yahboom:arm"
  },
  {
    "api": "rdk:component:gripper",
    "model": "rand:yahboom:gripper"
  }
  ```

- The `viam-labs:audioout:pygame` model uses the repository name [audioout](https://github.com/viam-labs/audioout)
  It implements the custom API `viam-labs:service:audioout`.

  ```json {class="line-numbers linkable-line-numbers"}
  {
    "api": "viam-labs:service:audioout",
    "model": "viam-labs:audioout:pygame"
  }
  ```

A model with the `viam` namespace is always Viam-provided.

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
