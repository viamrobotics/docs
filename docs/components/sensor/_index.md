---
title: "Sensor Component"
linkTitle: "Sensor"
weight: 70
no_list: true
type: "docs"
description: "A device that sends information about the outside world to the computer controlling a robot."
tags: ["sensor", "components"]
icon: "/components/img/components/sensor.svg"
images: ["/components/img/components/sensor.svg"]
# SME: #team-bucket
---

A *sensor* is a device that can measure information about the outside world.
Add a sensor component to your robot to send the information the sensor measures to the computer controlling the robot.

{{% alert title="Note" color="note" %}}

Viam has two component types defined separately from *sensor* that you can use to implement sensors with specific functions:

1. [Movement sensors](/components/movement-sensor/) for Global Positioning System (GPS) units, inertial measurement units (IMUs), and other sensors that detect position, velocity, and acceleration.
2. [Encoders](/components/encoder/) for sensors that can detect speed and direction of rotation of a motor or a joint.

{{% /alert %}}

Most robots with a sensor need at least the following hardware:

- A [board](/components/board/)
- Depending on your sensor's output type (analog or digital), an analog-to-digital converter (ADC) may be necessary to allow the sensor to communicate with the board

## Configuration

Supported sensor models include:

| Model | Description |
| ----- | ----------- |
| [`fake`](fake) | A model used for testing, with no physical hardware. |
| [`ultrasonic`](ultrasonic) | [HC-S204 ultrasonic distance sensor](https://www.sparkfun.com/products/15569) |
| [`bme280`](bme280) | [BME280 environmental sensor](https://www.adafruit.com/product/2652) |
| [`ds18b20`](ds18b20) | [DallasTemperature DS18B20 digital temperature sensor](https://www.adafruit.com/product/381) |
| [`power_ina219`](power_ina219) | [INA219 current sensor](https://www.amazon.com/dp/B07QJW6L4C) |
| [`renogy`](renogy)| [Renogy battery temperature sensor](https://www.amazon.com/Renogy-Battery-Temperature-Sensor-Controllers/dp/B07WMMJFWY) |
| [`sensirion-sht3xd`](sensirion-sht3xd) | [Sensirion SHT3x-DIS temperature and humidity sensor](https://www.adafruit.com/product/2857) |

You can implement a model of sensor that is not natively supported by Viam by [creating and registering your own model of a sensor](/program/extend/modular-resources/).
This allows you to have the same access and control of the sensor through Viam as you would if it was a built-in model.

For an example of creating a custom component, see a [WiFi strength sensor built with the Viam Go SDK](https://github.com/viam-labs/wifi-sensor/blob/main/linuxwifi/linuxwifi.go) or [custom resource types implemented with the Viam Python SDK](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/module).

## Control your sensor with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code Sample** tab, select your preferred programming language, and copy the sample code generated.

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have a sensor called `"my_sensor"` configured as a component of your robot.
If your sensor has a different name, change the `name` in the code.

## API

The sensor component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [Readings](#readings) | Get the measurements or readings that this sensor provides. |

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
readings = await my_sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `readings` [(map[string]interface{})](https://go.dev/blog/maps): The measurements or readings that this sensor provides.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/sensor#Sensor).

```go
mySensor, err := sensor.FromRobot(robot, "my_sensor")

// Get the readings provided by the sensor.
readings, err := mySensor.Readings(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
