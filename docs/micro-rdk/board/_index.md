---
title: "Micro-RDK Board Models"
linkTitle: "Board"
weight: 30
type: "docs"
description: "The micro-RDK board component for the signal wire hub of a smart machine, with GPIO pins for transmitting signals between the machine's computer and its other components."
images: ["/icons/components/board.svg"]
icon: true
tags: ["board", "components", "micro-rdk"]
no_list: true
aliases:
  - /micro-rdk/board/
# SMEs: Nick M., Gautham V.
---

A board is the signal wire hub of a {{< glossary_tooltip term_id="machine" text="smart machine" >}}, with GPIO pins for transmitting signals between the machine's computer and its other components.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Board Component](/machine/components/board/).

## Supported models

For configuration information, click on the supported board model name:

<!-- prettier-ignore -->
| Model             | Description              |
| ----------------- | ------------------------ |
| [`esp32`](esp32/) | An ESP32 microcontroller |

{{% readfile "/static/include/micro-create-your-own.md" %}}

## API

The micro-RDK [board API](/machine/components/board/#api) supports only the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`SetPWM()`](/machine/components/board/#setpwm)
- [`DoCommand()`](/machine/components/board/#docommand)

For `GPIOPin`s:

- [`SetGPIO()`](/machine/components/board/#setgpio)
- [`GetGPIO()`](/machine/components/board/#getgpio)
- [`GetPWM()`](/machine/components/board/#getpwm)
- [`SetPWM()`](/machine/components/board/#setpwm)
- [`PWMFreq()`](/machine/components/board/#pwmfreq)
- [`SetPWMFreq()`](/machine/components/board/#setpwmfreq)

See [PWM signals on `esp32` pins](/micro-rdk/board/esp32/#pwm-signals-on-esp32-pins) for more information on setting PWM frequencies with `esp32` boards.

For `Analog`s:

- [`Read()`](/machine/components/board/#read)

For `DigitalInterrupt`s:

- [`Value()`](/machine/components/board/#value)
