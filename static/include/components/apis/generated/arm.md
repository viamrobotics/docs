### GetEndPosition

Get the current position of the arm as a [pose](/internals/orientation-vector/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.components.arm.Pose](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Pose)): A representation of the arm’s current position as a 6 DOF (six degrees of freedom) pose. The Pose is composed of values for location and orientation with respect to the origin. Location is expressed as distance, which is represented by x, y, and z coordinate values. Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

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
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Pose](https://flutter.viam.dev/viam_sdk/Pose-class.html)>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Get the pose of an arm named "myArm"
final currentPose = await myArm.endPosition();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/endPosition.html).

{{% /tab %}}
{{< /tabs >}}

### MoveToPosition

Move the end of the arm to the desired [pose](/internals/orientation-vector/), relative to the base of the arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `pose` ([viam.components.arm.Pose](https://python.viam.dev/autoapi/viam/components/arm/arm/index.html#viam.components.arm.arm.Pose)) (required): The destination Pose for the arm. The Pose is composed of values for location and orientation with respect to the origin. Location is expressed as distance, which is represented by x, y, and z coordinate values. Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

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
        &spatialmath.OrientationVectorDegrees{0X: 5, 0Y: 5, Theta: 20}
)

// Move your arm to the Pose.
err = myArm.MoveToPosition(context.Background(), examplePose, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `pose` [Pose](https://flutter.viam.dev/viam_sdk/Pose-class.html) (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

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

- `positions` ([viam.proto.component.arm.JointPositions](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.JointPositions)) (required): The destination JointPositions for the arm.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Declare a list of values with your desired rotational value for each joint on
# the arm.
degrees = [0.0, 45.0, 0.0, 0.0, 0.0]

# Declare a new JointPositions with these values.
jointPos = arm.move_to_joint_positions(
    JointPositions(values=[0.0, 45.0, 0.0, 0.0, 0.0]))

# Move each joint of the arm to the position these values specify.
await my_arm.move_to_joint_positions(positions=jointPos)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.move_to_joint_positions).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positionDegs` [(*pb.JointPositions)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#JointPositions): The desired position of each joint of the arm at the end of movement. JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Assumes you have imported "go.viam.com/api/component/arm/v1" as `componentpb`
myArm, err := arm.FromRobot(machine, "my_arm")

// Declare an array of values with your desired rotational value for each joint on the arm.
degrees := []float64{4.0, 5.0, 6.0}

// Declare a new JointPositions with these values.
jointPos := &componentpb.JointPositions{Values: degrees}

// Move each joint of the arm to the position these values specify.
err = myArm.MoveToJointPositions(context.Background(), jointPos, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `positions` [List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)> (required)
- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

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

### GetJointPositions

Get the current position of each joint on the arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.component.arm.JointPositions](https://python.viam.dev/autoapi/viam/proto/component/arm/index.html#viam.proto.component.arm.JointPositions)): The current JointPositions for the arm. JointPositions can have one attribute, values, a list of joint positions with rotational values (degrees) and translational values (mm).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

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

- [(*pb.JointPositions)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#JointPositions): The desired position of each joint of the arm at the end of movement.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myArm , err := arm.FromRobot(machine, "my_arm")

// Get the current position of each joint on the arm as JointPositions.
pos, err := myArm.JointPositions(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)<[double](https://api.flutter.dev/flutter/dart-core/double-class.html)>>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
List<double> currentJointPositions = await myArm.moveToJointPosition();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/jointPositions.html).

{{% /tab %}}
{{< /tabs >}}

### GetKinematics

{{% alert title="Note" color="note" %}}
This method is not yet available with the Viam Go SDK.
{{% /alert %}}

Get the kinematics information associated with the arm as the format and byte contents of the [kinematics file](/internals/kinematic-chain-config/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[[KinematicsFileFormat.ValueType](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.KinematicsFileFormat), [bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)]): A tuple containing two values; the first [0] value represents the format of the file, either in URDF format (KinematicsFileFormat.KINEMATICS_FILE_FORMAT_URDF) or Viam’s kinematic parameter format (spatial vector algebra) (KinematicsFileFormat.KINEMATICS_FILE_FORMAT_SVA), and the second [1] value represents the byte contents of the file.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Get the kinematics information associated with the arm.
kinematics = await my_arm.get_kinematics()

# Get the format of the kinematics file.
k_file = kinematics[0]

# Get the byte contents of the file.
k_bytes = kinematics[1]
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_kinematics).

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
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await my_arm.stop()

# Print if the arm is currently moving.
print(my_arm.is_moving())
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
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[bool](https://api.flutter.dev/flutter/dart-core/bool-class.html)>

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
my_arm = Arm.from_robot(robot=robot, name="my_arm")

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
{{% tab name="Flutter" %}}

**Parameters:**

- `extra` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>? (optional)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<void>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
await myArm.stop();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/stop.html).

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the arm in its current configuration, in the [frame](/services/frame-system/) of the arm.
The [motion](/services/motion/) and [navigation](/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([List[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry)): The geometries associated with the Component.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
geometries = await component.get_geometries()

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
   fmt.Println("Pose of the first geometry's center point:", elem.center)
}
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Shaped).

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
If you are implementing your own arm and add features that have no built-in API method, you can access them with `DoCommand`.

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
command = {"cmd": "test", "data1": 500}
result = component.do(command)
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
// This example shows using DoCommand with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myArm.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `command` [Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic> (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)<[Map](https://api.flutter.dev/flutter/dart-core/Map-class.html)<[String](https://api.flutter.dev/flutter/dart-core/String-class.html), dynamic>>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example using doCommand with an arm component
const command = {'cmd': 'test', 'data1': 500};
var result = myArm.doCommand(command);
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Resource/doCommand.html).

{{% /tab %}}
{{< /tabs >}}

### FromRobot

Get the resource from the provided robot with the given name.

{{< tabs >}}
{{% tab name="Flutter" %}}

**Parameters:**

- `robot` [RobotClient](https://flutter.viam.dev/viam_sdk/RobotClient-class.html) (required)
- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [Arm](https://flutter.viam.dev/viam_sdk/Arm-class.html)

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/Arm/fromRobot.html).

{{% /tab %}}
{{< /tabs >}}

### Name

Get the `ResourceName` for this arm with the given name.

{{< tabs >}}
{{% tab name="Flutter" %}}

**Parameters:**

- `name` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)

**Returns:**

- [ResourceName](https://flutter.viam.dev/viam_sdk/ResourceName-class.html)

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
await component.close()
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
// This example shows using Close with an arm component.
myArm, err := arm.FromRobot(machine, "my_arm")

err = myArm.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
