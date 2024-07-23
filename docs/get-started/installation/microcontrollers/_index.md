---
title: "Microcontrollers: the Micro-RDK"
linkTitle: "Microcontrollers"
weight: 50
no_list: true
type: docs
images: ["/get-started/installation/thumbnails/esp32-espressif.png"]
imageAlt: "E S P 32 - espressif"
description: "Set up the Espressif ESP32 with the micro-RDK."
aliases:
  - /installation/microcontrollers/
  - /installation/prepare/microcontrollers/
  - /get-started/installation/prepare/microcontrollers/
  - /build/micro-rdk/
# SMEs: Nicolas M., Gautham V., Andrew M.
---

{{% readfile "/static/include/micro-rdk.md" %}}

{{% readfile "/static/include/micro-rdk-hardware.md" %}}

## Install the micro-RDK

The micro-RDK installer is a CLI that allows you to flash a build of micro-RDK, along with your machine's credentials and your wifi information, directly to your ESP32.

With this installation, you can use your ESP32 with all supported resource APIs, but you cannot write your own code directly interacting with the chip.
If you want to program the chip directly, follow the setup instructions in [the Micro-RDK Development Setup](/get-started/installation/microcontrollers/development-setup/) instead.

### Flash your ESP32 with the micro-RDK installer

Navigate to [the Viam app](https://app.viam.com) and [add a new machine](/cloud/machines/#add-a-new-machine) in your desired location.

1. Click on the name of the machine to go to its page.
2. Navigate to the **CONFIGURE** tab and find your machine's card. An alert will be present directing you to **Set up your machine part**. Click **View setup instructions** to open the setup instructions.
3. Select your computer's architecture and operating system, and select **Micro-RDK** as **RDK type**.
4. Follow the instructions to flash the micro-RDK directly to an ESP32 connected to your computer through a data cable.

   To see the micro-RDK server logs through the serial connection, add `--monitor` to the command in step 3.
   If the program cannot auto-detect the serial port to which your ESP32 is connected, you may be prompted to select the correct one among a list.

Go back to your new machine's page on [the Viam app](https://app.viam.com).
If successful, your machine will show that it's **Live**.

For more `micro-rdk-installer` CLI usage options, see [GitHub](https://github.com/viamrobotics/micro-rdk/tree/main/micro-rdk-installer).

### Configure your machine

The micro-RDK provides different component models than the fully featured RDK.
See the [Micro-RDK](/get-started/installation/microcontrollers/) tab in the Supported Models section of each component page.

## Next steps

{{< cards >}}
{{% manualcard link="/components/board/esp32/" %}}

<h4>Configure your board </h4>

Configure your `esp32` board for your machine.

{{% /manualcard %}}
{{% card link="/build/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/build/program/" %}}
{{< /cards >}}

## Recommendations when using an SDK

If the connection to the ESP32 with an SDK is unstable we recommend the following changes to the default settings in your SDK code when connecting to an ESP32.
This will disable the SDK background task that monitors the connection to the micro-RDK, saving bandwidth.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Replace the connect function found in the CONNECT tab with the following
async def connect():
    opts = RobotClient.Options(
        # Micro-RDK configures once at boot,
        # so we don't need to check if the components have changed
        refresh_interval=0,
        # Checking the connection can safely be disabled
        check_connection_interval=0,
        # Same for Attempting to reconnect
        attempt_reconnect_interval=0,
        disable_sessions=True,
        # Micro-RDK doesn't support sessions so it is safe to disable them
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
    client.WithDisableSessions(), // Micro-RDK doesn't support sessions so it is safe to disable them
    client.WithCheckConnectedEvery(0), // Checking the connection can safely be disabled
    client.WithReconnectEvery(0), // Same for Attempting to reconnect
    client.WithRefreshEvery(0), // Micro-RDK configures once at boot, so we don't need to check if the components have changed
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

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}
