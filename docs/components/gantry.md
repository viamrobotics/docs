---
title: "Gantry Component"
linkTitle: "Gantry"
draft: false
weight: 50
type: "docs"
description: "A mechanical system of linear rails that can precisely position an attached device."
tags: ["gantry", "components"]
icon: "/components/img/components/gantry.svg"
# SME: Rand
---

A robotic *gantry* is a mechanical system of linear actuators used to hold and position an [end effector](https://en.wikipedia.org/wiki/Robot_end_effector).
A 3D printer is an example of a three-axis gantry where each linear actuator can move the print head along one axis.
The linear rail design makes gantries a common and reliable system for simple positioning and placement tasks.

This component abstracts the hardware of a gantry to give you an easy interface for coordinated control of linear actuators, even many at once (multi-axis).
A multi-axis gantry is composed of many single-axis gantries.

<img src="../img/gantry/gantry-illustration.png" alt="Example of what a multi-axis robot gantry looks like as a black and white illustration of an XX YY mechanical gantry." style="max-width:300px; display: block; margin: 0 auto"></img>

Gantry components can only be controlled in terms of linear motion (you cannot rotate them).
Each gantry can only move in one axis within the limits of the length of the linear rail.

Most robots with a gantry need at least the following hardware:

- A [board](/components/board/) or [controller](/components/input-controller/) component that can detect changes in voltage on GPIO pins
- A [motor](/components/motor/) that can move linear rails
  - Encoded motor: See [DC motor with encoder](/components/motor/gpio/encoded-motor/) and [encoder component](/components/encoder/).
  - Stepper motor: See [Stepper motor](/components/motor/gpiostepper/).
  Requires setting limit switches in the config of the gantry, or setting offsets in the config of the stepper motor.
- Limit switches, to attach to the ends of the gantry's axis

## Configuration

Configuring this component on your robot with a gantry enables you to get and change the position of the linear rail axes.
You can configure your robot, as shown below, on the [Viam app](https://app.viam.com).

### One-Axis

This is how you configure a one-axis gantry:

{{< tabs name="Example Gantry Config One-Axis" >}}
{{< tab name="Config Builder" >}}

<img src="../img/gantry/gantry-config-ui-oneaxis.png" alt="Example of what configuration for a one-axis gantry component looks like in the Viam app config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="JSON Template" %}}

```json
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

### Multi-Axis

A multi-axis gantry component is made up of many single-axis gantries, with each referenced in configuration in the multi-axis models' attribute `subaxes_list`.

This is how you configure a multi-axis gantry:

{{< tabs name="Example Gantry Config Multi-Axis" >}}
{{< tab name="Config Builder" >}}

<img src="../img/gantry/gantry-config-ui-multiaxis.png" alt="Example of what configuration for a multi-axis gantry component looks like in the Viam app config builder." style="width:100%"/>

{{< /tab >}}
{{% tab name="JSON Template" %}}

```json
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

```json
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

## Control your gantry with Viam's client SDK libraries

Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries.

The following example assumes you have a gantry called "my_gantry" configured as a component of your robot.
If your gantry has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.gantry import Gantry

async def main():
    # Connect to your robot.
    robot = await connect()

    # Log an info message with the names of the different resources that are connected to your robot.
    print('Resources:')
    print(robot.resource_names)

    # Connect to your gantry.
    my_gantry = Gantry.from_robot(robot=robot, name='my_gantry')

    # Disconnect from your robot.
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "context"

  "github.com/edaniels/golog"

  "go.viam.com/rdk/components/gantry"
  "go.viam.com/rdk/referenceframe"
)

func main() {

  // Create an instance of a logger.
  logger := golog.NewDevelopmentLogger("client")

  // Connect to your robot.
  robot, err := client.New(
      context.Background(),
      "ADD YOUR ROBOT ADDRESS HERE. You can find this on the Code Sample tab of app.viam.com.",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "ADD YOUR LOCATION SECRET HERE. You can find this on the Code Sample tab of app.viam.com",
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

## API

The gantry component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
[Position](#position) | Get the current positions of the axes of the gantry in mm. |
[MoveToPosition](#movetoposition) | Move the axes of the gantry to the desired positions. |
[Lengths](#lengths) | Get the lengths of the axes of the gantry in mm. |
[Stop](#stop) | Stop the gantry from moving. |
[IsMoving](#stop) | Get if the gantry is currently moving. |
| [DoCommand](#docommand) | Sends or receives model-specific commands. |

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
my_gantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Get the current positions of the axes of the gantry in millimeters.
positions = await my_gantry.get_position()
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
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.move_to_position).

```python
my_gantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Create a list of positions for the axes of the gantry to move to. Assume in this example that the gantry is multiaxis, with 3 axes.
examplePositions = [1, 2, 3]

# Move the axes of the gantry to the positions specified.
await my_gantry.move_to_position(positions=examplePositions)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positions` [([]float64)](https://pkg.go.dev/builtin#float64): A list of positions for the axes of the gantry to move to, in millimeters.
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
myGantry.MoveToPosition(context.Background(), examplePositions, nil)
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
my_gantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Get the lengths of the axes of the gantry in millimeters.
lengths_mm = await my_gantry.get_lengths()
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
my_gantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Stop all motion of the gantry. It is assumed that the gantry stops immediately.
await my_gantry.stop()
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
my_gantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Stop all motion of the gantry. It is assumed that the gantry stops immediately.
await my_gantry.stop()

# Print if the gantry is currently moving.
print(my_gantry.is_moving())
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

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own gantry and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (`Dict[str, Any]`): The command to execute.

**Returns:**

- `result` (`Dict[str, Any]`): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot, "my_gantry")

command = {"cmd": "test", "data1": 500}
result = my_gantry.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/#the-do-method).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` ([`Context`](https://pkg.go.dev/context)): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` (`cmd map[string]interface{}`): The command to execute.

**Returns:**

- `result` (`cmd map[string]interface{}`): Result of the executed command.
- `error` ([`error`](https://pkg.go.dev/builtin#error)): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
  myGantry, err := gantry.FromRobot(robot, "my_gantry")

  command := map[string]interface{}{"cmd": "test", "data1": 500}
  result, err := myGantry.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/9be13108c8641b66fd4251a74ea638f47b040d62/components/input/input.go#L254).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
