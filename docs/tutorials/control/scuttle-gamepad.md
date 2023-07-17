---
title: "Drive a SCUTTLE Robot with a Bluetooth Gamepad"
linkTitle: "Drive a SCUTTLE with a Gamepad"
weight: 20
type: "docs"
description: "Drive a SCUTTLE Robot with a Bluetooth gamepad from the Viam app."
webmSrc: "/tutorials/videos/scuttle-gamepad-preview.webm"
mp4Src: "/tutorials/videos/scuttle-gamepad-preview.mp4"
videoAlt: "Drive a SCUTTLE Robot with a Bluetooth gamepad."
images: ["/tutorials/videos/scuttle-gamepad-preview.gif"]
aliases:
    - "/tutorials/scuttle-gamepad/"
    - "/tutorials/scuttlebot/scuttle-gamepad/"
tags: ["base", "scuttle", "gamepad"]
authors: []
languages: []
viamresources: [ "base", "input_controller" ]
level: "Beginner"
date: "10 August 2022"
cost: 575
---

The purpose of this tutorial is to add a Bluetooth gamepad input controller to a SCUTTLE Robot.
On completion of this tutorial, you'll be able to drive the SCUTTLE around like an RC car using the EasySMX ESM-9101 Wireless Controller.

## Prerequisites

* A pre-configured and controllable (using a keyboard and the Viam app ([app.viam.com](https://app.viam.com)) SCUTTLE Robot.
Refer to the [Setting up a SCUTTLE with Viam](/tutorials/configure/scuttlebot/) tutorial, if necessary.

* Connection to the Viam app
* EasySMX ESM-9101 Wireless Controller

The following video demonstrates controlling a SCUTTLE Robot using a Bluetooth gamepad:

{{<video webm_src="/tutorials/videos/scuttledemos_gamepad.webm" mp4_src="/tutorials/videos/scuttledemos_gamepad.mp4" alt="Controlling a SCUTTLE Robot using a Bluetooth gamepad" poster="/tutorials/scuttlebot/scuttledemos_gamepad.jpg">}}

## Adding the controller to the SCUTTLE's config

To add this controller to the robot’s config, from the Viam app ([app.viam.com](https://app.viam.com)), click on our old friend, **New COMPONENT**.
<OL>
<li>On the Create Component screen, enter "gamepad" as the component <strong>Name</strong>  and select "input_controller" for the component <strong>Type</strong>. </li>

<li>There are no <strong>Model</strong> options for input_controllers.
Therefore, for <strong>Model</strong>, please manually enter, "gamepad," (without the quotes) then press Tab. The Viam app will retain your entry.</li>

<li>Click <strong>New Component</strong>. The Viam app opens the Component Config panel for the gamepad. </li>
<li>On the Component Config panel, leave <strong>Depends On</strong> set to empty.</li>

The controller config adds the gamepad controller to your robot.
However, it does not wire it up to any functionality.
This requires a Service.

## Adding a Service

To link the controller's input to the base functionality, we need to add our first `service`.
Services are the software packages that provide our robots with cool and powerful functionality.

1. Click **Create Service** under **services** at the top of the Viam app ([app.viam.com](https://app.viam.com)).
2. Enter "Base Remote Control" for **Component** `type`. "Base Remote Control" is a service we provide for driving a rover with a gamepad.
3. Enter **scuttle_gamepad** for the **Service** `name`.

![Create service builder](/tutorials/scuttle-gamepad/pi-game-create-service.png)

Copy and paste the following into the empty **Attributes** field:
</OL>

```json {class="line-numbers linkable-line-numbers"}
{
 "base": "scuttle",
 "input_controller": "gamepad"
}
```

![Blank configuration json](/tutorials/scuttle-gamepad/pi-game-game-config-blank.png)

After adding the **Attributes**, your config screen should appear similar to this:

![Service configuration](/tutorials/scuttle-gamepad/pi-game-service-config.png)

Save the configuration and visit the control UI on the Viam app ([app.viam.com](https://app.viam.com)).

You should see the panel for the Controller Service and its connection indicator.
This is how your web UI will look.
Note the green connection indicator:

![Gamepad input UI](/tutorials/scuttle-gamepad/pi-game-controller-panel.png)

At this point, you should be able to move the SCUTTLE. If you are in the specific mode that allows you to use the Joystick (#7), it will change the values:

```sh {id="terminal-prompt" class="command-line" data-prompt="$" data-output="1-10"}
"X
0.0000
Y
0.0000"
```

If you are in the specific mode that allows you to use the D-Pad (#8), it will change the values:

```sh {id="terminal-prompt" class="command-line" data-prompt="$" data-output="1-10"}
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

To change the in-use movement/direction control on the gamepad between the D-Pad and the Joystick, press and hold the Home button (#11) until it displays the lighted segment combination for the gamepad configuration you need.
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
