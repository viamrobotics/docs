---
title: "Sensor Component"
linkTitle: "Sensor"
weight: 70
draft: false
type: "docs"
description: "Explanation of sensor configuration and usage in Viam."
tags: ["sensor", "components"]
icon: "img/components/sensor.png"
# SME: #team-bucket
---
This page explains how to set up a generic sensor component with Viam.
Viam has a few types of sensor implemented including an ultrasonic sensor, temperature sensors and more, but this doc covers setting up a custom sensor so you can build a robot using almost any sort of sensor.

{{% alert title="Note" color="note" %}}

Viam has a separate, more specific component type called [movement sensor](/components/movement-sensor/) specifically for Global Positioning System (GPS) units, inertial measurement units (IMUs), and other sensors that detect position, velocity, and acceleration.

Viam also has an [encoder component](/components/encoder/) that is distinct from sensor.

{{% /alert %}}

## Hardware requirements

* Some sort of sensor, such as an ultrasonic sensor or temperature sensor
* A [board](/components/board/)
* Depending on your sensor's output, an analog to digital converter may be necessary to allow the sensor to communicate with the board.

## Wiring

The wiring for your sensor depends on the specific sensor you are using.
Refer to the sensor’s data sheet for wiring details.

## Viam configuration

To create a custom sensor, you must create a set of attributes unique to that sensor model:

| Key     | Description                                                |
| ------- | ---------------------------------------------------------- |
| `name`  | The name that you use to refer to the sensor in your code. |
| `type`  | For a sensor, the type is `sensor`.                        |
| `model` | The name you gave your custom sensor model                 |

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

The following example configures an ultrasonic sensor component for a robot called `ultra1`.
Once configured, the code connects to the robot and reads values from the configured sensor:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.sensor import Sensor

robot = await connect()
sensor = Sensor.from_robot(robot, "mySensorName")
readings = await sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
"go.viam.com/rdk/components/sensor"
)

ultra, err := sensor.FromRobot(robot, "ultra1")
readings, err := ultra.Readings(context.Background())
```

{{% /tab %}}
{{< /tabs >}}
