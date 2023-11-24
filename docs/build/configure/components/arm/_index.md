---
title: "Arm Component"
linkTitle: "Arm"
childTitleEndOverwrite: "Arm Component"
weight: 10
type: "docs"
description: "A robotic arm is made up of a series of links and joints, ending with a device you can position."
no_list: true
tags: ["arm", "components"]
icon: "/icons/components/arm.svg"
images: ["/icons/components/arm.svg"]
modulescript: true
aliases:
  - "/components/arm/"
# SME: Peter L
---

A robotic arm is a serial chain of joints and links, with a fixed end and an end effector end.
Joints may rotate, translate, or both, while a link is a rigid connector between joints.

In simple terms, an _arm_ has two ends: one fixed in place, and one with a device you can position.

When controlling an arm component, you can place the end effector at arbitrary cartesian positions relative to the base of the arm.
You can do this by calling the `MoveToPosition` method to move the end effector to specified cartesian coordinates, or by controlling the joint positions directly with the `MoveToJointPositions` method.

When controlling an arm with `viam-server`, the following features are implemented for you:

- Linear motion planning
- Self-collision prevention
- Obstacle avoidance

## Motion planning with your arm's built-in software

Each arm model is supported with a driver that is compatible with the software API that the model's manufacturer supports.
While some arm models build inverse kinematics into their software, many do not.

- Most of the arm drivers for the Viam RDK bypass any onboard inverse kinematics, and use Viam's [motion service](/build/configure/services/motion/) instead.

- This driver handles turning the arm on and off, querying the arm for its current joint position, sending requests for the arm to move to a specified set of joint positions, and engaging brakes as needed, if supported.

Arm drivers are also paired, in the RDK, with JSON files that describe the kinematics parameters of each arm.

- When you configure a supported arm model to connect to `viam-server`, the Arm driver will load and parse the kinematics file for the Viam RDK's [frame system](/build/configure/services/frame-system/) service to use.

- The [frame system](/build/configure/services/frame-system/) will allow you to easily calculate where any part of your robot is relative to any other part, other robot, or piece of the environment.

- All arms have a `Home` position, which corresponds to setting all joint angles to 0.

- When an arm is moved with a `move_to_position` call, the movement will follow a straight line, and not deviate from the start or end orientations more than the start and orientations differ from one another

- If there is no way for the arm to move to the desired location in a straight line, or if it would self-collide or collide with an obstacle that was passed in as something to avoid, then the `move_to_position` call will fail.

## Related Services

{{< cards >}}
{{< relatedcard link="/build/configure/services/motion/" >}}
{{< relatedcard link="/build/configure/services/frame-system/" >}}
{{< relatedcard link="/build/configure/services/data/" >}}
{{< /cards >}}

## Supported Models

To use your arm with Viam, check whether one of the following [built-in models](#built-in-models) or [modular resources](#modular-resources) supports your arm.

{{< alert title="Add support for other models" color="tip" >}}

If none of the existing models fit your use case, you can [create a modular resource](/registry/) to add support for it.

You can follow [this guide](/registry/examples/custom-arm/) to implement your custom arm as a [modular resource](/registry/).

{{< /alert >}}

### Built-in models

For configuration information, click on the model name:

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`fake`](fake/) | A model used for testing, with no physical hardware. |
| [`xArm6`](xarm6/) | [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6) |
| [`xArm7`](xarm7/) | [UFACTORY xArm 7](https://www.ufactory.cc/product-page/ufactory-xarm-7) |
| [`xArmLite`](xarmlite/) | [UFACTORY Lite 6](https://www.ufactory.cc/product-page/ufactory-lite-6) |
| [`ur5e`](ur5e/) | [Universal Robots UR5e](https://www.universal-robots.com/products/ur5-robot) |

### Modular Resources

{{<modular-resources api="rdk:component:arm" type="arm">}}

## Control your arm with Viam's client SDK libraries

To get started using Viam's SDKs to connect to and control your robot, go to your robot's page on [the Viam app](https://app.viam.com), navigate to the **Code sample** tab, select your preferred programming language, and copy the sample code generated.

{{% snippet "show-secret.md" %}}

When executed, this sample code will create a connection to your robot as a client.
Then control your robot programmatically by adding API method calls as shown in the following examples.

These examples assume you have an arm called `"my_arm"` configured as a component of your robot.
If your arm has a different name, change the `name` in the code.

Be sure to import the arm package for the SDK you are using:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.arm import Arm
# To use move_to_position:
from viam.proto.common import Pose
# To use move_to_joint_positions:
from viam.proto.component.arm import JointPositions
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
  "go.viam.com/rdk/components/arm"
  // To use MoveToPosition:
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/spatialmath"
  // To use MoveToJointPositions ("armapi" name optional, but necessary if importing other packages called "v1"):
  armapi "go.viam.com/api/component/arm/v1"
)
```

{{% /tab %}}
{{< /tabs >}}

## API

The arm component supports the following methods:

{{< readfile "/static/include/components/apis/arm.md" >}}

### GetEndPosition

Get the current position of the arm as a [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Pose)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose.
  The `Pose` is composed of values for location and orientation with respect to the origin.
  Location is expressed as distance, which is represented by x, y, and z coordinate values.
  Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.get_end_position).

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Get the end position of the arm as a Pose.
pos = await my_arm.get_end_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.
  **Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose.
  The `Pose` is composed of values for location and orientation with respect to the origin.
  Location is expressed as distance, which is represented by x, y, and z coordinate values.
  Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")

// Get the end position of the arm as a Pose.
err, pos := myArm.EndPosition(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### MoveToPosition

Move the end of the arm to the desired [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose), relative to the base of the arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `pose` [(Pose)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose.
  The `Pose` is composed of values for location and orientation with respect to the origin.
  Location is expressed as distance, which is represented by x, y, and z coordinate values.
  Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.move_to_position).

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Create a Pose for the arm.
examplePose = Pose(x=5, y=5, z=5, o_x=5, o_y=5, o_z=5, theta=20)

# Move your arm to the Pose.
await my_arm.move_to_position(pose=examplePose)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `Pose` [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose.
  The `Pose` is composed of values for location and orientation with respect to the origin.
  Location is expressed as distance, which is represented by x, y, and z coordinate values.
  Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")

// Create a Pose for the arm.
examplePose = []float64{x: 5, y: 5, z: 5, o_x: 5, o_y: 5, o_z: 5, theta:20}

// Move your arm to the Pose.
err := myArm.MoveToPosition(context.Background(), pose: examplePose, nil)
```

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

- `positions` [(JointPositions)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.JointPositions): The desired position of each joint of the arm at the end of movement.
  JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.move_to_joint_positions)

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

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positions` [(JointPositions)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#JointPositions): The desired position of each joint of the arm at the end of movement.
  JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")

// Declare an array of values with your desired rotational value for each joint on the arm.
degrees := []float64{4.0, 5.0, 6.0}

// Declare a new JointPositions with these values.
jointPos := componentpb.JointPositions{degrees}

// Move each joint of the arm to the position these values specify.
err := myArm.MoveToJointPositions(context.Background(), jointPos, nil)
```

{{% /tab %}}
{{< /tabs >}}

### JointPositions

Get the current position of each joint on the arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(JointPositions)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.JointPositions): The position of each joint of the arm.
  JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.get_joint_positions)

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Get the current position of each joint on the arm as JointPositions.
pos = await my_arm.get_joint_positions()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- [(JointPositions)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#JointPositions): The desired position of each joint of the arm at the end of movement.
  JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
my_arm, err := arm.FromRobot(robot, "my_arm")

// Get the current position of each joint on the arm as JointPositions.
pos, err := my_arm.JointPositions(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop all motion of the arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.stop).

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await my_arm.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")

// Stop all motion of the arm. It is assumed that the arm stops immediately.
err := myArm.Stop(context.Background(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetKinematics

{{% alert title="Note" color="note" %}}
This method is not yet available with the Viam Go SDK.
{{% /alert %}}

Get the kinematics information associated with the arm as the format and byte contents of the [kinematics file](/reference/internals/kinematic-chain-config/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Tuple[[KinematicsFileFormat.ValueType](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.KinematicsFileFormat), [bytes](https://docs.python.org/3/library/stdtypes.html#bytes)): A tuple containing [the format](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.KinematicsFileFormat) of the arm's <file>.URDF</file> or <file>.json</file> kinematics file and the [byte](https://docs.python.org/3/library/stdtypes.html#bytes) contents of the file.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_kinematics).

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Get the kinematics information associated with the arm.
kinematics = await my_arm.get_kinematics()

# Get the format of the kinematics file.
k_file = kinematics[0]

# Get the byte contents of the file.
k_bytes = kinematics[1]
```

{{% /tab %}}
{{< /tabs >}}

### IsMoving

Get if the arm is currently moving.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): If it is true or false that the arm is currently moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.is_moving).

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await my_arm.stop()

# Print if the arm is currently moving.
print(my_arm.is_moving())
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): If it is true or false that the arm is currently moving.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")

// Stop all motion of the arm. It is assumed that the arm stops immediately.
myArm.Stop(context.Background(), nil)

// Log if the arm is currently moving.
is_moving, err := myArm.IsMoving(context.Background())
logger.Info(is_moving)
```

{{% /tab %}}
{{< /tabs >}}

### GetGeometries

Get all the geometries associated with the arm in its current configuration, in the [frame](/build/configure/services/frame-system/) of the arm.
The [motion](/build/configure/services/motion/) and [navigation](/build/configure/services/navigation/) services use the relative position of inherent geometries to configured geometries representing obstacles for collision detection and obstacle avoidance while motion planning.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[Geometry])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry): The geometries associated with the arm, in any order.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_geometries).

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name="my_arm")

geometries = await my_arm.get_geometries()

if geometries:
    # Get the center of the first geometry
    print(f"Pose of the first geometry's centerpoint: {geometries[0].center}")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [`[]spatialmath.Geometry`](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): The geometries associated with the arm, in any order.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Shaped).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")

geometries, err := myArm.Geometries(context.Background(), nil)

if len(geometries) > 0 {
    // Get the center of the first geometry
    elem := geometries[0]
    fmt.Println("Pose of the first geometry's center point:", elem.center)
}
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the component API.
For built-in models, model-specific commands are covered with each model's documentation.
If you are implementing your own arm and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.

**Returns:**

- [(Dict[str, Any])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot, "my_arm")

command = {"cmd": "test", "data1": 500}
result = my_arm.do(command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.do_command).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map[string]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map[string]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myArm.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot, "my_arm")

await my_arm.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")

err := myArm.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/reference/appendix/troubleshooting/).

You can also ask questions on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next Steps

{{< cards >}}
{{% card link="/tutorials/services/accessing-and-moving-robot-arm" %}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{< /cards >}}
