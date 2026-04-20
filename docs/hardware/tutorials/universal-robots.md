---
linkTitle: "Universal Robots arm"
title: "Set up a Universal Robots arm"
weight: 10
layout: "docs"
type: "docs"
description: "Configure a UR3e, UR5e, UR7e, or UR20 arm end-to-end: power-on, pendant network and security settings, remote control mode, and the Viam component configuration."
date: "2026-04-20"
---

This guide walks through everything required to get a Universal Robots e-Series arm talking to Viam. It covers the steps that are easy to miss: the pendant's network services (which ship disabled on new arms), the separate Local and Remote toggles, and the compute-machine-side verification.

For general information about the arm component API, frame configuration, and motion planning, see [Add an arm](/hardware/common-components/add-an-arm/).

## Before you start

You need:

- A supported arm: **UR3e**, **UR5e**, **UR7e**, or **UR20**. The [`viam:universal-robots`](https://app.viam.com/module/viam/universal-robots) module does not support UR10e or UR16e.
- A compute machine running `viam-server` (installed through `viam-agent`) on the same local network as the arm. Wired ethernet to the arm is strongly recommended.
- Administrative access to the arm's teach pendant.
- The arm mounted securely. Brake release causes the arm to settle under gravity; an unmounted arm will fall.

The pendant steps below use Polyscope 5 (the e-Series interface). Menu paths are from Polyscope 5.11; earlier versions are similar.

## 1. Power on and initialize the arm

1. Flip the main power switch on the controller box. The pendant boots Polyscope (about 30 seconds).
2. Confirm the emergency stop on the pendant is not pressed. If it is, twist clockwise to release.
3. Tap the robot status indicator at the bottom-left of the pendant screen. The **Initialize** panel opens.
4. Tap **ON**. Motor power engages, brakes stay applied. Status reads "Idle."
5. Tap **START**. You will hear a row of clicks as the brakes release. Status reads "Normal" (green).

The arm is now live.

## 2. Set the admin password (first boot only)

New arms prompt for a Polyscope admin password the first time you open Network or Security settings. There is no universal factory default. Set one now and keep a record of it. You will need it later when changing network services.

## 3. Set the arm's network address

The Viam module reaches the arm by IP, so the arm needs a stable address on the same subnet as the compute machine.

**Find the compute machine's subnet.** On the compute machine:

```sh
ip route
```

Look for the line starting `default via`. That is your gateway. The line for your wired interface shows the subnet (for example, `10.1.0.0/20 dev enp86s0 src 10.1.2.36`).

**Pick an address for the arm** on that subnet and outside the router's DHCP pool. If you don't know the DHCP range, either check the router's admin page or create a DHCP reservation so the router will never reassign your chosen address.

**Configure the pendant.** On the teach pendant:

1. Open the hamburger menu (top-right) → **Settings** → **System** → **Network**.
2. Select **Static Address**.
3. Enter:
   - **IP address:** the address you picked (for example, `10.1.0.84`).
   - **Subnet mask:** the mask that matches the compute machine's subnet (for example, `255.255.240.0` for a `/20`).
   - **Default gateway:** the gateway from `ip route`.
   - **DNS:** the same as the gateway, or any public resolver.
4. Tap **Apply**.

**Verify from the compute machine:**

```sh
ping <arm-ip>
```

Ping must succeed before moving on. If it doesn't, the arm and compute machine are not on the same network segment; check cabling and subnet values.

## 4. Enable network services

{{% alert title="Important" color="note" %}}
This step is the most common silent failure. Ping works even when these services are disabled, so the arm appears reachable while the Viam module fails with an opaque "Failed to connect to UR dashboard" error.
{{% /alert %}}

On the pendant:

1. If the arm is in Remote mode (top-right status bar), switch to **Local**. Security settings cannot be changed in Remote mode.
2. **Settings** → **Security** → **Services**.
3. Enable:
   - **Dashboard Server** (port 29999).
   - **Primary Client Interface** (port 30001).
   - **RTDE** (port 30004).
4. Leave Modbus TCP and XML-RPC disabled unless you specifically need them.
5. Apply.

New e-Series arms ship with most services disabled for security hardening. Enabling these three is the minimum the Viam module needs.

## 5. Enable remote control

Two separate toggles, both required:

1. **Settings** → **System** → **Remote Control** → toggle **Enable**.
2. Back out to the main Polyscope screen. Tap the mode indicator in the top-right corner and switch **Local** to **Remote**.

The arm must be in Remote mode for the Viam module to send motion commands. In Local mode the module will connect but report the arm as not controllable.

## 6. Verify the dashboard port

From the compute machine:

```sh
nc -zv <arm-ip> 29999
```

Expected: "succeeded" or "open" immediately. If the command hangs, a service in step 4 is still disabled. If it reports "refused," the arm is not fully initialized (go back to step 1).

## 7. Configure the Viam component

1. On your machine's page in the [Viam app](https://app.viam.com), open the **CONFIGURE** tab.
2. Click **+** → **Component**.
3. Search for your arm model: `ur3e`, `ur5e`, `ur7e`, or `ur20`. Select the `viam:universal-robots` result for your model. This adds both the module and the arm component.
4. Name the component (for example, `arm1`) and click **Create**.
5. In the component's attribute panel, paste:

   ```json
   {
     "host": "<arm-ip>",
     "speed_degs_per_sec": 60,
     "acceleration_degs_per_sec2": 8
   }
   ```

   Start with conservative speed and acceleration values. Raise them once you have confirmed motion behaves as expected.

6. Click **Save** (top-right).

The first save pulls down the module, which takes about a minute. Watch the **LOGS** tab to see the module download and connect to the arm. For the full attribute list, including trajectory tuning parameters and WiFi-specific options, see the [`viam:universal-robots` module README](https://github.com/viam-modules/universal-robots#configuration-and-usage).

## 8. Verify motion

1. Open the **CONTROL** tab.
2. Expand the arm component. Live joint angles should update as the arm moves or holds position.
3. In a safe pose with the workspace clear, jog one joint a few degrees using the joint controls.

If the arm moves, the setup is complete. Move on to [configuring a frame](/hardware/common-components/add-an-arm/#3-configure-a-frame-recommended) if you plan to use motion planning.

## Troubleshooting

{{< expand "Module logs: \"Failed to connect to UR dashboard\"" >}}

Ping works, the dashboard port does not. The network services in [step 4](#4-enable-network-services) are disabled or partially disabled. Put the arm in Local mode, enable Dashboard Server, Primary Client Interface, and RTDE, then return to Remote mode.

Confirm from the compute machine: `nc -zv <arm-ip> 29999` must return immediately with "succeeded."

{{< /expand >}}

{{< expand "Module connects but the arm reports as not controllable" >}}

The pendant is in Local mode. Tap the mode indicator in the top-right and switch to **Remote**.

A program running on the pendant also blocks external control. Stop any running program.

{{< /expand >}}

{{< expand "Motion commands are rejected with a protective stop" >}}

The arm has hit a safety limit, collision detection, or a torque threshold. Clear it from the pendant, or send a DoCommand to the arm component:

```json
{ "clear_pstop": "" }
```

Investigate what triggered the stop before continuing. Lower the configured speed and acceleration if motion was too aggressive for the payload.

{{< /expand >}}

{{< expand "Ping fails but the arm is plugged in" >}}

The arm and compute machine are on different network segments. Check:

- The ethernet cable is seated in the controller box (not the pendant).
- Both devices are on the same switch or router.
- The arm's static IP, subnet mask, and gateway match the compute machine's network (from `ip route`).

{{< /expand >}}

{{< expand "The admin password was set by someone else" >}}

There is no universal factory default. Try leaving the prompt blank, or contact whoever commissioned the arm. If neither works, Universal Robots support can walk you through a recovery procedure with proof of ownership. A factory reset through a USB recovery stick will clear all passwords but also wipes installations and programs.

{{< /expand >}}

## Related

- [Add an arm](/hardware/common-components/add-an-arm/): arm component API, frame configuration, and code samples.
- [`viam:universal-robots` module](https://github.com/viam-modules/universal-robots): full attribute list, DoCommand reference, and build instructions.
- [Motion planning](/motion-planning/): plan collision-free paths once the arm is configured.
