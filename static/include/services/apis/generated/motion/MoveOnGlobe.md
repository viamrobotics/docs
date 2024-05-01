### MoveOnGlobe

{{< tabs >}}
{{% tab name="Python" %}}

Move a component to a specific latitude and longitude, using a MovementSensor to check the location.

**Parameters:**

- `component_name` [(viam.proto.common.ResourceName)](https://python.viam.dev/autoapi/viam/../gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName) (required): The ResourceName of the base to move.
- `destination` [(viam.proto.common.GeoPoint)](https://python.viam.dev/autoapi/viam/../components/movement_sensor/index.html#viam.components.movement_sensor.GeoPoint) (required): The location of the component’s destination, represented in geographic notation as a GeoPoint (lat, lng).
- `movement_sensor_name` [(viam.proto.common.ResourceName)](https://python.viam.dev/autoapi/viam/../gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName) (required): The ResourceName of the movement sensor that you want to use to check the machine’s location.
- `obstacles` [(Sequence[viam.proto.common.GeoObstacle])](https://python.viam.dev/autoapi/viam/../gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.GeoObstacle) (optional): Obstacles to consider when planning the motion of the component, with each represented as a GeoObstacle. Default: None
- `heading` [(float)](<INSERT PARAM TYPE LINK>) (optional): The compass heading, in degrees, that the machine’s movement sensor should report at the destination point. Range: [0-360) 0: North, 90: East, 180: South, 270: West. Default: None
- `configuration` [(viam.proto.service.motion.MotionConfiguration)](https://python.viam.dev/autoapi/viam/../gen/service/motion/v1/motion_pb2/index.html#viam.gen.service.motion.v1.motion_pb2.MotionConfiguration) (optional): The configuration you want to set across this machine for this motion service. This parameter and each of its fields are optional. - obstacle_detectors (Iterable[ObstacleDetector]): The names of each vision service and camera resource pair  you want to use for transient obstacle avoidance.   position_polling_frequency_hz (float): The frequency in hz to poll the position of the machine. obstacle_polling_frequency_hz (float): The frequency in hz to poll the vision service for new obstacles. plan_deviation_m (float): The distance in meters that the machine can deviate from the motion plan. linear_m_per_sec (float): Linear velocity this machine should target when moving. angular_degs_per_sec (float): Angular velocity this machine should target when turning.  
- `extra` [(Mapping[str, Any])](<INSERT PARAM TYPE LINK>) (optional): Extra options to pass to the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.


**Returns:**

- [(str)](INSERT RETURN TYPE LINK): ExecutionID of the move_on_globe() call, which can be used to track execution progress.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move_on_globe).

``` python {class="line-numbers linkable-line-numbers"}
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

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx`[(Context)](https://pkg.go.dev/context#ctx):
- `req`[(MoveOnGlobeReq)](<INSERT PARAM TYPE LINK>)
- [())](<INSERT PARAM TYPE LINK>)

**Returns:**

- [(ExecutionID)](<INSERT PARAM TYPE LINK>)
- [(error)](<INSERT PARAM TYPE LINK>)

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/motion#Service).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `componentName` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)> (required):
- `destination` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)> (required):
- `extra` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)> (required):
- `heading` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)> (required):
- `motionConfiguration` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)> (required):
- `movementSensorName` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)> (required):
- `name` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)> (required):
- `obstacles` [(List)](https://api.flutter.dev/flutter/dart-core/List-class.html)<[GeoObstacle](https://flutter.viam.dev/viam_protos.common.common/GeoObstacle-class.html)> (required):


For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_protos.service.motion/MotionServiceClient/moveOnGlobe.html).

{{% /tab %}}
{{< /tabs >}}
