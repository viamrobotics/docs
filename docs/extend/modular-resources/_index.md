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
`viam-server` [manages](/extend/modular-resources/key-concepts/) modular resources and built-in resources in the same way.

Modular resources can be:

1. New models of built-in [components](/components/) or [services](/services/) that implement the built-in resource {{< glossary_tooltip term_id="api-namespace-triplet" text="subtype" >}}'s API through Viam's [client SDKs](/program/apis/).
2. Brand new types of resources that define their own API in [protocol buffers](https://developers.google.com/protocol-buffers).

## Get Started

To get started adding custom resources to your robot, learn the [key concepts](/extend/modular-resources/key-concepts/) behind Viam's resource APIs that make the module system possible.

Then, follow one of these [example tutorials](/extend/modular-resources/examples/) to add previously built modules and modular resources to your robot.

If you want to create your own module providing a new resource model or a new resource type as a modular resource, follow [these instructions](/extend/modular-resources/create/).
Then, follow [these steps](/extend/modular-resources/configure/) to configure the module and modular resource.

Once you have configured a modular resource, you can test the custom resource using the [Control tab](/manage/fleet/#remote-control) and [program](/program/) it with Viam's Go or Python SDKs.

## Related tutorials

{{< cards >}}
    {{% card link="/extend/modular-resources/examples/rplidar" %}}
    {{% card link="/extend/modular-resources/examples/odrive" %}}
    {{% card link="/tutorials/custom/custom-base-dog/" %}}
{{< /cards >}}
