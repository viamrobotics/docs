### GetOperations

Get the list of operations currently running on the machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- ([List[viam.proto.robot.Operation]](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.Operation)): The list of operations currently running on a given machine.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
operations = await machine.get_operations()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_operations).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (Promise<[Operation](https://ts.viam.dev/classes/robotApi.Operation.html)[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const operations = await machine.getOperations();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#getoperations).

{{% /tab %}}
{{< /tabs >}}

### GetMachineStatus

Get status information about the machine.
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- ([viam.proto.robot.GetMachineStatusResponse](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.GetMachineStatusResponse)): current status of the machine (initializing or running), resources (List\[ResourceStatus]) and config of the machine.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
machine_status = await machine.get_machine_status()
machine_state = machine_status.state
resource_statuses = machine_status.resources
cloud_metadata = machine_status.resources[0].cloud_metadata
config_status = machine_status.config
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_machine_status).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(MachineStatus)](https://pkg.go.dev/go.viam.com/rdk/robot#MachineStatus)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (Promise<[GetMachineStatusResponse](https://ts.viam.dev/classes/robotApi.GetMachineStatusResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const machineStatus = await machine.getMachineStatus();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#getmachinestatus).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[GetMachineStatusResponse](https://flutter.viam.dev/viam_protos.robot.robot/GetMachineStatusResponse-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var machineStatus = await machine.getMachineStatus();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/RobotClient/getMachineStatus.html).

{{% /tab %}}
{{< /tabs >}}

### GetSessions

Get the list of sessions currently connected to the robot.

{{< tabs >}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (Promise<[Session](https://ts.viam.dev/classes/robotApi.Session.html)[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const sessions = await machine.getSessions();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#getsessions).

{{% /tab %}}
{{< /tabs >}}

### ResourceNames

Get a list of all known resource names connected to this machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- None.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
resource_names = machine.resource_names
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.resource_names).

{{% /tab %}}
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

- None.

**Returns:**

- (Promise<[commonApi](https://ts.viam.dev/modules/commonApi.html).[ResourceName](https://ts.viam.dev/classes/commonApi.ResourceName.html)[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const resourceNames = await machine.resourceNames();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#resourcenames).

{{% /tab %}}
{{< /tabs >}}

### ResourceRPCSubtypes

Get a list of all resource types.

{{< tabs >}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (Promise<[ResourceRPCSubtype](https://ts.viam.dev/classes/robotApi.ResourceRPCSubtype.html)[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const resourceRPCSubtypes = await machine.resourceRPCSubtypes();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#resourcerpcsubtypes).

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
await machine.cancel_operation("INSERT OPERATION ID")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.cancel_operation).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): ID of operation to kill.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await machine.cancelOperation('INSERT OPERATION ID');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#canceloperation).

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
await machine.block_for_operation("INSERT OPERATION ID")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.block_for_operation).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `id` (string) (required): ID of operation to block on.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await machine.blockForOperation('INSERT OPERATION ID');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#blockforoperation).

{{% /tab %}}
{{< /tabs >}}

### FrameSystemConfig

Get the configuration of the frame system of a given machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `additional_transforms` ([List[viam.proto.common.Transform]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)) (optional): Any additional transforms.

**Returns:**

- ([List[viam.proto.robot.FrameSystemConfig]](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.FrameSystemConfig)): The configuration of a given machine’s frame system.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Get a list of each of the reference frames configured on the machine.
frame_system = await machine.get_frame_system_config()
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
frameSystem, err := machine.FrameSystemConfig(context.Background())
fmt.Println(frameSystem)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `transforms` ([commonApi](https://ts.viam.dev/modules/commonApi.html)) (required)

**Returns:**

- (Promise<[FrameSystemConfig](https://ts.viam.dev/classes/robotApi.FrameSystemConfig.html)[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const frameSystemConfig = await machine.frameSystemConfig();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#framesystemconfig).

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
from viam.proto.common import Pose, PoseInFrame

pose = Pose(
    x=1.0,    # X coordinate in mm
    y=2.0,    # Y coordinate in mm
    z=3.0,    # Z coordinate in mm
    o_x=0.0,  # X component of orientation vector
    o_y=0.0,  # Y component of orientation vector
    o_z=0.0,  # Z component of orientation vector
    theta=0.0 # Orientation angle in degrees
)

pose_in_frame = PoseInFrame(
    reference_frame="world",
    pose=pose
)

transformed_pose = await machine.transform_pose(pose_in_frame, "world")
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
movementSensorToBase, err := machine.TransformPose(context.Background(), baseOrigin, "my-movement-sensor", nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `source` ([commonApi](https://ts.viam.dev/modules/commonApi.html)) (required)
- `destination` (string) (required): The name of the reference frame to transform the given.
- `supplementalTransforms` ([commonApi](https://ts.viam.dev/modules/commonApi.html)) (required): Pose information on any additional
  reference frames that are needed to perform the transform.

**Returns:**

- (Promise<[commonApi](https://ts.viam.dev/modules/commonApi.html).[PoseInFrame](https://ts.viam.dev/classes/commonApi.PoseInFrame.html)>)

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#transformpose).

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
{{% tab name="TypeScript" %}}

**Parameters:**

- `pointCloudPCD` (Uint8Array) (required): The point clouds to transform. This should be in the
  [PCD format encoded into bytes](https://pointclouds.org/documentation/tutorials/pcd_file_format.html).
- `source` (string) (required): The reference frame of the point cloud.
- `destination` (string) (required): The reference frame into which the source data should
  be transformed, if unset this defaults to the "world" reference frame. Do
  not move the robot between the generation of the initial pointcloud and
  the receipt of the transformed pointcloud because that will make the
  transformations inaccurate.

**Returns:**

- (Promise<Uint8Array>)

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#transformpcd).

{{% /tab %}}
{{< /tabs >}}

### GetModelsFromModules

Get a list of all models provided by local and registry modules on the machine.
This includes models that are not currently configured on the machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- ([List[viam.proto.robot.ModuleModel]](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.ModuleModel)): A list of discovered models.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
# Get module models
module_models = await machine.get_models_from_modules(qs)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_models_from_modules).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [([]resource.ModuleModel)](https://pkg.go.dev/go.viam.com/rdk/resource#ModuleModel)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
//Get a list of models found in configured modules.
models, err := machine.GetModelsFromModules(ctx)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (Promise<[ModuleModel](https://ts.viam.dev/classes/robotApi.ModuleModel.html)[]>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const models = await machine.getModelsFromModules();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#getmodelsfrommodules).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[List](https://api.flutter.dev/flutter/dart-core/List-class.html)\<[ModuleModel](https://flutter.viam.dev/viam_protos.robot.robot/ModuleModel-class.html)\>\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var modelsFromModules = await machine.getModelsFromModules();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/RobotClient/getModelsFromModules.html).

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
# Cancel all current and outstanding operations for the machine and stop all actuators and movement.
await machine.stop_all()
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
err := machine.StopAll(context.Background(), nil)
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await machine.stopAll();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#stopall).

{{% /tab %}}
{{< /tabs >}}

### RestartModule

Reload a module as if its config changed.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `id` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): The id matching the module_id field of the registry module in your part configuration.
- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (optional): The name matching the name field of the local/registry module in your part configuration.

**Returns:**

- None.

**Raises:**

- (GRPCError): If a module can’t be found matching the provided ID or name.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await machine.restart_module(id="namespace:module:model", name="my_model")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.restart_module).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `req` [(RestartModuleRequest)](https://pkg.go.dev/go.viam.com/rdk/robot#RestartModuleRequest)

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `moduleId` (string) (optional): The id matching the module\_id field of the registry
  module in your part configuration.
- `moduleName` (string) (optional): The name matching the name field of the local/registry
  module in your part configuration.

**Returns:**

- (Promise<void>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
await machine.restartModule('namespace:module:model', 'my_model_name');
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#restartmodule).

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
- `message` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The log message.
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

- ([viam.proto.robot.GetCloudMetadataResponse](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.GetCloudMetadataResponse)): App\-related metadata.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
metadata = await machine.get_cloud_metadata()
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

- [(cloud.Metadata)](https://pkg.go.dev/go.viam.com/rdk/cloud#Metadata): App-related metadata containing the primary organization ID, location ID, and robot part ID for a machine running on Viam.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
metadata, err := machine.CloudMetadata(context.Background())
primary_org_id := metadata.PrimaryOrgID
location_id := metadata.LocationID
machine_id := metadata.MachineID
machine_part_id := metadata.MachinePartID
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (Promise<[GetCloudMetadataResponse](https://ts.viam.dev/classes/robotApi.GetCloudMetadataResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const cloudMetadata = await machine.getCloudMetadata();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#getcloudmetadata).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[CloudMetadata](https://flutter.viam.dev/viam_sdk/CloudMetadata.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
var metadata = await machine.getCloudMetadata();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/RobotClient/getCloudMetadata.html).

{{% /tab %}}
{{< /tabs >}}

### GetVersion

Return version information about the machine.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None.

**Returns:**

- ([viam.proto.robot.GetVersionResponse](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.GetVersionResponse)): Machine version related information.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
result = await machine.get_version()
print(result.platform)
print(result.version)
print(result.api_version)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_version).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(VersionResponse)](https://pkg.go.dev/go.viam.com/rdk/robot#VersionResponse)
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None.

**Returns:**

- (Promise<[GetVersionResponse](https://ts.viam.dev/classes/robotApi.GetVersionResponse.html)>)

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/Client.html#getversion).

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

machine = await RobotClient.at_address('<ADDRESS-FROM-THE-VIAM-APP>', opts)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options.with_api_key).

{{% /tab %}}
{{< /tabs >}}

### AtAddress

Create a RobotClient that is connected to the machine at the provided address.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `address` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): Address of the machine (IP address, URL, etc.).
- `options` ([Options](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options)) (required): Options for connecting and refreshing.

**Returns:**

- ([typing_extensions.Self](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient))

**Example:**

```python {class="line-numbers linkable-line-numbers"}
async def connect():

    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's API key
        api_key='<API-KEY>',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
        api_key_id='<API-KEY-ID>'
    )
    return await RobotClient.at_address('MACHINE ADDRESS', opts)


async def main():
    # Make a RobotClient
    machine = await connect()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.at_address).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- `url` [String](https://api.flutter.dev/flutter/dart-core/String-class.html) (required)
- `options` [RobotClientOptions](https://flutter.viam.dev/viam_sdk/RobotClientOptions-class.html) (required)

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<[RobotClient](https://flutter.viam.dev/viam_sdk/RobotClient-class.html)\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
// Example usage; see your machine's CONNECT tab for your machine's address and API key.

Future<void> connectToViam() async {
  const host = '<YOUR ROBOT ADDRESS>.viam.cloud';
  // Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID
  const apiKeyID = '<API-KEY-ID>';
  // Replace "<API-KEY>" (including brackets) with your machine's API key
  const apiKey = '<API-KEY>';

  final machine = await RobotClient.atAddress(
    host,
    RobotClientOptions.withApiKey(apiKeyID, apiKey),
  );
}
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/RobotClient/atAddress.html).

{{% /tab %}}
{{< /tabs >}}

### WithChannel

Create a RobotClient that is connected to a machine over the given channel.
Any machines created using this method will NOT automatically close the channel upon exit.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `channel` ([grpclib.client.Channel | viam.rpc.dial.ViamChannel](https://python.viam.dev/autoapi/viam/rpc/dial/index.html#viam.rpc.dial.ViamChannel)) (required): The channel that is connected to a machine, obtained by viam.rpc.dial.
- `options` ([Options](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.Options)) (required): Options for refreshing. Any connection options will be ignored.

**Returns:**

- ([typing_extensions.Self](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient))

**Example:**

```python {class="line-numbers linkable-line-numbers"}
from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions, dial


async def connect_with_channel() -> RobotClient:
    async with await dial('ADDRESS', DialOptions()) as channel:
        return await RobotClient.with_channel(channel, RobotClient.Options())

machine = await connect_with_channel()
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
await machine.refresh()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.refresh).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
await machine.refresh();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/RobotClient/refresh.html).

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

- (GRPCError): Raised with DeadlineExceeded status if shutdown request times out, or if the machine server shuts down before having a chance to send a response. Raised with status Unavailable if server is unavailable, or if machine server is in the process of shutting down when response is ready.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
await machine.shutdown()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.shutdown).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Shut down the robot.
err := machine.Shutdown(context.Background())
```

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
await machine.close()
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
err := machine.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="Flutter" %}}

**Parameters:**

- None.

**Returns:**

- [Future](https://api.flutter.dev/flutter/dart-async/Future-class.html)\<void\>

**Example:**

```dart {class="line-numbers linkable-line-numbers"}
await machine.close();
```

For more information, see the [Flutter SDK Docs](https://flutter.viam.dev/viam_sdk/RobotClient/close.html).

{{% /tab %}}
{{< /tabs >}}
