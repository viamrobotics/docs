---
title: "Drive a Rover (like SCUTTLE or Yahboom) Using a Gamepad"
linkTitle: "Drive a Rover with a Gamepad"
type: "docs"
description: "Drive a wheeled rover with a Bluetooth gamepad that has a dongle."
videos:
  [
    "/tutorials/videos/scuttle-gamepad-preview.webm",
    "/tutorials/videos/scuttle-gamepad-preview.mp4",
  ]
videoAlt: "Drive a Scuttle Robot with a Bluetooth gamepad."
images: ["/tutorials/videos/scuttle-gamepad-preview.gif"]
aliases:
  - "/tutorials/scuttle-gamepad/"
  - "/tutorials/scuttlebot/scuttle-gamepad/"
  - "/tutorials/control/scuttle-gamepad/"
tags: ["base", "scuttle", "gamepad"]
authors: []
languages: []
viamresources: ["base", "input_controller", "base_remote_control"]
level: "Intermediate"
date: "2022-08-10"
updated: "2024-04-17"
cost: 575
---

By the end of this tutorial, you'll be able to drive your rover around like an RC car.

{{< alert title="Learning Goals" color="info" >}}

After following this tutorial, you will be able to use the input controller component to control your machine using a gamepad.

{{< /alert >}}

## Requirements

You will need the following hardware to complete this tutorial:

- A wheeled rover, configured with a [base component](/machine/components/base/) on the [Viam app](https://app.viam.com/).
  This tutorial uses a [SCUTTLE rover](https://www.scuttlerobot.org/shop/) as an example but you can complete this tutorial using a [Yahboom 4WD Smart Robot](https://category.yahboom.net/collections/robotics/products/4wdrobot) or an entirely different rover.
  - For a tutorial on configuring your rover, see [Configure a Rover](/tutorials/configure/configure-rover/).
- [EasySMX ESM-9101 Wireless Controller](https://www.amazon.com/Wireless-Controller-EasySMX-ESM-9101-Gamepad/dp/B07F1NLGW2?th=1) or a similar gamepad and dongle.
  This is the controller that comes with the SCUTTLE rover.
  You can also use an 8BitDo controller with additional setup.

{{<video webm_src="/tutorials/videos/scuttledemos_gamepad.webm" mp4_src="/tutorials/videos/scuttledemos_gamepad.mp4" alt="Controlling a Scuttle robot using a Bluetooth gamepad" poster="/tutorials/scuttlebot/scuttledemos_gamepad.jpg">}}

## Set up the hardware

If your gamepad has a dongle, plug the gamepad Bluetooth dongle into a USB port on the rover's [board](/machine/components/board/).
Then turn on power to the rover.

{{% expand "Click here if your gamepad does not have a dongle for bluetooth pairing instructions." %}}

Make sure your bluetooth controller is in pairing mode.
For an 8bitdo controller, set the mode switch to **S**, hold down **Start** for a few seconds, and when the LED underneath the controller changes to green, press the pair button for 3 seconds.
For more information about the controller buttons and Bluetooth modes, consult the manual included with the controller.

Run `sudo bluetoothctl scan on` to list all Bluetooth devices within reach of your machine.
As you do this, make sure you run this command on the machine that runs `viam-server` which may be a different machine to your laptop.

This command scans all bluetooth devices.
Find your gamepad.
For an 8bitdo controller, the MAC address begins with E4:17:D8.

![A screenshot of a Raspberry Pi terminal with the following command: sudo bluetoothctl scan on. The results of the command are displayed: a list of device MAC addresses.](/tutorials/yahboom-rover/bluetooth-scan.png)

Once you find your controller, pair with the controller by running the following command: `sudo bluetoothctl pair <8bitdo-mac-address>`.
Do not forget to take the `<` and `>` symbols out as you paste your address.

Then connect the controller: `sudo bluetoothctl connect <8bitdo-mac-address>`

To make reconnecting easier in the future, trust the controller by running the following command: `sudo bluetoothctl trust <8bitdo-mac-address>`

To confirm the connection, you can list connected devices with: `sudo bluetoothctl devices | cut -f2 -d| while read uuid; do sudo bluetoothctl info $uuid; done|grep -e "Device\|Connected\|Name"`

![A screenshot of a Pi terminal showing the above bluetoothctl commands and their outputs.](/tutorials/yahboom-rover/bluetoothpair-connect.png)

If you would like a stronger understanding of `bluetoothctl` and managing Bluetooth devices in Linux, we recommend [How to Manage Bluetooth Devices on Linux Using bluetoothctl](https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/).

{{% /expand%}}

## Add the controller to the rover's config

Go to your rover's **CONFIGURE** tab on the [Viam app](https://app.viam.com/).

{{< tabs >}}
{{% tab name="Config Builder" %}}

Configure a [gamepad](/machine/components/input-controller/gamepad/):

Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `input_controller` type, then select the `gamepad` model.
Enter a name or use the suggested name for your input controller and click **Create**.

![An example configuration for a linux-based gamepad input controller component in the Viam App config builder](/machine/components/input-controller/gamepad-input-controller-ui-config.png)

You can set the `auto_reconnect` attribute to `true`.

{{% /tab %}}
{{% tab name="JSON" %}}

If instead of using the config builder, you prefer to write raw JSON, switch to [**JSON** mode](/machine/configure/#the-configure-tab) on the **CONFIGURE** tab.
Inside the `components` array of your config, add the following configuration for your [gamepad](/machine/components/input-controller/gamepad/):

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my-gamepad",
  "model": "gamepad",
  "type": "input_controller",
  "namespace": "rdk",
  "attributes": { "auto_reconnect": true },
  "depends_on": []
}
```

{{% /tab %}}
{{< /tabs >}}

The controller config adds the gamepad controller to your machine.
However, it is not functional yet.
To link the controller input to the base functionality, you need to add the base remote control service.

## Add the base remote control service

Services are software packages that provide robots with higher level functionality.
To link the controller's input to the base functionality, you need to configure the [base remote control service](/machine/services/base-rc/):

{{< tabs >}}
{{% tab name="Config Builder" %}}

Click the **+** icon next to your machine part in the left-hand menu and select **Service**.
Select the `base remote control` type.
Enter a name or use the suggested name for your service and click **Create**.

In your base remote control service's configuration panel, copy and paste the following JSON object into the attributes field:

```json {class="line-numbers linkable-line-numbers"}
{
  "base": "<your-base-name>",
  "input_controller": "my-gamepad"
}
```

<br>

For example:

![An example configuration for a base remote control service in the Viam app Config Builder.](/machine/services/base-rc/base-rc-ui-config.png)

{{% /tab %}}
{{% tab name="Raw JSON" %}}

Add the following configuration for your base remote control service, replacing `<your-base-name>` with your base's name:

```json {class="line-numbers linkable-line-numbers"}
  "services": [
    {
      "name": "gamepad_service",
      "type": "base_remote_control",
      "attributes": {
        "input_controller": "my-gamepad",
        "base": "<your-base-name>"
      }
    }
  ]
```

If you already have a `"services"` array with other services configured, add just the contents of the square brackets above to that array, rather than creating two different `"services"` arrays.
{{% /tab %}}
{{< /tabs >}}

Click **Save**, then go to the **CONTROL** tab.

You should see the panel for the gamepad and its connection indicator:

![Gamepad input UI showing a "connected" indicator and a list of inputs from all the buttons, for example X=0.0, RY=0.0 and East=0.](/tutorials/scuttle-gamepad/control-tab-input.png)

Try moving the left joystick or pressing the D-pad to move the rover using the gamepad.

The ESM-9101 controller has different [modes](#easysmx-esm-9101-wireless-controller-information) that allow you to use either the joystick or the D-pad.
If you are in the mode that allows you to use the joystick (#7), it will change the `X` and `Y` values on the **Control** tab gamepad panel:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
"X
0.0000
Y
0.0000"
```

If you are in the mode that allows you to use the D-pad (#8), it will change the `Hat0X` and `Hat0Y` values:

```sh {class="command-line" data-prompt="$" data-output="1-10"}
"Hat0X
0.0000
Hat0Y
0.0000"
```

Testing these attributes tells you which mode you are in.

## EasySMX ESM-9101 wireless controller information

Here is a diagram of the gamepad.

<table>
<tr>
<td>{{<imgproc src="/tutorials/scuttle-gamepad/pi-game-gamepad-diagram.png" resize="800x" alt="gamepad diagram">}}</td>
<td>{{<imgproc src="/tutorials/scuttle-gamepad/pi-game-gamepad-legend.png" resize="800x" alt="gamepad legend">}}</td>
</tr>
</table>

To change the movement/direction control on the gamepad between the D-pad and the joystick, press and hold the Home button (#11) until it displays the lighted segment combination for the gamepad configuration you need.
Each red color arrangement allows you to control the gamepad in the Viam app:

<table>
<tr><td>LED 1 and 3: Use the D-Pad<BR>
{{<imgproc src="/tutorials/scuttle-gamepad/pi-game-cont-1and3.jpg" resize="300x" declaredimensions=true alt="Led 1 and 3 are lit">}}
</td><td>LED 3 and 4: Use the D-Pad<BR>
{{<imgproc src="/tutorials/scuttle-gamepad/pi-game-cont-3and4.jpg" resize="300x" declaredimensions=true alt="Led 3 and 4 are lit">}}</td></tr>
<tr><td>LED 1 and 2: Use the D-Pad<BR>
{{<imgproc src="/tutorials/scuttle-gamepad/pi-game-cont-1and2.jpg" resize="300x" declaredimensions=true alt="Led 1 and 4 are lit">}}</td><td>LED 1 and 4: Use the Joystick<BR>
{{<imgproc src="/tutorials/scuttle-gamepad/pi-game-cont-1and4.jpg" resize="300x" declaredimensions=true alt="Led 1 and 4 are lit">}}</td></tr>
</table>

## Next steps

You can now drive your rover with a wireless controller.
If you'd like to do more with your rover, check out one of these tutorials:

{{< cards >}}
{{% card link="/tutorials/get-started/try-viam-sdk/" %}}
{{% card link="/tutorials/services/try-viam-color-detection/" %}}
{{% card link="/tutorials/services/navigate-with-rover-base/" %}}
{{< /cards >}}
