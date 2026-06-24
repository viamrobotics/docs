---
title: "Phase 3: Static positions and safety obstacles"
linkTitle: "3. Static positions"
type: "docs"
slug: "static-positions"
weight: 30
description: "Save the arm's key poses and configure WorldState obstacles, proving the hardware and motion planning work before you add perception."
workshop: "pick-and-place"
phase: 3
phase_total: 5
time_estimate: "20 minutes"
prev: "/tutorials/pick-and-place/configure-resources/"
next: "/tutorials/pick-and-place/local-python-script/"
languages: ["python"]
draft: true
---

<!-- TODO: companion repo viam-devrel/pick-and-place does not exist yet; these links are placeholders. -->

In this phase you move the arm through the full pick-and-place sequence using saved poses, with no perception yet. The goal is to prove that the hardware and motion planning work before you add detection, so that any bug you encounter later has only one new cause.

## Why static positions first

When you add perception and motion planning at the same time, a failure could live in detection, the frame transform, the pose math, the motion planner, or gripper timing, and there is no straightforward way to tell which. Saving fixed poses lets you run the full hardware loop first. Once the arm reliably travels through every stage of the sequence, perception becomes the only new variable when you move to Phase 4.

The table below shows what each step in the static sequence validates:

| Step | What it validates |
|------|-------------------|
| Arm reaches home pose | Observation position is safe and repeatable |
| Arm reaches approach pose | Arm can get above the workspace without collision |
| Arm reaches grasp pose | Descent distance is correct |
| Gripper opens and closes | Finger timing is right |
| Arm reaches travel pose | Safe carrying height clears obstacles |
| Arm reaches place pose | Bin position is correct |

## The key poses

Each saved pose has a specific role in the sequence:

| Pose | Purpose |
|------|---------|
| home-pose | Observation position above the workspace; the camera has a clear view of all cubes |
| approach-pose | Directly above the pick zone, roughly 80 to 100 mm above the highest cube |
| grasp-pose | At the cube with the gripper open; fingertips are level with the cube top |
| travel-pose | Safe carrying height that clears bins and table edges while holding a cube |
| [color]-bin-pose | Above each target sorting bin; one pose per color (red, blue, green) |

The approach pose and the grasp pose share the same x and y coordinates. The only motion between them is straight down the z axis, so if the arm drifts sideways during the descent you have a frame or calibration issue to investigate.

## Save each pose with the arm position saver

The machine is already configured with `arm-position-saver` switch components (model `erh:vmodutils:arm-position-saver`), one per pose. Each switch has an `arm` attribute pointing to `arm-1`. If you are setting up your own machine rather than using the pre-loaded configuration, add the `erh:vmodutils` module from the Viam registry and add a switch component for each pose.

For each pose, follow these steps:

1. Open the **CONTROL** tab and find the arm test card. Use the joint sliders to jog the arm into position.
2. Select **Get end position** on the arm card and note the x, y, and z values to confirm the arm is where you expect it.
3. On the pose's switch test card, set the switch to **position 1** to save the current joint positions.
4. Set the switch to **position 2** to confirm the arm returns to the saved pose from any starting position.

Repeat this process for home-pose, approach-pose, grasp-pose, travel-pose, red-bin-pose, blue-bin-pose, and green-bin-pose.

{{< alert title="Switch positions" color="note" >}}
On an `arm-position-saver` switch, position 1 saves the current joint positions, position 2 moves the arm to the saved pose, and position 0 clears any saved data. Always save with position 1 before you attempt position 2. Setting position 2 on an unsaved switch does nothing.
{{< /alert >}}

{{< checkpoint >}}
Set each saved switch to position 2 in turn. The arm should move to each pose you saved. If a switch does nothing when you set it to position 2, you have not saved it yet. Set position 1 first, then try position 2 again.
{{< /checkpoint >}}

## Teach the planner about obstacles with WorldState

The Viam motion planner is collision-aware, but it can only avoid geometry it knows about. Without a WorldState configuration, the planner avoids self-collisions only. When you add WorldState, the planner treats the table surface, the sorting bins, and any workspace boundary walls as hard obstacles it cannot plan through.

This matters both for correctness and for safety. Without the table obstacle, the planner might find a path that swings the arm through the table surface. Without bin obstacles, it might carry a cube directly through a bin wall. Virtual obstacle walls at the workspace boundary also prevent the arm from swinging into people standing nearby.

For this workshop you define three categories of obstacle: the table surface, one box per sorting bin, and safety walls at the workspace boundary.

## Measure and configure the obstacles

Your workshop facilitator provides the table and bin dimensions. To find each bin's position relative to the arm base, move the arm over the center of the bin and read the x and y values from **Get end position**. The z coordinate for a box obstacle is the center of the box, not its top surface.

The following JSON shows the structure for the obstacles array. Add this to the WorldState configuration for your motion service:

```json
{
  "obstacles": [
    {
      "label": "table",
      "geometries": [
        {
          "type": "box",
          "x": 1200,
          "y": 800,
          "z": 30,
          "translation": {
            "x": 0,
            "y": 0,
            "z": -15
          }
        }
      ]
    },
    {
      "label": "red-bin",
      "geometries": [
        {
          "type": "box",
          "x": 200,
          "y": 200,
          "z": 150,
          "translation": {
            "x": "[measured]",
            "y": "[measured]",
            "z": 75
          }
        }
      ]
    }
  ]
}
```

The table z translation is -15 because the box is 30 mm thick and its center sits 15 mm below the world origin at z = 0. Each bin's z translation is half its height because the box center is at the midpoint of the bin walls. Replace `[measured]` with the x and y values you read from the arm when centered over each bin, then add a matching entry for blue-bin and green-bin.

You can import a ready-made starting point from the companion repo: [obstacles-template.json](https://github.com/viam-devrel/pick-and-place/blob/main/config/obstacles-template.json). The full machine configuration, including all pose switches, is in [machine-fragment.json](https://github.com/viam-devrel/pick-and-place/blob/main/config/machine-fragment.json).

## Test the full static sequence

From the **CONTROL** tab, trigger the pose switches in this order:

```text
home-pose (2) -> approach-pose (2) -> open gripper ->
grasp-pose (2) -> close gripper -> travel-pose (2) ->
red-bin-pose (2) -> open gripper -> home-pose (2)
```

As the arm moves, open the **3D scene** tab and watch the arm's path to confirm it does not intersect the table surface or bin walls. If the path clips an obstacle boundary, the planner will report a collision error. Open the **LOGS** tab alongside the 3D scene to monitor for motion planning errors in real time.

{{< checkpoint >}}
The arm completes the full sequence without stopping, the gripper opens and closes at the correct moments, and the LOGS tab shows no collision errors. If planning fails at a step, open the 3D scene tab to see what geometry the planner sees. Adjust the pose or the obstacle dimensions and retry. A common cause is a bin obstacle that is positioned slightly off center, causing the planner to see the arm path as intersecting the bin wall even though the physical arm clears it.
{{< /checkpoint >}}

{{< workshop-nav >}}
