### MoveStraight

Move the base in a straight line across the given distance (mm) at the given velocity (mm/sec).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `distance` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The distance (in millimeters) to move. Negative implies backwards.
- `velocity` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The velocity (in millimeters per second) to move. Negative implies backwards.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=machine, name="my_base")

# Move the base 40 mm at a velocity of 90 mm/s, forward.
await my_base.move_straight(distance=40, velocity=90)

# Move the base 40 mm at a velocity of -90 mm/s, backward.
await my_base.move_straight(distance=40, velocity=-90)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.move_straight).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `distanceMm` [(int)](https://pkg.go.dev/builtin#int): The distance to move the base in millimeters. Positive implies forwards. Negative implies backwards.
- `mmPerSec` [(float64)](https://pkg.go.dev/builtin#float64): The velocity at which to move the base in millimeters per second. Positive implies forwards. Negative implies backwards.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromProvider(machine, "my_base")
// Move the base forward 40 mm at a velocity of 90 mm/s.
myBase.MoveStraight(context.Background(), 40, 90, nil)

// Move the base backward 40 mm at a velocity of -90 mm/s.
myBase.MoveStraight(context.Background(), 40, -90, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `distanceMm` (number) (required): Distance to move, in millimeters.
- `mmPerSec` (number) (required): Movement speed, in millimeters per second.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const base = new VIAM.BaseClient(machine, 'my_base');

// Move forward 40mm at 90mm/s
await base.moveStraight(40, 90);

// Move backward 40mm at -90mm/s (backwards)
await base.moveStraight(40, -90);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BaseClient.html#movestraight).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `distance` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)
- `velocity` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Move the base 40mm forward at 90 mm/s
await myBase.moveStraight(40, 90);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Base/moveStraight.html).

{{% /tab %}}
{{< /tabs >}}

### Spin

Turn the base in place, rotating it to the given angle (degrees) at the given angular velocity (degrees/sec).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `angle` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The angle (in degrees) to spin.
- `velocity` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The angular velocity (in degrees per second) to spin. Given a positive angle and a positive velocity, the base will turn to the left.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=machine, name="my_base")

# Spin the base 10 degrees at an angular velocity of 15 deg/sec.
await my_base.spin(angle=10, velocity=15)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.spin).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `angleDeg` [(float64)](https://pkg.go.dev/builtin#float64): The angle to spin in degrees. Positive implies turning to the left.
- `degsPerSec` [(float64)](https://pkg.go.dev/builtin#float64): The angular velocity at which to spin in degrees per second. Given a positive angle and a positive velocity, the base turns to the left (for built-in base models).
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromProvider(machine, "my_base")

// Spin the base 10 degrees at an angular velocity of 15 deg/sec.
myBase.Spin(context.Background(), 10, 15, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `angleDeg` (number) (required): Degrees to spin.
- `degsPerSec` (number) (required): Angular speed, in degrees per second.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const base = new VIAM.BaseClient(machine, 'my_base');

// Spin 10 degrees clockwise at 15 degrees per second
await base.spin(10, 15);

// Spin 180 degrees counter-clockwise at 20 degrees per second
await base.spin(-180, 20);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BaseClient.html#spin).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `angle` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `velocity` [double](https://api.flutter.dev/flutter/dart-core/double-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Spin the base 10 degrees at 15 deg/s
await myBase.spin(10, 15);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Base/spin.html).

{{% /tab %}}
{{< /tabs >}}

### SetPower

Set the linear and angular power of the base, represented as a percentage of max power for each direction in the range of [-1.0 to 1.0].
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `linear` ([viam.components.base.Vector3](https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Vector3)) (required): The linear component. Only the Y component is used for wheeled base. Positive implies forwards.
- `angular` ([viam.components.base.Vector3](https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Vector3)) (required): The angular component. Only the Z component is used for wheeled base. Positive turns left; negative turns right.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=machine, name="my_base")

# Make your wheeled base move forward. Set linear power to 75%.
print("move forward")
await my_base.set_power(
    linear=Vector3(x=0, y=.75, z=0),
    angular=Vector3(x=0, y=0, z=0))

# Make your wheeled base move backward. Set linear power to -100%.
print("move backward")
await my_base.set_power(
    linear=Vector3(x=0, y=-1.0, z=0),
    angular=Vector3(x=0, y=0, z=0))

# Make your wheeled base spin left. Set angular power to 100%.
print("spin left")
await my_base.set_power(
    linear=Vector3(x=0, y=0, z=0),
    angular=Vector3(x=0, y=0, z=1))

# Make your wheeled base spin right. Set angular power to -75%.
print("spin right")
await my_base.set_power(
    linear=Vector3(x=0, y=0, z=0),
    angular=Vector3(x=0, y=0, z=-.75))
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_power).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `linear` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The percentage of max power of the base's linear propulsion. In the range of -1.0 to 1.0, with 1.0 meaning 100% power. Viam's coordinate system considers +Y to be the forward axis (+/- X right/left, +/- Z up/down), so use the Y component of this vector to move forward and backward when controlling a wheeled base. Positive "Y" values imply moving forwards. Negative "Y" values imply moving backwards.
- `angular` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The percentage of max power of the base's angular propulsion. In the range of -1.0 to 1.0, with 1.0 meaning 100% power. Use the Z component of this vector to spin left or right when controlling a wheeled base. Positive "Z" values imply spinning to the left (for built-in base models).
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromProvider(machine, "my_base")

// Make your wheeled base move forward. Set linear power to 75%.
logger.Info("move forward")
err = myBase.SetPower(context.Background(), r3.Vector{Y: .75}, r3.Vector{}, nil)

// Make your wheeled base move backward. Set linear power to -100%.
logger.Info("move backward")
err = myBase.SetPower(context.Background(), r3.Vector{Y: -1}, r3.Vector{}, nil)

// Make your wheeled base spin left. Set angular power to 100%.
logger.Info("spin left")
err = myBase.SetPower(context.Background(), r3.Vector{}, r3.Vector{Z: 1}, nil)

// Make your wheeled base spin right. Set angular power to -75%.
logger.Info("spin right")
err = myBase.SetPower(context.Background(), r3.Vector{}, r3.Vector{Z: -.75}, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `linear` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (required): Desired linear power percentage from \-1 to 1\.
- `angular` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (required): Desired angular power percentage from \-1 to 1\.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const base = new VIAM.BaseClient(machine, 'my_base');

// Move forward at 75% power
await base.setPower(
  { x: 0, y: 0.75, z: 0 }, // linear power
  { x: 0, y: 0, z: 0 } // no rotation
);

// Move straight back at 100% power
await base.setPower(
  { x: 0, y: -1, z: 0 }, // linear power
  { x: 0, y: 0, z: 0 } // no rotation
);

// Turn counter-clockwise at 50% power
await base.setPower(
  { x: 0, y: 0, z: 0 }, // no linear movement
  { x: 0, y: 0, z: 0.5 } // rotate around z-axis
);

// Turn clockwise at 60% power
await base.setPower(
  { x: 0, y: 0, z: 0 }, // no linear movement
  { x: 0, y: 0, z: -0.6 } // rotate around z-axis
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BaseClient.html#setpower).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `linear` [Vector3](https://flutter.viam.dev/viam_sdk/Vector3-class.html) (required)
- `angular` [Vector3](https://flutter.viam.dev/viam_sdk/Vector3-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Move the base straight forward at 75% power:
await myBase.setPower(Vector3(0, 0.75, 0), Vector3());

// Move the base straight backward at 100% power:
await myBase.setPower(Vector3(0, -1, 0), Vector3());

// Turn the base to the left at 50% power:
await myBase.setPower(Vector3(), Vector3(0, 0, 0.5));

// Turn the base to the right at 60% power:
await myBase.setPower(Vector3(), Vector3(0, 0, -0.6));
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Base/setPower.html).

{{% /tab %}}
{{< /tabs >}}

### SetVelocity

Set the linear velocity (mm/sec) and angular velocity (degrees/sec) of the base.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `linear` ([viam.components.base.Vector3](https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Vector3)) (required): Velocity in mm/sec.
- `angular` ([viam.components.base.Vector3](https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Vector3)) (required): Velocity in deg/sec.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=machine, name="my_base")

# Set the linear velocity to 50 mm/sec and the angular velocity to
# 15 degree/sec.
await my_base.set_velocity(
    linear=Vector3(x=0, y=50, z=0), angular=Vector3(x=0, y=0, z=15))
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.set_velocity).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `linear` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The linear velocity in millimeters per second. Only the Y component of the vector is used for a wheeled base.
- `angular` [(r3.Vector)](https://pkg.go.dev/github.com/golang/geo/r3#Vector): The angular velocity in degrees per second. Only the Z component of the vector is used for a wheeled base.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromProvider(machine, "my_base")

// Set the linear velocity to 50 mm/sec and the angular velocity to 15 deg/sec.
myBase.SetVelocity(context.Background(), r3.Vector{Y: 50}, r3.Vector{Z: 15}, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `linear` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (required): Desired linear velocity in millimeters per second.
- `angular` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (required): Desired angular velocity in degrees per second.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const base = new VIAM.BaseClient(machine, 'my_base');

// Move forward at 50mm/s while spinning 15 degrees per second to the left
await base.setVelocity(
  { x: 0, y: 50, z: 0 }, // linear velocity in mm/s
  { x: 0, y: 0, z: 15 } // 15 degrees per second counter-clockwise
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BaseClient.html#setvelocity).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `linear` [Vector3](https://flutter.viam.dev/viam_sdk/Vector3-class.html) (required)
- `angular` [Vector3](https://flutter.viam.dev/viam_sdk/Vector3-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Set the linear velocity to 50mm/s forward, and the angular velocity
to 15 deg/s counterclockwise
//
await myBase.setVelocity(Vector3(0, 50, 0), Vector3(0, 0, 15));
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Base/setVelocity.html).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get the width and turning radius of the {{< glossary_tooltip term_id="model" text="model" >}} of base in meters.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.base.Base.Properties](https://python.viam.dev/autoapi/viam/components/base/index.html#viam.components.base.Base.Properties)): The properties of the base.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=machine, name="my_base")

# Get the width and turning radius of the base
properties = await my_base.get_properties()

# Get the width
print(f"Width of base: {properties.width_meters}")

# Get the turning radius
print(f"Turning radius of base: {properties.turning_radius_meters}")

# Get the wheel circumference
print(f"Wheel circumference of base: {properties.wheel_circumference_meters}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(Properties)](https://pkg.go.dev/go.viam.com/rdk/components/base#Properties): A structure with three fields, `WidthMeters`, `TurningRadiusMeters`, and `WheelCircumferenceMeters` representing the width, turning radius, and wheel circumference of the physical base in meters _(m)_.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromProvider(machine, "my_base")

// Get the width and turning radius of the base
properties, err := myBase.Properties(context.Background(), nil)

// Get the width
myBaseWidth := properties.WidthMeters

// Get the turning radius
myBaseTurningRadius := properties.TurningRadiusMeters

// Get the wheel circumference
myBaseWheelCircumference := properties.WheelCircumferenceMeters
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/base#Base).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[baseApi](https://ts.viam.dev/modules/baseApi.html).[GetPropertiesResponse](https://ts.viam.dev/classes/baseApi.GetPropertiesResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const base = new VIAM.BaseClient(machine, 'my_base');
const properties = await base.getProperties();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BaseClient.html#getproperties).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[BaseProperties](https://flutter.viam.dev/viam_sdk/BaseProperties.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
final myBaseResourceName = myBase.getResourceName("my_base");
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Base/properties.html).

{{% /tab %}}
{{< /tabs >}}

### IsMoving

Returns whether the base is actively moving (or attempting to move) under its own power.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Whether the base is moving.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=machine, name="my_base")

# Check whether the base is currently moving.
moving = await my_base.is_moving()
print('Moving: ', moving)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.is_moving).

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
myArm, err := arm.FromProvider(machine, "my_arm")

// Stop all motion of the arm. It is assumed that the arm stops immediately.
myArm.Stop(context.Background(), nil)

// Log if the arm is currently moving.
is_moving, err := myArm.IsMoving(context.Background())
logger.Info(is_moving)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Actuator).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<boolean>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const base = new VIAM.BaseClient(machine, 'my_base');
const moving = await base.isMoving();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BaseClient.html#ismoving).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[bool](https://api.flutter.dev/flutter/dart-core/bool-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
bool baseIsMoving = await myBase.isMoving();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Base/isMoving.html).

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop the base from moving immediately.
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
my_base = Base.from_robot(robot=machine, name="my_base")

# Move the base forward 10 mm at a velocity of 50 mm/s.
await my_base.move_straight(distance=10, velocity=50)

# Stop the base.
await my_base.stop()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.stop).

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
myArm, err := arm.FromProvider(machine, "my_arm")

// Stop all motion of the arm. It is assumed that the arm stops immediately.
err = myArm.Stop(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Actuator).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const base = new VIAM.BaseClient(machine, 'my_base');
await base.stop();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BaseClient.html#stop).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
await myBase.stop();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Base/stop.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the base in its current configuration, in the [frame](/operate/reference/services/frame-system/) of the base.
The [motion](/operate/reference/services/motion/) and [navigation](/operate/reference/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry)): The geometries associated with the Component.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=machine, name="my_base")
geometries = await my_base.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.get_geometries).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]spatialmath.Geometry)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): The geometries associated with this resource, in any order.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// This example shows using Geometries with an base component.
myBase, err := base.FromProvider(machine, "my_base")

geometries, err := myBase.Geometries(context.Background(), nil)

if len(geometries) > 0 {
   // Get the center of the first geometry
   elem := geometries[0]
   fmt.Println("Pose of the first geometry's center point:", elem.Pose())
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Shaped).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[commonApi](https://ts.viam.dev/modules/commonApi.html).[Geometry](https://ts.viam.dev/classes/commonApi.Geometry.html)[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const base = new VIAM.BaseClient(machine, 'my_base');
const geometries = await base.getGeometries();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BaseClient.html#getgeometries).

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
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own base and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Raises:**

- (NotImplementedError): Raised if the Resource does not support arbitrary commands.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_base = Base.from_robot(robot=machine, name="my_base")
command = {"cmd": "test", "data1": 500}
result = await my_base.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): The command response.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromRobot(machine, "my_base")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myBase.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `command` ([Struct](https://ts.viam.dev/classes/Struct.html)) (required): The command to execute.
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[JsonValue](https://ts.viam.dev/types/JsonValue.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
import { Struct } from '@viamrobotics/sdk';

const result = await resource.doCommand(
  Struct.fromJson({
    myCommand: { key: 'value' },
  })
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BaseClient.html#docommand).

{{% /tab %}}
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

Get the `ResourceName` for this base.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_base_name = Base.get_resource_name("my_base")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromRobot(machine, "my_base")

err = myBase.Name()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (string): The name of the resource.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
base.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/BaseClient.html#name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Base/getResourceName.html).

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
my_base = Base.from_robot(robot=machine, name="my_base")
await my_base.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/base/client/index.html#viam.components.base.client.BaseClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myBase, err := base.FromRobot(machine, "my_base")

err = myBase.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
