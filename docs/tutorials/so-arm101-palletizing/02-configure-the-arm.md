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
time_estimate: "20 minutes"
prev: "/tutorials/so-arm101-palletizing/platform-mental-model/"
next: "/tutorials/so-arm101-palletizing/teach-the-cell/"
languages: ["python"]
draft: true
---

In this phase you get the arm and gripper configured and verified on the **CONTROL** tab, then place the arm in the frame system so the rest of the platform knows where it sits.

## Add the discovery service

Rather than typing the arm and gripper configs by hand, start with the SO-ARM101 module's **discovery service**. A discovery service reports the hardware attached to a machine and suggests configurations for it, so you configure the right components without hunting for serial ports or attribute names by hand. See [Discovery service](/reference/services/discovery/) for the general pattern.

On the **CONFIGURE** tab, click the **+** icon and select **Blocks**. Search for `so101` and select the `devrel:so101:discovery` result. Leave its name as the default and save the config. Saving is the moment `viam-server` downloads the `devrel:so101` module; the arm, gripper, and calibration models you add later in this phase come from that same module, so the download happens only once.

Before you open the discovery service's test panel, know what it is looking for: the serial port your SO-ARM101 is connected to over USB.

- On Linux, the port shows up as `/dev/ttyUSB0` or `/dev/ttyACM0`.
- On macOS, look under `/dev/tty.*` for a name containing `usbmodem` or `usbserial`.

Open the discovery service's **TEST** panel. It scans for a connected SO-ARM101 and, if it finds one, returns ready-made configuration snippets for the arm and the gripper, with the detected `port` already filled in. The discovery service also suggests a calibration sensor you can add if the arm still needs calibrating.

<!-- ASSET discovery-test-panel (UI): discovery service test panel with suggested components -->

With the arm connected and powered, select **Add component** next to each suggested snippet to create the arm and gripper components from it. If discovery does not find your arm, confirm the USB cable is connected and that no other program (such as a LeRobot script) is holding the serial port open, then retry.

{{< alert title="Discovery has done its job" color="note" >}}
Like the config it suggests, the discovery service is not part of the pack sequence you build later in this workshop. Leave it in place if you expect to re-discover hardware, or remove it once the arm and gripper are configured.
{{< /alert >}}

## Calibrate the arm (first-time builds)

If discovery did not find an existing calibration file, your SO-ARM101 has not been calibrated yet and needs one guided pass before its joint positions are accurate. Add the `devrel:so101:calibration` sensor discovery suggested (or add it by hand with the same `port` as your arm), open its test panel, and follow the guided workflow: first you set the homing position, then you move each joint through its full range while the sensor records the min and max it sees. The sensor saves the result to a calibration file the arm and gripper read on startup.

This workshop does not reproduce the full calibration flow. If you built and calibrated your arm following the [prerequisites](/tutorials/so-arm101-palletizing/#prerequisites), skip this section. Otherwise, follow the guided steps in the [SO-ARM101 module documentation](https://app.viam.com/module/devrel/so101-arm) before continuing.

## Add the arm component

If you used discovery, confirm the arm component it created has one attribute, `port`, set to your arm's serial port:

```json
{
  "port": "/dev/ttyUSB0"
}
```

If you are configuring the arm by hand instead, click the **+** icon, select **Blocks**, search for `so101`, and select the `devrel:so101:arm` result. Name it `arm`, paste the attribute above with your own port, and save.

Open the **CONTROL** tab and find the arm's test card. Test cards call the same API your Python code calls later in this workshop; jogging a joint here is an API call, not a simulation. Move one joint slider a small amount and press **Execute**, then watch the physical arm turn.

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

If you are configuring the gripper by hand, click the **+** icon, select **Blocks**, search for `so101`, and select the `devrel:so101:gripper` result. Name it `gripper`, set `port` to the same value as the arm's, and save.

Open the gripper's test card on the **CONTROL** tab. Press **Open** and watch the jaw open, then press **Grab** and watch it close.

{{< checkpoint >}}
Pressing **Open** and **Grab** on the gripper's test card opens and closes the physical jaw. If nothing moves, confirm the gripper shows online in the CONFIGURE tab and that its `port` matches the arm's.
{{< /checkpoint >}}

## Place the arm in the frame system

Adding the arm and gripper tells `viam-server` how to talk to them, but not where the arm sits in the cell. As Phase 1 covered, the frame system answers that question for every component in the workshop, the same idea the simulated Viam 101 course uses for its palletizer: a frame places a component relative to a parent, and every frame traces back to `world`. See [Frame system](/motion-planning/frame-system/overview/) for the general concept.

Open the arm's card on the **CONFIGURE** tab and select **Frame**. Set the arm's frame so its base sits at the world origin: parent `world`, translation `(0, 0, 0)`, no rotation, which is what the default frame already describes. Leave the defaults and save. Keeping the base at the world origin means the poses you read back in Phase 3 are already world poses, which keeps your motion code simple.

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

You do not add a frame for the gripper. Unlike a gripper bolted onto a separate arm, the SO-ARM101's gripper is part of the arm module's own kinematic chain: the arm's kinematics already define a tool frame at the fingertip, the gripper's tool-center-point (TCP). Every motion command you send later in this workshop, through the motion service, already plans to that fingertip, with no separate frame to configure.

## See it in the 3D scene

Open the **3D scene** tab. The arm renders using the kinematics built into the `devrel:so101:arm` model, sitting at the frame you just configured. This is the same view you will return to throughout the rest of the workshop to watch the pack sequence run.

<!-- ASSET 3dscene-arm (UI): 3D scene tab showing the SO-ARM101 model -->

Jog a joint on the arm's test card again and watch the 3D scene update alongside the physical arm.

{{< checkpoint >}}
The 3D scene shows the SO-ARM101 model at its current joint positions, and it updates as you jog a joint from the CONTROL tab. If the scene is blank, confirm the arm's frame saved and that the arm shows online in the CONFIGURE tab.
{{< /checkpoint >}}

With the arm and gripper configured, verified, and placed in the frame system, you are ready for [Phase 3](/tutorials/so-arm101-palletizing/teach-the-cell/), where you map the physical cell, the staging spot and the pallet, into the arm's frame by hand.

{{< workshop-nav >}}
