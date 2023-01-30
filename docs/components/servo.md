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

Hobby servos are a type of actuator comprising a small motor with built-in closed-loop control.

The Viam `servo` component is designed to support hobby servos, not servomotors.
Configure an industrial servomotor as a [motor](/components/motor/) with an [encoder](/components/encoder/).

## Hardware Requirements

A typical servo control setup comprises the following:

- A Raspberry Pi (or other [board](/components/board/))
- A servo
- An appropriate power supply

## Wiring Example

{{% alert title="Caution" color="caution" %}}  
Always disconnect devices from power before plugging, unplugging or moving wires or otherwise modifying electrical circuits.
{{% /alert %}}

Here's an example of how a servo might be wired to a Raspberry Pi:  

![A diagram showing the signal wire of a servo connected to pin 16 on a Raspberry Pi. The servo's power wires are connected to a 4.8V power supply.](../img/servo/servo-wiring.png)

{{% alert title="Note" color="note" %}}

Instead of powering the servo with a separate power supply, you may choose to power it using the 5V and ground pins on the board.
This can work, as long as the servo is not under any significant load.
Keep in mind that if the servo draws too much power, it can cause the board to temporarily lose power.

{{% /alert %}}

## Viam Configuration

The following fields are required when configuring a servo:

- **Name**: A name of the user's choosing by which to identify the component

- **Type**: `servo` for all servos

- **Model**: Either `pi`, `gpio`, or `fake`:

  - `pi` is the recommended model when configuring a hobby servo wired to a Raspberry Pi.
  Unlike other servo models, it is implemented as part of the `pi` board component; [you can see the code here](https://github.com/viamrobotics/rdk/blob/main/components/board/pi/impl/servo.go).

  - `gpio` is the general-purpose model, compatible with Viam-supported boards.

  - `fake` is for testing code without any actual hardware.

- **Attributes**: Other details the component requires to function.
All models require the following:

  - `pin` (string): The board pin (with PWM capabilities) to which the servo's control wire is attached.
  Use pin number, not GPIO number.

  - `board` (string): The name of the board to which the servo is wired.

  - Some models have additional attributes which are [described below](#optional-attributes-gpio-model).

### Example Config

The following is an example configuration file showing a board component and a servo component:

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
        "pin": "16"
      },
      "depends_on": [
        "example-pi"
      ]
    }
  ]
}
```

{{% /tab %}}
{{< tab name="Annotated JSON" >}}

<img src="../img/servo/servo-json.png" alt="An example servo config file with explanatory annotations."></img>

{{< /tab >}}
{{< /tabs >}}

### Optional Attributes: GPIO Model

| Attribute Name          | Type    | Description                                                                                                                                                             |
| ----------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `min_angle_deg`         | float64 | Specifies the minimum angle in degrees to which the servo can move. Does not affect PWM calculation.                                                                    |
| `max_angle_deg`         | float64 | Specifies the maximum angle in degrees to which the servo can move. Does not affect PWM calculation.                                                                    |
| `starting_position_deg` | float64 | Starting position of the servo in degrees.                                                                                                                              |
| `frequency_hz`          | uint    | The rate of pulses sent to the servo. The servo driver will attempt to change the GPIO pin's frequency (in Hz). The recommended PWM frequency for servos is typically in the range of 40-200 Hz, with most servos using 50 Hz (see your servo's data sheet). Maximum supported frequency by this driver is 450Hz |
| `pwm_resolution`        | uint    | Resolution of the PWM driver (e.g. number of ticks for a full period). Must be in range (0, 450). If not specified, the driver will attempt to estimate the resolution. |
| `min_width_us`          | uint    | Override the safe minimum pulse width in microseconds. This affects PWM calculation.                                                                                    |
| `max_width_us`          | uint    | Override the safe maximum pulse width in microseconds. This affects PWM calculation.                                                                                    |

## API

The servo component supports the following methods:

| Method Name                   | Golang                 | Python                              | Description                                                            |
| ----------------------------- | ---------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
| [Move](#move)                 | [Move][go_servo]       | [move][python_move]                 | Move the servo to the provided angle.                                  |
| [Get Position](#get-position) | [GetPosition][go_servo]| [get_position][python_get_position] | Returns an int representing the current angle of the servo in degrees. |
| [Stop](#stop)                 | [Stop][go_servo]       | [stop][python_stop]                 | Stops the servo.                                                       |

[go_servo]: https://pkg.go.dev/go.viam.com/rdk@v0.2.1/components/servo#Servo
[python_move]: https://python.viam.dev/autoapi/viam/components/servo/index.html#viam.components.servo.ServoClient.move
[python_get_position]: https://python.viam.dev/autoapi/viam/components/servo/index.html#viam.components.servo.ServoClient.get_position
[python_stop]: https://python.viam.dev/autoapi/viam/components/servo/index.html#viam.components.servo.ServoClient.stop

### Controlling a servo via SDK

{{% alert title="Note" color="note" %}}

First make sure you have [set up your robot and connected it to the Viam app](/installation/).

The following example assumes you have a servo called "my_servo" configured as a component of your robot.
If your servo has a different name, swap out the name where needed.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.servo import ServoClient

async def main():
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    # Get the servo client from the robot
    myServo = ServoClient.from_robot(robot=robot, name='my_servo')

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
  // robot, err := client.New(...)

  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Get the servo client from the robot.
  myServo, err := servo.FromRobot(robot, "my_servo")
  if err != nil {
    logger.Fatalf("cannot get servo: %v", err)
  }
}
```

{{% /tab %}}
{{< /tabs >}}

### Move

Move requests the servo of the underlying robot to move.

{{% alert title="Note" color="note" %}}
If you are using a continuous rotation servo, you will still use the Move command but instead of moving to a given position, the servo will start moving at a set speed.
The speed will be approximately linearly related to the "angle" you pass in, but you will need to determine based on your own hardware which "angle" represents your desired speed.
{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- angle (int): The desired angle of the servo in degrees.

**Returns:**

- None

[Python SDK Move Documentation](https://python.viam.dev/autoapi/viam/components/servo/index.html#viam.components.servo.ServoClient.move)

```python
myServo = ServoClient.from_robot(robot=robot, name='my_servo')

# Move the servo to the provided angle, which is 10 degrees in this case
await myServo.move(10)

# Move the servo to 90 degrees
await myServo.move(90)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- angleDeg (uint8): The desired angle of the servo in degrees.
- extra (map[string]interface{}): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error if one occurred.

[Go SDK Move Documentation](https://pkg.go.dev/go.viam.com/rdk@v0.2.1/components/servo#Servo)

```go
myServo, err := servo.FromRobot(robot, "my_servo")
if err != nil {
  logger.Fatalf("cannot get servo: %v", err)
}

// Move the servo to the provided angle, which is 10 degrees in this case
myServo.Move(context.Background(), 10)

// Move the servo to the 90 degrees
myServo.Move(context.Background(), 90)
```

{{% /tab %}}
{{< /tabs >}}

### Get Position

Get Position returns an int representing the current angle of the servo in degrees.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- The current angle of the servo in degrees. (int)

[Python SDK Get Position Documentation](https://python.viam.dev/autoapi/viam/components/servo/index.html#viam.components.servo.ServoClient.get_position)

```python
myServo = ServoClient.from_robot(robot=robot, name='my_servo')

# Move the servo to the provided angle, which is 10 degrees in this case
await myServo.move(10)

# Get the current position of the servo, which returns 10
await myServo.get_position()

# Move the servo to 20 degrees
await myServo.move(20)

# Get the current position of the servo, which returns 20
await myServo.get_position()
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- extra (map[string]interface{}): Extra options to pass to the underlying RPC call.

**Returns:**

- angleDeg ([uint8](https://pkg.go.dev/builtin#uint8)): The current angle of the servo in degrees.
- [error](https://pkg.go.dev/builtin#error): An error if one occurred.

[Go SDK Get Position Documentation](https://pkg.go.dev/go.viam.com/rdk@v0.2.1/components/servo#Servo)

```go
myServo, err := servo.FromRobot(robot, "my_servo")
if err != nil {
  logger.Fatalf("cannot get servo: %v", err)
}

// Move the servo to the provided angle, which is 10 degrees in this case
myServo.Move(context.Background(), 10)

// Move the servo to 20 degrees
myServo.Move(context.Background(), 20)
```

{{% /tab %}}
{{< /tabs >}}

### Stop

Stops the servo. It is assumed that the servo stops immediately.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None.

[Python SDK Stop Documentation](https://python.viam.dev/autoapi/viam/components/servo/index.html#viam.components.servo.ServoClient.stop)

```python
myServo = ServoClient.from_robot(robot=robot, name='my_servo')

# Move the servo to the provided angle, which is 10 degrees in this case
await myServo.move(10)

# Stop the servo
await myServo.stop()
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- extra (map[string]interface{}): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error if one occurred.

[Go SDK Stop Documentation](https://pkg.go.dev/go.viam.com/rdk@v0.2.1/components/servo#Servo)

```go
myServo, err := servo.FromRobot(robot, "my_servo")
if err != nil {
  logger.Fatalf("cannot get servo: %v", err)
}

// Move the servo to the provided angle, which is 10 degrees in this case
myServo.Move(context.Background(), 10)

// Stop the servo
myServo.Stop(context.Background())
```

{{% /tab %}}
{{< /tabs >}}
