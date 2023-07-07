---
title: "Motion Service"
linkTitle: "Motion"
weight: 40
type: "docs"
description: "The Motion Service enables your robot to plan and move its components relative to itself, other robots, and the world."
tags: ["motion", "motion planning", "services"]
icon: "/services/img/icons/motion.svg"
no_list: true
# SME: Motion team
---

The Motion Service enables your robot to plan and move itself or its components relative to itself, other robots, and the world.
The Motion Service:

1. Gathers the current positions of the robot’s components as defined with the [Frame System](../frame-system/).
2. Plans the necessary motions to move a component to a given destination while obeying any [constraints you configure](constraints/).

The Motion Service can:

- use motion [planning algorithms](algorithms/) locally on your robot to plan coordinated motion across many components.
- pass movement requests through to individual components which have implemented their own motion planning.

## Configuration

You need to configure frames for your robot's components with the [Frame System](../frame-system/).
This defines the spatial context within which the Motion Service operates.

The Motion Service itself is enabled on the robot by default, so you do not need to do any extra configuration in the [Viam app](https://app.viam.com/) to enable it.

{{% alert title="Note" color="note" %}}

Because the Motion Service is enabled by default, you don't give it a `"name"` while configuring it.
Use the name `"builtin"` to access the built-in Motion Service in your code with methods like `FromRobot()` that require a `ResourceName`.

{{% /alert %}}

## API

The Motion Service supports the following methods:

Method Name | Description
----------- | -----------
[`Move`](#move) | Move multiple components in a coordinated way to achieve a desired motion.
[`MoveSingleComponent`](#movesinglecomponent) | Move a single component "manually."
[`GetPose`](#getpose) | Get the current location and orientation of a component.
[`MoveOnMap`](#moveonmap) | Move a component to a `Pose` in respect to the origin of a [SLAM](/services/slam/) map.

{{% alert title="Note" color="note" %}}

The following code examples assume that you have a robot configured with a gripper, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### Move

The `Move` method is the primary way to move multiple components, or to move any object to any other location.
Given a destination pose and a component to move to that destination, `Move` will:

1. Construct a full kinematic chain from goal to destination including all movable components in between.
2. Solve that chain to move the specified component frame to the destination while adhering to any constraints.
3. Execute that movement to move the actual robot.
4. Return whether or not this process succeeded.

The Motion Service takes the volumes associated with all configured robot components (local and remote) into account for each request to ensure that the robot does not collide with itself or other known objects.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): Name of the piece of the robot that should arrive at the destination.
  Note that `move` moves the distal end of the component to the destination.
  For example, when moving a robotic arm, the piece that will arrive at the destination is the end effector attachment point, not the base of the arm.

- `destination` ([PoseInFrame](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame)):
  Describes where the `component_name` frame should be moved to.
  Can be any pose, from the perspective of any component whose location is configured as a [`frame`](../frame-system/).

  Note that the destination pose is relative to the distal end of the specified frame.
  This means that if the `destination` is the same as the `component_name` frame, for example an arm's frame, then a pose of {X: 10, Y: 0, Z: 0} will move that arm’s end effector by 10 mm in the local X direction.

- `world_state` ([WorldState](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState)) (*optional*): Data structure specifying information about the world around the robot.
  Used to augment the motion solving process.
  `world_state` includes obstacles and transforms:
  - **Obstacles**: Geometries located at a pose relative to some frame.
    When solving a motion plan with movable frames that contain inherent geometries, the solved path is constrained such that none of those inherent geometries intersect with the obstacles.
    Important considerations:
    - If a motion begins with a component already in collision with an obstacle, collisions between that specific component and that obstacle will not be checked.
    - The Motion Service assumes that obstacles are static.
      If a worldstate obstacle is physically attached to a part of the robot such that it will move with the robot, specify it with *transforms*.
    - Obstacles are defined by a pose and a [geometry](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.Geometry) with dimensions.
      The pose location is the point at the center of the geometry.
    - Obstacle locations are defined with respect to the *origin* of the specified frame.
      Their poses are relative to the *origin* of the specified frame.
      An obstacle associated with the frame of an arm with a pose of {X: 0, Y: 0, Z: -10} is interpreted as being 10mm below the base of the arm, not 10mm below the end effector.
      This is different from `destination` and `component_name`, where poses are relative to the distal end of a frame.
  - **Transforms**: A list of `PoseInFrame` messages that specify other transformations to temporarily add to the frame system at solve time.
  Transforms can be used to account for geometries that are attached to the robot but not configured as robot components.
  For example, you could use a transform to represent the volume of a marker held in your robot's gripper.
  Transforms are not added to the config or carried into later processes.

- `constraints` ([Constraints](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.Constraints)) (*optional*): Pass in [motion constraints](./constraints/).
By default, motion is unconstrained with the exception of obstacle avoidance.

- `extra` (Mapping[str, Any]) (*optional*): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): Whether the move was successful.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.MotionClient.move).

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")

# Assumes a gripper configured with name "my_gripper" on the robot
gripper_name = Gripper.get_resource_name("my_gripper")
my_frame = "my_gripper_offset"

goal_pose = Pose(x=0, y=0, z=300, o_x=0, o_y=0, o_z=1, theta=0)

# Move the gripper
moved = await motion.move(component_name=gripper_name, destination=PoseInFrame(reference_frame="myFrame", pose=goal_pose), world_state=worldState, constraints={}, extra={})
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

- `componentName` ([resource.Name](https://pkg.go.dev/go.viam.com/rdk/resource#Name)): Name of the piece of the robot that should arrive at the destination.
  Note that `Move` moves the distal end of the component to the destination.
  For example, when moving a robotic arm, the piece that will arrive at the destination is the end effector attachment point, not the base of the arm.

- `destination` ([PoseInFrame](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame)):
  Describes where the `component_name` should end up.
  Can be any pose, from the perspective of any component whose location is configured as a [`frame`](../frame-system/).

  Note that the destination pose is relative to the distal end of the specified frame.
  This means that if the `destination` is the same as the `component_name` frame, for example an arm's frame, then a pose of {X: 10, Y: 0, Z: 0} will move that arm’s end effector by 10 mm in the local X direction.

- `worldState` ([WorldState](https://pkg.go.dev/go.viam.com/rdk/referenceframe#WorldState)): Data structure specifying information about the world around the robot.
  Used to augment the motion solving process.
  `worldState` includes obstacles and transforms:
  - **Obstacles**: Geometries located at a pose relative to some frame.
    When solving a motion plan with movable frames that contain inherent geometries, the solved path is constrained such that none of those inherent geometries intersect with the obstacles.
    Important considerations:
    - If a motion begins with a component already in collision with an obstacle, collisions between that specific component and that obstacle will not be checked.
    - The Motion Service assumes that obstacles are static.
      If a worldstate obstacle is physically attached to a part of the robot such that it will move with the robot, specify it with *transforms*.
    - Obstacles are defined by a pose and a [geometry](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry) with dimensions.
      The pose location is the point at the center of the geometry.
    - Obstacle locations are defined with respect to the *origin* of the specified frame.
      Their poses are relative to the *origin* of the specified frame.
      An obstacle associated with the frame of an arm with a pose of {X: 0, Y: 0, Z: -10} is interpreted as being 10mm below the base of the arm, not 10mm below the end effector.
      This is different from `destination` and `componentName`, where poses are relative to the distal end of a frame.
  - **Transforms**: A list of `PoseInFrame` messages that specify other transformations to temporarily add to the frame system at solve time.
  Transforms can be used to account for geometries that are attached to the robot but not configured as robot components.
  For example, you could use a transform to represent the volume of a marker held in your robot's gripper.
  Transforms are not added to the config or carried into later processes.

- `constraints` ([Constraints](https://pkg.go.dev/go.viam.com/api/service/motion/v1#Constraints)): Pass in optional [motion constraints](./constraints/).
  By default, motion is unconstrained with the exception of obstacle avoidance.

- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): Whether the move was successful.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")

// Assumes a gripper configured with name "my_gripper" on the robot
gripperName := Gripper.Named("my_gripper")
myFrame := "my_gripper_offset"

goalPose := PoseInFrame(0, 0, 300, 0, 0, 1, 0)

// Move the gripper
moved, err := motionService.Move(context.Background(), gripperName, goalPose, worldState, nil, nil)
```

{{% /tab %}}
{{< /tabs >}}

### MoveSingleComponent

The `MoveSingleComponent` method allows you to bypass Viam’s internal motion planning entirely, if desired, for a single component.
It looks similar to `Move` above but may result in radically different behavior.

`MoveSingleComponent` translates the given destination into the frame of the specified component, and then calls `MoveToPosition` on that component to move it to the desired location.
As of April 25, 2023, [arms](/components/arm/) are the only component supported by `MoveSingleComponent`.

As the name of the method suggests, only the single component specified by `component_name` will actuate.

An example of when this may be useful is if you have implemented your own custom arm model, and wish to use your own motion planning for it.
Implement `MoveToPosition` on that arm using whatever method you desire to plan motion to the specified pose, and then use `MoveSingleComponent` to pass the destination in the frame of any other robot component.

{{% alert title="Note" color="note" %}} <a id="move-vs-movetoposition">

If you call this method on an arm that uses Viam’s motion planning on the backend, then this method is equivalent to using `robot.TransformPose` to transform the destination into the frame of the arm, and then calling [`MoveToPosition`](/components/arm/#movetoposition) on the arm directly.
Note that `arm.MoveToPosition` does not use `world_state`, so collision checking and obstacle avoidance *will not* be performed.

If you need collision checking and obstacle avoidance, use [`Move`](#move).

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): The name of the component to move.
  This component must support the `move_to_position` API call with a Pose.
  As of April 21, 2023, [arm](/components/arm/) is the only component so supported.

- `destination` ([PoseInFrame](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame)):
  Describes where the `component_name` should end up.
  Can be any pose, from the perspective of any component whose location is configured as a [`frame`](../frame-system/).
  The `destination` will be converted into the frame of the component specified in `component_name` when passed to `move_to_position`.

- `world_state` ([WorldState](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState)) (*optional*): Not used. See [note above](#move-vs-movetoposition).

- `extra` (Mapping[str, Any]) (*optional*): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): Whether the move was successful.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.MotionClient.move_single_component).

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")

# Assumes an arm configured with name "my_arm" on the robot
my_frame = "my_arm_offset"

goal_pose = Pose(x=0, y=400, z=0, o_x=0, o_y=0, o_z=1, theta=0)

# Move the arm
moved = await motion.move_to_position(component_name=my_arm, destination=PoseInFrame(reference_frame="myFrame", pose=goal_pose), world_state=worldState, extra={})
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

- `componentName` ([resource.Name](https://pkg.go.dev/go.viam.com/rdk/resource#Name)): The name of the component to move.
This component must support the `MoveToPosition` API call with a Pose.
As of April 21, 2023, [arm](/components/arm/) is the only component so supported.

- `destination` ([PoseInFrame](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame)):
  Describes where the `component_name` should end up.
  Can be any pose, from the perspective of any component whose location is configured as a [`frame`](../frame-system/).
  The `destination` will be converted into the frame of the component specified in `componentName` when passed to `MoveToPosition`.

- `worldState` ([WorldState](https://pkg.go.dev/go.viam.com/rdk/referenceframe#WorldState)): Not used. See [note above](#move-vs-movetoposition).

- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): Whether the move was successful.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")

// Assumes an arm configured with name "my_arm" on the robot
myFrame := "my_arm_offset"

goalPose := PoseInFrame(0, 400, 0, 0, 0, 1, 0)

// Move the arm
moved, err := motionService.MoveSingleComponent(context.TODO(), goalPose, worldState, nil)
```

{{% /tab %}}
{{< /tabs >}}

### MoveOnMap

Move a component to a [`Pose`](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) in respect to the origin of a [SLAM](/services/slam/) map.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): The `"name"` of the component to move.
- `destination` ([Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose)): The destination, which can be any [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) with respect to the SLAM map's origin.
- `slam_service_name` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): The `"name"` of the [SLAM Service](/services/slam/) from which the SLAM map is requested.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): Whether the request to `MoveOnMap` was successful.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.MotionClient.move_on_map).

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")

# Define a destination pose with respect to the origin of the map from the SLAM service "my_slam_service"
my_pose = Pose(y=10)

# Move the base component "my_base" to the destination pose of Y=10, a location of (0, 10, 0) in respect to the origin of the map
success = await motion.move_on_map(component_name="my_base", destination=my_pose, slam_service_name="my_slam_service")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `"name"` of the component to move.
- `destination` [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk@v0.2.50/spatialmath#Pose): The destination, which can be any [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) with respect to the SLAM map's origin.
- `slamName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `"name"` of the [SLAM Service](/services/slam/) from which the SLAM map is requested.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): Whether the request to `MoveOnMap` was successful.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.2.50/services/motion#Service).

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")

// Define a destination Pose with respect to the origin of the map from the SLAM service "my_slam_service"
myPose := spatialmath.NewPoseFromPoint(r3.Vector{Y: 10})

// Move the base component "my_base" to the destination pose of Y=10, a location of (0, 10, 0) in respect to the origin of the map
success, err := motionService.MoveOnMap(context.Background(), "my_base", myPose, "my_slam_service", nil)
```

{{% /tab %}}
{{< /tabs >}}

### GetPose

`GetPose` gets the location and orientation of a component within the [Frame System](../frame-system/).
The return type of this function is a `PoseInFrame` describing the pose of the specified component with respect to the specified destination frame.
You can use the `supplemental_transforms` argument to augment the robot's existing frame system with supplemental frames.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): Name of the piece of the robot whose pose is returned.

- `destination_frame` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)):
  The name of the frame with respect to which the component's pose is reported.

- `supplemental_transforms` ([Optional\[List\[Transforms\]\]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)) (*optional*): A list of `Transform`s.
  A `Transform` represents an additional frame which is added to the robot's frame system.
  It consists of the following fields:
  - `pose_in_observer_frame`: Provides the relationship between the frame being added and another frame.
  - `physical_object`: An optional `Geometry` can be added to the frame being added.
  - `reference_frame`: Specifies the name of the frame which will be added to the frame system.

  When `supplemental_transforms` are provided, a frame system is created within the context of the `GetPose` function.
  This new frame system builds off the robot's frame system and incorporates the `Transform`s provided.
  If the result of adding the `Transform`s results in a disconnected frame system, an error is thrown.

- `extra` (Mapping[str, Any]) (*optional*): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(PoseInFrame)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame): The pose of the component.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.MotionClient.get_pose).

The following code example gets the pose of the tip of a [gripper](../../components/gripper/) named `my_gripper` which is attached to the end of an arm, in the "world" `reference_frame`:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.gripper import Gripper
from viam.services.motion import MotionClient

# Assume that the connect function is written and will return a valid robot.
robot = await connect()

motion = MotionClient.from_robot(robot=robot, name="builtin")
gripperName = Gripper.get_resource_name("my_gripper")
gripperPoseInWorld = await robot.get_pose(component_name=gripperName, destination_frame="world")
```

For a more complicated example, take the same scenario and get the pose of the same gripper with respect to an object situated at a location (100, 200, 0) relative to the "world" frame:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.gripper import Gripper
from viam.services.motion import MotionClient
from viam.proto.common import Transform, PoseInFrame, Pose

# Assume that the connect function is written and will return a valid robot.
robot = await connect()

motion = MotionClient.from_robot(robot=robot, name="builtin")
objectPose = Pose(x=100, y=200, z=0, o_x=0, o_y=0, o_z=1, theta=0)
objectPoseInFrame = PoseInFrame(reference_frame="world", pose=objectPose)
objectTransform = Transform(reference_frame="object", pose_in_observer_frame=objectPoseInFrame)
gripperName = Gripper.get_resource_name("my_gripper")
gripperPoseInObjectFrame = await motion.get_pose(
  component_name=gripperName,
  destination_frame="world",
  supplemental_transforms=objectTransform
)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

- `componentName` ([resource.Name](https://pkg.go.dev/go.viam.com/rdk/resource#Name)): Name of the piece of the robot whose pose is returned.

- `destinationFrame` ([string](https://pkg.go.dev/builtin#string)):
  The name of the frame with respect to which the component's pose is reported.

- `supplementalTransforms` ([LinkInFrame](https://pkg.go.dev/go.viam.com/rdk/referenceframe#LinkInFrame)): An optional list of `LinkInFrame`s.
  A `LinkInFrame` represents an additional frame which is added to the robot's frame system.
  It consists of:
  - a `PoseInFrame`: Provides the relationship between the frame being added and another frame.
  - `Geometry`: An optional `Geometry` can be added to the frame being added.
  When `supplementalTransforms` are provided, a frame system is created within the context of the `GetPose` function.
  This new frame system builds off the robot's frame system and incorporates the `LinkInFrame`s provided.
  If the result of adding the `LinkInFrame`s results in a disconnected frame system, an error is thrown.

- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): The pose of the component.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

```go {class="line-numbers linkable-line-numbers"}
import (
  "context"

  "github.com/edaniels/golog"
  "go.viam.com/rdk/components/gripper"
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/services/motion"
)

// Insert code to connect to your robot.
// (see code sample tab of your robot's page in the Viam app)

// Assumes a gripper configured with name "my_gripper" on the robot
gripperName := Gripper.Named("my_gripper")
myFrame := "my_gripper_offset"

 // Access the Motion Service
motionService, err := motion.FromRobot(robot, "builtin")
if err != nil {
  logger.Fatal(err)
}

myArmMotionPose, err := motionService.GetPose(context.Background(), my_gripper, referenceframe.World, nil, nil)
if err != nil {
  logger.Fatal(err)
}
logger.Info("Position of myArm from the Motion Service:", myArmMotionPose.Pose().Point())
logger.Info("Orientation of myArm from the Motion Service:", myArmMotionPose.Pose().Orientation())
```

{{% /tab %}}
{{< /tabs >}}

## Next Steps

The following tutorials contain complete example code for interacting with a robot arm through the arm component API, and with the Motion Service API, respectively:

{{< cards >}}
  {{% card link="/tutorials/services/accessing-and-moving-robot-arm" %}}
  {{% card link="/tutorials/services/plan-motion-with-arm-gripper" %}}
{{< /cards >}}
