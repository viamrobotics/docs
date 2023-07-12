---
title: "SLAM Service"
linkTitle: "SLAM"
weight: 70
type: "docs"
description: "Simultaneous Localization And Mapping (SLAM) allows your robot to create a map of its surroundings and find its location within that map."
tags: ["slam", "services"]
icon: "/services/img/icons/slam.svg"
no_list: true
# SMEs: Kat, Jeremy
---

{{% alert title="Stability Notice" color="note" %}}
The SLAM Service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

[Simultaneous Localization And Mapping (SLAM)](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping) allows your robot to create a map of its surroundings and find its location within that map.
SLAM is an important area of ongoing research in robotics, particularly for mobile applications such as drones, boats, and rovers.

The Viam SLAM Service supports the integration of SLAM as a service on your robot.
You can conduct SLAM with data collected live by a [RPlidar](/extend/modular-resources/examples/rplidar/) or with LIDAR data you provide in configuration, and easily view the map you build on the **Control** tab of your robot's page in the [Viam app](https://app.viam.com):

![SLAM map built with Viam of a triangle shaped building.](img/run_slam/slam-map-example.png)

## Configuration

Integrated SLAM Libraries include:

| Model | Description |
| ----- | ----------- |
| [`viam:slam:cartographer`](cartographer/) | [The Cartographer Project](https://github.com/cartographer-project) performs dense SLAM using LIDAR data. |

## API

The SLAM Service supports the following methods:

Method Name | Description
----------- | -----------
[`GetPosition`](#getposition) | Get the current position of the specified component in the point cloud SLAM map.
[`GetPointCloudMap`](#getpointcloudmap) | Get the point cloud SLAM map.
[`GetInternalState`](#getinternalstate) | Get the internal state of the SLAM algorithm required to continue mapping/localization.
[`GetLatestMapInfo`](#getlatestmapinfo) | Get the timestamp of the last update to the point cloud SLAM map.

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured with a SLAM Service called `"my_slam_service"`, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### GetPosition

Get the current position of the specified component in the SLAM map.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk@v0.3.0/spatialmath#Pose): A `Pose` representing the current position of the specified component.
- [(string)](https://pkg.go.dev/builtin#string): The `"name"` of the SLAM service.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam).

```go {class="line-numbers linkable-line-numbers"}
slam_svc, err := slam.FromRobot(robot, "my_slam_service")

// Get the current position of the specified component in the SLAM map as a Pose.
pos, name, err := slam_svc.GetPosition(context.Background())
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Pose)](https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Pose): A `Pose` representing the current position of the specified component.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_position).

```python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the current position of the specified component in the SLAM map as a Pose.
pose = await slam.get_position()
```

{{% /tab %}}
{{< /tabs >}}

### GetPointCloudMap

Get the point cloud map.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/datamanager).

```go {class="line-numbers linkable-line-numbers"}
slam_svc, err := slam.FromRobot(robot, "my_slam_service")

// Get the point cloud map.
err := slam_svc.GetPointCloudMap(context.Background())
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[GetPointCloudMapResponse])](https://python.viam.dev/autoapi/viam/gen/service/slam/v1/slam_pb2/index.html#viam.gen.service.slam.v1.slam_pb2.GetPointCloudMapResponse): Complete pointcloud in standard PCD format.
Chunks of the PointCloud, concatenating all GetPointCloudMapResponse.point_cloud_pcd_chunk values.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_position).

```python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the point cloud map
internal_state = await slam.get_point_cloud_map()
```

{{% /tab %}}
{{< /tabs >}}

### GetInternalState

Get the internal state of the SLAM algorithm required to continue mapping/localization.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [([]byte)](https://pkg.go.dev/builtin#byte):
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/datamanager).

```go {class="line-numbers linkable-line-numbers"}
slam_svc, err := slam.FromRobot(robot, "my_slam_service")

// Get the internal state of the SLAM algorithm required to continue mapping/localization.
internal_state, err := slam_svc.GetInternalState(context.Background())
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `extra` [(Optional\[Dict\[str, Any\]\])](https://docs.python.org/library/typing.html#typing.Optional): Extra options to pass to the underlying RPC call.

**Returns:**

- (List[[ResourceName](https://python.viam.dev/autoapi/viam/gen/common/v1/common_pb2/index.html#viam.gen.common.v1.common_pb2.ResourceName)]): Names of the available sensors of the robot.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/index.html#viam.services.slam.SLAMClient.get_internal_state).

```python {class="line-numbers linkable-line-numbers"}
slam = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the internal state of the SLAM algorithm required to continue mapping/localization.
internal_state = await slam.get_internal_state()
```

{{% /tab %}}
{{< /tabs >}}

### GetLatestMapInfo

{{% alert title="Important" color="tip" %}}

This method is not yet available in the Viam Python SDK.

{{% /alert %}}

Get the timestamp of the last update to the point cloud SLAM map.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `extra` [(map\[string\]interface{})](https://go.dev/blog/maps): Extra options to pass to the underlying RPC call.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/datamanager).

```go {class="line-numbers linkable-line-numbers"}
slam_svc, err := slam.FromRobot(robot, "my_slam_service")

// Get the timestamp of the last update to the point cloud SLAM map.
err := slam_svc.GetLatestMapInfo(context.Background())
```

{{% /tab %}}
{{< /tabs >}}