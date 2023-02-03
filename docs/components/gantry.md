---
title: "Gantry Component"
linkTitle: "Gantry"
draft: false
weight: 50
type: "docs"
description: "Explanation of gantry configuration and usage in Viam."
tags: ["gantry", "components"]
icon: "img/components/gantry.png"
# SME: Rand
---

## Overview

A gantry is a specific type of robot component that uses only linear links to move an end effector in 3D space.
A gantry can only control the position of the end effector, and is a commonly used machine design for simple positioning and placement.
A linear axis has the advantage of being a stiffer machine layout than an open chain of links, and holding or repetitively positioning the end effector is more attainable in this configuration.

### Requirements

A gantry in Viam requires the following:

* A board or controller that can detect changes in voltage on gpio pins.
* A motor:
  * An encoded motor
  * A stepper motor
    * Requires limit switches to be set in the gantry config or offsets to be set in stepper motor.
* Limit switches to attach to the brackets

A customized encoded motor controller can be used in the configuration of a gantry to move the linear rail.
This component abstracts this type of hardware to give the user an easy interface for moving many linear rails.

Since gantries are linearly moving components, each gantry can only move in one axis within the limits of its length.

Each gantry can be given a reference [frame](/services/frame-system/) in the configuration that describes its translation and orientation to the world.

A multi-axis gantry is composed of many single-axis gantries.
The multiple axis system is composed of the supplied gantry names.
The system will then use any reference frames in the single-axis configs to place the gantries in the correct position and orientation.
The “world” frame of each gantry becomes the moveable frame of the gantry before it in order.

## Attribute Configuration

### Single-Axis Gantry Attributes

The attributes are configured as such for a single-axis gantry:

<table>
  <tr>
    <td>
      <strong>
        Attribute
      </strong>
    </td>
    <td>
      <strong>
        Description
      </strong>
    </td>
  </tr>
  <tr>
    <td>
      board
    </td>
    <td>
      The name of the board that is connected to the and limit pin switches.
    </td>
  </tr>
  <tr>
    <td>
      motor
    </td>
    <td>
      The name of the motor that moves the gantry.
    </td>
  </tr>
  <tr>
    <td>
      limit_pins
    </td>
    <td>
      The pins attached to the limit switches on either end. Optional for encoded
      motor gantry types.
    </td>
  </tr>
  <tr>
    <td>
      limit_pin_enabled
    </td>
    <td>
      Is the Limit Pin enabled? I.e., true (pin HIGH)?
    </td>
  </tr>
  <tr>
    <td>
      mm_per_revolution
    </td>
    <td>
      How far the gantry moves linearly per one revolution of the motor’s output
      shaft.
      <p>
        This typically corresponds to
        <p>
          Distance = PulleyDiameter *2* pi
          <p>
            or the pitch of a linear screw.
    </td>
  </tr>
  <tr>
    <td>
      gantry_rpm
    </td>
    <td>
      The gantry’s motor’s default rpm.
    </td>
  </tr>
  <tr>
    <td>
      axis
    </td>
    <td>
      The axis in which the gantry is allowed to move relative to the reference
      frame (x, y, z).
      <p>
        You can add a frame to a single-axis gantry attribute to describe its
        position in the local “world” frame.
        <p>
          See
          <a href="/services/frame-system">
            Frame System
          </a>
          for further information.
    </td>
  </tr>
</table>

A frame can also be added to a one axis gantry attribute to describe its position in the local “world” [frame](/services/frame-system/).

### Multi-Axis Gantry Attributes

In addition to the attributes for single-axis gantries, multi-axis gantries also use these attributes:

<table>
  <tr>
    <td>
      <strong>
        Attribute
      </strong>
    </td>
    <td>
      <strong>
        Description
      </strong>
    </td>
  </tr>
  <tr>
    <td>
      <strong>
        subaxes_list
      </strong>
    </td>
    <td>
      A complete list of the sub-axes that compose the multi-axis gantry.
    </td>
  </tr>
</table>

## Gantry Methods

All gantries implement the following methods:

<table>
  <tr>
   <td><strong>Method Name</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td><file>GetPosition </file>
   </td>
   <td>Returns an array of floats that describe the current position to the gantry in each axis on which it moves.
<p>
The units are millimeters. A single-axis gantry returns a list with one element. A three-axis gantry returns a list containing three elements.
   </td>
  </tr>
  <tr>
   <td><file>MoveToPosition </file>
   </td>
   <td>Takes in a list of positions (units millimeters) and moves each axis of the gantry to the corresponding position.
<p>
The number of elements in the list must equal the number of moveable axes on the gantry, and the order of the elements in the list correspond to the order of the axes present in the gantry.
   </td>
  </tr>
  <tr>
   <td><file>GetLengths </file>
   </td>
   <td>Returns a list of lengths of each axis of the gantry in millimeters.
   </td>
  </tr>
  <tr>
   <td><file>Stop </file>
   </td>
   <td>Stops the actuating components of the Gantry.
   </td>
  </tr>
  <tr>
   <td><file>Do </file>
   </td>
   <td>Viam supplies this interface on each component to allow for additional, non-standard functionality that users may wish to include that is <em>not</em> available from  Viam’s interfaces.
   </td>
  </tr>
  <tr>
   <td><file>ModelFrame </file>
   </td>
   <td>Returns the Gantry model. This interface is used in Motion Planning. It is an interface that is used in <a href="/services/motion">motion service</a>.
   </td>
  </tr>
  <tr>
   <td><file>CurrentInputs </file>
   </td>
   <td>gets the positions of each axis of the gantry and transforms them into an Input type. It is used by the <a href="/services/motion">motion service</a>.
   </td>
  </tr>
  <tr>
   <td><file>GoToInputs </file>
   </td>
   <td>returns results from motion planning and Inputs to the gantry, and sends them to MoveToPosition as positions. It is used by the <a href="/services/motion">motion service</a>.
   </td>
  </tr>
  </table>

## Code Examples

### Example Multi-Axis Gantry Configuration

``` json
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
                "rpm": 500,
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
                "rpm": 500,
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
                "rpm": 500,
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

## Implementation

<<<<<<< HEAD
[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/gantry/index.html)
=======
### Position

Get the current positions of the axis of the gantry (mm).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `positions` [(List[float])](https://docs.python.org/3/library/typing.html#typing.List): A list of the position of the axes of the gantry in millimeters.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.get_position)

```python
myGantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Get the current positions of the axes of the gantry in millimeters.
positions = await myGantry.get_position()
```

{{% /tab %}}
{{% tab name="Golang" %}}

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
Plan for the gantry to avoid obstacles and comply with the constraints for movement specified in [(WorldState)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `positions` [(List[float])](https://docs.python.org/3/library/typing.html#typing.List): A list of positions for the axes of the gantry to move to, in millimeters.
- `world_state`[(WorldState)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState): Obstacles that the gantry must avoid while it moves from its original position to the position specified in `pose`.
A `WorldState` can include a variety of attributes, including a list of obstacles around the object (`obstacles`), a list of spaces the robot may operate within (`interaction_spaces`), and a list of supplemental transforms (`transforms`).
These fields are optional.
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
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positions` [([]float64)](https://pkg.go.dev/builtin#float64): A list of positions for the axes of the gantry to move to, in millimeters.
- `world_state`[(WorldState)](https://pkg.go.dev/go.viam.com/rdk@v0.2.12/referenceframe#WorldState): Obstacles that the gantry must avoid while it moves from its original position to the position specified in `pose`.
A `WorldState` can include a variety of attributes, including a list of obstacles around the object (`obstacles`), a list of spaces the robot may operate within (`interaction_spaces`), and a list of supplemental transforms (`transforms`).
These fields are optional.
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

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/gantry/gantry.html#Gantry.lengths)

```python
myGantry = Gantry.from_robot(robot=robot, name='my_gantry')

# Get the lengths of the axes of the gantry in millimeters.
lengths_mm = await myGantry.get_lengths()
```

{{% /tab %}}
{{% tab name="Golang" %}}

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
{{% tab name="Golang" %}}

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
{{% tab name="Golang" %}}

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
logger.Info(is_moving)
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next Steps

<div class="container text-center">
  <div class="row">
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="/tutorials/custom-base-dog/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Control a Robot Dog with a Custom Viam Base Component</h4>
            <p style="text-align: left;">How to integrate a custom base component with the Viam Python SDK.</p>
        <a>
    </div>
  </div>
</div>
>>>>>>> parent of 116a0b3 (explain worldstate implementation)
