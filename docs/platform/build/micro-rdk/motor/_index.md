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
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Motor Component](/platform/build/configure/components/motor/).

## Supported Models

For configuration information, click on the supported motor model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`gpio`](./gpio/) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor) |

## API

The micro-RDK [motor API](/platform/build/configure/components/motor/#api) supports only the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`SetPower()`](/platform/build/configure/components/motor/#setpower)
- [`GetPosition()`](/platform/build/configure/components/motor/#getposition)
- [`GetProperties()`](/platform/build/configure/components/motor/#getproperties)
- [`Stop()`](/platform/build/configure/components/motor/#stop)
- [`IsMoving()`](/platform/build/configure/components/motor/#ismoving)
