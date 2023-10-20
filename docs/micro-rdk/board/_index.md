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

Click on the model names above for configuration information.

## API

The [Board API](/components/board/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`SetPowerMode()`](/components/board/#setpowermode)
- [`GPIOPin` `Set()`](/components/board/#set)
- [`GPIOPin` `Get()`](/components/board/#get)
- [`GPIOPin` `GetPWM()`](/components/board/#getpwm)
- [`GPIOPin` `SetPWM()`](/components/board/#setpwm)
- [`GPIOPin` `PWMFreq()`](/components/board/#pwmfreq)
- [`GPIOPin` `SetPWMFreq()`](/components/board/#setpwmfreq)
- [`AnalogReader` `Read()`](/components/board/#read)
- [`DigitalInterrupt` `Value()`](/components/board/#value)
