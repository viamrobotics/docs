---
title: "Micro-RDK Movement Sensor Models"
linkTitle: "Movement Sensor"
weight: 30
type: "docs"
description: "The micro-RDK movement sensor component for sensors that measure location, kinematic data, or both."
images: ["/icons/components/imu.svg"]
icon: true
tags: ["movement sensor", "components", "micro-rdk"]
no_list: true
aliases:
  - /micro-rdk/movement-sensor/
# SMEs: Nick M., Gautham V.
---

A movement sensor is a sensor that gives data on where a machine is and how fast it is moving.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Movement Sensor Component](/machine/components/movement-sensor/).

## Supported models

For configuration information, click a supported movement sensor model name:

<!-- prettier-ignore -->
| Model |Description |
| ----- | ---------- |
| [`accel-adxl345`](accel-adxl345/) | The [Analog Devices ADXL345](https://www.analog.com/en/products/adxl345.html) digital accelerometer |
| [`gyro-mpu6050`](gyro-mpu6050/) | A gyroscope/accelerometer manufactured by TDK InvenSense |

{{% readfile "/static/include/micro-create-your-own.md" %}}

## API

The micro-RDK [movement sensor API](/machine/components/movement-sensor/#api) supports only the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`GetReadings()`](/machine/components/movement-sensor/#getreadings)
- [`GetAngularVelocity()`](/machine/components/movement-sensor/#getangularvelocity)
- [`GetLinearVelocity()`](/machine/components/movement-sensor/#getlinearvelocity)
- [`GetCompassHeading()`](/machine/components/movement-sensor/#getcompassheading)
- [`GetPosition()`](/machine/components/movement-sensor/#getposition)
- [`GetProperties()`](/machine/components/movement-sensor/#getproperties)
- [`GetLinearAcceleration()`](/machine/components/movement-sensor/#getlinearacceleration)
- [`DoCommand()`](/machine/components/movement-sensor/#docommand)
