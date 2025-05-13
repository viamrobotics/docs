---
title: "Advanced Modular Resources"
linkTitle: "Advanced Modules"
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
description: "Some usage may require you to define new APIs or deploy custom components in non-standard ways."
aliases:
  - /program/extend/
  - /modular-resources/advanced/
  - /registry/advanced/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
toc_hide: true
---

Some use cases may require advanced considerations when designing or deploying modular resources.
Depending on your needs, you may wish to define an entirely new resource API, deploy a custom component using a server on a {{< glossary_tooltip term_id="remote-part" text="remote" >}} {{< glossary_tooltip term_id="part" text="part" >}}, or design a custom ML model.

## New APIs

The [component APIs](/dev/reference/apis/#component-apis) and [service APIs](/dev/reference/apis/#service-apis) provide a standard interface for controlling common hardware components and higher level functionality.
If your use case aligns closely with an existing API, you should use that API to program your new resource.

If you want to use most of an existing API but need just a few other functions, you can use the `DoCommand` endpoint together with [extra parameters](/dev/reference/sdks/use-extra-params/) to add custom functionality to an existing resource API.

Or, if your resource does not fit into an existing resource API, you can use one of the following:

- If you are working with a component that doesn't fit into any of the existing [component APIs](/dev/reference/apis/#component-apis), you can use the [generic component](/operate/reference/components/generic/) to build your own component API.
- If you are designing a service that doesn't fit into any of the existing [service APIs](/dev/reference/apis/#service-apis), you can use the [generic service](/dev/reference/apis/services/generic/) to build your own service API.

Both generic resources use the [`DoCommand`](/dev/reference/apis/components/generic/#docommand) endpoint to enable you to make arbitrary calls as needed for your resource.

Alternatively, you can also [define a new resource API](/operate/reference/advanced-modules/create-subtype/) if none of the above options are a good fit for your use case.

## Custom components as remotes

Running {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} on the computer directly connected to your components is the preferred way of managing and controlling custom components.

However, if you are unable to use modular resources because you need to host `viam-server` on a non-Linux system or have an issue with compilation, you may need to [implement a custom component and register it on a server configured as a remote](/operate/reference/advanced-modules/custom-components-remotes/) on your machine.

## Deploy a module using Docker

If you need to package and deploy a module using Docker, for example if your module relies on complex system dependencies, see [Deploy a module using Docker](/operate/reference/advanced-modules/docker-modules/) for suggestions.

## Design a custom ML model

When working with the [ML model service](/dev/reference/apis/services/ml/), you can deploy an [existing model](/data-ai/train/deploy/) or [train your own model](/data-ai/train/train/).

However, if you are writing your own {{< glossary_tooltip term_id="module" text="module" >}} that uses the ML model service together with the [vision service](/dev/reference/apis/services/vision/), you can also [design your own ML model](/data-ai/reference/mlmodel-design/) to better match your specific use case.
