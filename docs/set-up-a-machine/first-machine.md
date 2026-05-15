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

A wizard dialog opens with the heading **Install `viam-server`**.
Click **Next** to begin.

## 3. Tell the wizard about your hardware {#sbc-setup-instructions}

The wizard asks a few questions so it can build the right install command for your platform.
Answer each one by clicking the card that matches your setup:

- **Does your project have a separate board/computer?**
  Choose **Yes** if you'll install `viam-server` on a board or industrial PC connected to your hardware.
  Choose **No** if you're running on a laptop or desktop, typically for testing or development.
- **What kind of board is it?** or **What operating system?**
  Pick the matching card: **Raspberry Pi**, **NVIDIA Jetson**, or **Something else** for boards; **MacOS**, **Linux**, or **Windows** for laptops and desktops.
- **Operating system check.**
  Depending on what you picked, the wizard either confirms that your machine has a 64-bit Linux OS, walks you through installing one, or shows a command that verifies system requirements.

If you're using a single-board computer that doesn't come with an OS pre-installed, the wizard links to board-specific setup guides on the **Install an operating system** screen.
Install a 64-bit Linux OS on your board following that guide, then return to the wizard, check **I've installed a compatible OS on my `<board>`**, and click **Continue setup**.

## 4. Run the install command

The wizard reaches the **Download and install `viam-server`** screen with a platform-specific command.
The command embeds an API key so your machine can authenticate to Viam on its own.

Run the command on your compute device.

## 5. Wait for the success screen

After the install command finishes, the wizard polls for your machine's connection status.
When the wizard shows **Success! Your machine is connected.**, your machine is online and ready to configure.

This should happen within 30 seconds.
Click **Configure my machine** to close the wizard and return to the **CONFIGURE** tab.

{{< alert title="Tip" color="tip" >}}

To reopen the wizard later, open the machine status dropdown at the top of the machine page and click **View setup instructions** under the part name.
The wizard starts from the beginning each time; it does not remember where you left off.

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

## 6. Connect with code

Your machine is online. Now connect to it programmatically.

1. Go to your machine's page in the Viam app.
2. Click the **CONNECT** tab.
3. Select **SDK code sample**.
4. Choose your language (Python, TypeScript, Golang, C++, or Flutter).
5. Toggle **Include API key** to embed your credentials directly in the snippet.
6. Copy the code sample, install the SDK, and run it.

If the connection succeeds, the script prints your machine's available resources.

## What's next

- [Configure hardware](/hardware/configure-hardware/) to add cameras, motors, sensors, and other components to your machine.
- [Set up machines with the CLI](/set-up-a-machine/with-cli/) to provision additional machines from the command line.
