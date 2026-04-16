---
linkTitle: "Overview"
title: "Frame system"
weight: 1
layout: "docs"
type: "docs"
description: "Build a unified coordinate tree so all components agree on where things are in physical space."
aliases:
  - /work-cell-layout/define-your-frame-system/
  - /build/work-cell-layout/define-your-frame-system/
  - /operate/mobility/move-arm/frame-how-to/
  - /reference/services/frame-system/
  - /services/frame-system/
  - /mobility/frame-system/
  - /services/frame-system/frame-config/
  - /mobility/frame-system/frame-config/
  - /reference/services/frame-system/frame-config/
  - /motion-planning/frame-system-how-to/
---

A robot with an arm, a camera, and a gripper has three components, and each one
reports positions in its own local coordinate system. The camera sees an object
at pixel (320, 240), but the arm needs that object's position in
three-dimensional space relative to its own base. Without a unified spatial
model, you cannot translate between coordinate systems.

The frame system stores the position and orientation of every component in a
single coordinate tree. You define where each component sits relative to its
parent, and Viam computes the transforms between any two frames automatically.
Once the tree is configured, a single API call answers questions like "where is
this point in my camera frame, expressed in world coordinates?"

Getting the frame system right is a prerequisite for motion planning and
obstacle avoidance, and for any task where components must agree on where
things are in physical space.

## Concepts

### The world frame

The world frame is the fixed root of your frame system. You do not configure it
directly; you define it implicitly when you give other frames a position
relative to it. The physical location is your choice, for example the corner of
a table, the center of a work surface, or the base of an arm.

Pick a point that is easy to measure from and that will not move. For a
table-mounted arm, the arm base or a table corner works well. For a mobile
robot, the center of the base is typical.

### Parent-child hierarchy

Each component's frame has a parent frame. The parent defaults to the world
frame if you do not specify one. When you attach a camera to an arm, you set the
camera's frame parent to the arm. This means the camera's position is defined
relative to the arm's end, and when the arm moves, the camera frame moves with
it automatically.

The hierarchy forms a tree rooted at the world frame:

```text
world
├── my-arm
│   ├── my-gripper (attached to arm)
│   └── my-camera (mounted on arm)
├── my-sensor (mounted on table)
└── table-surface
```

### Parent to an intermediate arm link

If you mount a component on an intermediate link of an arm rather than on the
end effector, set the parent to `<arm-name>:<link-name>`. The link name is the
`id` of a link in the arm's kinematic model. For example, if you have an arm
named `my-arm` with a UR5e kinematic model and you strap a camera to the
forearm, set the camera's parent to `my-arm:forearm_link`.

```json
{
  "parent": "my-arm:forearm_link",
  "translation": { "x": 0, "y": 0, "z": 30 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

The motion service plans around components attached to intermediate links the
same way it plans for components attached to the arm's end effector. To find
the link names for an arm, inspect its kinematic model file or run
`viam machines part motion print-config` and look for frames under the arm's name.

### Translation

Translation is the offset in millimeters from the parent frame's origin to the
component's origin. It is specified as an (x, y, z) vector:

- **x**: offset along the right-left axis
- **y**: offset along the forward-backward axis
- **z**: offset along the up-down axis

The exact meaning of each axis depends on the parent frame's orientation. If the
parent is the world frame with the standard orientation, +z points up.

### Orientation

Orientation describes how a component's axes are rotated relative to its parent
frame. Viam supports several orientation formats:

| Type           | Fields             | Description                                       |
| -------------- | ------------------ | ------------------------------------------------- |
| `ov_degrees`   | `x, y, z, th`      | Orientation vector (axis) with angle in degrees   |
| `ov_radians`   | `x, y, z, th`      | Orientation vector (axis) with angle in radians   |
| `euler_angles` | `roll, pitch, yaw` | Rotation around x, y, z axes (radians)            |
| `axis_angles`  | `x, y, z, th`      | Rotation axis (unit vector) with angle in radians |
| `quaternion`   | `w, x, y, z`       | Unit quaternion (auto-normalized)                 |

The default is `ov_degrees` with values `(0, 0, 1), 0`, which leaves the
component's axes aligned with its parent frame. The vector `(x, y, z)` defines
the rotation axis, and `th` defines the rotation angle around that axis. The
axis must be a non-zero vector; Viam normalizes it internally.

For a detailed reference on orientation vectors, see
[Orientation Vectors](/motion-planning/reference/orientation-vectors/).

### Geometry

Each frame can optionally include collision geometry. This is a simple shape that
approximates the component's physical footprint. The motion planner uses these
shapes to avoid collisions. Supported types:

- **box**: defined by x, y, z dimensions in mm
- **sphere**: defined by a radius in mm
- **capsule**: defined by a radius and length in mm

Geometry is centered on the frame's origin by default. You can add a
`translation` offset and `orientation` offset within the geometry config to shift
it relative to the frame.

For detailed information about obstacle geometry, see
[Define obstacles](/motion-planning/obstacles/).

## Edit a frame in the Viam app

To configure a frame, open the **CONFIGURE** tab in the Viam app, click
the component's card in the sidebar, and click **Frame**. The Frame
section is a JSON editor with no form, parent dropdown, or
geometry-type picker. Edit the JSON directly to set parent, translation,
orientation, and any geometry. Save with the **Save** button (or
`⌘`/`Ctrl`+`S`).

A typical frame configuration looks like this:

```json
{
  "parent": "world",
  "translation": { "x": 0, "y": 0, "z": 0 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

After saving, the [3D SCENE tab](/motion-planning/3d-scene/) renders the
frame at its computed world pose so you can verify visually. For
hardware-specific walkthroughs (table-mounted arm with gripper and
camera, mobile manipulator, mobile base with sensors), see the cards at
the bottom of this page.

### Verify with TransformPose

To verify a frame programmatically, transform a known point in the
component's frame to the world frame and compare against a physical
measurement.

For example, transform the gripper's origin into the world frame; the
result should match where the gripper physically sits when the arm is
at its current joint configuration:

```python
gripper_origin = PoseInFrame(
    reference_frame="my-gripper",
    pose=Pose(x=0, y=0, z=0, o_x=0, o_y=0, o_z=1, theta=0),
)
gripper_in_world = await machine.transform_pose(gripper_origin, "world")
print(f"Gripper in world: x={gripper_in_world.pose.x:.1f}, y={gripper_in_world.pose.y:.1f}, z={gripper_in_world.pose.z:.1f}")
```

If the printed coordinates do not match the physical measurement, check
the translation and orientation values in the frame configuration.

## TransformPose

`TransformPose` converts a pose from one reference frame to another. You
provide a source pose with its reference frame and a destination frame name;
the frame system computes the transform using the configured hierarchy and
current joint positions.

For example, to find where a camera's origin is in the world frame:

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.proto.common import PoseInFrame, Pose

# Express the camera's origin (0,0,0) in its own frame
camera_origin = PoseInFrame(
    reference_frame="my-camera",
    pose=Pose(x=0, y=0, z=0, o_x=0, o_y=0, o_z=1, theta=0)
)

# Transform to the world frame
world_pose = await machine.transform_pose(camera_origin, "world")
print(f"Camera in world: x={world_pose.pose.x}, y={world_pose.pose.y}, z={world_pose.pose.z}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
baseOrigin := referenceframe.NewPoseInFrame("my-camera", spatialmath.NewZeroPose())
worldPose, err := machine.TransformPose(context.Background(), baseOrigin, "world", nil)
```

{{% /tab %}}
{{< /tabs >}}

The optional `supplemental_transforms` parameter lets you include additional frame relationships that are not part of the stored configuration.
This is useful for dynamic frames, such as an object detected by a camera whose position is known relative to the camera but not configured in the frame system.

Common uses:

- **Verify frame configuration**: transform a component's origin to the world frame and check that the result matches its physical position.
- **Convert detections**: transform a point detected in a camera frame to world coordinates so an arm can reach it.
- **Compare across frames**: when two components report positions in different frames, transform both to a common frame before comparing.

## Verify visually with the 3D SCENE tab

The [3D SCENE tab](/motion-planning/3d-scene/) renders your frame hierarchy in
3D: every configured component appears at its computed world pose, with
geometry and axes drawn. Open it after a configuration change to confirm the
arm is mounted on the table, the camera is above the arm, and any obstacles
sit where you expect. Most frame configuration mistakes (wrong parent, wrong
axis, missing rotation) show up immediately in this view.

## Verify with the CLI

You can inspect your frame system from the command line without writing code:

```sh
# Print the frame system configuration
viam machines part motion print-config --part "my-machine-main"

# Print the current pose of every component relative to world
viam machines part motion print-status --part "my-machine-main"
```

If a component's pose looks wrong, check the translation and orientation values
in its frame configuration. For details on all CLI motion commands, see
[Motion Service Configuration](/motion-planning/reference/motion-service/#cli-commands).

## Configure frames for your hardware

{{< cards >}}
{{% card link="/motion-planning/frame-system/arm-gripper-camera/" noimage="true" %}}
{{% card link="/motion-planning/frame-system/arm-fixed-camera/" noimage="true" %}}
{{% card link="/motion-planning/frame-system/mobile-base-sensors/" noimage="true" %}}
{{% card link="/motion-planning/frame-system/mobile-base-arm/" noimage="true" %}}
{{% card link="/motion-planning/frame-system/camera-calibration/" noimage="true" %}}
{{< /cards >}}
