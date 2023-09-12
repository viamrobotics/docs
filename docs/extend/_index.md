---
title: "Extend Viam with modular resources"
linkTitle: "Extend Viam"
weight: 63
simple_list: true
no_list: true
type: docs
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Extend Viam with modular resources from the Viam registry."
aliases:
  - "/program/extend/"
---

Viam's [Robot Development Kit (RDK)](/internals/rdk/) provides built-in support for a variety of {{< glossary_tooltip term_id="resource" text="resources" >}}:

- Various types of hardware [components](/components/).
- High-level functionality exposed as [services](/services/).

However, if you want to work with a new hardware component that is not already supported by Viam, or want to introduce a new software service or service model to support additional functionality on your robot, you can extend Viam by adding a [modular resource](/extend/modular-resources/) to your robot.

Click on the cards below for instructions on implementing modular resources through {{< glossary_tooltip term_id="module" text="modules" >}} or {{< glossary_tooltip term_id="remote" text="remotes" >}}:

{{< cards >}}
    {{% card link="/extend/modular-resources" %}}
    {{% card link="/extend/custom-components-remotes" %}}
{{< /cards >}}

{{% alert title="Tip" color="tip" %}}

[Modular resources](/extend/modular-resources/) provided by custom {{< glossary_tooltip term_id="module" text="modules" >}} are the preferred method of creating custom resource implementations.

[Adding a custom component as a remote](/extend/custom-components-remotes/) is recommended if you are hosting `viam-server` on a non-Linux system or have another issue with compilation.

{{% /alert %}}
