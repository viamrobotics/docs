---
title: "Phase 3: Teach the cell by hand"
linkTitle: "3. Teach the cell"
type: "docs"
slug: "teach-the-cell"
weight: 30
description: "Move the arm by hand with torque disabled, read back two anchor poses, and compute the pallet grid from them."
workshop: "so-arm101-palletizing"
toc_hide: true
phase: 3
phase_total: 6
time_estimate: "20 minutes"
prev: "/tutorials/so-arm101-palletizing/configure-the-arm/"
next: "/tutorials/so-arm101-palletizing/pack-from-python/"
languages: ["python"]
draft: true
---

In this phase you map the physical cell into the arm's frame. Nothing in the cell is pre-measured: you find where the staging spot and the pallet actually sit, expressed in the arm's own coordinate frame, by moving the arm there yourself and reading back where it ended up. You capture two anchor poses this way, then compute the rest of the pallet grid from them arithmetically.

{{< alert title="The arm goes limp" color="caution" >}}
Disabling torque lets you move the arm by hand, but it also means the arm no longer holds its position against gravity. It drops as soon as you disable torque, and stays free to fall until you re-enable it. Support the arm with one hand while torque is off, clear the workspace and cubes from underneath it, and re-enable torque before you send any motion command.
{{< /alert >}}

## Why teach by hand

This cell needs eight target poses, one per cube, and teaching all eight by hand would be slow and error-prone. Instead, you capture just two anchors: the staging spot, where you hand-feed each cube, and the pallet's origin corner, the bottom-layer cell at grid position [0, 0]. Every other pallet position is a fixed offset from that origin corner, so once you know the origin and the grid spacing, you compute the remaining seven poses instead of teaching them individually.

## Disable torque

The SO-ARM101 module exposes a `set_torque` command over `DoCommand`. On the arm's test card on the **CONTROL** tab, open the DoCommand box and send:

```json
{
  "command": "set_torque",
  "enable": false
}
```

You can send the same command from a terminal with `viam machines part run` if you prefer the command-line interface (CLI) to the test card. Once the command succeeds, the arm's joints go slack and you can move it by hand.

## Capture the staging pose

With torque disabled, gently guide the gripper to the staging spot, the place where you will set down one cube at the start of every pick cycle in later phases. Hold the arm steady once it's in position.

`capture_pose.py` is a small, self-contained script that connects to your machine and prints the arm's current end-effector pose. It needs nothing beyond the Viam Python SDK: no companion project, no helper file, just the code below. Its core is a single call to the arm's `get_end_position` API:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.arm import Arm


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="<api-key>", api_key_id="<api-key-id>"
    )
    robot = await RobotClient.at_address("<machine-address>", opts)
    arm = Arm.from_robot(robot, "arm")
    pose = await arm.get_end_position()
    print(f"x={pose.x:.1f} y={pose.y:.1f} z={pose.z:.1f}")
    print(f"o_x={pose.o_x:.3f} o_y={pose.o_y:.3f} o_z={pose.o_z:.3f} theta={pose.theta:.1f}")
    await robot.close()


asyncio.run(main())
```

Fill in the API key, key ID, and machine address from your machine's **CONNECT** tab. Save this as `capture_pose.py` and run it with:

```sh
uv run --with viam-sdk python capture_pose.py
```

The script calls the arm's standard [`get_end_position`](/reference/apis/components/arm/#getendposition) API, which returns the arm's end point, where the gripper mounts, computed by forward kinematics: x, y, and z in millimeters, plus an orientation, already expressed in the arm's own frame. You position the arm so the gripper's jaws sit at the spot you want, then record that end point; because the gripper is rigidly attached, driving the end point back to the same pose in Phase 4 returns the jaws to the same spot. Because you placed the arm's base at the world origin in Phase 2, this pose is also the pose in the world frame, which is what the motion service expects when you write `palletizer.py` in Phase 4. Move the arm slightly and run the script again to confirm the printed numbers change with it.

Record the printed x, y, and z for the staging pose. You will save these numbers in the last section of this phase.

## Capture the pallet origin corner

Still with torque disabled, guide the gripper to the bottom-layer corner of the pallet, cell [0, 0], the corner you treat as the origin of the pallet grid. Run `capture_pose.py` again and record the printed x, y, and z. This is your pallet origin pose.

## Re-enable torque

Send the same `DoCommand` with `enable` flipped to `true`:

```json
{
  "command": "set_torque",
  "enable": true
}
```

The arm's joints stiffen and it holds its current position. Confirm this by letting go of the arm; it should stay put instead of drooping.

## Derive the grid

With the pallet origin corner captured, the remaining seven target poses follow from two constants: the center-to-center spacing between cube slots, and the cube's own size, which sets the offset between the two stacked layers.

```python
PITCH = 30  # mm, center-to-center spacing between adjacent pallet cells
CUBE = 20  # mm, cube side length, and the z offset between layers
```

The four bottom-layer cells are the origin corner plus every combination of `(0, PITCH)` in x and y:

```text
(0, 0)  (PITCH, 0)
(0, PITCH)  (PITCH, PITCH)
```

The top layer repeats those same four x, y offsets at `z + CUBE`. In Phase 4, the companion project's `helpers.py` wraps this same arithmetic in a `grid` function:

```python
def grid(origin, pitch, cube):
    """Return the eight target poses for a two-layer, four-cell pallet,
    given the bottom-layer origin corner (cell [0, 0])."""
    bottom = [
        Pose(x=origin.x + dx, y=origin.y + dy, z=origin.z)
        for dx in (0, pitch)
        for dy in (0, pitch)
    ]
    top = [Pose(x=p.x, y=p.y, z=p.z + cube) for p in bottom]
    return bottom + top
```

These are positions only. In Phase 4 you apply a straight-down tool orientation to each one with a `down_pose` helper before sending it to the motion service.

The staging pose is not part of this grid. It stays a single fixed pose for the whole pack sequence: you hand-feed one cube to that same spot at the start of every cycle, and the arm always picks from there.

## Save your anchors

Write down the two poses you just captured, staging and pallet origin, each as the x, y, and z you read back with `capture_pose.py`. Keep this note handy: in Phase 4 you paste these numbers into the companion project's `helpers.py`, into the `STAGING_POSE` and `PALLET_ORIGIN` constants that `palletizer.py` reads. From there, `palletizer.py` passes `PALLET_ORIGIN` into `helpers.grid` to get all eight target poses, and uses `STAGING_POSE` as the fixed pick location for every cycle.

{{< checkpoint >}}
With torque disabled, running `capture_pose.py` repeatedly while you move the arm by hand returns different x, y, and z values each time, confirming the readback tracks the physical arm. After you re-enable torque, the arm holds its pose and does not drift when you let go. You have two recorded poses, staging and pallet origin, written down and ready to carry into Phase 4. If `capture_pose.py` returns the same values every time, confirm torque is actually disabled; if the arm still droops after re-enabling torque, resend the `set_torque` command with `enable` set to `true` and check the LOGS tab for a serial error.
{{< /checkpoint >}}

With your two anchor poses recorded, [Phase 4](/tutorials/so-arm101-palletizing/pack-from-python/) is where you write the Python that reads them back and drives the arm through a pick-and-place pack.

{{< workshop-nav >}}
