---
title: "Create a Custom Sensor Model"
linkTitle: "custom model"
weight: 40
draft: false
type: "docs"
description: "Extend the sensor class to define a custom sensor model and build your robot with any type of sensor."
tags: ["sensor", "components"]
image: "/components/img/components/sensor.png"
imageAlt: "sensor"
# SME: #team-bucket
---

This page explains how to set up a generic sensor component with Viam.

Viam has a few types of sensor models built-in including an ultrasonic sensor, and certain temperature sensors, but you can implement any other model of sensor for building your robot with Viam by extending the [sensor class]() and defining your own model.

<!-- this doc covers setting up a custom sensor so you can build a robot using almost any sort of sensor. -->

{{% alert title="Note" color="note" %}}

Viam has a separate, more specific component type called [movement sensor](/components/movement-sensor/) specifically for Global Positioning System (GPS) units, inertial measurement units (IMUs), and other sensors that detect position, velocity, and acceleration.

Viam also has an [encoder component](/components/encoder/) that is distinct from sensor.

{{% /alert %}}

Most robots with a sensor need at least the following hardware:

- A [board](/components/board/)
- Depending on your sensor's output type (analog or digital), an analog to digital converter (ADC) may be necessary to allow the sensor to communicate with the board.

## Configuration

To create a custom sensor, you must create a set of attributes unique to that sensor model:

| Key     | Description                                                  |
| ------- | ----------------------------------------------------------   |
| `name`  | The name that you use to refer to the sensor in your code.   |
| `type`  | For a sensor, the type is `sensor`.                          |
| `model` | The model of sensor used (for example, "ultrasonic"). Either a built-in Viam model or one you define when implementing a custom sensor model. |

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

## Control your sensor with Viam's client SDK libraries

The following example connects to and gets readings from an ultrasonic sensor component named `mySensorName`:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.components.sensor import Sensor

robot = await connect()
sensor = Sensor.from_robot(robot, "mySensorName")
readings = await sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
    "context"
    "github.com/edaniels/golog"
    "go.viam.com/rdk/components/sensor"
)

func main() {
    // Connect to your robot.
    robot, err := client.New(
        context.Background(),
        "ADD YOUR ROBOT ADDRESS HERE. You can find this on the Code Sample tab of app.viam.com.",
        logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "ADD YOUR LOCATION SECRET HERE. You can find this on the Code Sample tab of app.viam.com.",
      })),
  )

    ultra, err := sensor.FromRobot(robot, "ultra1")
    readings, err := ultra.Readings(context.Background())
 }
```

{{% /tab %}}
{{< /tabs >}}

You can read more about sensor implementation in the [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/sensor/index.html) or the [Go SDK Documentation](https://pkg.go.dev/go.viam.com/rdk).
