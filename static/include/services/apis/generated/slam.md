### GetPosition

Get the current position of the component the SLAM service is configured to source point cloud data from in the SLAM map as a [`Pose`](/operate/mobility/orientation-vector/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- ([viam.services.slam.Pose](https://python.viam.dev/autoapi/viam/services/slam/index.html#viam.services.slam.Pose)): The current position of the specified component.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=machine, name="my_slam_service")

# Get the current position of the specified source component in the SLAM map as a Pose.
pose = await slam.get_position()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_position).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): A `Pose` representing the current position of the specified component.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the current position of the specified source component
// in the SLAM map as a Pose.
pos, name, err := mySLAMService.Position(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[slamApi](https://ts.viam.dev/modules/slamApi.html).[GetPositionResponse](https://ts.viam.dev/classes/slamApi.GetPositionResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const slam = new VIAM.SlamClient(machine, 'my_slam');

// Get the current position of the robot in the SLAM map
const position = await slam.getPosition();
console.log('Current position:', position);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SlamClient.html#getposition).

{{% /tab %}}
{{< /tabs >}}

### GetPointCloudMap

Get the point cloud map.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `return_edited_map` ([bool](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)) (required): signal to the SLAM service to return an edited map, if the map package contains one and if the SLAM service supports the feature.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (List[[bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)]): Complete pointcloud in standard PCD format. Chunks of the PointCloud, concatenating all
GetPointCloudMapResponse.point\_cloud\_pcd\_chunk values.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=machine, name="my_slam_service")

# Get the point cloud map in standard PCD format.
pcd_map = await slam_svc.get_point_cloud_map()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_point_cloud_map).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `returnEditedMap` [(bool)](https://pkg.go.dev/builtin#bool)

**Returns:**

- None.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `returnEditedMap` (boolean) (optional)
- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<Uint8Array>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const slam = new VIAM.SlamClient(machine, 'my_slam');

// Get the point cloud map
const pointCloudMap = await slam.getPointCloudMap();

// Get the edited point cloud map
const editedMap = await slam.getPointCloudMap(true);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SlamClient.html#getpointcloudmap).

{{% /tab %}}
{{< /tabs >}}

### GetInternalState

Get the internal state of the SLAM algorithm required to continue mapping/localization.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (List[[bytes](https://docs.python.org/3/library/stdtypes.html#bytes-objects)]): Chunks of the internal state of the SLAM algorithm.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
slam = SLAMClient.from_robot(robot=machine, name="my_slam_service")

# Get the internal state of the SLAM algorithm required to continue mapping/localization.
internal_state = await slam.get_internal_state()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_internal_state).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- None.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<Uint8Array>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const slam = new VIAM.SlamClient(machine, 'my_slam');

// Get the internal state of the SLAM algorithm
const internalState = await slam.getInternalState();
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SlamClient.html#getinternalstate).

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get information about the current SLAM session.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (viam.services.slam.slam.SLAM.Properties): The properties of SLAM.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=machine, name="my_slam_service")

# Get the properties of your current SLAM session.
slam_properties = await slam_svc.get_properties()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_properties).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(Properties)](https://pkg.go.dev/go.viam.com/rdk/services/slam#Properties): 
Information about the current SLAM session.
An object containing four fields:

- `SensorInfo` [(SensorInfo[])](https://pkg.go.dev/go.viam.com/api/service/slam/v1#SensorInfo): Information about the sensors (camera and movement sensor) configured for your SLAM service, including the name and type of sensor.
- `CloudSlam` [(bool)](https://pkg.go.dev/builtin#bool): A boolean which indicates whether the session is being run in the cloud.
- `MappingMode` [(MappingMode)](https://pkg.go.dev/go.viam.com/rdk/services/slam#MappingMode): Represents the [form of mapping and localizing the current session is performing](/operate/reference/services/slam/cartographer/#using-cartographer). This includes creating a new map, localizing on an existing map and updating an existing map.
- `InternalStateFileType` [(string)](https://pkg.go.dev/builtin#string): The file type the service's internal state algorithm is stored in.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
// Get the properties of your current SLAM session
properties, err := mySLAMService.Properties(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `callOptions` (CallOptions) (optional)

**Returns:**

- (Promise<[slamApi](https://ts.viam.dev/modules/slamApi.html).[GetPropertiesResponse](https://ts.viam.dev/classes/slamApi.GetPropertiesResponse.html)>)

**Example:**

```ts {class="line-numbers linkable-line-numbers"}
const slam = new VIAM.SlamClient(machine, 'my_slam');

// Get the properties of the SLAM service
const properties = await slam.getProperties();
console.log('SLAM properties:', properties);
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SlamClient.html#getproperties).

{{% /tab %}}
{{< /tabs >}}

### InternalStateFull

`InternalStateFull` concatenates the streaming responses from `InternalState` into the internal serialized state of the SLAM algorithm.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `slamSvc` [(Service)](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service): The SLAM service name to fetch the internal state for.

**Returns:**

- [([]byte)](https://pkg.go.dev/builtin#byte): A byte value representing the internal serialized state of the SLAM algorithm.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#InternalStateFull).

{{% /tab %}}
{{< /tabs >}}

### PointCloudMapFull

`PointCloudMapFull` concatenates the streaming responses from `PointCloudMap` into a full point cloud.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `slamSvc` [(Service)](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service): The SLAM service name to fetch the point cloud map for.
- `returnEditedMap` [(bool)](https://pkg.go.dev/builtin#bool): A boolean representing whether to return the edited map (`true`) or not (`false`).

**Returns:**

- [([]byte)](https://pkg.go.dev/builtin#byte): The returned `PointCloudMap`.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#PointCloudMapFull).

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
Most models do not implement `DoCommand`.
Any available model-specific commands should be covered in the model's documentation.
If you are implementing your own SLAM service and want to add features that have no corresponding built-in API method, you can implement them with [`DoCommand`](/dev/reference/sdks/docommand/).

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `command` (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), ValueTypes]) (required): The command to execute.
- `timeout` ([float](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)) (optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (Mapping[[str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str), viam.utils.ValueTypes]): Result of the executed command.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_slam_svc = SLAMClient.from_robot(robot=machine, "my_slam_svc")

my_command = {
  "cmnd": "dosomething",
  "someparameter": 52
}

await my_slam_svc.do_command(command=my_command)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.do_command).

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
mySLAMService, err := slam.FromRobot(machine, "my_slam_svc")

command := map[string]interface{}{"cmd": "test", "data1": 500}
result, err := mySLAMService.DoCommand(context.Background(), command)
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

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SlamClient.html#docommand).

{{% /tab %}}
{{< /tabs >}}

### GetResourceName

Get the `ResourceName` for this instance of the SLAM service.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `name` ([str](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)) (required): The name of the Resource.

**Returns:**

- ([viam.proto.common.ResourceName](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName)): The ResourceName of this Resource.

**Example:**

```python {class="line-numbers linkable-line-numbers"}
my_slam_svc_name = SLAMClient.get_resource_name("my_slam_svc")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_resource_name).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None.

**Returns:**

- [(Name)](https://pkg.go.dev/go.viam.com/rdk@v0.89.0/resource#Name)

**Example:**

```go {class="line-numbers linkable-line-numbers"}
mySlamSvc, err := slam.FromRobot(machine, "my_slam_svc")

err = mySlamSvc.Name()
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
slam.name
```

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/SlamClient.html#name).

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
my_slam_svc = SLAMClient.from_robot(robot=machine, name="my_slam_svc")
await my_slam_svc.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

**Example:**

```go {class="line-numbers linkable-line-numbers"}
mySlamSvc, err := slam.FromRobot(machine, "my_slam_svc")

err = mySlamSvc.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
