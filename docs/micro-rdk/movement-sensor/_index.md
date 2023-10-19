---
title: "Micro-RDK Movement Sensor Models"
linkTitle: "Movement Sensor"
weight: 30
type: "docs"
description: "Movement Sensor support in the micro-rdk."
images: ["/icons/components/imu.svg"]
tags: ["movement sensor", "components", "micro-rdk"]
# SMEs: Nick M., Gautham V.
---

The micro-RDK currently supports the following models of Movement Sensor:

| Model | Description |
| ----- | ----------- |
| [`accel-adxl345`](accel-adxl345/) | The [Analog Devices ADXL345](https://www.analog.com/en/products/adxl345.html) digital accelerometer |
| [`gyro-mpu6050`](gyro-mpu6050/) | A gyroscope/accelerometer manufactured by TDK InvenSense |

The [Movement Sensor API](/components/movement-sensor/#api) is limited to the following supported client SDK API methods, which operate the same as in the full-featured RDK:

- [`GetAngularVelocity()`](/components/movement-sensor/#getangularvelocity)
- [`GetLinearVelocity()`](/components/movement-sensor/#getlinearvelocity)
- [`GetCompassHeading()`](/components/movement-sensor/#getcompassheading)
- [`GetPosition()`](/components/movement-sensor/#getposition)
- [`GetProperties()`](/components/movement-sensor/#getproperties)
- [`GetLinearAcceleration()`](/components/movement-sensor/#getlinearacceleration)