---
title: "Integrate Modular Resources into your robot"
linkTitle: "Modular Resources"
weight: 10
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Use the Viam module system to implement custom resources that can be included in any Viam-powered robot."
no_list: true
aliases:
    - "/program/extend/modular-resources/"
---

The Viam module system allows you to integrate custom {{< glossary_tooltip term_id="resource" text="resources" >}} into any robot running on Viam.

Modular resources can be either:

1. New models of built-in [components](/components/) or [services](/services/) that implement the built-in resource type's API through Viam's [client SDKs](/program/sdks/).
2. Brand new types of resources that define their own API in [protocol buffers](https://developers.google.com/protocol-buffers).

To get started adding custom resources to your robot, learn the [key concepts](/extend/modular-resources/key-concepts) behind Viam's resource APIs that make the module system possible.

Then, follow one of the [example tutorials](/extend/examples) to add previously built modules and modular resources to your robot.

If you want to create your own module providing custom resource models or new resource types as modular resources, follow [these instructions](/extend/modular-resources/create) instead.
Then, follow [these steps](/extend/modular-resources/configure) to configure the module and modular resource.

Once you have configured a modular resource, you can test the custom resource using the [Control tab](/manage/fleet/#remote-control) and program it with the [Viam SDKs](/program/apis/).

<!-- Detailed, working examples of various types of modular resources are included in [Viam's GitHub](https://github.com/viamrobotics/rdk/tree/main/examples/customresources). -->

### Modular resource management

With one [exception](#limitations), modular resources function like built-in resources:

#### Dependency Management

Modular resources may depend on other built-in resources or other modular resources, and vice versa.
The Viam RDK handles dependency management.

#### Start-up

The RDK ensures that any configured modules are loaded automatically on start-up, and that configured modular resource instances are started alongside configured built-in resource instances.

#### Reconfiguration

When you change the configuration of a Viam robot, the behavior of modular resource instances versus built-in resource instances is equivalent.
This means you can add, modify, and remove a modular resource instance from a running robot as normal.

#### Data management

Data capture for individual components is supported on [certain component types](../../services/data/configure-data-capture/#configure-data-capture-for-individual-components).
If your modular resource is a model of one of these types, you can configure data capture on it just as you would on a built-in resource.

#### Shutdown

During robot shutdown, the RDK handles modular resource instances similarly to built-in resource instances - it signals them for shutdown in topological (dependency) order.

#### Modular resources as remotes

[Remote](/manage/parts-and-remotes/) parts may load their own modules and provide modular resources, just as the main part can.
This means that you can compose a robot of any number of parts running in different compute locations, each containing both built-in and custom resources.

### Limitations

Custom models of the [arm](/components/arm/) component type are not yet supported, as kinematic information is not currently exposed through the arm API.

{{< cards >}}
    {{% card link="/services/slam/cartographer/" %}}
    {{% card link="/extend/modular-resources/examples/rplidar" %}}
    {{% card link="/extend/modular-resources/examples/odrive" %}}
{{< /cards >}}
