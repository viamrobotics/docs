---
title: "Micro-RDK Servo Models"
linkTitle: "Servo"
weight: 30
type: "docs"
description: "Support in the micro-RDK for servos, small motors whose position you can precisely control."
images: ["/icons/components/servo.svg"]
tags: ["servo", "components", "micro-rdk"]
no_list: true
aliases:
  - /micro-rdk/servo/
# SMEs: Nicolas M., Gautham V.
---

The servo component supports ["RC" or "hobby" servo motors](https://learn.adafruit.com/adafruit-motor-selection-guide/rc-servos).
These are small motors with built-in potentiometer position sensors, enabling you to control the angular position of the servo precisely.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Servo Component](/build/configure/components/servo/).

## Supported Models

For configuration information, click on the supported servo model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`gpio`](gpio/) | A hobby servo. |

## API

The micro-RDK [servo API](/build/configure/components/servo/#api) supports the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`Move()`](/build/configure/components/servo/#move)
- [`GetPosition()`](/build/configure/components/servo/#getposition)
- [`Stop()`](/build/configure/components/servo/#stop)
