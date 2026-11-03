---
title: "Phase 2: Configure the cell"
linkTitle: "2. Configure the cell"
type: "docs"
slug: "configure-the-cell"
weight: 20
description: "Set up the physical cell, add the fragment that configures every resource, override your per-cell values, and teleoperate the xArm6 with the SO-ARM101 leader."
workshop: "xarm-act-stacking"
toc_hide: true
phase: 2
phase_total: 7
time_estimate: "75 minutes"
prev: "/tutorials/xarm-act-stacking/platform-mental-model/"
next: "/tutorials/xarm-act-stacking/record-demonstrations/"
languages: ["python"]
capabilities:
  [
    "hw-arm",
    "hw-camera",
    "frame-system",
    "motion-planning",
    "teleop",
    "machine-config",
    "docs",
  ]
diataxis: tutorial
draft: true
---

In this phase you build the cell and get the leader steering the follower. You set up the hardware, add one fragment that configures every resource, then review each resource and edit the values that depend on your setup. The phase ends when moving the leader moves the xArm6.

## Set up the cell

Lay out the printed mat on your table. Mount the scene webcam at its marked position on the mat so it sees the whole stacking area. Mount the RealSense camera on the xArm6 wrist.

<!-- ASSET cell-layout (PHOTO): the printed mat on the table with the xArm6, the scene webcam at its marked position, the wrist RealSense, and the SO-ARM101 leader beside the xArm -->

Place the leader arm where you can reach it comfortably and where it can't hit the follower's workspace. Where you put it matters in step 8, when you describe its position to the teleop service.

## Add the fragment

A fragment is a reusable block of machine config. The companion repo's `config/cell.json` holds every resource in this phase, so you don't add them one by one. See [Reuse configuration with fragments](/fleet/reuse-configuration/) for how fragments work.

1. In the Viam app, open **FLEET**, then **Fragments**, and create a new fragment in your organization.
2. Paste in the contents of `config/cell.json` from the [companion repo](https://github.com/viam-devrel/xarm-act-stacking).
3. Save the fragment.
4. Open your machine's **CONFIGURE** tab, add the fragment, and save.

<!-- TODO(dep): switch to a public fragment ID if devrel publishes one -->

The fragment adds every resource in steps 3 to 9. You add nothing by hand. You only override the values that differ per cell:

- The xArm `host` IP address.
- The leader's serial `port`.
- The webcam's `video_path`.
- The table obstacle's size and pose.
- The teleop mapping.

To override a value, find the fragment card on the **CONFIGURE** tab and click the field you want to change. Modified fields are highlighted. In JSON mode, overrides go in the `fragment_mods` array, using the path to the field:

```json
{
  "fragment_mods": [
    {
      "fragment_id": "<your-fragment-id>",
      "mods": [
        {
          "$set": {
            "components.xarm.attributes.host": "192.168.1.100"
          }
        }
      ]
    }
  ]
}
```

Each step below shows the resource as the fragment defines it. Change only the values the step names.

## Review the follower: xArm6 and gripper

The xArm6 is the follower. The `viam:ufactory` module provides both the arm and the gripper. The gripper's `arm` attribute makes the arm a dependency of the gripper, because the gripper shares the arm's connection.

Edit the `host` on `xarm` to your arm's IP address:

```json
{
  "host": "192.168.1.100"
}
```

The gripper config points at the arm:

```json
{
  "arm": "xarm"
}
```

The gripper also has a frame with `parent: "xarm"`. This matters because teleop drives the gripper frame (`follower_component`), so the gripper's tool center point, not the arm's flange, tracks the leader. For the general concept, see [Arm and end effector frames](/motion-planning/frame-system/end-effector-frames/).

Open the **CONTROL** tab and find the `xarm` test card. Press **Current position** under **MoveToPosition** to fill the pose values. Then jog a joint a small amount with the **+** and **-** buttons.

{{< alert title="The arm is about to move" color="caution" >}}
Clear the workspace and keep the e-stop within reach. Change one joint by a small amount at a time.
{{< /alert >}}

{{< checkpoint >}}
Pressing **Current position** fills the pose values, and jogging a joint moves the physical xArm6. If nothing moves, confirm `host` is correct and check the **LOGS** tab for a connection error.
{{< /checkpoint >}}

## Review the cameras

You have two cameras. Edit the webcam's `video_path` to match your machine.

`wrist-cam` is the RealSense, configured for color only. That way `GetImages` returns no depth image, and training sees exactly two image features: `wrist-cam` and `scene-cam`.

<!-- TODO(dep): exact RealSense attribute for color-only (for example sensors: ["color"]); confirm against the realsense module docs -->

```json
{
  "sensors": ["color"]
}
```

`scene-cam` is a USB webcam. Set its device path:

```json
{
  "video_path": "<your-webcam-video-path>"
}
```

To find the webcam's path or ID, see [Using `video_path`](/reference/components/camera/webcam/#using-video_path). An ID is more consistent than a path.

Open the **CONTROL** tab and check each camera card.

{{< checkpoint >}}
Both `wrist-cam` and `scene-cam` show a live color image. The `wrist-cam` card shows color only. If a card is blank, check the **LOGS** tab for a camera error and confirm the `video_path`.
{{< /checkpoint >}}

## Edit the leader: SO-ARM101 arm and gripper

The fragment adds `leader-arm` and `leader-gripper`. The leader is a hand-guided SO-ARM101. You only need to edit its serial `port`.

To find the port, add the SO-ARM101 module's discovery service the way [Phase 2 of the SO-ARM101 palletizing tutorial](/tutorials/so-arm101-palletizing/configure-the-arm/) describes. Its **TEST** panel returns a suggested arm config with the detected `port` filled in. Copy the `port` value, then override `leader-arm`'s `port` with it. Don't add the components the discovery service suggests, because the fragment already provides them.

```json
{
  "port": "/dev/ttyUSB0"
}
```

The leader gripper is the SO-ARM101's sixth servo on the same serial bus, so its config points at the arm:

```json
{
  "arm": "leader-arm"
}
```

You need both because teleop's `leader_gripper` and `follower_gripper` mirror the jaw. Closing the leader's jaw closes the xArm gripper.

## Edit the table obstacle

The builtin motion service plans every teleop step and checks it for collisions. The fragment includes the table as a box obstacle, so the follower never plans through it.

Measure your table, then edit the obstacle's size and pose. The geometry origin is the center of the box, so for a 40 mm thick table whose top is at world z = 0, translate the frame to z = -20.

```json
{
  "geometries": [{ "type": "box", "x": 1800, "y": 1100, "z": 40 }]
}
```

```json
{
  "parent": "world",
  "translation": { "x": 500, "y": 0, "z": -20 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

These values are an example. Use your own measurements. For the full config shape, see [Configure workspace obstacles](/motion-planning/obstacles/configure-workspace-obstacles/).

## Review the Cartesian teleop service

The `teleop` service reads the leader's tool pose, maps it into the follower's frame, and hands it to the motion service, which plans the xArm's joints. Review its config:

<!-- TODO(dep): module ID, model name, and attribute names from the extracted teleop module -->

```json
{
  "leader_arm": "leader-arm",
  "leader_gripper": "leader-gripper",
  "follower_component": "xarm-gripper",
  "follower_gripper": "xarm-gripper",
  "gripper_invert": true,
  "leader_tool_offset_mm": { "z": 96 }
}
```

`follower_component` is the frame the motion service positions, so it's the gripper. `follower_gripper` is the gripper that mirrors the leader's jaw. Both point to `xarm-gripper`.

`gripper_invert: true` makes squeezing the leader's jaw close the follower. Without it, the follower sits closed and squeezing opens it. `leader_tool_offset_mm` moves the mirrored point out to the tip of the stock SO-ARM101 leader handle. Without it, leader rotations pivot the follower off its tip.

## Edit the teleop mapping

Two more attributes, `gripper_invert` and `leader_tool_offset_mm`, are already set in the previous step. Three attributes place the leader relative to the xArm. They depend on where you put the leader in step 1.

- `scale` multiplies the leader's translation about its base, so a desktop arm can span the follower's larger workspace. The default is `1`.
- `origin_translation_mm` is the position of the leader's base in the follower's world frame, in millimeters, as `{x, y, z}`.
- `origin_orientation` is the orientation of the leader's base in the follower's world frame, in the same syntax as a frame's `orientation` (for example `ov_degrees`).

```json
{
  "scale": 2.0,
  "origin_translation_mm": { "x": 0, "y": 0, "z": 0 },
  "origin_orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

To tune these, set `align_on_start` to `true`:

```json
{
  "align_on_start": true
}
```

On `start`, the leader drives itself to match the follower's pose. If the mapping is wrong, you see the offset as a visible mismatch between the two arms. For every attribute and its default, see the Cartesian teleop module's documentation.

<!-- TODO(dep): link the extracted teleop module's docs -->

Tune in a short loop:

1. Send `start`.
2. Move the leader along one axis.
3. Compare the directions of the leader and the xArm.
4. If the arms are offset, adjust `origin_translation_mm`.
5. If an axis is reversed or swapped, fix the sign or rotation in `origin_orientation`. If the arm covers too much or too little distance, adjust `scale`.
6. Send `stop`, save, and repeat.

## Review the home poses

The fragment adds two `erh:vmodutils:arm-position-saver` switches, `follower-home` and `leader-home`. Don't create them. Move each arm to a safe home pose, then save that pose to its switch.

To save a pose, open the **CONTROL** tab and jog the arm to its home pose. Then find the switch's card and set it to position 1 ("update config") to save the pose. Set it to position 2 ("go to") to confirm the arm returns there. Position 0 is the idle state. Save with position 1 before you use position 2. For more on the switch, see [Phase 3 of the pick-and-place tutorial](/tutorials/pick-and-place/static-positions/).

<!-- TODO(dep): confirm saving to a fragment-defined switch works (becomes a fragment_mods override) -->

In Phase 3, the **H** key in the capture-control webapp stops teleop and moves each arm to its saved pose between episodes.

{{< checkpoint >}}
Open the `teleop` service's DoCommand test panel and send `{"command": "start"}`. Move the leader. The xArm moves in the same direction. Close the leader's jaw and the xArm gripper closes. Then send `{"command": "stop"}`. If the directions are wrong, return to the tuning loop.
{{< /checkpoint >}}

## If it doesn't move

Send `{"command": "status"}` to the `teleop` service. Each pair of arms reports these fields:

- `last_error` is the most recent error. Start here. It also carries planner and collision failures, for example a target that collides with the table.
  <!-- TODO(dep): define what rejected counts -->
- `rejected` is reported alongside it. If it climbs as you move, check `last_error` and the table obstacle.
- `align_position_error_mm` is how far the leader ended up from the follower's mapped pose after `align_on_start`. A large value means the mapping or the leader's reach is off.

{{< workshop-nav >}}
