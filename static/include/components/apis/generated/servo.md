### Move

Move the servo to the desired angle in degrees.

{{% alert title="Stability Notice" color="note" %}}
Support for continuous servos with the GPIO servo model is experimental.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.

If you are using a continuous rotation servo, you can use the `Move` command, but instead of moving to a given position, the servo will start moving at a set speed.

The speed will be related to the "angle" you pass in as a linear approximation.
90 degrees represents stop, 91 to 180 represents counter-clockwise rotation from slowest to fastest, and 89 to 1 represents clockwise from slowest to fastest.
It is recommended that you test your servo to determine the desired speed.

{{% /alert %}}
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `angle` ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (required): The desired angle of the servo in degrees.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name="my_servo")

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Move the servo from its origin to the desired angle of 90 degrees.
await my_servo.move(90)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.move).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `angleDeg` [(uint32)](https://pkg.go.dev/builtin#uint32): The desired angle of the servo in degrees.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Move the servo from its origin to the desired angle of 30 degrees.
myServoComponent.Move(context.Background(), 30, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `angle` [int](https://api.flutter.dev/flutter/dart-core/int-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Move the servo from its origin to the desired angle of 30 degrees.
await myServo.move(30);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Servo/move.html).

{{% /tab %}}
{{< /tabs >}}

### GetPosition

Get the current set angle of the servo in degrees.
Supported by `viam-micro-server`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([int](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)): The current angle of the servo in degrees.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name="my_servo")

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Get the current set angle of the servo.
pos1 = await my_servo.get_position()

# Move the servo from its origin to the desired angle of 20 degrees.
await my_servo.move(20)

# Get the current set angle of the servo.
pos2 = await my_servo.get_position()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.get_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(uint32)](https://pkg.go.dev/builtin#uint32): The current set angle of the servo in degrees.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current set angle of the servo.
pos1, err := myServoComponent.Position(context.Background(), nil)

// Move the servo from its origin to the desired angle of 20 degrees.
myServoComponent.Move(context.Background(), 20, nil)

// Get the current set angle of the servo.
pos2, err := myServoComponent.Position(context.Background(), nil)

logger.Info("Position 1: ", pos1)
logger.Info("Position 2: ", pos2)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/servo#Servo).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[int](https://api.flutter.dev/flutter/dart-core/int-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var angle = await myServo.position();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Servo/position.html).

{{% /tab %}}
{{< /tabs >}}

### IsMoving

Returns whether the servo is actively moving (or attempting to move) under its own power.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Whether the servo is moving.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_servo = Servo.from_robot(robot=robot, name="my_servo")

print(await my_servo.is_moving())
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.is_moving).

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

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[bool](https://api.flutter.dev/flutter/dart-core/bool-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var isItMoving = await myServo.isMoving();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Servo/isMoving.html).

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop the servo from moving.
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
my_servo = Servo.from_robot(robot=robot, name="my_servo")

# Move the servo from its origin to the desired angle of 10 degrees.
await my_servo.move(10)

# Stop the servo. It is assumed that the servo stops moving immediately.
await my_servo.stop()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.stop).

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
await myServo.stop();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Servo/stop.html).

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

### GetResourceName

Get the `ResourceName` for this servo with the given name.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_servo_name = Servo.get_resource_name("my_servo")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.get_resource_name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example:
var name = Servo.getResourceName('myServo');
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Servo/getResourceName.html).

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
await my_servo.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/servo/client/index.html#viam.components.servo.client.ServoClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myServo, err := servo.FromRobot(machine, "my_servo")

err = myServo.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
