---
linkTitle: "Frames across machines"
title: "Frames across machines"
weight: 25
layout: "docs"
type: "docs"
description: "Attach a remote part's components into your machine's frame tree with the correct spatial offset."
date: "2026-04-16"
---

When a component lives on a different computer than your main part, the motion service still needs to know where that component sits in space.
A camera on a remote Raspberry Pi, an IMU on a sub-part's board, a shared warehouse camera on a stationary rig: all of them need a frame entry in the main machine's frame tree, not only in their own.
This page shows how to set that up.

## What the remote's frame field does

Every entry in your `remotes` array can include a `frame` field.
When your machine runs, two things happen with it:

1. A new frame is created in the main machine's frame tree, named `<remote-name>_world`. Its position in the tree comes from the `frame` field you configured: `parent`, `translation`, `orientation`.
2. Every resource on the remote that declares `parent: "world"` is re-parented to that new `<remote-name>_world` frame. Resources that declare a non-world parent keep their parent names (with the remote's `prefix` prepended if one is configured).

The bridge frame's name pattern matters when you debug.
If you named your remote `end-effector-cam`, look for `end-effector-cam_world` in the computed frame system.

## Edit the JSON directly

The form UI on a remote part's configuration card does not expose the `frame.parent` field.
Click **{}** on the remote's card to switch to advanced JSON view, and add the `frame` object alongside `name`, `address`, and `auth`.

## Worked example: camera on an arm's end effector

Setup: a robot arm connected to the main computer, and a small computer mounted on the end effector that hosts a depth camera.
You want the camera's pose to be correct relative to the arm so motion planning and pose queries work.

Main machine config (abbreviated):

```json
{
  "components": [
    {
      "name": "arm-1",
      "api": "rdk:component:arm",
      "model": "viam:ufactory:xArm850",
      "attributes": { "host": "192.168.1.233" },
      "frame": {
        "parent": "world",
        "translation": { "x": 0, "y": 0, "z": 0 }
      }
    },
    {
      "name": "gripper-1",
      "api": "rdk:component:gripper",
      "model": "viam:ufactory:vacuum_gripper",
      "attributes": { "arm": "arm-1" },
      "frame": {
        "parent": "arm-1",
        "translation": { "x": 0, "y": 0, "z": 150 }
      }
    }
  ],
  "remotes": [
    {
      "name": "end-effector-cam",
      "address": "end-effector-cam-main.abc123.viam.cloud:8080",
      "auth": {
        "credentials": { "type": "api-key", "payload": "<api-key-payload>" },
        "entity": "<api-key-id>"
      },
      "frame": {
        "parent": "arm-1",
        "translation": { "x": 95, "y": -17.5, "z": 38.175 },
        "orientation": {
          "type": "ov_degrees",
          "value": { "x": 0, "y": 0, "z": 1, "th": 90 }
        }
      }
    }
  ]
}
```

On the remote, the camera is configured with `parent: "world"` and no additional frame offset.
The main machine's computed frame tree comes out as:

```text
world
├── arm-1 (arm base, origin)
│   ├── gripper-1 (offset 0, 0, 150 mm along arm's tool frame)
│   └── end-effector-cam_world (offset 95, -17.5, 38.175 mm; 90° around Z)
│       └── camera-1 (at end-effector-cam_world's origin)
```

A `TransformPose` call asking for the camera's pose in `world` now returns the correct world-space pose as the arm moves, because the camera is parented into the arm's frame chain.

## Picking the numbers

Three fields control where the remote's world lands:

- **`parent`**: a frame that exists in the main machine's frame tree. Usually a component name (`arm-1` above) or `world`. For hardware physically mounted to another component, use that component's name.
- **`translation`**: the offset from `parent` to the remote's world origin, in millimeters. X/Y/Z.
- **`orientation`**: rotation of the remote's world axes relative to `parent`. The `ov_degrees` form uses a unit axis `(x, y, z)` and an angle `th` in degrees.

You have a design choice about where offsets live:

**Put the full physical offset in the remote's frame.**
The remote's own components stay at `parent: "world"` with no additional offset.
One place to edit when you re-measure, and the remote's config stays trivial.

**Split between the remote's frame and per-component frames on the remote.**
The remote's frame positions the remote's world at a meaningful anchor (a mount plate, a chassis corner).
Each component on the remote has its own offset from there.
Useful when the remote carries multiple components at different offsets, or when whoever owns that computer maintains its own config.

## Common mistakes

- **Omitting the remote's `frame` entirely.** Without it, the remote's resources appear at the main machine's world origin. Motion planning uses bad poses and visualization overlays land in the wrong place.
- **Configuring `frame` on the wrong side.** The `frame` inside a `remotes` entry lives in the config of the machine doing the remoting. The remote machine's own config does not know it is being remoted into; any frames it declares describe only its own local frame system.
- **Forgetting that sub-parts share this mechanism.** A sub-part's frame, even when configured through the Viam app, is stored as a `frame` field on a `remotes` entry and follows the same rules.
- **Referencing a parent that does not exist.** If `frame.parent` names a component you have not yet created, the frame system cannot attach the remote. Create the parent component first.

## Verify the result

From a Python SDK client, fetch the assembled frame system to inspect what the main machine actually computed:

```python
fs_config = await machine.get_frame_system_config()
for part in fs_config:
    print(part)
```

To verify a specific transform, call `transform_pose` with a known pose and target frame:

```python
from viam.proto.common import PoseInFrame, Pose

zero_in_camera = PoseInFrame(
    reference_frame="camera-1",
    pose=Pose(x=0, y=0, z=0, o_x=0, o_y=0, o_z=1, theta=0),
)
camera_in_world = await machine.transform_pose(zero_in_camera, "world")
print(camera_in_world)
```

If the returned pose does not match your measurements, compare each field of the remote's `frame` config against the physical offset, and confirm the remote's own components declare the expected parent.

## Next steps

{{< cards >}}
{{% card link="/hardware/multi-machine/add-a-remote-part/" %}}
{{% card link="/hardware/multi-machine/add-a-sub-part/" %}}
{{% card link="/operate/reference/services/frame-system/" %}}
{{< /cards >}}
