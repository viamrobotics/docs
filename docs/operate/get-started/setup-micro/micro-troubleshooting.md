---
title: "Micro-RDK Troubleshooting"
linkTitle: "Micro-RDK Troubleshooting"
weight: 100
no_list: true
type: docs
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install viam-micro-server"
description: "Troubleshooting tips and best practices for installing and using viam-micro-server or other Micro-RDK-based firmware on a microcontroller."
aliases:
  - /operate/reference/viam-micro-server/viam-micro-server-setup/
  - /operate/reference/viam-micro-server/micro-troubleshooting/
# date: "2024-10-07"
# updated: ""  # When the content was last entirely checked
---

{{% alert title="Tip" color="tip" %}}
The [Viam Micro-RDK installer](https://github.com/viamrobotics/micro-rdk/tree/main/micro-rdk-installer) is a command line tool that can be helpful for troubleshooting.
{{% /alert %}}

## Installation issues

### Error: `xtensa-esp32-elf-gcc: error: unrecognized command line option '--target=xtensa-esp32-espidf'` when building on macOS

This is caused by an [upstream bug](https://github.com/esp-rs/esp-idf-template/issues/174).
To work around this issue, ensure that `CRATE_CC_NO_DEFAULTS=1` is set in the environment when building.

### Error: `error: externally-managed-environment` when building ESP-IDF on macOS

This is encountered when attempting to build ESP-IDF projects while using Python obtained from Homebrew.
Homebrew's Python infrastructure is not intended for end-user consumption but is instead made available to support Homebrew packages which require a python interpreter.
The preferred workaround for this issue is to obtain a user-facing python installation not from Homebrew, but there are other, less safe, workarounds.
Please see the macOS specific notes in the [development technical notes on GitHub](https://github.com/viamrobotics/micro-rdk/blob/main/DEVELOPMENT.md#fixing-esp-builds-on-macos) for more details.

### Error: Failed to open serial port

If you run into the error `Failed to open serial port` when flashing your ESP32 with Linux, make sure the user is added to the group `dialout` with `sudo gpasswd -a $USER dialout`.

### Error: `espflash::timeout`

If you get the following error while connecting to your ESP32:

```sh { class="command-line" data-prompt="$"}
`Error: espflash::timeout

  × Error while connecting to device
  ╰─▶ Timeout while running command
```

Run the following command, replacing `<YOUR_PROJECT_NAME>` with the name of your project firmware (for example, `esp32-camera`):

```sh { class="command-line" data-prompt="$"}
espflash flash --erase-parts nvs --partition-table partitions.csv  target/xtensa-esp32-espidf/release/<YOUR_PROJECT_NAME> --baud 115200 && sleep 2 && espflash monitor
```

Try the connection command again.
The baud rate on your device may not have been fast enough to connect.
If successful, Viam will show that your machine part's status is **Live**.

You can also try disconnecting and reconnecting the ESP32 to the USB port, then retrying the flash command.

### Error: `viam.json` not found

If you get the error `viam.json not found` try the following to manually add your machine cloud credentials as a file in your project:

1. Navigate to your machine's page and select the **CONFIGURE** tab.
1. Select the part status dropdown to the right of your machine's name on the top of the page:

   {{<imgproc src="/get-started/micro-credentials.png" resize="450x" declaredimensions=true alt="Machine part info menu accessed by Live status indicator, with machine cloud credentials button highlighted." class="shadow" >}}

1. Click the copy icon underneath **Machine cloud credentials**.
   The Micro-RDK needs this JSON object, which contains your machine part secret key and cloud app address, to connect to Viam.
1. Navigate to the directory of the project you just created.
1. Create a new <file>viam.json</file> file and paste the machine cloud credentials in.
1. Save the file.

### Error: failed to run custom build command for `esp32-explorer (/host)`

This may occur for various reasons such as your machine cloud credentials, Wi-Fi SSID, or password not being populated.
Check that your project directory contains machine cloud credentials in a <file>viam.json</file>, and that you provided Wi-Fi credentials.

### Error: invalid value `460800` for `--before <BEFORE>`

Change `"-b"` to `"-B` in the <file>Makefile</file>, as `"-B"` is the Baudrate config.
Run the following commands to flash <file>esp32-server.bin</file> to your ESP32 microcontroller at a high baud rate, wait for 2 seconds, and observe the device's output:

```sh {class="command-line" data-prompt="$"}
espflash write-bin 0x0 target/esp32-server.bin -B 460800  && sleep 2 && espflash monitor
```

## Other issues

### Unstable connection

Because microcontrollers are more resource-constrained than single-board computers or other computers, when you run [control code](/dev/reference/sdks/) to control your Micro-RDK machine, you may experience instability.
If your connection is unstable, we recommend changing the default settings by making the following changes to your connection code.
This code will disable the SDK background task that monitors the connection to your machine, reducing processing demands and improving the reliability of connection establishment.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# TODO: Replace the connect function found in the CONNECT tab with the following
async def connect():
    opts = RobotClient.Options(
        # viam-micro-server configures once at boot,
        # so we don't need to check if the components have changed
        refresh_interval=0,
        # Checking the connection can safely be disabled
        check_connection_interval=0,
        # Same for Attempting to reconnect
        attempt_reconnect_interval=0,
        # viam-micro-server doesn't support sessions
        # so it is safe to disable them
        disable_sessions=True,
        dial_options=DialOptions.with_api_key(
            # TODO: Replace "<API-KEY-ID>" (including brackets)
            # with your machine's api key id
            api_key_id='<API-KEY-ID>',
            # TODO: Replace "<API-KEY>" (including brackets)
            # with your machine's api key
            api_key='<API-KEY>')
    )
    # TODO: Replace "<ROBOT-URL>" (including brackets) with your machine's url
    return await RobotClient.at_address('<ROBOT-URL>', opts)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// TODO: Replace the call to client.New with the following block
robot, err := client.New(
    context.Background(),
    "<ROBOT-URL>", // TODO: Replace "<ROBOT-URL>" (including brackets) with your machine's url
    logger,
    client.WithDisableSessions(), // viam-micro-server doesn't support sessions so it is safe to disable them
    client.WithCheckConnectedEvery(0), // Checking the connection can safely be disabled
    client.WithReconnectEvery(0), // Same for Attempting to reconnect
    client.WithRefreshEvery(0), // viam-micro-server configures once at boot, so we don't need to check if the components have changed
    client.WithDialOptions(rpc.WithEntityCredentials(
        // TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's api key id
        "<API-KEY-ID>",
        rpc.Credentials{
            Type: rpc.CredentialsTypeAPIKey,
            // TODO: Replace "<API-KEY>" (including brackets) with your machine's api key
            Payload: "<API-KEY>",
        })),
    )
if err != nil {
    logger.Fatal(err)
}

```

{{% /tab %}}
{{% /tabs %}}

### Error: IceTransportClosed

If you are trying to connect to an ESP32 and the connection is unstable with the repeating error `E (412486) micro_rdk::common::webrtc::ice: closing ice agent with error IceTransportClosed`, you have opened too many connections to the ESP32, which has a maximum of 3 connections by default.
Make sure you only have one tab with your machine's page open to limit the number of connections to your ESP32.

### Linux port permissions

If a "Permission Denied" or similar port error occurs, first check the connection of the ESP32 to the machine's USB port.
If connected and the error persists, run `sudo usermod -a -G dialout $USER` to add the current user to the `dialout` group, restart your terminal, and try again.

### macOS executable permissions

When using a machine running a version of macOS, the user is blocked from running the executable by default.
To fix this, **Control+Click** the binary in Finder and then, in the following two prompts select **Open**.
Close whatever terminal window this opens to be able to run the installer.

### Error: FlashConnect

This may occur because the serial port chosen if/when prompted is incorrect.
However, if the correct port has been selected, try the following:

1. Run the installer as explained above.
2. When prompted to select a serial port:
   1. Hold down the "EN" or enable button on your ESP32.
   2. With the above button held down, select the correct serial port.
   3. Press and hold down the "EN" and "Boot" buttons at the same time. Then release both.

If this doesn't work, try wiggling or reattaching the connections on both ends of the data cable connecting your ESP32 to your computer.
You can also try using a different cable entirely; make sure it is a data-compatible cable.

### Ubuntu not recognizing the microcontroller

If you’re trying to connect a microcontroller using serial port to an Ubuntu system and the computer doesn’t seem to be recognizing the microcontroller, check if the `brltty` service or its secondary service `brltty-udev` are active (`brltty` is a service installed by default that provides access to a braille display):

```sh {class="command-line" data-prompt="$" data-output="2"}
sudo systemctl status | grep brltty
brltty-udev.service loaded active running Braille Device Support
```

It is a known issue that this service takes ownership of cp210x devices that are used in serial communication with microcontrollers.

To disable the services, run the following:

```sh {class="command-line" data-prompt="$"}
sudo systemctl stop brltty-udev.service
sudo systemctl mask brltty-udev.service
sudo systemctl stop brltty.service
sudo systemctl disable brltty.service
```

You may also need to reboot your system, and/or unplug the cable from the computer and re-plug it in.

See this [blog post](https://koen.vervloesem.eu/blog/how-to-stop-brltty-from-claiming-your-usb-uart-interface-on-linux/) and [Ubuntu bug report](https://bugs.launchpad.net/ubuntu/+source/brltty/+bug/1958224) for more.

### Additional assistance

You can find general Viam troubleshooting information in the [Troubleshooting section](/manage/troubleshoot/troubleshoot/).

{{< snippet "social.md" >}}
