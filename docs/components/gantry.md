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

A *gantry* on a robot is a mechanical system that you can use to hold and position a variety of end-effectors: devices designed to attach to the robot and interact with the environment to perform tasks.

A multi-axis gantry component is made up of many single-axis gantries, with each referenced in configuration in the multi-axis models' attribute `subaxes_list`.
<!-- - Each gantry can be given a reference [frame](/services/frame-system/) in configuration that describes its translation and orientation to the world.
- The system will then use any reference frames in the single-axis configs to place the gantries in the correct position and orientation. The “world” frame of each gantry becomes the moveable frame of the gantry. -->

Gantry components can only be controlled in terms of linear motion.
Each gantry can only move in one axis within the limits of its length.

**Requirements:**

- A [board](/components/board/) or [controller](/components/input-controller/) component that can detect changes in voltage on GPIO pins
- A [motor](/components/motor/) that can move linear rails
  - Encoded motor: See [DC motor with encoder](/components/motor/#dc-motor-with-encoder) and [encoder component](/components/encoder/) for more information.
  - [Stepper motor](/components/motor/#stepper-motor): Requires setting limit switches in the config of the gantry, or setting offsets in the config of the stepper motor.
- Limit switches, to attach to the ends of the gantry's axis

### Configuration

Configuring this component on your robot with a gantry enables you to get and change the position of the linear rail axes.
You can easily configure your component, as pictured below, on the [Viam App](https://app.viam.com/).

#### One-Axis

This is how you configure a one-axis gantry:

{{< tabs name="Example Gantry Config One-Axis" >}}
{{< tab name="Config Builder" >}}

<img src="../img/gantry/gantry-config-ui-oneaxis.png" alt="Picture of what an example configuration for a one-axis gantry component looks like in the Viam App config builder." width="800"/>

{{< /tab >}}
{{% tab name="Raw JSON" %}}

```json-viam
{
  "components": [
    {
      "name": <your_oneaxis_gantry_name>,
      "type": "gantry",
      "model": "oneaxis",
      "attributes": {
        "motor": <your_motor_name>,
        "length_mm": 800,
        "axis": {
          "X": 0,
          "Y": 0,
          "Z": 0
        }
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

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
      The name of the board that is connected to the limit switches and pins.
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
      limit_pin_enabled_high
    </td>
    <td>
      If it is true or false that the limit pins are enabled.
    </td>
  </tr>
  <tr>
    <td>
      length_mm
    </td>
    <td>
      The length of the axis of the gantry in mm.
    </td>
  </tr>
  <tr>
    <td>
      mm_per_rev
    </td>
    <td>
      How far the gantry moves (linear, distance in mm) per one revolution of the motor’s output
      shaft. This typically corresponds to Distance = PulleyDiameter*2*pi, or the pitch of a linear screw.
    </td>
  </tr>
  <tr>
    <td>
      gantry_rpm
    </td>
    <td>
      The gantry motor's default rpm.
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
        You can add a frame to a one-axis gantry attribute to describe its
        position in the local "world" frame.
        <p>
          See
          <a href="/services/frame-system">
            Frame System
          </a>
          for more information.
    </td>
  </tr>
</table>

A frame can also be added to a one-axis gantry attribute to describe its position in the local "world" [frame](/services/frame-system/).

#### Multi Axis

This is how you configure a multi-axis gantry:

{{< tabs name="Example Gantry Config Multi-Axis" >}}
{{< tab name="Config Builder" >}}

<img src="../img/gantry/gantry-config-ui-multiaxis.png" alt="TODO" width="800"/>

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

{{% /tab %}}
{{< /tabs >}}

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
        subaxes_list
    </td>
    <td>
      A complete list of the sub-axes, the one-axis gantries that make up the multi-axis gantry.
    </td>
  </tr>
</table>

## Code Examples

### Control your Gantry with Viam's Client SDK Libraries

Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and the [Getting Started with the Viam App guide](/program/app-usage/) for app-specific guidance.

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
{{% tab name="Golang" %}}

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
      "[ADD YOUR ROBOT ADDRESS HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP]",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "[PLEASE ADD YOUR SECRET HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP]",
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
{{% tab name="Golang" %}}

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
```

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next Steps

<div class="container text-center">
  <div class="row">
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="/tutorials/yahboom-rover/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Drive a Yahboom Rover with a Gamepad</h4>
            <p style="text-align: left;">Instructions for getting a Yahboom 4WD Rover driving with a Bluetooth Gamepad and the Viam app.</p>
        </a>
    </div>
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="/tutorials/controlling-an-intermode-rover-canbus/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Control an Intermode Rover with CAN Bus and Viam</h4>
            <p style="text-align: left;">How to abstract CAN bus protocol to control an Intermode rover with Viam.</p>
        </a>
    </div>
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="/tutorials/viam-rover/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Drive the Viam Rover with the Viam SDK</h4>
            <p style="text-align: left;">Try Viam by using the Viam SDK to make your Viam Rover move in a square.</p>
        </a>
    </div>
  </div>
</div>
