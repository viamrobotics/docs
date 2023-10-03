---
title: "Power Sensor Component"
linkTitle: "Power Sensor"
childTitleEndOverwrite: "Power Sensor"
weight: 70
no_list: true
type: "docs"
description: "A device that provides information about a robot's power systems, including voltage, current, and power consumption."
tags: ["sensor", "components", "power sensor", "ina219", "ina226", "renogy"]
icon: "/icons/components/power-sensor.svg"
images: ["/icons/components/power-sensor.svg"]
# SME: #team-bucket
---

A power sensor is a device that reports measurements of the voltage, current and power consumption in your robot's system.
Integrate this component to monitor your power levels.

## Supported Models

To use your power sensor with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your power sensor.

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Built-in models

For configuration information, click on the model name:

| Model                 | Description <a name="model-table"></a>         |
| --------------------- | ---------------------------------------------- |
| [`fake`](./fake/)     | a digital power sensor for testing             |
| [`ina219`](./ina219/) | INA219 power sensor; current and power monitor |
| [`ina226`](./ina226/) | INA226 power sensor; current and power monitor |
| [`renogy`](./renogy/) | solar charge controller                        |

### Modular Resources

{{<modular-resources api="rdk:component:power_sensor" type="power_sensor">}}

## Control your power sensor with Viam’s client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your robot as a client.
Once connected, you can control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have a power sensor called `"my_power_sensor"` configured as a component of your robot.
If your power sensor has a different name, change the `name` in the code.

Import the power sensor package for the SDK you are using:
{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.powersensor import powersensor
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/powersensor"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The power sensor component supports the following methods:

{{< readfile "/static/include/components/apis/power-sensor.md" >}}

### GetCurrent

Return the current of a specified device and whether it is AC or DC.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str,Any]])](https://docs.python.org/library/typing.html#typing.Optional): Pass additional data and configuration options to the {{< glossary_tooltip term_id="grpc" text="RPC call" >}}.
- `timeout` [(Optional[float])](https://docs.python.org/3/library/typing.html#typing.Optional): Specify a time limit in seconds for how long `get_current` should wait for a response.

**Returns:**

- [(Tuple[float, bool])](https://docs.python.org/3/library/functions.html#float): A tuple which includes a float representing the current reading in amps, and a bool indicating whether the current is AC (`true`) or DC (`false`).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/power_sensor/index.html#viam.components.power_sensor.power_sensor.PowerSensor.get_current).

```python
# Get the current reading from the power sensor
current, is_ac = await my_power_sensor.get_current()
print("The current is ", current, " A, Is AC: ", is_ac)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [Context](https://pkg.go.dev/context): Control the lifecycle of the operation by handling timeouts and managing cancellations.
- `extra`[(Optional[Dict[str, Any]])](https://docs.python.org/3/library/typing.html#typing.Optional): Pass additional data and configuration options to the [RPC call](/appendix/glossary/#term-grpc).

**Returns:**

- `float64`: The measurement of the current, represented as a 64-bit float number.
- `bool`: Indicate whether current is AC (`true`) or DC (`false`).
- `error`: Report any errors that might occur during operation.
  For a successful operation, `error` returns `nil`.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#PowerSensor).

```go
// Create a power sensor instance
myPowerSensor, err := powersensor.FromRobot(robot, "my_power_sensor")
if err != nil {
  logger.Fatalf("cannot get power sensor: %v", err)
}

// Get the current reading from device in amps
current, isAC, err := myPowerSensor.Current(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetVoltage

Return the voltage reading of a specified device and whether it is AC or DC.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra`[(Optional[Dict[str, Any]])](https://docs.python.org/3/library/typing.html#typing.Optional): Pass additional data and configuration options to the [RPC call](/appendix/glossary/#term-grpc).
- `timeout`[(Optional[float])](https://docs.python.org/3/library/functions.html#float): Specify a time limit in seconds for how long `get_voltage` should wait for a response.

**Returns:**

- [(Tuple[float, bool])](https://docs.python.org/3/library/stdtypes.html): A float representing the current reading in amps. A bool indicating whether the voltage is AC (`true`) or DC (`false`).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/power_sensor/index.html#viam.components.power_sensor.power_sensor.PowerSensor.get_voltage).

```Python
# Get the voltage reading from the power sensor
    voltage, is_ac = await my_power_sensor.get_voltage()
    print("The voltage is", voltage, "V, Is AC:", is_ac)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [Context](https://pkg.go.dev/context): Control the lifecycle of the operation by handling timeouts and managing cancellations.
- `extra`[(Optional[Dict[str, Any]])](https://docs.python.org/3/library/typing.html#typing.Optional): Pass additional data and configuration options to the [RPC call](/appendix/glossary/#term-grpc).

**Returns:**

- `float64`: The measurement of the voltage, represented as a 64-bit float number.
- `bool`: Indicate whether voltage is AC (`true`) or DC (`false`).
- `error`: Report any errors that might occur during operation.
  For a successful operation, `error` returns `nil`.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#PowerSensor).

```Go
// Create a power sensor instance
myPowerSensor, err := powersensor.FromRobot(robot, "my_power_sensor")
if err != nil {
  logger.Fatalf("cannot get power sensor: %v", err)
}

// Get the voltage from device in volts
voltage, isAC, err := myPowerSensor.Voltage(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetPower

Return the power reading in watts.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra`[(Optional[Dict[str, Any]])](https://docs.python.org/3/library/typing.html#typing.Optional): Pass additional data and configuration options to the [RPC call](/appendix/glossary/#term-grpc).
- `timeout`[(Optional[float])](https://docs.python.org/3/library/functions.html#float): Specify a time limit in seconds for how long `get_power` should wait for a response.

**Returns:**

- `float`: The measurement of the power, represented as a float.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/power_sensor/index.html#viam.components.power_sensor.power_sensor.PowerSensor.get_power).

```Python
# Get the power reading from the power sensor
    power = await my_power_sensor.get_power()
    print("The power is", power, "Watts")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [Context](https://pkg.go.dev/context): Control the lifecycle of the operation by handling timeouts and managing cancellations.
- `extra`[(Optional[Dict[str, Any]])](https://docs.python.org/3/library/typing.html#typing.Optional): Pass additional data and configuration options to the [RPC call](/appendix/glossary/#term-grpc).

**Returns:**

- `float64`: The measurement of the power, represented as a 64-bit float number.
- `error`: Report any errors that might occur during operation.
  For a successful operation, `error` returns `nil`.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#PowerSensor).

```Go
// Create a power sensor instance
myPowerSensor, err := powersensor.FromRobot(robot, "my_power_sensor")
if err != nil {
  logger.Fatalf("cannot get power sensor: %v", err)
}

// Get the power measurement from device in watts
power, err := myPowerSensor.Power(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetReadings

Get the measurements or readings that this power sensor provides.
If a sensor is not configured to have a measurement or fails to read a piece of data, it will not appear in the readings dictionary.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping\[str, Any\])](https://docs.python.org/3/library/typing.html#typing.Mapping): The measurements or readings that this power sensor provides.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_readings).

```python
my_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

# Get the readings provided by the sensor.
readings = await my_sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): The measurements or readings that this sensor provides.
- [(error)](https://pkg.go.dev/builtin#error): Report any errors that might occur during operation.
  For a successful operation, `error` returns `nil`.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#Readings).

```go
myPowerSensor, err := powersensor.FromRobot(robot, "my_power_sensor")

// Get the readings provided by the sensor.
readings, err := myPowerSensor.Readings(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetReadings

Get the measurements or readings that this power sensor provides.
If a sensor is not configured to have a measurement or fails to read a piece of data, it will not appear in the readings dictionary.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping\[str, Any\])](https://docs.python.org/3/library/typing.html#typing.Mapping): The measurements or readings that this power sensor provides.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_readings).

```python
my_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

# Get the readings provided by the sensor.
readings = await my_sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): The measurements or readings that this sensor provides.
- [(error)](https://pkg.go.dev/builtin#error): Report any errors that might occur during operation.
  For a successful operation, `error` returns `nil`.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/powersensor#Readings).

```go
myPowerSensor, err := powersensor.FromRobot(robot, "my_power_sensor")

// Get the readings provided by the sensor.
readings, err := myPowerSensor.Readings(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

## Related Services

{{< cards >}}
{{% card link="/services/data/" class="small" %}}
{{</ cards >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
