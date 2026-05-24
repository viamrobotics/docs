---
linkTitle: "Add a sub-part"
title: "Add a sub-part"
weight: 15
layout: "docs"
type: "docs"
description: "Attach a second computer to your existing machine as a sub-part so the main part can access its components."
date: "2026-04-16"
---

A sub-part is a second computer that the Viam cloud wires into your existing machine automatically.
The main part can access everything the sub-part has, and the whole system shows up as one machine in the app.
This page walks through adding one.
If you have not yet decided between a sub-part and a remote part, start at the [multi-machine overview](/hardware/multi-machine/).

## Before you start

- The main part is set up and online. If not, work through [Set up a machine](/set-up-a-machine/) first.
- You have the second computer ready: powered on, on the network, and able to reach the public internet. `viam-server` does not have to be installed yet.

## 1. Create the sub-part entry

In the Viam app:

1. Go to the machine's **CONFIGURE** tab.
2. Click the **+** icon next to the main part's name in the left sidebar.
3. Select **Sub-part**.
4. Give the sub-part a name (for example, `end-effector` or `line-cam-3`). Names are short, descriptive, and unique on this machine.
5. Click **Save**.

The sub-part now exists in the configuration. It is not yet running.

## 2. Install viam-server on the second computer

1. Click the **...** menu next to the sub-part's name in the **CONFIGURE** tab.
2. Select **View setup instructions**.
3. Follow the platform and install method selections, then run the install command on the second computer.

The install flow is the same one used for the main part.
See [Set up a machine](/set-up-a-machine/) for details on platform choices and troubleshooting.

## 3. Confirm the sub-part is online

Within about 30 seconds of install, the sub-part shows as **Live** in the **CONFIGURE** tab next to its name.
The main part's resource list now includes the sub-part's entries, although they will be empty until you add components.

If it does not come online, check:

- `viam-agent` is running on the second computer (`sudo systemctl status viam-agent` on Linux).
- The second computer has network access.
- `/etc/viam.json` on the second computer contains valid credentials. Re-run the install command if unsure.

## 4. Add components to the sub-part

Adding hardware to a sub-part works the same way as adding it to the main part.
The difference is where you click **+** in the sidebar: under the sub-part's name, not the main part's.
Any component you add there should be physically connected to the sub-part's computer.

See [How components work](/hardware/configure-hardware/) for the add-a-component flow.

## From your code

Resources on the sub-part appear in the same resource list as the main part's.
Calling them uses the same `from_robot` pattern as a local component:

```python
arm = Arm.from_robot(machine, "arm-1")               # on the main part
camera = Camera.from_robot(machine, "wrist-camera")  # on the sub-part
```

By default, sub-parts do not carry a name prefix, so you reference components on the sub-part by their configured names.

## Frames

By default, every sub-part sits at the world origin.
For spatial setups where the sub-part's hardware has a known physical position, configure the sub-part's frame.
For example, a camera mounted on an arm's end effector, or a sensor at a known offset from the main part's frame.
See [Frames across machines](/hardware/multi-machine/cross-machine-frames/).
