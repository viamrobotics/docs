---
title: "Micro-RDK Movement Sensor Models"
linkTitle: "Movement Sensor"
weight: 30
type: "docs"
description: "Support in the micro-RDK for movement sensors, sensors that measure location, kinematic data, or both."
images: ["/icons/components/imu.svg"]
tags: ["movement sensor", "components", "micro-rdk"]
no_list: true
# SMEs: Nick M., Gautham V.
---

A movement sensor is a sensor that gives data on where a robot is and how fast it is moving.
For more information and models supported by the {{< glossary_tooltip term_id="rdk" text="RDK" >}}, see [Movement Sensor Component](/components/movement-sensor/).

## Configuration

For configuration information, click a supported movement sensor model name:

<!-- prettier-ignore -->
| Model |Description |
| ----- | ---------- |
| [`accel-adxl345`](accel-adxl345/) | The [Analog Devices ADXL345](https://www.analog.com/en/products/adxl345.html) digital accelerometer |
| [`gyro-mpu6050`](gyro-mpu6050/) | A gyroscope/accelerometer manufactured by TDK InvenSense |

## API

The micro-RDK [movement sensor API](/components/movement-sensor/#api) supports only the following client SDK API methods, which operate the same as in the full-featured RDK:

- [`GetAngularVelocity()`](/components/movement-sensor/#getangularvelocity)
- [`GetLinearVelocity()`](/components/movement-sensor/#getlinearvelocity)
- [`GetCompassHeading()`](/components/movement-sensor/#getcompassheading)
- [`GetPosition()`](/components/movement-sensor/#getposition)
- [`GetProperties()`](/components/movement-sensor/#getproperties)
- [`GetLinearAcceleration()`](/components/movement-sensor/#getlinearacceleration)
