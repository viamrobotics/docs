---
title: "Micro-RDK Motor Models"
linkTitle: "Motor"
weight: 30
type: "docs"
description: "Motor support in the micro-rdk."
images: ["/icons/components/motor.svg"]
tags: ["motor", "components", "micro-rdk"]
no_list: true
# SMEs: Nick M., Gautham V.
---

## Supported Models

For configuration information, click on the supported motor model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`gpio`](./gpio/) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor) |

Click on the model names above for configuration information.

## API

The micro-RDK [motor API](/components/motor/#api) supports only the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`SetPower()`](/components/motor/#setpower)
- [`GetPosition()`](/components/motor/#getposition)
- [`Stop()`](/components/motor/#stop)
