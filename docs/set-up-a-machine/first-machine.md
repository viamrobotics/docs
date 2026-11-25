---
linkTitle: "Set up your first machine"
title: "Set up your first machine"
weight: 1
layout: "docs"
type: "docs"
description: "Create a machine in the Viam app and install Viam on your compute device."
capabilities: ["device-provisioning"]
diataxis: how-to
date: "2025-01-30"
aliases:
  - /set-up-a-machine/overview/
  - /foundation/
  - /build/foundation/
  - /foundation/initialize-a-viam-machine/
  - /build/foundation/initialize-a-viam-machine/
  - /operate/install/
  - /operate/reference/prepare/
  - /installation/viam-server-setup/
  - /how-tos/configure/
  - /installation/prepare/
  - /installation/macos-install/
  - /installation/linux-install/
  - /installation/install/
  - /installation/install/linux-install/
  - /installation/install/macos-install
  - /getting-started/installation/
  - /getting-started/macos-install/
  - /getting-started/linux-install/
  - /installation/
  - /get-started/installation/
  - /operate/get-started/setup/
  - /operate/hello-world/building/
  - /operate/install/setup/
---

Connect your first machine to the Viam platform so you can configure, control, and monitor it from anywhere.
You'll create a machine in the Viam app, install Viam on your compute device, and confirm it's online.

A **machine** is the combination of your compute resources and hardware that you want to control using Viam.
Every machine has at least one **part**: the computer that runs Viam's software and is connected to one or more physical devices.
A part can be almost any computer, including your own Mac or PC.
For more, see [Machines and parts](/overview/#machines-and-parts).

## 1. Create a machine in the Viam app

1. Go to [app.viam.com](https://app.viam.com) and log in (or create an account).
2. Open a location.
3. Click **Add machine**, enter a name (for example, `my-first-machine`), and click **Add machine** again.

You can also start from the [**Machines**](https://app.viam.com/fleet/machines) page under **FLEET**.
Click **Add machine**, select a location, and click **Choose**.
To put the machine in a new location, type the location's name and click **Create location "&lt;name&gt;"** instead.
Then enter a name for the machine and click **Add machine**.

The app opens your new machine's page on the **CONFIGURE** tab.
The tab shows a banner titled **Set up your machine**.

## 2. Open the setup wizard

In the **Set up your machine** banner, click **Install**.

The setup wizard opens and asks **Does your project have a separate board/computer?**
Follow the guidance in the setup wizard to set up your machine on Viam.

If you don't have your hardware yet, you can simulate your machine instead:

- To run Isaac Sim on a Viam cloud GPU, choose **No hardware yet • Simulate it** in the setup wizard.
  Viam runs `viam-server` for the machine in the cloud, so you skip the rest of this page.
  Continue with [Run an Isaac Sim simulation](/simulate/isaac-sim/#start-the-machine).
  If the wizard doesn't show this option, simulation isn't turned on for your organization yet.
- To run MuJoCo on your own Mac or Linux computer, finish this step on that computer, then continue with [Run a MuJoCo simulation on your computer](/simulate/mujoco/).

For how the two simulators compare, see [Simulate a machine](/simulate/).

## 3. Add hardware in the CONFIGURE tab

Your machine is connected, but it has no components configured yet.
To make the machine do anything, add the hardware you want to use through the **CONFIGURE** tab on your machine's page.

For each piece of hardware (camera, motor, sensor, arm, gripper, base):

1. Click the **+** button on the **CONFIGURE** tab.
2. Select **Component**.
3. Search for the model that matches your hardware. Search by manufacturer or hardware type (for example, `webcam`, `viam:raspberry-pi:rpi5`, `viam:ufactory:xArm6`).
4. Name the component and click **Create**.
5. Fill in the required attributes (pin numbers, device paths, API keys) and click **Save**.

For walkthroughs by component type and the full configuration reference, see [Configure hardware](/hardware/configure-hardware/).
If you're simulating the machine, add simulated components instead, as described in [Simulate a machine](/simulate/).

## What's next

- [Set up machines with the CLI](/set-up-a-machine/with-cli/) to provision additional machines from the command line.
- [Simulate a machine](/simulate/) to develop and test code before your hardware arrives.
