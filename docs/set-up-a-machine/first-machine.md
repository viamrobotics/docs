---
linkTitle: "Set up your first machine"
title: "Set up your first machine"
weight: 1
layout: "docs"
type: "docs"
description: "Create a machine in the Viam app and install Viam on your compute device."
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

## 1. Create a machine in the Viam app

1. Go to [app.viam.com](https://app.viam.com) and log in (or create an account).
2. Open a location.
3. Click **Add machine**, enter a name (for example, `my-first-machine`), and click **Add machine** again.

The app opens your new machine's page on the **CONFIGURE** tab.
The tab shows a card titled **Set up your machine part**.

## 2. Open the setup wizard

In the **Set up your machine part** card, click **Set up**.

A wizard dialog will open with the heading **Install `viam-server`**.
Click **Next** to begin. Follow the guidance in the setup wizard to set up your machine on Viam.

## 8. Add hardware in the CONFIGURE tab

Your machine is connected, but it has no components configured yet.
To make the machine do anything, add the hardware you want to use through the **CONFIGURE** tab on your machine's page.

For each piece of hardware (camera, motor, sensor, arm, gripper, base):

1. Click the **+** button on the **CONFIGURE** tab.
2. Select **Component**.
3. Search for the model that matches your hardware. Search by manufacturer or hardware type (for example, `webcam`, `viam:raspberry-pi:rpi5`, `ufactory:xarm6`).
4. Name the component and click **Create**.
5. Fill in the required attributes (pin numbers, device paths, API keys) and click **Save**.

For walkthroughs by component type and the full configuration reference, see [Configure hardware](/hardware/configure-hardware/).

## What's next

- [Set up machines with the CLI](/set-up-a-machine/with-cli/) to provision additional machines from the command line.
