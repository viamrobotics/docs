### Move

The `Move` method is the primary way to move multiple components, or to move any object to any other location.
Given a destination pose and a component to move to that destination, `Move` will:

1. Construct a full kinematic chain from goal to destination including all movable components in between.
2. Solve that chain to move the specified component frame to the destination while adhering to any constraints.
3. Execute that movement to move the actual machine.
4. Return whether or not this process succeeded.

The motion service takes the volumes associated with all configured machine components (local and remote) into account for each request to ensure that the machine does not collide with itself or other known objects.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)) (required): The `ResourceName` of the piece of the robot that should arrive at the destination. Note that `move` moves the distal end of the component to the destination. For example, when moving a robotic arm, the piece that will arrive at the destination is the end effector attachment point, not the base of the arm.
- `destination` ([viam.proto.common.PoseInFrame](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame)) (required): Describes where the `component_name` frame should be moved to. Can be any pose, from the perspective of any component whose location is configured as a [`frame`](../frame-system/).
- `world_state` ([viam.proto.common.WorldState](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState)) (optional): Data structure specifying information about the world around the machine.
  Used to augment the motion solving process.
  `world_state` includes obstacles and transforms:

  - **Obstacles**: Geometries located at a pose relative to some frame.
    When solving a motion plan with movable frames that contain inherent geometries, the solved path is constrained such that none of those inherent geometries intersect with the obstacles.
    Important considerations:
    - If a motion begins with a component already in collision with an obstacle, collisions between that specific component and that obstacle will not be checked.
    - The motion service assumes that obstacles are static.
      If a worldstate obstacle is physically attached to a part of the robot such that it will move with the robot, specify it with _transforms_.
    - Obstacles are defined by a pose and a [geometry](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Geometry) with dimensions.
      The pose location is the point at the center of the geometry.
    - Obstacle locations are defined with respect to the _origin_ of the specified frame.
      Their poses are relative to the _origin_ of the specified frame.
      An obstacle associated with the frame of an arm with a pose of {X: 0, Y: 0, Z: -10} is interpreted as being 10mm below the base of the arm, not 10mm below the end effector.
      This is different from `destination` and `component_name`, where poses are relative to the distal end of a frame.
  - **Transforms**: A list of `PoseInFrame` messages that specify other transformations to temporarily add to the frame system at solve time.
    Transforms can be used to account for geometries that are attached to the robot but not configured as robot components.
    For example, you could use a transform to represent the volume of a marker held in your machine's gripper.
    Transforms are not added to the config or carried into later processes.
- `constraints` ([viam.proto.service.motion.Constraints](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.Constraints)) (optional): Pass in [motion constraints](./constraints/). By default, motion is unconstrained with the exception of obstacle avoidance.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Whether the move was successful (`true`) or unsuccessful (`false`).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")

# Assumes a gripper configured with name "my_gripper" on the machine
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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the piece of the robot that should arrive at the destination. Note that `Move` moves the distal end of the component to the destination. For example, when moving a robotic arm, the piece that will arrive at the destination is the end effector attachment point, not the base of the arm.
- `destination` [(*referenceframe.PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): Describes where the `component_name` should end up. Can be any pose, from the perspective of any component whose location is configured as a [`frame`](../frame-system/). Note that the destination pose is relative to the distal end of the specified frame. This means that if the `destination` is the same as the `component_name` frame, for example an arm's frame, then a pose of `{X: 10, Y: 0, Z: 0}` will move that arm’s end effector by 10 mm in the local `X` direction.
- `worldState` [(*referenceframe.WorldState)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#WorldState): Data structure specifying information about the world around the machine.
  Used to augment the motion solving process.
  `worldState` includes obstacles and transforms:

  - **Obstacles**: Geometries located at a pose relative to some frame.
    When solving a motion plan with movable frames that contain inherent geometries, the solved path is constrained such that none of those inherent geometries intersect with the obstacles.
    Important considerations:
    - If a motion begins with a component already in collision with an obstacle, collisions between that specific component and that obstacle will not be checked.
    - The motion service assumes that obstacles are static.
      If a worldstate obstacle is physically attached to a part of the robot such that it will move with the robot, specify it with _transforms_.
    - Obstacles are defined by a [(pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose) and a [(geometry)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry) with dimensions.
      The pose location is the point at the center of the geometry.
    - Obstacle locations are defined with respect to the _origin_ of the specified frame.
      Their poses are relative to the _origin_ of the specified frame.
      An obstacle associated with the frame of an arm with a pose of {X: 0, Y: 0, Z: -10} is interpreted as being 10mm below the base of the arm, not 10mm below the end effector.
      This is different from `destination` and `componentName`, where poses are relative to the distal end of a frame.
  - **Transforms**: A list of `PoseInFrame` messages that specify other transformations to temporarily add to the frame system at solve time.
    Transforms can be used to account for geometries that are attached to the robot but not configured as robot components.
    For example, you could use a transform to represent the volume of a marker held in your machine's gripper.
    Transforms are not added to the config or carried into later processes.
- `constraints` [(*motionplan.Constraints)](https://pkg.go.dev/go.viam.com/rdk/motionplan#Constraints): Pass in optional [motion constraints](./constraints/). By default, motion is unconstrained with the exception of obstacle avoidance.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): Whether the move was successful (`true`) or unsuccessful (`false`).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(machine, "builtin")

// Assumes a gripper configured with name "my_gripper" on the machine
gripperName := gripper.Named("my_gripper")

// Define a destination Pose
destination := referenceframe.NewPoseInFrame("world", spatialmath.NewPoseFromPoint(r3.Vector{X: 0.1, Y: 0.0, Z: 0.0}))

// Create obstacles
boxPose := spatialmath.NewPoseFromPoint(r3.Vector{X: 0.0, Y: 0.0, Z: 0.0})
boxDims := r3.Vector{X: 0.2, Y: 0.2, Z: 0.2} // 20cm x 20cm x 20cm box
obstacle, _ := spatialmath.NewBox(boxPose, boxDims, "obstacle_1")

geometryInFrame := referenceframe.NewGeometriesInFrame("base", []spatialmath.Geometry{obstacle})
obstacles := []*referenceframe.GeometriesInFrame{geometryInFrame}

// Create transforms
transform := referenceframe.NewLinkInFrame("gripper",
  spatialmath.NewPoseFromPoint(r3.Vector{X: 0.1, Y: 0.0, Z: 0.1}), "transform_1", nil
)
transforms := []*referenceframe.LinkInFrame{transform}

// Create WorldState
worldState, err := referenceframe.NewWorldState(obstacles, transforms)

// Move gripper component
moved, err := motionService.Move(context.Background(), gripperName, destination, worldState, nil, nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{< /tabs >}}

### MoveOnMap

Move a [base](/components/base/) component to a destination [pose](/internals/orientation-vector/) on a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map.

`MoveOnMap()` is non blocking, meaning the motion service will move the component to the destination [pose](/internals/orientation-vector/) after `MoveOnMap()` returns.

Each successful `MoveOnMap()` call returns a unique `ExecutionID` which you can use to identify all plans generated during the `MoveOnMap()` call.

{{< alert title="Info" color="info" >}}
If you specify a goal pose and the robot's current position is already within the set `PlanDeviationM`, then `MoveOnMap` returns an error.
{{< /alert >}}

You can monitor the progress of the `MoveOnMap()` call by querying `GetPlan()` and `ListPlanStatuses()`.

Use the machine's position reported by the {{< glossary_tooltip term_id="slam" text="SLAM" >}} service to check the location of the machine.

`MoveOnMap()` is intended for use with the [navigation service](/services/navigation/), providing autonomous indoor navigation for rover [bases](/components/base/).

{{< alert title="Requirements" color="info" >}}
To use `MoveOnMap()`, your [SLAM service](/services/slam/) must implement `GetPointCloudMap()` and `GetPosition()`

Make sure the [SLAM service](/services/slam/) you use alongside the this motion service supports the following methods in its {{< glossary_tooltip term_id="model" text="model's" >}} implementation of the [SLAM service API](/services/slam/#api):

- It must support `GetPointCloudMap()` to report the SLAM map as a pointcloud.
- It must support `GetPosition()` to report the machine's current location on the SLAM map.
  {{< /alert >}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.ResourceName)) (required): The `ResourceName` of the base to move.
- `destination` ([viam.proto.common.Pose](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.Pose)) (required): The destination, which can be any [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) with respect to the SLAM map's origin.
- `slam_service_name` ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.ResourceName)) (required): The `ResourceName` of the [SLAM service](/services/slam/) from which the SLAM map is requested.
- `configuration` ([viam.proto.service.motion.MotionConfiguration](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionConfiguration)) (optional): The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.
  - `obstacle_detectors` [(Iterable[ObstacleDetector])](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.ObstacleDetector): The names of each [vision service](/services/vision/) and [camera](/components/camera/) resource pair you want to use for transient obstacle avoidance.
  - `position_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the position of the machine.
  - `obstacle_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the vision service for new obstacles.
  - `plan_deviation_m` [(float)](https://docs.python.org/3/library/functions.html#float): The distance in meters that the machine can deviate from the motion plan. By default this is set to 2.6 m which is an appropriate value for outdoor usage. When you use the `MoveOnMap()` method from the **CONTROL** tab, the default is overwritten to 0.5 m for testing.
  - `linear_m_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Linear velocity this machine should target when moving.
  - `angular_degs_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Angular velocity this machine should target when turning.
- `obstacles` ([Iterable[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.Geometry)) (optional): Obstacles, specified in the SLAM frame coordinate system, to be considered when planning the motion of the component.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ExecutionID of the `MoveOnMap` call.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")

# Get the ResourceNames of the base component and SLAM service
my_base_resource_name = Base.get_resource_name("my_base")
my_slam_service_name = SLAMClient.get_resource_name("my_slam_service")

# Define a destination pose with respect to the origin of the map from the SLAM service "my_slam_service"
my_pose = Pose(y=10)

# Move the base component to the destination pose of Y=10, a location of
# (0, 10, 0) in respect to the origin of the map
execution_id = await motion.move_on_map(component_name=my_base_resource_name,
                                        destination=my_pose,
                                        slam_service_name=my_slam_service_name)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move_on_map).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [(MoveOnMapReq)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MoveOnMapReq): A `MoveOnMapReq` which contains the following values:
  - `ComponentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to move.
  - `Destination` [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): The destination, which can be any [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) with respect to the SLAM map's origin.
  - `SlamName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the [SLAM service](/services/slam/) from which the SLAM map is requested.
  - `MotionConfig` [(\*MotionConfiguration)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MotionConfiguration): The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.
    - `ObstacleDetectors` [([]ObstacleDetectorName)](https://pkg.go.dev/go.viam.com/rdk/services/motion#ObstacleDetectorName): The names of each [vision service](/services/vision/) and [camera](/components/camera/) resource pair you want to use for transient obstacle avoidance.
    - `PositionPollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the position of the machine.
    - `ObstaclePollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the vision service for new obstacles.
    - `PlanDeviationM` [(float64)](https://pkg.go.dev/builtin#float64): The distance in meters that the machine can deviate from the motion plan. By default this is set to 2.6 m which is an appropriate value for outdoor usage. When you use the the **CONTROL** tab, the underlying calls to `MoveOnMap()` use 0.5 m instead.
    - `LinearMPerSec` [(float64)](https://pkg.go.dev/builtin#float64): Linear velocity this machine should target when moving.
    - `AngularDegsPerSec` [(float64)](https://pkg.go.dev/builtin#float64): Angular velocity this machine should target when turning.
  - `Obstacles` [(\[\]spatialmath.Geometry)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Geometry): Obstacles, specified in the SLAM frame coordinate system, to be considered when planning the motion of the component.
  - `Extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(ExecutionID)](https://pkg.go.dev/go.viam.com/rdk/services/motion#ExecutionID): ExecutionID of the `MoveOnMap` call.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Assumes a base with the name "my_base" is configured on the machine
myBaseResourceName := base.Named("my_base")
mySLAMServiceResourceName := slam.Named("my_slam_service")

// Define a destination Pose
myPose := spatialmath.NewPoseFromPoint(r3.Vector{Y: 10})

// Move the base component to the destination pose
executionID, err := motionService.MoveOnMap(context.Background(), motion.MoveOnMapReq{
  ComponentName: myBaseResourceName,
  Destination:   myPose,
  SlamName:      mySLAMServiceResourceName,
})

// MoveOnMap is a non-blocking method and this line can optionally be added to block until the movement is done
err = motion.PollHistoryUntilSuccessOrError(
  context.Background(),
  motionService,
  time.Duration(time.Second),
  motion.PlanHistoryReq{
    ComponentName: myBaseResourceName,
    ExecutionID:   executionID,
  },
)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{< /tabs >}}

### MoveOnGlobe

Move a [base](/components/base/) component to a destination GPS point, represented in geographic notation _(latitude, longitude)_.
Use a [movement sensor](/components/movement-sensor/) to check the location of the machine.

`MoveOnGlobe()` is non blocking, meaning the motion service will move the component to the destination GPS point after `MoveOnGlobe()` returns.

Each successful `MoveOnGlobe()` call returns a unique `ExecutionID` which you can use to identify all plans generated during the `MoveOnGlobe()`.

{{< alert title="Info" color="info" >}}
If you specify a goal pose and the robot's current position is already within the set `PlanDeviationM`, `MoveOnGlobe` returns an error.
{{< /alert >}}

You can monitor the progress of the `MoveOnGlobe()` call by querying `GetPlan()` and `ListPlanStatuses()`.

`MoveOnGlobe()` is intended for use with the [navigation service](/services/navigation/), providing autonomous GPS navigation for rover [bases](/components/base/).

{{< alert title="Requirements" color="info" >}}
To use `MoveOnGlobe()`, your movement sensor must be able to measure the GPS location and orientation of the machine.

Make sure the [movement sensor](/components/movement-sensor/) you use supports usage of the following methods in its {{< glossary_tooltip term_id="model" text="model's" >}} implementation of the [movement sensor API](/components/movement-sensor/#api).

- It must support `GetPosition()` to report the machine's current GPS location.
- It must **also** support **either** `GetCompassHeading()` or `GetOrientation()` to report which way the machine is facing.
- If your movement sensor provides multiple methods, your machine will default to using the values returned by `GetCompassHeading()`.
  {{< /alert >}}

{{< alert title="Stability Notice" color="alert" >}}

The `heading` parameter is experimental.
Specifying `heading` in a request to `MoveOnGlobe` is not currently recommended if the minimum turning radius of your component is greater than zero, as this combination may cause high latency in the [motion planning algorithms](/services/motion/algorithms/).

Specifying `obstacles` in a request to `MoveOnGlobe()` will cause an error if you configure a `"translation"` in the `"geometries"` of any of the `GeoGeometry` objects.
Translation in obstacles is not supported by the [navigation service](/services/navigation/).

{{< /alert >}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.ResourceName)) (required): The `ResourceName` of the base to move.
- `destination` ([viam.proto.common.GeoPoint](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.GeoPoint)) (required): The location of the component's destination, represented in geographic notation as a [GeoPoint](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.GeoPoint) _(lat, lng)_.
- `movement_sensor_name` ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.ResourceName)) (required): The `ResourceName` of the [movement sensor](/components/movement-sensor/) that you want to use to check the machine's location.
- `obstacles` ([Sequence[viam.proto.common.GeoGeometry]](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.GeoGeometry)) (optional): Obstacles to consider when planning the motion of the component, with each represented as a `GeoGeometry`. <ul><li> Default: `None` </li></ul>
- `heading` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): The compass heading, in degrees, that the machine's movement sensor should report at the `destination` point. <ul><li> Range: `[0-360)` `0`: North, `90`: East, `180`: South, `270`: West </li><li>Default: `None`</li></ul>
- `configuration` ([viam.proto.service.motion.MotionConfiguration](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionConfiguration)) (optional): The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.
  - `obstacle_detectors` [(Iterable[ObstacleDetector])](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.ObstacleDetector): The names of each [vision service](/services/vision/) and [camera](/components/camera/) resource pair you want to use for transient obstacle avoidance.
  - `position_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the position of the machine.
  - `obstacle_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the vision service for new obstacles.
  - `plan_deviation_m` [(float)](https://docs.python.org/3/library/functions.html#float): The distance in meters that the machine can deviate from the motion plan.
  - `linear_m_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Linear velocity this machine should target when moving.
  - `angular_degs_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Angular velocity this machine should target when turning.
- `bounding_regions` ([Sequence[viam.proto.common.GeoGeometry]](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.GeoGeometry)) (optional): Set of obstacles which the robot must remain within while navigating.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ExecutionID of the `MoveOnGlobe` call.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")

# Get the ResourceNames of the base and movement sensor
my_base_resource_name = Base.get_resource_name("my_base")
mvmnt_sensor_resource_name = MovementSensor.get_resource_name(
    "my_movement_sensor")
#  Define a destination GeoPoint at the GPS coordinates [0, 0]
my_destination = movement_sensor.GeoPoint(latitude=0, longitude=0)

# Move the base component to the designated geographic location, as reported by the movement sensor
execution_id = await motion.move_on_globe(
    component_name=my_base_resource_name,
    destination=my_destination,
    movement_sensor_name=mvmnt_sensor_resource_name)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move_on_globe).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [(MoveOnGlobeReq)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MoveOnGlobeReq): A `MoveOnGlobeReq` which contains the following values:
  - `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to move.
  - `destination` [(\*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): The location of the component's destination, represented in geographic notation as a [Point](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point) _(lat, lng)_.
  - `heading` [(float64)](https://pkg.go.dev/builtin#float64): The compass heading, in degrees, that the machine's movement sensor should report at the `destination` point. <ul><li> Range: `[0-360)` 0: North, 90: East, 180: South, 270: West</li><li>Default: `0`</li></ul>
  - `movementSensorName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the [movement sensor](/components/movement-sensor/) that you want to use to check the machine's location.
  - `obstacles` [([]\*spatialmath.GeoGeometry)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#GeoGeometry): Obstacles to consider when planning the motion of the component, with each represented as a `GeoGeometry`. <ul><li> Default: `nil` </li></ul>
  - `motionConfig` [(\*MotionConfiguration)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MotionConfiguration): The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.
    - `ObstacleDetectors` [([]ObstacleDetectorName)](https://pkg.go.dev/go.viam.com/rdk/services/motion#ObstacleDetectorName): The names of each [vision service](/services/vision/) and [camera](/components/camera/) resource pair you want to use for transient obstacle avoidance.
    - `PositionPollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the position of the machine.
    - `ObstaclePollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the vision service for new obstacles.
    - `PlanDeviationM` [(float64)](https://pkg.go.dev/builtin#float64): The distance in meters that the machine can deviate from the motion plan.
    - `LinearMPerSec` [(float64)](https://pkg.go.dev/builtin#float64): Linear velocity this machine should target when moving.
    - `AngularDegsPerSec` [(float64)](https://pkg.go.dev/builtin#float64): Angular velocity this machine should target when turning.

**Returns:**

- [(ExecutionID)](https://pkg.go.dev/go.viam.com/rdk/services/motion#ExecutionID): ExecutionID of the `MoveOnGlobe` call.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Assumes a base with the name "myBase" is configured on the machine
// Get the resource names of the base and movement sensor
myBaseResourceName := base.Named("myBase")
myMvmntSensorResourceName := movementsensor.Named("my_movement_sensor")

// Define a destination Point at the GPS coordinates [0, 0]
myDestination := geo.NewPoint(0, 0)

// Move the base component to the designated geographic location, as reported by the movement sensor
executionID, err := motionService.MoveOnGlobe(context.Background(), motion.MoveOnGlobeReq{
  ComponentName:      myBaseResourceName,
  Destination:        myDestination,
  MovementSensorName: myMvmntSensorResourceName,
})

// Assumes there is an active MoveOnMap() or MoveonGlobe() in progress for myBase
//  MoveOnGlobe is a non-blocking method and this line can optionally be added to block until the movement is done
err = motion.PollHistoryUntilSuccessOrError(
  context.Background(),
  motionService,
  time.Duration(time.Second),
  motion.PlanHistoryReq{
    ComponentName: myBaseResourceName,
    ExecutionID:   executionID,
  },
)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{< /tabs >}}

### GetPose

`GetPose` gets the location and orientation of a component within the [frame system](../frame-system/).
The return type of this function is a `PoseInFrame` describing the pose of the specified component with respect to the specified destination frame.
You can use the `supplemental_transforms` argument to augment the machine's existing frame system with supplemental frames.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)) (required): The `ResourceName` of the piece of the machine whose pose is returned.
- `destination_frame` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the frame with respect to which the component's pose is reported.
- `supplemental_transforms` ([List[viam.proto.common.Transform]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)) (optional): A list of `Transform` objects.
  A `Transform` represents an additional frame which is added to the machine's frame system.
  It consists of the following fields:

  - `pose_in_observer_frame`: Provides the relationship between the frame being added and another frame.
  - `physical_object`: An optional `Geometry` can be added to the frame being added.
  - `reference_frame`: Specifies the name of the frame which will be added to the frame system.

  When `supplemental_transforms` are provided, a frame system is created within the context of the `GetPose` function.
  This new frame system builds off the machine's frame system and incorporates the `Transform`s provided.
  If the result of adding the `Transform`s results in a disconnected frame system, an error is thrown.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.common.PoseInFrame](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame)): Pose of the given component and the frame in which it was observed.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Note that the example uses the ``Arm`` class, but any component class that inherits from ``ComponentBase`` will work
# (``Base``, ``Gripper``, etc).

# Create a `component_name`:
component_name = Arm.get_resource_name("arm")

from viam.components.gripper import Gripper
from viam.services.motion import MotionClient

# Assume that the connect function is written and will return a valid machine.
robot = await connect()

motion = MotionClient.from_robot(robot=robot, name="builtin")
gripperName = Gripper.get_resource_name("my_gripper")
gripperPoseInWorld = await motion.get_pose(component_name=gripperName,
                                        destination_frame="world")
```

The following code example gets the pose of the tip of a [gripper](/components/gripper/) named `my_gripper` which is attached to the end of an arm, in the "world" `reference_frame`:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.gripper import Gripper
from viam.services.motion import MotionClient

# Assume that the connect function is written and will return a valid machine.
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

# Assume that the connect function is written and will return a valid machine.
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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.get_pose).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the piece of the machine whose pose is returned.
- `destinationFrame` [(string)](https://pkg.go.dev/builtin#string): The name of the frame with respect to which the component's pose is reported.
- `supplementalTransforms` [([]*referenceframe.LinkInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#LinkInFrame): An optional list of `LinkInFrame`s.
  A `LinkInFrame` represents an additional frame which is added to the machine's frame system.
  It consists of:

  - a `PoseInFrame`: Provides the relationship between the frame being added and another frame.
  - `Geometry`: An optional `Geometry` can be added to the frame being added.
    When `supplementalTransforms` are provided, a frame system is created within the context of the `GetPose` function.
    This new frame system builds off the machine's frame system and incorporates the `LinkInFrame`s provided.
    If the result of adding the `LinkInFrame`s results in a disconnected frame system, an error is thrown.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(*referenceframe.PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): The pose of the component.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Insert code to connect to your machine.
// (see CONNECT tab of your machine's page in the Viam app)

// Assumes a gripper configured with name "my_gripper" on the machine
gripperName := gripper.Named("my_gripper")

// Access the motion service
motionService, err := motion.FromRobot(machine, "builtin")
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

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{< /tabs >}}

### StopPlan

Stop a [base](/components/base/) component being moved by an in progress [`MoveOnGlobe`](/services/motion/#moveonglobe) or [`MoveOnMap`](/services/motion/#moveonmap) call.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.ResourceName)) (required): The `ResourceName` of the piece of the robot that should arrive at the destination. Note that `move` moves the distal end of the component to the destination. For example, when moving a robotic arm, the piece that will arrive at the destination is the end effector attachment point, not the base of the arm.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Assuming a `move_on_globe()` started the execution
# Stop the base component which was instructed to move by `move_on_globe()`
# or `move_on_map()`
my_base_resource_name = Base.get_resource_name("my_base")
await motion.stop_plan(component_name=mvmnt_sensor)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.stop_plan).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [(StopPlanReq)](https://pkg.go.dev/go.viam.com/rdk/services/motion#StopPlanReq): A `StopPlanReq` which contains the following values:
  - `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to stop.
  - `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(machine, "builtin")
myBaseResourceName := base.Named("myBase")

myMvmntSensorResourceName := movement_sensor.Named("my_movement_sensor")
myDestination := geo.NewPoint(0, 0)

// Assuming a `MoveOnGlobe()`` started the execution
// Stop the base component which was instructed to move by `MoveOnGlobe()` or `MoveOnMap()`
err := motionService.StopPlan(context.Background(), motion.StopPlanReq{
    ComponentName: s.req.ComponentName,
})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{< /tabs >}}

### ListPlanStatuses

Returns the statuses of plans created by [`MoveOnGlobe`](/services/motion/#moveonglobe) or [`MoveOnMap`](/services/motion/#moveonmap) calls that meet at least one of the following conditions since the motion service initialized:

- the plan's status is in progress
- the plan's status changed state within the last 24 hours

All repeated fields are in chronological order.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `only_active_plans` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): If supplied, the response will filter out any plans that are not executing.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.service.motion.ListPlanStatusesResponse](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.ListPlanStatusesResponse)): List of last known statuses with the associated IDs of all plans within the TTL ordered by timestamp in ascending order.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")
# List the plan statuses of the motion service within the TTL
resp = await motion.list_plan_statuses()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.list_plan_statuses).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [(ListPlanStatusesReq)](https://pkg.go.dev/go.viam.com/rdk/services/motion#ListPlanStatusesReq): A `ListPlanStatusesReq` which contains the following values:
  - `onlyActivePlans` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the response will only return plans which are executing.
  - `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]PlanStatusWithID)](https://pkg.go.dev/go.viam.com/rdk/services/motion#PlanStatusWithID): The state of a given plan at a point in time plus the `PlanId`, `ComponentName` and `ExecutionID` the status is associated with.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromRobot(machine, "builtin")

// Get the plan(s) of the base component's most recent execution i.e. `MoveOnGlobe()` or `MoveOnMap()` call.
planStatuses, err := motionService.ListPlanStatuses(context.Background(), motion.ListPlanStatusesReq{})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{< /tabs >}}

### GetPlan

By default, returns the plan history of the most recent [`MoveOnGlobe`](/services/motion/#moveonglobe) or [`MoveOnMap`](/services/motion/#moveonmap) call to move a [base](/components/base/) component.

The plan history for executions before the most recent can be requested by providing an `ExecutionID` in the request.

Returns a result if both of the following conditions are met:

- the execution (call to `MoveOnGlobe` or `MoveOnMap`) is still executing **or** changed state within the last 24 hours
- the machine has not reinitialized

Plans never change.

Replans always create new plans.

Replans share the `ExecutionID` of the previously executing plan.

All repeated fields are in chronological order.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.ResourceName)) (required): The component to stop.
- `last_plan_only` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): If supplied, the response will only return the last plan for the component / execution.
- `execution_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): If supplied, the response will only return plans with the provided execution_id.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.service.motion.GetPlanResponse](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.GetPlanResponse)): The current PlanWithStatus & replan history which matches the request.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=robot, name="builtin")
my_base_resource_name = Base.get_resource_name("my_base")
# Get the plan(s) of the base component which was instructed to move by `MoveOnGlobe()` or `MoveOnMap()`
resp = await motion.get_plan(component_name=my_base_resource_name)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.get_plan).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [(PlanHistoryReq)](https://pkg.go.dev/go.viam.com/rdk/services/motion#PlanHistoryReq): A `PlanHistoryReq` which contains the following values:
  - `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to stop.
  - `lastPlanOnly` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the response will only return the the last plan for the component / execution
  - `executionID` [(ExecutionID)](https://pkg.go.dev/go.viam.com/rdk/services/motion#PlanHistoryReq): If non empty, the response will return the plans of the provided execution & component. Useful for retrieving plans from executions before the current execution.
  - `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]PlanWithStatus)](https://pkg.go.dev/go.viam.com/rdk/services/motion#PlanWithStatus): PlanWithStatus contains a plan, its current status, and all state changes that came prior sorted by ascending timestamp.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the resource name of the base component
myBaseResourceName := base.Named("myBase")

// Get the plan history of the base component's most recent execution (e.g., MoveOnGlobe or MoveOnMap call)
planHistory, err := motionService.PlanHistory(context.Background(), motion.PlanHistoryReq{
  ComponentName: myBaseResourceName,
})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

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

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own motion service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Access the motion service
motion = MotionClient.from_robot(robot=robot, name="builtin")

my_command = {
  "command": "dosomething",
  "someparameter": 52
}

await motion.do_command(my_command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.do_command).

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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.close).

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
