### MoveOnMap

{{< tabs >}}
{{% tab name="Python" %}}

Move a component to a specific pose, using a SlamService for the SLAM map, using a SLAM Service to check the location.

**Parameters:**

- `component_name` [(viam.proto.common.ResourceName)](https://python.viam.dev/autoapi/viam/../gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName) (required): The ResourceName of the base to move.
- `destination` [(viam.proto.common.Pose)](https://python.viam.dev/autoapi/viam/../components/arm/index.html#viam.components.arm.Pose) (required): The destination, which can be any Pose with respect to the SLAM map’s origin.
- `slam_service_name` [(viam.proto.common.ResourceName)](https://python.viam.dev/autoapi/viam/../gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName) (required): The ResourceName of the SLAM service from which the SLAM map is requested.
- `configuration` [(viam.proto.service.motion.MotionConfiguration)](https://python.viam.dev/autoapi/viam/../gen/service/motion/v1/motion_pb2/index.html#viam.gen.service.motion.v1.motion_pb2.MotionConfiguration) (optional): The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional. - obstacle_detectors (Iterable[ObstacleDetector]): The names of each vision service and camera resource pair you want to use  for transient obstacle avoidance.   position_polling_frequency_hz (float): The frequency in hz to poll the position of the machine. obstacle_polling_frequency_hz (float): The frequency in hz to poll the vision service for new obstacles. plan_deviation_m (float): The distance in meters that the machine can deviate from the motion plan. linear_m_per_sec (float): Linear velocity this machine should target when moving. angular_degs_per_sec (float): Angular velocity this machine should target when turning.  
- `obstacles` [(Iterable[viam.proto.common.Geometry])](https://python.viam.dev/autoapi/viam/../gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.Geometry) (optional): Obstacles to be considered for motion planning.
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): ExecutionID of the move_on_map() call, which can be used to track execution progress.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move_on_map).

``` python {class="line-numbers linkable-line-numbers"}
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

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context):
- `req` [(MoveOnMapReq)](https://pkg.go.dev#MoveOnMapReq):
- [())](<INSERT PARAM TYPE LINK>):

**Returns:**

- [(ExecutionID)](https://pkg.go.dev#ExecutionID):
- [(error)](https://pkg.go.dev/builtin#error):

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `componentName` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html) (required):
- `destination` [(Pose)](https://flutter.viam.dev/viam_sdk/Pose-class.html) (required):
- `extra` [(Struct)](<INSERT PARAM TYPE LINK>) (required):
- `motionConfiguration` [(MotionConfiguration)](https://flutter.viam.dev/viam_protos.service.motion/MotionConfiguration-class.html) (required):
- `name` [(String)](https://api.flutter.dev/flutter/dart-core/String-class.html) (required):
- `obstacles` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[Geometry](https://flutter.viam.dev/viam_protos.common.common/Geometry-class.html)> (required):
- `slamServiceName` [(ResourceName)](https://flutter.viam.dev/viam_sdk/ResourceName-class.html) (required):

**Returns:**

- None.

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/moveOnMap.html).

{{% /tab %}}
{{< /tabs >}}
