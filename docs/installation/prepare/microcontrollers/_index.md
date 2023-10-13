---
title: "Microcontroller Setup: the Micro-RDK"
linkTitle: "Microcontroller Setup"
weight: 50
no_list: true
type: docs
image: "installation/thumbnails/esp32-espressif.png"
imageAlt: "E S P 32 - espressif"
images: ["/installation/thumbnails/esp32-espressif.png"]
description: "Set up the Espressif ESP32 with the micro-RDK."
aliases:
  - /installation/microcontrollers
# SMEs: Nicolas M., Gautham V.
---

{{% readfile "/static/include/micro-rdk.md" %}}

{{% readfile "/static/include/micro-rdk-hardware.md" %}}

## Install the Micro-RDK

The [Micro-RDK Installer](https://github.com/viamrobotics/micro-rdk/tree/main/micro-rdk-installer) is a CLI that allows you to flash a build of Micro-RDK, along with your robot's credentials and your wifi information, directly to your ESP32.

With this installation, you can use your ESP32 with all supported resource APIs, but you cannot write your own code directly interacting with the chip.
If you want to program the chip directly, follow the setup instructions in [the Micro-RDK Development Setup](/installation/prepare/microcontrollers/development-setup/) instead.

### Download the Micro-RDK Installer

Select the appropriate pre-built binary for the architecture of your development machine:

- [Linux (x86_64)](https://github.com/viamrobotics/micro-rdk/releases/latest/download/micro-rdk-installer-amd64-linux)
- [Linux (Aarch64)](https://github.com/viamrobotics/micro-rdk/releases/latest/download/micro-rdk-installer-arm64-linux)
- [MacOS](https://github.com/viamrobotics/micro-rdk/releases/latest/download/micro-rdk-installer-macos)
- [Windows](https://github.com/viamrobotics/micro-rdk/releases/latest/download/micro-rdk-installer-windows.exe)

### Flash your ESP32 with the Micro RDK Installer

Navigate to [the Viam app](https://app.viam.com) and [add a new robot](/manage/fleet/robots/#add-a-new-robot) in your desired location.

1. Click on the name of the robot to go to the robot's page.
2. Click on the **Setup** tab.
3. Regardless of your operating system, select **Mac** and press the button that appears in Step 2 to download the Viam app config for your robot.

   In your terminal, `cd` to the directory where you downloaded your pre-built binary and run the following command to flash the micro-RDK directly to an ESP32 connected to your computer through a data cable:

   {{< tabs name="Download pre-built binaries" >}}
   {{% tab name="Linux (x86_64)"%}}

```sh { class="command-line" data-prompt="$"}
./micro-rdk-installer-amd64-linux write-flash --app-config=<your-file-path-to/viam.json>
```

    {{% /tab %}}
    {{% tab name="Linux (Aarch64)" %}}

```sh { class="command-line" data-prompt="$"}
./micro-rdk-installer-arm64-linux write-flash --app-config=<your-file-path-to/viam.json>
```

    {{% /tab %}}
    {{% tab name="MacOS" %}}

```sh { class="command-line" data-prompt="$"}
./micro-rdk-installer-macos write-flash --app-config=<your-file-path-to/viam.json>
```

    {{% /tab %}}
    {{% tab name="Windows" %}}

```sh { class="command-line" data-prompt="$"}
./micro-rdk-installer-windows write-flash --app-config=<your-file-path-to/viam.json>
```

    {{% /tab %}}
    {{< /tabs >}}

    To see the micro-RDK server logs through the serial connection, add `--monitor`.
    If the program cannot auto-detect the serial port to which your ESP32 is connected, you may be prompted to select the correct one among a list.

Go back to your new robot's page on [the Viam app](https://app.viam.com).
If successful, your robot will show that it's **Live**.

For more `micro-rdk-installer` CLI usage options, see [GitHub](https://github.com/viamrobotics/micro-rdk/tree/main/micro-rdk-installer).

### Configure an esp32 board

{{< alert title="Info" color="info" >}}

The`esp32` [board](/components/board/) model is not currently provided for you as a built-in option in [the Viam app](https://app.viam.com), so you cannot use the **Config Builder** to configure this board.

{{< /alert >}}

To add an `esp32` board, navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com) and select **Raw JSON** mode.

Copy the following JSON template and paste it into your configuration inside the `"components"` array:

{{< tabs name="Configure an esp32 Board" >}}
{{% tab name="JSON Template"%}}

```json {class="line-numbers linkable-line-numbers"}
{
  "attributes": {
    "pins": [
      <int>
    ],
    "analogs": [
      {
        "pin": "<number>",
        "name": "<your-analog-name>"
      }
    ]
  },
  "depends_on": [],
  "model": "esp32",
  "name": "<your-board-name>",
  "type": "board"
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "attributes": {
    "pins": [15],
    "analogs": [
      {
        "pin": "34",
        "name": "sensor"
      }
    ]
  },
  "depends_on": [],
  "model": "esp32",
  "name": "board",
  "type": "board"
}
```

{{% /tab %}}
{{< /tabs >}}

Edit and fill in the attributes as applicable.
Click **Save config**.

The following attributes are available for `esp32` boards:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `pins` | object | Required | The {{< glossary_tooltip term_id="pin-number" text="pin number" >}} of any GPIO pins you wish to use as input/output with the [`GPIOPin` API](/program/apis/#gpio-pins). |
| `analogs` | object | Optional | Attributes of any pins that can be used as analog-to-digital converter (ADC) inputs. See [configuration info](/components/board/#analogs). |

### Troubleshooting

#### Linux Port Permissions

If a "Permission Denied" or similar port error occurs, first check the connection of the ESP32 to the machine's USB port.
If connected and the error persists, run `sudo usermod -a -G dialout $USER` to add the current user to the `dialout` group, then try again.

#### MacOS Executable Permissions

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
