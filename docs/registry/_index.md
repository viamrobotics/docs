---
title: "Extend Viam with Modules from the Viam Registry"
linkTitle: "Registry"
weight: 33
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
description: "Support additional hardware components or services by adding them from the Viam Registry or by creating new modular resources."
no_list: true
modulescript: true
aliases:
  - "/build/program/extend/modular-resources/"
  - "/extend/modular-resources/"
  - "/extend/"
  - "/build/program/extend/modular-resources/key-concepts/"
  - "/modular-resources/key-concepts/"
  - "/modular-resources/"
menuindent: true
---

Viam provides built-in support for a variety of {{< glossary_tooltip term_id="resource" text="resources" >}}:

- Various types of hardware {{< glossary_tooltip term_id="component" text="components" >}}.
- High-level functionality exposed as {{< glossary_tooltip term_id="service" text="services" >}}.

If the component or service you want to use for your project is not natively supported, you can use _{{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}_ from [the Viam Registry](#the-viam-registry) or [create your own](#create-your-own-modules).

## The Viam Registry

The [Viam registry](https://app.viam.com/registry) is the central place where you can browse {{< glossary_tooltip term_id="module" text="modules" >}} that add capabilities to your machine beyond what is built-in to `viam-server`.

A module provides one or more {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}.
You can search the available modular resources from the Viam Registry here:

<div id="searchbox"></div>
<p>
<div id="searchstats"></div></p>
<div class="mr-component" id="">
  <div class="modellistheader">
    <div class="type">API</div>
    <div class="name">Model</div>
    <div>Description</div>
  </div>
<div id="hits" class="modellist">
</div>
<div id="pagination"></div>
</div>

You can see details about each module in the [Viam registry](https://app.viam.com/registry) on its dedicated module page.
You can integrate modules into any Viam-powered machine.

## Use modules

To use a modular resource from the registry, add it from your robot's **Config** tab in the Viam app, using the **Create component** button.

After adding a module to your robot, you can choose to [configure](/registry/configure/) it for automatic version updates from the Viam registry, or update your module manually.
By default, newly added modules will remain at the version they were when you installed them, and will not update automatically.

Once you have added and configured the module you would like to use in the Viam app, you can test your added resource using the [**Control** tab](/fleet/#remote-control) and program it using [standardized APIs](/build/program/apis/).

`viam-server` manages the [dependencies](/reference/internals/rdk/#dependency-management), [start-up](/reference/internals/rdk/#start-up), [reconfiguration](/fleet/#reconfiguration), [data management](/build/configure/services/data/configure-data-capture/#configure-data-capture-for-individual-components), and [shutdown](/reference/internals/rdk/#shutdown) behavior of your modular resource.

### Tutorials using modules

{{< cards >}}
{{% card link="/tutorials/projects/make-a-plant-watering-robot/" %}}
{{% card link="/tutorials/projects/integrating-viam-with-openai/" %}}
{{< /cards >}}

## Create your own modules

If none of the existing modular resources in the Viam registry support your use case, you can create your own modules with your own modular resources:

- **Implement a custom component**: Write a driver for an unsupported {{< glossary_tooltip term_id="component" text="component" >}} by implementing the corresponding component API.

- **Implement a custom service**: Implement your own algorithm or {{< glossary_tooltip term_id="model" text="model" >}} against a corresponding service API or use custom algorithms or data models when working with services such as {{< glossary_tooltip term_id="slam" text="SLAM" >}}, vision, or motion planning.

You can write modules in a variety of programming languages, such as, Go, Python, C++, Rust, while implementing the same [APIs](/build/program/apis/).
To create a new module:

1. [Create a module](/registry/create/) with one or more modular resources by implementing all methods for the component's or service's standardized API.
1. [Upload the module to the Viam registry](/registry/upload/) to make it available for deployment to robots or add it as a [local module](/registry/configure/#local-modules).
   You can upload _private_ modules for your {{< glossary_tooltip term_id="organization" text="organization" >}} or _public_ modules.
1. Once you have uploaded your module to the registry, [deploy and configure the module](/registry/configure/) from the Viam app.
   Then, you can test your added resource using the [**Control** tab](/fleet/#remote-control) and [program](/build/program/) it with Viam's Go or Python SDKs.

### Tutorials creating modules

{{< cards >}}
{{% card link="/tutorials/custom/custom-base-dog/" %}}
{{% card link="/registry/examples/custom-arm/" %}}
{{< /cards >}}
