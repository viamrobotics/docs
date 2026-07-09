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

In this phase you will teach an arm to move through a set of named poses that together form a pick-and-place cycle, and you let Viam's motion service create collision-free paths between them. First you will save each pose by hand, jogging the arm into position and recording where it is. Then you create obstacles so the Motion Service knows what to avoid when creating the collision free motion.

## Why static positions first

When you add perception and motion planning at the same time, a failure could live in detection, the frame transform, the pose math, the motion planner, or gripper timing, and there is no straightforward way to tell which. Saving fixed poses lets you run the full hardware loop first. In the following phase, you drive this same proven sequence from a Python script. Once the arm reliably travels through every stage of the sequence, perception becomes the only new variable when you reach it.

Pose-to-pose motion without perception is a real production workcell pattern: any time a part always lands in the same spot, a fixed sequence of saved poses is simpler and more reliable than running detection on every cycle.

Each move in that sequence also validates one part of your setup, which the next section lays out pose by pose.

## The key poses

You save five named poses. Run in order, they form one pick-and-place cycle:

<!-- ASSET P0 diagram-five-poses (DIAGRAM): the five poses in space (home/approach/grasp/travel/place) with the motion path. See plans/2026-07-02-pick-and-place-shot-list.md -->

```text
home      observe and rest, above the workspace
  │
  ▼
approach  standoff directly above the block
  │  gripper.open()
  ▼
grasp     down at the block
  │  gripper.grab()
  ▼
travel    lift clear of obstacles
  │
  ▼
place     above the bin
  │  gripper.open()
  ▼
home      back to the start
```

Each pose has a specific role, and reaching it cleanly validates one part of your setup:

| Pose          | Purpose                                                                                   | What reaching it validates                                        |
| ------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| home-pose     | Observation position above the workspace; the wrist camera has a clear view of the blocks | Observation position is safe and repeatable                       |
| approach-pose | Standoff directly above the pick zone, roughly 80 to 100 mm above the highest block       | Arm can get above the workspace without collision                 |
| grasp-pose    | At the block, gripper open and ready to close; fingertips are level with the block top    | Descent distance is correct and the gripper's finger timing works |
| travel-pose   | Safe carrying height that clears obstacles while holding a block                          | Safe carrying height clears obstacles                             |
| place-pose    | Above the bin where blocks are dropped                                                    | Bin position is correct                                           |

The approach pose and the grasp pose share the same x and y coordinates. The only motion between them is straight down the z axis, so if the arm drifts sideways during the descent you have a frame or calibration issue to investigate.

## Save each pose with the arm position saver

You configure pose saving by hand, the same way you configured the arm, gripper, and camera in Phases 1 and 2.

On the **CONFIGURE** tab, click the **+** icon and select **Blocks**. Search for `arm-position-saver`, select the `vmodutils/arm-position-saver` result, and name it `home-pose`. This is the first model you use from the `erh:vmodutils` module, so `viam-server` downloads that module now; the same module also provides the `vmodutils/obstacle` model you configure later in this phase, so it downloads only once.

The `arm-position-saver` is a **switch**: a resource whose numbered positions each trigger an action instead of reporting a value. You use two of its positions, one to save the arm's current joint positions ("update config") and one to replay them ("go to"). Throughout this phase, "the switch" refers to this pose-saver resource.

Set one attribute:

```json
{
  "arm": "arm-1"
}
```

This attribute is also a dependency, the same way `gripper-1` depends on `arm-1`: the switch cannot save or recall a pose until the arm it points at is running.

{{< alert title="The arm will move" color="caution" >}}
The steps in this phase move the physical arm, both when you jog it into position and when you set a switch to "go to" (position 2) to replay a saved pose. Keep the workspace clear and the e-stop within reach. Verify each pose individually before you run the full sequence at the end of the phase.
{{< /alert >}}

With the `home-pose` switch added, save and verify it. Home is your observation pose, so jog the arm to a spot above the workspace where the wrist camera has a clear, unobstructed view of the blocks; Phase 5 detects from exactly this pose.

You have two ways to jog the arm on its CONTROL card, and you can mix them:

- **Joint control (`MoveToJointPositions`)** sets each joint angle directly. Move one joint slider a small amount, press **Execute**, and that joint rotates. It is the most predictable way to make coarse changes and to lift the arm clear before repositioning.
- **End-effector control (`MoveToPosition`)** moves the tip of the arm to a Cartesian target instead of setting joints. Press **Current position** to load the arm's current pose into the fields, then change a coordinate and press **Execute**. The values are millimeters in the world frame at the arm base: raising or lowering **z** moves the gripper straight up or down, while **x** and **y** slide it horizontally across the workspace. Change one value by a small amount and watch the arm, or the 3D scene, to learn which way each axis points for your setup. Use this to nudge the gripper in a specific direction without solving for joint angles.

Run these four steps to save and verify the pose:

1. On the arm test card, jog the arm into position using joint control, end-effector control, or a mix of the two.
2. Press **Current position** under **MoveToPosition** and note the x, y, and z values to confirm the arm is where you expect it.
3. On the switch test card, set the switch to **update config** (position 1) to save the current joint positions.
4. Set the switch to **go to** (position 2) to confirm the arm returns to the saved pose from any starting position.

Setting the switch to **update config** writes the current joint positions straight into the switch's own configuration. Unlike the components you added in Phases 1 and 2, there is no separate **Save** step here: the pose is persisted as soon as you trigger position 1, and you can see the saved joint values appear in the switch's config JSON:

```json
{
  "arm": "arm-1",
  "joints": [
    0.0000025790882318688095, -0.7929777503013611, -0.8206289410591125,
    -6.174358873067831e-7, 1.611369013786316, 2.2541650324114926e-8
  ],
  "motion": "",
  "vision_services": [],
  "constraints": {},
  "extra": {}
}
```

The `joints` array holds the six joint angles, in radians, captured the moment you triggered position 1; `arm` is the dependency you set earlier, and the remaining fields stay at their defaults for this workshop. Triggering **update config** again overwrites `joints` with wherever the arm is now, which is why you jog to the pose you want before saving.

<!-- ASSET P0 control-armsaver-switch (UI+): arm-position-saver switch card with position 1 = save and 2 = execute annotated -->

{{<imgproc src="/tutorials/pick-and-place/control-armsaver-switch.png" resize="1200x" declaredimensions=true alt="The arm-position-saver switch test card with its update config and go to positions.">}}

Now that `home-pose` is saved, open its resource card on the **CONFIGURE** tab and use the **Duplicate** feature to create a copy. Rename the copy to `approach-pose`, and its `arm` attribute carries over automatically since it is already set to `"arm-1"`. Duplicate three more times for `grasp-pose`, `travel-pose`, and `place-pose`. This is faster than adding five switches from scratch and less error-prone, since you only type the `arm` attribute once.

<!-- ASSET P1 configure-duplicate-feature (UI+): the resource Duplicate control highlighted -->

{{<imgproc src="/tutorials/pick-and-place/configure-duplicate-feature.png" resize="1200x" declaredimensions=true alt="A resource card menu with the Duplicate option.">}}

Run the same four save-and-verify steps for each of the four new poses: jog the arm into position, confirm it with **Current position** under **MoveToPosition**, set the switch to "update config" to save, and set it to "go to" to confirm the arm returns.

{{< alert title="Switch positions" color="note" >}}
On an `arm-position-saver` switch, position 1 saves the current joint positions and position 2 moves the arm to the saved pose. Position 0 is the idle resting state the switch returns to after a save or a move; it does not clear the saved pose. Always save with position 1 before you attempt position 2. Setting position 2 on an unsaved switch does nothing.
{{< /alert >}}

{{< checkpoint >}}
Working one pose at a time, set each saved switch to position 2 and confirm the arm moves to the pose you saved. Check that `home-pose` still gives the wrist camera a clear view of the blocks. If a switch does nothing when you set it to position 2, you have not saved it yet; set position 1 first, then try position 2 again.
{{< /checkpoint >}}

## Teach the planner about obstacles

The Viam motion planner is collision-aware, but it can only avoid geometry it knows about. Without any obstacle configuration, the planner avoids self-collisions only. Once you add obstacle geometry, the planner treats the table surface and the workspace boundary as hard obstacles it cannot plan through.

This matters both for correctness and for safety. Without the table obstacle, the planner might find a path that swings the arm through the table surface. Virtual safety walls at the workspace boundary also prevent the arm from swinging into people standing nearby. This is not just a classroom convenience: it is the same pattern you would use to keep a production workcell's motion planner honoring the real boundaries of its cell.

In this workshop you configure two types of obstacles: the table surface and two safety walls at the workspace boundary.

## Obstacles as components

An obstacle can be configured as an `erh:vmodutils:obstacle` component you add on the **CONFIGURE** tab, the same way you added the arm, gripper, and camera. This obstacle model uses the gripper API, so once configured, each obstacle has the same control UI as a gripper. This is purely as a resource container for geometry.

The obstacle geometry is then automatically included in the world state the motion service uses to plan a safe path for the arm to a target position in 3D space.

### Add the table obstacle

Start with the table. The 3D scene below is the goal for this section: the table surface and two safety walls rendered around the arm, so the motion planner treats them as hard boundaries it cannot plan through.

<!-- ASSET P1 3dscene-obstacles (UI): 3D scene rendering the table + wall boxes around the arm -->

{{<imgproc src="/tutorials/pick-and-place/3dscene-obstacles.png" resize="1200x" declaredimensions=true alt="The 3D scene showing the table and safety-wall obstacle boxes around the arm.">}}

Click the **+** icon and select **Blocks**, then search for `obstacle` and select the `vmodutils/obstacle` result. Name it `table`. Paste the box dimensions into the attributes editor, then click **Frame** on the component card and set the frame that positions it in the world.

The attributes hold the box **dimensions**, its full size in millimeters:

```json
{
  "geometries": [
    {
      "type": "box",
      "x": 1200,
      "y": 800,
      "z": 30
    }
  ]
}
```

The frame places the box in the world. `parent` is `world`, and `translation` is where the box **center** sits relative to the world origin, which in this setup is the arm base:

```json
{
  "parent": "world",
  "translation": { "x": 0, "y": 0, "z": -15 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

The one detail that trips people up is that `translation.z` is the box's **center**, not its top or bottom surface. The world origin sits at table-top height (`z = 0`), so a 30 mm thick table needs `translation.z` of `-15`, half its thickness: the box extends from `-30` up to `0`, and its center is at `-15`. The safety walls you add next use the same rule in the other direction: a 600 mm tall wall gets `translation.z` of `300` so it rises from `0` to `600`. An obstacle only appears in the 3D scene and the planner's world state once it has this frame.

### Measure your workspace

<!-- ASSET P1 photo-measure-workspace (PHOTO): tape measure on the table / measuring a boundary -->

The dimensions and translation above are examples. Replace them with measurements of your own table and workspace boundary. You need two kinds of measurement, and each one feeds a different part of the config:

- **Tape-measure dimensions** for the box sizes: the table's length, width, and thickness go into the table obstacle's `x`, `y`, and `z`. Use the tape measure for how big each box is.
- **Arm-relative positions** for the box translations: jog the arm to a landmark, such as the front edge of the table or the safe working boundary behind the arm, and press **Current position** under **MoveToPosition** on the arm's CONTROL card to read the x and y coordinates in the arm's coordinate frame. Because all obstacle geometry is expressed against the world origin at the arm base, these coordinates drop straight into the frame's `translation` fields without any conversion. They fill the `REPLACE_WITH_MEASURED_FRONT_X` and `REPLACE_WITH_MEASURED_BACK_X` placeholders in the safety walls below.

If your table is not centered on the arm base in x and y, adjust the frame's `translation.x` and `translation.y` to match, using the values you read from **Current position** when jogging to the table edges.

### Add the safety walls

Add two more `erh:vmodutils:obstacle` components the same way, one per boundary you want to wall off. Each has its box dimensions in `geometries` and a `world`-parented `frame` that places it.

`safety-wall-front` attributes:

```json
{
  "geometries": [{ "type": "box", "x": 20, "y": 1200, "z": 600 }]
}
```

`safety-wall-front` frame:

```json
{
  "parent": "world",
  "translation": {
    "x": "REPLACE_WITH_MEASURED_FRONT_X",
    "y": 0,
    "z": 300
  },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

`safety-wall-back` attributes:

```json
{
  "geometries": [{ "type": "box", "x": 20, "y": 1200, "z": 600 }]
}
```

`safety-wall-back` frame:

```json
{
  "parent": "world",
  "translation": {
    "x": "REPLACE_WITH_MEASURED_BACK_X",
    "y": 0,
    "z": 300
  },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

Replace `REPLACE_WITH_MEASURED_FRONT_X` and `REPLACE_WITH_MEASURED_BACK_X` with the coordinates you measured for the front and back boundaries of your workspace. Both walls are 600 mm tall, so their frame `translation.z` is 300, half the height.

You can check your obstacle configuration against the companion repo's [obstacles-template.json](https://github.com/viam-devrel/pick-and-place/blob/main/config/obstacles-template.json), which has the full set with example measurements filled in. The full machine configuration, including all pose switches and obstacles, is in [machine-fragment.json](https://github.com/viam-devrel/pick-and-place/blob/main/config/machine-fragment.json). Treat both as references to check your work against, not as files to import over what you configured by hand.

## Test the full static sequence

<!-- ASSET P2 logs-clean-sequence (UI): LOGS with no collision errors after the run -->

From the **CONTROL** tab, trigger the pose switches in this order:

```text
home-pose (2) -> approach-pose (2) -> Open gripper ->
grasp-pose (2) -> Grab -> travel-pose (2) ->
place-pose (2) -> Open gripper -> home-pose (2)
```

The **Open** and **Grab** buttons are the same gripper controls you used in Phase 2: **Grab** closes the fingers on a block and **Open** releases it.

<!-- ASSET P0 static-sequence (MOTION): the arm running the full static loop home->approach->grasp->travel->place->home -->

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/7wRyUKvnjSg">}}

As the arm moves, open the **3D scene** tab to watch its path alongside the table surface and the safety walls.

The planner refuses to plan through configured geometry, so an obstacle conflict shows up as a planning failure in the logs, not as the arm passing through the obstacle. Open the **LOGS** tab alongside the 3D scene to catch any such planning failure in real time.

{{< checkpoint >}}
At this point you have triggered the full sequence manually, one pose at a time: the arm reaches every pose, the gripper opens and closes at the correct moments, and the LOGS tab shows no collision errors. For each move, the motion service planned a collision-free path, steering the arm around the table and the safety walls you configured rather than through them. If planning fails at a step, open the 3D scene tab to see what geometry the planner sees, then adjust the pose or the obstacle dimensions and retry. A common cause is an obstacle positioned slightly off from its physical counterpart, so the planner sees the arm path as intersecting geometry that the physical arm actually clears.
{{< /checkpoint >}}

You now have a working static sequence. In Phase 4 you drive this same sequence from a Python script, replacing the manual switch triggers with code.

{{< workshop-nav >}}
