---
title: "Template Component"
linkTitle: "Template"
childTitleEndOverwrite: "Template Component"
weight: 10
type: "docs"
description: "A NAME is a ... description of what the component is."
tags: ["camera", "components"]
icon: true # this should be used when the image is an icon, it will adjust the sizing and object-fit
images: ["/icons/components.png"]
draft: true
no_list: true
modulescript: true
# SMEs:
---

{{<imgproc src="/icons/components.png" resize="400x" declaredimensions=true alt="ALT" class="alignright">}}

Brief description of the component and what you can do with it.

Use cases (optional):

- A brief description of one sample use case.
- ...

Most machines with a COMPONENT need at least the following hardware (optional):

- Board
- ...

## Related services

Add services commonly used with the component.

{{< cards >}}
{{< relatedcard link="/data/" >}}
{{< relatedcard link="/mobility/frame-system/" >}}
{{< /cards >}}

## Supported models

{{<resources api="rdk:component:component" type="component">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Control your board with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **CONNECT** tab's **Code sample** page, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by getting your `COMPONENT` component from the machine with `FromRobot` and adding API method calls, as shown in the following examples.

These examples assume you have a board called "my_board" configured as a component of your machine.
If your board has a different name, change the `name` in the code.

Be sure to import the COMPONENT package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.componentname import ComponentName
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/componentname"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The COMPONENT component supports the following methods:

_Writing Instructions: Use the method names in the [protobuf](https://github.com/viamrobotics/api/blob/main/component/board/v1/board_grpc.pb.go), not the Python or Go-specific method names._
_Use an included snippet so you can add it to <file>/program/apis/</file>._

{{< readfile "/static/include/components/apis/component.md" >}}

### GetReadings

Get the measurements or readings that this sensor provides.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `readings` [(Mapping\[str, Any\])](https://docs.python.org/3/library/typing.html#typing.Mapping): The measurements or readings that this sensor provides.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/sensor/index.html#viam.components.sensor.Sensor.get_readings) (INSERT RELEVANT LINK).

```python
my_sensor = Sensor.from_robot(robot=robot, name='my_sensor')

# Get the readings provided by the sensor.
readings = await my_sensor.get_readings()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- `readings` [(map\[string\]interface{})](https://go.dev/blog/maps): The measurements or readings that this sensor provides.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/sensor#Sensor).

```go
mySensor, err := sensor.FromRobot(robot, "my_sensor")
if err != nil {
  logger.Fatalf("cannot get sensor: %v", err)
}

readings, err := mySensor.Readings(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### MethodName2

1-2 sentence description of what the method does.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/sensor/index.html#viam.components.sensor.Sensor.get_readings) (INSERT RELEVANT LINK).

```python
my_sensor = Sensor.from_robot(robot=robot, name='my_sensor')

# Do the thing that the method does.
await my_sensor.method_name_two()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/sensor#Sensor).

```go
mySensor, err := sensor.FromRobot(robot, "my_sensor")
if err != nil {
  logger.Fatalf("cannot get sensor: %v", err)
}

err := mySensor.MethodNameTwo(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

Troubleshooting information for configuration errors.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

{{< cards >}}
{{< /cards >}}
