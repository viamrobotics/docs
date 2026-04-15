---
linkTitle: "Frame system API"
title: "Frame system API reference"
weight: 27
layout: "docs"
type: "docs"
description: "The RPCs for querying and transforming frame system poses live on the robot service, not a standalone frame system service."
---

The frame system is exposed to SDK callers through RPCs on the
**robot service**, not on a dedicated `FrameSystemService`. This is a
common point of confusion: users looking for "the frame system API"
expect a service matching the concept. The four methods listed here
are all members of `RobotService` in `api/proto/viam/robot/v1/robot.proto`.

| Method              | Purpose                                                                 |
| ------------------- | ----------------------------------------------------------------------- |
| `FrameSystemConfig` | Return the list of frame parts that make up the machine's frame system. |
| `GetPose`           | Return a component's pose in any reference frame.                       |
| `TransformPose`     | Convert a pose between reference frames.                                |
| `TransformPCD`      | Convert a point cloud between reference frames.                         |

The SDK client classes surface these as methods on the robot or
machine client object (`machine.transform_pose`, `machine.get_pose`,
and so on). You do not instantiate a separate frame system client.

## Service names

Inside the RDK, the frame system is registered under two names:

- **Internal name: `builtin`.** The default frame system instance that
  ships with `viam-server`.
- **Public name: `$framesystem`.** The name modules use to get a
  reference to the robot's frame system. If you are writing a module
  that needs frame transforms, resolve dependencies through this name.

SDK callers do not need to reference either name; they call the methods
on the robot/machine client directly.

## FrameSystemConfig

Returns the list of frame parts configured on the machine. Each part
has a name, parent, translation, orientation, and optional geometry.
This is what the CLI's
[`print-config`](/motion-planning/reference/cli-commands/#print-config)
command prints.

{{< tabs >}}
{{% tab name="Python" %}}

```python
parts = await machine.get_frame_system_config()
for part in parts:
    print(part.name, "parent:", part.pose_in_parent_frame.reference_frame)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
parts, err := machine.FrameSystemConfig(ctx)
if err != nil {
    logger.Fatal(err)
}
for _, part := range parts.Parts {
    logger.Infof("%s parent: %s", part.FrameConfig.Name(), part.FrameConfig.Parent())
}
```

{{% /tab %}}
{{< /tabs >}}

## GetPose

Returns a component's pose in the specified destination frame.

| Parameter                 | Description                                                                        |
| ------------------------- | ---------------------------------------------------------------------------------- |
| `component_name`          | The component whose pose to return.                                                |
| `destination_frame`       | The reference frame to express the pose in. Default: `"world"`.                    |
| `supplemental_transforms` | Optional additional frame relationships not stored in the machine's configuration. |
| `extra`                   | Optional map for implementation-specific extras.                                   |

Returns a `PoseInFrame`.

{{< tabs >}}
{{% tab name="Python" %}}

The Python `RobotClient` does not expose `GetPose`. Call `get_pose` on
the motion service client instead:

```python
from viam.services.motion import MotionClient

motion_service = MotionClient.from_robot(machine, "builtin")
gripper_in_world = await motion_service.get_pose(
    component_name="my-gripper",
    destination_frame="world",
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
gripperInWorld, err := machine.GetPose(
    ctx,
    "my-gripper",
    referenceframe.World,
    nil, // supplemental_transforms
    nil, // extra
)
```

{{% /tab %}}
{{< /tabs >}}

### Python goes through the motion service, Go through the robot service

The `GetPose` RPC lives on `RobotService` in the proto. The Go SDK
surfaces it as `RobotClient.GetPose`, so Go callers hit the robot
service directly. The Python SDK never wrapped it on `RobotClient`, so
Python callers must use `MotionClient.get_pose`, which calls the motion
service's `GetPose` (a separate, older, deprecated RPC with the same
parameter shape).

The two paths return equivalent results today. The underlying API
surface will eventually consolidate, but until then Python callers
stay on the motion-service path. The CLI's `print-status`, `get-pose`,
and `set-pose` commands also invoke the deprecated motion-service
method internally.

## TransformPose

Convert a pose expressed in one reference frame into the equivalent
pose in another. Unlike `GetPose`, the starting pose can be any point
you choose, not just a component origin.

| Parameter                 | Description                                                                        |
| ------------------------- | ---------------------------------------------------------------------------------- |
| `source`                  | The input `PoseInFrame` (pose plus its reference frame name).                      |
| `destination`             | The reference frame to express the pose in.                                        |
| `supplemental_transforms` | Optional additional frame relationships not stored in the machine's configuration. |

Returns a `PoseInFrame` in the destination frame.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import PoseInFrame, Pose

detected_in_camera = PoseInFrame(
    reference_frame="my-camera",
    pose=Pose(x=50, y=30, z=400),
)

detected_in_world = await machine.transform_pose(detected_in_camera, "world")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
detectedInCamera := referenceframe.NewPoseInFrame("my-camera",
    spatialmath.NewPoseFromPoint(r3.Vector{X: 50, Y: 30, Z: 400}))

detectedInWorld, err := machine.TransformPose(ctx, detectedInCamera, "world", nil)
```

{{% /tab %}}
{{< /tabs >}}

### Supplemental transforms

Use `supplemental_transforms` to augment the machine's configured frame
system for a single call. A common case: an object the camera has
detected whose pose you know relative to the camera, but which is not
configured as a component. Pass the object's frame relationship as a
supplemental transform, then call `TransformPose` or `GetPose` to
compute poses involving that object.

Supplemental transforms apply only to the current call. They do not
modify the stored frame system configuration.

**Python kwarg naming.** The proto field and the Go SDK use
`supplemental_transforms`. The Python SDK is inconsistent:
`MotionClient.get_pose` uses `supplemental_transforms`, but
`RobotClient.transform_pose` and `RobotClient.get_frame_system_config`
use `additional_transforms`. Pass the kwarg that matches the client
class you are calling.

## TransformPCD

Transform a point cloud from one reference frame to another. Useful for
aligning point clouds from multiple cameras into a common frame, or for
expressing lidar scans in world coordinates.

| Parameter      | Description                                                 |
| -------------- | ----------------------------------------------------------- |
| `source`       | The source point cloud (bytes, PCD format).                 |
| `source_frame` | The reference frame the source point cloud is expressed in. |
| `destination`  | The reference frame to express the point cloud in.          |

Returns the transformed point cloud (bytes).

Point cloud transforms are computationally expensive for large clouds.
Consider down-sampling before calling.

## Common patterns

- **Verify frame configuration**: transform a component's origin to
  the world frame and compare against physical measurements.
- **Convert camera detections to world coordinates**: transform a
  detection pose from the camera frame to the world frame before
  commanding an arm to that pose.
- **Compare poses across frames**: transform each pose to a common
  frame (typically `"world"`), then compare.
- **Carry dynamic frame relationships**: pass objects the machine
  picks up or detects as supplemental transforms so the planner and
  your code agree on their position.

## What's next

- [Frame system](/motion-planning/frame-system/): the concept these
  RPCs operate on.
- [Motion CLI commands](/motion-planning/reference/cli-commands/):
  CLI wrappers around the same RPCs.
- [Motion service API](/motion-planning/reference/api/): the motion
  RPCs, which take `supplemental_transforms` through the same
  `WorldState` mechanism.
