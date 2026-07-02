---
title: "Phase 3: Static positions and obstacles"
linkTitle: "3. Static positions"
type: "docs"
slug: "static-positions"
weight: 30
description: "Save the arm's key poses and configure obstacle components, proving the hardware and motion planning work before you add perception."
workshop: "pick-and-place"
toc_hide: true
phase: 3
phase_total: 6
time_estimate: "20 minutes"
prev: "/tutorials/pick-and-place/configure-resources/"
next: "/tutorials/pick-and-place/control-the-robot-from-python/"
languages: ["python"]
---

In this phase you move the arm through the full pick-and-place sequence using saved poses, with no perception yet. The goal is to prove that the hardware and motion planning work before you add detection, so that any bug you encounter later has only one new cause.

{{< workshop-phases >}}

## Why static positions first

When you add perception and motion planning at the same time, a failure could live in detection, the frame transform, the pose math, the motion planner, or gripper timing, and there is no straightforward way to tell which. Saving fixed poses lets you run the full hardware loop first. In Phase 4 you drive this same proven sequence from a Python script, and perception does not enter the picture until Phase 5. Once the arm reliably travels through every stage of the sequence, perception becomes the only new variable when you reach it.

This is not just a classroom shortcut. Pose-to-pose motion without perception is a real production workcell pattern: any time a part always lands in the same spot, a fixed sequence of saved poses is simpler and more reliable than running detection on every cycle.

The table below shows what each step in the static sequence validates:

| Step                      | What it validates                                 |
| ------------------------- | ------------------------------------------------- |
| Arm reaches home pose     | Observation position is safe and repeatable       |
| Arm reaches approach pose | Arm can get above the workspace without collision |
| Arm reaches grasp pose    | Descent distance is correct                       |
| Gripper opens and closes  | Finger timing is right                            |
| Arm reaches travel pose   | Safe carrying height clears obstacles             |
| Arm reaches place pose    | Bin position is correct                           |

## The key poses

Each saved pose has a specific role in the sequence:

| Pose          | Purpose                                                                                   |
| ------------- | ----------------------------------------------------------------------------------------- |
| home-pose     | Observation position above the workspace; the wrist camera has a clear view of the blocks |
| approach-pose | Standoff directly above the pick zone, roughly 80 to 100 mm above the highest block       |
| grasp-pose    | At the block, gripper open and ready to close; fingertips are level with the block top    |
| travel-pose   | Safe carrying height that clears obstacles while holding a block                          |
| place-pose    | Above the bin where blocks are dropped                                                    |

The approach pose and the grasp pose share the same x and y coordinates. The only motion between them is straight down the z axis, so if the arm drifts sideways during the descent you have a frame or calibration issue to investigate.

## Save each pose with the arm position saver

You configure pose saving by hand, the same way you configured the arm, gripper, and camera in Phase 2.

Add the `erh:vmodutils` module from the Viam registry to your machine. This module provides the `erh:vmodutils:arm-position-saver` switch model you use to save and recall poses, and the `erh:vmodutils:obstacle` model you use later in this phase.

Add a **switch** component for `home-pose`:

- API: `rdk:component:switch`
- Model: `erh:vmodutils:arm-position-saver`
- Attribute: `arm`: `"arm-1"`

This attribute is also a dependency, the same way `gripper-1` depends on `arm-1`: the switch cannot save or recall a pose until the arm it points at is running.

With the `home-pose` switch added, save and verify it:

1. Open the **CONTROL** tab and find the arm test card. Use the joint sliders to jog the arm into position.
2. Select **Get end position** on the arm card and note the x, y, and z values to confirm the arm is where you expect it.
3. On the switch test card, set the switch to **position 1** to save the current joint positions.
4. Set the switch to **position 2** to confirm the arm returns to the saved pose from any starting position.

Now that `home-pose` is saved, open its resource card on the **CONFIGURE** tab and use the **Duplicate** feature to create a copy. Rename the copy to `approach-pose`, and its `arm` attribute carries over automatically since it is already set to `"arm-1"`. Duplicate three more times for `grasp-pose`, `travel-pose`, and `place-pose`. This is faster than adding five switches from scratch and less error-prone, since you only type the `arm` attribute once.

Run the same four save-and-verify steps for each of the four new poses: jog the arm into position, confirm it with **Get end position**, set the switch to position 1 to save, and set it to position 2 to confirm the arm returns.

{{< alert title="Switch positions" color="note" >}}
On an `arm-position-saver` switch, position 1 saves the current joint positions, position 2 moves the arm to the saved pose, and position 0 clears any saved data. Always save with position 1 before you attempt position 2. Setting position 2 on an unsaved switch does nothing.
{{< /alert >}}

{{< checkpoint >}}
Set each saved switch to position 2 in turn. The arm should move to each pose you saved. If a switch does nothing when you set it to position 2, you have not saved it yet. Set position 1 first, then try position 2 again.
{{< /checkpoint >}}

## Teach the planner about obstacles

The Viam motion planner is collision-aware, but it can only avoid geometry it knows about. Without any obstacle configuration, the planner avoids self-collisions only. Once you add obstacle geometry, the planner treats the table surface and the workspace boundary as hard obstacles it cannot plan through.

This matters both for correctness and for safety. Without the table obstacle, the planner might find a path that swings the arm through the table surface. Virtual safety walls at the workspace boundary also prevent the arm from swinging into people standing nearby. This is not just a classroom convenience: it is the same pattern you would use to keep a production workcell's motion planner honoring the real boundaries of its cell.

In this workshop you configure two categories of obstacle: the table surface and two safety walls at the workspace boundary. Bin geometry is out of scope for this phase.

## Obstacles are components

Obstacles are not a separate WorldState file you import. Each obstacle is an `erh:vmodutils:obstacle` component you add on the **CONFIGURE** tab, the same way you added the arm, gripper, and camera. The obstacle model uses the gripper API, so once configured, each obstacle shows up in `resource_names` as a gripper. That is expected; the model reuses the gripper API purely as a resource container for geometry, it does not add a real gripper to your machine.

### Measure your workspace

Before you can fill in the obstacle geometry, measure your own table and workspace boundary. You need two kinds of measurement, and each one feeds a different part of the config:

- **Tape-measure dimensions** for the box sizes: the table's length, width, and thickness go into the table obstacle's `x`, `y`, and `z`. Use the tape measure for how big each box is, not for where it sits.
- **Arm-relative positions** for the box translations: jog the arm to a landmark, such as the front edge of the table or the side boundary, and select **Get end position** on the arm's CONTROL card to read the x and y coordinates in the arm's coordinate frame. These are the numbers that fill the `REPLACE_WITH_MEASURED_FRONT_Y` and `REPLACE_WITH_MEASURED_SIDE_X` placeholders in the safety walls below.

All obstacle geometry is expressed against the world origin, which in this setup sits at the arm base, so the x and y coordinates you read from **Get end position** drop straight into the `translation` fields without any conversion.

Each obstacle geometry is a box defined by its `x`, `y`, and `z` dimensions (the box's full size in millimeters) and a `translation` (the box's center point in the parent frame). Two details trip people up:

- The `z` value in a box's dimensions is its height, but the `translation.z` you provide is the box's **center**, not its top or bottom surface. A 30 mm thick table sitting flush with the world origin at `z = 0` needs a `translation.z` of `-15`, half the thickness, because the box extends from `-30` to `0` and its center is at `-15`.
- The safety walls are thin, tall boxes. A wall that is 600 mm tall has `z: 600` for its dimension, but its `translation.z` is `300`, half the height, for the same reason.

### Add the table obstacle

Add a component:

- API: `rdk:component:gripper`
- Model: `erh:vmodutils:obstacle`

```json
{
  "name": "table",
  "api": "rdk:component:gripper",
  "model": "erh:vmodutils:obstacle",
  "attributes": {
    "geometries": [
      {
        "label": "table",
        "type": "box",
        "x": 1200,
        "y": 800,
        "z": 30,
        "translation": { "x": 0, "y": 0, "z": -15 },
        "parent": "world"
      }
    ]
  }
}
```

Replace the `x`, `y`, and `z` dimensions with your own measured table length, width, and thickness. If your table is not centered on the arm base in x and y, adjust `translation.x` and `translation.y` to match, using the values you read from **Get end position** when jogging to the table edges.

### Add the safety walls

Add two more `erh:vmodutils:obstacle` components, one per boundary you want to wall off:

```json
{
  "name": "safety-wall-front",
  "api": "rdk:component:gripper",
  "model": "erh:vmodutils:obstacle",
  "attributes": {
    "geometries": [
      {
        "label": "safety-wall-front",
        "type": "box",
        "x": 1200,
        "y": 20,
        "z": 600,
        "translation": {
          "x": 0,
          "y": "REPLACE_WITH_MEASURED_FRONT_Y",
          "z": 300
        },
        "parent": "world"
      }
    ]
  }
}
```

```json
{
  "name": "safety-wall-side",
  "api": "rdk:component:gripper",
  "model": "erh:vmodutils:obstacle",
  "attributes": {
    "geometries": [
      {
        "label": "safety-wall-side",
        "type": "box",
        "x": 20,
        "y": 800,
        "z": 600,
        "translation": {
          "x": "REPLACE_WITH_MEASURED_SIDE_X",
          "y": 0,
          "z": 300
        },
        "parent": "world"
      }
    ]
  }
}
```

Replace `REPLACE_WITH_MEASURED_FRONT_Y` and `REPLACE_WITH_MEASURED_SIDE_X` with the coordinates you measured for the front and side boundaries of your workspace. Both walls are 600 mm tall, so their `translation.z` is 300, half the height.

You can check your obstacle configuration against the companion repo's [obstacles-template.json](https://github.com/viam-devrel/pick-and-place/blob/main/config/obstacles-template.json), which has the full set with example measurements filled in. The full machine configuration, including all pose switches, is in [machine-fragment.json](https://github.com/viam-devrel/pick-and-place/blob/main/config/machine-fragment.json). Treat both as references to check your work against, not as files to import over what you configured by hand.

## Test the full static sequence

From the **CONTROL** tab, trigger the pose switches in this order:

```text
home-pose (2) -> approach-pose (2) -> Open gripper ->
grasp-pose (2) -> Grab -> travel-pose (2) ->
place-pose (2) -> Open gripper -> home-pose (2)
```

The **Open** and **Grab** buttons are the same gripper controls you used in Phase 2: **Grab** closes the fingers on a block and **Open** releases it.

As the arm moves, open the **3D scene** tab to watch its path alongside the table surface and the safety walls. The planner refuses to plan through configured geometry, so an obstacle conflict shows up as a planning failure in the logs, not as the arm passing through the obstacle. Open the **LOGS** tab alongside the 3D scene to catch any such planning failure in real time.

{{< checkpoint >}}
The arm completes the full sequence without stopping, the gripper opens and closes at the correct moments, and the LOGS tab shows no collision errors. If planning fails at a step, open the 3D scene tab to see what geometry the planner sees. Adjust the pose or the obstacle dimensions and retry. A common cause is an obstacle that is positioned slightly off from its physical counterpart, causing the planner to see the arm path as intersecting geometry that the physical arm actually clears.
{{< /checkpoint >}}

You now have a working static sequence. In Phase 4 you drive this same sequence from a Python script, replacing the manual switch triggers with code.

{{< workshop-nav >}}
