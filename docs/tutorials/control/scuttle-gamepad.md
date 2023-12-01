---
title: "Drive a Rover (like SCUTTLE) Using a Gamepad with a Dongle"
linkTitle: "Drive a Rover with a Dongle Gamepad"
type: "docs"
description: "Drive a wheeled rover with a Bluetooth gamepad that has a dongle."
webmSrc: "/tutorials/videos/scuttle-gamepad-preview.webm"
mp4Src: "/tutorials/videos/scuttle-gamepad-preview.mp4"
videoAlt: "Drive a Scuttle Robot with a Bluetooth gamepad."
images: ["/tutorials/videos/scuttle-gamepad-preview.gif"]
aliases:
  - "/tutorials/scuttle-gamepad/"
  - "/tutorials/scuttlebot/scuttle-gamepad/"
tags: ["base", "scuttle", "gamepad"]
authors: []
languages: []
viamresources: ["base", "input_controller"]
level: "Intermediate"
date: "2022-08-10"
# updated: ""
cost: 575
---

This tutorial teaches you how to add a Bluetooth dongle gamepad controller to your wheeled robot.
By the end of this tutorial, you'll be able to drive your rover around like an RC car.

{{% alert title="Tip" color="tip" %}}

If your gamepad has a dongle, keep reading.
If your gamepad does not have a dongle, check out [Drive a Yahboom Rover with a Gamepad](../yahboom-rover/#connecting-a-bluetooth-controller) for Bluetooth pairing instructions.

{{% /alert %}}

## Requirements

You will need the following hardware to complete this tutorial:

- A wheeled rover, configured with a [base component](/components/base/) on the [Viam app](https://app.viam.com/).
  This tutorial uses a [SCUTTLE rover](https://www.scuttlerobot.org/shop/) as an example but you can complete this tutorial using a different rover.
  - Regardless of the type of base you are using, [Setting up a SCUTTLE with Viam](/tutorials/configure/scuttlebot/) is a good place to start if you haven't already configured your base.
- [EasySMX ESM-9101 Wireless Controller](https://www.amazon.com/Wireless-Controller-EasySMX-ESM-9101-Gamepad/dp/B07F1NLGW2?th=1) or a similar gamepad and dongle.
  This is the controller that comes with the SCUTTLE rover.

{{<video webm_src="/tutorials/videos/scuttledemos_gamepad.webm" mp4_src="/tutorials/videos/scuttledemos_gamepad.mp4" alt="Controlling a Scuttle robot using a Bluetooth gamepad" poster="/tutorials/scuttlebot/scuttledemos_gamepad.jpg">}}

## Set up the hardware

Plug the gamepad Bluetooth dongle into a USB port on the rover's [board](/components/board/).
Turn on power to the rover.

## Add the controller to the rover's config

Go to your rover's **Config** tab on the [Viam app](https://app.viam.com/).

{{< tabs >}}
{{% tab name="Config Builder" %}}

Configure a [gamepad](/components/input-controller/gamepad/):

- Click **Create component**.
- Select `input_controller` for the component **Type**.
- Select `gamepad` for the **Model**.
- Enter `my-gamepad` as the component **Name**.
- Click **Create**.

![Blank configuration JSON](/tutorials/scuttle-gamepad/gamepad-config.png)

{{% /tab %}}
{{% tab name="Raw JSON" %}}

If instead of using the config builder, you prefer to write raw JSON, switch to [**Raw JSON** mode](/build/configure/#the-config-tab) on the **Config** tab.
Inside the `components` array of your config, add the following configuration for your [gamepad](/components/input-controller/gamepad/):

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "my-gamepad",
  "model": "gamepad",
  "type": "input_controller",
  "namespace": "rdk",
  "attributes": {},
  "depends_on": []
}
```

{{% /tab %}}
{{< /tabs >}}

The controller config adds the gamepad controller to your robot.
However, it is not functional yet.
To make it functional, you need to add the base remote control service.

## Add the base remote control service

Services are software packages that provide robots with higher level functionality.
To link the controller's input to the base functionality, you need to configure the [base remote control service](/mobility/base-rc/):

{{< tabs >}}
{{% tab name="Config Builder" %}}

- Go to the **Services** subtab of your robot's **Config** tab.
- In the **Create service** panel, click the **Type** dropdown and select `Base Remote Control`.
- Enter `gamepad_service` for the **Service** **name**.
- Click **Create service**.

Copy and paste the following into the empty **Attributes** field, replacing `<your-base-name>` with your base's name.

```json {class="line-numbers linkable-line-numbers"}
{
  "base": "<your-base-name>",
  "input_controller": "my-gamepad"
}
```

<br>

![Service configuration](/tutorials/scuttle-gamepad/gamepad-service-config.png)

{{% /tab %}}
{{% tab name="Raw JSON" %}}

If instead of using the config builder, you prefer to write raw JSON, switch to [**Raw JSON** mode](/build/configure/#the-config-tab) on the **Config** tab.
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

Click **Save config**, then go to the **Control** tab.

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
