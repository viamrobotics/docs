---
title: "Robot API Methods with Viam's SDKs"
linkTitle: "For the Robot"
weight: 20
type: "docs"
description: "Using the built-in Robot API methods with Viam's SDKs."
icon: "/services/img/icons/sdk.svg"
tags: ["sdk"]
---

The Robot API is the designated interface for a robot, the root of all robotic parts.

To interact with the Robot API with Viam's SDKs, instantiate a `RobotClient` ([gRPC](https://grpc.io/) client) and use that class for all interactions.

## DiscoverComponents

Get a list of discovered component configurations.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `queries` [(List [viam.proto.robot.DiscoveryQuery])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery): A list of [tuples of API and model](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [(List[viam.proto.robot.Discovery])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.Discovery): The list of discovered component configurations corresponding to `queries`.

``` python
# Define a new discovery query.
q = robot.DiscoveryQuery(subtype=acme.API, model="some model")

# Define a list of discovery queries.
qs = [q]

# Get component configurations with these queries.
component_configs = await robot.discover_components(qs)
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.discover_components)

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `qs` [([]resource.DiscoveryQuery)](https://pkg.go.dev/go.viam.com/rdk@v0.2.46/resource#DiscoveryQuery): A list of [tuples of API and model](https://pkg.go.dev/go.viam.com/rdk/resource#DiscoveryQuery) that you want to retrieve the component configurations corresponding to.

**Returns:**

- [([]resource.Discovery)](https://pkg.go.dev/go.viam.com/rdk@v0.2.46/resource#Discovery): The search query `qs` and the corresponding list of discovered component configurations as an interface called `Results`.
`Results` may be comprised of primitives, a list of primitives, maps with string keys (or at least can be decomposed into one), or lists of the forementioned type of maps.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
// Define a new discovery query.
q := resource.NewDiscoveryQuery(acme.API, resource.Model{Name: "some model"})

// Define a list of discovery queries.
qs := []resource.DiscoverQuery{q}

// Get component configurations with these queries.
component_configs, err := robot.DiscoverComponents(ctx.Background(), qs)
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
const componentConfigs = await robot.discoverComponents(queries);
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/classes/RobotClient.html).

{{% /tab %}}
{{< /tabs >}}

## FrameSystemConfig

Get the configuration of the Frame System of a given robot.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `additional_transforms` [(Optional[List[viam.proto.common.Transform]])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform): A optional list of [additional transforms](/services/frame-system/#additional-transforms).

**Returns:**

- `frame_system` [(List[FrameSystemConfig])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.FrameSystemConfig): The configuration of a given robot’s frame system.

```python {class="line-numbers linkable-line-numbers"}
# Get a list of each of the reference frames configured on the robot.
frame_system = await robot.get_frame_system_config()
print(f"Frame System Configuration: {frame_system}")
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_frame_system_config).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- [(framesystem.Config)](https://pkg.go.dev/go.viam.com/rdk/robot/framesystem#Config): The configuration of the given robot’s frame system.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Print the Frame System configuration
frameSystem, err := robot.FrameSystemConfig(context.Background(), nil)
fmt.Println(frameSystem)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `transforms` [(Transform[])](https://ts.viam.dev/classes/commonApi.Transform.html): An optional array of [additional transforms](/services/frame-system/#additional-transforms).

**Returns:**

- [(FrameSystemConfig[])](https://ts.viam.dev/classes/robotApi.FrameSystemConfig.html): An array of individual parts that make up a robot's frame system.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#frameSystemConfig).

```typescript {class="line-numbers linkable-line-numbers"}
// Get the Frame System configuration.
console.log('FrameSytemConfig:', await robot.frameSystemConfig());
```

{{% /tab %}}
{{< /tabs >}}

## Status

Get the status of the resources on the robot.
You can provide a list of ResourceNames for which you want statuses.
If no names are passed in, the status of every resource configured on the robot is returned.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `resourceNames` [(Optional[List[viam.proto.common.ResourceName]])](https://docs.python.org/library/typing.html#typing.Optional): An optional list of ResourceNames for components you want the status of.
If no names are passed in, all resource statuses are returned.

**Returns:**

- [(List[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): A list containing the status of each resource.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_status).

```python {class="line-numbers linkable-line-numbers"}
# Get the status of the resources on the robot.
statuses = await robot.get_status()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `resourceNames` [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk/resource#Name): An optional list of ResourceNames for components you want the status of.
If no names are passed in, all resource statuses are returned.

**Returns:**

- [([]Status)](): Status of each resource.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Get the status of the resources on the robot.
status, err = robot.Status(ctx.Background())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `resourceNames` [(commonApi.ResourceName[])](https://ts.viam.dev/classes/commonApi.ResourceName.html): An optional array of ResourceNames for components you want the status of.
If no names are passed in, all resource statuses are returned.

**Returns:**

- [(robotApi.Status[])](https://ts.viam.dev/classes/robotApi.Status.html): An array containing the status of each resource.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#transformPCD).

```typescript {class="line-numbers linkable-line-numbers"}
// Get the status of the resources on the robot.
const status = await robot.getStatus();
```

{{% /tab %}}
{{< /tabs >}}

## Close

Close the underlying connections and stop any periodic tasks across all constituent parts of the robot.
{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [Python SDK Docs]()).

```python {class="line-numbers linkable-line-numbers"}
# Cleanly close the underlying connections and stop any periodic tasks.
await robot.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Cleanly close the underlying connections and stop any periodic tasks,
err := robot.Close(ctx.Background())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#disconnect).

```typescript {class="line-numbers linkable-line-numbers"}
// Cleanly close the underlying connections and stop any periodic tasks
await robot.disconnect();
```

{{% /tab %}}
{{< /tabs >}}

## StopAll

Cancel all current and outstanding operations for the robot and stop all actuators and movement.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Dict[viam.proto.common.ResourceName, Dict[str, Any]])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName): Any extra parameters to pass to the resources’ stop methods, keyed on each resource’s [`ResourceName`](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName).

**Returns:**

- None

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.stop_all).

```python {class="line-numbers linkable-line-numbers"}
# Cancel all current and outstanding operations for the robot and stop all actuators and movement.
await robot.stop_all()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map[resource.Name]map[string]interface{})](https://pkg.go.dev/go.viam.com/rdk/resource#Name): Any extra parameters to pass to the resources’ stop methods, keyed on each resource’s [`Name`](https://pkg.go.dev/go.viam.com/rdk/resource#Name).

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the robot and stop all actuators and movement.
err := robot.StopAll(ctx.Background())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- None

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#stopAll).

```typescript {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the robot and stop all actuators and movement.
await robot.stopAll();
```

{{% /tab %}}
{{< /tabs >}}

## ResourceNames

Get a list of all known resource names connected to this robot.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(List[viam.proto.common.ResourceName])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.ResourceName): List of all known resource names. A property of a [RobotClient](https://python.viam.dev/autoapi/viam/robot/client/index.html)

``` python
resource_names = robot.resource_names
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- [([]resource.Name)](https://pkg.go.dev/go.viam.com/rdk@v0.2.47/resource#Name): List of all known resource names.

```go
resource_names = robot.ResourceNames()
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- [(ResourceName.AsObject[])](https://ts.viam.dev/modules/commonApi.ResourceName-1.html): List of all known resource names.

```typescript
// Get a list of all resources on the robot.
const resource_names = await robot.resourceNames();
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/classes/RobotClient.html).

{{% /tab %}}
{{< /tabs >}}

## ResourceByName

{{% alert title="Note" color="note" %}}
This method is not implemented with the Viam Python or TypeScript SDKs.
{{% /alert %}}

Get a resource by [`resource.Name`](https://pkg.go.dev/go.viam.com/rdk@v0.2.48/resource#Name).

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk@v0.2.48/resource#Name): Struct representing a resource's ID, with API triplet, remote address, and resource name fields.

**Returns:**

- [(resource.Resource)](https://pkg.go.dev/go.viam.com/rdk@v0.2.48/resource#Resource): The desired resource.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the robot and stop all actuators and movement.
err := robot.StopAll(ctx.Background())
```

{{% /tab %}}
{{< /tabs >}}

## RemoteByName

{{% alert title="Note" color="note" %}}
This method is not implemented with the Viam Python or TypeScript SDKs.
{{% /alert %}}

Get a remote robot by name.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(string)](https://pkg.go.dev/builtin#string): The name of the remote robot.

**Returns:**

- [(Robot)](https://pkg.go.dev/go.viam.com/rdk/robot#Robot): The remote robot with this `name`.
- [(bool)](https://pkg.go.dev/builtin#bool): If a remote robot was found with this name.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the robot and stop all actuators and movement.
robot2, ok := robot.RemoteByName("my-robot-remote")
```

For more information, see the[Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

{{% /tab %}}
{{< /tabs >}}

## RemoteNames

{{% alert title="Note" color="note" %}}
This method is not implemented with the Viam Python or TypeScript SDKs.
{{% /alert %}}

Get a resource by [`resource.Name`](https://pkg.go.dev/go.viam.com/rdk@v0.2.48/resource#Name).

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `name` [(resource.Name)](https://pkg.go.dev/go.viam.com/rdk@v0.2.48/resource#Name): Struct representing a resource's ID, with API triplet, remote address, and resource name fields.

**Returns:**

- [(resource.Resource)](https://pkg.go.dev/go.viam.com/rdk@v0.2.48/resource#Resource): The desired resource.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Cancel all current and outstanding operations for the robot and stop all actuators and movement.
err := robot.StopAll(ctx.Background())
```

{{% /tab %}}
{{< /tabs >}}

## TransformPose

Transform a given source pose from the reference frame to a new specified destination reference frame.
For example, if a 3D camera observes a point in space you can use this method to calculate where that point is relative to another object.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `query` [(`PoseInFrame`)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame): The pose that should be transformed.
- `destination` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The name of the reference frame to transform the given pose to.
- `additional_transforms` [Optional[List[Transform]]](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform): A list of [additional transforms](/components/frame-service/#additional-transforms).

**Returns:**

- [(PoseInFrame)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame): Transformed pose in destination reference frame.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.transform_pose).

```python {class="line-numbers linkable-line-numbers"}
# Transform a pose into the frame of myArm
first_pose = Pose(x=0.0, y=0.0, z=0.0, o_x=0.0, o_y=0.0, o_z=1.0, theta=0.0)
first_pif = PoseInFrame(reference_frame="world", pose=first_pose)
transformed_pif = await robot.transform_pose(first_pif, "myArm")
print("Position: (x:", transformed_pif.pose.x, ", y:", transformed_pif.pose.y, ", z:", transformed_pif.pose.z, ")")
print("Orientation: (o_x:", transformed_pif.pose.o_x,
      ", o_y:", transformed_pif.pose.o_y,
      ", o_z:",transformed_pif.pose.o_z,
      ", theta:", transformed_pif.pose.theta, ")")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `pose` [(PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): The pose that should be transformed.
- `dst` [(string)](https://pkg.go.dev/builtin#string): The name of the reference frame to transform the given pose to.
- `additionalTransforms` [(Optional[LinkInFrame])]((https://pkg.go.dev/go.viam.com/rdk/referenceframe#LinkInFrame)): A list of [additional transforms](/components/frame-service/#additional-transforms).

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- [(referenceframe.PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): Transformed pose in destination reference frame.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot).

```go {class="line-numbers linkable-line-numbers"}
// Define a Pose coincident with the world reference frame
firstPose := spatialmath.NewPoseFromPoint(r3.Vector{X: 0.0, Y: 0.0, Z: 0.0})

// Establish the world as the reference for firstPose
firstPoseInFrame := referenceframe.NewPoseInFrame(referenceframe.World, firstPose)

// Calculate firstPoseInFrame from the perspective of the origin frame of myArm
transformedPoseInFrame, err := robot.TransformPose(ctx, firstPoseInFrame, "myArm", nil)
fmt.Println("Transformed Position:", transformedPoseInFrame.Pose().Point())
fmt.Println("Transformed Orientation:", transformedPoseInFrame.Pose().Orientation())
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `source` [(commonApi.PoseInFrame)](https://ts.viam.dev/classes/RobotClient.html#transformPose): The pose that should be transformed.
- `destination` [(string)](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html): The name of the reference frame to transform the given pose to.
- `supplementalTransforms` [(commonApi.Transform[])](https://ts.viam.dev/classes/commonApi.Transform.html): A list of [additional transforms](/components/frame-service/#additional-transforms).

**Returns:**

- [(PoseInFrame)](https://ts.viam.dev/classes/commonApi.PoseInFrame.html): Transformed pose in destination reference frame.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#transformPose).

```typescript {class="line-numbers linkable-line-numbers"}
const transformedPoseInFrame = await robot.transformPose(transforms)
```

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/classes/RobotClient.html).

{{% /tab %}}
{{< /tabs >}}

## TransformPointCloud

Transform the pointcloud to the desired frame in the robot's Frame System.

{{% alert title="Note" color="note" %}}
This method is not implemented with the Viam Python SDK.
{{% /alert %}}

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `srcpc` [(PointCloud)](https://pkg.go.dev/go.viam.com/rdk@v0.2.46/pointcloud#PointCloud): The pointcloud to transformed.
- `srcName` [(string)](https://pkg.go.dev/builtin#string): The name of the source pointcloud's parent reference frame.
- `dstName` [(string)](https://pkg.go.dev/builtin#string): The name of the reference frame to transform the source pointcloud to.

**Returns:**

- [(PointCloud)](https://pkg.go.dev/go.viam.com/rdk@v0.2.46/pointcloud#PointCloud): Transformed pointcloud in destination reference frame.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot#Robot).

```go {class="line-numbers linkable-line-numbers"}
// Transform the pointcloud to the desired frame in the robot's Frame System.
transformed_pcd, err = robot.TransformPointCloud(ctx.Background(), source_pointcloud, "source_frame", "destination_frame")
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `pointCloudPCD` [(Uint8Array)](https://microsoft.github.io/PowerBI-JavaScript/interfaces/_node_modules_typedoc_node_modules_typescript_lib_lib_es5_d_.uint8array.html): The pointcloud to transform.
Should be in the [PCD format encoded into bytes](https://pointclouds.org/documentation/tutorials/pcd_file_format.html).
- `source` [(string)](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html): The name of the reference frame of `pointCloudPCD`.
- `destination` [(string)](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html): The name of the reference frame to transform `pointCloudPCD` to.
- `supplementalTransforms` [(commonApi.Transform[])](https://ts.viam.dev/classes/commonApi.Transform.html): A list of [additional transforms](/components/frame-service/#additional-transforms).

**Returns:**

- [(Uint8Array)](https://microsoft.github.io/PowerBI-JavaScript/interfaces/_node_modules_typedoc_node_modules_typescript_lib_lib_es5_d_.uint8array.html): Transformed pose in destination reference frame.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#transformPCD).

```typescript {class="line-numbers linkable-line-numbers"}
// Transform the pointcloud to the desired frame in the robot's Frame System.
const transformed_pcd = await robot.transformPCD(source_pointcloud, "source_frame", "destination_frame");
```

{{% /tab %}}
{{< /tabs >}}
