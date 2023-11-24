---
title: "Microcontroller Setup: the Micro-RDK"
linkTitle: "Microcontroller Setup"
weight: 50
no_list: true
type: docs
image: "get-started/installation/thumbnails/esp32-espressif.png"
imageAlt: "E S P 32 - espressif"
images: ["/get-started/installation/thumbnails/esp32-espressif.png"]
description: "Set up the Espressif ESP32 with the micro-RDK."
aliases:
  - /installation/microcontrollers/
  - /installation/prepare/microcontrollers/
# SMEs: Nicolas M., Gautham V., Andrew M.
---

{{% readfile "/static/include/micro-rdk.md" %}}

{{% readfile "/static/include/micro-rdk-hardware.md" %}}

## Install the Micro-RDK

The Micro-RDK Installer is a CLI that allows you to flash a build of Micro-RDK, along with your robot's credentials and your wifi information, directly to your ESP32.

With this installation, you can use your ESP32 with all supported resource APIs, but you cannot write your own code directly interacting with the chip.
If you want to program the chip directly, follow the setup instructions in [the Micro-RDK Development Setup](/get-started/installation/prepare/microcontrollers/development-setup/) instead.

### Flash your ESP32 with the Micro-RDK Installer

Navigate to [the Viam app](https://app.viam.com) and [add a new robot](/fleet/machines/#add-a-new-robot) in your desired location.

1. Click on the name of the robot to go to the robot's page.
2. Click on the **Setup** tab.
3. Select your computer's architecture as **Architecture** and select **Micro-RDK** as **RDK type**.
4. Follow the instructions to flash the micro-RDK directly to an ESP32 connected to your computer through a data cable.

   To see the micro-RDK server logs through the serial connection, add `--monitor` to the command in step 3.
   If the program cannot auto-detect the serial port to which your ESP32 is connected, you may be prompted to select the correct one among a list.

Go back to your new robot's page on [the Viam app](https://app.viam.com).
If successful, your robot will show that it's **Live**.

For more `micro-rdk-installer` CLI usage options, see [GitHub](https://github.com/viamrobotics/micro-rdk/tree/main/micro-rdk-installer).

### Configure your robot

The micro-RDK provides different component models than the fully featured RDK.
See [Micro-RDK](/build/micro-rdk/) to get a list of supported models and instructions on how to configure them.

## Next steps

{{< cards >}}
{{% manualcard link="/build/micro-rdk/board/esp32/" %}}

<h4>Configure your board </h4>

Configure your `esp32` board for your robot.

{{% /manualcard %}}
{{% card link="/build/configure/" %}}
{{% card link="/tutorials/" %}}
{{% card link="/build/program/" %}}
{{< /cards >}}

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

You can find additional assistance in the [Troubleshooting section](/reference/appendix/troubleshooting/).

{{< snippet "social.md" >}}
