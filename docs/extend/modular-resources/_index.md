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

With one exception, modular resources are [managed by the RDK](/extend/modular-resources/key-concepts/) like built-in resources.

## Get started

To get started adding custom resources to your robot, learn the [key concepts](/extend/modular-resources/key-concepts) behind Viam's resource APIs that make the module system possible.

Then, follow one of the [example tutorials](/extend/examples) to add previously built modules and modular resources to your robot.

If you want to create your own module providing custom resource models or new resource types as modular resources, follow [these instructions](/extend/modular-resources/create) instead.
Then, follow [these steps](/extend/modular-resources/configure) to configure the module and modular resource.

Once you have configured a modular resource, you can test the custom resource using the [Control tab](/manage/fleet/#remote-control) and program it with the [Viam SDKs](/program/apis/).

<!-- Detailed, working examples of various types of modular resources are included in [Viam's GitHub](https://github.com/viamrobotics/rdk/tree/main/examples/customresources). -->

{{< cards >}}
    {{% card link="/services/slam/cartographer/" %}}
    {{% card link="/extend/modular-resources/examples/rplidar" %}}
    {{% card link="/extend/modular-resources/examples/odrive" %}}
{{< /cards >}}
