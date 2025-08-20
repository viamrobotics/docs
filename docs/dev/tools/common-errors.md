---
title: "Common Errors & Known Issues"
linkTitle: "Common Errors"
weight: 50
type: "docs"
description: "A guide to troubleshooting a Viam-based machine or system of machines with fixes to common problems."
date: "2022-01-01"
no_list: true
# updated: ""  # When the content was last entirely checked
---

This document lists common errors encountered when working with Viam, and provides steps to resolve them.
While many common issues and their possible resolutions are presented here, this list is not comprehensive.

To view logs or get a remote shell on a machine see [Troubleshoot](/manage/troubleshoot/troubleshoot/).

If you have encountered an error that is not listed here, we'd love to hear from you on our [Community Discord](https://discord.gg/viam)!
Please post the error message you received along with how you were able to trigger it and we'll see if we can help.

## Status

For information on the status of [app.viam.com](https://app.viam.com), visit [status.viam.com](https://status.viam.com/).

## Common installation errors

### The authenticity of host 'hostname.local' can't be established

**Description:** When following our [installation guides](/operate/get-started/setup/), you will likely encounter this message the first time you try to make an `ssh` connection to your newly-imaged {{< glossary_tooltip term_id="board" text="board" >}}.
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
- If that fails, try re-imaging your board following the [installation guide](/operate/get-started/setup/) appropriate for your board.
  - If using the [Raspberry Pi installation guide](/operate/reference/prepare/rpi-setup/), be sure to carefully enter the configuration details under the **Advanced Options** (gear icon) button on the [Raspberry Pi imager](https://www.raspberrypi.com/software/) before you re-image your board.
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

**Description:** The `viam-server` [installation](/operate/get-started/setup/) or [update](/operate/reference/viam-server/manage-viam-server/#update-viam-server) process may have been interrupted partway, with some files either partially-written or missing.

**Solution:** Reinstall `viam-server` following the [installation instructions](/operate/get-started/setup/).

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

## Common connection errors

### Failed to connect; retrying

**Description:** Viam is unable to communicate with your machine, and will attempt to reconnect every few seconds until it is able to do so.
When a machine is disconnected, it will continue to run with its locally-cached current configuration, but will not be accessible for remote control or configuration through the web UI.

**Solution:** Check the following to ensure your machine is accessible to Viam:

- Is the {{< glossary_tooltip term_id="board" text="board" >}} component connected to the internet?
- Is the `ssh` service configured and running locally on the board?
- Is the `viam-server` service running locally on the board?
  You can check by running `sudo systemctl status viam-server` from within an `ssh` session to the board.
  It should be listed as `active (running)`.

  - If it is listed as `stopped` or `failed`, you can try restarting it with `sudo systemctl start viam-server`.
  - If the command returns the message `Unit viam-server.service could not be found`, be sure you have followed the [installation instructions for your board](/operate/get-started/setup/), and then followed the {{< glossary_tooltip term_id="setup" text="setup instructions" >}}.
  - If none of the above succeed in getting `viam-server` up and running, check the logs on your board for any pertinent error messages.
    Depending on your board's specific Linux OS, you might use a command similar to the following to show the 50 most recent log messages from `viam-server`. Run this command from within an `ssh` session to the board:

    ```sh {class="command-line" data-prompt="$"}
    grep 'viam-server' /var/log/syslog | tail -50
    ```

### Error: error connecting to peer, error not connected

**Full Error:** `error connecting to peer   error not connected`

**Description:** This error indicates a networking or connection issue.

**Solution:**

1. Verify your machine's internet connection is stable and working properly.
1. Ensure your machine is using the correct machine cloud credentials.
   You can obtain your machine cloud credentials from the machine's status in the part status dropdown to the right of your machine’s name on the top of the page.
1. If you are using API keys to connect, ensure you are using the correct credentials for the machine.
1. If you have multiple tabs open with your machine's page, close all but one.
   Having too many connections can cause instability on some machines.

### Error: cannot parse config: JSON: cannot unmarshal string into Go struct

**Full Error:** `Error: cannot parse config: JSON: cannot unmarshal string into Go struct field Component.components.frame of type float64.`

**Description:** A [frame](/operate/reference/services/frame-system/) attribute may be malformed, and is preventing the parsing of the component's configuration.

**Solution:** Check the **CONFIGURE** tab for your machine and look for a `frame` attribute, either in **Frame** or **JSON** mode.
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

### Error: resource build error: unknown resource type

**Full Error:**

Generalized example::

```sh {class="command-line" data-prompt="$" data-output="1-10"}
resource build error: unknown resource type: API "<API-TRIPLET>" with model "<MODEL-TRIPLET>" not registered
```

Camera example:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
resource build error: unknown resource type: API "rdk:component:camera" with model "viam:orbbec:astra2" not registered.
```

**Description:** This error occurs when your configuration requests a model with an associated API and the combination of model name and API triplet is not registered with viam-server.

**Solution:**

1. If you are using a registry-provided models, ensure that your machine's configuration includes the module that provides the model.
   On your machine page, find the module and navigate to it's module page in the registry.
   You can find the correct model triplet (for example `viam:camera:csi-pi`) in the **Components & services** section of the registry page.
1. Check for typos in the model triplet.
   It must exactly match the model registered with `viam-server`.
1. Ensure the model supports the requested API.
   You can find the requested APIs next to each model entry in the **Components & services** section of the registry page.
1. Check for typos in the API triplet (for example `rdk:component:camera`).
1. Check the logs for other errors.
   It may be that the instantiation of the model is failing, for other reasons such as the hardware being disconnected.

### Could not connect to machine part

**Full Error:** `Could not connect to machine part: error updating resources: rpc error: code = ResourceExhausted desc = exceeded request limit 100 on resource viam.robot.v1.RobotService`

**Description:** This error occurs when there are more than 100 concurrent requests to a resource.
These connections can come from modules or other scripts and apps.

**Solution:** Try to find bottlenecks in scripts or modules that are hitting APIs for the machine in loops.
You can check operations and sessions for a machine on its **CONTROL** tab at the bottom of the screen.
To adjust the per-resource limit for modules, you can set the `VIAM_RESOURCE_REQUESTS_LIMIT` [environment variable on your machine](/manage/reference/viam-agent/#environment-variables-for-viam-server) to a positive integer higher than the default, 100.

### exceeded request limit on resource

**Full Error:**

```sh {class="command-line" data-prompt="$" data-output="1-10"}
Error: exceeded request limit <LIMIT> on resource <RESOURCE>
```

**Description**:

This error occurs when there are more than, by default, 100 concurrent requests to a resource on a machine.
The limit applies to calls through both WebRTC and direct gRPC connection, that means requests can come from modules, the Viam web UI, or other resources.

**Solution:**

Try to find bottlenecks in scripts or modules that are hitting APIs for the machine in loops. You can check operations and sessions for a machine on its **CONTROL** tab at the bottom of the screen. To adjust the per-resource limit for modules, you can set the `VIAM_RESOURCE_REQUESTS_LIMIT` [environment variable on your machine](/manage/reference/viam-agent/#environment-variables-for-viam-server) to a positive integer higher than the default, 100.

## Other common errors

### Accidental deletion of machines, locations, organizations, or accounts

If you delete your machine, location, organization, or account by mistake, contact [contact@viam.com](mailto:contact@viam.com) immediately.
They will try to help but cannot guarantee recovery or restoration.

## Common module errors

### Timed out waiting for module

**Full Error:** `Error adding module - Module X - Error while starting module X: Timed out waiting for module X to start listening.` or `Resource X timed out during reconfigure`

**Description:** This error occurs when a module fails to start up or reconfigure within the default timeout period (5 minutes to start up, 1 minute to reconfigure).
This can happen when there is a slow internet connection, when the module is trying to download a large number of dependencies, or when the module is running on a device with limited compute resources.

**Solution:**

- Try using a faster internet connection.
- If you are the module author, consider packaging the module with required dependencies so they don't need to be downloaded on startup.
  For Python modules, you can package your module with dependencies by using the PyInstaller steps when [uploading your module](/operate/get-started/other-hardware/create-module/#upload-your-module).
- If the problem persists, try setting the `VIAM_MODULE_STARTUP_TIMEOUT` or `VIAM_RESOURCE_CONFIGURATION_TIMEOUT` environment variables on your machine to a higher value.
  You can set these environment variables when you start `viam-server`, for instance `VIAM_MODULE_STARTUP_TIMEOUT=6m30 VIAM_RESOURCE_CONFIGURATION_TIMEOUT=3m0s viam-server -config example-machine.json`.
  Pass a sequence of numbers and time units, for example "6m30s50ms" for a timeout of 6 minutes, 30 seconds, and 50 milliseconds, or "5m" for a timeout of 5 minutes.

## Common Micro-RDK errors

### Unable to properly process stun response IceStunEncodingError

**Full Error:** `unable to properly process stun response IceStunEncodingError`

**Description:** Occurs when a client sends a STUN message to a server and receives one of the following problematic responses:

- the response cannot be parsed properly
- the response indicates a server state that conflicts with the client's understanding of the session state

**Solution:** This error may resolve on its own.
If not, look for other related errors in your logs.

## Common warnings

### Connection establishment failed

**Full Warning:** `warn rdk.networking.signaler.external   rpc/wrtc_signaling_answerer.go:389   Connection establishment failed`

**Description:** This error indicates a networking or connection issue.

**Solution:**

1. Check networking:

   1. Check if your machine is showing as online on Viam and [check its logs](/manage/troubleshoot/troubleshoot/#check-logs).
      When `viam-server` starts it runs a set of network checks which you can view in the logs.

   ```sh {class="command-line" data-prompt="$"}
   2025-07-16T16:50:57.727Z    INFO    rdk.network-checks    networkcheck/network-check.go:28    Starting network checks
   2025-07-16T16:50:57.744Z    INFO    rdk    config/platform.go:181    platform tags    {"tags":"os_version:15"}
   2025-07-16T16:50:58.239Z    INFO    rdk.network-checks.udp    networkcheck/network-check-types.go:110    7/7 udp STUN tests succeeded    {"udp_tests":"[{stun_server_url: global.stun.twilio.com:3478, stun_server_addr: 18.156.18.181:3478, ... }]","udp_source_address":"[::]:54092"}
   ```

   1. Verify your machine's internet connection is stable and working properly.
   1. Check if you can access `turn.viam.com:443` and `global.turn.twilio.com:3478`:

      ```sh {class="command-line" data-prompt="$" data-output="2,4"}
      nc -zv turn.viam.com 443
      Connection to turn.viam.com port 443 [tcp/https] succeeded!
      nc -zv global.turn.twilio.com 3478
      Connection to global.turn.twilio.com port 3478 [tcp/nat-stun-port] succeeded!
      ```

   1. Check if UDP traffic is restricted in any way.
      You can do this by checking your router settings and talking to your IT department, if applicable.
   1. Restart your machine.

1. Check your SDK connection:

   1. If you are using API keys to connect, ensure you are using the correct credentials for the machine.
   1. Ensure network checks on `viam-server` succeed by using the Go SDK's [`client.WithNetworkStats()`](https://pkg.go.dev/go.viam.com/rdk/robot/client#WithNetworkStats) method when connecting and then checking the logs when executing the code:

      ```go {class="line-numbers linkable-line-numbers" data-line="13"}
      machine, err := client.New(
        context.Background(),
        "mac-main.vw3iu72d8n.viam.cloud",
      logger,
      client.WithDialOptions(rpc.WithEntityCredentials(
          /* Replace "<API-KEY-ID>" (including brackets) with your machine's API key ID */
        "<API-KEY-ID>",
        rpc.Credentials{
            Type:    rpc.CredentialsTypeAPIKey,
            /* Replace "<API-KEY>" (including brackets) with your machine's API key */
          Payload: "<API-KEY>",
        })),
          client.WithNetworkStats(),
      )
      ```

   1. Try connecting with a different SDK to check whether the issue may be SDK-specific or a code issue.

1. If you have multiple tabs open with your machine's page, close all but one.
   Having too many connections can cause instability on some machines.

### Unable to create PeerConnection with module

**Full Warning:** `Unable to create PeerConnection with module. Ignoring.`

**Description:** Indicates that while the gRPC connection to the module is working as expected, the connection to the module does not support efficient video streaming over WebRTC.
Only some Go-based camera modules support optimized video streaming over WebRTC.

{{% hiddencontent %}}
You can use any Viam SDK to implement a camera module, but only Go-based modules can access optimized video streaming over WebRTC.
{{% /hiddencontent %}}

**Solution:** This warning can be safely ignored.

## Known application and plugin conflicts

### macOS applications

None at this time.

### Windows applications

None at this time.

### Linux applications

None at this time.
