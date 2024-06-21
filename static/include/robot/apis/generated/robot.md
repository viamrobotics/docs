### GetOperations

Get the list of operations currently running on the machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- ([List[viam.proto.robot.Operation]](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.Operation)): The list of operations currently running on a given robot.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
operations = await robot.get_operations()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_operations).

{{% /tab %}}
{{< /tabs >}}

### ResourceNames

Get a list of all known resource names connected to this machine.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): A list of all known resource names.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
resource_names := machine.ResourceNames()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- [(ResourceName.AsObject[])](https://ts.viam.dev/modules/commonApi.ResourceName-1.html): List of all known resource names.

```typescript
// Get a list of all resources on the machine.
const resource_names = await machine.resourceNames();
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/classes/RobotClient.html).

{{% /tab %}}
{{< /tabs >}}

### CancelOperation

Cancel the specified operation on the machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of operation to cancel.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await robot.cancel_operation("INSERT OPERATION ID")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.cancel_operation).

{{% /tab %}}
{{< /tabs >}}

### BlockForOperation

Blocks on the specified operation on the machine.
This function will only return when the specific operation has finished or has been cancelled.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): ID of operation to block on.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await robot.block_for_operation("INSERT OPERATION ID")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.block_for_operation).

{{% /tab %}}
{{< /tabs >}}

### DiscoverComponents

Get a list of discovered component configurations.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `queries` ([List[viam.proto.robot.DiscoveryQuery]](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery)) (required): The list of component models to lookup configurations for.

**Returns:**

- ([List[viam.proto.robot.Discovery]](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.Discovery)): A list of discovered component configurations.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Define a new discovery query.
q = robot.DiscoveryQuery(subtype=acme.API, model="some model")

# Define a list of discovery queries.
qs = [q]

# Get component configurations with these queries.
component_configs = await robot.discover_components(qs)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.discover_components).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `qs` [([]resource.DiscoveryQuery)](https://pkg.go.dev/go.viam.com/rdk/resource#DiscoveryQuery): A list of [tuples of API and model](https://pkg.go.dev/go.viam.com/rdk/resource#DiscoveryQuery) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [([]resource.Discovery)](https://pkg.go.dev/go.viam.com/rdk/resource#Discovery): The search query `qs` and the corresponding list of discovered component configurations as an interface called `Results`. `Results` may be comprised of primitives, a list of primitives, maps with string keys (or at least can be decomposed into one), or lists of the forementioned type of maps.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Define a new discovery query.
q := resource.NewDiscoveryQuery(acme.API, resource.Model{Name: "some model"})

// Define a list of discovery queries.
qs := []resource.DiscoverQuery{q}

// Get component configurations with these queries.
component_configs, err := machine.DiscoverComponents(ctx.Background(), qs)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `queries` [(DiscoveryQuery[])](https://ts.viam.dev/classes/robotApi.DiscoveryQuery.html): An array of [tuples of API and model](https://ts.viam.dev/classes/robotApi.DiscoveryQuery.html#constructor) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [(Discovery[])](https://ts.viam.dev/classes/robotApi.Discovery.html): List of discovered component configurations.

```typescript
// Define a new discovery query.
const q = new proto.DiscoveryQuery(acme.API, resource.Model{Name: "some model"})

// Define an array of discovery queries.
let qs:  proto.DiscoveryQuery[] = [q]

// Get the array of discovered component configurations.
const componentConfigs = await machine.discoverComponents(queries);
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/classes/RobotClient.html).

{{% /tab %}}
{{< /tabs >}}

### FrameSystemConfig

Get the configuration of the frame system of a given machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `additional_transforms` ([List[viam.proto.common.Transform]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)) (optional): Any additional transforms.

**Returns:**

- ([List[viam.proto.robot.FrameSystemConfig]](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.FrameSystemConfig)): The configuration of a given robot’s frame system.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Get a list of each of the reference frames configured on the machine.
frame_system = await robot.get_frame_system_config()
print(f"frame system configuration: {frame_system}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_frame_system_config).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(*framesystem.Config)](https://pkg.go.dev/go.viam.com/rdk/robot/framesystem#Config): The configuration of the given machine’s frame system.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Print the frame system configuration
frameSystem, err := machine.FrameSystemConfig(context.Background(), nil)
fmt.Println(frameSystem)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `transforms` [(Transform[])](https://ts.viam.dev/classes/commonApi.Transform.html): An optional array of [additional transforms](/services/frame-system/#additional-transforms).

**Returns:**

- [(FrameSystemConfig[])](https://ts.viam.dev/classes/robotApi.FrameSystemConfig.html): An array of individual parts that make up a machine's frame system.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#frameSystemConfig).

```typescript {class="line-numbers linkable-line-numbers"}
// Get the frame system configuration
console.log("FrameSytemConfig:", await robot.frameSystemConfig());
```

{{% /tab %}}
{{< /tabs >}}

### TransformPose

Transform a given source Pose from the original reference frame to a new destination reference frame.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `query` ([viam.proto.common.PoseInFrame](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame)) (required): The pose that should be transformed.
- `destination` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the reference frame to transform the given pose to.
- `additional_transforms` ([List[viam.proto.common.Transform]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)) (optional): Any additional transforms.

**Returns:**

- ([viam.proto.common.PoseInFrame](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame)): The pose and the reference frame for the new destination.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
pose = await robot.transform_pose(PoseInFrame(), "origin")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.transform_pose).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `pose` [(*referenceframe.PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): The pose that should be transformed.
- `dst` [(string)](https://pkg.go.dev/builtin#string): The name of the reference pose to transform the given pose to.
- `additionalTransforms` [([]*referenceframe.LinkInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#LinkInFrame): Any additional transforms.

**Returns:**

- [(*referenceframe.PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): Transformed pose in frame.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
import (
  "go.viam.com/rdk/referenceframe"
  "go.viam.com/rdk/spatialmath"
)

baseOrigin := referenceframe.NewPoseInFrame("test-base", spatialmath.NewZeroPose())
movementSensorToBase, err := machine.TransformPose(ctx, baseOrigin, "my-movement-sensor", nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{< /tabs >}}

### TransformPCD

Transforms the pointcloud to the desired frame in the robot's frame system.
Do not move the robot between the generation of the initial pointcloud and the receipt of the transformed pointcloud, as doing so will make the transformations inaccurate.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `srcpc` [(pointcloud.PointCloud)](https://pkg.go.dev/go.viam.com/rdk/pointcloud#PointCloud): The source `PointCloud` to transform.
- `srcName` [(string)](https://pkg.go.dev/builtin#string): The name of the source point cloud to transform.
- `dstName` [(string)](https://pkg.go.dev/builtin#string): The name of the destination point cloud.

**Returns:**

- [(pointcloud.PointCloud)](https://pkg.go.dev/go.viam.com/rdk/pointcloud#PointCloud): The transformed `PointCloud`.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{< /tabs >}}

### GetStatus

Get the status of the resources on the machine.
You can provide a list of ResourceNames for which you want statuses.
If no names are passed in, the status of every resource configured on the machine is returned.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `components` ([List[viam.proto.common.ResourceName]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)) (optional): Optional list of ResourceName for components you want statuses.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Get the status of the resources on the machine.
statuses = await robot.get_status()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_status).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `resourceNames` [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): A list of resource names for components you want the status of. If no names are passed in, all resource statuses are returned.

**Returns:**

- [([]Status)](https://pkg.go.dev/go.viam.com/rdk/robot#Status): The `Status` of each resource queried. If no resource was provided as a parameter, the status of all resources is returned.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
status, err := machine.Status(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `resourceNames` [(commonApi.ResourceName[])](https://ts.viam.dev/classes/commonApi.ResourceName.html): An optional array of ResourceNames for components you want the status of.
  If no names are passed in, all resource statuses are returned.

**Returns:**

- [(robotApi.Status[])](https://ts.viam.dev/classes/robotApi.Status.html): An array containing the status of each resource.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#transformPCD).

```typescript {class="line-numbers linkable-line-numbers"}
// Get the status of the resources on the machine.
const status = await machine.getStatus();
```

{{% /tab %}}
{{< /tabs >}}

### StopAll

Cancel all current and outstanding operations for the machine and stop all actuators and movement.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), Any]) (required): Extra options to pass to the underlying RPC call.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Cancel all current and outstanding operations for the robot and stop all actuators and movement.
await robot.stop_all()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.stop_all).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[string]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the machine and stop all actuators and movement.
err := machine.StopAll(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#stopAll).

```typescript {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the machine and stop all actuators and movement.
await machine.stopAll();
```

{{% /tab %}}
{{< /tabs >}}

### Log

Create a LogEntry object from the log to send to the RDK over gRPC.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The logger’s name.
- `level` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The level of the log.
- `time` ([datetime.datetime](https://docs.python.org/3/library/datetime.html)) (required): The log creation time.
- `log` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The log message.
- `stack` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The stack information of the log.

**Returns:**

- None.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.log).

{{% /tab %}}
{{< /tabs >}}

### GetCloudMetadata

Get app-related information about the robot.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- ([viam.proto.robot.GetCloudMetadataResponse](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.GetCloudMetadataResponse)): App-related metadata.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
metadata = machine.get_cloud_metadata()
print(metadata.machine_id)
print(metadata.machine_part_id)
print(metadata.primary_org_id)
print(metadata.location_id)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_cloud_metadata).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(cloud.Metadata)](https://pkg.go.dev/go.viam.com/rdk/cloud#Metadata): App-related metadata containing the primary organization ID, location ID, and robot part ID for a machine running on the Viam app.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
metadata, err := machine.CloudMetadata(ctx.Background())
machine_part_id = metadata.MachinePartID
primary_org_id = metadata.PrimaryOrgID
location_id = metadata.LocationID
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{< /tabs >}}

### Options.with_api_key

Create a `RobotClient.Options` using an API key as credentials.
Pass these options to [`AtAddress`](#ataddress).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `api_key` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): your API key.
- `api_key_id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): your API key ID. Must be a valid UUID.

**Returns:**

- ([typing_extensions.Self](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient)): the RobotClient.Options.

**Raises:**

- (ValueError): Raised if the api_key_id is not a valid UUID.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Replace "<API-KEY>" (including brackets) with your machine's API key
api_key = '<API-KEY>'
# Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
api_key_id = '<API-KEY-ID>'

opts = RobotClient.Options.with_api_key(api_key, api_key_id)

robot = await RobotClient.at_address('<ADDRESS-FROM-THE-VIAM-APP>', opts)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options.with_api_key).

{{% /tab %}}
{{< /tabs >}}

### AtAddress

Create a RobotClient that is connected to the machine at the provided address.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `address` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Address of the robot (IP address, URL, etc.).
- `options` ([Options](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options)) (required): Options for connecting and refreshing.

**Returns:**

- ([typing_extensions.Self](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient)): the RobotClient.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
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

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.at_address).

{{% /tab %}}
{{< /tabs >}}

### WithChannel

Create a RobotClient that is connected to a machine over the given channel.
Any machines created using this method will NOT automatically close the channel upon exit.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `channel` ([grpclib.client.Channel | viam.rpc.dial.ViamChannel](https://python.viam.dev/autoapi/viam/rpc/dial/index.html#viam.rpc.dial.ViamChannel)) (required): The channel that is connected to a robot, obtained by viam.rpc.dial.
- `options` ([Options](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options)) (required): Options for refreshing. Any connection options will be ignored.

**Returns:**

- ([typing_extensions.Self](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient)): the RobotClient.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions, dial


async def connect_with_channel() -> RobotClient:
    async with await dial('ADDRESS', DialOptions()) as channel:
        return await RobotClient.with_channel(channel, RobotClient.Options())

robot = await connect_with_channel()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.with_channel).

{{% /tab %}}
{{< /tabs >}}

### Refresh

Manually refresh the underlying parts of this machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await robot.refresh()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.refresh).

{{% /tab %}}
{{< /tabs >}}

### Shutdown

Shutdown shuts down the machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Raises:**

- (GRPCError): Raised with DeadlineExceeded status if shutdown request times out, or if robot server shuts down before having a chance to send a response. Raised with status Unavailable if server is unavailable, or if robot server is in the process of shutting down when response is ready.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.shutdown).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{< /tabs >}}

### Close

Close the underlying connections and stop any periodic tasks across all constituent parts of the machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await robot.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Cleanly close the underlying connections and stop any periodic tasks,
err := machine.Close(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#disconnect).

```typescript {class="line-numbers linkable-line-numbers"}
// Cleanly close the underlying connections and stop any periodic tasks
await machine.disconnect();
```

{{% /tab %}}
{{< /tabs >}}
