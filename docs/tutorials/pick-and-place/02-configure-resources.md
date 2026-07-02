---
title: "Phase 2: Configure resources"
linkTitle: "2. Configure resources"
type: "docs"
slug: "configure-resources"
weight: 20
description: "Configure the arm, gripper, and camera by hand, then verify each one from the control and 3D scene tabs."
workshop: "pick-and-place"
toc_hide: true
phase: 2
phase_total: 6
time_estimate: "20 minutes"
prev: "/tutorials/pick-and-place/platform-mental-model/"
next: "/tutorials/pick-and-place/static-positions/"
languages: ["python"]
---

In this phase you configure the three hardware resources every pick-and-place machine needs: an arm, a gripper, and a camera. Your machine starts with none of them. You add each one by hand, watch it come online, and confirm it works from the CONTROL tab before moving to the next.

{{< workshop-phases >}}

## The target state

By the end of this phase your CONFIGURE tab holds three components:

| Name        | API                     | Model                   |
| ----------- | ----------------------- | ----------------------- |
| `arm-1`     | `rdk:component:arm`     | `viam:ufactory:xArm6`   |
| `gripper-1` | `rdk:component:gripper` | `viam:ufactory:gripper` |
| `cam-1`     | `rdk:component:camera`  | `viam:camera:realsense` |

You will not touch the vision service in this phase. The `shape-detector` and `vision-segment` services that let the machine find blocks by shape come later, in Phase 5, right before you write the code that calls them. For now, focus on the hardware.

## Configure the arm

On the **CONFIGURE** tab, add a new component. In the add-component dialog, search for `xArm6` and select the `viam:ufactory:xArm6` result. Name the component `arm-1`.

Set the following attributes:

- `host`: the xArm controller's IP address, provided by your workshop facilitator
- `port`: `502`

You can leave `speed_degs_per_sec` and `acceleration_degs_per_sec_per_sec` unset for now; both are optional and default to safe values.

Save the config. This is the moment from Phase 1 made concrete: `viam-server` does not have `viam:ufactory:xArm6` built in, so it fetches the `viam:ufactory` module from the Viam registry and starts it. Open the **LOGS** tab and watch it happen: a log line for the module download, then one for the module starting, then `arm-1` itself coming online. The whole sequence usually takes well under a minute.

{{< alert title="Two components, one module" color="note" >}}
The `viam:ufactory` module provides both the arm model and the gripper model you configure next. You only pay the download cost once.
{{< /alert >}}

## Configure the gripper

Add another component. In the add-component dialog, search for the `viam:ufactory:gripper` model and select it. This model comes from the same `viam:ufactory` module as the arm. Name it `gripper-1`.

Set one attribute:

- `arm`: `"arm-1"`

This attribute is also a dependency: `gripper-1` cannot start until `arm-1` is running, because the gripper is physically mounted on the arm and controlled through the same connection. Save the config and check the **LOGS** tab again. Because `viam-server` already has the `viam:ufactory` module running from the previous step, `gripper-1` comes online immediately with no second download.

## Configure the camera

Add a third component. In the add-component dialog, search for `realsense` and select the `viam:camera:realsense` result. Name it `cam-1`.

Set the following attributes:

- `sensors`: `["color", "depth"]`
- `width_px`: `640`
- `height_px`: `480`

Save the config and confirm in the **LOGS** tab that `viam-server` downloads the `viam:camera-realsense` module and starts `cam-1`. This is a separate module from `viam:ufactory`, since it comes from a different publisher and family.

## Test each resource from the CONTROL tab

Open the **CONTROL** tab. You should now see a test card for each of the three components you just added.

On the camera card, confirm you get a live feed:

{{< checkpoint >}}
The camera card shows a live color stream from `cam-1`. If depth is available as a separate view, confirm that stream updates too. If the card is blank, check the LOGS tab for a camera error before moving on.
{{< /checkpoint >}}

On the arm card, jog a joint with the sliders and confirm the arm moves. Then select **Get end position** and confirm it returns x, y, and z coordinates.

{{< checkpoint >}}
Jogging a joint slider moves the physical arm, and **Get end position** returns a coordinate rather than an error. If jogging does nothing, confirm `arm-1` shows as online in the CONFIGURE tab and that the LOGS tab has no connection errors for it.
{{< /checkpoint >}}

On the gripper card, place a block between the gripper fingers by hand, then select **Grab**. The fingers should close and hold the block. Select **Open** and confirm the fingers release it.

{{< checkpoint >}}
With a block between the fingers, **Grab** closes the fingers and the gripper holds the block without dropping it. **Open** releases the block. This grab-and-release is the same action your Python code performs later in the workshop when it picks a block and drops it in a bin. If your gripper card also shows a holding status indicator, it now reads true while the block is held and false once the gripper is open and empty.
{{< /checkpoint >}}

## The 3D scene tab

Open the **3D scene** tab. You should see a rendered model of the arm and the `cam-1` frame positioned at the end of its wrist.

Jog joint 1 with the arm card's sliders and watch the 3D scene as the arm turns. The `cam-1` frame moves with the arm, because the camera is mounted on the wrist rather than fixed in the workspace.

{{< alert title="Why this matters later" color="note" >}}
Because the camera is wrist-mounted, every detection it makes is relative to wherever the arm happens to be pointed at that moment. In Phase 5 you will detect from a single known pose so that "camera space" always means the same thing. Notice that pose here; you will meet it again as the "detect from home" rule.
{{< /alert >}}

The exact camera mounting offset used to transform its frame into the arm's frame comes from your hardware setup guide or the pre-provisioned config, not from anything you configure in this phase. For now, just confirm the relationship: the frame exists, and it tracks the arm.

## Check your work

If you want to compare your configuration against a known-good version, the companion repo has a reference copy at [machine-fragment.json](https://github.com/viam-devrel/pick-and-place/blob/main/config/machine-fragment.json). Use it to check your work, not to import over what you just built by hand.

With `arm-1`, `gripper-1`, and `cam-1` all live and verified, you are ready for Phase 3, where you save a set of fixed arm poses and prove the full hardware sequence works before perception enters the picture.

{{< workshop-nav >}}
