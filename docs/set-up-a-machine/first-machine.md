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

A **machine** is what you configure and control in the Viam app: a computer running `viam-server`, plus the hardware attached to it.
A machine has one or more **parts**, and each part is one computer running `viam-server`.
Your compute device, such as a Raspberry Pi or a laptop, is a part of your machine.
For more, see [Machines and parts](/what-is-viam/#machines-and-parts).
<!-- TODO(draft): wording is provisional. Reconcile with the glossary and What is Viam? entries, and switch to the glossary_definition shortcode if it lands. -->

## 1. Create a machine in the Viam app

1. Go to [app.viam.com](https://app.viam.com) and log in (or create an account).
2. Open a location.
3. Click **Add machine**, enter a name (for example, `my-first-machine`), and click **Add machine** again.

The app opens your new machine's page on the **CONFIGURE** tab.
The tab shows a banner titled **Set up your machine**.

## 2. Open the setup wizard

In the **Set up your machine** banner, click **Install**.

The setup wizard opens and asks **Does your project have a separate board/computer?**
Follow the guidance in the setup wizard to set up your machine on Viam.

If you don't have your hardware yet, the setup wizard can also run your machine in a simulated environment in the cloud, so you can start configuring and testing right away.
See [Simulate a machine](/set-up-a-machine/simulate-a-machine/).
<!-- TODO(draft): confirm where the simulation option appears in the wizard (before or after the board/computer question) and whether it's gated by a feature flag at launch. -->

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

## What's next

- [Set up machines with the CLI](/set-up-a-machine/with-cli/) to provision additional machines from the command line.
