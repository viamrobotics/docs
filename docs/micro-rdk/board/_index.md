---
title: "Micro-RDK Board Models"
linkTitle: "Board"
weight: 30
type: "docs"
description: "Board support in the micro-rdk."
images: ["/icons/components/board.svg"]
tags: ["board", "components", "micro-rdk"]
# SMEs: Nick M., Gautham V.
---

The micro-RDK currently supports the following models of Board:

| Model | Description |
| ----- | ----------- |
| [`esp32`](esp32/) | ESP32 board |

The [Board API](/components/board/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`Stop()`](/components/Board/#stop)
- [`SetPower()`](/components/Board/#setpower)
