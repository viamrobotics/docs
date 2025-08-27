### GetEndPosition

Get the current position of the arm as a [pose](/operate/mobility/orientation-vector/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.arm.Pose](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Pose)): A representation of the arm’s current position as a 6 DOF (six degrees of freedom) pose.
The `Pose` is composed of values for location and orientation with respect to the origin.
Location is expressed as distance, which is represented by x, y, and z coordinate values.
Orientation is expressed as an orientation vector, which is represented by o\_x, o\_y, o\_z, and theta values.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=machine, name="my_arm")

# Get the end position of the arm as a Pose.
pos = await my_arm.get_end_position()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_end_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose. The `Pose` is composed of values for location and orientation with respect to the origin. Location is expressed as distance, which is represented by x, y, and z coordinate values. Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(machine, "my_arm")
// Get the end position of the arm as a Pose.
pos, err := myArm.EndPosition(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[commonApi](https://ts.viam.dev/modules/commonApi.html).[Pose](https://ts.viam.dev/classes/commonApi.Pose.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const arm = new VIAM.ArmClient(machine, 'my_arm');
const pose = await arm.getEndPosition();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/ArmClient.html#getendposition).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[Pose](https://flutter.viam.dev/viam_sdk/Pose-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
final currentPose = await myArm.endPosition();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/endPosition.html).

{{% /tab %}}
{{< /tabs >}}

### MoveToPosition

Move the end of the arm in a straight line to the desired [pose](/operate/mobility/orientation-vector/), relative to the base of the arm.

All arms have a `Home` position, which corresponds to setting all joint angles to 0.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `pose` ([viam.components.arm.Pose](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Pose)) (required): The destination Pose for the arm. The Pose is composed of values for location and orientation with respect to the origin. Location is expressed as distance, which is represented by x, y, and z coordinate values. Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=machine, name="my_arm")

# Create a Pose for the arm.
examplePose = Pose(x=5, y=5, z=5, o_x=5, o_y=5, o_z=5, theta=20)

# Move your arm to the Pose.
await my_arm.move_to_position(pose=examplePose)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.move_to_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `pose` [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): A representation of the arm's destination position as a 6 DOF (six degrees of freedom) pose. The `Pose` is composed of values for location and orientation with respect to the origin. Location is expressed as distance, which is represented by x, y, and z coordinate values. Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(machine, "my_arm")
// Create a Pose for the arm.
examplePose := spatialmath.NewPose(
        r3.Vector{X: 5, Y: 5, Z: 5},
        &spatialmath.OrientationVectorDegrees{OX: 5, OY: 5, Theta: 20},
)

// Move your arm to the Pose.
err = myArm.MoveToPosition(context.Background(), examplePose, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `pose` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (required): The destination pose for the arm.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const arm = new VIAM.ArmClient(machine, 'my_arm');

// Create a pose for the arm to move to
const pose: Pose = {
  x: -500,
  y: -200,
  z: 62,
  oX: 1,
  oY: 0,
  oZ: 1,
  theta: 90,
};

// Move the arm to the pose
await arm.moveToPosition(pose);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/ArmClient.html#movetoposition).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `pose` [Pose](https://flutter.viam.dev/viam_sdk/Pose-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Create a pose for the arm to move to
final targetPose = Pose.fromBuffer([12, 0, 400, 0, 0, 1, 90]);

// Move the arm to the pose
await myArm.moveToPosition(targetPose);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/moveToPosition.html).

{{% /tab %}}
{{< /tabs >}}

### MoveToJointPositions

Move each joint on the arm to the position specified in `positions`.

{{% alert title="Caution" color="caution" %}}

Collision checks are not enabled when doing direct joint control with MoveToJointPositions().

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `positions` ([viam.proto.component.arm.JointPositions](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.JointPositions)) (required): The destination JointPositions for the arm.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=machine, name="my_arm")

# Declare a list of values with your desired rotational value for each joint on
# the arm. This example is for a 5dof arm.
degrees = [0.0, 45.0, 0.0, 0.0, 0.0]

# Declare a new JointPositions with these values.
jointPos = JointPositions(values=degrees)

# Move each joint of the arm to the position these values specify.
await my_arm.move_to_joint_positions(positions=jointPos)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.move_to_joint_positions).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positions` [([]referenceframe.Input)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#Input)
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(machine, "my_arm")

// Declare an array of values with your desired rotational value (in radians) for each joint on the arm.
inputs := referenceframe.FloatsToInputs([]float64{0, math.Pi/2, math.Pi})

// Move each joint of the arm to the positions specified in the above slice
err = myArm.MoveToJointPositions(context.Background(), inputs, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `jointPositionsList` (number) (required): List of angles (0\-360\) to move each joint to.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const arm = new VIAM.ArmClient(machine, 'my_arm');

// Move an arm with 6 joints (6 DoF)
await arm.moveToJointPositions([90, 0, 0, 0, 15, 0]);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/ArmClient.html#movetojointpositions).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `positions` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)\> (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Create a list of joint angles for each arm joint
List<double> targetPositions = [180, 90, 15.75, 30, 90, 0];

// Move the arm joints to those angles
await myArm.moveToJointPositions(targetPositions);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/moveToJointPositions.html).

{{% /tab %}}
{{< /tabs >}}

### MoveThroughJointPositions

Move the arm's joints through the given positions in the order they are specified.
This will block until done or a new operation cancels this one.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positions` [([][]referenceframe.Input)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#Input)
- `options` [(*MoveOptions)](https://pkg.go.dev/go.viam.com/rdk/components/arm#MoveOptions)
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(machine, "my_arm")

// Declare a 2D array of values with your desired rotational value (in radians) for each joint on the arm.
inputs := [][]referenceframe.Input{
  referenceframe.FloatsToInputs([]float64{0, math.Pi/2, math.Pi})
  referenceframe.FloatsToInputs([]float64{0, 0, 0})
}

// Move each joint of the arm through the positions in the slice defined above
err = myArm.MoveThroughJointPositions(context.Background(), inputs, nil, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{< /tabs >}}

### GetJointPositions

Get the current position of each joint on the arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.component.arm.JointPositions](https://python.viam.dev/autoapi/viam/proto/component/arm/index.html#viam.proto.component.arm.JointPositions)): The current `JointPositions` for the arm.
`JointPositions` can have one attribute, `values`, a list of joint positions with rotational values (degrees)
and translational values (mm).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=machine, name="my_arm")

# Get the current position of each joint on the arm as JointPositions.
pos = await my_arm.get_joint_positions()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_joint_positions).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]referenceframe.Input)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#Input)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myArm , err := arm.FromRobot(machine, "my_arm")

// Get the current position of each joint on the arm as JointPositions.
pos, err := myArm.JointPositions(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[JointPositions](https://ts.viam.dev/classes/armApi.JointPositions.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const arm = new VIAM.ArmClient(machine, 'my_arm');
const jointPositions = await arm.getJointPositions();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/ArmClient.html#getjointpositions).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
List<double> currentJointPositions = await myArm.moveToJointPosition();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/jointPositions.html).

{{% /tab %}}
{{< /tabs >}}

### GetKinematics

Get the kinematics information associated with the arm as the format and byte contents of the [kinematics file](/operate/reference/kinematic-chain-config/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[[KinematicsFileFormat.ValueType](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.KinematicsFileFormat), [bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)]): A tuple containing two values; the first \[0] value represents the format of the
file, either in URDF format (`KinematicsFileFormat.KINEMATICS_FILE_FORMAT_URDF`) or
Viam’s kinematic parameter format (spatial vector algebra) (`KinematicsFileFormat.KINEMATICS_FILE_FORMAT_SVA`),
and the second \[1] value represents the byte contents of the file.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=machine, name="my_arm")

# Get the kinematics information associated with the arm.
kinematics = await my_arm.get_kinematics()

# Get the format of the kinematics file.
k_file = kinematics[0]

# Get the byte contents of the file.
k_bytes = kinematics[1]
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_kinematics).

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
{{< /tabs >}}

### IsMoving

Get if the arm is currently moving.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Whether the arm is moving.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=machine, name="my_arm")

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await my_arm.stop()

# Print if the arm is currently moving.
print(await my_arm.is_moving())
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.is_moving).

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
const arm = new VIAM.ArmClient(machine, 'my_arm');
const isMoving = await arm.isMoving();
console.log(isMoving);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/ArmClient.html#ismoving).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[bool](https://api.flutter.dev/flutter/dart-core/bool-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
bool isArmMoving = await myArm.isMoving();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/isMoving.html).

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop all motion of the arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=machine, name="my_arm")

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await my_arm.stop()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.stop).

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
const arm = new VIAM.ArmClient(machine, 'my_arm');
await arm.stop();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/ArmClient.html#stop).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)\<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic\>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
await myArm.stop();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/stop.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the arm in its current configuration, in the [frame](/operate/reference/services/frame-system/) of the arm.
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
my_arm = Arm.from_robot(robot=machine, name="my_arm")
geometries = await my_arm.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_geometries).

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
// This example shows using Geometries with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

geometries, err := myArm.Geometries(context.Background(), nil)

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
const arm = new VIAM.ArmClient(machine, 'my_arm');
const geometries = await arm.getGeometries();
console.log(geometries);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/ArmClient.html#getgeometries).

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
If you are implementing your own arm and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

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
my_arm = Arm.from_robot(robot=machine, name="my_arm")
command = {"cmd": "test", "data1": 500}
result = await my_arm.do_command(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.do_command).

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
myArm, err := arm.FromRobot(machine, "my_arm")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myArm.DoCommand(context.Background(), command)
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

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/ArmClient.html#docommand).

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

Get the `ResourceName` for this arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm_name = Arm.get_resource_name("my_arm")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(machine, "my_arm")

err = myArm.Name()
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
arm.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/ArmClient.html#name).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
final myArmResourceName = myArm.getResourceName("my_arm");
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/getResourceName.html).

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
my_arm = Arm.from_robot(robot=machine, name="my_arm")
await my_arm.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(machine, "my_arm")

err = myArm.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
