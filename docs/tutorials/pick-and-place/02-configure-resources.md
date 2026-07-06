---
title: "Phase 2: Configure resources"
linkTitle: "2. Configure resources"
type: "docs"
slug: "configure-resources"
weight: 20
description: "Add the gripper and camera to the arm from Phase 1, connect the three with frames, then verify each one from the control and 3D scene tabs."
workshop: "pick-and-place"
toc_hide: true
phase: 2
phase_total: 6
time_estimate: "15 minutes"
prev: "/tutorials/pick-and-place/platform-mental-model/"
next: "/tutorials/pick-and-place/static-positions/"
languages: ["python"]
---

You configured the arm in Phase 1. In this phase you add the two resources that work alongside it, a gripper and a camera, connect all three with frames, and confirm each one works from the CONTROL tab before moving on.

## The target state

By the end of this phase your CONFIGURE tab holds all three components: `arm-1` from Phase 1, plus the gripper and camera you add here.

| Name        | API                     | Model                   |
| ----------- | ----------------------- | ----------------------- |
| `arm-1`     | `rdk:component:arm`     | `viam:ufactory:xArm6`   |
| `gripper-1` | `rdk:component:gripper` | `viam:ufactory:gripper` |
| `cam-1`     | `rdk:component:camera`  | `viam:camera:realsense` |

You will not touch the vision service in this phase. The `shape-detector` and `vision-segment` services that let the machine find blocks by shape come later, in Phase 5, right before you write the code that calls them. For now, focus on the hardware.

## Configure the gripper

<!-- ASSET P2 configure-gripper (UI): gripper-1 config with arm: "arm-1" -->

Start with the gripper. On the **CONFIGURE** tab, click the **+** icon and select **Blocks**. Search for the `viam:ufactory:gripper` model and select it. Name it `gripper-1`.

{{< alert title="One module, two models" color="note" >}}
The `viam:ufactory` module you downloaded in Phase 1 provides both the arm model and this gripper model, so `viam-server` already has the code it needs. No second download happens here.
{{< /alert >}}

Set one attribute:

- `arm`: `"arm-1"`

This attribute is also a dependency: `gripper-1` cannot start until `arm-1` is running, because the gripper is physically mounted on the arm and controlled through the same connection. Save the config and check the **LOGS** tab: `gripper-1` comes online immediately, because the `viam:ufactory` module has been running since Phase 1.

## Configure the camera with a discovery service

<!-- ASSET P0 configure-add-discovery (UI+): add-component dialog, "realsense" searched, discovery / realsense:discovery result highlighted -->
<!-- ASSET P0 discovery-test-panel (UI+): realsense discovery TEST panel showing a camera config snippet with serial_number filled in -->
<!-- ASSET P2 configure-camera (UI): cam-1 realsense config, sensors color+depth, align_color_depth true, serial_number populated -->

You could add the camera by hand like the arm and gripper, but the RealSense module ships a **discovery service** that does the tedious part for you: it finds the connected camera and hands you a ready-made config with the correct serial number already filled in. A discovery service reports the hardware attached to a machine and suggests configurations for it, so you configure the right device without hunting for identifiers by hand. See [Discovery service](/reference/services/discovery/) for the general pattern.

### Add the discovery service

Click the **+** icon and select **Blocks**. Search for `realsense` and select the `discovery / realsense:discovery` service. Leave its name as the default and save the config.

Saving now is the moment `viam-server` fetches the `viam:realsense` module: the discovery service and the camera model both come from it, so the download happens once here, the same way `viam:ufactory` downloaded once for the arm and gripper. Watch the **LOGS** tab for the module download and the discovery service starting.

### Discover the camera

Open the discovery service's **TEST** panel. It lists every RealSense it detects on the machine, each as a copy-pasteable configuration snippet with that camera's `serial_number` already populated. With one camera connected you see one entry. Select **Add component** next to it to create a camera component from the snippet.

The discovered component arrives named `realsense-<serial_number>`, with `sensors` set to `["color", "depth"]` and `serial_number` already filled in. Rename it to `cam-1` so it matches the rest of this workshop, then add the one attribute discovery does not set:

- `align_color_depth`: `true`

Leave the discovered `sensors` and `serial_number` as they are; letting discovery set the serial number is the whole point of using the service. You do not need to set `width_px` or `height_px`; the module uses a supported default resolution, and pinning one that the camera cannot produce would fail the build.

`align_color_depth` is the attribute that makes perception work later. With it set to `true`, the module aligns each depth frame to the color frame, so a given pixel in the color image and the same pixel in the depth image describe the same physical point. The `vision-segment` service in Phase 5 relies on that alignment to turn a 2D detection into a 3D point cloud segment. Both `color` and `depth` must be in the `sensors` list for it to take effect.

Save the config and confirm in the **LOGS** tab that `cam-1` starts. Because `viam-server` already downloaded the `viam:realsense` module when you added the discovery service, the camera comes online with no second download.

{{< alert title="The discovery service has done its job" color="note" >}}
The discovery service is not part of the pick-and-place pipeline; it only helped you configure `cam-1`. Leave it in place to re-discover hardware later, or remove it once the camera works. The rest of the workshop does not use it.
{{< /alert >}}

## Connect the components with frames

<!-- ASSET P1 configure-arm-frame (UI): arm-1 card Frame editor, parent world, translation 0,0,0 -->
<!-- ASSET P0 configure-camera-frame (UI+): cam-1 Frame editor JSON, parent arm-1, translation -73,40,18 -->

Adding the arm, gripper, and camera tells `viam-server` how to talk to each one, but not where each sits in space. The motion service needs that spatial relationship: it has to know the gripper rides on the end of the arm and the camera looks out from the wrist, or it cannot plan a pick. You supply it by adding a **frame** to each component.

The three frames form a tree rooted at `world`:

```text
world
└── arm-1
    ├── gripper-1   (rides on the end effector)
    └── cam-1       (mounted on the wrist)
```

### Frame the arm

Open the `arm-1` card and select **Frame**. The default frame already describes what you want: parent `world`, translation `(0, 0, 0)`, no rotation. That places the arm's base at the origin of the world, and every other frame is measured from there. Leave the defaults and save.

### Frame the gripper

Open the `gripper-1` card and select **Frame**. Switch the editor to JSON and set:

```json
{
  "parent": "arm-1",
  "translation": { "x": 0, "y": 0, "z": 105 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

Parent `arm-1` attaches the gripper to the end of the arm, and `z: 105` places the gripper frame 105 mm out from the arm's end effector, at the gripper's tool center point. This is the point the motion service drives to a target when you call `motion.move` later in the workshop, and the reference the grasp math in Phase 5 builds on. This frame is separate from the `arm` attribute you set earlier: the attribute shares the arm's connection, while the frame tells the planner where the gripper sits.

### Frame the camera

Open the `cam-1` card and select **Frame**. Switch the editor to JSON and set:

```json
{
  "parent": "arm-1",
  "translation": { "x": -73, "y": 40, "z": 18 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 270 }
  }
}
```

Parent `arm-1` mounts the camera on the wrist so it moves with the arm. The translation places the camera's optical center relative to the end effector, and the 270-degree rotation around z lines the camera's axes up with the arm's. Save the config.

{{< alert title="These values match this workshop's hardware" color="note" >}}
The translation and orientation above describe the specific gripper and camera mount used in this workshop. If your hardware differs, work through the [frame calibration worksheet](https://github.com/viam-devrel/pick-and-place/blob/main/setup/frame-calibration-worksheet.md) to measure your own offsets, and see [Configure frames for an arm, gripper, and wrist camera](/motion-planning/frame-system/arm-gripper-camera/) for the full method.
{{< /alert >}}

## Test each resource from the CONTROL tab

<!-- ASSET P1 control-camera-stream (UI): CONTROL camera card, live color + depth -->
<!-- ASSET P1 control-arm-card (UI+): joint sliders + Get end position boxed -->
<!-- ASSET P1 control-gripper-grab (MOTION): gripper closing on a block via Grab, then Open releasing -->

Open the **CONTROL** tab. You should now see a test card for each of the three components you just added.

On the camera card, confirm you get a live feed:

{{< checkpoint >}}
The camera card shows a live color stream from `cam-1`. Because you configured both the `color` and `depth` sensors, switch the card to the depth view and confirm that stream updates too. If the card is blank, check the LOGS tab for a camera error before moving on.
{{< /checkpoint >}}

{{< alert title="The arm is about to move" color="caution" >}}
Jogging a joint slider moves the physical arm immediately. Before you touch a slider, confirm the workspace is clear, keep the e-stop within reach, and move one joint a small amount at a time. Large or combined joint moves can drive the arm into the table, the camera, or itself.
{{< /alert >}}

On the arm card, jog a joint with the sliders and confirm the arm moves. Then select **Get end position** and confirm it returns x, y, and z coordinates.

{{< checkpoint >}}
Jogging a joint slider moves the physical arm, and **Get end position** returns a coordinate rather than an error. If jogging does nothing, confirm `arm-1` shows as online in the CONFIGURE tab and that the LOGS tab has no connection errors for it.
{{< /checkpoint >}}

On the gripper card, place a block between the gripper fingers by hand, then select **Grab**. The fingers should close and hold the block. Select **Open** and confirm the fingers release it.

{{< checkpoint >}}
With a block between the fingers, **Grab** closes the fingers and the gripper holds the block without dropping it. **Open** releases the block. This grab-and-release is the same action your Python code performs later in the workshop when it picks a block and drops it in a bin. If your gripper card also shows a holding status indicator, it now reads true while the block is held and false once the gripper is open and empty.
{{< /checkpoint >}}

## The 3D scene tab

<!-- ASSET P0 3dscene-wrist-camera (MOTION): jog joint 1 and watch the cam-1 frame move with the arm (the wrist-camera insight) -->

Open the **3D scene** tab. You should see a rendered model of the arm and the `cam-1` frame positioned at the end of its wrist.

Jog joint 1 with the arm card's sliders and watch the 3D scene as the arm turns. The `cam-1` frame moves with the arm, because the camera is mounted on the wrist rather than fixed in the workspace.

{{< alert title="Why this matters later" color="note" >}}
Because the camera is wrist-mounted, every detection it makes is relative to wherever the arm happens to be pointed at that moment. In Phase 5 you will detect from a single known pose so that "camera space" always means the same thing. Notice that pose here; you will meet it again as the "detect from home" rule.
{{< /alert >}}

The frames you configured earlier are what make this work: because `cam-1`'s parent is `arm-1`, its frame rides along every time the arm moves. Confirm the relationship in the scene: the `cam-1` frame sits out at the wrist and tracks the arm as you jog it.

## Check your work

If you want to compare your configuration against a known-good version, the companion repo has a reference copy at [machine-fragment.json](https://github.com/viam-devrel/pick-and-place/blob/main/config/machine-fragment.json). Use it to check your work, not to import over what you just built by hand.

With `arm-1`, `gripper-1`, and `cam-1` all live and verified, you are ready for [Phase 3](/tutorials/pick-and-place/static-positions/), where you save a set of fixed arm poses and prove the full hardware sequence works before perception enters the picture.

{{< workshop-nav >}}
