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

## Configuration

The micro-RDK currently supports the following models of Motor:

| Model | Description |
| ----- | ----------- |
| [`gpio`](./gpio/) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor) |

## API

The [Motor API](/components/Motor/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`SetPower()`](/components/motor/#setpower)
- [`GetPosition()`](/components/motor/#getposition)
- [`Stop()`](/components/motor/#stop)
