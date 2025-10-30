### Open

Opens the gripper.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=machine, name="my_gripper")

# Open the gripper.
await my_gripper.open()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.open).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGripper, err := gripper.FromProvider(machine, "my_gripper")

// Open the gripper.
err := myGripper.Open(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const gripper = new VIAM.GripperClient(machine, 'my_gripper');

// Open the gripper
await gripper.open();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GripperClient.html#open).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
await myGripper.open();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gripper/open.html).

{{% /tab %}}
{{< /tabs >}}

### Grab

Closes the gripper until it grabs something or closes completely, and returns whether it grabbed something or not.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Indicates if the gripper grabbed something.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=machine, name="my_gripper")

# Grab with the gripper.
grabbed = await my_gripper.grab()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.grab).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool):  True if the gripper grabbed something with non-zero thickness.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGripper, err := gripper.FromProvider(machine, "my_gripper")

// Grab with the gripper.
grabbed, err := myGripper.Grab(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const gripper = new VIAM.GripperClient(machine, 'my_gripper');

// Close the gripper to grab
await gripper.grab();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GripperClient.html#grab).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
await myGripper.grab();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gripper/grab.html).

{{% /tab %}}
{{< /tabs >}}

### IsMoving

Returns whether the gripper is actively moving (or attempting to move) under its own power.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Whether the gripper is moving.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=machine, name="my_gripper")

# Check whether the gripper is currently moving.
moving = await my_gripper.is_moving()
print('Moving:', moving)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.is_moving).

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
const gripper = new VIAM.GripperClient(machine, 'my_gripper');

// Check if the gripper is currently moving
const moving = await gripper.isMoving();
console.log('Gripper is moving:', moving);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GripperClient.html#ismoving).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[bool](https://api.flutter.dev/flutter/dart-core/bool-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var isItMoving = await myGripper.isMoving();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gripper/isMoving.html).

{{% /tab %}}
{{< /tabs >}}

### IsHoldingSomething

Return if the gripper is holding something.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.gripper.gripper.Gripper.HoldingStatus](https://python.viam.dev/autoapi/viam/components/gripper/gripper/index.html#viam.components.gripper.gripper.Gripper.HoldingStatus)): see documentation on HoldingStatus for more information.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=machine, name="my_gripper")

# Grab with the gripper.
holding_status = await my_gripper.is_holding_something()
# get the boolean result
is_holding_something = holding_status.is_holding_something
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.is_holding_something).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(HoldingStatus)](https://pkg.go.dev/go.viam.com/rdk/components/gripper#HoldingStatus)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/gripper#Gripper).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[HoldingStatus](https://flutter.viam.dev/viam_sdk/HoldingStatus-class.html)\>

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gripper/isHoldingSomething.html).

{{% /tab %}}
{{< /tabs >}}

### Stop

Stops the gripper.
It is assumed that the gripper stops immediately, so `IsMoving` will return false after calling `Stop`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=machine, name="my_gripper")

# Stop the gripper.
await my_gripper.stop()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.stop).

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
const gripper = new VIAM.GripperClient(machine, 'my_gripper');

// Stop the gripper's current motion
await gripper.stop();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GripperClient.html#stop).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
await myGripper.stop();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gripper/stop.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the gripper in its current configuration, in the [frame](/operate/reference/services/frame-system/) of the gripper.
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
my_gripper = Gripper.from_robot(robot=machine, name="my_gripper")
geometries = await my_gripper.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.get_geometries).

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
// This example shows using Geometries with an gripper component.
myGripper, err := gripper.FromProvider(machine, "my_gripper")

geometries, err := myGripper.Geometries(context.Background(), nil)

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
const gripper = new VIAM.GripperClient(machine, 'my_gripper');

// Get the geometries of this component
const geometries = await gripper.getGeometries();
console.log('Geometries:', geometries);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GripperClient.html#getgeometries).

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
If you are implementing your own gripper and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

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
my_gripper = Gripper.from_robot(robot=machine, name="my_gripper")
command = {"cmd": "test", "data1": 500}
result = await my_gripper.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.do_command).

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
myGripper, err := gripper.FromProvider(machine, "my_gripper")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myGripper.DoCommand(context.Background(), command)
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

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GripperClient.html#docommand).

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

Get the kinematics information associated with the gripper as the format and byte contents of the [kinematics file](/operate/reference/kinematic-chain-config/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[viam.components.gripper.KinematicsFileFormat.ValueType, [bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)]): A tuple containing two values; the first \[0] value represents the format of the
file, either in URDF format (`KinematicsFileFormat.KINEMATICS_FILE_FORMAT_URDF`) or
Viam’s kinematic parameter format (spatial vector algebra) (`KinematicsFileFormat.KINEMATICS_FILE_FORMAT_SVA`),
and the second \[1] value represents the byte contents of the file.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gripper = Gripper.from_robot(robot=machine, name="my_gripper")

# Get the kinematics information associated with the gripper.
kinematics = await my_gripper.get_kinematics()

# Get the format of the kinematics file.
k_file = kinematics[0]

# Get the byte contents of the file.
k_bytes = kinematics[1]
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.get_kinematics).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(referenceframe.Model)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#Model): The kinematics model of the resource.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot/framesystem#InputEnabled).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[Kinematics](https://flutter.viam.dev/viam_sdk/Kinematics-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var kinematics = await myGripper.getKinematics();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gripper/getKinematics.html).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this gripper.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_gripper_name = Gripper.get_resource_name("my_gripper")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGripper, err := gripper.FromProvider(machine, "my_gripper")

err = myGripper.Name()
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
gripper.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/GripperClient.html#name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
final myGripperResourceName = myGripper.getResourceName("my_gripper");
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Gripper/getResourceName.html).

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
my_gripper = Gripper.from_robot(robot=machine, name="my_gripper")
await my_gripper.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/gripper/client/index.html#viam.components.gripper.client.GripperClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myGripper, err := gripper.FromProvider(machine, "my_gripper")

err = myGripper.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
