---
title: "Micro-RDK Board Models"
linkTitle: "Board"
weight: 30
type: "docs"
description: "Board support in the micro-rdk."
images: ["/icons/components/board.svg"]
tags: ["board", "components", "micro-rdk"]
# SMEs: Nick M., Gautham V.
---

## Configuration

The micro-RDK currently supports the following models of board:

| Model | Description |
| ----- | ----------- |
| [`esp32`](esp32/) | An ESP32 microcontroller |

## API

The [Board API](/components/board/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`SetGPIO()`](/components/board/#setgpio)
- [`GetGPIO()`](/components/board/#getgpio)
- [`PWM()`](/components/board/#pwm)
- [`SetPWM()`](/components/board/#setpwm)
- [`PWMFrequency()`](/components/board/#pwmfrequency)
- [`SetPWMFrequency()`](/components/board/#setpwmfrequency)
- [`ReadAnalogReader()`](/components/board/#readanalogreader)
- [`GetDigitalInterruptValue()`](/components/board/#getdigitalinterruptvalue)
- [`SetPowerMode()`](/components/board/#setpowermode)
