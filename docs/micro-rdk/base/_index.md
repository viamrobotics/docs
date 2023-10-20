---
title: "Micro-RDK Base Models"
linkTitle: "Base"
weight: 30
type: "docs"
description: "The micro-RDK support for moving platforms that the other parts of a mobile robot attach to."
images: ["/icons/components/base.svg"]
tags: ["base", "components", "micro-rdk"]
no_list: true
# SMEs: Nick M., Gautham V.
---

## Supported Models

The micro-RDK currently supports the following models of base:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`esp32_wheeled_base`](esp32_wheeled_base/) | Mobile robot with two wheels |

Click on the model names above for configuration information.

## API

The micro-RDK [base API](/components/base/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`Stop()`](/components/base/#stop)
- [`SetPower()`](/components/base/#setpower)
