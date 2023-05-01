---
title: "Extend Viam with custom resources"
linkTitle: "Extend Viam"
weight: 60
simple_list: true
no_list: true
type: docs
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Extend Viam by creating custom components and services."
---

Viam's [Robot Development Kit (RDK)](/internals/rdk/) provides built-in support for a variety of {{< glossary_tooltip term_id="resource" text="resources" >}}:

- Various types and models of hardware [components](/components).
- High-level functionality exposed as [services](/services).

However, you may want to use a hardware component to build your robot that is not built-in to the RDK.
Alternatively, you might want to add new functionality to an existing model of component or create a custom service for your robot to use.
You can extend Viam in these and other ways by creating and using custom resources.

{{< cards >}}
    {{% card link="/program/extend/modular-resources" size="large" %}}
    {{% card link="/program/extend/custom-components-remotes" size="large" %}}
{{< /cards >}}
