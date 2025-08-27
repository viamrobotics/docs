### GetPosition

Get the current positions of the axis of the gantry (mm).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (List[[float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)]): A list of the position of the axes of the gantry in millimeters.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=machine, name="my_gantry")

# Get the current positions of the axes of the gantry in millimeters.
positions = await my_gantry.get_position()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.get_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]float64)](https://pkg.go.dev/builtin#float64): A list of the position of the axes of the gantry in millimeters.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGantry, err := gantry.FromRobot(machine, "my_gantry")

// Get the current positions of the axes of the gantry in millimeters.
position, err := myGantry.Position(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<number[]>): A list of the current position of each axis in millimeters.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const gantry = new VIAM.GantryClient(machine, 'my_gantry');

// Get the current positions of the axes in millimeters
const positions = await gantry.getPosition();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GantryClient.html#getposition).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var position = await myGantry.position();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gantry/position.html).

{{% /tab %}}
{{< /tabs >}}

### MoveToPosition

Move the axes of the gantry to the desired positions (mm) at the requested speeds (mm/sec).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `positions` (List[[float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)]) (required): A list of positions for the axes of the gantry to move to, in millimeters.
- `speeds` (List[[float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)]) (required): A list of speeds in millimeters per second for the gantry to move at respective to each axis.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=machine, name="my_gantry")

# Create a list of positions for the axes of the gantry to move to. Assume in
# this example that the gantry is multi-axis, with 3 axes.
examplePositions = [1, 2, 3]

exampleSpeeds = [3, 9, 12]

# Move the axes of the gantry to the positions specified.
await my_gantry.move_to_position(
    positions=examplePositions, speeds=exampleSpeeds)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.move_to_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positionsMm` [([]float64)](https://pkg.go.dev/builtin#float64): A list of positions for the axes of the gantry to move to, in millimeters.
- `speedsMmPerSec` [([]float64)](https://pkg.go.dev/builtin#float64): A list of speeds in millimeters per second for the gantry to move at respective to each axis.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGantry, err := gantry.FromRobot(machine, "my_gantry")

// Create a list of positions for the axes of the gantry to move to.
// Assume in this example that the gantry is multi-axis, with 3 axes.
examplePositions := []float64{1, 2, 3}

exampleSpeeds := []float64{3, 9, 12}

// Move the axes of the gantry to the positions specified.
myGantry.MoveToPosition(context.Background(), examplePositions, exampleSpeeds, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `positionsMm` (number) (required): The goal positions for each axis of the gantry.
- `speedsMmPerSec` (number) (required): The desired speed for each axis to move to the
  respective position in positionsMm.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const gantry = new VIAM.GantryClient(machine, 'my_gantry');

// Create positions for a 3-axis gantry
const positions = [1, 2, 3];
const speeds = [3, 9, 12];

// Move the axes to the specified positions
await gantry.moveToPosition(positions, speeds);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GantryClient.html#movetoposition).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `positions` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)\> (required)
- `speeds` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)\> (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
await myGantry.moveToPosition([0.0, 20.5], [15, 15]);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gantry/moveToPosition.html).

{{% /tab %}}
{{< /tabs >}}

### GetLengths

Get the lengths of the axes of the gantry (mm).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (List[[float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)]): A list of the lengths of the axes of the gantry in millimeters.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=machine, name="my_gantry")

# Get the lengths of the axes of the gantry in millimeters.
lengths_mm = await my_gantry.get_lengths()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.get_lengths).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]float64)](https://pkg.go.dev/builtin#float64): A list of the lengths of the axes of the gantry in millimeters.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGantry, err := gantry.FromRobot(machine, "my_gantry")

// Get the lengths of the axes of the gantry in millimeters.
lengths_mm, err := myGantry.Lengths(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<number[]>): A list of the length of each axis in millimeters.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const gantry = new VIAM.GantryClient(machine, 'my_gantry');

// Get the lengths of the axes in millimeters
const lengths = await gantry.getLengths();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GantryClient.html#getlengths).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var lengths = await myGantry.lengths();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gantry/lengths.html).

{{% /tab %}}
{{< /tabs >}}

### Home

Run the homing sequence of the gantry to re-calibrate the axes with respect to the limit switches.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Whether the gantry has run the homing sequence successfully.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=machine, name="my_gantry")

await my_gantry.home()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.home).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): Whether the gantry has run the homing sequence successfully.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGantry, err := gantry.FromRobot(machine, "my_gantry")

myGantry.Home(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gantry#Gantry).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<boolean>): A bool representing whether the gantry has run the homing sequence
successfully.

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const gantry = new VIAM.GantryClient(machine, 'my_gantry');

// Run the homing sequence
const success = await gantry.home();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GantryClient.html#home).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[bool](https://api.flutter.dev/flutter/dart-core/bool-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var homed = await myGantry.home();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gantry/home.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the gantry in its current configuration, in the [frame](/operate/reference/services/frame-system/) of the gantry.
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
my_gantry = Gantry.from_robot(robot=machine, name="my_gantry")
geometries = await my_gantry.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.get_geometries).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[commonApi](https://ts.viam.dev/modules/commonApi.html).[Geometry](https://ts.viam.dev/classes/commonApi.Geometry.html)[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const gantry = new VIAM.GantryClient(machine, 'my_gantry');

// Get the geometries of this component
const geometries = await gantry.getGeometries();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GantryClient.html#getgeometries).

{{% /tab %}}
{{< /tabs >}}

### IsMoving

Get if the gantry is currently moving.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Whether the gantry is moving.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=machine, name="my_gantry")

# Stop all motion of the gantry. It is assumed that the
# gantry stops immediately.
await my_gantry.stop()

# Print if the gantry is currently moving.
print(await my_gantry.is_moving())
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.is_moving).

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
{{% tab name="TypeScript" %}}

**Parameters:**

- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<boolean>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const gantry = new VIAM.GantryClient(machine, 'my_gantry');

// Check if the gantry is moving
const moving = await gantry.isMoving();
console.log('Moving:', moving);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GantryClient.html#ismoving).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[bool](https://api.flutter.dev/flutter/dart-core/bool-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var moving = await myGantry.isMoving();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gantry/isMoving.html).

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop all motion of the gantry.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gantry = Gantry.from_robot(robot=machine, name="my_gantry")

# Stop all motion of the gantry. It is assumed that the gantry stops
# immediately.
await my_gantry.stop()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.stop).

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
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const gantry = new VIAM.GantryClient(machine, 'my_gantry');

// Stop all motion of the gantry
await gantry.stop();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GantryClient.html#stop).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
await myGantry.stop();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gantry/stop.html).

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
If you are implementing your own gantry and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

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
my_gantry = Gantry.from_robot(robot=machine, name="my_gantry")
command = {"cmd": "test", "data1": 500}
result = await my_gantry.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.do_command).

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
myGantry, err := gantry.FromRobot(machine, "my_gantry")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myGantry.DoCommand(context.Background(), command)
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

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GantryClient.html#docommand).

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

### GetKinematics

Get the kinematics information associated with the gantry.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(referenceframe.Model)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#Model): The kinematics model of the resource.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot/framesystem#InputEnabled).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this gantry.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gantry_name = Gantry.get_resource_name("my_gantry")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGantry, err := gantry.FromRobot(machine, "my_gantry")

err = myGantry.Name()
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
gantry.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GantryClient.html#name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
final myGantryResourceName = myGantry.getResourceName("my_gantry");
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gantry/getResourceName.html).

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
my_gantry = Gantry.from_robot(robot=machine, name="my_gantry")
await my_gantry.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gantry/client/index.html#viam.components.gantry.client.GantryClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGantry, err := gantry.FromRobot(machine, "my_gantry")

err = myGantry.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
