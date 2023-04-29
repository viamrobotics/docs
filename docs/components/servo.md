---
title: "Servo Component"
linkTitle: "Servo"
weight: 80
type: "docs"
description: "A hobby servo is a special type of small motor whose position you can precisely control."
tags: ["servo", "components"]
icon: "/components/img/components/servo.svg"
# SME: #team-bucket
---

The Viam *servo* component supports hobby servos: small motors with built-in closed-loop control.
Servos can be useful in robotics because their position is easily and precisely controlled.

- The servo component does not support servomotors.
To configure an industrial servomotor, use the [motor](/components/motor/) component with an [encoder](/components/encoder/).

Example wiring diagram for a servo wired to a Raspberry Pi board:

![A diagram showing the signal wire of a servo connected to pin 16 on a Raspberry Pi. The servo's power wires are connected to a 4.8V power supply.](../img/servo/servo-wiring.png)

Most robots with a servo need at least the following hardware:

- A [board component](/components/board/) that can run `viam-server`
- A servo
- A power supply for the board
- A power supply for the servo

{{% alert title="Note" color="note" %}}

Instead of powering the servo with a separate power supply, you may choose to power it using the 5V and ground pins on the board.
This can work, as long as the servo is not under any significant load.
Keep in mind that if the servo draws too much power, it can cause the board to temporarily lose power.

{{% /alert %}}

## Configuration

Refer to the following example configuration file, including the board and servo:

{{< tabs name="Example Servo Config" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
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

**Required Attributes**:

In addition to the required fields, servo models require the following `attributes` in their configuration:

- `pin` (string): The board pin (with PWM capabilities) that the servo's control wire is attached to.
Use the pin number, not the GPIO number.
- `board` (string): The name of the board to which the servo is wired.

**Optional Attributes**:

The `gpio` model has the following attributes, which are optional to define in your configuration:

| Attribute Name          | Type    | Description |
| ----------------------- | ------- | ----------- |
| `min_angle_deg`         | float64 | Specifies the minimum angle in degrees to which the servo can move. Does not affect PWM calculation. |
| `max_angle_deg`         | float64 | Specifies the maximum angle in degrees to which the servo can move. Does not affect PWM calculation. |
| `starting_position_deg` | float64 | Starting position of the servo in degrees. |
| `frequency_hz`          | uint    | The rate of pulses sent to the servo. The servo driver will attempt to change the GPIO pin's frequency (in Hz). The recommended PWM frequency for servos is typically in the range of 40-200 Hz, with most servos using 50 Hz (see your servo's data sheet). Maximum supported frequency by this driver is 450Hz |
| `pwm_resolution`        | uint    | Resolution of the PWM driver (for example, the number of ticks for a full period). Must be in range (0, 450). If not specified, the driver will attempt to estimate the resolution. |
| `min_width_us`          | uint    | Override the safe minimum pulse width in microseconds. This affects PWM calculation.                                                                                    |
| `max_width_us`          | uint    | Override the safe maximum pulse width in microseconds. This affects PWM calculation. |
| `max_rotation`           | uint    | Default: 180. Specifies the maximum angle of rotation based on the hardware. Only for the `pi` model. |

## Control your servo with Viam's client SDK libraries

- [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/servo/index.html)
- [Go SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/servo)

{{% alert title="Note" color="note" %}}

The following example assumes you have a servo called "my_servo" configured as a component of your robot, and that your robot is connected on [the Viam app](https://app.viam.com/).
If your servo has a different name, change the `name` in the example.

Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.components.servo import Servo

async def main():
    # Connect to your robot.
    robot = await connect()

    # Log an info message with the names of the different resources that are connected to your robot.
    print('Resources:')
    print(robot.resource_names)

    # Connect to your servo.
    my_servo = Servo.from_robot(robot=robot, name='my_servo')

    # Disconnect from your robot.
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
  "context"
  "github.com/edaniels/golog"
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

## API

The servo component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [Move](#move) | Move the servo to the desired angle. |
| [Position](#position) | Get the current angle of the servo. |
| [Stop](#stop) | Stop the servo. |
| [DoCommand](#docommand) | Sends or receives model-specific commands. |

### Move

Move the servo to the desired angle in degrees.

{{% alert title="Note" color="note" %}}
Support for continuous servos  with the GPIO servo model is experimental.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

If you are using a continuous rotation servo, you can use the `Move` command, but instead of moving to a given position, the servo will start moving at a set speed.

The speed will be related to the "angle" you pass in as a linear approximation.
90 degrees represents stop, 91 to 180 represents counter-clockwise rotation from slowest to fastest, and 89 to 1 represents clockwise from slowest to fastest.
It is recommended that you test your servo to determine the desired speed.

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

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name='my_servo')

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Move the servo from its origin to the desired angle of 90 degrees.
await my_servo.move(90)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `angleDeg` [(uint32)](https://pkg.go.dev/builtin#uint32): The desired angle of the servo in degrees.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

```go {class="line-numbers linkable-line-numbers"}
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

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name='my_servo')

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Get the current set angle of the servo.
pos1 = await my_servo.get_position()

# Move the servo from its origin to the desired angle of 20 degrees.
await my_servo.move(20)

# Get the current set angle of the servo.
pos2 = await my_servo.get_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `angleDeg` [uint32](https://pkg.go.dev/builtin#uint32)): The current set angle of the servo in degrees.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

```go {class="line-numbers linkable-line-numbers"}
my_servo, err := servo.FromRobot(robot, "my_servo")
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

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name='my_servo')

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Stop the servo. It is assumed that the servo stops moving immediately.
await my_servo.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

```go {class="line-numbers linkable-line-numbers"}
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

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own servo and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (`Dict[str, Any]`): The command to execute.

**Returns:**

- `result` (`Dict[str, Any]`): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot, "my_servo")

command = {"cmd": "test", "data1": 500}
result = my_servo.do(command)
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
  myServo, err := servo.FromRobot(robot, "my_servo")

  command := map[string]interface{}{"cmd": "test", "data1": 500}
  result, err := myServo.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/main/resource/resource.go).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next Steps

{{< cards >}}
  {{% card link="/tutorials/control/yahboom-rover" size="small" %}}
  {{% card link="/tutorials/projects/integrating-viam-with-openai" size="small" %}}
{{< /cards >}}
