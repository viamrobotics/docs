---
title: "Micro-RDK Generic Models"
linkTitle: "Generic"
weight: 30
type: "docs"
description: "Support in the micro-RDK for generic compoent types."
images: ["/icons/components/generic.svg"]
tags: ["generic", "components", "micro-rdk"]
no_list: true
# SMEs: Gautham V.
---

The _generic_ component {{< glossary_tooltip term_id="subtype" text="subtype" >}} enables you to add support for unique types of hardware that do not already have an [appropriate API](/build/program/apis/#component-apis) defined for them.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Generic Component](/components/generic/).

## Supported Models

For configuration information, click on the supported generic model name:

<!-- prettier-ignore -->
Model | Description
----- | -----------
[`fake`](fake/) | A model used for testing, with no physical hardware.

## API

The micro-RDK [generic API](/components/generic/#api) supports only the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`DoCommand()`](/components/generic/#docommand)
