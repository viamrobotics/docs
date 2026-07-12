---
title: "Phase 2: Configure the SO-ARM101"
linkTitle: "2. Configure the arm"
type: "docs"
slug: "configure-the-arm"
weight: 20
description: "Add the arm and gripper with the discovery service, verify them with test cards, and place the arm in the frame system."
workshop: "so-arm101-palletizing"
toc_hide: true
phase: 2
phase_total: 6
prev: "/tutorials/so-arm101-palletizing/platform-mental-model/"
next: "/tutorials/so-arm101-palletizing/teach-the-cell/"
languages: ["python"]
draft: true
---

In this phase you configure the arm and gripper, verify them with their test cards on the **CONTROL** tab, then place both in the frame system so the rest of the platform knows where they sit.

## Add the discovery service

Rather than typing the arm and gripper configs by hand, start with the SO-ARM101 module's **discovery service**. A discovery service reports the hardware attached to a machine and suggests configurations for it, so you configure the right components without hunting for serial ports or attribute names by hand. See [Discovery service](/reference/services/discovery/) for the general pattern.

On the **CONFIGURE** tab, click the **+** icon and select **Blocks**. Search for `so101` and select the `so101/discovery` result. Leave its name as the default and save the config. Saving is the moment `viam-server` downloads the SO-ARM101 module; the arm and gripper models you add later in this phase come from that same module, so the download happens only once.

Before you open the discovery service's test panel, know what it is looking for: the serial port your SO-ARM101 is connected to over USB.

- On Linux, the port shows up as `/dev/ttyUSB0` or `/dev/ttyACM0`.
- On macOS, look under `/dev/tty.*` for a name containing `usbmodem` or `usbserial`.

Open the discovery service's **TEST** panel. It scans for a connected SO-ARM101 and, if it finds one, returns ready-made configuration snippets for the arm and the gripper, with the detected `port` already filled in.

<!-- ASSET discovery-test-panel (UI): discovery service test panel with suggested components -->

With the arm connected and powered, select **Add component** next to each suggested snippet to create the arm and gripper components from it. If discovery does not find your arm, confirm the USB cable is connected and that no other program is holding the serial port open, then retry.

{{< alert title="Discovery has done its job" color="note" >}}
Like the config it suggests, the discovery service is not part of the pack sequence you build later in this workshop. Leave it in place if you expect to re-discover hardware, or remove it once the arm and gripper are configured.
{{< /alert >}}

## Add the arm component

If you used discovery, confirm the arm component it created has one attribute, `port`, set to your arm's serial port:

```json
{
  "port": "/dev/ttyUSB0"
}
```

If you are configuring the arm by hand instead, click the **+** icon, select **Blocks**, search for `so101`, and select the `so101/arm` result. Name it `arm`, paste the attribute above with your own port, and save.

Open the **CONTROL** tab and find the arm's test card. Test cards call the same API your Python code calls later in this workshop; jogging a joint here is a real API call that moves the hardware. Move one joint slider a small amount and press **Execute**, then watch the physical arm turn.

{{< alert title="The arm is about to move" color="caution" >}}
Keep the workspace clear and change one joint a small amount at a time. Large or combined joint moves can drive the arm into the table or itself.
{{< /alert >}}

{{< checkpoint >}}
Moving a joint slider and pressing **Execute** on the arm's test card moves the physical arm. If nothing moves, confirm the arm shows online in the CONFIGURE tab and check the LOGS tab for a serial connection error.
{{< /checkpoint >}}

## Add the gripper component

The gripper is the SO-ARM101's sixth servo, on the same serial bus as the other five, so its config looks almost identical to the arm's: the same `port` attribute, pointed at the same serial port.

If you used discovery, confirm the gripper component it created carries this same port:

```json
{
  "port": "/dev/ttyUSB0"
}
```

If you are configuring the gripper by hand, click the **+** icon, select **Blocks**, search for `so101`, and select the `so101/gripper` result. Name it `gripper`, set `port` to the same value as the arm's, and save.

Open the gripper's test card on the **CONTROL** tab. Press **Open** and watch the jaw open, then press **Grab** and watch it close.

{{< checkpoint >}}
Pressing **Open** and **Grab** on the gripper's test card opens and closes the physical jaw. If nothing moves, confirm the gripper shows online in the CONFIGURE tab and that its `port` matches the arm's.
{{< /checkpoint >}}

## Place the arm and gripper in the frame system

Adding the arm and gripper tells `viam-server` how to talk to them, but not where they sit in the cell. As Phase 1 covered, the frame system answers that question for every component in the workshop: a frame places a component relative to a parent, and every frame traces back to `world`. See [Frame system](/motion-planning/frame-system/overview/) for the general concept.

The **world frame** is the fixed reference point for the whole cell, the origin that every other position is measured from. Every frame in the system traces back to it. Placing the arm's frame with parent `world` and translation `(0, 0, 0)` puts the arm's base exactly at that origin.

That choice matters for the next phase. Because the arm's base is the world origin, any position you read from the arm, including the poses you capture by hand in Phase 3, is already a position in the world frame, with no conversion needed. You use the arm itself as your measuring tool, and what it reports is directly usable.

Open the arm's card on the **CONFIGURE** tab and select **Frame**. The default frame already describes parent `world`, translation `(0, 0, 0)`, and no rotation, so you can leave the defaults and save.

```json
{
  "parent": "world",
  "translation": { "x": 0, "y": 0, "z": 0 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

The gripper is a separate component with its own collision geometry, so it needs its own frame to place that geometry in the cell. You attach it to the arm. Open the gripper's card, select **Frame**, set its parent to `arm`, and leave the translation and rotation at zero:

```json
{
  "parent": "arm",
  "translation": { "x": 0, "y": 0, "z": 0 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

Attaching the gripper to the arm places its shape in the cell: the 3D scene draws the gripper on the end of the arm, and the motion service accounts for the gripper's shape when it plans, so it keeps the jaws clear of obstacles.

## See it in the 3D scene

Open the **3D scene** tab. The arm renders using the kinematics built into the `so101/arm` model, sitting at the frame you configured, with the gripper attached at its end point. This is the same view you will return to throughout the rest of the workshop to watch the pack sequence run.

<!-- ASSET 3dscene-arm (UI): 3D scene tab showing the SO-ARM101 model -->

Jog a joint on the arm's test card again and watch the 3D scene update alongside the physical arm.

{{< checkpoint >}}
The 3D scene shows the SO-ARM101 model, gripper included, at its current joint positions, and it updates as you jog a joint from the CONTROL tab. If the gripper is missing or floating away from the arm, recheck that its frame parent is set to `arm` with zero translation. If the scene is blank, confirm the arm's frame saved and that the arm shows online in the CONFIGURE tab.
{{< /checkpoint >}}

With the arm and gripper configured, verified, and placed in the frame system, you are ready for [Phase 3](/tutorials/so-arm101-palletizing/teach-the-cell/), where you map the physical cell, the staging spot and the pallet, into the arm's frame by hand.

{{< workshop-nav >}}
