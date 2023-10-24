---
title: "Micro-RDK Board Models"
linkTitle: "Board"
weight: 30
type: "docs"
description: "The micro-RDK support for the signal wire hub of a robot, with GPIO pins for transmitting signals between the robot's computer and its other components."
images: ["/icons/components/board.svg"]
tags: ["board", "components", "micro-rdk"]
no_list: true
# SMEs: Nick M., Gautham V.
---

A board is the signal wire hub of a robot, with GPIO pins for transmitting signals between the robot's computer and its other components.
For more information and models supported by [the RDK (features provided by the full version of `viam-server`)](/internals/rdk/), see the [Board component](/components/board/).

## Supported Models

For configuration information, click on the supported board model name:

<!-- prettier-ignore -->
| Model             | Description              |
| ----------------- | ------------------------ |
| [`esp32`](esp32/) | An ESP32 microcontroller |

## API

The micro-RDK [board API](/components/board/#api) supports only the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`SetPowerMode()`](/components/board/#setpowermode)

For `GPIOPin`s:

- [`Set()`](/components/board/#set)
- [`Get()`](/components/board/#get)
- [`GetPWM()`](/components/board/#getpwm)
- [`SetPWM()`](/components/board/#setpwm)
- [`PWMFreq()`](/components/board/#pwmfreq)
- [`SetPWMFreq()`](/components/board/#setpwmfreq)

For `AnalogReader`s:

- [`Read()`](/components/board/#read)

For `DigitalInterrupt`s:

- [`Value()`](/components/board/#value)
