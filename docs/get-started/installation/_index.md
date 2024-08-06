---
title: "Installation Guide"
linkTitle: "Installation Guide"
childTitleEndOverwrite: "Try Viam"
weight: 100
no_list: true
type: docs
images: ["/get-started/installation/thumbnails/install.png"]
imageAlt: "Install Viam"
description: "To use Viam software with your machine, install and run the viam-server binary on the computer that will run your machine and is connected to your hardware."
aliases:
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
  - /installation/microcontrollers/
  - /installation/prepare/microcontrollers/
  - /get-started/installation/prepare/microcontrollers/
  - /build/micro-rdk/
  - /get-started/installation/microcontrollers/
---

To use Viam, you need to install either the `viam-server` binary or the micro-RDK.

`viam-server` is the binary built from [Robot Development Kit](https://github.com/viamrobotics/rdk) that contains and manages communications between all Viam's built-in hardware drivers ({{< glossary_tooltip term_id="component" text="components" >}}) and software {{< glossary_tooltip term_id="service" text="services" >}}, connects your machine to the cloud, manages machine configuration, and manages dependencies including {{< glossary_tooltip term_id="module" text="modules" >}}.

The micro-RDK is a lightweight version of the {{% glossary_tooltip term_id="rdk" text="Robot Development Kit (RDK)"%}} which can run on resource-limited embedded systems that cannot run the fully-featured [`viam-server`](/get-started/viam/).

For an overview of the Viam software platform, see [Viam in 3 minutes](/get-started/viam/).

## Compatibility

{{< tabs >}}
{{% tab name="viam-server" %}}

`viam-server` supports:

- Linux 64-bit operating systems running on the `aarch64` or `x86_64` architectures
- Windows Subsystem for Linux (WSL)
- macOS

{{< readfile "/static/include/install/windows-support.md" >}}

{{% /tab %}}
{{% tab name="micro-RDK" %}}

The only microcontroller the micro-RDK currently supports is the [ESP32](https://www.espressif.com/en/products/socs/esp32).

{{% readfile "/static/include/micro-rdk-hardware.md" %}}

{{% /tab %}}
{{< /tabs >}}

## Prepare your board

If you are using one of the following boards, click on the card to follow the guide for that board:

{{< cards >}}
{{% card link="/get-started/prepare/rpi-setup/" class="small" %}}
{{% card link="/get-started/prepare/odroid-c4-setup/" class="small" %}}
{{% card link="/get-started/prepare/orange-pi-3-lts/" class="small" %}}
{{% card link="/get-started/prepare/orange-pi-zero2/" class="small" %}}
{{% card link="/get-started/prepare/beaglebone-setup/" class="small" %}}
{{% card link="/get-started/prepare/jetson-agx-orin-setup/" class="small" %}}
{{% card link="/get-started/prepare/jetson-nano-setup/" class="small" %}}
{{% card link="/get-started/prepare/pumpkin/" class="small" %}}
{{% card link="/get-started/prepare/sk-tda4vm/" class="small" %}}
{{< /cards >}}

Viam also provides a lightweight version of `viam-server` called the micro-RDK which can run on resource-limited embedded systems that cannot run the fully-featured Robot Development Kit (RDK).
If you are using a microcontroller, prepare your board using the following guide:

{{< cards >}}
{{% card link="/get-started/installation/micro-rdk-dev/" canonical="/get-started/installation/#install-micro-rdk" class="small" customTitle="ESP32 Setup" %}}
{{< /cards >}}

Other SBCs such as the [RockPi S](https://wiki.radxa.com/RockpiS) and [Orange Pi Zero 2](https://orangepi.com/index.php?route=product/product&path=237&product_id=849) can run Viam with an experimental [periph.io](https://periph.io/) based [modular component](https://github.com/viam-labs/periph_board).

## Install `viam-server`

If you have a [compatible operating system](/get-started/installation/), follow along with the steps outlined below or with the video beneath it to install `viam-server`:

{{< tabs name="Install on computer" >}}
{{% tab name="Linux computer" %}}

{{< readfile "/static/include/install/install-linux.md" >}}

{{% /tab %}}
{{% tab name="macOS computer" %}}

`viam-server` is available for macOS users through Homebrew, and supports both Intel and Apple Silicon macOS computers.
To install `viam-server` on a macOS computer:

1. If not installed already, install [Homebrew](https://brew.sh/).

1. Go to the [Viam app](https://app.viam.com). Create an account if you haven't already.

1. Add a new machine by providing a name in the **New machine** field and clicking **Add machine**:

   ![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

1. Navigate to the **CONFIGURE** tab and find your machine's card.
   An alert will be present directing you to **Set up your machine part**:

   ![Machine setup alert in a newly created machine](/get-started/installation/setup-part.png)

   Click **View setup instructions** to open the setup instructions.

1. Select **Mac** as your system's OS and **RDK** as your RDK type.

1. Follow the steps shown to install `viam-server` on your macOS computer.

1. Once you have followed the steps on the setup instructions, `viam-server` is installed and running.
   Wait for confirmation that your computer has successfully connected.

{{% /tab %}}
{{% tab name="Windows" %}}

1. Go to the [Viam app](https://app.viam.com).
   Create an account if you haven't already.

1. Add a new machine by providing a name in the **New machine** field and clicking **Add machine**:

   ![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

1. Navigate to the **CONFIGURE** tab and find your machine's card.
   An alert will be present directing you to **Set up your machine part**:

   ![Machine setup alert in a newly-created machine](/get-started/installation/setup-part.png)

   Click **View setup instructions** to open the setup instructions:

   ![Setup instructions](/get-started/installation/wsl-setup-instructions.png)

1. Select **Windows** as your system's OS and **RDK** as your RDK type.

1. Follow the steps shown to install `viam-server` on your Windows machine.

1. Once you have followed the steps on the setup instructions, `viam-server` is installed and running.
   Wait for confirmation that your computer has successfully connected.

{{% /tab %}}
{{< /tabs >}}

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/gmIW9JoWStA">}}

### Manage `viam-server`

To learn how to run, update, or uninstall `viam-server`, see [Manage `viam-server`](/get-started/installation/manage/).

### Next steps

{{< cards >}}
{{% card link="/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/sdks/" %}}
{{< /cards >}}

## Install micro-RDK

{{% alert title="BETA" color="note" %}}
The micro-RDK is in beta mode and many features supported by the RDK are still being added to the micro-RDK.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

The micro-RDK installer is a CLI that allows you to flash a build of micro-RDK, along with your machine's credentials and your wifi information, directly to your ESP32.

With this installation, you can use your ESP32 with all supported resource APIs, but you cannot write your own code directly interacting with the chip.
If you want to program the chip directly, follow the setup instructions in [the Micro-RDK Development Setup](/get-started/installation/#install-micro-rdk) instead.

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

### Supported resources

The micro-RDK provides different component models than the fully featured RDK.
See the micro-RDK tab in the **Available Models** section of each component page.

[Client API](/appendix/apis/) usage with the micro-RDK currently supports the following {{< glossary_tooltip term_id="resource" text="resources" >}}:

{{< cards >}}
{{< relatedcard link="/components/base/" >}}
{{< relatedcard link="/components/board/" >}}
{{< relatedcard link="/components/encoder/" >}}
{{< relatedcard link="/components/movement-sensor/" >}}
{{< relatedcard link="/components/motor/" >}}
{{< relatedcard link="/components/sensor/" >}}
{{< relatedcard link="/components/servo/" >}}
{{< relatedcard link="/components/generic/" >}}
{{< relatedcard link="/services/data/capture/" >}}
{{< /cards >}}

Click on each supported resource to see available models, API methods, and configuration info.

See [GitHub](https://github.com/viamrobotics/micro-rdk) for code examples and more information on the micro-RDK.

### Next steps

{{< cards >}}
{{% manualcard link="/components/board/esp32/" %}}

<h4>Configure your board </h4>

Configure your `esp32` board for your machine.
{{% /manualcard %}}
{{% card link="/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/sdks/" %}}
{{< /cards >}}

### Recommendations when using an SDK

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

### Troubleshooting

#### Linux port permissions

If a "Permission Denied" or similar port error occurs, first check the connection of the ESP32 to the machine's USB port.
If connected and the error persists, run `sudo usermod -a -G dialout $USER` to add the current user to the `dialout` group, restart your terminal, and try again.

#### MacOS executable permissions

When using a machine running a version of MacOS, the user is blocked from running the executable by default.
To fix this, **Control+Click** the binary in Finder and then, in the following two prompts select **Open**.
Close whatever terminal window this opens to be able to run the installer.

#### Error: FlashConnect

This may occur because the serial port chosen if/when prompted is incorrect.
However, if the correct port has been selected, try the following:

1. Run the installer as explained above.
2. When prompted to select a serial port:
   1. Hold down the "EN" or enable button on your ESP32.
   2. With the above button held down, select the correct serial port.
   3. Press and hold down the "EN" and "Boot" buttons at the same time. Then release both.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

#### Ubuntu not recognizing the microcontroller

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