---
title: "Movement Sensor Component"
linkTitle: "Movement sensor"
childTitleEndOverwrite: "Movement Sensor Component"
weight: 20
type: "docs"
description: "Configuration attribute reference for built-in movement sensor models."
no_list: true
tags: ["movement-sensor", "components"]
icon: true
images: ["/icons/components/imu.svg"]
aliases:
  - "/components/movement-sensor/"
---

This section documents the configuration attributes for each built-in movement sensor model.
Use these pages when you are writing a JSON configuration, debugging a config validation error, or looking up the default for a specific attribute.

- For how to add and configure a movement sensor component on your machine, see [Movement sensor](/hardware/common-components/add-a-movement-sensor/).
- For the methods you call on a movement sensor in code, see the [Movement sensor API reference](/reference/apis/components/movement-sensor/).
- For movement sensor models outside the built-in set, search for `movement sensor` in the [Viam registry](https://app.viam.com/registry). Each registry module's configuration is documented in its own README on its registry page.

## Built-in models

The following movement sensor models ship with `viam-server`:

| Model                                   | Description                                                                                                                                                                   |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`fake`](fake/)                         | A model for testing, with no physical hardware.                                                                                                                               |
| [`merged`](merged/)                     | A model that allows you to aggregate the API methods supported by multiple sensors into a singular sensor client, effectively merging the models of the individual resources. |
| [`wheeled-odometry`](wheeled-odometry/) | A model that uses encoders to get an odometry estimate from a wheeled base.                                                                                                   |

## Micro-RDK models

The following movement sensor models ship with the [Micro-RDK](/reference/device-setup/setup-micro/):

| Model                                       | Description |
| ------------------------------------------- | ----------- |
| [`accel-adxl345`](micro-rdk/accel-adxl345/) | —           |
| [`gyro-mpu6050`](micro-rdk/gyro-mpu6050/)   | —           |
