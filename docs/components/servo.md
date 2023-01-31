---
title: "Servo Component"
linkTitle: "Servo"
weight: 80
type: "docs"
description: "Explanation of servo wiring and configuration in Viam."
tags: ["servo", "components"]
icon: "img/components/servo.png"
# SME: #team-bucket
---

The Viam servo component supports hobby servos: small motors with built-in closed-loop control.
Servos can be useful in robotics because their position is easily and precisely controlled.

- The servo component does not support servomotors.
To configure an industrial servomotor, use the [motor](/components/motor/) component with an [encoder](/components/encoder/).

{{% alert title="Caution" color="caution" %}}  
Always disconnect devices from power before plugging, unplugging or moving wires or otherwise modifying electrical circuits.
{{% /alert %}}

Example wiring diagram for a servo wired to a Raspberry Pi board:  

![A diagram showing the signal wire of a servo connected to pin 16 on a Raspberry Pi. The servo's power wires are connected to a 4.8V power supply.](../img/servo/servo-wiring.png)

Most robots with a servo need at least the following hardware:

- A [board component](/components/board/) that can run `viam-server`.
- A servo
- A power supply for the board
- A power supply for the servo

## Configuration

Refer to the following example configuration file, including the board and servo:

{{< tabs name="Example Servo Config" >}}
{{% tab name="Raw JSON" %}}

```json
{
  "components": [
    {
      "name": "example-pi",
      "type": "board",
      "model": "pi"
    },
    {
      "name": "example-name",
      "type": "servo",
      "model": "pi",
      "attributes": {
        "pin": "16",
        "board": "example-pi"
      }
    }
  ]
}
```

{{% /tab %}}
{{< tab name="Annotated JSON" >}}

<img src="../img/servo/servo-json.png" alt="An example servo config file with explanatory annotations."></img>

{{< /tab >}}
{{< /tabs >}}

**Required Fields**:

- **Name**: a name that identifies the component

- **Type**: `servo`

- **Model**: Either `pi`, `gpio`, or `fake`:

  - `pi` is the recommended model when configuring a hobby servo wired to a Raspberry Pi.
  Unlike other servo models, it is implemented as part of the [`pi` board component](https://github.com/viamrobotics/rdk/blob/main/components/board/pi/impl/servo.go).
  - `gpio` is the general-purpose model, compatible with Viam-supported boards.
  - `fake` is for testing code without any actual hardware.

- **Depends On**: For model `pi`, you must include the name of the board in the `depends_on` field.

**Required Attributes**:

In addition to the required fields, servo models require the following `attributes` in their configuration:

- `pin` (string): The board pin (with PWM capabilities) that the servo's control wire is attached to.
Use the pin number, not the GPIO number.
- `board` (string): The name of the board to which the servo is wired. Required for `gpio` model; does not apply to `pi` model.

**Optional Attributes**:

The `gpio` model has the following attributes, which are optional to define in your configuration:

| Attribute Name          | Type    | Description                                                                                                                                                             |
| ----------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `min_angle_deg`         | float64 | Specifies the minimum angle in degrees to which the servo can move. Does not affect PWM calculation.                                                                    |
| `max_angle_deg`         | float64 | Specifies the maximum angle in degrees to which the servo can move. Does not affect PWM calculation.                                                                    |
| `starting_position_deg` | float64 | Starting position of the servo in degrees.                                                                                                                              |
| `frequency_hz`          | uint    | The rate of pulses sent to the servo. The servo driver will attempt to change the GPIO pin's frequency (in Hz). The recommended PWM frequency for servos is typically in the range of 40-200 Hz, with most servos using 50 Hz (see your servo's data sheet). Maximum supported frequency by this driver is 450Hz |
| `pwm_resolution`        | uint    | Resolution of the PWM driver (e.g. number of ticks for a full period). Must be in range (0, 450). If not specified, the driver will attempt to estimate the resolution. |
| `min_width_us`          | uint    | Override the safe minimum pulse width in microseconds. This affects PWM calculation.                                                                                    |
| `max_width_us`          | uint    | Override the safe maximum pulse width in microseconds. This affects PWM calculation. |

## API

The servo component supports the following methods:

| Method Name | Golang | Python | Description |
| ----------- | -------| ------ | ----------- |
| [Move](#move) | [Move][go_servo] | [move][python_move] | Move the servo to the desired angle. |
| [Position](#position) | [Position][go_servo] | [get_position][python_get_position] | Get the current angle of the servo. |
| [Stop](#stop) | [Stop][go_servo] | [stop][python_stop] | Stop the servo. |

[go_servo]: https://pkg.go.dev/go.viam.com/rdk@v0.2.1/components/servo#Servo
[python_move]: https://python.viam.dev/autoapi/viam/components/servo/index.html#viam.components.servo.ServoClient.move
[python_get_position]: https://python.viam.dev/autoapi/viam/components/servo/index.html#viam.components.servo.ServoClient.get_position
[python_stop]: https://python.viam.dev/autoapi/viam/components/servo/index.html#viam.components.servo.ServoClient.stop

### Control your servo with Viam's Client SDK Libraries

- [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/servo/index.html)
- [Golang SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/servo)

{{% alert title="Note" color="note" %}}

Make sure you have set up your robot and connected it to the Viam app. Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and the [Getting Started with the Viam App guide](/program/app-usage/) for app-specific guidance.

The following example assumes you have a servo called "my_servo" configured as a component of your robot.
If your servo has a different name, change the `name` in the example.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.servo import Servo

async def main():
    # Connect to your robot.
    robot = await connect()

    # Log an info message with the names of the different resources that are connected to your robot. 
    print('Resources:')
    print(robot.resource_names)

    # Connect to your servo.
    myServo = Servo.from_robot(robot=robot, name='my_servo')

    # Disconnect from your robot.
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Golang" %}}

```go
import (
 "go.viam.com/rdk/components/servo"
)

func main() {
  
  // Create an instance of a logger. 
  logger := golog.NewDevelopmentLogger("client")

  // Connect to your robot. 
  robot, err := client.New(
      context.Background(),
      "[ADD YOUR ROBOT ADDRESS HERE. YOU CAN FIND THIS ON THE CODE SAMPLE TAB OF THE VIAM APP]",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "[PLEASE ADD YOUR SECRET HERE. YOU CAN FIND THIS ON THE CODE SAMPLE TAB OF THE VIAM APP]",
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

  // Connect to your servo.
  myServo, err := servo.FromRobot(robot, "my_servo")
  if err != nil {
    logger.Fatalf("cannot get servo: %v", err)
  }

}
```

{{% /tab %}}
{{< /tabs >}}

### Move

Move the servo to the desired angle in degrees.

{{% alert title="Note" color="note" %}}

If you are using a continuous rotation servo, you can still use the `Move` command.
Please note that instead of moving to a given position, the servo will start moving at a set speed.

The speed will be related to the "angle" you pass in as a linear approximation, but you will need to determine from your hardware which "angle" represents your desired speed.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `angle` [(int)](https://docs.python.org/3/library/functions.html#int): The desired angle of the servo in degrees.
- `extra` [(Optional[Mapping[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.
  
**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.move).

```python
myServo = Servo.from_robot(robot=robot, name='my_servo')

# Move the servo from its origin to the desired angle of 10 degrees.
await myServo.move(10)

# Move the servo from its origin to the desired angle of 90 degrees.
await myServo.move(90)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `angleDeg` [(uint32)](https://pkg.go.dev/builtin#uint32): The desired angle of the servo in degrees.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

```go
myServo, err := servo.FromRobot(robot, "my_servo")
if err != nil {
  logger.Fatalf("cannot get servo: %v", err)
}

// Move the servo from its origin to the desired angle of 10 degrees.
myServo.Move(context.Background(), 10, nil)

// Move the servo from its origin to the desired angle of 90 degrees.
myServo.Move(context.Background(), 90, nil)
```

{{% /tab %}}
{{< /tabs >}}

### Position

Get the current set angle of the servo in degrees.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Mapping[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `position`[(int)](https://docs.python.org/3/library/functions.html#int): The current set angle of the servo in degrees.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.get_position).

```python
myServo = Servo.from_robot(robot=robot, name='my_servo')

# Move the servo from its origin to the desired angle of 10 degrees.
await myServo.move(10)

# Get the current set angle of the servo. 
pos1 = await myServo.get_position()

# Move the servo from its origin to the desired angle of 20 degrees.
await myServo.move(20)

# Get the current set angle of the servo.
pos2 = await myServo.get_position()
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `angleDeg` [uint32](https://pkg.go.dev/builtin#uint32)): The current set angle of the servo in degrees.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

```go
myServo, err := servo.FromRobot(robot, "my_servo")
if err != nil {
  logger.Fatalf("cannot get servo: %v", err)
}

// Move the servo from its origin to the desired angle of 10 degrees.
myServo.Move(context.Background(), 10, nil)

// Get the current set angle of the servo.
pos1, err = myServo.Position(context.Background(), nil)

// Move the servo from its origin to the desired angle of 20 degrees.
myServo.Move(context.Background(), 20, nil)

// Get the current set angle of the servo.
pos2, err = myServo.Position(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop the servo from moving.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Mapping[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.stop).

```python
myServo = Servo.from_robot(robot=robot, name='my_servo')

# Move the servo from its origin to the desired angle of 10 degrees.
await myServo.move(10)

# Stop the servo. It is assumed that the servo stops moving immediately.
await myServo.stop()
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

```go
myServo, err := servo.FromRobot(robot, "my_servo")
if err != nil {
  logger.Fatalf("cannot get servo: %v", err)
}

// Move the servo from its origin to the desired angle of 10 degrees.
myServo.Move(context.Background(), 10, nil)

// Stop the servo. It is assumed that the servo stops moving immediately.
myServo.Stop(context.Background(), nil)
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
        <a href="/tutorials/yahboom-rover/">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Drive a Yahboom Rover with a Gamepad</h4>
            <p style="text-align: left;">Instructions for getting a Yahboom 4WD Rover driving with a Bluetooth Gamepad and the Viam app.</p>
        </a>
    </div>
  </div>
</div>
