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
---

Some use cases may require you to define a new API, or deploy a custom component using a server on a {{< glossary_tooltip term_id="remote" text="remote part" >}}.

## New API subtypes

The [component APIs](/program/apis/#component-apis) and [service APIs](/program/apis/#service-apis) provide a standard interface for controlling common hardware components and higher level functionality.

If you want to use most of an existing API but need just a few other functions, try using the [`DoCommand`](/program/apis/#docommand) endpoint and [extra parameters](/program/use-extra-params/) to add custom functionality to an existing subtype.

If your resource does not fit into any of the existing {{< glossary_tooltip term_id="component" text="component" >}} or {{< glossary_tooltip term_id="service" text="service" >}} {{< glossary_tooltip term_id="subtype" text="subtypes" >}} or you want to define different methods for the API, you can use the [generic API](/components/generic/) with the [`DoCommand`](/program/apis/#docommand) or [define a new resource subtype and an API for that subtype](/modular-resources/advanced/create-subtype/).

## Custom components as remotes

Running {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} on the [board](/components/board/) directly connected to your components is the preferred way of managing and controlling custom components.
However, if you are unable to use [modular resources](/modular-resources/) because you have to host `viam-server` on a non-Linux system or have an issue with compilation, you may need to [implement a custom component and register it on a server configured as a remote](/modular-resources/advanced/custom-components-remotes/) of your robot.
