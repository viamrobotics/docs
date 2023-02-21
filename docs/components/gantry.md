---
title: "Gantry Component"
linkTitle: "Gantry"
draft: false
weight: 50
type: "docs"
description: "A mechanical system of linear rails that can precisely position an attached device."
tags: ["gantry", "components"]
icon: "img/components/gantry.png"
# SME: Rand
---

A *gantry* on a robot is a mechanical system made up of one or more linear rails that can hold and position a variety of end-effectors: devices designed to attach to the robot and interact with the environment to perform tasks.
The linear rail design makes gantries a common design on robots for simple positioning and placement.
A customized encoded motor controller can be used in the configuration of a gantry to move the linear rail.

This component abstracts the hardware of a gantry to give you an easy interface for moving linear rails, even many at once (multi-axis).
A multi-axis gantry is composed of many single-axis gantries.

<img src="../img/gantry/gantry-illustration.png" alt="Example of what a multi-axis robot gantry looks like as a black and white illustration of an XX YY mechanical gantry." style="max-width:300px; display: block; margin: 0 auto"></img>

Gantry components can only be controlled in terms of linear motion.
Each gantry can only move in one axis within the limits of the length of the linear rail.

Most robots with a gantry need at least the following hardware:

- A [board component](/components/board/) or controller that can detect changes in voltage on GPIO pins.
- A [motor](/components/motor/) that can move linear rails.
  - Encoded motor: See [DC motor with encoder](/components/motor/#dc-motor-with-encoder) and [encoder component](/components/encoder/).
  - Stepper motor: See [Stepper motor](/components/motor/#stepper-motor).
  Requires setting limit switches in the config of the gantry, or setting offsets in the config of the stepper motor.
- Limit switches, to attach to the ends of the gantry's axis

### Configuration

Configuring this component on your robot with a gantry enables you to get and change the position of the linear rail axes.
You can configure your robot, as shown below, on the [Viam app](https://app.viam.com).

#### One-Axis

This is how you configure a one-axis gantry:

{{< tabs name="Example Gantry Config One-Axis" >}}
{{< tab name="Config Builder" >}}

<img src="../img/gantry/gantry-config-ui-oneaxis.png" alt="Example of what configuration for a one-axis gantry component looks like in the Viam App config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam
{
  "components": [
    {
      "depends_on": [],
      "name": <your_gantry_name>,
      "type": "gantry",
      "model": "oneaxis",
      "attributes": {
        "board": <your_board_name>,
        "motor": <your_motor_name>,
        "gantry_rpm": 500,
        "limit_pins": [
          <your_lim_1>,
          <your_lim_2>
        ],
        "limit_pin_enabled_high": false,
        "length_mm": 800,
        "axis": {
          "Z": 0,
          "X": 1,
          "Y": 0
        }
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `board`  |  Optional | The name of the board that is connected to the limit switches and pins. If limit pins exist, board is required. |
| `motor` | *Required* | The name of the motor that moves the gantry. |
| `limit_pins`  | Optional | The pins attached to the limit switches on either end. If motor type is not encoded, limit_pins is required. |
| `limit_pin_enabled_high` | Optional | If it is true or false that the limit pins are enabled. Default is false. |
| `length_mm` | *Required* | The length of the axis of the gantry in mm. |
| `mm_per_rev` | Optional | How far the gantry moves (linear, distance in mm) per one revolution of the motor’s output shaft. This typically corresponds to Distance = PulleyDiameter*pi, or the pitch of a linear screw. |
| `gantry_rpm` | Optional | The gantry motor's default rpm. |
| `axis` | *Required* | The axis in which the gantry is allowed to move (x, y, z). |

#### Multi-Axis

A multi-axis gantry component is made up of many single-axis gantries, with each referenced in configuration in the multi-axis models' attribute `subaxes_list`.

This is how you configure a multi-axis gantry:

{{< tabs name="Example Gantry Config Multi-Axis" >}}
{{< tab name="Config Builder" >}}

<img src="../img/gantry/gantry-config-ui-multiaxis.png" alt="Example of what configuration for a multi-axis gantry component looks like in the Viam App config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam
{
  "components": [
    {
      "name": <your_multiaxis_gantry_name>,
      "type": "gantry",
      "model": "multiaxis",
      "attributes": {
        "subaxes_list": [
          <your_oneaxis_gantry_name_1>,
          <your_oneaxis_gantry_name_2>,
          <your_oneaxis_gantry_name_3>
        ]
      },
      "depends_on": []
    }
  ]
}
```

{{< /tab >}}
{{% tab name="Full JSON Example" %}}

```json-viam
{
    "components": [
        {
            "name": "local",
            "type": "board",
            "model": "pi"
        },
        {
            "name": "xmotor",
            "type": "motor",
            "model": "gpiostepper",
            "attributes": {
                "board": "local",
                "pins": {
                    "dir": "dirx",
                    "pwm": "pwmx",
                    "step": "stepx"
                },
                "stepperDelay": 50,
                "ticksPerRotation": 200
            }
        },
        {
            "name": "ymotor",
            "type": "motor",
            "model": "gpiostepper",
            "attributes": {
                "board": "local",
                "pins": {
                    "dir": "diry",
                    "pwm": "pwmy",
                    "step": "stepy"
                },
                "stepperDelay": 50,
                "ticksPerRotation": 200
            }
        },
        {
            "name": "zmotor",
            "type": "motor",
            "model": "gpiostepper",
            "attributes": {
                "board": "local",
                "pins": {
                    "dir": "dirz",
                    "pwm": "pwmz",
                    "step": "stepz"
                },
                "stepperDelay": 50,
                "ticksPerRotation": 200
            }
        },
        {
            "name": "xaxis",
            "type": "gantry",
            "model": "oneaxis",
            "attributes": {
                "length_mm": 1000,
                "board": "local",
                "limit_pin_enabled_high": false,
                "limit_pins": [
                    "xlim1",
                    "xlim2"
                ],
                "motor": "xmotor",
                "gantry_rpm": 500,
                "axis": {
                    "x": 1,
                    "y": 0,
                    "z": 0
                }
            }
        },
        {
            "name": "yaxis",
            "type": "gantry",
            "model": "oneaxis",
            "attributes": {
                "length_mm": 1000,
                "board": "local",
                "limit_pin_enabled_high": false,
                "limit_pins": [
                    "ylim1",
                    "ylim2"
                ],
                "motor": "ymotor",
                "gantry_rpm": 500,
                "axis": {
                    "x": 0,
                    "y": 1,
                    "z": 0
                }
            }
        },
        {
            "name": "zaxis",
            "type": "gantry",
            "model": "oneaxis",
            "attributes": {
                "length_mm": 1000,
                "board": "local",
                "limit_pin_enabled_high": false,
                "limit_pins": [
                    "zlim1",
                    "zlim2"
                ],
                "motor": "zmotor",
                "gantry_rpm": 500,
                "axis": {
                    "x": 0,
                    "y": 0,
                    "z": 1
                }
            },
            "frame": {
                "parent": "world",
                "orientation": {
                    "type": "euler_angles",
                    "value": {
                        "roll": 0,
                        "pitch": 40,
                        "yaw": 0
                    }
                },
                "translation": {
                    "x": 0,
                    "y": 3,
                    "z": 0
                }
            }
        },
        {
            "name": "test",
            "type": "gantry",
            "model": "multiaxis",
            "attributes": {
                "subaxes_list": [
                    "xaxis",
                    "yaxis",
                    "zaxis"
                ]
            }
        }
    ]
}
```

{{% /tab %}}
{{< /tabs >}}

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `subaxes_list`  | *Required* | A complete list of the sub-axes, the one-axis gantries that make up the multi-axis gantry. |

## API

The gantry component supports the following methods:

| Method Name | Go | Python | Description |
| ----------- | -- | ------ | ----------- |
[Position](#position) | [Position][go_gantry]  |  [get_position][python_get_position] | Get the current positions of the axes of the gantry in mm. |
[MoveToPosition](#movetoposition) | [MoveToPosition][go_gantry] | [move_to_position][python_move_to_position] | Move the axes of the gantry to the desired positions. |
[Lengths](#lengths) | [Lengths][go_gantry] | [get_lengths][python_get_lengths] | Get the lengths of the axes of the gantry in mm. |
[Stop](#stop) | [Stop][go_gantry] | [stop][python_stop] | Stop the gantry from moving. |
[IsMoving](#stop) | [IsMoving][go_gantry] | [stop][python_is_moving] | Get if the gantry is currently moving. |

[go_gantry]: https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry
[python_get_position]: https://python.viam.dev/autoapi/viam/components/gantry/index.html#viam.components.gantry.Gantry.get_position
[python_move_to_position]: https://python.viam.dev/autoapi/viam/components/gantry/index.html#viam.components.gantry.Gantry.move_to_position
[python_get_lengths]: https://python.viam.dev/autoapi/viam/components/gantry/index.html#viam.components.gantry.Gantry.get_lengths
[python_stop]: https://python.viam.dev/autoapi/viam/components/gantry/index.html#viam.components.gantry.Gantry.stop
[python_is_moving]: https://python.viam.dev/autoapi/viam/components/gantry/index.html#viam.components.gantry.Gantry.is_moving

## Code Examples

### Control your Gantry with Viam's Client SDK Libraries

Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and the [Getting Started with the Viam App guide](/manage/app-usage/) for app-specific guidance.

The following example assumes you have a gantry called "my_gantry" configured as a component of your robot.
If your gantry has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.gantry import Gantry
from viam.proto.common import WorldState

async def main():
    # Connect to your robot.
    robot = await connect()

    # Log an info message with the names of the different resources that are connected to your robot.
    print('Resources:')
    print(robot.resource_names)

    # Connect to your gantry.
    myGantry = Gantry.from_robot(robot=robot, name='my_gantry')

    # Disconnect from your robot.
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
 "go.viam.com/rdk/components/gantry"
 "go.viam.com/rdk/referenceframe"
)

func main() {

  // Create an instance of a logger.
  logger := golog.NewDevelopmentLogger("client")

  // Connect to your robot.
  robot, err := client.New(
      context.Background(),
      "[ADD YOUR ROBOT ADDRESS HERE. YOU CAN FIND THIS ON THE SECURITY TAB OF THE VIAM APP]",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "[PLEASE ADD YOUR SECRET HERE. YOU CAN FIND THIS ON THE LOCATION'S PAGE IN THE VIAM APP]",
      })),
  )

  // Log any errors that occur.
  if err != nil {
      logger.Fatal(err)
  }

  // Delay closing your connection to your robot until main() exits.
  defer robot.Close(context.Background())

  // Log an info message with the names of the different resources that are connected to your robot.
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Connect to your gantry.
  myGantry, err := gantry.FromRobot(robot, "my_gantry")
  if err != nil {
    logger.Fatalf("cannot get gantry: %v", err)
  }

}
```

{{% /tab %}}
{{< /tabs >}}

### Position

Get the current positions of the axis of the gantry (mm).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `positions` [(List[float])](https://docs.python.org/3/library/typing.html#typing.List): A list of the position of the axes of the gantry in millimeters.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.get_position).

```python
myGantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Get the current positions of the axes of the gantry in millimeters.
positions = await myGantry.get_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `positions` [([]float64)](https://pkg.go.dev/builtin#float64): A list of the position of the axes of the gantry in millimeters.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")
if err != nil {
  logger.Fatalf("cannot get gantry: %v", err)
}

// Get the current positions of the axes of the gantry in millimeters.
position, err := myGantry.Position(context.Background(), nil)

// Log any errors that occur.
if err != nil {
  logger.Fatalf("cannot get positions of gantry axes: %v", err)
}

```

{{% /tab %}}
{{< /tabs >}}

### MoveToPosition

Move the axes of the gantry to the desired positions (mm).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `positions` [(List[float])](https://docs.python.org/3/library/typing.html#typing.List): A list of positions for the axes of the gantry to move to, in millimeters.
- `world_state`[(WorldState)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState): Optional and not yet fully implemented, see [the arm component](/components/arm/) for an example of usage with full component implementation.
Specifies obstacles that the gantry must avoid while it moves from its original position to the position specified in `pose`.
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.move_to_position).

```python
myGantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Create a list of positions for the axes of the gantry to move to. Assume in this example that the gantry is multiaxis, with 3 axes.
examplePositions = [1, 2, 3]

# Move the axes of the gantry to the positions specified.
await myGantry.move_to_position(positions=examplePositions, world_state=WorldState())
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positions` [([]float64)](https://pkg.go.dev/builtin#float64): A list of positions for the axes of the gantry to move to, in millimeters.
- `world_state`[(WorldState)](https://pkg.go.dev/go.viam.com/rdk@v0.2.12/referenceframe#WorldState): Optional and not yet fully implemented, see [the arm component](/components/arm/) for an example of usage with full component implementation.
Specifies obstacles that the gantry must avoid while it moves from its original position to the position specified in `pose`.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")
if err != nil {
  logger.Fatalf("cannot get gantry: %v", err)
}

// Create a list of positions for the axes of the gantry to move to. Assume in this example that the gantry is multiaxis, with 3 axes.
examplePositions = []float64{1, 2, 3}

// Move the axes of the gantry to the positions specified.
myGantry.MoveToPosition(context.Background(), examplePositions, referenceframe.WorldState(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### Lengths

Get the lengths of the axes of the gantry (mm).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `lengths_mm` [(List[float])](https://docs.python.org/3/library/typing.html#typing.List): A list of the lengths of the axes of the gantry in millimeters.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.lengths).

```python
myGantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Get the lengths of the axes of the gantry in millimeters.
lengths_mm = await myGantry.get_lengths()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `lengths_mm` [([]float64)](https://pkg.go.dev/builtin#float64): A list of the lengths of the axes of the gantry in millimeters.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")
if err != nil {
  logger.Fatalf("cannot get gantry: %v", err)
}

// Get the lengths of the axes of the gantry in millimeters.
lengths_mm, err := myGantry.Lengths(context.Background(), nil)

// Log any errors that occur.
if err != nil {
  logger.Fatalf("cannot get axis lengths of gantry: %v", err)
}

```

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop all motion of the gantry.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.stop).

```python
myGantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Stop all motion of the gantry. It is assumed that the gantry stops immediately.
await myGantry.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")
if err != nil {
  logger.Fatalf("cannot get gantry: %v", err)
}

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

- `is_moving` [(bool)](https://docs.python.org/c-api/bool.html): If it is true or false that the gantry is currently moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.is_moving).

```python
myGantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Stop all motion of the gantry. It is assumed that the gantry stops immediately.
await myGantry.stop()

# Print if the gantry is currently moving.
print(myGantry.is_moving())
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- `is_moving` [(bool)](https://pkg.go.dev/builtin#bool): If it is true or false that the gantry is currently moving.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

```go
myGantry, err := gantry.FromRobot(robot, "my_gantry")
if err != nil {
  logger.Fatalf("cannot get gantry: %v", err)
}

// Stop all motion of the gantry. It is assumed that the gantry stops immediately.
myGantry.Stop(context.Background(), nil)

// Log if the gantry is currently moving.
is_moving, err := myGantry.IsMoving(context.Background())
if err != nil {
  logger.Fatalf("cannot get if gantry is moving: %v", err)
}
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.
