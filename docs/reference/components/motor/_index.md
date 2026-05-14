---
title: "Motor Component"
linkTitle: "Motor"
childTitleEndOverwrite: "Motor Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in motor models."
no_list: true
tags: ["motor", "components"]
icon: true
images: ["/icons/components/motor.svg"]
aliases:
  - "/components/motor/"
---

This section documents the configuration attributes for each built-in motor model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a motor component on your machine, see [Motor](/hardware/common-components/add-a-motor/).
- For the methods you call on a motor in code, see the [Motor API reference](/reference/apis/components/motor/).
- For motor models outside the built-in set, search for `motor` in the [Viam registry](https://app.viam.com/registry). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following motor models ship with `viam-server`:

| Model                             | Description                                                                   |
| --------------------------------- | ----------------------------------------------------------------------------- |
| [`dmc4000`](dmc4000/)             | Stepper motor driven by a DMC-40x0 series motion controller.                  |
| [`encoded-motor`](encoded-motor/) | Standard brushed or brushless DC motor with an encoder.                       |
| [`fake`](fake/)                   | A model for testing, with no physical hardware.                               |
| [`gpio`](gpio/)                   | Supports standard brushed or brushless DC motors.                             |
| [`gpiostepper`](gpiostepper/)     | Supports stepper motors driven by basic GPIO-controlled stepper driver chips. |

## Micro-RDK models

The following motor models ship with the [Micro-RDK](/reference/device-setup/setup-micro/):

| Model                     | Description |
| ------------------------- | ----------- |
| [`gpio`](micro-rdk/gpio/) | —           |
