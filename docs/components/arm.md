---
title: "Arm Component"
linkTitle: "Arm"
weight: 10
type: "docs"
description: "Explanation of arm configuration and usage in Viam."
tags: ["arm", "components"]
icon: "img/components/arm.png"
# SME: Peter L
---

Arms are serial chains of joints and links, with a fixed end and an end effector end.
The end effector is able to be placed at arbitrary cartesian positions relative to the base of the arm, and can be moved to cartesian coordinates or controlled directly via the joint positions.

As an example, to move an xArm6 whose component name is "my_xArm6" forwards in the X direction by 300mm:

```python
from viam.components.arm import Arm
from viam.proto.api.common import WorldState

arm = Arm.from_robot(robot=robot, name='my_xArm6')
pos = await arm.get_end_position()
pos.x += 300
await arm.move_to_position(pose=pos, world_state=WorldState())
```

This document will teach you how to configure, connect to, and move the arms with preprogrammed support from Viam, as well as introduce you to the steps required to implement support for any other arm.

An arm consists of movable pieces, joints, immovable pieces, and links. Joints may rotate, translate, or both, while a link will always be the same shape.

An arm can be thought of as something that can set or get joint positions, and can compute the cartesian position of its end effector(s) given its set of joint positions.
Arms will also support moving to a specified cartesian position, something that requires inverse kinematics and motion planning to determine the ending joint positions.

The way most supported arms are set up is via a driver in Viam's RDK which is compatible with whatever software API is supported by that specific arm's manufacturer.
This driver handles turning the arm on and off, engaging brakes as needed (if supported), querying the arm for its current joint position, and sending requests for the arm to move to a specified set of joint positions.

Arm drivers are paired with JSON files describing the kinematics parameters of each arm.
The arm driver will load and parse the kinematics file to be used with the Frame System that is part of RDK.
The Frame System will allow you to easily calculate where any part of your robot is relative to any other part, other robot, or piece of the environment.

All arms have a "Home" position, which corresponds to setting all joint angles to 0.

While some arms include onboard inverse kinematics, many do not.
Most Viam RDK arm drivers bypass any onboard inverse kinematics, and use Viam's motion planning instead.
When an arm is moved via the `move_to_position` call, it is enforced that the movement will follow a straight line, and not deviate from the start or end orientations more than the start and orientations differ from one another.
If there is no way to move to the desired location in a straight line for the arm in question, or if it would self-collide or collide with an obstacle that was passed in as something to avoid, then the `move_to_position` call will fail.

## Features

- Linear motion planning
- Self-collision prevention
- Obstacle avoidance

## Viam Configuration

```json-viam
{
  "components": [{
      "attributes": {
          "host": "10.0.0.97"
      },
      "depends_on": [],
      "frame": {
          "orientation": {
              "type": "ov_degrees",
              "value": {
                  "th": 0,
                  "x": 0,
                  "y": 0,
                  "z": 1
              }
          },
          "parent": "world",
          "translation": {
              "x": 0,
              "y": 0,
              "z": 0
          }
      },
      "model": "xArm6",
      "name": "xArm6",
      "type": "arm"
  }]
}
```

### Optional Attributes

Individual arm implementations have their own sets of configurable parameters that vary by vendor.
For example, for an xArm6 or an xArm7, there are three parameters:

- **host**: A string representing the IP address of the arm.
  
- **speed** (Optional. Default: 20.0): A float representing the desired maximum joint movement speed in degrees/second.
  
- **acceleration** (Optional. Default: 50.0):  A float representing the desired maximum joint acceleration in degrees/second/second.

## Examples

The following code for an xArm6 will do the following:

1. First perform a linear movement 300mm +X from its starting point, then a linear movement back to the starting point, assuming the +300mm position is within the arm's workspace.
If you have trouble with this, try starting the arm in the home position.
1. Next, it will define an obstacle along the straight-line path between the start and the same goal from above.
It will then call the Viam motion service to move the arm (rather than `arm.move_to_position`), which is able to route around the hypothetical obstacle. It will return to the starting point, again routing around the obstacle.
1. Finally, it will call `arm.move_to_position` to the goal as in the first movement, but this time passing the obstacle.
As there is no straight-line path to the goal that does not intersect the obstacle, this request will fail with a "unable to solve for position" GRPC error.

``` python
arm = Arm.from_robot(robot=robot, name="xArm6")
pos = await arm.get_end_position()

print("~~~~TESTING ARM LINEAR MOVE~~~~~")
pos = await arm.get_end_position()
print(pos)
pos.x += 300
# Note we are passing an empty worldstate
await arm.move_to_position(pose=pos, world_state=WorldState())
pos = await arm.get_end_position()
print(pos)
pos.x -= 300
await asyncio.sleep(1)
await arm.move_to_position(pose=pos, world_state=WorldState())

print("~~~~TESTING MOTION SERVICE MOVE~~~~~")

geom = Geometry(
    center=Pose(x=pos.x + 150, y=pos.y, z=pos.z),
    box=RectangularPrism(width_mm=2, length_mm=5, depth_mm=5),
)
geomFrame = GeometriesInFrame(reference_frame="xArm6", geometries=[geom])
worldstate = WorldState(obstacles=[geomFrame])

pos = await arm.get_end_position()
jpos = await arm.get_joint_positions()
print(pos)
print("joints", jpos)
pos.x += 300

for resname in robot.resource_names:
    if resname.name == "xArm6":
        armRes = resname

# We pass the WorldState above with the geometry. The arm should successfully route around it.
await motionServ.move(
    component_name=armRes,
    destination=PoseInFrame(reference_frame="world", pose=pos),
    world_state=worldstate,
)
pos = await arm.get_end_position()
jpos = await arm.get_joint_positions()
print(pos)
print("joints", jpos)
pos.x -= 300
await asyncio.sleep(1)
await motionServ.move(
    component_name=armRes,
    destination=PoseInFrame(reference_frame="world", pose=pos),
    world_state=worldstate,
)

print("~~~~TESTING ARM MOVE- SHOULD FAIL~~~~~")
pos = await arm.get_end_position()
print(pos)
pos.x += 300
# We pass the WorldState above with the geometry. As arm.move_to_position will enforce linear motion, this should fail
# since there is no linear path from start to goal that does not intersect the obstacle.
await arm.move_to_position(pose=pos, world_state=worldstate)

```

## Implementation

- [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/arm/index.html)
- [Golang SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/arm)

## API

The arm component supports the following methods:

| Method Name                   | Golang                 | Python                              | Description                                                            |
| ----------------------------- | ---------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
| [GetEndPosition](#getendposition)                 | [EndPosition][go_arm]       | [get_end_position][python_get_end_position]                 | Get the current position of the arm as a Pose.                                  |
| [MoveToPosition](#movetoposition) | [MoveToPosition][go_arm]| [move_to_position][python_move_to_position] | Move the end of the arm to the desired Pose. |
| [MoveToJointPositions](#movetojointpositions)                 | [MoveToJointPositions][go_arm]       | [move_to_joint_positions][python_move_to_joint_positions]                 | Move each joint on the arm to the desired position.                                                      |
| [GetJointPositions](#getjointpositions)                 | [GetJointPositions][go_arm]       | [get_joint_positions][python_get_joint_positions]                 | Get the current position of each joint on the arm.                                                       |
| [Stop](#stop)                 | [Stop][go_arm]       | [stop][python_stop]                 | Stop the arm from moving.                                                       |
| [IsMoving](#stop)                 | [IsMoving][go_arm]       | [is_moving][python_is_moving]                 | Get if the arm is currently moving.                                                       |

[go_arm]: https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm
[python_get_end_position]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.get_end_position
[python_move_to_position]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.move_to_position
[python_move_to_joint_positions]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.move_to_joint_positions
[python_get_joint_positions]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.get_joint_positions
[python_stop]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.stop
[python_is_moving]: https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.is_moving

### Control your Arm with Viam's Client SDK Libraries

- [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/arm/index.html)
- [Golang SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/arm)

{{% alert title="Note" color="note" %}}

Make sure you have set up your robot and connected it to the Viam app.
Check out the [Client SDK Libraries Quick Start](/program/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and the [Getting Started with the Viam App guide](/program/app-usage/) for app-specific guidance.

{{% /alert %}}

The following example assumes you have an arm called "my_arm" configured as a component of your robot.
If your arm has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.arm import Arm, JointPositions
from viam.proto.common import Pose, WorldState

async def main():

  # Connect to your robot.
  robot = await connect()

  # Log an info message with the names of the different resources that are connected to your robot. 
  print('Resources:')
  print(robot.resource_names)

  # Connect to your arm. 
  myArm = Arm.from_robot(robot=robot, name='my_arm')

  # Disconnect from your robot. 
  await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Golang" %}}

```go
import (
  "context"
  "go.viam.com/rdk/components/arm"
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/spatialmath"
  componentpb "go.viam.com/api/component/arm/v1"
)

func main() { 

  // Create an instance of a logger. 
  logger := golog.NewDevelopmentLogger("client")

  // Connect to your robot. 
  robot, err := client.New(
      context.Background(),
      "[ADD YOUR ROBOT ADDRESS HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP]",
      logger,
      client.WithDialOptions(rpc.WithCredentials(rpc.Credentials{
          Type:    utils.CredentialsTypeRobotLocationSecret,
          Payload: "[PLEASE ADD YOUR SECRET HERE. YOU CAN FIND THIS ON THE CONNECT TAB OF THE VIAM APP]",
      })),
  )

  // Log any errors that occur.
  if err != nil {
      logger.Fatal(err)
  }

  // Delay closing your connection to your robot until main() exits. 
  defer robot.Close(context.Background())

  // Log an info message with the names of the different resources that are connected to your robot. 
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())

  // Connect to your arm.
  myArm, err := arm.FromRobot(robot, "my_arm")
  if err != nil {
    logger.Fatalf("cannot get arm: %v", err)
  }

}
```

{{% /tab %}}
{{< /tabs >}}

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

```python
myArm = Arm.from_robot(robot=robot, name='my_arm')

# Get the end position of the arm as a Pose.
pos = await myArm.get_end_position()
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- `Pose` [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose.
The `Pose` is composed of values for location and orientation with respect to the origin.
Location is expressed as distance, which is represented by x, y, and z coordinate values.
Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.
  
For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Get the end position of the arm as a Pose. 
err, pos := myArm.EndPosition(context.Background())

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

```python
myArm = Arm.from_robot(robot=robot, name='my_arm')

# Create a Pose for the arm.
examplePose = Pose(x=5, y=5, z=5, o_x=5, o_y=5, o_z=5, theta=20)

# Move your arm to the Pose. 
await myArm.move_to_position(pose=examplePose, world_state=WorldState())
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `Pose` [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): A representation of the arm's current position as a 6 DOF (six degrees of freedom) pose.
The `Pose` is composed of values for location and orientation with respect to the origin.
Location is expressed as distance, which is represented by x, y, and z coordinate values.
Orientation is expressed as an orientation vector, which is represented by o_x, o_y, o_z, and theta values.
- `world_state`[(WorldState)](https://pkg.go.dev/go.viam.com/rdk@v0.2.12/referenceframe#WorldState): Obstacles that the arm must avoid while it moves from its original position to the position specified in `pose`.
A `WorldState` can include a variety of attributes, including a list of obstacles around the object (`obstacles`), a list of spaces the robot may operate within (`interaction_spaces`), and a list of supplemental transforms (`transforms`).
These fields are optional.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Create a Pose for the arm. 
examplePose = []float64{x: 5, y: 5, z: 5, o_x: 5, o_y: 5, o_z: 5, theta:20}

// Move your arm to the Pose. 
myArm.MoveToPosition(context.Background(), pose: examplePose, referenceframe.WorldState())
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

- `positions` [(JointPositions)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.JointPositions): The desired position of each joint of the arm at the end of movement.
JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).
- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.move_to_joint_positions)

```python
myArm = Arm.from_robot(robot=robot, name='my_arm')

# Declare a list of values with your desired rotational value for each joint on the arm.
degrees = [0.0, 45.0, 0.0, 0.0, 0.0]

# Declare a new JointPositions with these values.  
jointPos = arm.move_to_joint_positions(JointPositions(values=[0.0, 45.0, 0.0, 0.0, 0.0]))

# Move each joint of the arm to the position these values specify.
await myBase.move_to_joint_positions(positions= jointPos)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `positions` [(JointPositions)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#JointPositions): The desired position of each joint of the arm at the end of movement.
JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Declare an array of values with your desired rotational value for each joint on the arm. 
degrees := []float64{4.0, 5.0, 6.0}

// Declare a new JointPositions with these values.
jointPos := componentpb.JointPositions{Values= degrees}

// Move each joint of the arm to the position these values specify.
myArm.MoveToJointPositions(context.Background(), jointPos)
```

{{% /tab %}}
{{< /tabs >}}

### GetJointPositions

Get the current position of each joint on the arm.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.
  
**Returns:**

- `positions` [(JointPositions)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.JointPositions): The position of each joint of the arm.
JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.get_joint_positions)

```python
myArm = Arm.from_robot(robot=robot, name='my_arm')

# Get the current position of each joint on the arm as JointPositions. 
pos = await myArm.get_joint_positions()
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- `positions` [(JointPositions)](https://pkg.go.dev/go.viam.com/api/component/arm/v1#JointPositions): The desired position of each joint of the arm at the end of movement.
JointPositions can have one attribute, `values`, a list of joint positions with rotational values (degrees) and translational values (mm).

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Get the current position of each joint on the arm as JointPositions. 
pos, err := myArm.GetJointPositions(context.Background())

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

- `extra` [(Optional[Dict[str, Any]])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.
  
**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.stop).

```python
myArm = Arm.from_robot(robot=robot, name='my_arm')

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await myArm.stop()
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Stop all motion of the arm. It is assumed that the arm stops immediately.
myArm.Stop(context.Background())
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

- `is_moving` [(bool)](https://docs.python.org/c-api/bool.html): If it is true or false that the arm is currently moving.

For more information, see the [Python SDK Docs](https://python.viam.dev/_modules/viam/components/arm/arm.html#Arm.is_moving).

```python
myArm = Arm.from_robot(robot=robot, name='my_arm')

# Stop all motion of the arm. It is assumed that the arm stops immediately.
await myArm.stop()

# Print if the arm is currently moving.
print(myArm.is_moving())
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- `Context` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- `is_moving` [(bool)](https://pkg.go.dev/builtin#bool): If it is true or false that the arm is currently moving.
- `error` [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}

// Stop all motion of the arm. It is assumed that the arm stops immediately.
myArm.Stop(context.Background())

// Log if the arm is currently moving.
is_moving, err := myArm.IsMoving(context.Background())
if err != nil {
  logger.Fatalf("cannot get if arm is moving: %v", err)
}
logger.Info(is_moving)
```

{{% /tab %}}
{{< /tabs >}}

## Next Steps

See also:

<a href="/services/motion">Viam's Motion Service</a>
