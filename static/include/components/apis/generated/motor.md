### SetPower

Set the portion of max power to send to the motor (between `-1` and `1`).
A value of `1` represents 100% power forwards, while a value of `-1` represents 100% power backwards.

Power is expressed as a floating point between `-1` and `1` that scales between -100% and 100% power.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `power` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Power between -1 and 1 (negative implies backwards).
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Set the power to 40% forwards.
await my_motor.set_power(power=0.4)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.set_power).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `powerPct` [(float64)](https://pkg.go.dev/builtin#float64): Portion of full power to send to the motor expressed as a floating point between `-1` and `1`. A value of `1` represents 100% power forwards, while a value of `-1` represents 100% power backwards.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myMotorComponent, err := motor.FromRobot(machine, "my_motor")
// Set the motor power to 40% forwards.
myMotorComponent.SetPower(context.Background(), 0.4, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `powerPct` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Set the power to  40% forwards.
await myMotor.setPower(0.4);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/setPower.html).

{{% /tab %}}
{{< /tabs >}}

### SetRPM

Spin the motor indefinitely at the specified speed, in revolutions per minute. If `rpm` is positive, the motor will spin forwards, and if `rpm` is negative, the motor will spin backwards.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `rpm` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Speed at which the motor should rotate.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Spin the motor at 75 RPM.
await my_motor.set_rpm(rpm=75)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.set_rpm).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `rpm` [(float64)](https://pkg.go.dev/builtin#float64): The speed in RPM for the motor to move at.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Set the motor's RPM to 50
myMotorComponent.SetRPM(context.Background(), 50)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `rpm` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Set the motor to turn backwards at 120.5 RPM.
await myMotor.setRPM(-120.5);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/setRPM.html).

{{% /tab %}}
{{< /tabs >}}

### GoFor

Spin the motor the specified number of revolutions at specified revolutions per minute.
When `rpm` or `revolutions` is a negative value, the motor spins in the backward direction.
If both `rpm` and `revolutions` are negative, the motor spins in the forward direction.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `rpm` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Speed at which the motor should move in rotations per minute (negative implies backwards).
- `revolutions` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Number of revolutions the motor should run for (negative implies backwards).
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Turn the motor 7.2 revolutions at 60 RPM.
await my_motor.go_for(rpm=60, revolutions=7.2)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.go_for).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `rpm` [(float64)](https://pkg.go.dev/builtin#float64): Speed at which the motor should move in revolutions per minute (negative implies backwards).
- `revolutions` [(float64)](https://pkg.go.dev/builtin#float64): Number of revolutions the motor should run for (negative implies backwards). If revolutions is `0`, this runs the motor at `rpm` indefinitely. If revolutions not equal to `0`, this blocks until the number of revolutions has been completed or another operation comes in.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myMotorComponent, err := motor.FromRobot(machine, "my_motor")
// Turn the motor 7.2 revolutions at 60 RPM.
myMotorComponent.GoFor(context.Background(), 60, 7.2, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `rpm` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `revolutions` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Turn the motor 7.2 revolutions forward at 60 RPM.
await myMotor.goFor(60, 7.2);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/goFor.html).

{{% /tab %}}
{{< /tabs >}}

### GoTo

Turn the motor to a specified position (in terms of revolutions from home/zero) at a specified speed in revolutions per minute (RPM).
Regardless of the directionality of the `rpm`, the motor will move towards the specified target position.
This blocks until the position has been reached.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `rpm` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Speed at which the motor should rotate (absolute value).
- `position_revolutions` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): Target position relative to home/zero, in revolutions.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Turn the motor to 8.3 revolutions from home at 75 RPM.
await my_motor.go_to(rpm=75, revolutions=8.3)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.go_to).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `rpm` [(float64)](https://pkg.go.dev/builtin#float64): Speed at which the motor should move in revolutions per minute (absolute value).
- `positionRevolutions` [(float64)](https://pkg.go.dev/builtin#float64): Target position relative to home/zero, in revolutions.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Turn the motor to 8.3 revolutions from home at 75 RPM.
myMotorComponent.GoTo(context.Background(), 75, 8.3, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `rpm` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `positionRevolutions` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Turn the motor to 8.3 revolutions from home at 75 RPM.
await myMotor.goTo(75, 8.3);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/goTo.html).

{{% /tab %}}
{{< /tabs >}}

### ResetZeroPosition

Set the current position (modified by `offset`) to be the new zero (home) position.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `offset` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The offset from the current position to new home/zero position.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Set the current position as the new home position with no offset.
await my_motor.reset_zero_position(offset=0.0)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.reset_zero_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `offset` [(float64)](https://pkg.go.dev/builtin#float64): The offset from the current position to the new home (zero) position.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Set the current position as the new home position with no offset.
myMotorComponent.ResetZeroPosition(context.Background(), 0.0, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `offset` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Set the current position as the new home position with no offset.
await myMotor.resetZeroPosition(0.0);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/resetZeroPosition.html).

{{% /tab %}}
{{< /tabs >}}

### GetPosition

Report the position of the motor based on its encoder.
The value returned is the number of revolutions relative to its zero position.
This method raises an exception if position reporting is not supported by the motor.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): Number of revolutions the motor is away from zero/home.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Get the current position of the motor.
position = await my_motor.get_position()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.get_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(float64)](https://pkg.go.dev/builtin#float64): The unit returned is the number of revolutions which is intended to be fed back into calls of `GoFor`.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current position of an encoded motor.
position, err := myMotorComponent.Position(context.Background(), nil)

// Log the position
logger.Info("Position:")
logger.Info(position)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Get the current position of an encoded motor.
var position = await myMotor.position();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/position.html).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Report a dictionary mapping optional properties to whether it is supported by this motor.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.motor.motor.Motor.Properties](https://python.viam.dev/autoapi/viam/components/motor/motor/index.html#viam.components.motor.motor.Motor.Properties)): Map of feature names to supported status.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Report a dictionary mapping optional properties to whether it is supported by
# this motor.
properties = await my_motor.get_properties()

# Print out the properties.
print(f'Properties: {properties}')
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Properties)](https://pkg.go.dev/go.viam.com/rdk/components/motor#Properties): A map indicating whether or not the motor supports certain optional features.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Return whether or not the motor supports certain optional features.
properties, err := myMotorComponent.Properties(context.Background(), nil)

// Log the properties.
logger.Info("Properties:")
logger.Info(properties)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[MotorProperties](https://flutter.viam.dev/viam_sdk/MotorProperties.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Return whether the motor supports certain optional features
var properties = await myMotor.properties();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/properties.html).

{{% /tab %}}
{{< /tabs >}}

### IsPowered

Return whether or not the motor is currently running, and the portion of max power (between `0` and `1`; if the motor is off the power will be `0`).
Stepper motors will report `true` if they are being powered while holding a position, as well as when they are turning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[[bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool), [float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)]):  A tuple containing two values; the first [0] value indicates whether the motor is currently powered, andthe second [1] value indicates the current power percentage of the motor.   .

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Check whether the motor is currently running.
powered = await my_motor.is_powered()

print('Powered: ', powered)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.is_powered).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): `True` if the motor is currently running; `false` if not.
- [(float64)](https://pkg.go.dev/builtin#float64): The current portion of max power to the motor (between 0 and 1).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Check whether the motor is currently running.
powered, pct, err := myMotorComponent.IsPowered(context.Background(), nil)

logger.Info("Is powered?")
logger.Info(powered)
logger.Info("Power percent:")
logger.Info(pct)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/motor#Motor).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[PowerState](https://flutter.viam.dev/viam_sdk/PowerState-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Check whether the motor is currently powered and
// check the percentage of max power to the motor.
var powerState = await myMotor.powerState();
var powered = powerState.isOn;
var pct = powerState.powerPct;
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/powerState.html).

{{% /tab %}}
{{< /tabs >}}

### IsMoving

Return whether the motor is actively moving (or attempting to move) under its own power.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Whether the motor is moving.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Check whether the motor is currently moving.
moving = await my_motor.is_moving()
print('Moving: ', moving)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.is_moving).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): Whether this resource is moving (`true`) or not (`false`).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using IsMoving with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

// Stop all motion of the arm. It is assumed that the arm stops immediately.
myArm.Stop(context.Background(), nil)

// Log if the arm is currently moving.
is_moving, err := myArm.IsMoving(context.Background())
logger.Info(is_moving)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Actuator).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[bool](https://api.flutter.dev/flutter/dart-core/bool-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Check whether the motor is moving.
var moving = await myMotor.isMoving();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/isMoving.html).

{{% /tab %}}
{{< /tabs >}}

### Stop

Cut the power to the motor immediately, without any gradual step down.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor = Motor.from_robot(robot=robot, name="my_motor")

# Stop the motor.
await my_motor.stop()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.stop).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using Stop with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

// Stop all motion of the arm. It is assumed that the arm stops immediately.
err = myArm.Stop(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Actuator).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Stop the motor.
await myMotor.stop();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/stop.html).

{{% /tab %}}
{{< /tabs >}}

### Reconfigure

Reconfigure this resource.
Reconfigure must reconfigure the resource atomically and in place.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `deps` [(Dependencies)](https://pkg.go.dev/go.viam.com/rdk/resource#Dependencies): The resource dependencies.
- `conf` [(Config)](https://pkg.go.dev/go.viam.com/rdk/resource#Config): The resource configuration.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own motor and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example using doCommand with an arm component
const command = {'cmd': 'test', 'data1': 500};
var result = myArm.doCommand(command);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Resource/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this motor with the given name.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motor_name = Motor.get_resource_name("my_motor")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.get_resource_name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var name = Motor.getResourceName('myMotor');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Motor/getResourceName.html).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await my_motor.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/motor/client/index.html#viam.components.motor.client.MotorClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myMotor, err := motor.FromRobot(machine, "my_motor")

err = myMotor.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
