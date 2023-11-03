---
title: "Troubleshooting"
linkTitle: "Troubleshooting"
weight: 130
type: "docs"
description: "A guide to basic troubleshooting of a Viam-based robotic system, with easy fixes to common problems."
---

This document lists common errors encountered when working with `viam-server` and the [Viam app](https://app.viam.com), and provides simple steps to resolve them.
While many common issues and their possible resolutions are presented here, this list is not comprehensive.

If you have encountered an error that is not listed here, we'd love to hear from you on our [Community Discord](https://discord.gg/viam)!
Please post the error message you received along with how you were able to trigger it and we'll see if we can help.

## Common Installation Errors

### The authenticity of host 'hostname.local' can't be established

**Description:** When following our [installation guides](/installation/), you will likely encounter this message the first time you try to make an `ssh` connection to your newly-imaged {{< glossary_tooltip term_id="board" text="board" >}}.
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
- If that fails, try re-imaging your board following the [installation guide](/installation/) appropriate for your board.
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

**Description:** The `viam-server` [installation](/installation/) or [update](/installation/manage/#update-viam-server) process may have been interrupted partway, with some files either partially-written or missing.

**Solution:** Reinstall `viam-server` following the [installation instructions](/installation/).

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

**Description**: When configuring a Linux {{< glossary_tooltip term_id="board" text="board" >}}, Linux installations with broken or misconfigured sound libraries may experience one or both of these errors, even if not using audio components in the robot configuration.

**Solution:** Consult the documentation for your Linux OS and chosen sound library for guidance on installing any missing software dependencies.
For example, if you are using `jackd` and `PulseAudio` on a Raspberry Pi, you can run the following to install any missing dependencies:

```sh {class="command-line" data-prompt="$"}
sudo apt install jackd qjackctl libpulse-dev pulseaudio
```

This error can be safely ignored if you do not intend to use audio on your robot.

## Common Viam App Errors

### Failed to connect; retrying

**Description:** The [Viam app](https://app.viam.com) is unable to communicate with your robot, and will attempt to reconnect every few seconds until it is able to do so.
When a robot is disconnected, it will continue to run with its locally-cached current configuration, but will not be accessible for remote control or configuration through the Viam app.

**Solution:** Check the following to ensure your robot is accessible to the Viam app:

- Is the {{< glossary_tooltip term_id="board" text="board" >}} component connected to the internet?
- Is the `ssh` service configured and running locally on the board?
- Is the `viam-server` service running locally on the board?
  You can check by running `sudo systemctl status viam-server` from within an `ssh` session to the board.
  It should be listed as `active (running)`.

  - If it is listed as `stopped` or `failed`, you can try restarting it with `sudo systemctl start viam-server`.
  - If the command returns the message `Unit viam-server.service could not be found`, be sure you have followed the [installation instructions for your board](https://docs.viam.com/installation/#preparation), and then followed the instructions on the **Setup** tab on the Viam app.
  - If none of the above succeed in getting `viam-server` up and running, check the logs on your board for any pertinent error messages.
    Depending on your board's specific Linux OS, you might use a command similar to the following to show the 50 most recent log messages from `viam-server`. Run this command from within an `ssh` session to the board:

    ```sh
    grep 'viam-server' /var/log/syslog | tail -50
    ```

### Error: cannot parse config: JSON: cannot unmarshal string into Go struct

**Full Error:** `Error: cannot parse config: JSON: cannot unmarshal string into Go struct field Component.components.frame of type float64.`

**Description:** A [frame](/services/frame-system/) attribute may be malformed, and is preventing the parsing of the component's configuration.

**Solution:** Check the **Config** tab for your robot in the [Viam app](https://app.viam.com) and look for a frame attribute, either in **Builder** mode, under the **Frame System** tab or in **Raw JSON** mode.
If you see a `frame` attribute that you didn't create yourself, delete the whole `frame` object from the JSON config.
It will resemble the following:

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

### Error: failed to find camera

**Additional Errors:** `cannot open webcam`, and `found no webcams`.

**Description:** When working with a [camera](/components/camera/) component on the Linux platform, your Linux OS must be able to access the camera properly, and the camera must be configured to use a pixel format that Viam supports.

**Solution:** On your Linux system, verify each of the following:

- Ensure that your Linux OS is able to access your camera:

  1.  First, find your video device:

      ```sh {class="command-line" data-prompt="$"}
      ls -l /dev/v4l/*
      ```

      In the list of camera devices returned, find the entry that matches the `video_path` from your camera component's configuration in the Viam app.
      For example, if your camera is configured with a `video_path` of `usb-GENERAL_GENERAL_WEBCAM-video-index0`, you would find it in the output of the above command like so:

      ```sh
      usb-GENERAL_GENERAL_WEBCAM-video-index0 -> ../../video0
      ```

      The video device number is the number after `video` appearing on the symlink target for that device, in this case `0`.

  1.  Then, [stop `viam-server`](/installation/manage/#run-viam-server), and verify that your Linux OS is able to access that video device properly:

      ```sh {class="command-line" data-prompt="$"}
      v4l2-ctl -d0 --stream-mmap
      ```

      Replace the `0` in the above command with the number you determined for your video device above.
      You should receive output resembling like the following, which indicates that your Linux OS is successfully able to use your video device:

      ```sh
      <<<<<<<<<<<<<<<<<<<<<<<< 22.81 fps
      <<<<<<<<<<<<<<<<<<<<<<<< 23.50 fps
      ```

      If the command does not return FPS readings as shown above, consult the documentation for your camera and Linux distribution to troubleshoot.
      If you receive the error `Device or resource busy` instead, be sure you have [stopped `viam-server`](/installation/manage/#run-viam-server) first, then re-run the command above.

- Ensure that your camera uses a supported pixel format:

  1.  First, determine your video device number, like `0`, following the instructions above.
  1.  Then, run the following command:

      ```sh {class="command-line" data-prompt="$"}
      v4l2-ctl --list-formats-ext --device /dev/video0
      ```

      Replace the `0` in the above command with the number you determined for your video device above.
      Or, if your video device uses a different path, supply that path to this command instead of `/dev/video0`.

      The command will return a list of pixel formats your camera supports, such as `MJPG` or `YUYV`.
      In order to use a camera device with Viam, it must support at least one of the [pixel formats supported by Viam](/components/camera/webcam/#using-format).
      If your camera does not support any of these formats, it cannot be used with Viam.

If you are still having issues with your camera component on the Linux platform, and would like to [file an issue](https://github.com/viamrobotics/rdk), include your smart machine's camera debug file contained in the <file>/root/.viam/debug/components/camera</file> directory.
If you are running `viam-server` as a different user, find the <file>.viam/debug/components/camera</file> directory in that user's home directory instead.
This file contains basic diagnostic and configuration information about your camera that helps to quickly troubleshoot issues.

### Error: failed to find the best driver that fits the constraints

**Description:** When working with a [camera](/components/camera/) component, depending on the camera, you may need to explicitly provide some camera-specific configuration parameters.

**Solution:** Check the specifications for your camera, and manually provide configuration parameters such as width and height to the camera component configuration page on the [Viam app](https://app.viam.com).
Under **Config > Components**, find your camera, then fill in your camera's specific configuration either using the **Show more** button to show the relevant configuration options, or the **Go to advanced** link in the component panel's upper-right to enter these attributes manually.
Provide at least the width and height values to start.

## Known Application and Plugin Conflicts

### macOS Applications

None at this time.

### Windows Applications

None at this time.

### Linux Applications

None at this time.

### Browser Plugins

**Chrome Plugin: Allow right click** - This Chrome plugin interferes with the [Viam app](https://app.viam.com)'s ability to configure a service.
If you are experiencing issues with the **Create Service** pane in the Viam app, temporarily disable this plugin until you have saved your configuration in the Viam app.
