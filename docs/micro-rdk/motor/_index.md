---
title: "Micro-RDK Motor Models"
linkTitle: "Motor"
weight: 30
type: "docs"
description: "Motor support in the micro-rdk."
images: ["/icons/components/motor.svg"]
tags: ["motor", "components", "micro-rdk"]
# SMEs: Nick M., Gautham V.
---

The micro-RDK currently supports the following models of Motor:

| Model | Description |
| ----- | ----------- |
| [`single`](single/) | |
| [`incremental`](incremental/) | |

The [Motor API](/components/Motor/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`Stop()`](/components/Motor/#stop)
- [`SetPower()`](/components/Motor/#setpower)
