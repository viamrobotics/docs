---
title: "Motion Service"
linkTitle: "Motion"
weight: 20
type: "docs"
description: "The motion service enables your robot to plan and move its components relative to itself, other robots, and the world."
tags: ["motion", "motion planning", "services"]
icon: "/services/icons/motion.svg"
no_list: true
aliases:
  - "/services/motion/"
# SME: Motion team
---

The motion service enables your robot to plan and move itself or its components relative to itself, other robots, and the world.
The motion service:

1. Gathers the current positions of the robot’s components as defined with the [frame system](../frame-system/).
2. Plans the necessary motions to move a component to a given destination while obeying any [constraints you configure](constraints/).

The motion service can:

- use motion [planning algorithms](algorithms/) locally on your robot to plan coordinated motion across many components.
- pass movement requests through to individual components which have implemented their own motion planning.

## Used With

{{< cards >}}
{{< relatedcard link="/mobility/frame-system/" >}}
{{< relatedcard link="/components/movement-sensor/" required="yes">}}
{{< relatedcard link="/components/base/" >}}
{{< relatedcard link="/components/arm/" >}}
{{< relatedcard link="/components/gripper/" >}}
{{< /cards >}}

{{% snippet "required-legend.md" %}}

## Configuration

You need to configure frames for your robot's components with the [frame system](../frame-system/).
This defines the spatial context within which the motion service operates.

The motion service itself is enabled on the robot by default, so you do not need to do any extra configuration in the [Viam app](https://app.viam.com/) to enable it.

{{% alert title="Tip" color="tip" %}}

Because the motion service is enabled by default, you don't give it a `"name"` while configuring it.
Use the name `"builtin"` to access the built-in motion service in your code with methods like [`FromRobot()`](/build/program/apis/#fromrobot) that require a `ResourceName`.

{{% /alert %}}

## API

The motion service supports the following methods:

{{< readfile "/static/include/services/apis/motion.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured with a gripper, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

{{% alert title="Important" color="note" %}}

When using Viam component APIs, you generally pass the component name of type `string` as an argument to the methods.
When using the motion service, you pass an argument of type `ResourceName` instead of the string name.
For examples showing how to construct the `ResourceName`, see the code samples below or [this tutorial](/tutorials/services/plan-motion-with-arm-gripper/#get-the-resourcename).

{{% /alert %}}

### Move

The `Move` method is the primary way to move multiple components, or to move any object to any other location.
Given a destination pose and a component to move to that destination, `Move` will:

1. Construct a full kinematic chain from goal to destination including all movable components in between.
2. Solve that chain to move the specified component frame to the destination while adhering to any constraints.
3. Execute that movement to move the actual robot.
4. Return whether or not this process succeeded.

The motion service takes the volumes associated with all configured robot components (local and remote) into account for each request to ensure that the robot does not collide with itself or other known objects.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): The `ResourceName` of the piece of the robot that should arrive at the destination.
  Note that `move` moves the distal end of the component to the destination.
  For example, when moving a robotic arm, the piece that will arrive at the destination is the end effector attachment point, not the base of the arm.

- `destination` ([PoseInFrame](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame)):
  Describes where the `component_name` frame should be moved to.
  Can be any pose, from the perspective of any component whose location is configured as a [`frame`](../frame-system/).

  Note that the destination pose is relative to the distal end of the specified frame.
  This means that if the `destination` is the same as the `component_name` frame, for example an arm's frame, then a pose of {X: 10, Y: 0, Z: 0} will move that arm’s end effector by 10 mm in the local X direction.

- `world_state` ([WorldState](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState)) (_optional_): Data structure specifying information about the world around the robot.
  Used to augment the motion solving process.
  `world_state` includes obstacles and transforms:

  - **Obstacles**: Geometries located at a pose relative to some frame.
    When solving a motion plan with movable frames that contain inherent geometries, the solved path is constrained such that none of those inherent geometries intersect with the obstacles.
    Important considerations:
    - If a motion begins with a component already in collision with an obstacle, collisions between that specific component and that obstacle will not be checked.
    - The motion service assumes that obstacles are static.
      If a worldstate obstacle is physically attached to a part of the robot such that it will move with the robot, specify it with _transforms_.
    - Obstacles are defined by a pose and a [geometry](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.Geometry) with dimensions.
      The pose location is the point at the center of the geometry.
    - Obstacle locations are defined with respect to the _origin_ of the specified frame.
      Their poses are relative to the _origin_ of the specified frame.
      An obstacle associated with the frame of an arm with a pose of {X: 0, Y: 0, Z: -10} is interpreted as being 10mm below the base of the arm, not 10mm below the end effector.
      This is different from `destination` and `component_name`, where poses are relative to the distal end of a frame.
  - **Transforms**: A list of `PoseInFrame` messages that specify other transformations to temporarily add to the frame system at solve time.
    Transforms can be used to account for geometries that are attached to the robot but not configured as robot components.
    For example, you could use a transform to represent the volume of a marker held in your robot's gripper.
    Transforms are not added to the config or carried into later processes.

- `constraints` ([Constraints](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.Constraints)) (_optional_): Pass in [motion constraints](./constraints/).
  By default, motion is unconstrained with the exception of obstacle avoidance.

- `extra` (Mapping[str, Any]) (_optional_): A generic struct, containing extra options to pass to the underlying RPC call.

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
moved = await motion.move(component_name=gripper_name,
                          destination=PoseInFrame(reference_frame="myFrame",
                                                  pose=goal_pose),
                          world_state=worldState,
                          constraints={},
                          extra={})
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

- `componentName` ([resource.Name](https://pkg.go.dev/go.viam.com/rdk/resource#Name)): The `resource.Name` of the piece of the robot that should arrive at the destination.
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
    - The motion service assumes that obstacles are static.
      If a worldstate obstacle is physically attached to a part of the robot such that it will move with the robot, specify it with _transforms_.
    - Obstacles are defined by a pose and a [geometry](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry) with dimensions.
      The pose location is the point at the center of the geometry.
    - Obstacle locations are defined with respect to the _origin_ of the specified frame.
      Their poses are relative to the _origin_ of the specified frame.
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

### GetPose

`GetPose` gets the location and orientation of a component within the [frame system](../frame-system/).
The return type of this function is a `PoseInFrame` describing the pose of the specified component with respect to the specified destination frame.
You can use the `supplemental_transforms` argument to augment the robot's existing frame system with supplemental frames.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): The `ResourceName` of the piece of the robot whose pose is returned.

- `destination_frame` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)):
  The name of the frame with respect to which the component's pose is reported.

- `supplemental_transforms` ([Optional\[List\[Transforms\]\]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)) (_optional_): A list of `Transform` objects.
  A `Transform` represents an additional frame which is added to the robot's frame system.
  It consists of the following fields:

  - `pose_in_observer_frame`: Provides the relationship between the frame being added and another frame.
  - `physical_object`: An optional `Geometry` can be added to the frame being added.
  - `reference_frame`: Specifies the name of the frame which will be added to the frame system.

  When `supplemental_transforms` are provided, a frame system is created within the context of the `GetPose` function.
  This new frame system builds off the robot's frame system and incorporates the `Transform`s provided.
  If the result of adding the `Transform`s results in a disconnected frame system, an error is thrown.

- `extra` (Mapping[str, Any]) (_optional_): A generic struct, containing extra options to pass to the underlying RPC call.

**Returns:**

- [(PoseInFrame)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame): The pose of the component.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.MotionClient.get_pose).

The following code example gets the pose of the tip of a [gripper](/components/gripper/) named `my_gripper` which is attached to the end of an arm, in the "world" `reference_frame`:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.gripper import Gripper
from viam.services.motion import MotionClient

# Assume that the connect function is written and will return a valid robot.
robot = await connect()

motion = MotionClient.from_robot(robot=robot, name="builtin")
gripperName = Gripper.get_resource_name("my_gripper")
gripperPoseInWorld = await motion.get_pose(component_name=gripperName,
                                           destination_frame="world")
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
objectTransform = Transform(reference_frame="object",
                            pose_in_observer_frame=objectPoseInFrame)
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

- `componentName` ([resource.Name](https://pkg.go.dev/go.viam.com/rdk/resource#Name)): The `resource.Name` of the piece of the robot whose pose is returned.

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

  "go.viam.com/rdk/components/gripper"
  "go.viam.com/rdk/logging"
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/services/motion"
)

// Insert code to connect to your robot.
// (see code sample tab of your robot's page in the Viam app)

// Assumes a gripper configured with name "my_gripper" on the robot
gripperName := Gripper.Named("my_gripper")
myFrame := "my_gripper_offset"

 // Access the motion service
motionService, err := motion.FromRobot(robot, "builtin")
if err != nil {
  logger.Fatal(err)
}

myArmMotionPose, err := motionService.GetPose(context.Background(), my_gripper, referenceframe.World, nil, nil)
if err != nil {
  logger.Fatal(err)
}
logger.Info("Position of myArm from the motion service:", myArmMotionPose.Pose().Point())
logger.Info("Orientation of myArm from the motion service:", myArmMotionPose.Pose().Orientation())
```

{{% /tab %}}
{{< /tabs >}}

### MoveOnMap

Move a [base](/components/base/) component to a [`Pose`](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) in respect to the origin of a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): The `ResourceName` of the base to move.
- `destination` ([Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose)): The destination, which can be any [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) with respect to the SLAM map's origin.
- `slam_service_name` ([ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)): The `ResourceName` of the {{< glossary_tooltip term_id="slam" text="SLAM service" >}} from which the SLAM map is requested.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): Whether the request to `MoveOnMap` was successful.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.MotionClient.move_on_map).

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")

# Get the ResourceNames of the base and SLAM service
my_base_resource_name = Base.get_resource_name("my_base")
my_slam_resource_name = SLAMClient.get_resource_name("my_slam_service")

# Define a destination pose with respect to the origin of the map from the SLAM
# service "my_slam_service"
my_pose = Pose(y=10)

# Move the base component to the destination pose of Y=10, a location of
# (0, 10, 0) in respect to the origin of the map
success = await motion.move_on_map(component_name=my_base_resource_name,
                                   destination=my_pose,
                                   slam_service_name=my_slam_resource_name)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to move.
- `destination` [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk@v0.2.50/spatialmath#Pose): The destination, which can be any [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) with respect to the SLAM map's origin.
- `slamName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the {{< glossary_tooltip term_id="slam" text="SLAM service" >}} from which the SLAM map is requested.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): Whether the request to `MoveOnMap` was successful.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk@v0.2.50/services/motion#Service).

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")

// Get the resource.Names of the base and of the SLAM service
myBaseResourceName := base.Named("myBase")
mySLAMServiceResourceName := slam.Named("my_slam_service")
// Define a destination Pose with respect to the origin of the map from the SLAM service "my_slam_service"
myPose := spatialmath.NewPoseFromPoint(r3.Vector{Y: 10})

// Move the base component to the destination pose of Y=10, a location of (0, 10, 0) in respect to the origin of the map
success, err := motionService.MoveOnMap(context.Background(), myBaseResourceName, myPose, mySLAMServiceResourceName, nil)
```

{{% /tab %}}
{{< /tabs >}}

### MoveOnGlobe

Move a [base](/components/base/) component to a destination GPS point, represented in geographic notation _(latitude, longitude)_.
Use a [movement sensor](/components/movement-sensor/) to check the location of the robot.

{{< alert title="Usage" color="tip" >}}

`MoveOnGlobe()` is non blocking, meaning the motion service will move the component to the destination GPS point after `MoveOnGlobe()` returns.

Each successful `MoveOnGlobe()` call retuns a unique ExectionID which you can use to identify all plans generated durring the `MoveOnGlobe()`.

You can monitor the progress of the `MoveOnGlobe()` call by querying `GetPlan()` and `ListPlanStatuses()`.

`MoveOnGlobe()` is intended for use with the [navigation service](/mobility/navigation/), providing autonomous GPS navigation for rover [bases](/components/base/).

To use `MoveOnGlobe()`, your movement sensor must be able to measure the GPS location and orientation of the robot.

Make sure the [movement sensor](/components/movement-sensor/) you use supports usage of the following methods in its {{< glossary_tooltip term_id="model" text="model's" >}} implementation of the [movement sensor API](/components/movement-sensor/#api).

- It must support `GetPosition()` to report the robot's current GPS location.
- It must **also** support **either** `GetCompassHeading()` or `GetOrientation()` to report which way the robot is facing.
- If your movement sensor provides multiple methods, your robot will default to using the values returned by `GetCompassHeading()`.

{{< /alert >}}

{{< alert title="Stability Notice" color="alert" >}}

The `heading` parameter is experimental.
Specifying `heading` in a request to `MoveOnGlobe` is not currently recommended if the minimum turning radius of your component is greater than zero, as this combination may cause high latency in the [motion planning algorithms](/mobility/motion/algorithms/).

Specifying `obstacles` in a request to `MoveOnGlobe()` will cause an error if you configure a `"translation"` in the `"geometries"` of any of the `GeoObstacle` objects.
Translation in obstacles is not supported by the [navigation service](/mobility/navigation/).

{{< /alert >}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` [(ResourceName)](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName): The `ResourceName` of the base to move.
- `destination` [(GeoPoint)](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.GeoPoint): The location of the component's destination, represented in geographic notation as a [GeoPoint](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.GeoPoint) _(lat, lng)_.
- `movement_sensor_name` [(ResourceName)](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName): The `ResourceName` of the [movement sensor](/components/movement-sensor/) that you want to use to check the robot's location.
- `obstacles` [(Optional[Sequence[GeoObstacle]])](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.GeoObstacle): Obstacles to consider when planning the motion of the component, with each represented as a `GeoObstacle`. <ul><li> Default: `None` </li></ul>
- `heading` [(Optional[float])](https://docs.python.org/library/typing.html#typing.Optional): The compass heading, in degrees, that the robot's movement sensor should report at the `destination` point. <ul><li> Range: `[0-360)` 0: North, 90: East, 180: South, 270: West </li><li>Default: `None`</li></ul>
- `configuration` [(Optional[MotionConfiguration])](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.MotionConfiguration): The configuration you want to set across this robot for this motion service. This parameter and each of its fields are optional.
  - `obstacle_detectors` [(Iterable[ObstacleDetector])](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.ObstacleDetector): The names of each [vision service](/ml/vision/) and [camera](/components/camera/) resource pair you want to use for transient obstacle avoidance.
  - `position_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the position of the robot.
  - `obstacle_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the vision service for new obstacles.
  - `plan_deviation_m` [(float)](https://docs.python.org/3/library/functions.html#float): The distance in millimeters that the machine can deviate from the motion plan.
  - `linear_m_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Linear velocity this machine should target when moving.
  - `angular_degs_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Angular velocity this machine should target when turning.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): ExecutionID of the `MoveOnGlobe` call.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.MotionClient.move_on_globe).

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")

# Get the ResourceNames of the base and movement sensor
my_base_resource_name = Base.get_resource_name("my_base")
mvmnt_sensor_resource_name = MovementSensor.get_resource_name(
    "my_movement_sensor")
#  Define a destination GeoPoint at the GPS coordinates [0, 0]
my_destination = movement_sensor.GeoPoint(latitude=0, longitude=0)

# Move the base component to the designated geographic location, as reported by
# the movement sensor
execution_id = await motion.move_on_globe(
    component_name=my_base_resource_name,
    destination=my_destination,
    movement_sensor_name=mvmnt_sensor_resource_name)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [MoveOnGlobeReq](https://pkg.go.dev/go.viam.com/rdk/services/motion@v0.15.1#MoveOnGlobeReq): A `MoveOnGlobeReq` which contains the following values:
  - `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to move.
  - `destination` [(\*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): The location of the component's destination, represented in geographic notation as a [Point](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point) _(lat, lng)_.
  - `heading` [(float64)](https://pkg.go.dev/builtin#float64): The compass heading, in degrees, that the robot's movement sensor should report at the `destination` point. <ul><li> Range: `[0-360)` 0: North, 90: East, 180: South, 270: West</li><li>Default: `0`</li></ul>
  - `movementSensorName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the [movement sensor](/components/movement-sensor/) that you want to use to check the robot's location.
  - `obstacles` [([]\*spatialmath.GeoObstacle)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#GeoObstacle): Obstacles to consider when planning the motion of the component, with each represented as a `GeoObstacle`. <ul><li> Default: `nil` </li></ul>
  - `motionConfig` [(\*MotionConfiguration)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MotionConfiguration): The configuration you want to set across this robot for this motion service. This parameter and each of its fields are optional.
    - `ObstacleDetectors` [([]ObstacleDetectorName)](https://pkg.go.dev/go.viam.com/rdk/services/motion#ObstacleDetectorName): The names of each [vision service](/ml/vision/) and [camera](/components/camera/) resource pair you want to use for transient obstacle avoidance.
    - `PositionPollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the position of the robot.
    - `ObstaclePollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the vision service for new obstacles.
    - `PlanDeviationMM` [(float64)](https://pkg.go.dev/builtin#float64): The distance in millimeters that the machine can deviate from the motion plan.
    - `LinearMPerSec` [(float64)](https://pkg.go.dev/builtin#float64): Linear velocity this machine should target when moving.
    - `AngularDegsPerSec` [(float64)](https://pkg.go.dev/builtin#float64): Angular velocity this machine should target when turning.
  - `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(ExecutionID)](https://pkg.go.dev/go.viam.com/rdk/services/motion@v0.15.1#ExecutionID): ExecutionID of the `MoveOnGlobe` call.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")

// Get the resource.Names of the base and movement sensor
myBaseResourceName := base.Named("myBase")
myMvmntSensorResourceName := movement_sensor.Named("my_movement_sensor")
// Define a destination Point at the GPS coordinates [0, 0]
myDestination := geo.NewPoint(0, 0)

// Move the base component to the designated geographic location, as reported by the movement sensor
ctx := context.Background()
executionID, err := motionService.MoveOnGlobe(ctx, motion.MoveOnGlobeReq{
    ComponentName:      myBaseResourceName,
    Destination:        myDestination,
    MovementSensorName: myMvmntSensorResourceName,
})
```

{{% /tab %}}
{{< /tabs >}}

### StopPlan

Stop a [base](/components/base/) component being moved by an in progress [`MoveOnGlobe`](/mobility/motion/#moveonglobe) call.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` [(ResourceName)](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName): The `ResourceName` of the base to stop.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(None)](https://docs.python.org/3/library/stdtypes.html#the-null-object)

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.MotionClient.stop_plan).

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")
my_base_resource_name = Base.get_resource_name("my_base")

# Assuming a move_on_globe started started the execution
# mvmnt_sensor = MovementSensor.get_resource_name("my_movement_sensor")
# my_destination = movement_sensor.GeoPoint(latitude=0, longitude=0)
# execution_id = await motion.move_on_globe(
#    component_name=my_base_resource_name,
#    destination=my_destination,
#    movement_sensor_name=mvmnt_sensor_resource_name)

# Stop the base component which was instructed to move by `MoveOnGlobe()`
my_base_resource_name = Base.get_resource_name("my_base")
await motion.stop_plan(component_name=mvmnt_sensor)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [StopPlanReq](https://pkg.go.dev/go.viam.com/rdk/services/motion@v0.15.1#StopPlanReq): A `StopPlanReq` which contains the following values:
  - `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to stop.
  - `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")
myBaseResourceName := base.Named("myBase")
ctx := context.Background()

// Assuming a move_on_globe started started the execution
// myMvmntSensorResourceName := movement_sensor.Named("my_movement_sensor")
// myDestination := geo.NewPoint(0, 0)
// executionID, err := motionService.MoveOnGlobe(ctx, motion.MoveOnGlobeReq{
//     ComponentName:      myBaseResourceName,
//     Destination:        myDestination,
//     MovementSensorName: myMvmntSensorResourceName,
// })

// Stop the base component which was instructed to move by `MoveOnGlobe()`
err := motionService.StopPlan(context.Background(), motion.StopPlanReq{
    ComponentName: s.req.ComponentName,
})
```

{{% /tab %}}
{{< /tabs >}}

### GetPlan

Returns the plan history of the most recent [`MoveOnGlobe`](/mobility/motion/#moveonglobe) call to move a [base](/components/base/) component.

Returns a result if both of the following conditions are met:

- the execution (call to `MoveOnGlobe`) is still executing **or** changed state within the last 24 hours
- the robot has not reinitialized

Plans never change.

Replans always create new plans.

Replans share the ExecutionID of the previously executing plan.

All repeated fields are in time ascending order.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` [(ResourceName)](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName): The `ResourceName` of the base to stop.
- `lastPlanOnly` [(Optional\[bool\])](https://docs.python.org/library/typing.html#typing.Optional): If `true`, the response will only return the the last plan for the component / execution
- `executionID` [(Optional\[str\])](https://docs.python.org/library/typing.html#typing.Optional): If non empty, the response will return the plans of the provided execution & component. Useful for retrieving plans from executions before the current execution.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(GetPlanResponse)](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.GetPlanResponse)

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.MotionClient.get_plan).

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")
my_base_resource_name = Base.get_resource_name("my_base")
# Get the plan(s) of the base component which was instructed
# to move by `MoveOnGlobe()`
resp = await motion.get_plan(component_name=my_base_resource_name)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [PlanHistoryReq](https://pkg.go.dev/go.viam.com/rdk/services/motion@v0.15.1#PlanHistoryReq): A `PlanHistoryReq` which contains the following values:
  - `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to stop.
  - `lastPlanOnly` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the response will only return the the last plan for the component / execution
  - `executionID` [(ExecutionID)](https://pkg.go.dev/go.viam.com/rdk/services/motion@v0.15.1#PlanHistoryReq): If non empty, the response will return the plans of the provided execution & component. Useful for retrieving plans from executions before the current execution.
  - `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]PlanWithStatus)](https://pkg.go.dev/go.viam.com/rdk/services/motion@v0.15.1#PlanWithStatus): PlanWithStatus contains a plan, its current status, and all state changes that came prior sorted by ascending timestamp.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")
# Get the plan(s) of the base component's most recent execution i.e. `MoveOnGlobe()` call.
ctx := context.Background()
planHistory, err := motionService.PlanHistory(ctx, motion.PlanHistoryReq{
    ComponentName: s.req.ComponentName,
})
```

{{% /tab %}}
{{< /tabs >}}

### ListPlanStatuses

Returns the statuses of plans created by [`MoveOnGlobe`](/mobility/motion/#moveonglobe) calls that meet at least one of the following conditions since the motion service initialized:

- the plan's status is in progress
- the plan's status changed state within the last 24 hours

All repeated fields are in chronological order.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `onlyActivePlans` [(Optional\[bool\])](https://docs.python.org/library/typing.html#typing.Optional): If `true`, the response will only return plans which are executing.
- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(ListPlanStatusesResponse)](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.ListPlanStatusesResponse)

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/index.html#viam.services.motion.MotionClient.list_plan_statuses).

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")
# List the plan statuses of the motion service within the TTL
resp = await motion.list_plan_statuses()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [ListPlanStatusesReq](https://pkg.go.dev/go.viam.com/rdk/services/motion@v0.15.1#ListPlanStatusesReq): A `ListPlanStatusesReq` which contains the following values:
  - `onlyActivePlans` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the response will only return plans which are executing.
  - `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]PlanStatusWithID)](https://pkg.go.dev/go.viam.com/rdk/services/motion@v0.15.1#PlanStatusWithID): PlanStatusWithID describes the state of a given plan at a point in time plus the PlanId, ComponentName and ExecutionID the status is associated with.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")
# Get the plan(s) of the base component's most recent execution i.e. `MoveOnGlobe()` call.
ctx := context.Background()
planStatuses, err := motionService.ListPlanStatuses(ctx, motion.ListPlanStatusesReq{})
```

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own motion service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.do_command).

```python {class="line-numbers linkable-line-numbers"}
# Access the motion service
motion = MotionClient.from_robot(robot=robot, name="builtin")

my_command = {
  "command": "dosomething",
  "someparameter": 52
}

await motion.do_command(my_command)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map\[string\]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
// Access the motion service
motionService, err := motion.FromRobot(robot, "builtin")

resp, err := motionService.DoCommand(ctx, map[string]interface{}{"command": "dosomething", "someparameter": 52})
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
motion = MotionClient.from_robot(robot, "builtin")

await motion.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(robot, "builtin")

err := motionService.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

## Next steps

The following tutorials contain complete example code for interacting with a robot arm through the arm component API, and with the motion service API, respectively:

{{< cards >}}
{{% card link="/tutorials/services/accessing-and-moving-robot-arm" %}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper" %}}
{{< /cards >}}
