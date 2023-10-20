---
title: "Micro-RDK Board Models"
linkTitle: "Board"
weight: 30
type: "docs"
description: "Board support in the micro-rdk."
images: ["/icons/components/board.svg"]
tags: ["board", "components", "micro-rdk"]
no_list: true
# SMEs: Nick M., Gautham V.
---

## Supported Models

The micro-RDK currently supports the following models of board:

<!-- prettier-ignore -->
| Model             | Description              |
| ----------------- | ------------------------ |
| [`esp32`](esp32/) | An ESP32 microcontroller |

## API

The [Board API](/components/board/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`SetPowerMode()`](/components/board/#setpowermode)

For `GPIOPin`s:

- [`Set()`](/components/board/#set)
- [`Get()`](/components/board/#get)
- [`GetPWM()`](/components/board/#getpwm)
- [`SetPWM()`](/components/board/#setpwm)
- [`PWMFreq()`](/components/board/#pwmfreq)
- [`SetPWMFreq()`](/components/board/#setpwmfreq)

For `AnalogReader`s:

- `Read()`](/components/board/#read)

For `DigitalInterrupt`s:

- `Value()`](/components/board/#value)
