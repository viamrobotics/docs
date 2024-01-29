---
title: "Micro-RDK Motor Models"
linkTitle: "Motor"
weight: 30
type: "docs"
description: "Support in the micro-RDK for motors, rotating machines that transform electrical energy into mechanical energy."
images: ["/icons/components/motor.svg"]
tags: ["motor", "components", "micro-rdk"]
no_list: true
aliases:
  - /micro-rdk/motor/
# SMEs: Nick M., Gautham V.
---

A motor is a rotating machine that transforms electrical energy into mechanical energy.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Motor Component](/components/motor/).

## Supported models

For configuration information, click on the supported motor model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`gpio`](./gpio/) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor) |

## API

The micro-RDK [motor API](/components/motor/#api) supports only the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`SetPower()`](/components/motor/#setpower)
- [`GetPosition()`](/components/motor/#getposition)
- [`GetProperties()`](/components/motor/#getproperties)
- [`Stop()`](/components/motor/#stop)
- [`IsMoving()`](/components/motor/#ismoving)
