---
title: "SLAM Service"
linkTitle: "SLAM"
weight: 30
type: "docs"
description: "Simultaneous Localization And Mapping (SLAM) allows your machine to create a map of its surroundings and find its location within that map."
tags: ["slam", "services"]
icon: true
images: ["/services/icons/slam.svg"]
no_list: true
aliases:
  - "/services/slam/"
# SMEs: Kat, Jeremy
---

{{% alert title="Stability Notice" color="note" %}}
The SLAM service is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

[Simultaneous Localization And Mapping (SLAM)](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping) allows your machine to create a map of its surroundings and find its location within that map.
SLAM is an important area of ongoing research in robotics, particularly for mobile applications such as drones, boats, and rovers.

The Viam SLAM service supports the integration of SLAM as a service on your machine.
You can conduct SLAM with data collected live by a [RPlidar](https://github.com/viamrobotics/rplidar) or with LIDAR data you provide in configuration, and easily view the map you build on the **SLAM library** tab of your location's page in the [Viam app](https://app.viam.com):

![Completed SLAM maps in the SLAM library tab](/mobility/slam/view-map-page.png)

## Used with

<!-- markdownlint-disable MD034 -->

{{< cards >}}
{{< relatedcard link="/components/camera/" alt_title="RPlidar" alt_link="https://github.com/viamrobotics/rplidar" required="yes">}}
{{< relatedcard link="/components/movement-sensor/" required="no" >}}
{{< /cards >}}

{{% snippet "required-legend.md" %}}

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

The following code examples assume that you have a machine configured with a SLAM service called `"my_slam_service"`, and that you add the required code to connect to your machine and import any required packages at the top of your code file.
Go to your machine's **CONNECT** tab on the [Viam app](https://app.viam.com) and select the **Code sample** page for boilerplate code to connect to your machine.

{{% /alert %}}

### GetPosition

Get the current position of the component the SLAM service is configured to source point cloud data from in the SLAM map as a [`Pose`](/internals/orientation-vector/).

{{< tabs >}}
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
mySlam, err := slam.FromRobot(machine, "my_slam_service")
if err != nil {
  logger.Error(err)
  return
}

// Get the current position of the specified source component in the SLAM map as a Pose.
pos, name, err := mySlam.Position(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

### GetPointCloudMap

Get the point cloud map.

{{< tabs >}}
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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `returnEditedMap` [(bool)](https://pkg.go.dev/builtin#bool): A flag that determines if the method should return the edited version of the point cloud map or the original map. Setting this parameter to `true` triggers a formatted map to be retrieved.

**Returns:**

- (func() [[]byte](https://pkg.go.dev/builtin#byte), [error](https://pkg.go.dev/builtin#error)): The complete point cloud map in standard PCD format.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

```go {class="line-numbers linkable-line-numbers"}
mySlam, err := slam.FromRobot(machine, "my_slam_service")
if err != nil {
  logger.Error(err)
  return
}

// Get the point cloud map in standard PCD format.
pcd_map, err := mySlam.PointCloudMap(context.Background(), true)
```

{{% /tab %}}
{{< /tabs >}}

### GetProperties

Get information about the current SLAM session.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- `timeout` [(Optional\[float\])](https://docs.python.org/library/typing.html#typing.Optional): An option to set how long to wait (in seconds) before calling a time-out and closing the underlying RPC call.

**Returns:**

- [(Properties)](https://python.viam.dev/autoapi/viam/proto/service/slam/index.html#viam.proto.service.slam.GetPropertiesResponse): Information about the current SLAM session. An object containing four fields:
  - `sensor_info` [(Iterable[SensorInfo])](https://python.viam.dev/autoapi/viam/proto/service/slam/index.html#viam.proto.service.slam.SensorInfo): Information about the sensors (camera and movement sensor) configured for your SLAM service, including the name and type of sensor.
  - `cloud_slam` [(bool)](https://docs.python.org/3/library/stdtypes.html#bltin-boolean-values): A boolean which indicates whether the session is being run in the cloud.
  - `mapping_mode` [(MappingMode)](https://python.viam.dev/autoapi/viam/proto/service/slam/index.html#viam.proto.service.slam.MappingMode): Represents the [form of mapping and localizing the current session is performing](/mobility/slam/cartographer/#use-a-live-machine). This includes creating a new map, localizing on an existing map and updating an existing map.
  - `internal_state_file_type` [(str)](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str): The file type the service's internal state algorithm is stored in.

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.get_properties).

```python {class="line-numbers linkable-line-numbers"}
slam_svc = SLAMClient.from_robot(robot=robot, name="my_slam_service")

# Get the properties of your current SLAM session.
slam_properties = await slam_svc.get_properties()
```

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(Properties)](https://pkg.go.dev/go.viam.com/rdk/services/slam#Properties): Information about the current SLAM session.
  An object containing four fields:
  - `SensorInfo` [(SensorInfo[])](https://pkg.go.dev/go.viam.com/api/service/slam/v1#SensorInfo): Information about the sensors (camera and movement sensor) configured for your SLAM service, including the name and type of sensor.
  - `CloudSlam` [(bool)](https://pkg.go.dev/builtin#bool): A boolean which indicates whether the session is being run in the cloud.
  - `MappingMode` [(MappingMode)](https://pkg.go.dev/go.viam.com/rdk/services/slam#MappingMode): Represents the [form of mapping and localizing the current session is performing](/mobility/slam/cartographer/#use-a-live-machine). This includes creating a new map, localizing on an existing map and updating an existing map.
  - `InternalStateFileType` [(string)](https://pkg.go.dev/builtin#string): The file type the service's internal state algorithm is stored in.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Properties).

```go {class="line-numbers linkable-line-numbers"}
mySlam, err := slam.FromRobot(machine, "my_slam_service")
if err != nil {
  logger.Error(err)
  return
}

// Get the properties of your current SLAM session
properties, err := mySlam.Properties(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

### GetInternalState

Get the internal state of the SLAM algorithm required to continue mapping/localization.

{{< tabs >}}
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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- (func() [[]byte](https://pkg.go.dev/builtin#byte), [error](https://pkg.go.dev/builtin#error)): Chunks of the internal state of the SLAM algorithm.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/services/slam#Service).

```go {class="line-numbers linkable-line-numbers"}
mySlam, err := slam.FromRobot(machine, "my_slam_service")
if err != nil {
  logger.Error(err)
  return
}

// Get the internal state of the SLAM algorithm required to continue mapping/localization.
internalState, err := mySlam.InternalState(context.Background())
```

{{% /tab %}}
{{< /tabs >}}

## DoCommand

Execute model-specific commands that are not otherwise defined by the service API.
For built-in service models, any model-specific commands available are covered with each model's documentation.
If you are implementing your own SLAM service and add features that have no built-in API method, you can access them with `DoCommand`.

{{< tabs >}}
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
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.
- `cmd` [(map\[string\]interface{})](https://go.dev/blog/maps): The command to execute.

**Returns:**

- [(map\[string\]interface{})](https://go.dev/blog/maps): Result of the executed command.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
mySlam, err := slam.FromRobot(machine, "my_slam_service")
if err != nil {
  logger.Error(err)
  return
}

resp, err := mySlam.DoCommand(context.Background(), map[string]interface{}{"command": "dosomething", "someparameter": 52})
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}

### Close

Safely shut down the resource and prevent further use.

{{< tabs >}}
{{% tab name="Python" %}}

**Parameters:**

- None

**Returns:**

- None

```python {class="line-numbers linkable-line-numbers"}
slam = SLAMClient.from_robot(robot, "my_slam_service")

await slam.close()
```

For more information, see the [Python SDK Docs](https://python.viam.dev/autoapi/viam/services/slam/client/index.html#viam.services.slam.client.SLAMClient.close).

{{% /tab %}}
{{% tab name="Go" %}}

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(error)](https://pkg.go.dev/builtin#error) : An error, if one occurred.

```go {class="line-numbers linkable-line-numbers"}
mySlam, err := slam.FromRobot(machine, "my_slam_service")
if err != nil {
  logger.Error(err)
  return
}

err := mySlam.Close(context.Background())
```

For more information, see the [Go SDK Docs](https://pkg.go.dev/go.viam.com/rdk/resource#Resource).

{{% /tab %}}
{{< /tabs >}}
