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

## RobotClient

"this class should be used for all interactions with a robot"

## RobotService

"Helper class that provides a standard way to create an ABC using inheritance."

` type Robot interface `

### DiscoverComponents

Get a list of discovered component configurations.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `queries` [(List[viam.proto.robot.DiscoveryQuery])]():

**Returns:**

- [(List[viam.proto.robot.Discovery])]():

``` python
discover_components(queries: List[viam.proto.robot.DiscoveryQuery])→ List[viam.proto.robot.Discovery]
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(List[viam.proto.robot.Discovery])]():

```go
// DiscoverComponents returns discovered component configurations.
DiscoverComponents(ctx context.Context, qs []resource.DiscoveryQuery) ([]resource.Discovery, error)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```typescript
// Get the list of discovered component configurations.
discoverComponents(queries: DiscoveryQuery[]): Promise<Discovery[]>
```

[Typescript SDK](https://ts.viam.dev/classes/RobotClient.html)

{{% /tab %}}
{{< /tabs >}}

### ResourceNames

PYTHON: propertyresource_names: List[viam.proto.common.ResourceName]
GO: // ResourceNames returns a list of all known resource names.
    ResourceNames() []resource.Name

### OperationManager

GO: // OperationManager returns the operation manager the robot is using.
    OperationManager() *operation.Manager

PYTHON: ROBOT.CLIENT
async get_operations()→ List[viam.proto.robot.Operation]
async cancel_operation(id: str)
asyncblock_for_operation(id: str)

### SessionManager

GO: // SessionManager returns the session manager the robot is using.
    SessionManager() session.Manager

PYTHON ROBOT.SERVICE:
async GetSessions(stream: grpclib.server.Stream[viam.proto.robot.GetSessionsRequest, viam.proto.robot.GetSessionsResponse])→ None[source

asyncStartSession(stream: grpclib.server.Stream[viam.proto.robot.StartSessionRequest, viam.proto.robot.StartSessionResponse])→ None[

asyncSendSessionHeartbeat(stream: grpclib.server.Stream[viam.proto.robot.SendSessionHeartbeatRequest, viam.proto.robot.SendSessionHeartbeatResponse])→ None

### FrameSystemConfig

PYTHON: async get_frame_system_config(additional_transforms: Optional[List[viam.proto.common.Transform]] = None)→ List[viam.proto.robot.FrameSystemConfig][source]
GO: // FrameSystemConfig returns the individual parts that make up a robot's frame system
    FrameSystemConfig(ctx context.Context, additionalTransforms []*referenceframe.LinkInFrame) (framesystemparts.Parts, error)

### TransformPose

PYTHON: async transform_pose(query: viam.proto.common.PoseInFrame, destination: str, additional_transforms: Optional[List[viam.proto.common.Transform]] = None)→ viam.proto.common.PoseInFrame
GO: // TransformPose will transform the pose of the requested poseInFrame to the desired frame in the robot's frame system.
    TransformPose(
        ctx context.Context,
        pose *referenceframe.PoseInFrame,
        dst string,
        additionalTransforms []*referenceframe.LinkInFrame,
    ) (*referenceframe.PoseInFrame, error)

### TransformPointCloud

PYTHON: transform_point_cloud()
GO:
    // TransformPointCloud will transform the pointcloud to the desired frame in the robot's frame system.
    // Do not move the robot between the generation of the initial pointcloud and the receipt
    // of the transformed pointcloud because that will make the transformations inaccurate.
    TransformPointCloud(ctx context.Context, srcpc pointcloud.PointCloud, srcName, dstName string) (pointcloud.PointCloud, error)

### Status

PYTHON: get_status(components: Optional[List[viam.proto.common.ResourceName]] = None)

Get the status of the robot’s components. You can optionally provide a list of ResourceName for which you want statuses.

Parameters
: components (Optional[List[viam.proto.common.ResourceName]]) – Optional list of ResourceName for components you want statuses.

GO:
    // Status takes a list of resource names and returns their corresponding statuses. If no names are passed in, return all statuses.
    Status(ctx context.Context, resourceNames []resource.Name) ([]Status, error)

### Close

PYTHON: close() // Cleanly close the underlying connections and stop any periodic tasks
GO:
    // Close attempts to cleanly close down all constituent parts of the robot.
    Close(ctx context.Context) error

### StopAll

PYTHON: stop_all(extra: Dict[viam.proto.common.ResourceName, Dict[str, Any]] = {})
GO:
// StopAll cancels all current and outstanding operations for the robot and stops all actuators and movement
StopAll(ctx context.Context, extra map[resource.Name]map[string]interface{}) error

### RemoteByName

PYTHON: ?
GO: // RemoteByName returns a remote robot by name.
    RemoteByName(name string) (Robot, bool)

### ResourceByName

PYTHON: ?
GO: // ResourceByName returns a resource by name
    ResourceByName(name resource.Name) (resource.Resource, error)

### RemoteNames

PYTHON: ?
GO: // RemoteNames returns the names of all known remote robots.
    RemoteNames() []string

### PackageManager

PYTHON: ?
GO: // PackageManager returns the package manager the robot is using.
    PackageManager() packages.Manager

### Logger

PYTHON: ?
GO: // Logger returns the logger the robot is using.
    Logger() golog.Logger

### ResourceRPCAPIs

PYTHON: ?
GO: // ResourceRPCAPIs returns a list of all known resource RPC APIs.
    ResourceRPCAPIs() []resource.RPCAPI

### ProcessManager

PYTHON: ?
GO: // ProcessManager returns the process manager for the robot.
    ProcessManager() pexec.ProcessManager
