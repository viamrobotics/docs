---
title: "Gantry Component"
linkTitle: "Gantry"
childTitleEndOverwrite: "Gantry Component"
no_list: true
weight: 50
type: "docs"
description: "A mechanical system of linear rails that can precisely position an attached device."
tags: ["gantry", "components"]
icon: "/icons/components/gantry.svg"
images: ["/icons/components/gantry.svg"]
modulescript: true
aliases:
  - "/components/gantry/"
# SME: Rand
---

A robotic _gantry_ is a mechanical system of linear actuators used to hold and position an [end effector](https://en.wikipedia.org/wiki/Robot_end_effector).
A 3D printer is an example of a three-axis gantry where each linear actuator can move the print head along one axis.
The linear rail design makes gantries a common and reliable system for simple positioning and placement tasks.

This component abstracts the hardware of a gantry to give you an easy interface for coordinated control of linear actuators, even many at once [(multi-axis)](multi-axis/).

<div class="td-max-width-on-larger-screens text-center">
{{<imgproc src="/components/gantry/gantry-illustration.png" resize="300x" declaredimensions=true alt="Example of what a multi-axis robot gantry looks like as a black and white illustration of an XX YY mechanical gantry.">}}
</div>

Gantry components can only be controlled in terms of linear motion (you cannot rotate them).
Each gantry can only move in one axis within the limits of the length of the linear rail.

Most machines with a gantry need at least the following hardware:

- A [board](/components/board/) or [controller](/components/input-controller/) component that can detect changes in voltage on GPIO pins
- A [motor](/components/motor/) that can move linear rails
  - Encoded motor: See [DC motor with encoder](/components/motor/gpio/encoded-motor/) and [encoder component](/components/encoder/).
  - Stepper motor: See [Stepper motor](/components/motor/gpiostepper/).
    Requires setting limit switches in the config of the gantry, or setting offsets in the config of the stepper motor.
- Limit switches, to attach to the ends of the gantry's axis

## Related services

{{< cards >}}
{{< relatedcard link="/mobility/frame-system/" >}}
{{< relatedcard link="/mobility/motion/" >}}
{{< /cards >}}

## Supported models

To use your gantry with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your gantry.

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`fake`](fake/) | A model used for testing, with no physical hardware. |
| [`single-axis`](single-axis/) | A gantry with a singular linear rail. |
| [`multi-axis`](multi-axis/) | A gantry with multiple linear rails. Composed of multiple `single-axis` gantries. |

### Modular resources

{{<modular-resources api="rdk:component:gantry" type="gantry">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## Control your gantry with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your machine, go to your machine's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your machine as a client.
Then control your machine programmatically by adding API method calls as shown in the following examples.

These examples assume you have a gantry called `"my_gantry"` configured as a component of your machine.
If your gantry has a different name, change the `name` in the code.

Be sure to import the gantry package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.gantry import Gantry
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/gantry"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The gantry component supports the following methods:

{{< readfile "/static/include/components/apis/gantry.md" >}}

### GetPosition

Get the current positions of the axis of the gantry (mm).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List\[float\])](https://docs.python.org/3/library/typing.html#typing.List): A list of the position of the axes of the gantry in millimeters.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.get_position).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Get the current positions of the axes of the gantry in millimeters.
positions = await my_gantry.get_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]float64)](https://pkg.go.dev/builtin#float64): A list of the position of the axes of the gantry in millimeters.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")

// Get the current positions of the axes of the gantry in millimeters.
position, err := myGantry.Position(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### MoveToPosition

Move the axes of the gantry to the desired positions (mm) at the requested speeds (mm/sec).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `positions` [(List\[float\])](https://docs.python.org/3/library/typing.html#typing.List): A list of positions for the axes of the gantry to move to, in millimeters.
- `speeds` [(List\[float\])](https://docs.python.org/3/library/typing.html#typing.List): A list of speeds in millimeters per second for the gantry to move at respective to each axis.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.move_to_position).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Create a list of positions for the axes of the gantry to move to. Assume in
# this example that the gantry is multi-axis, with 3 axes.
examplePositions = [1, 2, 3]

exampleSpeeds = [3, 9, 12]

# Move the axes of the gantry to the positions specified.
await my_gantry.move_to_position(
    positions=examplePositions, speeds=exampleSpeeds)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positions` [([]float64)](https://pkg.go.dev/builtin#float64): A list of positions for the axes of the gantry to move to, in millimeters.
- `speeds` [([]float64)](https://pkg.go.dev/builtin#float64): A list of speeds in millimeters per second for the gantry to move at respective to each axis.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")

// Create a list of positions for the axes of the gantry to move to. Assume in this example that the gantry is multi-axis, with 3 axes.
examplePositions = []float64{1, 2, 3}

exampleSpeeds = []float64{3, 9, 12}

// Move the axes of the gantry to the positions specified.
myGantry.MoveToPosition(context.Background(), examplePositions, exampleSpeeds, nil)
```

{{% /tab %}}
{{< /tabs >}}

### Home

Run the homing sequence of the gantry to re-calibrate the axes with respect to the limit switches.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(boolean)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): Whether the gantry has run the homing sequence successfully.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.move_to_position).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

await my_gantry.home()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): Whether the gantry has run the homing sequence successfully.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")

myGantry.Home(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetLengths

Get the lengths of the axes of the gantry (mm).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List\[float\])](https://docs.python.org/3/library/typing.html#typing.List): A list of the lengths of the axes of the gantry in millimeters.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.get_lengths).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Get the lengths of the axes of the gantry in millimeters.
lengths_mm = await my_gantry.get_lengths()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]float64)](https://pkg.go.dev/builtin#float64): A list of the lengths of the axes of the gantry in millimeters.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")

// Get the lengths of the axes of the gantry in millimeters.
lengths_mm, err := myGantry.Lengths(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop all motion of the gantry.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.stop).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Stop all motion of the gantry. It is assumed that the gantry stops
# immediately.
await my_gantry.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")

// Stop all motion of the gantry. It is assumed that the gantry stops immediately.
myGantry.Stop(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### IsMoving

Get if the gantry is currently moving.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If it is true or false that the gantry is currently moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.is_moving).

```python
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

# Stop all motion of the gantry. It is assumed that the
# gantry stops immediately.
await my_gantry.stop()

# Print if the gantry is currently moving.
print(my_gantry.is_moving())
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): If it is true or false that the gantry is currently moving.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")

// Stop all motion of the gantry. It is assumed that the gantry stops immediately.
myGantry.Stop(context.Background(), nil)

// Log if the gantry is currently moving.
is_moving, err := myGantry.IsMoving(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the gantry in its current configuration, in the [frame](/mobility/frame-system/) of the gantry.
The [motion](/mobility/motion/) and [navigation](/mobility/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[Geometry])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry): The geometries associated with the gantry, in any order.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.get_geometries).

```python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

geometries = await my_gantry.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

{{% /tab %}}

<!-- Go tab

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [`[]spatialmath.Geometry`](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): The geometries associated with the gantry, in any order.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Shaped).

```go {class="line-numbers linkable-line-numbers"}
myGantry, err := gantry.FromRobot(robot, "my_gantry")

geometries, err := myGantry.Geometries(context.Background(), nil)

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
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own gantry and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot, "my_gantry")

command = {"cmd": "test", "data1": 500}
result = my_gantry.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myGantry, err := gantry.FromRobot(robot, "my_gantry")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myGantry.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/main/resource/resource.go).

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
my_gantry = Gantry.from_robot(robot, "my_gantry")

await my_gantry.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myGantry, err := gantry.FromRobot(robot, "my_gantry")

err := myGantry.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
