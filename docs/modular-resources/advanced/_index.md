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
description: "Some usage may require you to extend the standardized API definitions or deploy custom components using a server on a remote part"
aliases:
  - "/program/extend/"
---

Some usage may require you to extend the standardized API definitions or deploy custom components using a server on a {{< glossary_tooltip term_id="remote" text="remote part" >}}.

## Custom Components as Remotes

[Modular resources](/modular-resources/) running on the board directly connected to your components are the preferred way of managing and controlling custom components.
However, if you are unable to use [modular resources](/modular-resources/) because you have to host `viam-server` on a non-Linux system or have an issue with compilation, you may need to [implement a custom component and register it on a server configured as a remote](/modular-resources/advanced/custom-components-remotes/) of your robot.

## New API Subtypes

The [component APIs](/program/apis/#component-apis) and [service APIs](/program/apis/#service-apis) provide a standard interface for controlling common hardware components and higher level functionality.

If you want to use most of an existing API but need just a few other functions, try using the [`DoCommand`](/program/apis/#docommand) endpoint and [extra parameters](/program/use-extra-params/) to add custom functionality to an existing subtype.

If your resource does not fit into any of the existing {{< glossary_tooltip term_id="component" text="component" >}} or {{< glossary_tooltip term_id="service" text="service" >}} {{< glossary_tooltip term_id="subtype" text="subtypes" >}} or you want to define different methods for the API, you can [define a new resource _subtype_ and an API for that subtype](/modular-resources/advanced/create-subtype/).
