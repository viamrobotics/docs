---
title: "Common Errors & Known Issues"
linkTitle: "Common Errors"
weight: 50
type: "docs"
description: "A guide to troubleshooting a Viam-based machine or system of machines with fixes to common problems."
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

This document lists common errors encountered when working with `viam-server` and the [Viam app](https://app.viam.com), and provides simple steps to resolve them.
While many common issues and their possible resolutions are presented here, this list is not comprehensive.

To view logs or get a remote shell on a machine see [Troubleshoot](/manage/troubleshoot/troubleshoot/).

If you have encountered an error that is not listed here, we'd love to hear from you on our [Community Discord](https://discord.gg/viam)!
Please post the error message you received along with how you were able to trigger it and we'll see if we can help.

## Status

For information on the status of [app.viam.com](https://app.viam.com), visit [status.viam.com](https://status.viam.com/).

## Common installation errors

### The authenticity of host 'hostname.local' can't be established

**Description:** When following our [installation guides](/installation/viam-server-setup/), you will likely encounter this message the first time you try to make an `ssh` connection to your newly-imaged {{< glossary_tooltip term_id="board" text="board" >}}.
This is expected: `ssh` is advising you that it has not yet connected to this address, and prompts you for how to proceed.

**Solution:** The message will ask `Are you sure you want to continue connecting?`.
Type `yes` and then press the return key to continue with the connection.
You should receive a successful confirmation message similar to: `Warning: Permanently added 'hostname.local' to the list of known hosts.`
This is only required for the first `ssh` connection you make to a newly-imaged board.

### ssh: connect to host hostname.local port 22: Host is down

**Description:** Your computer is not able to connect to the {{< glossary_tooltip term_id="board" text="board" >}} through `ssh`.

**Solution:** Ensure that both your computer and the board itself are connected to the internet, and verify each of the following:

- If you are on a Windows computer, be sure that you do not have an outgoing firewall rule preventing `ssh` connections over port `22`.
- Your `ssh` connection string should resemble the following: `ssh username@hostname.local`.
  Be sure that you match hostname, username, and password exactly to what you initially configured when imaging your board.
- If you are still unable to connect, restart your board and try your `ssh` connection again after a few minutes.
- If that fails, try re-imaging your board following the [installation guide](/installation/viam-server-setup/) appropriate for your board.
  - If using the [Raspberry Pi installation guide](/installation/prepare/rpi-setup/), be sure to carefully enter the configuration details under the **Advanced Options** (gear icon) button on the [Raspberry Pi imager](https://www.raspberrypi.com/software/) before you re-image your board.
  - If you re-imaged your board and provided a different hostname, you may need to accept the `ssh` host key again by typing `yes` when prompted.
  - If you re-imaged your board and provided the same hostname, you may see an error message similar to `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`.
    - If so, edit your `~/.ssh/known_hosts` file to delete any single lines that begin with the board hostname you specified (like `hostname.local` or similar).
    - Afterwards, when you go to `ssh` to your board again, you will need to accept the `ssh` host key once more by typing `yes` when prompted.

### ssh: connect to host hostname port 22: Connection timed out

**Description:** Your computer is not able to connect to the {{< glossary_tooltip term_id="board" text="board" >}} through `ssh` before reaching a timeout.

**Solution:** Depending on your local network and board, it may take a minute or two for your `ssh` connection to successfully reach the board.

- If you have just powered on or restarted your board, wait a few minutes and then try your connection again.
  Depending on your board, it may take a few minutes for the `ssh` service to be ready to receive connections.
- If you encounter this error once or twice, try your `ssh` command again and wait until it completes.
- If the error persists, try the solutions presented for the `Host is down` error message above.

### Something went wrong trying to read the squashfs image

**Full Error:** `Something went wrong trying to read the squashfs image. Open dir error: No such file or directory`

**Description:** The `viam-server` [installation](/installation/viam-server-setup/) or [update](/installation/manage-viam-server/#update-viam-server) process may have been interrupted partway, with some files either partially-written or missing.

**Solution:** Reinstall `viam-server` following the [installation instructions](/installation/viam-server-setup/).

### AppImages require FUSE to run

**Related Error:** `dlopen(): error loading libfuse.so.2`

**Description:** `viam-server` is distributed for Linux as an [AppImage](https://appimage.org/), which requires FUSE (Filesystem-in-Userspace) version 2.
FUSE version 2 is included in almost all modern Linux distributions by default, but some older Linux distros or minimal installs might not provide it out of the box, and some newer systems may ship with FUSE version 3 installed by default, which is not compatible with `viam-server`.
For example, the latest Raspberry Pi OS (Debian GNU/Linux 12 bookworm) includes FUSE version 3 as its default FUSE installation, and requires FUSE version 2 to be installed as well to support `viam-server`.

In addition, if you are installing `viam-server` within a Docker container, you may also experience this error due to its default security restrictions.
FUSE is not required for macOS installations of `viam-server`.

{{% alert title="Important" color="note" %}}
`viam-server` requires FUSE version 2 (`libfuse2`), _not_ FUSE version 3 (`fuse3` or `libfuse3`) or versions of FUSE previous to FUSE version 2 (`fuse`).
To support a `viam-server` installation, you must install `libfuse2`.
{{% /alert %}}

**Solution:** If you receive this error, install FUSE version 2 on your Linux system according to one of the following steps:

- If installing `viam-server` on a Raspberry Pi running Raspberry Pi OS (Debian GNU/Linux 12 bookworm or later), install FUSE version 2 with the following command:

  ```sh {class="command-line" data-prompt="$"}
  sudo apt install libfuse2
  ```

- If installing `viam-server` on Ubuntu, install FUSE version 2 with the following command:

  ```sh {class="command-line" data-prompt="$"}
  sudo add-apt-repository universe
  sudo apt install libfuse2
  ```

- If installing `viam-server` on a different Linux distribution, see the [AppImage FUSE troubleshooting article](https://github.com/AppImage/AppImageKit/wiki/FUSE) for more information.

- If installing `viam-server` on a Docker image, see [I get some errors related to something called "FUSE" - AppImage documentation](https://docs.appimage.org/user-guide/troubleshooting/fuse.html) for Docker-specific troubleshooting steps.

### PulseAudio: Unable to connect: Connection refused

**Additional Error:** `jack server is not running or cannot be started`

**Description**: When configuring a Linux {{< glossary_tooltip term_id="board" text="board" >}}, Linux installations with broken or misconfigured sound libraries may experience one or both of these errors, even if not using audio components in the machine configuration.

**Solution:** Consult the documentation for your Linux OS and chosen sound library for guidance on installing any missing software dependencies.
For example, if you are using `jackd` and `PulseAudio` on a Raspberry Pi, you can run the following to install any missing dependencies:

```sh {class="command-line" data-prompt="$"}
sudo apt install jackd qjackctl libpulse-dev pulseaudio
```

This error can be safely ignored if you do not intend to use audio on your machine.

## Common Viam App Errors

### Failed to connect; retrying

**Description:** the [Viam app](https://app.viam.com) is unable to communicate with your machine, and will attempt to reconnect every few seconds until it is able to do so.
When a machine is disconnected, it will continue to run with its locally-cached current configuration, but will not be accessible for remote control or configuration through the Viam app.

**Solution:** Check the following to ensure your machine is accessible to the Viam app:

- Is the {{< glossary_tooltip term_id="board" text="board" >}} component connected to the internet?
- Is the `ssh` service configured and running locally on the board?
- Is the `viam-server` service running locally on the board?
  You can check by running `sudo systemctl status viam-server` from within an `ssh` session to the board.
  It should be listed as `active (running)`.

  - If it is listed as `stopped` or `failed`, you can try restarting it with `sudo systemctl start viam-server`.
  - If the command returns the message `Unit viam-server.service could not be found`, be sure you have followed the [installation instructions for your board](/installation/viam-server-setup/#platform-requirements), and then followed the {{< glossary_tooltip term_id="setup" text="setup instructions" >}}.
  - If none of the above succeed in getting `viam-server` up and running, check the logs on your board for any pertinent error messages.
    Depending on your board's specific Linux OS, you might use a command similar to the following to show the 50 most recent log messages from `viam-server`. Run this command from within an `ssh` session to the board:

    ```sh {class="command-line" data-prompt="$"}
    grep 'viam-server' /var/log/syslog | tail -50
    ```

### Error: cannot parse config: JSON: cannot unmarshal string into Go struct

**Full Error:** `Error: cannot parse config: JSON: cannot unmarshal string into Go struct field Component.components.frame of type float64.`

**Description:** A [frame](/services/frame-system/) attribute may be malformed, and is preventing the parsing of the component's configuration.

**Solution:** Check the **CONFIGURE** tab for your machine in the [Viam app](https://app.viam.com) and look for a `frame` attribute, either in **Frame** or **JSON** mode.
If you see a `frame` attribute that you didn't create yourself, delete the whole `frame` object from the JSON config.
In **JSON** mode, it will resemble the following:

```json
"frame": {
   "orientation": {
      "value": {}
   },
   "parent": "",
   "translation": {
      "x": "",
      "y": "",
      "z": ""
   }
}
```

## Known application and plugin conflicts

### macOS applications

None at this time.

### Windows applications

None at this time.

### Linux applications

None at this time.

### Browser plugins

**Chrome plugin: Allow Right-Click** - This Chrome plugin interferes with the [Viam app](https://app.viam.com)'s ability to configure a service.
If you are experiencing issues with the **Create Service** pane in the Viam app, temporarily disable this plugin until you have saved your configuration in the Viam app.