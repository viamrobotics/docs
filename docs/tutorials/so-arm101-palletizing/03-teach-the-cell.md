---
title: "Phase 3: Teach the cell by hand"
linkTitle: "3. Teach the cell"
type: "docs"
slug: "teach-the-cell"
weight: 30
description: "Move the arm by hand with torque disabled, read two gripper anchor poses from the Motion tab, and compute the pallet grid from them."
workshop: "so-arm101-palletizing"
toc_hide: true
phase: 3
phase_total: 5
prev: "/tutorials/so-arm101-palletizing/configure-the-arm/"
next: "/tutorials/so-arm101-palletizing/pack-from-python/"
languages: ["python"]
---

In this phase you map the physical cell into the arm's frame. Nothing in the cell is pre-measured: you find where the staging spot and the pallet actually sit, measured from the arm's base, by moving the gripper there yourself and reading its position back from the Viam app. You capture two anchor poses this way; the code you write in Phase 4 computes the rest of the pallet grid from them.

{{< alert title="The arm goes limp" color="caution" >}}
Disabling torque lets you move the arm by hand, but it also means the arm no longer holds its position against gravity. It drops as soon as you disable torque, and stays free to fall until you re-enable it. Support the arm with one hand while torque is off, clear the workspace and cubes from underneath it, and re-enable torque before you send any motion command.
{{< /alert >}}

## Why teach by hand

This cell needs eight target poses, one per cube, and teaching all eight by hand would be slow and error-prone. Instead, you capture just two anchors: the staging spot, where you hand-feed each cube, and the pallet's origin corner, the bottom-layer cell at grid position [0, 0]. Every other pallet position is a fixed offset from that origin corner, so once you know the origin and the grid spacing, you compute the remaining seven poses instead of teaching them individually.

## Place the pallet mat and staging marker

Before you capture anything, set the position markers in place in your workspace. You can print the cube-and-pallet template from the [companion project](https://github.com/viam-devrel/mini-palletizer) or create your own markers. Both the staging square and the farthest corner of the pallet should be within about 20cm (8 inches) of the arm's base.

- Set the **pallet mat** on a flat surface within the arm's reach. Line up the mat's **x** and **y** arrows with the arm's x and y axes, which you can see on the world frame in the **3D scene** tab. The mat's **origin** square is the pallet corner you will teach.
- Set the **staging square** to one side of the pallet, also within reach. This is where you hand-feed each cube.
- **Tape both down.** They must not move while you teach poses or while the arm runs the pack later, or the cubes will miss their marks. Once they are fixed, leave them in place for the rest of the workshop.

With the markers fixed, you teach the arm two spots: the origin square on the mat and the staging square.

{{<imgproc src="/tutorials/so-arm101-palletizing/mat-placement.jpg" resize="1200x" declaredimensions=true class="imgzoom shadow" alt="Looking out from behind the SO-ARM101's base at the printed pallet mat and staging square taped to the desk. The mat's x arrow points straight out, away from the base, and its y arrow points to the arm's left; the origin square, marked with a dot, is the cell nearest the base.">}}

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

{{<imgproc src="/tutorials/so-arm101-palletizing/control-set-torque.png" resize="1200x" declaredimensions=true class="imgzoom shadow" alt="The arm-1 card on the CONTROL tab with the DO COMMAND section open. The input contains the set_torque command with enable set to false, and the output shows success true.">}}

## Read the gripper's position from the app

The poses you teach are **gripper** poses. The gripper's kinematics end at the point between its fingertips, and that point is what the motion service moves when your code plans in Phase 4. The arm's own end point sits at the wrist, about one finger length higher, so reading the arm's position instead of the gripper's would send the fingertips into the table.

Open the **MOTION** tab on your machine's page. It lists the current pose of each component in the world frame, and updates live as the arm moves. Read the x, y, and z from the `gripper-1` row: the position of the point between the fingertips, in millimeters. Because you placed the arm's base at the world origin in Phase 2, these coordinates are measured from the arm's base.

{{<imgproc src="/tutorials/so-arm101-palletizing/motion-tab-gripper-pose.png" resize="1200x" declaredimensions=true class="imgzoom shadow" alt="The MOTION tab pose table, in the world reference frame. The gripper-1 row shows x 159.19, y 0.01, z 59.08, with the pointer on its Copy pose button; the arm-1 row above it reads about 100 mm higher in z, because the arm frame ends at the wrist rather than between the fingertips.">}}

## Capture the staging pose

Set a cube on the staging square, the place where you will set down one cube at the start of every pick cycle in later phases. With torque disabled, gently guide the gripper over it until the cube sits between the jaws and the fingertips are level with the cube's top face.

Hold the arm steady once it is in position, then read the gripper's pose from the **MOTION** tab and record the x, y, and z. This is your staging pose. Move the arm slightly and watch the numbers change, so you know the table is tracking the live position, then guide it back and re-read if needed.

{{<imgproc src="/tutorials/so-arm101-palletizing/teach-by-hand.jpg" resize="1200x" declaredimensions=true class="imgzoom shadow" alt="Two hands guiding the SO-ARM101 by hand with torque disabled, lowering the gripper's fingertips toward an orange die sitting on a square of the printed pallet mat.">}}

## Capture the pallet origin corner

Move the cube to the mat's **origin** square, cell [0, 0]. The mat's x and y arrows point away from this square toward the other three cells, and the code computes those cells by stepping out from here, so teach this square and not another corner. Still with torque disabled, guide the gripper to the cube the same way: cube between the jaws, fingertips level with its top face. Read the gripper's pose from the **MOTION** tab again and record the x, y, and z. This is your pallet origin pose.

## Re-enable torque

To re-enable torque, send the same `DoCommand` with `enable` flipped to `true`:

```json
{
  "command": "set_torque",
  "enable": true
}
```

The arm's joints stiffen and it holds its current position. Confirm this by letting go of the arm; it should stay put instead of drooping.

## Save your anchors

Write down the two poses you just read, staging and pallet origin, each as the x, y, and z from the **MOTION** tab. Keep this note handy: in Phase 4 you paste these numbers into the companion project's `helpers.py`, into the `STAGING_POSE` and `PALLET_ORIGIN` constants that `palletizer.py` reads. From there, `palletizer.py` passes `PALLET_ORIGIN` into `helpers.grid` to get all eight target poses, and uses `STAGING_POSE` as the fixed pick location for every cycle.

{{< checkpoint >}}
With torque disabled, the gripper pose on the **MOTION** tab updates as you move the arm by hand, confirming it tracks the physical arm. After you re-enable torque, the arm holds its pose and does not drift when you let go. You have two recorded poses, staging and pallet origin, written down and ready to carry into Phase 4. If the pose does not change as you move the arm, confirm torque is actually disabled; if the arm still droops after re-enabling torque, resend the `set_torque` command with `enable` set to `true` and check the LOGS tab for a serial error.
{{< /checkpoint >}}

With your two anchor poses recorded, [Phase 4](/tutorials/so-arm101-palletizing/pack-from-python/) is where you write the Python that reads these positions and drives the arm through a pick-and-place pack.

{{< workshop-nav >}}
