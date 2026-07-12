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
---

In this phase you map the physical cell into the arm's frame. Nothing in the cell is pre-measured: you find where the staging spot and the pallet actually sit, expressed in the arm's own coordinate frame, by moving the arm there yourself and reading its position back from the Viam app. You capture two anchor poses this way; the code you write in Phase 4 computes the rest of the pallet grid from them.

{{< alert title="The arm goes limp" color="caution" >}}
Disabling torque lets you move the arm by hand, but it also means the arm no longer holds its position against gravity. It drops as soon as you disable torque, and stays free to fall until you re-enable it. Support the arm with one hand while torque is off, clear the workspace and cubes from underneath it, and re-enable torque before you send any motion command.
{{< /alert >}}

## Why teach by hand

This cell needs eight target poses, one per cube, and teaching all eight by hand would be slow and error-prone. Instead, you capture just two anchors: the staging spot, where you hand-feed each cube, and the pallet's origin corner, the bottom-layer cell at grid position [0, 0]. Every other pallet position is a fixed offset from that origin corner, so once you know the origin and the grid spacing, you compute the remaining seven poses instead of teaching them individually.

## Place the pallet mat and staging marker

Before you capture anything, set the printed markers in place. Print the cube-and-pallet template from the [companion project](https://github.com/viam-devrel/mini-palletizer) at 100% scale and cut out the pallet mat and the staging square. (If you are using your own cubes, you still want the mat and staging marker for consistent positions.)

- Set the **pallet mat** on a flat surface within the arm's reach. Line up the mat's **x** and **y** arrows with the arm's x and y axes, which you can see on the world frame in the **3D scene** tab. The mat's **origin** square is the pallet corner you will teach.
- Set the **staging square** to one side of the pallet, also within reach. This is where you hand-feed each cube.
- **Tape both down.** They must not move while you teach poses or while the arm runs the pack later, or the cubes will miss their marks. Once they are fixed, leave them put for the rest of the workshop.

With the markers fixed, you teach the arm two spots: the origin square on the mat and the staging square.

<!-- ASSET mat-placement (PHOTO): printed pallet mat and staging square taped flat under the arm, x and y arrows aligned with the arm axes -->

## Disable torque

The standard arm API covers moving the arm and reading its position, but hardware often has extra capabilities that do not fit those standard methods. Viam exposes those through **`DoCommand`**, a general-purpose command channel a module can use to accept commands specific to its hardware. The SO-ARM101 module uses it for a `set_torque` command that turns the servos' holding torque on and off.

On the arm's test card on the **CONTROL** tab, open the DoCommand box and send:

```json
{
  "command": "set_torque",
  "enable": false
}
```

Once the command succeeds, the arm's joints go slack and you can move it by hand.

<!-- ASSET control-set-torque (UI): the arm test card DoCommand box with the set_torque enable:false command entered -->

## Read the arm's position from the app

The arm's test card on the **CONTROL** tab shows its current **end position**: the x, y, and z of the arm's end point, in millimeters, plus an orientation. As you move the arm by hand with torque disabled, that readout updates to track it. Because you placed the arm's base at the world origin in Phase 2, this end position is also a position in the world frame.

You position the arm so the gripper's jaws sit where you want them, then read the end position off the card. Because the gripper is rigidly attached, driving the arm's end point back to that same pose later returns the jaws to the same spot.

<!-- ASSET arm-endposition-card (UI): arm test card end-position readout (x, y, z) highlighted -->

## Capture the staging pose

With torque disabled, gently guide the gripper to the staging spot, the place where you will set down one cube at the start of every pick cycle in later phases. Hold the arm steady once it is in position, then read the **end position** off the arm's test card and record the x, y, and z. This is your staging pose. Move the arm slightly and watch the readout change, so you know it is tracking the live position, then guide it back and re-read if needed.

<!-- ASSET teach-by-hand (VIDEO): back-driving the arm by hand to the staging square while the end-position readout on the test card updates live (signature moment) -->

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

## Save your anchors

Write down the two poses you just read, staging and pallet origin, each as the x, y, and z from the arm's test card. Keep this note handy: in Phase 4 you paste these numbers into the companion project's `helpers.py`, into the `STAGING_POSE` and `PALLET_ORIGIN` constants that `palletizer.py` reads. From there, `palletizer.py` passes `PALLET_ORIGIN` into `helpers.grid` to get all eight target poses, and uses `STAGING_POSE` as the fixed pick location for every cycle.

{{< checkpoint >}}
With torque disabled, the arm's end position on its test card changes as you move the arm by hand, confirming the readout tracks the physical arm. After you re-enable torque, the arm holds its pose and does not drift when you let go. You have two recorded poses, staging and pallet origin, written down and ready to carry into Phase 4. If the readout does not change as you move the arm, confirm torque is actually disabled; if the arm still droops after re-enabling torque, resend the `set_torque` command with `enable` set to `true` and check the LOGS tab for a serial error.
{{< /checkpoint >}}

With your two anchor poses recorded, [Phase 4](/tutorials/so-arm101-palletizing/pack-from-python/) is where you write the Python that reads them back and drives the arm through a pick-and-place pack.

{{< workshop-nav >}}
