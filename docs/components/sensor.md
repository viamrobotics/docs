---
title: "Sensor Component"
linkTitle: "Sensor"
weight: 70
draft: false
type: "docs"
description: "Explanation of sensor configuration and usage in Viam."
tags: ["sensor", "components"]
# SME: #team-bucket
---
This page explains how to set up a generic sensor component with Viam.
Viam has a few types of sensor implemented including an ultrasonic sensor, temperature sensors and more, but this doc covers setting up a custom sensor so you can build a robot using almost any sort of sensor.

{{% alert title="Note" color="note" %}}

Viam has a separate, more specific component type called [movement sensor](/components/movement-sensor/) specifically for Global Positioning Systems (GPS) units, IMUs, and other sensors that detect position, velocity, and acceleration.

{{% /alert %}}

## Hardware Requirements

* [Ultrasonic sensor](/components/ultrasonic-sensor/), [encoder](/components/encoder/), or [IMU](/components/imu/), or any other sensor that can connect to a robot.
* A [board](/components/board/)
* Depending on your sensor's output, an analog to digital converter may be necessary to allow the sensor to communicate with the board.

## Wiring

The wiring for your sensor depends on the specific sensor you are using. Refer to the sensor’s data sheet for wiring details.

## Viam Configuration

To create a custom sensor, you must create a set of attributes unique to that sensor model:

| key | description |
| --- | ------------ |
| `name` |  The name that you use to refer to the sensor in your code. |
| `type` |  For a sensor, the type is `sensor`. |
| `model` |  The name you gave your custom sensor model |
| `name` |

Don't forget to include any required attributes you define in your custom sensor component implementation.

``` json
{
    "name": "mySensorName",
    "type": "sensor",
    "model": "mySensorModel",
    "attributes": {},
    "depends_on": []
}
```

## Getting Started With Sensors and the Viam SDK

This example code reads values from an ultrasonic sensor connected to a robot.

Assumption: A sensor called "ultra1" configured as a component of your robot.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.sensor import Sensor

robot = await connect()
sensor = Sensor.from_robot(robot, "ultra1")
distance = await sensor.get_readings()["distance"]
readings = await sensor.get_readings()["distance"]
distance = readings["distance"]
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
"go.viam.com/rdk/components/sensor"
)

ultra, err := sensor.FromRobot(robot, "ultra1")
distance, err := ultra.Readings(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

You can read more about sensor implementation in the [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/sensor/index.html).
