---
title: "Encoder Component"
linkTitle: "Encoder"
childTitleEndOverwrite: "Encoder Component"
weight: 50
type: "docs"
description: "A special type of sensor that measures rotation of a motor or joint."
tags: ["encoder", "components"]
icon: "/icons/components/encoder.svg"
images: ["/icons/components/encoder.svg"]
no_list: true
# SME: Rand
---

An encoder is a type of sensor that can detect speed and direction of rotation of a motor or a joint.
It is often used in conjunction with a motor, and is sometimes even built into a motor.
An encoder could also be mounted on a passive joint or other rotating object to keep track of the joint angle.

The encoder component supports:

- [Incremental encoders](https://en.wikipedia.org/wiki/Incremental_encoder#Quadrature_outputs), which can measure the speed and direction of rotation in relation to a given reference point like a starting point.
  These encoders output two phases.
  Based on the sequence and timing of these phases, it is determined how far something has turned and in which direction.
  Each phase output goes to a different pin on the board.
- Single phase or single pin "pulse output" encoders, which measure the position relative to the starting position but not the direction.
- Absolute encoders, which provide the absolute position of a rotating shaft, without requiring a reference point.

Most robots with an encoder need at least the following hardware:

- A [board component](/components/board/) that can run a `viam-server` instance.
  For example, a Raspberry Pi, or another model of single-board computer with GPIO (general purpose input/output) pins.
- Some sort of rotary robot part (like a motor, joint or dial) for which you want to measure movement.

## Supported Models

To use your encoder with Viam, check whether one of the following [built-in models](#built-in-models) supports your encoder.

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`AMS-AS5048`](ams-as5048/) | The `AMS-AS5048` encoder is an absolute encoder that which can connect using an I2C interface. |
| [`fake`](fake/) | An encoder model for testing. |
| [`incremental`](incremental/) | A two phase encoder, which can measure the speed and direction of rotation in relation to a given reference point. |
| [`single`](single/) | A single pin "pulse output" encoder which returns its relative position but no direction. |

<!-- No encoders yet -->
<!-- ### Modular Resources

{{<modular-resources api="rdk:component:encoder" type="encoder">}} -->

### Micro-RDK

If you are using the micro-RDK, navigate to [Micro-RDK Encoder](/micro-rdk/encoder/) for supported model information.

## Control your encoder with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have an encoder called `"my_encoder"` configured as a component of your robot.
If your encoder has a different name, change the `name` in the code.

Be sure to import the encoder package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.encoder import Encoder
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/encoder"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The encoder component supports the following methods:

{{< readfile "/static/include/components/apis/encoder.md" >}}

### GetPosition

Get the current position of the encoder in ticks or degrees.
Relative encoders return ticks since last zeroing.
Absolute encoders return degrees.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `position_type` [(Optional[PositionType.ValueType])](https://docs.python.org/library/typing.html#typing.Optional): Specify whether to get the current position in ticks (`encoder.PositionTypeTicks`) or in degrees (`encoder.PositionTypeDegrees`).
  If you are not sure which position type your encoder supports but it is a built-in Viam-supported model, you can leave this parameter unspecified (`encoder.PositionTypeUnspecified`) or empty and it will default to the correct position type.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Tuple[float, PositionType.ValueType])](https://docs.python.org/3/library/functions.html#float): The current position in ticks or degrees, and the type of position the encoder returns (ticks or degrees).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.get_position).

```python
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

# Get the position of the encoder in ticks
position = await my_encoder.get_position(encoder.PositionTypeTicks)
print("The encoder position is currently ", position[0], position[1])
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positionType` [(PositionType)](https://pkg.go.dev/go.viam.com/rdk/components/encoder#PositionType): Specify whether to get the current position in ticks (`encoder.PositionTypeTicks`) or in degrees (`encoder.PositionTypeDegrees`).
  If you are not sure which position type your encoder supports but it is a built-in Viam-supported model, you can leave this parameter unspecified (`encoder.PositionTypeUnspecified`) and it will default to the correct position type.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The current position in ticks or degrees.
- [(PositionType)](https://pkg.go.dev/go.viam.com/rdk/components/encoder#PositionType): The type of position the encoder returns (ticks or degrees).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Encoder).

```go
myEncoder, err := encoder.FromRobot(robot, "my_encoder")
if err != nil {
  logger.Fatalf("cannot get encoder: %v", err)
}

// Get the position of the encoder in ticks
position, posType, err := myEncoder.Position(context.Background(), encoder.PositionTypeTicks, nil)
```

{{% /tab %}}
{{< /tabs >}}

### ResetPosition

Set the current position of the encoder to be the new zero position.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.reset_position).

```python
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

# Reset the zero position of the encoder.
await my_encoder.reset_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Encoder).

```go
myEncoder, err := encoder.FromRobot(robot, "my_encoder")
if err != nil {
  logger.Fatalf("cannot get encoder: %v", err)
}

err := myEncoder.ResetPosition(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get a list of all the position types that are supported by a given encoder.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Properties)](https://python.viam.dev/autoapi/viam/components/encoder/encoder/index.html#viam.components.encoder.encoder.Encoder.Properties): The position types supported by the encoder model.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/index.html#viam.components.encoder.Encoder.get_properties).

```python
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

# Get whether the encoder returns position in ticks or degrees.
properties = await my_encoder.get_properties()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(map[Feature]bool)](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Feature): The position types supported by the encoder model.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/encoder#Encoder).

```go
myEncoder, err := encoder.FromRobot(robot, "my_encoder")

// Get whether the encoder returns position in ticks or degrees.
properties, err := myEncoder.Properties(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
If you are implementing your own encoder as a [modular resource](/modular-resources/) and are adding features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_encoder = Encoder.from_robot(robot=robot, name='my_encoder')

reset_dict = {
  "command": "reset",
  "example_param": 30
}
do_response = await my_encoder.do_command(reset_dict)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/encoder/client/index.html#viam.components.encoder.client.EncoderClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myEncoder, err := encoder.FromRobot(robot, "my_encoder")

resp, err := myEncoder.DoCommand(ctx, map[string]interface{}{"command": "reset", "example_param": 30})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/main/resource/resource.go).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next Steps

{{< cards >}}
{{% card link="/tutorials/configure/scuttlebot" %}}
{{< /cards >}}
