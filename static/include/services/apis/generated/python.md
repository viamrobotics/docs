### DoCommand

Send/receive arbitrary commands.

**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute

**Returns:**

- [(Mapping[str, Any])](INSERT RETURN TYPE LINK): Result of the executed command

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/generic/client/index.html#viam.services.generic.client.GenericClient.do_command).

```python
motion = MotionClient.from_robot(robot, "builtin")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

# Can be used with any resource, using the motion service as an example
await motion.do_command(command=my_command)
```

### Close

Safely shut down the resource and prevent further use.

**Parameters:**


**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/generic/client/index.html#viam.services.generic.client.GenericClient.close).

```python
await component.close()
```

### Infer

Take an already ordered input tensor as an array, make an inference on the model, and return an output tensor map.

**Parameters:**

- `input_tensors` [(float)](<INSERT PARAM TYPE LINK>): Optional. A dictionary of input flat tensors as specified in the metadata
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. A dictionary of input flat tensors as specified in the metadata

**Returns:**

- [(Dict[str, numpy.typing.NDArray])](INSERT RETURN TYPE LINK): A dictionary of output flat tensors as specified in the metadata

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.infer).

```python
import numpy as np

my_mlmodel = MLModelClient.from_robot(robot=robot, name="my_mlmodel_service")

nd_array = np.array([1, 2, 3], dtype=np.float64)
input_tensors = {"0": nd_array}

output_tensors = await my_mlmodel.infer(input_tensors)
```

### Metadata

Get the metadata (such as name, type, expected tensor/array shape, inputs, and outputs) associated with the ML model.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

- [(viam.services.mlmodel.mlmodel.Metadata)](INSERT RETURN TYPE LINK): The metadata

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.metadata).

```python
my_mlmodel = MLModelClient.from_robot(robot=robot, name="my_mlmodel_service")

metadata = await my_mlmodel.metadata()
```

### DoCommand

Send/receive arbitrary commands.

**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute

**Returns:**

- [(Mapping[str, viam.utils.ValueTypes])](INSERT RETURN TYPE LINK): Result of the executed command

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.do_command).

```python
motion = MotionClient.from_robot(robot, "builtin")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

# Can be used with any resource, using the motion service as an example
await motion.do_command(command=my_command)
```

### Close

Safely shut down the resource and prevent further use.

**Parameters:**


**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/mlmodel/client/index.html#viam.services.mlmodel.client.MLModelClient.close).

```python
await component.close()
```

### Move

Plan and execute a movement to move the component specified to its goal destination.

**Parameters:**

- `component_name` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.Constraints): Optional. When supplied, the motion service will create a plan that obeys any
specified constraints
- `destination` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.Constraints): Optional. When supplied, the motion service will create a plan that obeys any
specified constraints
- `world_state` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.Constraints): Optional. When supplied, the motion service will create a plan that obeys any
specified constraints
- `constraints` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.Constraints): Optional. When supplied, the motion service will create a plan that obeys any
specified constraints
- `extra` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.Constraints): Optional. When supplied, the motion service will create a plan that obeys any
specified constraints
- `timeout` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.Constraints): Optional. When supplied, the motion service will create a plan that obeys any
specified constraints

**Returns:**

- [(bool)](INSERT RETURN TYPE LINK): Whether the move was successful

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move).

```python
resource_name = Arm.get_resource_name("externalFrame")
success = await MotionServiceClient.move(resource_name, ...)
```

### MoveOnGlobe

Move a component to a specific latitude and longitude, using a MovementSensor to check the location.

**Parameters:**

- `component_name` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.MotionConfiguration): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing
the underlying RPC call.
- `destination` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.MotionConfiguration): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing
the underlying RPC call.
- `movement_sensor_name` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.MotionConfiguration): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing
the underlying RPC call.
- `obstacles` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.MotionConfiguration): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing
the underlying RPC call.
- `heading` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.MotionConfiguration): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing
the underlying RPC call.
- `configuration` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.MotionConfiguration): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing
the underlying RPC call.
- `extra` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.MotionConfiguration): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing
the underlying RPC call.
- `timeout` [(float)](https://python.viam.dev/autoapi/viam/../proto/service/motion/index.html#viam.proto.service.motion.MotionConfiguration): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing
the underlying RPC call.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): ExecutionID of the move_on_globe() call, which can be used to track execution progress.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move_on_globe).

```python
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

### MoveOnMap

Move a component to a specific pose, using a SlamService for the SLAM map, using a SLAM Service to check the location.

**Parameters:**

- `component_name` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Geometry): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing the underlying
RPC call.
- `destination` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Geometry): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing the underlying
RPC call.
- `slam_service_name` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Geometry): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing the underlying
RPC call.
- `configuration` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Geometry): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing the underlying
RPC call.
- `obstacles` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Geometry): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing the underlying
RPC call.
- `extra` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Geometry): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing the underlying
RPC call.
- `timeout` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Geometry): Optional. An option to set how long to wait (in seconds) before calling a time-out and closing the underlying
RPC call.

**Returns:**

- [(str)](INSERT RETURN TYPE LINK): ExecutionID of the move_on_map() call, which can be used to track execution progress.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.move_on_map).

```python
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

### StopPlan

Stop a component being moved by an in progress move_on_globe() or move_on_map() call.

**Parameters:**

- `component_name` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.ResourceName): Optional. The component to stop
- `extra` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.ResourceName): Optional. The component to stop
- `timeout` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.ResourceName): Optional. The component to stop

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.stop_plan).

```python
# Assuming a `move_on_globe()` started the execution
# Stop the base component which was instructed to move by `move_on_globe()`
# or `move_on_map()`
my_base_resource_name = Base.get_resource_name("my_base")
await motion.stop_plan(component_name=mvmnt_sensor)
```

### GetPlan

By default: returns the plan history of the most recent move_on_globe() or move_on_map() call to move a component.

**Parameters:**

- `component_name` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.ResourceName): Optional. If supplied, the response will only return plans with the provided execution_id
- `last_plan_only` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.ResourceName): Optional. If supplied, the response will only return plans with the provided execution_id
- `execution_id` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.ResourceName): Optional. If supplied, the response will only return plans with the provided execution_id
- `extra` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.ResourceName): Optional. If supplied, the response will only return plans with the provided execution_id
- `timeout` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.ResourceName): Optional. If supplied, the response will only return plans with the provided execution_id

**Returns:**

- [(viam.proto.service.motion.GetPlanResponse)](INSERT RETURN TYPE LINK): The current PlanWithStatus & replan history which matches the request

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.get_plan).

```python
motion = MotionClient.from_robot(robot=robot, name="builtin")
my_base_resource_name = Base.get_resource_name("my_base")
# Get the plan(s) of the base component which was instructed to move by `MoveOnGlobe()` or `MoveOnMap()`
resp = await motion.get_plan(component_name=my_base_resource_name)
```

### ListPlanStatuses

Returns the statuses of plans created by move_on_globe() or move_on_map() calls that meet at least one of the following conditions since the motion service initialized:

**Parameters:**

- `only_active_plans` [(float)](<INSERT PARAM TYPE LINK>): Optional. If supplied, the response will filter out any plans that are not executing
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional. If supplied, the response will filter out any plans that are not executing
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. If supplied, the response will filter out any plans that are not executing

**Returns:**

- [(viam.proto.service.motion.ListPlanStatusesResponse)](INSERT RETURN TYPE LINK): List of last known statuses with the
associated IDs of all plans within the TTL ordered by timestamp in ascending order

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.list_plan_statuses).

```python
motion = MotionClient.from_robot(robot=robot, name="builtin")
# List the plan statuses of the motion service within the TTL
resp = await motion.list_plan_statuses()
```

### GetPose

Get the Pose and observer [frame](/mobility/frame-system/) for any given component on a robot. A component_name can be created like this:

**Parameters:**

- `component_name` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Transform): Optional. Transforms used to augment the robot’s frame while
calculating pose.
- `destination_frame` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Transform): Optional. Transforms used to augment the robot’s frame while
calculating pose.
- `supplemental_transforms` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Transform): Optional. Transforms used to augment the robot’s frame while
calculating pose.
- `extra` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Transform): Optional. Transforms used to augment the robot’s frame while
calculating pose.
- `timeout` [(float)](https://python.viam.dev/autoapi/viam/../proto/common/index.html#viam.proto.common.Transform): Optional. Transforms used to augment the robot’s frame while
calculating pose.

**Returns:**

- [(viam.proto.common.PoseInFrame)](INSERT RETURN TYPE LINK): Pose of the given component and the frame in which it was observed.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.get_pose).

```python
component_name = Arm.get_resource_name("arm")
```

METHOD OVERRIDE AFTER: The following code example gets the pose of the tip of a [gripper](/components/gripper/) named `my_gripper` which is attached to the end of an arm, in the "world" `reference_frame`:

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
### DoCommand

Send/receive arbitrary commands

**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute

**Returns:**

- [(Mapping[str, viam.utils.ValueTypes])](INSERT RETURN TYPE LINK): Result of the executed command

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.do_command).

```python
# Access the motion service
motion = MotionClient.from_robot(robot=robot, name="builtin")

my_command = {
  "command": "dosomething",
  "someparameter": 52
}

await motion.do_command(my_command)
```

### Close

Safely shut down the resource and prevent further use.

**Parameters:**


**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/motion/client/index.html#viam.services.motion.client.MotionClient.close).

```python
await component.close()
```

### GetPaths

Get each path, the series of geo points the robot plans to travel through to get to a destination waypoint, in the machine’s motion planning.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[viam.proto.service.navigation.Path])](INSERT RETURN TYPE LINK): An array comprised of Paths, where each path is either a user-provided destination or
a Waypoint, along with the corresponding set of geopoints. This outlines the route the machine is expected to take to
reach the specified destination or Waypoint.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_paths).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each path stored by the navigation service
paths = await my_nav.get_paths()
```

### GetLocation

Get the current location of the robot in the navigation service.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(viam.services.navigation.GeoPoint)](INSERT RETURN TYPE LINK): The current location of the robot in the navigation service,
represented in a GeoPoint with latitude and longitude values.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_location).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get the current location of the robot in the navigation service
location = await my_nav.get_location()
```

### GetObstacles

Get an array or list of the obstacles currently in the service’s data storage. These are objects designated for the robot to avoid when navigating. These include all transient obstacles which are discovered by the vision services configured for the navigation service, in addition to the obstacles that are configured as a part of the service.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[viam.services.navigation.GeoObstacle])](INSERT RETURN TYPE LINK): A list comprised of each GeoObstacle in the service’s data storage.
These are objects designated for the robot to avoid when navigating.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_obstacles).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each obstacle stored by the navigation service
obstacles = await my_nav.get_obstacles()
```

### GetWaypoints

Get an array of waypoints currently in the service’s data storage. These are locations designated within a path for the robot to navigate to.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[viam.services.navigation.Waypoint])](INSERT RETURN TYPE LINK): An array comprised of each Waypoint in the service’s data storage.
These are locations designated within a path for the robot to navigate to.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_waypoints).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get a list containing each waypoint stored by the navigation service
waypoints = await my_nav.get_waypoints()
```

### AddWaypoint

Add a waypoint to the service’s data storage.

**Parameters:**

- `point` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.add_waypoint).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

 # Create a new waypoint with latitude and longitude values of 0 degrees
 location = GeoPoint(latitude=0, longitude=0)


 # Add your waypoint to the service's data storage
 await my_nav.add_waypoint(point=location)
```

### RemoveWaypoint

Remove a waypoint from the service’s data storage. If the robot is currently navigating to this waypoint, the motion will be canceled, and the robot will proceed to the next waypoint.

**Parameters:**

- `id` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.remove_waypoint).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Remove the waypoint matching that ObjectID from the service's data storage
await my_nav.remove_waypoint(waypoint_id)
```

### GetMode

Get the Mode the service is operating in.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(viam.services.navigation.Mode.ValueType)](INSERT RETURN TYPE LINK): The Mode the service is operating in.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_mode).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get the Mode the service is operating in
await my_nav.get_mode()
```

### SetMode

Set the Mode the service is operating in.

**Parameters:**

- `mode` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.

**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.set_mode).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Set the Mode the service is operating in to MODE_WAYPOINT and begin navigation
await my_nav.set_mode(Mode.ValueType.MODE_WAYPOINT)
```

### GetProperties

Get information about the navigation service.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. An option to set how long to wait (in seconds)
before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(viam.services.navigation.MapType.ValueType)](INSERT RETURN TYPE LINK): Information about the type of map the service is using.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.get_properties).

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Get the properties of the current navigation service.
nav_properties = await my_nav.get_properties()
```

### DoCommand

Send/receive arbitrary commands.

**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute

**Returns:**

- [(Mapping[str, viam.utils.ValueTypes])](INSERT RETURN TYPE LINK): Result of the executed command

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.do_command).

```python
motion = MotionClient.from_robot(robot, "builtin")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

# Can be used with any resource, using the motion service as an example
await motion.do_command(command=my_command)
```

### Close

Safely shut down the resource and prevent further use.

**Parameters:**


**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/navigation/client/index.html#viam.services.navigation.client.NavigationClient.close).

```python
await component.close()
```

### GetPosition

Get current position of the specified component in the SLAM Map.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

- [(viam.services.slam.Pose)](INSERT RETURN TYPE LINK): The current position of the specified component

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_position).

```python
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the current position of the specified source component in the SLAM map as a Pose.
pose = await slam.get_position()
```

### GetPointCloudMap

Get the point cloud map.

**Parameters:**

- `return_edited_map` [(float)](<INSERT PARAM TYPE LINK>): Optional. signal to the SLAM service to return an edited map, if the map package contains one and if
the SLAM service supports the feature
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. signal to the SLAM service to return an edited map, if the map package contains one and if
the SLAM service supports the feature

**Returns:**

- [(List[bytes])](INSERT RETURN TYPE LINK): Complete pointcloud in standard PCD format. Chunks of the PointCloud, concatenating all
GetPointCloudMapResponse.point_cloud_pcd_chunk values.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_point_cloud_map).

```python
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the point cloud map in standard PCD format.
pcd_map = await slam_svc.get_point_cloud_map()
```

### GetInternalState

Get the internal state of the SLAM algorithm required to continue mapping/localization.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

- [(List[bytes])](INSERT RETURN TYPE LINK): Chunks of the internal state of the SLAM algorithm

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_internal_state).

```python
slam = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the internal state of the SLAM algorithm required to continue mapping/localization.
internal_state = await slam.get_internal_state()
```

### GetProperties

Get information regarding the current SLAM session.

**Parameters:**

- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional.

**Returns:**

- [(viam.services.slam.slam.SLAM.Properties)](INSERT RETURN TYPE LINK): The properties of SLAM

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_properties).

```python
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the properties of your current SLAM session.
slam_properties = await slam_svc.get_properties()
```

### DoCommand

Send/receive arbitrary commands.

**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute

**Returns:**

- [(Mapping[str, viam.utils.ValueTypes])](INSERT RETURN TYPE LINK): Result of the executed command

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.do_command).

```python
motion = MotionClient.from_robot(robot, "builtin")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

# Can be used with any resource, using the motion service as an example
await motion.do_command(command=my_command)
```

### Close

Safely shut down the resource and prevent further use.

**Parameters:**


**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.close).

```python
await component.close()
```

### GetDetectionsFromCamera

Get a list of detections in the next image given a camera and a detector

**Parameters:**

- `camera_name` [(float)](<INSERT PARAM TYPE LINK>): Optional. The name of the camera to use for detection
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional. The name of the camera to use for detection
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. The name of the camera to use for detection

**Returns:**

- [(List[viam.proto.service.vision.Detection])](INSERT RETURN TYPE LINK): A list of 2D bounding boxes, their labels, and the
confidence score of the labels, around the found objects in the next 2D image
from the given camera, with the given detector applied to it.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections_from_camera).

```python
camera_name = "cam1"

# Grab the detector you configured on your machine
my_detector = VisionClient.from_robot(robot, "my_detector")

# Get detections from the next image from the camera
detections = await my_detector.get_detections_from_camera(camera_name)
```

### GetDetections

Get a list of detections in the given image using the specified detector

**Parameters:**

- `image` [(float)](https://python.viam.dev/autoapi/viam/../media/video/index.html#viam.media.video.RawImage): Optional. The image to get detections from
- `extra` [(float)](https://python.viam.dev/autoapi/viam/../media/video/index.html#viam.media.video.RawImage): Optional. The image to get detections from
- `timeout` [(float)](https://python.viam.dev/autoapi/viam/../media/video/index.html#viam.media.video.RawImage): Optional. The image to get detections from

**Returns:**

- [(List[viam.proto.service.vision.Detection])](INSERT RETURN TYPE LINK): A list of 2D bounding boxes, their labels, and the
confidence score of the labels, around the found objects in the next 2D image
from the given camera, with the given detector applied to it.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_detections).

```python
# Grab camera from the machine
cam1 = Camera.from_robot(robot, "cam1")

# Get the detector you configured on your machine
my_detector = VisionClient.from_robot(robot, "my_detector")

# Get an image from the camera
img = await cam1.get_image()

# Get detections from that image
detections = await my_detector.get_detections(img)
```

### GetClassificationsFromCamera

Get a list of classifications in the next image given a camera and a classifier

**Parameters:**

- `camera_name` [(float)](<INSERT PARAM TYPE LINK>): Optional. The number of classifications desired
- `count` [(float)](<INSERT PARAM TYPE LINK>): Optional. The number of classifications desired
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional. The number of classifications desired
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. The number of classifications desired

**Returns:**

- [(List[viam.proto.service.vision.Classification])](INSERT RETURN TYPE LINK): The list of Classifications

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_classifications_from_camera).

```python
camera_name = "cam1"

# Grab the classifier you configured on your machine
my_classifier = VisionClient.from_robot(robot, "my_classifier")

# Get the 2 classifications with the highest confidence scores from the next image from the camera
classifications = await my_classifier.get_classifications_from_camera(
    camera_name, 2)
```

### GetClassifications

Get a list of classifications in the given image using the specified classifier

**Parameters:**

- `image` [(float)](https://python.viam.dev/autoapi/viam/../media/video/index.html#viam.media.video.RawImage): Optional. The number of classifications desired
- `count` [(float)](https://python.viam.dev/autoapi/viam/../media/video/index.html#viam.media.video.RawImage): Optional. The number of classifications desired
- `extra` [(float)](https://python.viam.dev/autoapi/viam/../media/video/index.html#viam.media.video.RawImage): Optional. The number of classifications desired
- `timeout` [(float)](https://python.viam.dev/autoapi/viam/../media/video/index.html#viam.media.video.RawImage): Optional. The number of classifications desired

**Returns:**

- [(List[viam.proto.service.vision.Classification])](INSERT RETURN TYPE LINK): The list of Classifications

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_classifications).

```python
# Grab camera from the machine
cam1 = Camera.from_robot(robot, "cam1")

# Get the classifier you configured on your machine
my_classifier = VisionClient.from_robot(robot, "my_classifier")

# Get an image from the camera
img = await cam1.get_image()

# Get the 2 classifications with the highest confidence scores
classifications = await my_classifier.get_classifications(img, 2)
```

### GetObjectPointClouds

Returns a list of the 3D point cloud objects and associated metadata in the latest picture obtained from the specified 3D camera (using the specified segmenter).

**Parameters:**

- `camera_name` [(float)](<INSERT PARAM TYPE LINK>): Optional. The name of the camera
- `extra` [(float)](<INSERT PARAM TYPE LINK>): Optional. The name of the camera
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. The name of the camera

**Returns:**

- [(List[viam.proto.common.PointCloudObject])](INSERT RETURN TYPE LINK): The pointcloud objects with metadata

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.get_object_point_clouds).

```python
import numpy as np
import open3d as o3d

# Grab the 3D camera from the machine
cam1 = Camera.from_robot(robot, "cam1")
# Grab the object segmenter you configured on your machine
my_segmenter = VisionClient.from_robot(robot, "my_segmenter")
# Get the objects from the camera output
objects = await my_segmenter.get_object_point_clouds(cam1)
# write the first object point cloud into a temporary file
with open("/tmp/pointcloud_data.pcd", "wb") as f:
    f.write(objects[0].point_cloud)
pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
points = np.asarray(pcd.points)
```

### DoCommand

Send/receive arbitrary commands.

**Parameters:**

- `command` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute
- `timeout` [(float)](<INSERT PARAM TYPE LINK>): Optional. The command to execute

**Returns:**

- [(Mapping[str, viam.utils.ValueTypes])](INSERT RETURN TYPE LINK): Result of the executed command

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.do_command).

```python
motion = MotionClient.from_robot(robot, "builtin")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

# Can be used with any resource, using the motion service as an example
await motion.do_command(command=my_command)
```

### Close

Safely shut down the resource and prevent further use.

**Parameters:**


**Returns:**

None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/vision/client/index.html#viam.services.vision.client.VisionClient.close).

```python
await component.close()
```

