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
  - "/build/program/extend/"
  - "/modular-resources/advanced/"
---

Some use cases may require advanced considerations when designing or deploying modular resources.
Depending on your needs, you may wish to define a new API subtype, deploy a custom component using a server on a {{< glossary_tooltip term_id="remote" text="remote" >}} {{< glossary_tooltip term_id="part" text="part" >}}, or design a custom ML model.

## New API subtypes

The [component APIs](/build/program/apis/#component-apis) and [service APIs](/build/program/apis/#service-apis) provide a standard interface for controlling common hardware components and higher level functionality.

If you want to use most of an existing API but need just a few other functions, try using the [`DoCommand`](/build/program/apis/#docommand) endpoint and [extra parameters](/build/program/use-extra-params/) to add custom functionality to an existing subtype.

If your resource does not fit into any of the existing {{< glossary_tooltip term_id="component" text="component" >}} or {{< glossary_tooltip term_id="service" text="service" >}} {{< glossary_tooltip term_id="subtype" text="subtypes" >}} or you want to define different methods for the API, you can use the [generic API](/build/configure/components/generic/) with [`DoCommand`](/build/program/apis/#docommand) or [define a new resource subtype and an API for that subtype](/registry/advanced/create-subtype/).

## Custom components as remotes

Running {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} on the [board](/build/configure/components/board/) directly connected to your components is the preferred way of managing and controlling custom components.

However, if you are unable to use [modular resources](/registry/) because you need to host `viam-server` on a non-Linux system or have an issue with compilation, you may need to [implement a custom component and register it on a server configured as a remote](/registry/advanced/custom-components-remotes/) on your machine.

## Design a custom ML model

When working with the [ML model service](/ml/), you can [deploy an existing model](/ml/upload-model/) or [train your own model](/ml/train-model/).

However, if you are writing your own {{< glossary_tooltip term_id="module" text="module" >}} that uses the ML model service together with the [vision service](/ml/vision/), you can also [design your own ML model](/registry/advanced/mlmodel-design/) to better match your specific use case.
