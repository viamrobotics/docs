---
title: "Extend Viam with custom resources"
linkTitle: "Extend Viam"
weight: 60
simple_list: true
no_list: true
type: docs
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Use the SDKs to extend Viam with custom components and services."
---

Viam's [Robot Development Kit (RDK)](/internals/rdk/) provides built-in support for a variety of {{< glossary_tooltip term_id="resource" text="resources" >}}:

- Various types and models of hardware [components](/components/).
- High-level functionality exposed as [services](/services/).

However, you may want to use a hardware component to build your robot that is not built-in to the RDK.
Alternatively, you might want to add new functionality to an existing model of component or create a custom service for your robot to use.
You can extend Viam in these and other ways by creating and using custom resources.

Click on the cards below for instructions on implementing custom resources through {{< glossary_tooltip term_id="module" text="modules" >}} or {{< glossary_tooltip term_id="remote" text="remotes" >}}:

{{< cards >}}
    {{% card link="/program/extend/modular-resources" size="large" %}}
    {{% card link="/program/extend/custom-components-remotes" size="large" %}}
{{< /cards >}}

{{% alert title="Tip" color="tip" %}}

{{< glossary_tooltip term_id="module" text="Modular resources" >}} are the preferred method of creating custom resource implementations with the [Python and Go SDKs](/program/sdks/).

[Adding a custom component as a remote](/program/extend/custom-components-remotes/) is recommended if you are hosting `viam-server` on a non-Linux system or have another issue with compilation.

{{% /alert %}}
