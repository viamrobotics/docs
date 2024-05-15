---
title: "Advanced Modular Resources"
linkTitle: "Advanced"
weight: 80
simple_list: true
no_list: true
type: docs
tags:
  [
    "server",
    "rdk",
    "extending viam",
    "modular resources",
    "components",
    "services",
  ]
description: "Some usage may require you to define new APIs or deploy custom components using a server on a remote part"
aliases:
  - "/program/extend/"
  - "/modular-resources/advanced/"
---

Some use cases may require advanced considerations when designing or deploying modular resources.
Depending on your needs, you may wish to define a new API subtype, deploy a custom component using a server on a {{< glossary_tooltip term_id="remote-part" text="remote" >}} {{< glossary_tooltip term_id="part" text="part" >}}, or design a custom ML model.

## New API subtypes

The [component APIs](/program/apis/#component-apis) and [service APIs](/program/apis/#service-apis) provide a standard interface for controlling common hardware components and higher level functionality.
If your use case aligns closely with an existing API, you should use that API to program your new resource.

If you want to use most of an existing API but need just a few other functions, you can use the [`DoCommand`](/program/apis/#docommand) endpoint together with [extra parameters](/program/use-extra-params/) to add custom functionality to an existing resource {{< glossary_tooltip term_id="subtype" text="subtype" >}}.

Or, if your resource does not fit into an existing resource subtype, you can use one of the following:

- If you are working with a component that doesn't fit into any of the existing [component APIs](/program/apis/#component-apis), you can use the [generic component](/machine/components/generic/) to build your own component API.
- If you are designing a service that doesn't fit into any of the existing [service APIs](/program/apis/#service-apis), you can use the [generic service](/app/registry/advanced/generic/) to build your own service API.

Both generic resources use the [`DoCommand`](/program/apis/#docommand) endpoint to enable you to make arbitrary calls as needed for your resource.

Alternatively, you can also [define a new resource subtype and an API for that subtype](/app/registry/advanced/create-subtype/) if none of the above options are a good fit for your use case.

## Custom components as remotes

Running {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} on the [board](/machine/components/board/) directly connected to your components is the preferred way of managing and controlling custom components.

However, if you are unable to use [modular resources](/app/registry/) because you need to host `viam-server` on a non-Linux system or have an issue with compilation, you may need to [implement a custom component and register it on a server configured as a remote](/app/registry/advanced/custom-components-remotes/) on your machine.

## Design a custom ML model

When working with the [ML model service](/ml/), you can [deploy an existing model](/ml/upload-model/) or [train your own model](/app/ml/train-model/).

However, if you are writing your own {{< glossary_tooltip term_id="module" text="module" >}} that uses the ML model service together with the [vision service](/services/vision/), you can also [design your own ML model](/app/registry/advanced/mlmodel-design/) to better match your specific use case.
