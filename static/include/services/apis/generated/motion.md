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

- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The `ResourceName` of the piece of the robot that should arrive at the destination. Note that `move` moves the distal end of the component to the destination. For example, when moving a robotic arm, the piece that will arrive at the destination is the end effector attachment point, not the base of the arm.
- `destination` ([viam.proto.common.PoseInFrame](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame)) (required): Describes where the `component_name` frame should be moved to. Can be any pose, from the perspective of any component whose location is configured as a [`frame`](/operate/reference/services/frame-system/).
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
- `constraints` ([viam.proto.service.motion.Constraints](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.Constraints)) (optional): Pass in [motion constraints](/operate/reference/services/motion/constraints/). By default, motion is unconstrained with the exception of obstacle avoidance.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)): Whether the move was successful (`true`) or unsuccessful (`false`).

**Example:**

```python {class="line-numbers linkable-line-numbers"}
success = await MotionServiceClient.move("externalFrame", ...)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [(MoveReq)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MoveReq)

**Returns:**

- [(bool)](https://pkg.go.dev/builtin#bool): Whether the move was successful (`true`) or unsuccessful (`false`).
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
motionService, err := motion.FromProvider(machine, "builtin")

// Assumes a gripper configured with name "my_gripper" on the machine
gripperName := "my_gripper"

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

moved, err := motionService.Move(context.Background(), motion.MoveReq{
  ComponentName: gripperName,
  Destination: destination,
  WorldState: worldState
})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `destination` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (required): Destination to move to, which can a pose in the
  reference frame of any frame in the robot's frame system.
- `componentName` (string) (required): Component on the robot to move to the specified
  destination.
- `worldState` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (optional): Avoid obstacles by specifying their geometries in the
  world state. Augment the frame system of the robot by specifying
  additional transforms to add to it for the duration of the Move.
- `constraints` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (optional): Constrain the way the robot will move.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<boolean>): Whether the move was successful (`true`) or unsuccessful (`false`).

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const motion = new VIAM.MotionClient(machine, 'builtin');

// Assumes a gripper configured with name "my_gripper"
cconst gripperName = "my_gripper";

const goalPose: VIAM.Pose = {
  x: -817,
  y: -230,
  z: 62,
  oX: -1,
  oY: 0,
  oZ: 0,
  theta: 90,
};
const goalPoseInFrame = new VIAM.PoseInFrame({
  referenceFrame: 'world',
  pose: goalPose,
});

// Move the gripper
const moved = await motion.move(goalPoseInFrame, gripperName);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MotionClient.html#move).

{{% /tab %}}
{{< /tabs >}}

### MoveOnMap

Move a [base](/operate/reference/components/base/) component to a destination [pose](/operate/mobility/orientation-vector/) on a {{< glossary_tooltip term_id="slam" text="SLAM" >}} map.

`MoveOnMap()` is non blocking, meaning the motion service will move the component to the destination [pose](/operate/mobility/orientation-vector/) after `MoveOnMap()` returns.

Each successful `MoveOnMap()` call returns a unique `ExecutionID` which you can use to identify all plans generated during the `MoveOnMap()` call.

{{< alert title="Info" color="info" >}}
If you specify a goal pose and the robot's current position is already within the set `PlanDeviationM`, then `MoveOnMap` returns an error.
{{< /alert >}}

You can monitor the progress of the `MoveOnMap()` call by querying `GetPlan()` and `ListPlanStatuses()`.

Use the machine's position reported by the {{< glossary_tooltip term_id="slam" text="SLAM" >}} service to check the location of the machine.

`MoveOnMap()` is intended for use with the [navigation service](/operate/reference/services/navigation/), providing autonomous indoor navigation for rover [bases](/operate/reference/components/base/).

{{< alert title="Requirements" color="info" >}}
To use `MoveOnMap()`, your [SLAM service](/operate/reference/services/slam/) must implement `GetPointCloudMap()` and `GetPosition()`

Make sure the [SLAM service](/operate/reference/services/slam/) you use alongside this motion service supports the following methods in its {{< glossary_tooltip term_id="model" text="model's" >}} implementation of the [SLAM service API](/dev/reference/apis/services/slam/):

- It must support `GetPointCloudMap()` to report the SLAM map as a pointcloud.
- It must support `GetPosition()` to report the machine's current location on the SLAM map.
  {{< /alert >}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The `ResourceName` of the base to move.
- `destination` ([viam.proto.common.Pose](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Pose)) (required): The destination, which can be any [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) with respect to the SLAM map's origin.
- `slam_service_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The `ResourceName` of the [SLAM service](/operate/reference/services/slam/) from which the SLAM map is requested.
- `configuration` ([viam.proto.service.motion.MotionConfiguration](https://python.viam.dev/autoapi/viam/gen/service/motion/v1/motion_pb2/index.html#viam.gen.service.motion.v1.motion_pb2.MotionConfiguration)) (optional): 
The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.

- `obstacle_detectors` [(Iterable[ObstacleDetector])](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.ObstacleDetector): The names of each [vision service](/operate/reference/services/vision/) and [camera](/operate/reference/components/camera/) resource pair you want to use for transient obstacle avoidance.
- `position_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the position of the machine.
- `obstacle_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the vision service for new obstacles.
- `plan_deviation_m` [(float)](https://docs.python.org/3/library/functions.html#float): The distance in meters that the machine can deviate from the motion plan. By default this is set to 2.6 m which is an appropriate value for outdoor usage. When you use the `MoveOnMap()` method from the **CONTROL** tab, the default is overwritten to 0.5 m for testing.
- `linear_m_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Linear velocity this machine should target when moving.
- `angular_degs_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Angular velocity this machine should target when turning.
- `obstacles` ([Sequence[viam.proto.common.Geometry]](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.Geometry)) (optional): Obstacles, specified in the SLAM frame coordinate system, to be considered when planning the motion of the component.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ExecutionID of the `MoveOnMap` call.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=machine, name="builtin")

# Get the names of the base component and SLAM service
my_base_name = "my_base"
my_slam_service_name = "my_slam_service"

# Define a destination pose with respect to the origin of the map from the SLAM service "my_slam_service"
my_pose = Pose(y=10)

# Move the base component to the destination pose of Y=10, a location of
# (0, 10, 0) in respect to the origin of the map
execution_id = await motion.move_on_map(component_name=my_base_name,
                                        destination=my_pose,
                                        slam_service_name=my_slam_service_name)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move_on_map).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [(MoveOnMapReq)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MoveOnMapReq): 
A `MoveOnMapReq` which contains the following values:

- `ComponentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to move.
- `Destination` [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): The destination, which can be any [Pose](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Pose) with respect to the SLAM map's origin.
- `SlamName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the [SLAM service](/operate/reference/services/slam/) from which the SLAM map is requested.
- `MotionConfig` [(\*MotionConfiguration)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MotionConfiguration): The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.
  - `ObstacleDetectors` [([]ObstacleDetectorName)](https://pkg.go.dev/go.viam.com/rdk/services/motion#ObstacleDetectorName): The names of each [vision service](/operate/reference/services/vision/) and [camera](/operate/reference/components/camera/) resource pair you want to use for transient obstacle avoidance.
  - `PositionPollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the position of the machine.
  - `ObstaclePollingFreqHz` [(float64)](https://pkg.go.dev/builtin#float64): The frequency in hz to poll the vision service for new obstacles.
  - `PlanDeviationM` [(float64)](https://pkg.go.dev/builtin#float64): The distance in meters that the machine can deviate from the motion plan. By default this is set to 2.6 m which is an appropriate value for outdoor usage. When you use the **CONTROL** tab, the underlying calls to `MoveOnMap()` use 0.5 m instead.
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
{{% tab name="TypeScript" %}}

**Parameters:**

- `destination` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (required): Specify a destination to, which can be any `Pose` with
  respect to the SLAM map's origin.
- `componentName` (string) (required): Component on the robot to move to the specified
  destination.
- `slamServiceName` (string) (required): Name of the `SLAM` service from which the SLAM map
  is requested.
- `motionConfig` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (optional)
- `obstacles` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (optional): Optional obstacles to be considered for motion planning.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<string>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const motion = new VIAM.MotionClient(machine, 'builtin');

// Define destination pose with respect to map origin
const myPose: VIAM.Pose = {
  x: 0,
  y: 10,
  z: 0,
  oX: 0,
  oY: 0,
  oZ: 0,
  theta: 0,
};

const baseName = 'my_base';
const slamServiceName = 'my_slam_service';

// Move the base to Y=10 (location of 0,10,0) relative to map origin
const executionId = await motion.moveOnMap(
  myPose,
  baseName,
  slamServiceName
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MotionClient.html#moveonmap).

{{% /tab %}}
{{< /tabs >}}

### MoveOnGlobe

Move a [base](/operate/reference/components/base/) component to a destination GPS point, represented in geographic notation _(latitude, longitude)_.
Use a [movement sensor](/operate/reference/components/movement-sensor/) to check the location of the machine.

`MoveOnGlobe()` is non blocking, meaning the motion service will move the component to the destination GPS point after `MoveOnGlobe()` returns.

Each successful `MoveOnGlobe()` call returns a unique `ExecutionID` which you can use to identify all plans generated during the `MoveOnGlobe()`.

{{< alert title="Info" color="info" >}}
If you specify a goal pose and the robot's current position is already within the set `PlanDeviationM`, `MoveOnGlobe` returns an error.
{{< /alert >}}

You can monitor the progress of the `MoveOnGlobe()` call by querying `GetPlan()` and `ListPlanStatuses()`.

`MoveOnGlobe()` is intended for use with the [navigation service](/operate/reference/services/navigation/), providing autonomous GPS navigation for rover [bases](/operate/reference/components/base/).

{{< alert title="Requirements" color="info" >}}
To use `MoveOnGlobe()`, your movement sensor must be able to measure the GPS location and orientation of the machine.

Make sure the [movement sensor](/operate/reference/components/movement-sensor/) you use supports usage of the following methods in its {{< glossary_tooltip term_id="model" text="model's" >}} implementation of the [movement sensor API](/dev/reference/apis/components/movement-sensor/).

- It must support `GetPosition()` to report the machine's current GPS location.
- It must **also** support **either** `GetCompassHeading()` or `GetOrientation()` to report which way the machine is facing.
- If your movement sensor provides multiple methods, your machine will default to using the values returned by `GetCompassHeading()`.
  {{< /alert >}}

{{< alert title="Stability Notice" color="alert" >}}

The `heading` parameter is experimental.
Specifying `heading` in a request to `MoveOnGlobe` is not currently recommended if the minimum turning radius of your component is greater than zero, as this combination may cause high latency in the [motion planning algorithms](/operate/reference/services/motion/algorithms/).

Specifying `obstacles` in a request to `MoveOnGlobe()` will cause an error if you configure a `"translation"` in the `"geometries"` of any of the `GeoGeometry` objects.
Translation in obstacles is not supported by the [navigation service](/operate/reference/services/navigation/).

{{< /alert >}}

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The `ResourceName` of the base to move.
- `destination` ([viam.proto.common.GeoPoint](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.GeoPoint)) (required): The location of the component's destination, represented in geographic notation as a [GeoPoint](https://python.viam.dev/autoapi/viam/components/movement_sensor/index.html#viam.components.movement_sensor.GeoPoint) _(lat, lng)_.
- `movement_sensor_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The `ResourceName` of the [movement sensor](/operate/reference/components/movement-sensor/) that you want to use to check the machine's location.
- `obstacles` ([Sequence[viam.proto.common.GeoGeometry]](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.GeoGeometry)) (optional): Obstacles to consider when planning the motion of the component, with each represented as a `GeoGeometry`. <ul><li> Default: `None` </li></ul>
- `heading` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): The compass heading, in degrees, that the machine's movement sensor should report at the `destination` point. <ul><li> Range: `[0-360)` `0`: North, `90`: East, `180`: South, `270`: West </li><li>Default: `None`</li></ul>
- `configuration` ([viam.proto.service.motion.MotionConfiguration](https://python.viam.dev/autoapi/viam/gen/service/motion/v1/motion_pb2/index.html#viam.gen.service.motion.v1.motion_pb2.MotionConfiguration)) (optional): 
The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.

- `obstacle_detectors` [(Iterable[ObstacleDetector])](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.ObstacleDetector): The names of each [vision service](/operate/reference/services/vision/) and [camera](/operate/reference/components/camera/) resource pair you want to use for transient obstacle avoidance.
- `position_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the position of the machine.
- `obstacle_polling_frequency_hz` [(float)](https://docs.python.org/3/library/functions.html#float): The frequency in hz to poll the vision service for new obstacles.
- `plan_deviation_m` [(float)](https://docs.python.org/3/library/functions.html#float): The distance in meters that the machine can deviate from the motion plan.
- `linear_m_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Linear velocity this machine should target when moving.
- `angular_degs_per_sec` [(float)](https://docs.python.org/3/library/functions.html#float): Angular velocity this machine should target when turning.
- `bounding_regions` ([Sequence[viam.proto.common.GeoGeometry]](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.GeoGeometry)) (optional): Set of obstacles which the robot must remain within while navigating.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)): ExecutionID of the `MoveOnGlobe` call.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=machine, name="builtin")

# Get the names of the base and movement sensor
my_base_name = "my_base"
mvmnt_sensor_name = "my_movement_sensor"
#  Define a destination GeoPoint at the GPS coordinates [0, 0]
my_destination = movement_sensor.GeoPoint(latitude=0, longitude=0)

# Move the base component to the designated geographic location, as reported by the movement sensor
execution_id = await motion.move_on_globe(
    component_name=my_base_name,
    destination=my_destination,
    movement_sensor_name=mvmnt_sensor_name)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move_on_globe).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [(MoveOnGlobeReq)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MoveOnGlobeReq): 
A `MoveOnGlobeReq` which contains the following values:

- `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to move.
- `destination` [(\*geo.Point)](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point): The location of the component's destination, represented in geographic notation as a [Point](https://pkg.go.dev/github.com/kellydunn/golang-geo#Point) _(lat, lng)_.
- `heading` [(float64)](https://pkg.go.dev/builtin#float64): The compass heading, in degrees, that the machine's movement sensor should report at the `destination` point. <ul><li> Range: `[0-360)` 0: North, 90: East, 180: South, 270: West</li><li>Default: `0`</li></ul>
- `movementSensorName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the [movement sensor](/operate/reference/components/movement-sensor/) that you want to use to check the machine's location.
- `obstacles` [([]\*spatialmath.GeoGeometry)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#GeoGeometry): Obstacles to consider when planning the motion of the component, with each represented as a `GeoGeometry`. <ul><li> Default: `nil` </li></ul>
- `motionConfig` [(\*MotionConfiguration)](https://pkg.go.dev/go.viam.com/rdk/services/motion#MotionConfiguration): The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional.
  - `ObstacleDetectors` [([]ObstacleDetectorName)](https://pkg.go.dev/go.viam.com/rdk/services/motion#ObstacleDetectorName): The names of each [vision service](/operate/reference/services/vision/) and [camera](/operate/reference/components/camera/) resource pair you want to use for transient obstacle avoidance.
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
{{% tab name="TypeScript" %}}

**Parameters:**

- `destination` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (required): Destination for the component to move to, represented
  as a `GeoPoint`.
- `componentName` (string) (required): The name of the component to move.
- `movementSensorName` (string) (required): The name of the `Movement Sensor` used to check
  the robot's location.
- `heading` (number) (optional): Compass heading, in degrees, to achieve at destination.
- `obstaclesList` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (optional): Obstacles to consider when planning the motion of
  the component.
- `motionConfig` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (optional)
- `boundingRegionsList` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (optional)
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<string>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const motion = new VIAM.MotionClient(machine, 'builtin');

// Define destination at GPS coordinates [0,0]
const destination: VIAM.GeoPoint = {
  latitude: 40.7,
  longitude: -73.98,
};

const baseName = 'my_base';
const movementSensorName = 'my_movement_sensor';

// Move the base to the geographic location
const globeExecutionId = await motion.moveOnGlobe(
  destination,
  baseName,
  movementSensorName
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MotionClient.html#moveonglobe).

{{% /tab %}}
{{< /tabs >}}

### GetPose

`GetPose` gets the location and orientation of a component within the [frame system](/operate/reference/services/frame-system/).
The return type of this function is a `PoseInFrame` describing the pose of the specified component with respect to the specified destination frame.
You can use the `supplemental_transforms` argument to augment the machine's existing frame system with supplemental frames.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The `ResourceName` of the piece of the machine whose pose is returned.
- `destination_frame` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the frame with respect to which the component's pose is reported.
- `supplemental_transforms` ([Sequence[viam.proto.common.Transform]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)) (optional): A list of `Transform` objects.
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
# Note that the example uses the ``Gripper`` class, but any component class that inherits from ``ComponentBase`` will work
# (``Arm``, ``Base``, etc).

from viam.components.gripper import Gripper
from viam.services.motion import MotionClient

# Assume that the connect function is written and will return a valid machine.
machine = await connect()

motion = MotionClient.from_robot(robot=machine, name="builtin")
gripperPoseInWorld = await motion.get_pose(component_name="my_gripper",
                                           destination_frame="world")
```

The following code example gets the pose of the tip of a [gripper](/operate/reference/components/gripper/) named `my_gripper` which is attached to the end of an arm, in the "world" `reference_frame`:

```python {class="line-numbers linkable-line-numbers"}
from viam.components.gripper import Gripper
from viam.services.motion import MotionClient

# Assume that the connect function is written and will return a valid machine.
robot = await connect()

motion = MotionClient.from_robot(robot=robot, name="builtin")
gripperPoseInWorld = await motion.get_pose(component_name="my_gripper",
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
gripperPoseInObjectFrame = await motion.get_pose(
  component_name="my_gripper",
  destination_frame="world",
  supplemental_transforms=objectTransform
)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.get_pose).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `componentName` [(string)](https://pkg.go.dev/builtin#string): The `resource.Name` of the piece of the machine whose pose is returned.
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

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `componentName` (string) (required): The component whose `Pose` is being requested.
- `destinationFrame` (string) (required): The reference frame in which the component's
  `Pose` should be provided, if unset this defaults to the "world"
  reference frame.
- `supplementalTransforms` ([PlainMessage](https://ts.viam.dev/types/PlainMessage.html)) (required): `Pose` information on any additional
  reference frames that are needed to compute the component's `Pose`.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[commonApi](https://ts.viam.dev/modules/commonApi.html).[PoseInFrame](https://ts.viam.dev/classes/commonApi.PoseInFrame.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const motion = new VIAM.MotionClient(machine, 'builtin');

const gripperName = 'my_gripper';

// Get the gripper's pose in world coordinates
const gripperPoseInWorld = await motion.getPose(
  gripperName,
  'world',
  []
);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MotionClient.html#getpose).

{{% /tab %}}
{{< /tabs >}}

### StopPlan

Stop a [base](/operate/reference/components/base/) component being moved by an in progress [`MoveOnGlobe`](/dev/reference/apis/services/motion/#moveonglobe) or [`MoveOnMap`](/dev/reference/apis/services/motion/#moveonmap) call.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The `ResourceName` of the piece of the robot that should arrive at the destination. Note that `move` moves the distal end of the component to the destination. For example, when moving a robotic arm, the piece that will arrive at the destination is the end effector attachment point, not the base of the arm.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=machine, name="builtin")

# Assuming a `move_on_globe()` started the execution
# Stop the base component which was instructed to move by `move_on_globe()`
# or `move_on_map()`
my_base_name = "my_base"
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
motionService, err := motion.FromProvider(machine, "builtin")
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
{{% tab name="TypeScript" %}}

**Parameters:**

- `componentName` (string) (required): The component to stop.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<null>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const motion = new VIAM.MotionClient(machine, 'builtin');
const baseName = 'my_base';

// Stop the base component which was instructed to move
await motion.stopPlan(baseName);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MotionClient.html#stopplan).

{{% /tab %}}
{{< /tabs >}}

### ListPlanStatuses

Returns the statuses of plans created by [`MoveOnGlobe`](/dev/reference/apis/services/motion/#moveonglobe) or [`MoveOnMap`](/dev/reference/apis/services/motion/#moveonmap) calls that meet at least one of the following conditions since the motion service initialized:

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

- ([Sequence[viam.proto.service.motion.PlanStatusWithID]](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.PlanStatusWithID)): List of last known statuses with the
associated IDs of all plans within the TTL ordered by timestamp in ascending order.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=machine, name="builtin")
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
motionService, err := motion.FromProvider(machine, "builtin")

// Get the plan(s) of the base component's most recent execution i.e. `MoveOnGlobe()` or `MoveOnMap()` call.
planStatuses, err := motionService.ListPlanStatuses(context.Background(), motion.ListPlanStatusesReq{})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `onlyActivePlans` (boolean) (optional): If true, the response will only return plans which
  are executing.
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[motionApi](https://ts.viam.dev/modules/motionApi.html).[ListPlanStatusesResponse](https://ts.viam.dev/classes/motionApi.ListPlanStatusesResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const motion = new VIAM.MotionClient(machine, 'builtin');

// List plan statuses within the TTL
const response = await motion.listPlanStatuses();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MotionClient.html#listplanstatuses).

{{% /tab %}}
{{< /tabs >}}

### GetPlan

By default, returns the plan history of the most recent [`MoveOnGlobe`](/dev/reference/apis/services/motion/#moveonglobe) or [`MoveOnMap`](/dev/reference/apis/services/motion/#moveonmap) call to move a [base](/operate/reference/components/base/) component.

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

- `component_name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The component to stop.
- `last_plan_only` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): If supplied, the response will only return the last plan for the component / execution.
- `execution_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): If supplied, the response will only return plans with the provided execution_id.
- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (optional): Extra options to pass to the underlying RPC call.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.proto.service.motion.GetPlanResponse](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.GetPlanResponse)): The current PlanWithStatus \& replan history which matches the request.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
motion = MotionClient.from_robot(robot=machine, name="builtin")
my_base_name = "my_base"
# Get the plan(s) of the base component which was instructed to move by `MoveOnGlobe()` or `MoveOnMap()`
resp = await motion.get_plan(component_name=my_base_name)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.get_plan).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [(PlanHistoryReq)](https://pkg.go.dev/go.viam.com/rdk/services/motion#PlanHistoryReq): A `PlanHistoryReq` which contains the following values:
  - `componentName` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): The `resource.Name` of the base to stop.
  - `lastPlanOnly` [(bool)](https://pkg.go.dev/builtin#bool): If `true`, the response will only return the last plan for the component / execution
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
{{% tab name="TypeScript" %}}

**Parameters:**

- `componentName` (string) (required): The component to query.
- `lastPlanOnly` (boolean) (optional)
- `executionId` (string) (optional)
- `extra` (None) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[motionApi](https://ts.viam.dev/modules/motionApi.html).[GetPlanResponse](https://ts.viam.dev/classes/motionApi.GetPlanResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const motion = new VIAM.MotionClient(machine, 'builtin');
const baseName = 'my_base';

// Get the plan(s) of the base component
const response = await motion.getPlan(baseName);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MotionClient.html#getplan).

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

### FromRobot

Get the resource from the provided machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `robot` ([viam.robot.client.RobotClient](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient)) (required): The robot.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the service.

**Returns:**

- ([typing_extensions.Self](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient)): The service, if it exists on the robot.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
async def connect() -> RobotClient:
    # Replace "<API-KEY>" (including brackets) with your API key and "<API-KEY-ID>" with your API key ID
    options = RobotClient.Options.with_api_key("<API-KEY>", "<API-KEY-ID>")
    # Replace "<MACHINE-URL>" (included brackets) with your machine's connection URL or FQDN
    return await RobotClient.at_address("<MACHINE-URL>", options)

async def main():
    robot = await connect()

    # Can be used with any resource, using the motion service as an example
    motion = MotionClient.from_robot(robot=machine, name="builtin")

    robot.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.from_robot).

{{% /tab %}}
{{< /tabs >}}

### DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own motion service and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motion_svc = MotionClient.from_robot(robot=machine, "builtin")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

await my_motion_svc.do_command(command=my_command)
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
myMotionSvc, err := motion.FromProvider(machine, "my_motion_svc")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := myMotionSvc.DoCommand(context.Background(), command)
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

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MotionClient.html#docommand).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this instance of the motion service.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_motion_svc_name = MotionClient.get_resource_name("my_motion_svc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
myMotionSvc, err := motion.FromProvider(machine, "my_motion_svc")

err = myMotionSvc.Name()
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
motion.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/MotionClient.html#name).

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
my_motion_svc = MotionClient.from_robot(robot=machine, name="my_motion_svc")
await my_motion_svc.close()
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
myMotionSvc, err := motion.FromProvider(machine, "my_motion_svc")

err = myMotionSvc.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
