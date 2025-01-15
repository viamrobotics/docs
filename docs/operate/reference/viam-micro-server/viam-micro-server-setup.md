---
title: "viam-micro-server Troubleshooting"
linkTitle: "viam-micro-server Troubleshooting"
weight: 100
no_list: true
type: docs
images: ["/installation/thumbnails/install.png"]
imageAlt: "Install viam-micro-server"
description: "Troubleshooting tips and best practices for installing and using viam-micro-server on a microcontroller."
# date: "2024-10-07"
# updated: ""  # When the content was last entirely checked
---

For more `micro-rdk-installer` CLI usage options, see [GitHub](https://github.com/viamrobotics/micro-rdk/tree/main/micro-rdk-installer).

For code examples and more information on `viam-micro-server`, see [GitHub](https://github.com/viamrobotics/micro-rdk).

## SDK usage recommendation

If you run [control code](/dev/reference/sdks/) to control your `viam-micro-server` machine, you may experience instability.
If the connection to the ESP32 with an SDK is unstable, we recommend the following changes to the default settings in your connection code.
This will disable the SDK background task that monitors the connection to `viam-micro-server`, saving bandwidth.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Replace the connect function found in the CONNECT tab with the following
async def connect():
    opts = RobotClient.Options(
        # viam-micro-server configures once at boot,
        # so we don't need to check if the components have changed
        refresh_interval=0,
        # Checking the connection can safely be disabled
        check_connection_interval=0,
        # Same for Attempting to reconnect
        attempt_reconnect_interval=0,
        disable_sessions=True,
        # viam-micro-server doesn't support sessions
        # so it is safe to disable them
        dial_options=DialOptions.with_api_key(
            # Replace "<API-KEY-ID>" (including brackets)
            # with your machine's api key id
            api_key_id='<API-KEY-ID>',
            # Replace "<API-KEY>" (including brackets)
            # with your machine's api key
            api_key='<API-KEY>')
    )
    # Replace "<ROBOT-URL>" (including brackets) with your machine's url
    return await RobotClient.at_address('<ROBOT-URL>', opts)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Replace the call to client.New with the following block
robot, err := client.New(
    context.Background(),
    "<ROBOT-URL>", // Replace "<ROBOT-URL>" (including brackets) with your machine's url
    logger,
    client.WithDisableSessions(), // viam-micro-server doesn't support sessions so it is safe to disable them
    client.WithCheckConnectedEvery(0), // Checking the connection can safely be disabled
    client.WithReconnectEvery(0), // Same for Attempting to reconnect
    client.WithRefreshEvery(0), // viam-micro-server configures once at boot, so we don't need to check if the components have changed
    client.WithDialOptions(rpc.WithEntityCredentials(
        // Replace "<API-KEY-ID>" (including brackets) with your machine's api key id
        "<API-KEY-ID>",
        rpc.Credentials{
            Type: rpc.CredentialsTypeAPIKey,
            // Replace "<API-KEY>" (including brackets) with your machine's api key
            Payload: "<API-KEY>",
        })),
    )
if err != nil {
    logger.Fatal(err)
}

```

{{% /tab %}}
{{% /tabs %}}

## Troubleshooting

### Error: IceTransportClosed

If you are trying to connect to an ESP32 and the connection is unstable with the repeating error `E (412486) micro_rdk::common::webrtc::ice: closing ice agent with error IceTransportClosed`, you have opened too many connections to the ESP32, which has a maximum of 3 connections by default.
Make sure you only have one tab with your machine's page open to limit the number of connections to your ESP32.

### Linux port permissions

If a "Permission Denied" or similar port error occurs, first check the connection of the ESP32 to the machine's USB port.
If connected and the error persists, run `sudo usermod -a -G dialout $USER` to add the current user to the `dialout` group, restart your terminal, and try again.

### MacOS executable permissions

When using a machine running a version of MacOS, the user is blocked from running the executable by default.
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

You can find additional assistance in the [Troubleshooting section](/manage/troubleshoot/troubleshoot/).

{{< snippet "social.md" >}}

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
