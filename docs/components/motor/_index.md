---
title: "Motor Component"
linkTitle: "Motor"
childTitleEndOverwrite: "Motor Component"
weight: 70
type: "docs"
description: "A motor is a rotating machine that transforms electrical energy into mechanical energy."
tags: ["motor", "components"]
icon: "/icons/components/motor.svg"
no_list: true
# SME: Rand
---

Electric motors are machines that convert electricity into rotary motion.
They are the most common form of [actuator](https://en.wikipedia.org/wiki/Actuator) in robotics.
The _motor_ component type natively supports brushed DC motors, brushless DC motors, and stepper motors controlled by a variety of [motor drivers](https://www.wellpcb.com/what-is-motor-driver.html).

Most robots with a motor need at least the following hardware:

- The motor itself.
- A compatible motor driver.
  This takes signals from the computer and sends the corresponding signals and power to the motor.
  Selected based on the type of motor (for example, brushed, brushless, or stepper) and its power requirements.
- A [board component](https://docs.viam.com/components/board/) to send signals to the motor driver[^dmcboard].
  For example, a Raspberry Pi, or another model of single-board computer with GPIO (general purpose input/output) pins.

[^dmcboard]: The `DMC4000` model does not require a board.

## Related Services

{{< cards >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< relatedcard link="/services/motion/" >}}
{{< relatedcard link="/services/navigation/" >}}
{{< relatedcard link="/services/slam/" >}}
{{< /cards >}}

## Supported Models

To use your motor with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your motor.

{{< readfile "/static/include/create-your-own-mr.md" >}}

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
Model | Description <a name="model-table"></a>
----- | -----------
[`gpio`](./gpio/) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor)
[`gpiostepper`](./gpiostepper/) | Bipolar stepper motor with current regulation and 1/32 microstepping driven by a basic driver like [DRV8825](https://www.ti.com/product/DRV8825) or [TMC2209](https://www.trinamic.com/support/eval-kits/details/tmc2209-bob/)
[`28byj48`](./28byj48/) | Small unipolar 28BYJ-48 stepper motor driven by a [ULN2003](https://www.ti.com/product/ULN2003A) driver
[`TMC5072`](./tmc5072/) | Stepper motor driven by [the TMC5072 chip](https://www.trinamic.com/support/eval-kits/details/tmc5072-bob/)
[`DMC4000`](./dmc4000/) | Stepper motor driven by a [DMC-40x0 series motion controller](https://www.galil.com/motion-controllers/multi-axis/dmc-40x0)
[`roboclaw`](./roboclaw/) | [Standard brushed DC motor](https://en.wikipedia.org/wiki/DC_motor) driven by [Basicmicro's](https://www.basicmicro.com/) [RoboClaw](https://www.basicmicro.com/RoboClaw-2x30A-Motor-Controller_p_9.html) motor controller
[`fake`](./fake/) | Used to test code without hardware

### Modular Resources

{{<modular-resources api="rdk:component:motor" type="motor">}}

### Micro-RDK

If you are using the micro-RDK, navigate to [Micro-RDK Motor](/micro-rdk/motor/) for supported model information.

## Control your motor with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have a motor called `"my_motor"` configured as a component of your robot.
If your motor has a different name, change the `name` in the code.

Be sure to import the motor package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.motor import Motor
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/motor"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The motor component supports the following methods:

{{< readfile "/static/include/components/apis/motor.md" >}}

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

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Set the power to 40% forwards.
await my_motor.set_power(power=0.4)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `powerPct` [(float64)](https://pkg.go.dev/builtin#float64): Portion of full power to send to the motor expressed as a floating point between -1 and 1. 1 is 100% power forwards; -1 is 100% power backwards.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

```go
myMotor, err := motor.FromRobot(robot, "my_motor")

// Set the motor power to 40% forwards.
myMotor.SetPower(context.Background(), 0.4, nil)

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

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

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
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

```go
myMotor, err := motor.FromRobot(robot, "my_motor")

// Turn the motor 7.2 revolutions at 60 RPM.
myMotor.GoFor(context.Background(), 60, 7.2, nil)
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

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Turn the motor to 8.3 revolutions from home at 75 RPM.
await my_motor.go_to(rpm=75, revolutions=8.3)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `rpm` [(float64)](https://pkg.go.dev/builtin#float64): Speed at which the motor should move in revolutions per minute (absolute value).
- `positionRevolutions` [(float64)](https://pkg.go.dev/builtin#float64): Target position relative to home/zero, in revolutions.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

```go
myMotor, err := motor.FromRobot(robot, "my_motor")

// Turn the motor to 8.3 revolutions from home at 75 RPM.
myMotor.GoTo(context.Background(), 75, 8.3, nil)
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

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Set the current position as the new home position with no offset.
await my_motor.reset_zero_position(offset=0.0)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `offset` [(float64)](https://pkg.go.dev/builtin#float64): The offset from the current position to the new home (zero) position.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

```go
myMotor, err := motor.FromRobot(robot, "my_motor")

// Set the current position as the new home position with no offset.
myMotor.ResetZeroPosition(context.Background(), 0.0, nil)
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

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Get the current position of the motor.
position = await my_motor.get_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The unit returned is the number of revolutions which is intended to be fed back into calls of GoFor.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

```go
myMotor, err := motor.FromRobot(robot, "my_motor")

// Get the current position of the motor.
position, err := myMotor.Position(context.Background(), nil)
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

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Report a dictionary mapping optional properties to whether it is supported by
# this motor.
properties = await my_motor.get_properties()

# Print out the properties.
print(f'Properties: {properties}')
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(map\[Feature\][bool])](https://pkg.go.dev/go.viam.com/rdk/components/motor#Feature): A map indicating whether or not the motor supports certain optional features.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

```go
myMotor, err := motor.FromRobot(robot, "my_motor")

// Return whether or not the motor supports certain optional features.
properties, err := myMotor.Properties(context.Background(), nil)

// Log the properties.
logger.Info("Properties:")
logger.Info(properties)
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

- [(tuple[bool, float])](https://docs.python.org/3/library/functions.html#bool): The bool is `true` if the motor is currently running; `false` if not.
  The float represents the current portion of max power to the motor (between 0 and 1).

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/index.html#viam.components.motor.Motor.is_powered).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Check whether the motor is currently running.
powered = await my_motor.is_powered()

print('Powered: ', powered)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): `True` if the motor is currently running; `false` if not.
- [(float64)](https://pkg.go.dev/builtin#float64): The current portion of max power to the motor (between 0 and 1).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

```go
myMotor, err := motor.FromRobot(robot, "my_motor")

// Check whether the motor is currently running.
powered, pct, err := myMotor.IsPowered(context.Background(), nil)

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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/motor/index.html#viam.components.motor.motor.Motor.is_moving).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Check whether the motor is currently moving.
moving = await my_motor.is_moving()
print('Moving: ', moving)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): True if the motor is currently moving.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/resource#MovingCheckable).

```go
myMotor, err := motor.FromRobot(robot, "my_motor")

// Check whether the motor is currently moving.
moving, err := myMotor.IsMoving(context.Background())

logger.Info("Is moving?")
logger.Info(moving)
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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/motor/index.html#viam.components.motor.motor.Motor.stop).

```python
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Stop the motor.
await my_motor.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

```go
myMotor, err := motor.FromRobot(robot, "my_motor")

// Stop the motor.
myMotor.Stop(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the motor in its current configuration, in the [frame](/services/frame-system/) of the motor.
The [motion](/services/motion/) and [navigation](/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for obstacle detection and avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[Geometry])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry): The geometries associated with the motor, in any order.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.get_geometries).

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

geometries = await my_motor.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's center point: {geometries[0].center}")
```

{{% /tab %}}

<!-- Go tab

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [`[]spatialmath.Geometry`](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): The geometries associated with the motor, in any order.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Shaped).

```go {class="line-numbers linkable-line-numbers"}
myMotor, err := motor.FromRobot(robot, "my_motor")

geometries, err := myMotor.Geometries(context.Background(), nil)

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
If you are implementing your own motor and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

raw_dict = {
  "command": "raw",
  "raw_input": "home"
}

await my_motor.do_command(raw_dict)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map\[string\]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myMotor, err := motor.FromRobot(robot, "my_motor")

resp, err := myMotor.DoCommand(ctx, map[string]interface{}{"command": "jog", "raw_input": "home"})
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/main/resource/resource.go).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next Steps

{{< cards >}}
{{% card link="/tutorials/get-started/confetti-bot/" %}}
{{% card link="/tutorials/get-started/lazy-susan/" %}}
{{% card link="/tutorials/control/yahboom-rover" %}}
{{% card link="/tutorials/configure/scuttlebot" %}}
{{< /cards >}}
