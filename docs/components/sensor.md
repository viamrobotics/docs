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
Viam has a few types of sensor implemented including an ultrasonic sensor, but this doc covers setting up a custom sensor so you can build a robot using almost any sort of sensor.

{{% alert title="Note" color="note" %}}

Viam has a separate, more specific component type called *movement sensor* specifically for Global Positioning Systems (GPS) units, IMUs, and other sensors that detect position, velocity, and acceleration.

{{% /alert %}}

* [Encoders (component type)](/components/movement-sensor//).

## Hardware Requirements

* Some sort of sensor, such as a [ultrasonic sensor](/components/ultrasonic-sensor/), [encoder](/components/encoder/), or [IMU](/components/imu/), or any other sensor that can connect to a robot.
* A [board](/components/board/)
* Depending on the your sensor's output, an analog to digital converter may be necessary to allow the sensor to communicate with the board.

## Wiring

This depends on the sensor. Refer to the sensor’s data sheet for wiring details.

## Viam Configuration

When you create a custom sensor you’ll create a set of attributes unique to that sensor model. The JSON file you create must include a type (`sensor`), model (whatever you named your custom sensor model), and name (of your choice; used to see that specific sensor in your code). You also must include whatever required attributes you define in your custom sensor component implementation.

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
