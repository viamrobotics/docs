---
title: "Micro-RDK Encoder Models"
linkTitle: "Encoder"
weight: 30
type: "docs"
description: "Encoder support in the micro-rdk."
images: ["/icons/components/encoder.svg"]
tags: ["encoder", "components", "micro-rdk"]
# SMEs: Nick M., Gautham V.
---

The micro-RDK currently supports the following models of Encoder:

| Model | Description |
| ----- | ----------- |
| [`single`](single/) | |
| [`incremental`](incremental/) | |

The [Encoder API](/components/Encoder/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`Stop()`](/components/Encoder/#stop)
- [`SetPower()`](/components/Encoder/#setpower)
