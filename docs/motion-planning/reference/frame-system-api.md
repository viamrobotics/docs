---
linkTitle: "Frame system API"
title: "Frame system API reference"
weight: 27
layout: "docs"
type: "docs"
description: "The RPCs for querying and transforming frame system poses live on the robot service, not a standalone frame system service."
---

The RPCs for querying and transforming frame system poses live on the robot service, not on a dedicated `FrameSystemService`. New users often look for a separate service matching the concept; there is none. All four methods below belong to `RobotService` in `api/proto/viam/robot/v1/robot.proto`.

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

Inside RDK, the frame system is registered under two names: `builtin` (the default instance that ships with `viam-server`) and `$framesystem` (the name modules use to resolve a dependency on the frame system). SDK callers do not reference either; the RPCs on the robot/machine client hit the frame system transparently.

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
    name = part.frame.reference_frame
    parent = part.frame.pose_in_observer_frame.reference_frame
    print(name, "parent:", parent)
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

`GetPose` exists on two services in the proto: the robot service (current) and the motion service (older, deprecated, same parameter shape). The Go SDK surfaces the robot service version as `RobotClient.GetPose`; Go callers go through the robot service. The Python SDK never wrapped the robot service version, so Python callers use `MotionClient.get_pose` and hit the deprecated motion service path.

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

**Python kwarg naming.** In Python, `MotionClient.get_pose` takes `supplemental_transforms`; `RobotClient.transform_pose` and `RobotClient.get_frame_system_config` take `additional_transforms`. The proto field and all Go methods use `supplemental_transforms`. Pass the kwarg that matches the client class you call.

#### Worked example: transform a detected object to the world frame

Suppose a camera at frame `my-camera` has detected a box 400 mm in
front of it. The box is not configured in the machine's frame system,
but you want to compute its world-frame pose so an arm can plan a
motion to it.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import PoseInFrame, Pose, Transform

# 1. Declare the detected box as a supplemental transform.
#    The Transform's reference_frame is the parent; the pose is the
#    box's position in that parent.
detected_box = Transform(
    reference_frame="detected-box",
    pose_in_observer_frame=PoseInFrame(
        reference_frame="my-camera",
        pose=Pose(x=0, y=0, z=400, o_x=0, o_y=0, o_z=1, theta=0),
    ),
)

# 2. Ask the motion service where the box sits in the world frame.
box_in_world = await motion_service.get_pose(
    component_name="detected-box",
    destination_frame="world",
    supplemental_transforms=[detected_box],
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "github.com/golang/geo/r3"
    "go.viam.com/rdk/referenceframe"
    "go.viam.com/rdk/spatialmath"
)

// 1. Build a LinkInFrame: detected-box is parented to my-camera,
//    sitting 400 mm in front along camera z.
detectedBox := referenceframe.NewLinkInFrame(
    "my-camera",
    spatialmath.NewPose(
        r3.Vector{X: 0, Y: 0, Z: 400},
        &spatialmath.OrientationVectorDegrees{OZ: 1},
    ),
    "detected-box",
    nil, // optional geometry
)

// 2. Ask the robot service for its world-frame pose.
boxInWorld, err := machine.GetPose(
    ctx,
    "detected-box",
    referenceframe.World,
    []*referenceframe.LinkInFrame{detectedBox},
    nil, // extra
)
```

{{% /tab %}}
{{< /tabs >}}

The transform is discarded after this call. If you want the box to
participate in a motion plan (as an obstacle, or as a component the
arm navigates relative to), pass the same transform on the motion
`Move` request through `WorldState.transforms`.

## TransformPCD

Transform a point cloud from one reference frame to another. Useful for
aligning point clouds from multiple cameras into a common frame, or for
expressing lidar scans in world coordinates.

| Parameter         | Description                                                                        |
| ----------------- | ---------------------------------------------------------------------------------- |
| `point_cloud_pcd` | The source point cloud (bytes, PCD format).                                        |
| `source`          | The reference frame the source point cloud is expressed in.                        |
| `destination`     | The reference frame to express the point cloud in. Defaults to `"world"` if unset. |

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
