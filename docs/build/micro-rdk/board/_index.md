---
title: "Micro-RDK Board Models"
linkTitle: "Board"
weight: 30
type: "docs"
description: "The micro-RDK support for the signal wire hub of a robot, with GPIO pins for transmitting signals between the robot's computer and its other components."
images: ["/icons/components/board.svg"]
tags: ["board", "components", "micro-rdk"]
no_list: true
aliases:
  - /micro-rdk/board/
# SMEs: Nick M., Gautham V.
---

A board is the signal wire hub of a robot, with GPIO pins for transmitting signals between the robot's computer and its other components.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Board Component](/build/configure/components/board/).

## Supported Models

For configuration information, click on the supported board model name:

<!-- prettier-ignore -->
| Model             | Description              |
| ----------------- | ------------------------ |
| [`esp32`](esp32/) | An ESP32 microcontroller |

## API

The micro-RDK [board API](/build/configure/components/board/#api) supports only the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`SetPowerMode()`](/build/configure/components/board/#setpowermode)

For `GPIOPin`s:

- [`Set()`](/build/configure/components/board/#set)
- [`Get()`](/build/configure/components/board/#get)
- [`GetPWM()`](/build/configure/components/board/#getpwm)
- [`SetPWM()`](/build/configure/components/board/#setpwm)
- [`PWMFreq()`](/build/configure/components/board/#pwmfreq)
- [`SetPWMFreq()`](/build/configure/components/board/#setpwmfreq)

See [PWM signals on `esp32` pins](/build/micro-rdk/board/esp32/#pwm-signals-on-esp32-pins) for more information on setting PWM frequencies with `esp32` boards.

For `AnalogReader`s:

- [`Read()`](/build/configure/components/board/#read)

For `DigitalInterrupt`s:

- [`Value()`](/build/configure/components/board/#value)
