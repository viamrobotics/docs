---
title: "Installation Guide"
linkTitle: "Installation Guide"
childTitleEndOverwrite: "Try Viam"
weight: 100
no_list: true
type: docs
images: ["/installation/thumbnails/install.png"]
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
  - /installation/prepare/microcontrollers/
  - /build/micro-rdk/
  - /get-started/installation/microcontrollers/
  - /get-started/installation/
---

To use Viam, you need to install either the `viam-server` binary or `viam-micro-server`.

[`viam-server`](/get-started/#viam-server) is the binary built from the [Robot Development Kit](https://github.com/viamrobotics/rdk) that contains and manages communications between all Viam's built-in hardware drivers ({{< glossary_tooltip term_id="component" text="components" >}}) and software {{< glossary_tooltip term_id="service" text="services" >}}, connects your machine to the cloud, manages machine configuration, and manages dependencies including {{< glossary_tooltip term_id="module" text="modules" >}}.

`viam-micro-server` is a lightweight version of `viam-server` which can run on resource-limited embedded systems that cannot run the fully-featured `viam-server`.
`viam-micro-server` is built from the [micro-RDK](https://github.com/viamrobotics/micro-rdk/tree/main).

For an overview of the Viam software platform, see [Learn about Viam](/get-started/).

{{< alert title="In this page" color="note" >}}
{{% toc %}}
{{< /alert >}}

## Compatibility

{{< tabs >}}
{{% tab name="viam-server" %}}

`viam-server` supports:

- Linux 64-bit operating systems running on the `aarch64` or `x86_64` architectures
- Windows Subsystem for Linux (WSL)
- macOS

{{< readfile "/static/include/install/windows-support.md" >}}

If you are using one of the following boards, click on the card to follow the guide to install a supported operating system for that board.
Otherwise proceed to [install `viam-server`](/installation/#install-viam-server).

{{< cards >}}
{{% card link="/installation/prepare/rpi-setup/" class="small" %}}
{{% card link="/installation/prepare/odroid-c4-setup/" class="small" %}}
{{% card link="/installation/prepare/orange-pi-3-lts/" class="small" %}}
{{% card link="/installation/prepare/orange-pi-zero2/" class="small" %}}
{{% card link="/installation/prepare/beaglebone-setup/" class="small" %}}
{{% card link="/installation/prepare/jetson-agx-orin-setup/" class="small" %}}
{{% card link="/installation/prepare/jetson-nano-setup/" class="small" %}}
{{% card link="/installation/prepare/pumpkin/" class="small" %}}
{{% card link="/installation/prepare/sk-tda4vm/" class="small" %}}
{{< /cards >}}

Other SBCs such as the [RockPi S](https://wiki.radxa.com/RockpiS) and [Orange Pi Zero 2](https://orangepi.com/index.php?route=product/product&path=237&product_id=849) can run Viam with an experimental [periph.io](https://periph.io/) based [modular component](https://github.com/viam-labs/periph_board).

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

The only microcontroller `viam-micro-server` currently supports is the [ESP32](https://www.espressif.com/en/products/socs/esp32).

{{% readfile "/static/include/micro-rdk-hardware.md" %}}

Proceed to [install `viam-micro-server`](/installation/#install-viam-micro-server).

{{% /tab %}}
{{< /tabs >}}

## Install `viam-server`

If you have a [compatible operating system](/installation/#compatibility), follow along with the steps outlined below to install `viam-server`:

1. Go to the [Viam app](https://app.viam.com). Create an account if you haven't already.

1. Add a new machine by providing a name in the **New machine** field and clicking **Add machine**:

   ![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

1. Navigate to the **CONFIGURE** tab and find your machine's card.
   An alert will be present directing you to **Set up your machine part**:

   ![Machine setup alert in a newly created machine](/installation/setup-part.png)

   Click **View setup instructions** to open the setup instructions.

1. Select the platform you want to run on.

1. If you selected **Linux / Aarch 64** or **Linux / x86** also select your installation method:

   - `manual`: installs only `viam-server` on your machine.
   - `viam-agent`: installs viam-agent, which will automatically install (or update) viam-server **and** provide additional functionality such as [provisioning](/fleet/provision/) and operating system update configuration.

1. Follow the steps shown on the setup page.

1. Once you have followed the steps on the setup instructions, wait for confirmation that your machine has successfully connected.

   On your machine's page on [the Viam app](https://app.viam.com), your machine will show that it's **Live**.

{{< alert title="Linux: Automatic startup" color="note" >}}
On Linux installs, by default `viam-server` or `viam-agent` and `viam-server` will start automatically when your system boots.
You can change this behavior if desired.
If you installed `viam-server` manually see [Manage `viam-server`](/installation/manage-viam-server/).
If you installed `viam-server` through `viam-agent` see [Manage `viam-agent`](/installation/manage-viam-agent/).
{{< /alert >}}

### Manage your installation

To learn how to run, update, or uninstall `viam-agent`, see [Manage `viam-agent`](/installation/manage-viam-agent/).

For manual installs of only `viam-server`, see [Manage `viam-server`](/installation/manage-viam-server/).

### Next steps

{{< cards >}}
{{% card link="/how-tos/configure/" %}}
{{% card link="/how-tos/develop-app/" %}}
{{% card link="/configure/" %}}
{{< /cards >}}

## Install `viam-micro-server`

`viam-micro-server` is the lightweight version of `viam-server` that you can run on ESP32 microcontrollers.

{{% alert title="BETA" color="note" %}}
`viam-micro-server` is in beta mode and many features supported by `viam-server` are still being added to `viam-micro-server`.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

The `viam-micro-server` installer is a CLI that allows you to flash a build of `viam-micro-server`, along with your machine's credentials and your wifi information, directly to your ESP32.

With this installation, you can use your ESP32 with all supported resource APIs, but you cannot write your own code directly interacting with the chip.
If you want to program the chip directly, follow the setup instructions in [`viam-micro-server` Development Setup](/installation/#install-viam-micro-server) instead.

### Flash your ESP32 with the `viam-micro-server` installer

If you have a [compatible microcontroller](/installation/#compatibility), follow along with the steps outlined below to install `viam-server`:

1. Go to the [Viam app](https://app.viam.com). Create an account if you haven't already.

1. Add a new machine by providing a name in the **New machine** field and clicking **Add machine**:

   ![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

1. Navigate to the **CONFIGURE** tab and find your machine's card.
   An alert will be present directing you to **Set up your machine part**:

   ![Machine setup alert in a newly created machine](/installation/setup-part.png)

   Click **View setup instructions** to open the setup instructions.

1. Select **ESP32** as the platform you want to run on.

1. Select the platform you want to use from which to flash the target system.

1. Follow the instructions to flash `viam-micro-server` directly to an ESP32 connected to your computer through a data cable.

1. Once you have followed the steps on the setup instructions, `viam-micro-server` is installed and will run.
   Wait for confirmation that your microcontroller has successfully connected.

   On your machine's page on [the Viam app](https://app.viam.com), your machine will show that it's **Live**.
   If something is not working, see [Troubleshooting](/installation/#troubleshooting).

For more `micro-rdk-installer` CLI usage options, see [GitHub](https://github.com/viamrobotics/micro-rdk/tree/main/micro-rdk-installer).

See [GitHub](https://github.com/viamrobotics/micro-rdk) for code examples and more information on `viam-micro-server`.

### Recommendations when using an SDK

As you use the ESP32, if you write [SDK code](/sdks/), you may experience instability.
If the connection to the ESP32 with an SDK is unstable, we recommend the following changes to the default settings in your SDK code when connecting to an ESP32.
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

### Next steps

{{< cards >}}
{{% card link="/how-tos/configure/" %}}
{{% card link="/how-tos/develop-app/" %}}
{{% card link="/configure/" %}}
{{< /cards >}}

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
