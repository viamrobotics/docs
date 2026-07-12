---
title: "Phase 3: Teach the cell by hand"
linkTitle: "3. Teach the cell"
type: "docs"
slug: "teach-the-cell"
weight: 30
description: "Move the arm by hand with torque disabled, read two anchor poses off its test card, and compute the pallet grid from them."
workshop: "so-arm101-palletizing"
toc_hide: true
phase: 3
phase_total: 6
prev: "/tutorials/so-arm101-palletizing/configure-the-arm/"
next: "/tutorials/so-arm101-palletizing/pack-from-python/"
languages: ["python"]
draft: true
---

In this phase you map the physical cell into the arm's frame. Nothing in the cell is pre-measured: you find where the staging spot and the pallet actually sit, expressed in the arm's own coordinate frame, by moving the arm there yourself and reading its position back from the Viam app. You capture two anchor poses this way, then compute the rest of the pallet grid from them arithmetically.

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

Once the command succeeds, the arm's joints go slack and you can move it by hand.

## Read the arm's position from the app

You do not need any code to read where the arm is. The arm's test card on the **CONTROL** tab shows its current **end position**: the x, y, and z of the arm's end point, in millimeters, plus an orientation. As you move the arm by hand with torque disabled, that readout updates to track it. Because you placed the arm's base at the world origin in Phase 2, this end position is also a world pose, which is exactly what the motion service expects when you write `palletizer.py` in Phase 4.

You position the arm so the gripper's jaws sit where you want them, then read the end position off the card. Because the gripper is rigidly attached, driving the arm's end point back to that same pose later returns the jaws to the same spot.

<!-- ASSET arm-endposition-card (UI): arm test card end-position readout (x, y, z) highlighted -->

## Capture the staging pose

With torque disabled, gently guide the gripper to the staging spot, the place where you will set down one cube at the start of every pick cycle in later phases. Hold the arm steady once it is in position, then read the **end position** off the arm's test card and record the x, y, and z. This is your staging pose. Move the arm slightly and watch the readout change, so you know it is tracking the live position, then guide it back and re-read if needed.

## Capture the pallet origin corner

Still with torque disabled, guide the gripper to the bottom-layer corner of the pallet, cell [0, 0], the corner you treat as the origin of the pallet grid. Read the **end position** again and record the x, y, and z. This is your pallet origin pose.

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

Write down the two poses you just read, staging and pallet origin, each as the x, y, and z from the arm's test card. Keep this note handy: in Phase 4 you paste these numbers into the companion project's `helpers.py`, into the `STAGING_POSE` and `PALLET_ORIGIN` constants that `palletizer.py` reads. From there, `palletizer.py` passes `PALLET_ORIGIN` into `helpers.grid` to get all eight target poses, and uses `STAGING_POSE` as the fixed pick location for every cycle.

{{< checkpoint >}}
With torque disabled, the arm's end position on its test card changes as you move the arm by hand, confirming the readout tracks the physical arm. After you re-enable torque, the arm holds its pose and does not drift when you let go. You have two recorded poses, staging and pallet origin, written down and ready to carry into Phase 4. If the readout does not change as you move the arm, confirm torque is actually disabled; if the arm still droops after re-enabling torque, resend the `set_torque` command with `enable` set to `true` and check the LOGS tab for a serial error.
{{< /checkpoint >}}

With your two anchor poses recorded, [Phase 4](/tutorials/so-arm101-palletizing/pack-from-python/) is where you write the Python that reads them back and drives the arm through a pick-and-place pack.

{{< workshop-nav >}}
