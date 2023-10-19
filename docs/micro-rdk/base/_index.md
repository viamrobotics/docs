---
title: "Micro-RDK Base Models"
linkTitle: "Base"
weight: 30
type: "docs"
description: "Base support in the micro-rdk."
images: ["/icons/components/base.svg"]
tags: ["base", "components", "micro-rdk"]
# SMEs: Nick M., Gautham V.
---

The micro-RDK currently supports the following models of base:

| Model | Description |
| ----- | ----------- |
| [`esp32_wheeled_base`](esp32-wheeled-base/) | Mobile robot with two wheels |

The [Base API](/components/base/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`Stop()`](/components/base/#stop)
- [`SetPower()`](/components/base/#setpower)
