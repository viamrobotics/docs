---
title: "Power Sensor Component"
linkTitle: "Power Sensor"
childTitleEndOverwrite: "Power Sensor"
weight: 70
no_list: true
type: "docs"
description: "A device that provides information about a machine's power systems, including voltage, current, and power consumption."
tags: ["sensor", "components", "power sensor", "ina219", "ina226", "renogy"]
icon: true
images: ["/icons/components/power-sensor.svg"]
modulescript: true
aliases:
  - "/components/power-sensor/"
# SME: #team-bucket
---

A power sensor is a device that reports measurements of the voltage, current, and power consumption in your machine's system.
Integrate this component to monitor your power levels.

## Related services

{{< cards >}}
{{< relatedcard link="/data/" >}}
{{< /cards >}}

## Supported models

To use your power sensor with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your power sensor.

### Built-in models

For configuration information, click on the model name:

| Model                 | Description <a name="model-table"></a>         |
| --------------------- | ---------------------------------------------- |
| [`fake`](./fake/)     | a digital power sensor for testing             |
| [`ina219`](./ina219/) | INA219 power sensor; current and power monitor |
| [`ina226`](./ina226/) | INA226 power sensor; current and power monitor |
| [`renogy`](./renogy/) | solar charge controller                        |

### Modular resources

{{<modular-resources api="rdk:component:power_sensor" type="power_sensor">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Control your power sensor with Viam’s client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Once connected, you can control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a power sensor called `"my_power_sensor"` configured as a component of your machine.
If your power sensor has a different name, change the `name` in the code.

Import the power sensor package for the SDK you are using:
{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.power_sensor import PowerSensor
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
my_power_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

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
my_power_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

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
my_power_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

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
my_power_sensor = PowerSensor.from_robot(robot=robot, name='my_power_sensor')

# Get the readings provided by the sensor.
readings = await my_power_sensor.get_readings()
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

### GetGeometries

Get all the geometries associated with the power sensor in its current configuration, in the [frame](/mobility/frame-system/) of the power sensor.
The [motion](/mobility/motion/) and [navigation](/mobility/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[Geometry])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry): The geometries associated with the power sensor, in any order.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.get_geometries).

```python {class="line-numbers linkable-line-numbers"}
my_power_sensor = PowerSensor.from_robot(robot=robot, name="my_power_sensor")

geometries = await my_power_sensor.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

{{% /tab %}}

<!-- Go tab

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [`[]spatialmath.Geometry`](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): The geometries associated with the power sensor, in any order.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Shaped).

```go {class="line-numbers linkable-line-numbers"}
myPowerSensor, err := powersensor.FromRobot(robot, "my_power_sensor")

geometries, err := myPowerSensor.Geometries(context.Background(), nil)

if len(geometries) > 0 {
    // Get the center of the first geometry
    elem := geometries[0]
    fmt.Println("Pose of the first geometry's center point:", elem.center)
}
```

 -->

{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
If you are implementing your own power sensor and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_power_sensor = PowerSensor.from_robot(robot=robot, name="my_power_sensor")

reset_dict = {
  "command": "reset",
  "example_param": 30
}

do_response = await my_power_sensor.do_command(reset_dict)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myPowerSensor, err := powersensor.FromRobot(robot, "my_power_sensor")

resp, err := myPowerSensor.DoCommand(ctx, map[string]interface{}{"command": "reset", "example_param": 30})
```

For more information, see the [Go SDK Code](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_power_sensor = PowerSensor.from_robot(robot, "my_power_sensor")

await my_power_sensor.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/power_sensor/client/index.html#viam.components.power_sensor.client.PowerSensorClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myPowerSensor, err := powersensor.FromRobot(robot, "my_power_sensor")

err := myPowerSensor.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
