---
title: "Using the Robot API Methods with Viam's SDKs"
linkTitle: "The Robot API"
weight: 20
type: "docs"
description: "Using the built-in Robot API methods with Viam's SDKs."
icon: "/services/img/icons/sdk.svg"
tags: ["sdk"]
---

Introduction --> why does this exist and why would you directly call this class?
Instantiation in Code Sample
What Is a "RobotClient"

## DiscoverComponents

Get a list of discovered component configurations.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `queries` (List [viam.proto.robot.DiscoveryQuery](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.DiscoveryQuery)): List of tuples of API and model used to look up discovery functions.

**Returns:**

- (List [viam.proto.robot.Discovery](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.Discovery)): List of discovered component configurations.

``` python
discover_components(queries: List[viam.proto.robot.DiscoveryQuery])→ List[viam.proto.robot.Discovery]
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
robot.DiscoverComponents(ctx.Background, qs)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `queries` [(DiscoveryQuery[])](https://ts.viam.dev/classes/robotApi.DiscoveryQuery.html): List of tuples of API and model used to look up discovery functions.

**Returns:**

- [(Discovery[])](https://ts.viam.dev/classes/robotApi.Discovery.html): List of discovered component configurations.

```typescript
// Get the list of discovered component configurations.
discoverComponents(queries: DiscoveryQuery[]): Promise<Discovery[]>
```

[Typescript SDK](https://ts.viam.dev/classes/RobotClient.html)

{{% /tab %}}
{{< /tabs >}}

## ResourceNames

Get a list of all known resource names.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(List[viam.proto.common.ResourceName])]():

``` python
property resource_names: List[viam.proto.common.ResourceName]
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- [([]resource.Name)]():

```go
// ResourceNames returns a list of all known resource names.
ResourceNames() []resource.Name
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- [(Promise<commonApi.ResourceName.AsObject[]>)]():

```typescript
// Get a list of all resources on the robot.
resourceNames(): Promise<commonApi.ResourceName.AsObject[]>
```

[Typescript SDK](https://ts.viam.dev/classes/RobotClient.html)

{{% /tab %}}
{{< /tabs >}}

## FrameSystemConfig

 returns the individual parts that make up a robot's frame system.
 TODO: this WAS documented in the Frame System API but is not at the moment, figure out the state on this!

Returns a topologically sorted list of all the reference frames monitored by the frame system. Any [additional transforms](/service/frame-system/#additional-transforms) are also merged into the tree, sorted, and returned.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `additional_transforms` (Optional[List[[viam.proto.common.Transform](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)]]): A list of [additional transforms](#additional-transforms).

**Returns:**

- `frame_system` (List[[viam.proto.robot.FrameSystemConfig](https://python.viam.dev/autoapi/viam/proto/robot/index.html#viam.proto.robot.FrameSystemConfig)]): The configuration of a given robot’s frame system.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/robot/client/index.html#viam.robot.client.RobotClient.get_frame_system_config).

```python {class="line-numbers linkable-line-numbers"}
# Get a list of each of the reference frames configured on the robot.
frame_system = await robot.get_frame_system_config()
print(f"Frame System Configuration: {frame_system}")
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(`Context`)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `additionalTransforms` (Optional[[referenceframe.LinkInFrame](https://pkg.go.dev/go.viam.com/rdk/referenceframe#LinkInFrame)]): A list of [additional transforms](#additional-transforms).

**Returns:**

- `error` [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- `framesystemparts` [(`framesystemparts.Parts`)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): The individual parts that make up a robot's frame system.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```go {class="line-numbers linkable-line-numbers"}
// Print the Frame System configuration
frameSystem, err := robot.FrameSystemConfig(context.Background(), nil)
fmt.Println(frameSystem)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `transforms` [(commonApi.Transform[])](https://ts.viam.dev/classes/commonApi.Transform.html): A list of [additional transforms](/services/frame-system/#additional-transforms).

**Returns:**

- [(Promise<FrameSystemConfig[]>)](https://ts.viam.dev/classes/robotApi.FrameSystemConfig.html): The individual parts that make up a robot's frame system.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/components/arm#Arm).

```typescript {class="line-numbers linkable-line-numbers"}
// Print the Frame System configuration
frameSystem = robot.frameSystemConfig(transforms)
// fmt.Println(frameSystem)
```

{{% /tab %}}
{{< /tabs >}}

## TransformPose

THIS IS IN THE FRAME SYSTEM API CURRENTLY!

Transform a given source pose from the reference frame to a new specified destination reference frame.
For example, if a 3D camera observes a point in space you can use this method to calculate where that point is relative to another object.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `query` [(`PoseInFrame`)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame): The pose that should be transformed.
- `destination` (str): The name of the reference frame to transform the given pose to.
- `additional_transforms` (Optional[List[[Transform](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.Transform)]]): A list of [additional transforms](/components/frame-service/#additional-transforms).

**Returns:**

- `PoseInFrame` [(PoseInFrame)](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.PoseInFrame): Transformed pose in destination reference frame.

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

- `ctx` [(`Context`)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `pose` [(`PoseInFrame`)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): The pose that should be transformed.
- `dst` [`string`](): The name of the reference frame to transform the given pose to.
- `additionalTransforms` (Optional[[LinkInFrame](https://pkg.go.dev/go.viam.com/rdk/referenceframe#LinkInFrame)]): A list of [additional transforms](/components/frame-service/#additional-transforms).

**Returns:**

- `error` [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- `PoseInFrame` [(referenceframe.PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): Transformed pose in destination reference frame.

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
- `destination` [(string)](): The name of the reference frame to transform the given pose to.
- `supplementalTransforms` [(commonApi.Transform[])](https://ts.viam.dev/classes/commonApi.Transform.html): A list of [additional transforms](/components/frame-service/#additional-transforms).

**Returns:**

- [(Promise<commonApi.PoseInFrame>)](https://ts.viam.dev/classes/commonApi.PoseInFrame.html): Transformed pose in destination reference frame.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#transformPose).

```typescript {class="line-numbers linkable-line-numbers"}
// TODO: Write this out properly
frameSystem = robot.transformPose(transforms)

```

{{% /tab %}}
{{< /tabs >}}

## TransformPointCloud

Transform the pointcloud to the desired frame in the robot's Frame System.

PYTHON: transform_point_cloud()
GO:
    // TransformPointCloud will transform the pointcloud to the desired frame in the robot's frame system.
    // Do not move the robot between the generation of the initial pointcloud and the receipt
    // of the transformed pointcloud because that will make the transformations inaccurate.
    TransformPointCloud(ctx context.Context, srcpc pointcloud.PointCloud, srcName, dstName string) (pointcloud.PointCloud, error)

{{< tabs >}}
{{% tab name="Python" %}}

raise NotImplementedError()

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(`Context`)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `srcpc` [(`PointCloud`)](https://pkg.go.dev/go.viam.com/rdk@v0.2.46/pointcloud#PointCloud): The pointcloud that should be transformed.
- `srcName` (string): The name of the source pointcloud's parent reference frame.
- `dstName` (string): The name of the reference frame to transform the source pointcloud to.

**Returns:**

- `error` [(`error`)](https://pkg.go.dev/builtin#error): An error, if one occurred.
- `PoseInFrame` [(referenceframe.PoseInFrame)](https://pkg.go.dev/go.viam.com/rdk/referenceframe#PoseInFrame): Transformed pose in destination reference frame.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/robot).

```go {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- `source` [(commonApi.PoseInFrame)](https://ts.viam.dev/classes/RobotClient.html#transformPose): The pose that should be transformed.
- `destination` [(string)](): The name of the reference frame to transform the given pose to.
- `supplementalTransforms` [(commonApi.Transform[])](https://ts.viam.dev/classes/commonApi.Transform.html): A list of [additional transforms](/components/frame-service/#additional-transforms).

**Returns:**

- [(commonApi.PoseInFrame)](https://ts.viam.dev/classes/commonApi.PoseInFrame.html): Transformed pose in destination reference frame.

For more information, see the [TypeScript SDK Docs](https://ts.viam.dev/classes/RobotClient.html#transformPose).

```typescript {class="line-numbers linkable-line-numbers"}

```

{{% /tab %}}
{{< /tabs >}}

## Status

PYTHON: get_status(components: Optional[List[viam.proto.common.ResourceName]] = None)

Get the status of the robot’s components. You can optionally provide a list of ResourceName for which you want statuses.

Parameters
: components (Optional[List[viam.proto.common.ResourceName]]) – Optional list of ResourceName for components you want statuses.

GO:
    // Status takes a list of resource names and returns their corresponding statuses. If no names are passed in, return all statuses.
    Status(ctx context.Context, resourceNames []resource.Name) ([]Status, error)

## Close

PYTHON: close() // Cleanly close the underlying connections and stop any periodic tasks
GO:
    // Close attempts to cleanly close down all constituent parts of the robot.
    Close(ctx context.Context) error

## StopAll

PYTHON: stop_all(extra: Dict[viam.proto.common.ResourceName, Dict[str, Any]] = {})
GO:
// StopAll cancels all current and outstanding operations for the robot and stops all actuators and movement
StopAll(ctx context.Context, extra map[resource.Name]map[string]interface{}) error

## RemoteByName

PYTHON: ?
GO: // RemoteByName returns a remote robot by name.
    RemoteByName(name string) (Robot, bool)

## ResourceByName

PYTHON: ?
GO: // ResourceByName returns a resource by name
    ResourceByName(name resource.Name) (resource.Resource, error)

## RemoteNames

PYTHON: ?
GO: // RemoteNames returns the names of all known remote robots.
    RemoteNames() []string

## PackageManager

PYTHON: ?
GO: // PackageManager returns the package manager the robot is using.
    PackageManager() packages.Manager

## Logger

PYTHON: ?
GO: // Logger returns the logger the robot is using.
    Logger() golog.Logger

## ResourceRPCAPIs

PYTHON: ?
GO: // ResourceRPCAPIs returns a list of all known resource RPC APIs.
    ResourceRPCAPIs() []resource.RPCAPI

## ProcessManager

PYTHON: ?
GO: // ProcessManager returns the process manager for the robot.
    ProcessManager() pexec.ProcessManager

## OperationManager

GO: // OperationManager returns the operation manager the robot is using.
    OperationManager() *operation.Manager

PYTHON: ROBOT.CLIENT
async get_operations()→ List[viam.proto.robot.Operation]
async cancel_operation(id: str)
async block_for_operation(id: str)

TS:
getOperations(): Promise<Operation[]>
cancelOperation(id: string): Promise<void>
blockForOperation(id: string): Promise<void>

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- [(List[viam.proto.common.ResourceName])]():

``` python
property resource_names: List[viam.proto.common.ResourceName]
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- None

**Returns:**

- [([]resource.Name)]():

```go
// ResourceNames returns a list of all known resource names.
ResourceNames() []resource.Name
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

**Parameters:**

- None

**Returns:**

- [(commonApi.ResourceName.AsObject[])]():

```typescript
// Get a list of all resources on the robot.
resourceNames(): Promise<commonApi.ResourceName.AsObject[]>
```

[Typescript SDK](https://ts.viam.dev/classes/RobotClient.html)

{{% /tab %}}
{{< /tabs >}}

## SessionManager

GO: // SessionManager returns the session manager the robot is using.
    SessionManager() session.Manager

PYTHON ROBOT.SERVICE:
async GetSessions(stream: grpclib.server.Stream[viam.proto.robot.GetSessionsRequest, viam.proto.robot.GetSessionsResponse])→ None[source

asyncStartSession(stream: grpclib.server.Stream[viam.proto.robot.StartSessionRequest, viam.proto.robot.StartSessionResponse])→ None[

asyncSendSessionHeartbeat(stream: grpclib.server.Stream[viam.proto.robot.SendSessionHeartbeatRequest, viam.proto.robot.SendSessionHeartbeatResponse])→ None