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

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/arm/index.html)
[Golang SDK Documentation](https://pkg.go.dev/go.viam.com/rdk/components/arm)

## API

The arm component supports the following methods:

| Method Name                   | Golang                 | Python                              | Description                                                            |
| ----------------------------- | ---------------------- | ----------------------------------- | ---------------------------------------------------------------------- |
| [EndPosition](#end-position)                 | [EndPosition][go_arm]       | [get_end_position][python_get_end_position]                 | Gets the current position of the arm as a Pose.                                  |
| [MoveToPosition](#move-to-position) | [MoveToPosition][go_arm]| [move_to_position][python_move_to_position] | Moves the end of the arm to the desired Pose. |
| [MoveToJointPositions](#move-to-joint-positions)                 | [MoveToJointPositions][go_arm]       | [move_to_joint_positions][python_move_to_joint_positions]                 | Moves each joint on the arm to the desired angle while avoiding obstacles as desired.                                                      |
| [GetJointPositions](#get-joint-positions)                 | [GetJointPositions][go_arm]       | [get_joint_positions][python_get_joint_positions]                 | Gets the current position of the arm.                                                       |
| [Stop](#stop)                 | [Stop][go_arm]       | [stop][python_stop]                 | Stops the arm.                                                       |
| [IsMoving](#stop)                 | [IsMoving][go_arm]       | [is_moving][python_is_moving]                 | Gets if the arm is currently moving.                                                       |

[go_arm]: https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm
[python_get_end_position]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.get_end_position
[python_move_to_position]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.move_to_position
[python_move_to_joint_positions]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.move_to_joint_positions
[python_get_joint_positions]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.get_joint_positions
[python_stop]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.stop
[python_is_moving]: https://google.com

### Control your Arm with the Viam SDK Libraries

{{% alert title="Note" color="note" %}}

Make sure you have set up your robot and connected it to the Viam app. Check out our [Client SDK Libraries Quick Start](/product-overviews/sdk-as-client/) documentation for an overview of how to get started connecting to your robot using these libraries, and our [Getting Started with the Viam App guide](/getting-started/) for app-specific guidance.

**Assumption:** An arm called "my_arm" is configured as a component of your robot in the Viam app.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.arm import ArmClient
async def main():
    robot = await connect()
    print('Resources:')
    print(robot.resource_names)
    # Get the arm client from the robot
    myArm = ArmClient.from_robot(robot=robot, name='my_arm')
    await robot.close()
if __name__ == '__main__':
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Golang" %}}

```go
import (
 "go.viam.com/rdk/components/arm"
)
func main() {
  //robot, err := client.New(...)
  logger.Info("Resources:")
  logger.Info(robot.ResourceNames())
  // Get the arm client from the robot.
  myArm, err := arm.FromRobot(robot, "my_arm")
  if err != nil {
    logger.Fatalf("cannot get arm: %v", err)
  }
}
```

{{% /tab %}}
{{< /tabs >}}

### GetEndPosition

<!-- Move the base in a straight line across the given distance (*mm*) at the given velocity (*mm/sec*). -->

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

<!-- - *distance* [(int)](https://docs.python.org/3/library/functions.html#int): The distance to move in millimeters.
Negative implies backwards.
- *velocity* [(float)](https://docs.python.org/3/library/functions.html#float): The velocity at which to move in millimeters per second.
Negative implies backwards. -->

**Returns:**

- *mmPerSec* [(float64)](https://pkg.go.dev/builtin#float64): The velocity

[Python SDK Docs: **get_end_position**](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_end_position)

```python
myArm = ArmClient.from_robot(robot=robot, name='my_arm')
# TEMP TEMP Move the base 10 mm at a velocity of 1 mm/s, forward
pos = await myArm.get_end_position()
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- extra [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error, if one occurred.
- [spatialmath.Pose](https://pkg.go.dev/go.viam.com/rdk@v0.2.12/spatialmath#Pose): A representation of the arm's current position as a 6dof pose, position and orientation, with respect to the origin. See [Go SDK Docs: **Pose**](https://pkg.go.dev/go.viam.com/rdk@v0.2.12/spatialmath#Pose) and [Python SDK Docs: **pose**](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Pose) for more information on how to use a Pose.

[Go SDK Docs: **GetEndPosition**](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm)

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}
// TEMP TEMP Move the base forward 10 mm at a velocity of 1 mm/s
myArm.GetEndPosition(context.Background(), temp: 10, temp: 1)
// TEMP TEMP Move the base backward 10 mm at a velocity of -1 mm/s
myArm.GetEndPosition(context.Background(), temp: 10, temp: -1)
```

{{% /tab %}}
{{< /tabs >}}

### MoveToPosition

<!-- Move the base in a straight line across the given distance (*mm*) at the given velocity (*mm/sec*). -->

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

<!-- - *distance* [(int)](https://docs.python.org/3/library/functions.html#int): The distance to move in millimeters.
Negative implies backwards.
- *velocity* [(float)](https://docs.python.org/3/library/functions.html#float): The velocity at which to move in millimeters per second.
Negative implies backwards. -->

**Returns:**

- None

[Python SDK Docs: **move_to_position**](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.move_to_position)

```python
myArm = ArmClient.from_robot(robot=robot, name='my_arm')
# TEMP TEMP Move the arm 10 mm at a velocity of 1 mm/s, forward
await myArm.move_to_position(temp=10, temp=1)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
<!-- - *distanceMm* [(int)](https://pkg.go.dev/builtin#int): The distance to move the base in millimeters.
Negative implies backwards.
- *mmPerSec* [(float64)](https://pkg.go.dev/builtin#float64): The velocity at which to move the base in millimeters per second.
Negative implies backwards. -->
- extra [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error, if one occurred.

[Go SDK Docs: **MoveToPosition**](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm)

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}
// TEMP TEMP Move the base forward 10 mm at a velocity of 1 mm/s
myArm.MoveToPosition(context.Background(), temp: 10, temp: 1)
```

{{% /tab %}}
{{< /tabs >}}

### MoveToJointPositions

<!-- Move the base in a straight line across the given distance (*mm*) at the given velocity (*mm/sec*). -->

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

<!-- - *distance* [(int)](https://docs.python.org/3/library/functions.html#int): The distance to move in millimeters.
Negative implies backwards.
- *velocity* [(float)](https://docs.python.org/3/library/functions.html#float): The velocity at which to move in millimeters per second.
Negative implies backwards. -->

**Returns:**

- None

[Python SDK Docs: **move_to_joint_positions**](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.move_to_joint_positions)

```python
myArm = ArmClient.from_robot(robot=robot, name='my_arm')
# TEMP TEMP Move the base 10 mm at a velocity of 1 mm/s, forward
await myArm.move_to_joint_positions(temp=10, temp=1)
# TEMP TEMPMove the base 10 mm at a velocity of -1 mm/s, backward
await myBase.move_to_joint_positions(temp=10, temp=-1)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
<!-- - *distanceMm* [(int)](https://pkg.go.dev/builtin#int): The distance to move the base in millimeters.
Negative implies backwards.
- *mmPerSec* [(float64)](https://pkg.go.dev/builtin#float64): The velocity at which to move the base in millimeters per second.
Negative implies backwards. -->
- extra [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error, if one occurred.

[Go SDK Docs: **MoveToJointPositions**](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm)

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}
// TEMP TEMP Move the base forward 10 mm at a velocity of 1 mm/s
myArm.MoveToJointPositions(context.Background(), temp: 10, temp: 1)
// TEMP TEMP Move the base backward 10 mm at a velocity of -1 mm/s
myArm.MoveToJointPositions(context.Background(), temp: 10, temp: -1)
```

{{% /tab %}}
{{< /tabs >}}

### GetJointPositions

<!-- Move the base in a straight line across the given distance (*mm*) at the given velocity (*mm/sec*). -->

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

<!-- - *distance* [(int)](https://docs.python.org/3/library/functions.html#int): The distance to move in millimeters.
Negative implies backwards.
- *velocity* [(float)](https://docs.python.org/3/library/functions.html#float): The velocity at which to move in millimeters per second.
Negative implies backwards. -->

**Returns:**

- None

[Python SDK Docs: **get_joint_positions**](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.get_joint_positions)

```python
myArm = ArmClient.from_robot(robot=robot, name='my_arm')
# TEMP TEMP Move the base 10 mm at a velocity of 1 mm/s, forward
await myArm.get_joint_positions(temp=10, temp=1)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
<!-- - *distanceMm* [(int)](https://pkg.go.dev/builtin#int): The distance to move the base in millimeters.
Negative implies backwards.
- *mmPerSec* [(float64)](https://pkg.go.dev/builtin#float64): The velocity at which to move the base in millimeters per second.
Negative implies backwards. -->
- extra [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error, if one occurred.

[Go SDK Docs: **GetEndPosition**](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm)

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}
// TEMP TEMP Move the base forward 10 mm at a velocity of 1 mm/s
myArm.GetJointPositions(context.Background(), temp: 10, temp: 1)
// TEMP TEMP Move the base backward 10 mm at a velocity of -1 mm/s
myArm.GetJointPositions(context.Background(), temp: 10, temp: -1)
```

{{% /tab %}}
{{< /tabs >}}

### Stop

<!-- Move the base in a straight line across the given distance (*mm*) at the given velocity (*mm/sec*). -->

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

<!-- - *distance* [(int)](https://docs.python.org/3/library/functions.html#int): The distance to move in millimeters.
Negative implies backwards.
- *velocity* [(float)](https://docs.python.org/3/library/functions.html#float): The velocity at which to move in millimeters per second.
Negative implies backwards. -->

**Returns:**

- None

[Python SDK Docs: **stop**](https://python.viam.dev/autoapi/viam/components/arm/client/index.html#viam.components.arm.client.ArmClient.stop)

```python
myArm = ArmClient.from_robot(robot=robot, name='my_arm')
# TEMP TEMP Move the base 10 mm at a velocity of 1 mm/s, forward
await myArm.move_to_position(temp=10, temp=1)
# TEMP TEMPMove the base 10 mm at a velocity of -1 mm/s, backward
await myArm.stop(temp=10, temp=-1)
```

{{% /tab %}}
{{% tab name="Golang" %}}

**Parameters:**

- [Context](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
<!-- - *distanceMm* [(int)](https://pkg.go.dev/builtin#int): The distance to move the base in millimeters.
Negative implies backwards.
- *mmPerSec* [(float64)](https://pkg.go.dev/builtin#float64): The velocity at which to move the base in millimeters per second.
Negative implies backwards. -->
- extra [(map[string]interface{})](https://pkg.go.dev/google.golang.org/protobuf/types/known/structpb): Extra options to pass to the underlying RPC call.

**Returns:**

- [error](https://pkg.go.dev/builtin#error): An error, if one occurred.

[Go SDK Docs: **GetEndPosition**](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm)

```go
myArm, err := arm.FromRobot(robot, "my_arm")
if err != nil {
  logger.Fatalf("cannot get arm: %v", err)
}
// TEMP TEMP Move the base forward 10 mm at a velocity of 1 mm/s
myArm.MoveToPosition(context.Background(), temp: 10, temp: 1)
// TEMP TEMP Move the base backward 10 mm at a velocity of -1 mm/s
myArm.Stop(context.Background(), temp: 10, temp: -1)
```

{{% /tab %}}
{{< /tabs >}}

<!-- ## IsMoving -->

## Next Steps

See also:

<a href="/services/motion">Viam's Motion Service</a>
