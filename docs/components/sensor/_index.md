---
title: "Sensor Component"
linkTitle: "Sensor"
weight: 70
draft: false
type: "docs"
description: "A device that sends information about the outside world to the computer controlling a robot."
tags: ["sensor", "components"]
icon: "img/components/sensor.png"
# SME: #team-bucket
---

A *sensor* is a device that can measure information about the outside world.
Adding a sensor component to your robot allows the information the sensor measures to be sent to the computer controlling the robot.

Most robots with a sensor need at least the following hardware:

- A [board](/components/board/)
- Depending on your sensor's output type (analog or digital), an analog to digital converter (ADC) may be necessary to allow the sensor to communicate with the board.

## Configuration

Supported sensor models include:

| Model | Description |
| ----- | ----------- |
| [`fake`](fake) | A model used for testing, with no physical hardware. |
| [`ultrasonic`](ultrasonic) | [An HC-S204 ultrasonic distance sensor](https://www.sparkfun.com/products/15569) |
| [`bme280`](bme280) | [BME280 environmental sensor](https://www.adafruit.com/product/2652) |
| [`ds18b20`](ds18b20) | [DS18B20 digital temperature sensor](https://www.adafruit.com/product/381) |
| [`power_ina219`](power_ina219) | [INA219 current sensor](https://www.amazon.com/dp/B07QJW6L4C) |
| [`renogy`](renogy)| [Renogy solar charge controller with temperature sensor](https://www.amazon.com/Renogy-Battery-Temperature-Sensor-Controllers/dp/B07WMMJFWY) |
| [`sensirion-sht3xd`](sensirion-sht3xd) | [Sensirion's SHT3x-DIS temperature and humidity sensor](https://www.adafruit.com/product/2857) |

Want to use another model of sensor to build your robot?
You can easily use another model of sensor for building your robot with Viam by defining your own model of [sensor](https://github.com/viamrobotics/rdk/blob/main/components/sensor/sensor.go).
Follow [these instructions](create-custom) to define a custom sensor model.

{{% alert title="Note" color="note" %}}

Viam has a separate, more specific component type called [movement sensor](/components/movement-sensor/) specifically for Global Positioning System (GPS) units, inertial measurement units (IMUs), and other sensors that detect position, velocity, and acceleration.

Viam also has an [encoder component](/components/encoder/) that is distinct from sensor.

{{% /alert %}}

## Control your sensor with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **CODE SAMPLE** tab, select your preferred programming language, and copy the sample code generated.
When executed, this sample code will create a connection to your robot as a client.
Then, adding API method calls into the code, as shown in the examples below, will allow you to control your robot programmatically.

These examples assumes you have a sensor called "my_sensor" configured as a component of your robot.
If your sensor has a different name, change the `name` in the code.

## API

The sensor component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
[Readings](#readings) | Get the measurements or readings that this sensor provides. |
<!-- | [DoCommand](#docommand) | Sends or receives model-specific commands. |  -->

### Readings

Get the measurements or readings that this sensor provides.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `readings` [(Mapping[str, Any])](https://docs.python.org/3/library/typing.html#typing.Mapping): The measurements or readings that this sensor provides.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/sensor/index.html#viam.components.sensor.Sensor.get_readings).

```python
my_sensor = Sensor.from_robot(robot=robot, name='my_sensor')

# Get the readings provided by the sensor.
positions = await my_sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `readings` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): The measurements or readings that this sensor provides.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/sensor#Sensor).

```go
mySensor, err := sensor.FromRobot(robot, "sensor")
if err != nil {
  logger.Fatalf("cannot get sensor: %v", err)
}

readings, err := mySensor.Readings(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
