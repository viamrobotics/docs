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
This page documents how to use the methods the `RobotClient` provides for the Robot API across Viam's SDKs.

## DiscoverComponents

Get a list of discovered component configurations.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `queries` [(List [viam.proto.robot.DiscoveryQuery])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery): List of tuples of API and model used to look up discovery functions.

**Returns:**

- [(List[viam.proto.robot.Discovery])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.Discovery): List of discovered component configurations.

``` python
component_configs = await robot.discover_components(queries)
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `qs` [([]resource.DiscoveryQuery)](https://pkg.go.dev/go.viam.com/rdk@v0.2.46/resource#DiscoveryQuery): A tuple of API and model used to look up discovery functions.

**Returns:**

- [([]resource.Discovery)](https://pkg.go.dev/go.viam.com/rdk@v0.2.46/resource#Discovery): The search `Query` (`qs`) and the list of discovered component configurations as an interface called `Results`.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go
// TODO: setting this up will be a little bit difficult: see https://github.com/search?q=repo%3Aviamrobotics%2Frdk%20DiscoveryQuery&type=code
// DiscoverComponents returns discovered component configurations.
component_configs, err := robot.DiscoverComponents(ctx.Background(), qs)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `queries` [(DiscoveryQuery[])](https://ts.viam.dev/classes/robotApi.DiscoveryQuery.html): List of tuples of API and model used to look up discovery functions.

**Returns:**

- [(Discovery[])](https://ts.viam.dev/classes/robotApi.Discovery.html): List of discovered component configurations.

```typescript
// Get the list of discovered component configurations.
const componentConfigs = await robot.discoverComponents(queries)
```

[Typescript SDK](https://ts.viam.dev/classes/RobotClient.html)

{{% /tab %}}
{{< /tabs >}}

## FrameSystemConfig

Get the configuration of the Frame System of a given robot.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `additional_transforms` [(Optional[List[viam.proto.common.Transform]])](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform): A list of [additional transforms](/services/frame-system/#additional-transforms).

**Returns:**

- `frame_system` [(List[FrameSystemConfig])](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.FrameSystemConfig): The configuration of a given robot’s frame system.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_frame_system_config).

```python {class="line-numbers linkable-line-numbers"}
# Get a list of each of the reference frames configured on the robot.
frame_system = await robot.get_frame_system_config()
print(f"Frame System Configuration: {frame_system}")
```

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

- `transforms` [(Transform[])](https://ts.viam.dev/classes/commonApi.Transform.html): A list of [additional transforms](/services/frame-system/#additional-transforms).

**Returns:**

- [(FrameSystemConfig[])](https://ts.viam.dev/classes/robotApi.FrameSystemConfig.html): The individual parts that make up a robot's frame system.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```typescript {class="line-numbers linkable-line-numbers"}
// Get the Frame System configuration
const frameSystemConfig = await robot.frameSystemConfig(transforms)
```

{{% /tab %}}
{{< /tabs >}}

## Status

Get the status of the robot’s components. You can optionally provide a list of ResourceNames for which you want statuses.
If no names are passed in, return all statuses.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `resourceNames` [(Optional[List[viam.proto.common.ResourceName]])](https://docs.python.org/library/typing.html#typing.Optional): An optional list of ResourceNames for components you want the status of.
If no names are passed in, all resource statuses are returned.

**Returns:**

- [(List[str])](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): Status of each resource.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_status).

```python {class="line-numbers linkable-line-numbers"}
# Get the status of the resources on the robot.
statuses = await robot.get_status()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `resourceNames` [([]resource.Name)](): An optional list of ResourceNames for components you want the status of.
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

- `resourceNames` [(commonApi.ResourceName[])](https://ts.viam.dev/classes/commonApi.ResourceName.html): An optional list of ResourceNames for components you want the status of. If no names are passed in, all resource statuses are returned.

**Returns:**

- [(robotApi.Status[])](https://ts.viam.dev/classes/robotApi.Status.html): Status of each resource.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#transformPCD).

```typescript {class="line-numbers linkable-line-numbers"}
// Get the status of the resources on the robot.
const status = await robot.getStatus()
```

{{% /tab %}}
{{< /tabs >}}

<!-- ## Close

PYTHON: close() // Cleanly close the underlying connections and stop any periodic tasks
GO:
    // Close attempts to cleanly close down all constituent parts of the robot.
    Close(ctx context.Context) error -->

## GetOperations

Get the Operation associated with the currently running function.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `kwargs` [(Mapping[str,Any])](https://docs.python.org/3/glossary.html#term-mapping): The kwargs object containing the operation.

**Returns:**

- [(operations.Operation)](https://python.viam.dev/autoapi/viam/operations/index.html#viam.operations.Operation): The operation associated with the currently running function.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/resource/base/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

 - not in there

{{% /tab %}}
{{% tab name="TypeScript" %}}

For more information, see the [Typescript SDK Docs](https://ts.viam.dev/classes/RobotClient.html).

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
await robot.stopAll()
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

[Go SDK](https://pkg.go.dev/go.viam.com/rdk/robot#Robot)

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- [(ResourceName.AsObject[])](https://ts.viam.dev/modules/commonApi.ResourceName-1.html): List of all known resource names.s

```typescript
// Get a list of all resources on the robot.
const resource_names = await robot.resourceNames()
```

[Typescript SDK](https://ts.viam.dev/classes/RobotClient.html)

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
const transformed_pcd = await robot.transformPCD(source_pointcloud, "source_frame", "destination_frame")
```

{{% /tab %}}
{{< /tabs >}}
