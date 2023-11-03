---
title: "Sensors Service"
linkTitle: "Sensors"
weight: 70
type: "docs"
description: "The sensors service provides a central interface for all of your robot's sensors."
tags: ["sensor", "services"]
icon: "/services/icons/sensor.svg"
images: ["/services/icons/sensor.svg"]
# SME: Cheuk
---

The sensors service is a built-in service that provides a central interface to all of your robot's [sensors](/components/sensor/), regardless of the sensor model.
With it you can obtain readings from multiple sensors on your robot at once.

## Required Components

{{< cards >}}
{{< relatedcard link="/components/board/" >}}
{{< relatedcard link="/components/sensor/" >}}
{{< /cards >}}

## API

The sensors service supports the following methods:

{{< readfile "/static/include/services/apis/sensors.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### GetSensors

Returns a list containing the `name` of each available sensor.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.

**Returns:**

- (List[[ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)]): Names of the available sensors of the robot.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/sensors/index.html#viam.services.sensors.SensorsClient.get_sensors).

```python {class="line-numbers linkable-line-numbers"}
# Access the sensors service
sensors_svc = SensorsClient.from_robot(robot=robot, name="builtin")

# Get available sensors
sensors = await sensors_svc.get_sensors()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): An array of sensor names.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/sensors#Service).

```go {class="line-numbers linkable-line-numbers"}
// Access the sensors service
sensorsService, err := sensors.FromRobot(robot, "builtin")
if err != nil {
  logger.Fatal(err)
}

// Get available sensors
sensor_names, err := sensorsService.Sensors(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetReadings

Returns a list of sensor readings from a given list of sensors.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `sensors` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): An array of sensor names for which to return readings.

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.

**Returns:**

- ([Mapping[[ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName), Any]]): A list of readings from the requested sensors.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/sensors/index.html#viam.services.sensors.SensorsClient.get_readings).

```python {class="line-numbers linkable-line-numbers"}
# Access the sensors service
sensors_svc = SensorsClient.from_robot(robot=robot, name="builtin")

# Get available sensors
sensors = await sensors_svc.get_sensors()
# Get readings for sensors
readings = await sensors_svc.get_readings(sensors)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

- `sensorNames` [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): An array of sensor names for which to return readings.

- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]Readings)](https://pkg.go.dev/go.viam.com/rdk/services/sensors#Readings): A list of readings from the requested sensors.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/sensors#Service).

```go {class="line-numbers linkable-line-numbers"}
// Access the sensors service
sensorsService, err := sensors.FromRobot(robot, "builtin")
if err != nil {
  logger.Fatal(err)
}

// Get readings from all available sensors
sensor_names, err := sensorsService.Sensors(context.Background(), nil)
readings, err := sensorsService.Readings(context.Background(), sensor_names, nil)
```

{{% /tab %}}
{{< /tabs >}}

## DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own sensors service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/sensors/client/index.html#viam.services.sensors.client.SensorsClient.do_command).

```python {class="line-numbers linkable-line-numbers"}
# Access the sensors service
sensors_svc = SensorsClient.from_robot(robot=robot, name="builtin")

my_command = {
  "command": "dosomething",
  "someparameter": 52
}

await sensors_svc.do_command(my_command)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map\[string\]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
// Access the sensors service
sensorsService, err := sensors.FromRobot(robot, "builtin")
if err != nil {
  logger.Fatal(err)
}

resp, err := sensorsService.DoCommand(ctx, map[string]interface{}{"command": "dosomething", "someparameter": 52})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## Next steps

{{< cards >}}
{{% card link="/tutorials/projects/tipsy/" %}}
{{< /cards >}}
