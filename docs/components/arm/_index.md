---
title: "Arm Component"
linkTitle: "Arm"
weight: 10
type: "docs"
description: "A robotic arm is made up of a series of links and joints, ending with a device you can position."
tags: ["arm", "components"]
icon: "img/components/arm.png"
# SME: Peter L
---

A robotic arm is a serial chain of joints and links, with a fixed end and an end effector end.
Joints may rotate, translate, or both, while a link is a rigid connector between joints.

In simple terms, an *arm* has two ends: one fixed in place, and one with a device you can position.

When controlling an arm component, you can place the end effector at arbitrary cartesian positions relative to the base of the arm.
You can do this by calling the `MoveToPosition` method to move the end effector to specified cartesian coordinates, or by controlling the joint positions directly with the `MoveToJointPositions` method.

When controlling an arm with `viam-server`, the following features are implemented for you:

- Linear motion planning
- Self-collision prevention
- Obstacle avoidance

#### `viam-server` Motion Planning with your Arm's Native Software

Arm models are supported with a driver built to be compatible with the software API that model's manufacturer supports.
While some Arm models build inverse kinematics into their software, many do not.

- Most of the Arm drivers for the Viam RDK bypass any onboard inverse kinematics, and use Viam's [Motion Planning](/services/motion/) service instead.

- This driver handles turning the arm on and off, querying the arm for its current joint position, sending requests for the arm to move to a specified set of joint positions, and engaging brakes as needed, if supported.

Arm drivers are also paired, in the RDK, with JSON files that describe the kinematics parameters of each arm.

- When you configure a supported arm model to connect to `viam-server`, the Arm driver will load and parse the kinematics file for the Viam RDK's [Frame System](/services/frame-system/) service to use.

- The [Frame System](/services/frame-system/) will allow you to easily calculate where any part of your robot is relative to any other part, other robot, or piece of the environment.

- All arms have a `Home` position, which corresponds to setting all joint angles to 0.

- When an arm is moved with a `move_to_position` call, the movement will follow a straight line, and not deviate from the start or end orientations more than the start and orientations differ from one another

- If there is no way for the arm to move to the desired location in a straight line, or if it would self-collide or collide with an obstacle that was passed in as something to avoid, then the `move_to_position` call will fail.

## Configuration

Supported arm models include:

| Model | Description |
| ----- | ----------- |
| [`fake`](fake) | A model used for testing, with no physical hardware. |
| [`xArm6`](xarm6) | [UFACTORY xArm 6](https://www.ufactory.cc/product-page/ufactory-xarm-6) |
| [`xArm7`](xarm7) | [UFACTORY xArm 7](https://www.ufactory.cc/product-page/ufactory-xarm-7) |
| `eva` | [Automata Eva](https://automata.tech/products/hardware/about-eva/) |
| `trossen-vx300s` | [Trossen Robotics ViperX 300](https://www.trossenrobotics.com/viperx-300-robot-arm.aspx) |
| `trossen-wx250s`| [Trossen Robotics WidowX 250](https://www.trossenrobotics.com/widowx-250-robot-arm.aspx) |
| `ur5e` | [Universal Robots UR5e](https://www.universal-robots.com/products/ur5-robot/) |
| `yahboom-dofbot` | [Yahboom DOFBOT](https://category.yahboom.net/collections/r-robotics-arm) |
| `wrapper_arm` | A model used to wrap a partially implemented arm. |

## Control your arm with Viam's client SDK libraries

The following example assumes you have an arm called "my_arm" configured as a component of your robot.
If your arm has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.components.arm import Arm, JointPositions
from viam.proto.common import Pose, WorldState

async def main():

  # Connect to your robot.
  robot = await connect() # Define a function to connect to your robot: see the CODE SAMPLE tab of your robot's page in app.viam.com.

  # Log an info message with the names of the different resources that are connected to your robot.
  print('Resources:')
  print(robot.resource_names)

  # Get your arm from your robot.
  my_arm = Arm.from_robot(robot=robot, name='my_arm')

  # Disconnect from your robot.
  await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
  "context"
  "github.com/edaniels/golog"

  "go.viam.com/rdk/components/arm"
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/spatialmath"

  componentpb "go.viam.com/api/component/arm/v1"
)

func main() {

  // Create an instance of a logger.
  logger := golog.NewDevelopmentLogger("client")

  // Define a function to connect to your robot: see the CODE SAMPLE tab of your robot's page in app.viam.com.
  robot, err := client.New( ... )

  // Log any errors that occur.
  if err != nil {
      logger.Fatal(err)
  }

  // Delay closing your connection to your robot until main() exits.
  defer robot.Close(context.Background())

  // Log an info message with the names of the different resources that are connected to your robot.
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Get your arm from your robot.
  myArm, err := arm.FromRobot(robot, "my_arm")
  if err != nil {
    logger.Fatalf("cannot get arm: %v", err)
  }

}
```

{{% /tab %}}
{{< /tabs >}}

## API

The arm component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [GetEndPosition](#getendposition) | Get the current position of the arm as a Pose. |
| [MoveToPosition](#movetoposition) | Move the end of the arm to the desired Pose. |
| [MoveToJointPositions](#movetojointpositions) | Move each joint on the arm to the desired position. |
| [JointPositions](#jointpositions) | Get the current position of each joint on the arm. |
| [Stop](#stop) | Stop the arm from moving. |
| [IsMoving](#stop) | Get if the arm is currently moving. |
| [DoCommand](#docommand) | Sends or receives model-specific commands. |

### GetEndPosition

Get the current position of the arm as a [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `Pose` [(Pose)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose.
The `Pose` is composed of values for location and orientation with respect to the origin.
Location is expressed as distance, which is represented by x, y, and z coordinate values.
Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.get_end_position).

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name='my_arm')

# Get the end position of the arm as a Pose.
pos = await my_arm.get_end_position()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(`Context`)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(`map[string]interface{}`)](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- `Pose` [(`spatialmath.Pose`)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose.
The `Pose` is composed of values for location and orientation with respect to the origin.
Location is expressed as distance, which is represented by x, y, and z coordinate values.
Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Get the end position of the arm as a Pose.
err, pos := myArm.EndPosition(context.Background(), nil)

// Log any errors that occur.
if err != nil {
  logger.Fatalf("cannot get end position of arm: %v", err)
}
```

{{% /tab %}}
{{< /tabs >}}

### MoveToPosition

Move the end of the arm to the desired [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose), relative to the base of the arm.
Plan for the arm to avoid obstacles and comply with the constraints for movement specified in [(WorldState)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `pose` [(Pose)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose.
The `Pose` is composed of values for location and orientation with respect to the origin.
Location is expressed as distance, which is represented by x, y, and z coordinate values.
Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.
- `world_state`[(WorldState)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState): Obstacles that the arm must avoid while it moves from its original position to the position specified in `pose`.
A `WorldState` can include a variety of attributes, including a list of obstacles around the object (`obstacles`), a list of spaces the robot may operate within (`interaction_spaces`), and a list of supplemental transforms (`transforms`).
These fields are optional.
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.move_to_position).

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name='my_arm')

# Create a Pose for the arm.
examplePose = Pose(x=5, y=5, z=5, o_x=5, o_y=5, o_z=5, theta=20)

# Move your arm to the Pose.
await my_arm.move_to_position(pose=examplePose, world_state=WorldState())
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(`Context`)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `Pose` [(`spatialmath.Pose`)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose.
The `Pose` is composed of values for location and orientation with respect to the origin.
Location is expressed as distance, which is represented by x, y, and z coordinate values.
Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.
- `world_state`[(`WorldState`)](https://pkg.go.dev/go.viam.com/rdk@v0.2.12/referenceframe#WorldState): Obstacles that the arm must avoid while it moves from its original position to the position specified in `pose`.
A `WorldState` can include a variety of attributes, including a list of obstacles around the object (`obstacles`), a list of spaces the robot may operate within (`interaction_spaces`), and a list of supplemental transforms (`transforms`).
These fields are optional.
- `extra` [(`map[string]interface{}`)](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Create a Pose for the arm.
examplePose = []float64{x: 5, y: 5, z: 5, o_x: 5, o_y: 5, o_z: 5, theta:20}

// Move your arm to the Pose.
myArm.MoveToPosition(context.Background(), pose: examplePose, referenceframe.WorldState(), nil)
```

{{% /tab %}}
{{< /tabs >}}

### MoveToJointPositions

Move each joint on the arm to the position specified in `positions`.

{{% alert title="Note" color="note" %}}

Collision checks are not enabled when doing direct joint control with MoveToJointPositions().

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `positions` [(`JointPositions`)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.JointPositions): The desired position of each joint of the arm at the end of movement.
JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).
- `extra` [(`Optional[Dict[str, Any]]`)](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(`Optional[float]`)](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.move_to_joint_positions)

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name='my_arm')

# Declare a list of values with your desired rotational value for each joint on the arm.
degrees = [0.0, 45.0, 0.0, 0.0, 0.0]

# Declare a new JointPositions with these values.
jointPos = arm.move_to_joint_positions(JointPositions(values=[0.0, 45.0, 0.0, 0.0, 0.0]))

# Move each joint of the arm to the position these values specify.
await my_arm.move_to_joint_positions(positions= jointPos)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(`Context`)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positions` [(`JointPositions`)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#JointPositions): The desired position of each joint of the arm at the end of movement.
JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).
- `extra` [(`map[string]interface{}`)](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Declare an array of values with your desired rotational value for each joint on the arm.
degrees := []float64{4.0, 5.0, 6.0}

// Declare a new JointPositions with these values.
jointPos := componentpb.JointPositions{Values= degrees}

// Move each joint of the arm to the position these values specify.
myArm.MoveToJointPositions(context.Background(), jointPos, nil)
```

{{% /tab %}}
{{< /tabs >}}

### JointPositions

Get the current position of each joint on the arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(`Optional[Dict[str, Any]]`)](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(`Optional[float]`)](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- `positions` [(`JointPositions`)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.JointPositions): The position of each joint of the arm.
JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.get_joint_positions)

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name='my_arm')

# Get the current position of each joint on the arm as JointPositions.
pos = await my_arm.get_joint_positions()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(`Context`)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(`map[string]interface{}`)](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- `positions` [(`JointPositions`)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#JointPositions): The desired position of each joint of the arm at the end of movement.
JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
my_arm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Get the current position of each joint on the arm as JointPositions.
pos, err := my_arm.JointPositions(context.Background(), nil)

// Log any errors that occur.
if err != nil {
  logger.Fatalf("cannot get JointPositions of arm: %v", err)
}

```

{{% /tab %}}
{{< /tabs >}}

### Stop

Stop all motion of the arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(`Optional[Dict[str, Any]]`)](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(`Optional[float]`)](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.stop).

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name='my_arm')

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await my_arm.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(`Context`)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(`map[string]interface{}`)](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Stop all motion of the arm. It is assumed that the arm stops immediately.
myArm.Stop(context.Background(), nil)
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

- `is_moving` [(`bool`)](https://docs.python.org/c-api/bool.html): If it is true or false that the arm is currently moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.is_moving).

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot=robot, name='my_arm')

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await my_arm.stop()

# Print if the arm is currently moving.
print(my_arm.is_moving())
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `Context` [(`Context`)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- `is_moving` [(`bool`)](https://pkg.go.dev/builtin#bool): If it is true or false that the arm is currently moving.
- `error` [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Stop all motion of the arm. It is assumed that the arm stops immediately.
myArm.Stop(context.Background(), nil)

// Log if the arm is currently moving.
is_moving, err := myArm.IsMoving(context.Background())
if err != nil {
  logger.Fatalf("cannot get if arm is moving: %v", err)
}
logger.Info(is_moving)
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

- `command` (`Dict[str, Any]`): The command to execute.

**Returns:**

- `result` (`Dict[str, Any]`): Result of the executed command.

```python {class="line-numbers linkable-line-numbers"}
my_arm = Arm.from_robot(robot, "arm1")

command = {"cmd": "test", "data1": 500}
result = my_arm.do(command)
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
  myArm, err := arm.FromRobot(robot, "my arm")

  command := map[string]interface{}{"cmd": "test", "data1": 500}
  result, err := myArm.DoCommand(context.Background(), command)
```

For more information, see the [Go SDK Code](https://github.com/viamrobotics/rdk/blob/9be13108c8641b66fd4251a74ea638f47b040d62/components/arm/arm.go#L198).

{{% /tab %}}
{{< /tabs >}}

## SDK Documentation

- [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/arm/index.html)
- [Go SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/arm)

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next Steps

<div class="container text-center td-max-width-on-larger-screens">
  <div class="row">
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="/tutorials/motion/accessing-and-moving-robot-arm">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Access and Move a Robot Arm</h4>
            <p style="text-align: left;">Tutorial on accessing and controlling one of the most fundamental systems in robotics: A robotic arm.</p>
        </a>
    </div>
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="/services/motion">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Viam's Motion Service</h4>
            <p style="text-align: left;">More information on Viam's Motion Service.</p>
        </a>
    </div>
  </div>
</div>
