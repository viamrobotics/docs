---
title: "Integrate Modular Resources into your Robot"
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
The {{< glossary_tooltip term_id="rdk" text="RDK">}} [manages](/extend/modular-resources/key-concepts/) these modular resources like the resource types and models that are built-in to the kit.

Modular resources can be:

1. New models of built-in [components](/components/) or [services](/services/) that implement the built-in resource type's API through Viam's [client SDKs](/program/apis/).
2. Brand new types of resources that define their own API in [protocol buffers](https://developers.google.com/protocol-buffers).

## Get Started

To get started adding custom resources to your robot, learn the [key concepts](/extend/modular-resources/key-concepts/) behind Viam's resource APIs that make the module system possible.

Then, follow one of these [example tutorials](/extend/modular-resources/examples/) to add previously built modules and modular resources to your robot.

If you want to create your own module providing custom resource models or new resource types as modular resources, follow [these instructions](/extend/modular-resources/create/) instead.
After that, follow [these steps](/extend/modular-resources/configure/) to configure the module and modular resource.

Once you have configured a modular resource, you can test the custom resource using the [Control tab](/manage/fleet/#remote-control) and [program](/program/) it with Viam's Go or Python SDKs.

{{< cards >}}
    {{% card link="/extend/modular-resources/examples/rplidar" %}}
    {{% card link="/extend/modular-resources/examples/odrive" %}}
{{< /cards >}}
