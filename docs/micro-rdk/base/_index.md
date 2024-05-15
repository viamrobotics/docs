---
title: "Micro-RDK Base Models"
linkTitle: "Base"
weight: 30
type: "docs"
description: "The micro-RDK base component for moving platforms that the other parts of a mobile robot attach to."
images: ["/icons/components/base.svg"]
icon: true
tags: ["base", "components", "micro-rdk"]
no_list: true
# SMEs: Nick M., Gautham V.
aliases:
  - /micro-rdk/base/
---

A base is the moving platform that the other parts of a mobile robot attach to.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see the [Base Component](/machine/components/base/).

## Supported models

For configuration information, click on the supported base model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`two_wheeled_base`](two_wheeled_base/) | Mobile robot with two wheels |

{{% readfile "/static/include/micro-create-your-own.md" %}}

## API

The micro-RDK [base API](/machine/components/base/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`Stop()`](/machine/components/base/#stop)
- [`SetPower()`](/machine/components/base/#setpower)
- [`DoCommand()`](/machine/components/base/#docommand)
