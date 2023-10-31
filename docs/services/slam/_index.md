---
title: "SLAM Service"
linkTitle: "SLAM"
weight: 70
type: "docs"
description: "Simultaneous Localization And Mapping (SLAM) allows your robot to create a map of its surroundings and find its location within that map."
tags: ["slam", "services"]
icon: "/services/icons/slam.svg"
no_list: true
# SMEs: Kat, Jeremy
---

{{% alert title="Stability Notice" color="note" %}}
The SLAM service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

[Simultaneous Localization And Mapping (SLAM)](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping) allows your robot to create a map of its surroundings and find its location within that map.
SLAM is an important area of ongoing research in robotics, particularly for mobile applications such as drones, boats, and rovers.

The Viam SLAM service supports the integration of SLAM as a service on your robot.
You can conduct SLAM with data collected live by a [RPlidar](/modular-resources/examples/rplidar/) or with LIDAR data you provide in configuration, and easily view the map you build on the **Control** tab of your robot's page in the [Viam app](https://app.viam.com):

![SLAM map built with Viam of a triangle shaped building.](/services/slam/slam-map-example.png)

## Configuration

Integrated SLAM libraries include the following.
Click the model name for configuration instructions.

<!-- prettier-ignore -->
| Model | Description |
| ----- | ----------- |
| [`viam:slam:cartographer`](cartographer/) | [The Cartographer Project](https://github.com/cartographer-project) performs dense SLAM using LIDAR data. |

## API

The SLAM service supports the following methods:

{{< readfile "/static/include/services/apis/slam.md" >}}

{{% alert title="Tip" color="tip" %}}

The following code examples assume that you have a robot configured with a SLAM service called `"my_slam_service"`, and that you add the required code to connect to your robot and import any required packages at the top of your code file.
Go to your robot's **Code sample** tab on the [Viam app](https://app.viam.com) for boilerplate code to connect to your robot.

{{% /alert %}}

### GetPosition

Get the current position of the component the SLAM service is configured to source point cloud data from in the SLAM map as a [`Pose`](/internals/orientation-vector/).

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(spatialmath.Pose)](https://pkg.go.dev/go.viam.com/rdk/spatialmath#Pose): A `Pose` representing the current position of the specified component.
- [(string)](https://pkg.go.dev/builtin#string): The `"name"` of the component the SLAM service is configured to source point cloud data from.
  For example, a [camera](/components/camera/) named `"cam"`.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam).

```go {class="line-numbers linkable-line-numbers"}
slam_svc, err := slam.FromRobot(robot, "my_slam_service")

// Get the current position of the specified source component in the SLAM map as a Pose.
pos, name, err := slam_svc.GetPosition(context.Background())
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Pose)](https://python.viam.dev/autoapi/viam/services/slam/index.html#viam.services.slam.Pose): A `Pose` representing the current position of the component the SLAM service is configured to source point cloud data from.
  For example, a [camera](/components/camera/) named `"cam"`.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_position).

```python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the current position of the specified source component in the SLAM map as
# a Pose.
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

**Returns:**

- (func() [[]byte](https://pkg.go.dev/builtin#byte), [error](https://pkg.go.dev/builtin#error)): The complete point cloud map in standard PCD format.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

```go {class="line-numbers linkable-line-numbers"}
slam_svc, err := slam.FromRobot(robot, "my_slam_service")

// Get the point cloud map in standard PCD format.
pcd_map, err := slam_svc.GetPointCloudMap(context.Background())
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(List[GetPointCloudMapResponse])](https://python.viam.dev/autoapi/viam/gen/service/slam/v1/slam_pb2/index.html#viam.gen.service.slam.v1.slam_pb2.GetPointCloudMapResponse): The complete point cloud map in standard PCD format.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_point_cloud_map).

```python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the point cloud map in standard PCD format.
pcd_map = await slam_svc.get_point_cloud_map()
```

{{% /tab %}}
{{< /tabs >}}

### GetInternalState

Get the internal state of the SLAM algorithm required to continue mapping/localization.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- (func() [[]byte](https://pkg.go.dev/builtin#byte), [error](https://pkg.go.dev/builtin#error)): Chunks of the internal state of the SLAM algorithm.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

```go {class="line-numbers linkable-line-numbers"}
slam_svc, err := slam.FromRobot(robot, "my_slam_service")

// Get the internal state of the SLAM algorithm required to continue mapping/localization.
internal_state, err := slam_svc.GetInternalState(context.Background())
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- (List[[GetInternalStateResponse](https://python.viam.dev/autoapi/viam/gen/service/slam/v1/slam_pb2/index.html#viam.gen.service.slam.v1.slam_pb2.GetInternalStateResponse)]): Chunks of the internal state of the SLAM algorithm.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/index.html#viam.services.slam.SLAMClient.get_internal_state).

```python {class="line-numbers linkable-line-numbers"}
slam = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the internal state of the SLAM algorithm required to continue
# mapping/localization.
internal_state = await slam.get_internal_state()
```

{{% /tab %}}
{{< /tabs >}}

### GetLatestMapInfo

Get the timestamp of the last update to the point cloud SLAM map.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(time.Time)](https://pkg.go.dev/time#Time): The timestamp of the last update to the point cloud SLAM map.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

```go {class="line-numbers linkable-line-numbers"}
slam_svc, err := slam.FromRobot(robot, "my_slam_service")

// Get the timestamp of the last update to the point cloud SLAM map.
timestamp, err := slam_svc.GetLatestMapInfo(context.Background())
```

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(`datetime`)](https://docs.python.org/3/library/datetime.html): The timestamp of the last update.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_latest_map_info).

```python {class="line-numbers linkable-line-numbers"}
slam = SLAMClient.from_robot(robot=robot, name="my_slam_service")

timestamp = slam.get_latest_map_info()
```

{{% /tab %}}
{{< /tabs >}}

## DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own SLAM service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map\[string\]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
slam_svc, err := slam.FromRobot(robot, "my_slam_service")

resp, err := slam_svc.DoCommand(ctx, map[string]interface{}{"command": "dosomething", "someparameter": 52})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{% tab name="Python" %}}

**Parameters:**

- `command` [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): The command to execute.
- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Mapping[str, ValueTypes])](https://docs.python.org/3/library/stdtypes.html#typesmapping): Result of the executed command.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.do_command).

```python {class="line-numbers linkable-line-numbers"}
slam = SLAMClient.from_robot(robot=robot, name="my_slam_service")

my_command = {
  "command": "dosomething",
  "someparameter": 52
}

await slam.do_command(my_command)
```

{{% /tab %}}
{{< /tabs >}}
