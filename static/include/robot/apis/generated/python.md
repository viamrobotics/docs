### Options.with_api_key

Create RobotClient.Options with an [API key](/fleet/cli/#authenticate) for credentials and default values for other arguments.


**Parameters:**

- `api_key` [(str)](<INSERT PARAM TYPE LINK>):
- `api_key_id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**

([typing_extensions.Self](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options.with_api_key).

```python
# Replace "<API-KEY>" (including brackets) with your machine's API key
api_key = '<API-KEY>'
# Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
api_key_id = '<API-KEY-ID>'

opts = RobotClient.Options.with_api_key(api_key, api_key_id)

robot = await RobotClient.at_address('<ADDRESS-FROM-THE-VIAM-APP>', opts)
```

### AtAddress

Create a robot client that is connected to the robot at the provided address.


**Parameters:**

- `address` [(Options)](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options):
- `options` [(Options)](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options):

**Returns:**

([typing_extensions.Self](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.at_address).

```python
async def connect():

    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('ADDRESS FROM THE VIAM APP', opts)


async def main():
    # Make a RobotClient
    robot = await connect()
```

### WithChannel

Create a robot that is connected to a robot over the given channel.


**Parameters:**

- `channel` [(Options)](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options):
- `options` [(Options)](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options):

**Returns:**

([typing_extensions.Self](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.with_channel).

```python
from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions, dial


async def connect_with_channel() -> RobotClient:
    async with await dial('ADDRESS', DialOptions()) as channel:
        return await RobotClient.with_channel(channel, RobotClient.Options())

robot = await connect_with_channel()
```

### Refresh

Manually refresh the underlying parts of this robot


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.refresh).

```python
await robot.refresh()
```

### Close

Cleanly close the underlying connections and stop any periodic tasks.


**Parameters:**


**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.close).

```python
await robot.close()
```

### GetStatus

Get the status of the robot’s components. You can optionally provide a list of ResourceName for which you want statuses.


**Parameters:**

- `components` [(List[viam.proto.common.ResourceName])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName): Optional.

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_status).

```python
# Get the status of the resources on the machine.
statuses = await robot.get_status()
```

### GetOperations

Get the list of operations currently running on the robot.


**Parameters:**


**Returns:**

([List[viam.proto.robot.Operation]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_operations).

```python
operations = await robot.get_operations()
```

### CancelOperation

Cancels the specified operation on the robot.


**Parameters:**

- `id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.cancel_operation).

```python
await robot.cancel_operation("INSERT OPERATION ID")
```

### BlockForOperation

Blocks on the specified operation on the robot. This function will only return when the specific operation has finished or has been cancelled.


**Parameters:**

- `id` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.block_for_operation).

```python
await robot.block_for_operation("INSERT OPERATION ID")
```

### FrameSystemConfig

Get the configuration of the [frame](/mobility/frame-system/) system of a given robot.


**Parameters:**

- `additional_transforms` [(List[viam.proto.common.Transform])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform): Optional.

**Returns:**

([List[viam.proto.robot.FrameSystemConfig]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_frame_system_config).

```python
# Get a list of each of the reference frames configured on the machine.
frame_system = await robot.get_frame_system_config()
print(f"frame system configuration: {frame_system}")
```

### TransformPose

Transform a given source Pose from the reference [frame](/mobility/frame-system/) to a new specified destination which is a reference [frame](/mobility/frame-system/).


**Parameters:**

- `query` [(List[viam.proto.common.Transform])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform): Optional.
- `destination` [(List[viam.proto.common.Transform])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform): Optional.
- `additional_transforms` [(List[viam.proto.common.Transform])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform): Optional.

**Returns:**

([viam.proto.common.PoseInFrame](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.transform_pose).

```python
pose = await robot.transform_pose(PoseInFrame(), "origin")
```

### DiscoverComponents

Get the list of discovered component configurations.


**Parameters:**

- `queries` [(List[viam.proto.robot.DiscoveryQuery])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery):

**Returns:**

([List[viam.proto.robot.Discovery]](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.discover_components).

```python
# Define a new discovery query.
q = robot.DiscoveryQuery(subtype=acme.API, model="some model")

# Define a list of discovery queries.
qs = [q]

# Get component configurations with these queries.
component_configs = await robot.discover_components(qs)
```

### StopAll

Cancel all current and outstanding operations for the robot and stop all actuators and movement.


**Parameters:**

- `extra` [(Dict[viam.proto.common.ResourceName, Dict[str, Any]])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.stop_all).

```python
# Cancel all current and outstanding operations for the robot and stop all actuators and movement.
await robot.stop_all()
```

### Log

Send log from Python module over gRPC.


**Parameters:**

- `name` [(str)](<INSERT PARAM TYPE LINK>):
- `level` [(str)](<INSERT PARAM TYPE LINK>):
- `time` [(str)](<INSERT PARAM TYPE LINK>):
- `log` [(str)](<INSERT PARAM TYPE LINK>):
- `stack` [(str)](<INSERT PARAM TYPE LINK>):

**Returns:**


For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.log).

### GetCloudMetadata

Get app-related information about the robot.


**Parameters:**


**Returns:**

([viam.proto.robot.GetCloudMetadataResponse](<INSERT RETURN TYPE LINK>)))
For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_cloud_metadata).

