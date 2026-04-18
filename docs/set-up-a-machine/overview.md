---
linkTitle: "Set up a machine"
title: "Set up a machine"
weight: 1
layout: "docs"
type: "docs"
description: "Create a machine in the Viam app and install Viam on your compute machine."
date: "2025-01-30"
aliases:
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

Connect a machine to the Viam platform so you can configure, control, and monitor it from anywhere.
You'll create a machine in the Viam app, install Viam on your machine, and confirm it's online.

## 1. Create a machine in the Viam app

1. Go to [app.viam.com](https://app.viam.com) and log in (or create an
   account).
2. Create or select an organization, then create or select a location.
3. Click **Add machine**.
4. Give your machine a name (for example, `my-first-machine`). Click **Add machine**.

The app creates a machine entry and opens the **CONFIGURE** tab.
A banner prompts you to set up the machine part.

## 2. Open the setup page

1. Click **View setup instructions** in the banner.
2. In the wizard dialog that opens, click **Go to Advanced setup**.

## 3. Select your platform {#sbc-setup-instructions}

Use the **Platform you want to run on** dropdown to select the operating system and architecture of the compute machine for your robot, the computer to which you've attached cameras, sensors, arms, or other components.

Options include Linux / Aarch64, Linux / x86, Mac, Windows native, Windows (WSL), Linux / Armv7l, and ESP32.

If you're using a single-board computer, follow the setup guide for your board before continuing:

- [Raspberry Pi](/reference/device-setup/rpi-setup/)
- [NVIDIA Jetson Nano](/reference/device-setup/jetson-nano-setup/)
- [NVIDIA Jetson AGX Orin](/reference/device-setup/jetson-agx-orin-setup/)
- [BeagleBone AI-64](/reference/device-setup/beaglebone-setup/)
- [Orange Pi Zero 2](/reference/device-setup/orange-pi-zero2/)
- [Orange Pi 3 LTS](/reference/device-setup/orange-pi-3-lts/)

See [all supported boards](/reference/device-setup/) for the full list.

## 4. Select your installation method

If your platform supports multiple installation methods, a second dropdown appears.

- **viam-agent**: Choose this unless you have a reason not to.
- **manual**: Installs `viam-server` directly.

## 5. Run the install command

The setup page displays platform-specific install instructions.
Follow the steps shown on your compute machine.

## 6. Wait for confirmation

After the install command finishes, the setup page polls for your machine's connection status.
When the banner changes to **"Your machine is connected!"**, your machine is online and ready to configure.

This should happen within 30 seconds.

{{< alert title="Tip" color="tip" >}}

To return to the setup page later, click the **...** menu next to any part name in the **CONFIGURE** tab and select **View setup instructions**.

{{< /alert >}}

## Troubleshooting

{{< expand "Machine shows offline in the Viam app" >}}

- **Is `viam-agent` running?** On Linux, check with
  `sudo systemctl status viam-agent`. If it's not running, start it with
  `sudo systemctl start viam-agent`. This will also start `viam-server`.
- **Does the machine have network access?** Verify with `ping google.com`.
- **Is the config correct?** Inspect `/etc/viam.json` and confirm it contains
  valid credentials. If in doubt, re-run the install command from the Viam app.

{{< /expand >}}

{{< expand "\"Permission denied\" during install" >}}

- The install script requires `sudo`. Run the `curl` command exactly as shown on
  the setup page.
- On some systems, your user may not be in the `sudo` group. Consult your
  device's documentation for how to grant sudo access.

{{< /expand >}}

{{< expand "viam-server starts but immediately exits" >}}

- Check the logs: `sudo journalctl -u viam-server -n 50`.
- Common causes: invalid JSON in `/etc/viam.json`, port conflicts (another
  service on port 8080), or missing system libraries.

{{< /expand >}}

## 7. Connect with code

Your machine is online. Now connect to it programmatically.

1. Go to your machine's page in the Viam app.
2. Click the **CONNECT** tab.
3. Select **API keys** and copy your **API key** and **API key ID**.
4. Copy the **machine address** from the same tab.
5. Choose your language (Python, TypeScript, Golang, C++, or Flutter).
6. Copy the code sample, install the SDK, paste in your credentials, and run it.

If the connection succeeds, the script prints your machine's available resources.

## What's next

- [Configure hardware](/hardware/configure-hardware/) — Add cameras, motors, sensors, and other components to your machine.
