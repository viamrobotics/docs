---
title: "Motor Component"
linkTitle: "Motor"
weight: 70
type: "docs"
description: "A motor is a rotating machine that transforms electrical energy into mechanical energy."
tags: ["motor", "components"]
icon: "img/components/motor.png"
no_list: true
aliases:
    - /components/motor/
# SME: Rand
---

Electric motors are machines that convert electricity into rotary motion.
They are the most common form of [actuator](https://en.wikipedia.org/wiki/Actuator) in robotics.
The *motor* component type natively supports brushed DC motors, brushless DC motors, and stepper motors controlled by a variety of [motor drivers](https://www.wellpcb.com/what-is-motor-driver.html).

Most robots with a motor need at least the following hardware:

- The motor itself.
- A compatible motor driver.
  This takes signals from the computer and sends the corresponding signals and power to the motor.
  Selected based on the type of motor (for example, brushed, brushless, or stepper) and its power requirements.
- A [board component](https://docs.viam.com/components/board/) to send signals to the motor driver[^dmcboard].
  For example, a Raspberry Pi, or another model of single-board computer with GPIO (general purpose input/output) pins.

[^dmcboard]: The `DMC4000` model does not require a board.

## Configuration

How you configure your motor with Viam depends more on the motor driver than on the motor itself.
Click the model names below for configuration information:

Model | Supported hardware <a name="model-table"></a>
---------- | ------------------
[`gpio`](./gpio/) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor)
[`gpiostepper`](./gpiostepper/) | [Stepper motor](https://en.wikipedia.org/wiki/Stepper_motor) driven by a basic stepper driver
[`TMC5072`](./tmc5072/) | Stepper motor driven by [the TMC5072 chip](https://www.trinamic.com/support/eval-kits/details/tmc5072-bob/)
[`DMC4000`](./dmc4000/) | Stepper motor driven by a [DMC-40x0 series motion controller](https://www.galil.com/motion-controllers/multi-axis/dmc-40x0)
[`fake`](./fake/) | Used to test code without hardware

## Control your motor with Viam's client SDK libraries

The following example assumes you have motors called `motor1` and `motor2` configured as components of your robot.
If your motor has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

Place the example code after the `robot = await connect()` function in `main()`.

```python
from viam.components.motor import Motor

robot = await connect() # Refer to CODE SAMPLE tab code
motor1 = Motor.from_robot(robot, "motor1")
motor2 = Motor.from_robot(robot, "motor2")

# Power motor1 at 100% for 3 seconds
await motor1.set_power(1)
await asyncio.sleep(3)
await motor1.stop()

# Run motor2 at 1000 rpm for 200 rotations
await motor2.go_for(1000, 200)
```

{{% /tab %}}
{{% tab name="Go" %}}

Example code should be placed after the `robot, err := client.New(...)` function in `main()`.

```go
import (
  "context"
  "time"

  "github.com/edaniels/golog"

  "go.viam.com/rdk/components/motor"
)

robot, err := client.New() // Refer to CODE SAMPLE tab code
// Grab the motors from the robot
m1, err := motor.FromRobot(robot, "motor1")
m2, err := motor.FromRobot(robot, "motor2")

// Power motor1 at 100% for 3 seconds
m1.SetPower(context.TODO(), 1, nil)
time.Sleep(3 * time.Second)
m1.Stop(context.TODO(), nil)

// Run motor2 at 1000 RPM for 200 rotations
m2.GoFor(context.TODO(), 1000, 200, nil)
```

{{% /tab %}}
{{< /tabs >}}

## API

Method Name | Description
----------- | -----------
[SetPower](#setpower) | Sets the power to send to the motor as a portion of max power.
[GoFor](#gofor) | Spins the motor the specified number of revolutions at specified RPM.
[GoTo](#goto) | Sends the motor to a specified position (in terms of revolutions from home) at a specified speed.
[ResetZeroPosition](#resetzeroposition) | Sets the current position to be the new zero (home) position.
[GetPosition](#getposition) | Reports the position of the motor based on its encoder. Not supported on all motors.
[GetProperties](#getproperties) | Returns whether or not the motor supports certain optional features.
[Stop](#stop) | Cuts power to the motor off immediately, without any gradual step down.
[IsPowered](#ispowered) | Returns whether or not the motor is currently on, and the amount of power to it.
[IsMoving](#ismoving) | Returns whether the motor is moving or not.
[DoCommand](#docommand) | Sends or receives model-specific commands.

In addition to the information below, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor)
or [Python SDK docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#).

### SetPower

Sets the portion of max power to send to the motor (between -1 and 1).
1 is 100% power forwards; -1 is 100% power backwards.

Power is expressed as a floating point between -1 and 1 that scales between -100% and 100% power.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `power` [(float)](https://docs.python.org/3/library/functions.html#float): Portion of full power to send to the motor expressed as a floating point between -1 and 1. 1 is 100% power forwards; -1 is 100% power backwards.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.set_power).

**Example usage:**

```python
my_motor = Motor.from_robot(robot=robot, name='my_motor')

# Set the power to 40% forwards.
await my_motor.set_power(power = 0.4)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `powerPct` [(float64)](https://pkg.go.dev/builtin#float64): Portion of full power to send to the motor expressed as a floating point between -1 and 1. 1 is 100% power forwards; -1 is 100% power backwards.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

**Example usage:**

```go
myMotor, err := motor.FromRobot(robot, "motor1")

// Set the motor power to 40% forwards.
myMotor.SetPower(context.TODO(), 0.4, nil)

```

{{% /tab %}}
{{< /tabs >}}

### GoFor

Spins the motor the specified number of revolutions at specified revolutions per minute.
When `rpm` or `revolutions` is a negative value, the motor spins in the backward direction.
If both `rpm` and `revolutions` are negative, the motor spins in the forward direction.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `rpm` [(float)](https://docs.python.org/3/library/functions.html#float): Speed at which the motor should move in revolutions per minute (negative implies backwards).
- `revolutions` [(float)](https://docs.python.org/3/library/functions.html#float): Number of revolutions the motor should run for (negative implies backwards).

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.go_for).

**Example usage:**

```python
my_motor = Motor.from_robot(robot=robot, name='my_motor')

# Turn the motor 7.2 revolutions at 60 RPM.
await my_motor.go_for(rpm=60, revolutions=7.2)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `rpm` [(float64)](https://pkg.go.dev/builtin#float64): Speed at which the motor should move in revolutions per minute (negative implies backwards).
- `revolutions` [(float64)](https://pkg.go.dev/builtin#float64): Number of revolutions the motor should run for (negative implies backwards).
  If revolutions is 0, this runs the motor at `rpm` indefinitely.
  If revolutions != 0, this blocks until the number of revolutions has been completed or another operation comes in.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

**Example usage:**

```go
myMotor, err := motor.FromRobot(robot, "motor1")

// Turn the motor 7.2 revolutions at 60 RPM.
myMotor.GoFor(context.TODO(), 60, 7.2, nil)
```

{{% /tab %}}
{{< /tabs >}}

### GoTo

Turns the motor to a specified position (in terms of revolutions from home/zero) at a specified speed in revolutions per minute (RPM).
Regardless of the directionality of the `rpm`, the motor will move towards the specified target position.
This blocks until the position has been reached.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `rpm` [(float)](https://docs.python.org/3/library/functions.html#float): Speed at which the motor should move in revolutions per minute (absolute value).
- `position_revolutions` [(float)](https://docs.python.org/3/library/functions.html#float): Target position relative to home/zero, in revolutions.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.go_to).

**Example usage:**

```python
my_motor = Motor.from_robot(robot=robot, name='my_motor')

# Turn the motor to 8.3 revolutions from home at 75 RPM.
await my_motor.go_to(rpm=75, revolutions=8.3)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `rpm` [(float64)](https://pkg.go.dev/builtin#float64): Speed at which the motor should move in revolutions per minute (absolute value).
- `positionRevolutions` [(float64)](https://pkg.go.dev/builtin#float64): Target position relative to home/zero, in revolutions.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

**Example usage:**

```go
myMotor, err := motor.FromRobot(robot, "motor1")

// Turn the motor to 8.3 revolutions from home at 75 RPM.
myMotor.GoTo(context.TODO(), 75, 8.3, nil)
```

{{% /tab %}}
{{< /tabs >}}

### ResetZeroPosition

Set the current position (modified by `offset`) to be the new zero (home) position.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `offset` [(float)](https://docs.python.org/3/library/functions.html#float): The offset from the current position to the new home (zero) position.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.reset_zero_position).

**Example usage:**

```python
my_motor = Motor.from_robot(robot=robot, name='my_motor')

# Set the current position as the new home position with no offset.
await my_motor.reset_zero_position(offset=0.0)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `offset` [(float64)](https://pkg.go.dev/builtin#float64): The offset from the current position to the new home (zero) position.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

**Example usage:**

```go
myMotor, err := motor.FromRobot(robot, "motor1")

// Set the current position as the new home position with no offset.
myMotor.ResetZeroPosition(context.TODO(), 0.0, nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetPosition

Report the position of the motor based on its encoder.
The value returned is the number of revolutions relative to its zero position.
This method raises an exception if position reporting is not supported by the motor.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(float)](https://docs.python.org/3/library/functions.html#float) Number of revolutions the motor is away from zero/home.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.get_position).

**Example usage:**

```python
my_motor = Motor.from_robot(robot=robot, name='my_motor')

# Get the current position of the motor.
position = await my_motor.get_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The unit returned is the number of revolutions which is intended to be fed back into calls of GoFor.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

**Example usage:**

```go
myMotor, err := motor.FromRobot(robot, "motor1")

// Get the current position of the motor.
position, _ := myMotor.Position(context.TODO(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Report a dictionary mapping optional properties to whether it is supported by this motor.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(Properties)](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.Properties): Map of feature names to supported status.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.get_properties).

**Example usage:**

```python
my_motor = Motor.from_robot(robot=robot, name='my_motor')

# Report a dictionary mapping optional properties to whether it is supported by this motor.
properties = await my_motor.get_properties()
print('Properties:')
print(properties)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- (map[[Feature]](https://pkg.go.dev/go.viam.com/rdk/components/motor#Feature)[bool](https://pkg.go.dev/builtin#bool), [error](https://pkg.go.dev/builtin#error)): A map indicating whether or not the motor supports certain optional features.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

**Example usage:**

```go
myMotor, err := motor.FromRobot(robot, "motor1")

// Return whether or not the motor supports certain optional features.
properties, _ := myMotor.Properties(context.TODO(), nil)
logger.Info("Properties:")
logger.Info(properties)
```

{{% /tab %}}
{{< /tabs >}}

### Stop

Cut the power to the motor immediately, without any gradual step down.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.stop).

**Example usage:**

```python
my_motor = Motor.from_robot(robot=robot, name='my_motor')

# Stop the motor.
await my_motor.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

**Example usage:**

```go
myMotor, err := motor.FromRobot(robot, "motor1")

// Stop the motor.
myMotor.Stop(context.TODO(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### IsPowered

Returns whether or not the motor is currently running, and the portion of max power (between 0 and 1; if the motor is off the power will be 0).
Stepper motors will report `true` if they are being powered while holding a position, as well as when they are turning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[bool](https://docs.python.org/3/library/functions.html#bool), [float](https://docs.python.org/3/library/functions.html#float)]: The bool is true if the motor is currently running; false if not.
The float represents the current portion of max power to the motor (between 0 and 1).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.is_powered).

**Example usage:**

```python
my_motor = Motor.from_robot(robot=robot, name='my_motor')

# Check whether the motor is currently running.
powered = await my_motor.is_powered()
print('Powered:', powered)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): True if the motor is currently running; false if not.
- [(float64)](https://pkg.go.dev/builtin#float64): The current portion of max power to the motor (between 0 and 1).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

**Example usage:**

```go
myMotor, err := motor.FromRobot(robot, "motor1")

// Check whether the motor is currently running.
powered, pct, _ := myMotor.IsPowered(context.TODO(), nil)
logger.Info("Is powered?")
logger.Info(powered)
logger.Info("Power percent:")
logger.Info(pct)
```

{{% /tab %}}
{{< /tabs >}}

### IsMoving

Returns whether the motor is actively moving (or attempting to move) under its own power.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(bool)](https://docs.python.org/3/library/functions.html#bool): True if the motor is currently moving; false if not.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.is_moving).

**Example usage:**

```python
my_motor = Motor.from_robot(robot=robot, name='my_motor')

# Check whether the motor is currently moving.
moving = await my_motor.is_moving()
print('Moving:', moving)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): True if the motor is currently moving.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#MovingCheckable).

**Example usage:**

```go
myMotor, err := motor.FromRobot(robot, "motor1")

// Check whether the motor is currently moving.
moving, _ := myMotor.IsMoving(context.TODO())
logger.Info("Is moving?")
logger.Info(moving)
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own motor and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (`Dict[str, Any]`): The command to execute.

**Returns:**

- `result` (`Dict[str, Any]`): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name='my_motor')

raw_dict = {
  "command": "raw",
  "raw_input": "home"
}
await my_motor.do_command(raw_dict)
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
myMotor, err := motor.FromRobot(robot, "motor1")

resp, err := myMotor.DoCommand(ctx, map[string]interface{}{"command": "jog", "raw_input": "home"})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/9be13108c8641b66fd4251a74ea638f47b040d62/components/motor/motor.go#L213).

{{% /tab %}}
{{< /tabs >}}

## Next Steps

{{< cards >}}
    {{% card link="/tutorials/yahboom-rover" size="small" %}}
    {{% card link="/tutorials/scuttlebot/scuttlebot" size="small" %}}
{{< /cards >}}
