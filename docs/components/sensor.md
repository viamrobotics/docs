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
Viam has a few types of sensor implemented including an ultrasonic sensor, but this doc will go over setting up a custom sensor so you can implement almost any sort of sensor.
Note that Viam has a separate, more specific component type called *movement sensor* specifically for GPS units, IMUs, and other sensors that detect position, velocity and acceleration.
<!-- * [Movement Sensors](../movementsensor/) Not quite ready to land movement-sensor doc --->
* [Encoders (component type)](../encoder/).

## Hardware Requirements

* Some sort of sensor
* A [board](../board/)
* Depending on the type of sensor output, an analog to digital converter may be necessary to allow the sensor to communicate with the board

## Wiring

This will depend on the sensor. Refer to the sensor’s data sheet.

## Viam Configuration

When you create a custom sensor you’ll create a set of attributes unique to that sensor model. The JSON file you create must include a type (`sensor`), model (whatever you named your custom sensor model), and name (of your choice; used to refer to that specific sensor in your code). You will also need to include whatever required attributes you define in your custom sensor component implementation.

``` json
{
    "name": "mySensorName",
    "type": "sensor",
    "model": "mySensorModel",
    "attributes": {},
    "depends_on": []
}
```

## Getting started with sensors and the Viam SDK

This example code reads values from an ultrasonic sensor connected to a robot.

Assumption: A sensor called "ultra1" is configured as a component of your robot.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.sensor import Sensor

robot = await connect()
sensor = Sensor.from_robot(robot, "ultra1")
distance = await sensor.get_readings()["distance"]
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
