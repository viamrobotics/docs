---
title: "How to Configure a SCUTTLE Robot with a Camera"
linkTitle: "Configure a SCUTTLE Robot"
weight: 15
type: "docs"
description: "Instructions for configuring a SCUTTLE Robot on the Viam platform."
tags: ["base", "camera", "raspberry pi", "scuttle"]
---
## Requirements

* A Raspberry Pi with Raspberry Pi OS 64-bit Lite and the viam-server installed.

Refer to [Installing Raspberry Pi OS on the Raspberry Pi](/installation/rpi-setup/#installing-raspberry-pi-os), if necessary.

* <a href="https://www.scuttlerobot.org/shop/" target="_blank">A SCUTTLE Robot</a>[^asr]
* A USB camera (webcam)

[^asr]: SCUTTLE Robot: <a href="https://www.scuttlerobot.org/shop/" target="_blank">ht<span></span>tps://www.scuttlerobot.org/shop/</a>

## Start configuring your robot

<ol>
<li class="spacing">Go to the Viam app at <a href="https://app.viam.com" target="_blank">https://app.viam.com</a>.</li>
<li class="spacing">If you already created your robot in the app, navigate to its <strong>CONFIG</strong> tab and skip to <a href="./#configuring-the-board">Configuring the board</a>.</li>
<li class="spacing">Create an <strong>Organization</strong>.
If you already have an Organization, then this step is optional. If you need help with organizations and locations, see our <a href="/getting-started/app-usage/">guide to using the Viam app</a>.</li>
<li class="spacing">Create a <strong>Location</strong>.
If you already have a Location, then this step is optional.</li>
<li class="spacing">Create a <strong>robot</strong> and navigate to its <strong>CONFIG</strong> tab.
We will stay in <strong>Builder</strong> mode for this tutorial (as opposed to <strong>Raw JSON</strong>).</li>
<img src="../img/scuttlebot/createcomponent.png" alt="A screenshot of the Viam app UI showing the CONFIG tab of a robot."></ol>

{{% alert title="Note" color="note" %}}  
When naming components, remember to use consistent letter casing to avoid problems with "missing" components.
{{% /alert %}}

## Configuring the board

Add your first component, the <a href="/components/board/">board</a> (in this case the Raspberry Pi).</li>
<ol>
<li class="spacing">Enter a name for your board in the <strong>Name</strong> field.
In this tutorial, we've named the board "local."
As long as you're consistent, you can name the board whatever you want.</li>
<li class="spacing">Select the component <strong>Type</strong>, "board."</li>
<li class="spacing">Select "pi" from the <strong>Model</strong> drop-down.</li>
<li class="spacing">Click <strong>Create Component</strong> and the board component panel will expand.
We don't need to worry about any other attributes for this component.</li>
<img src="../img/scuttlebot/board-empty-json.png" alt="Screenshot of the component configuration panel for a board component.
The name (local), type (board) and model (pi) are shown at the top of the panel. No other attributes are configured."></ol>

## Configuring the motors

### Adding the right motor

The next step is to add a motor and make it spin a wheel.

<ol>
<li class="spacing">Begin by adding the right motor, naming the component "right".</li>
<li class="spacing">Select "motor" from the <strong>Type</strong> drop-down.</li>
<li class="spacing">Select "gpio" from the <strong>Model</strong> drop-down.</li>
<li class="spacing">Click <strong>Create Component</strong>, which will generate the motor component panel.</li>
<li class="spacing">Then select <code>local</code> from the <strong>Board</strong> drop-down (since the motor is wired to the Raspberry Pi named "local").</li>
<li class="spacing">Set <strong>Max RPM</strong> to <code>100</code>.

<li class="spacing">Next, you'll need to describe how the motor is wired to the Pi:</li>
<ol type="a">
  <li class="spacing">Switch the Component Pin Assignment Type to <strong>In1/In2</strong>.</li>
  <li class="spacing">Set <strong>A/In1</strong> to <code>16</code>.</li>
  <li class="spacing">Set <strong>B/In2</strong> to <code>15</code>.</li>
  <li class="spacing">Leave the <code>pwm</code> (pulse-width modulation) pin blank, because this specific motor driver’s configuration does not require a separate PWM pin.</li>
</ol></ol>
<img src="../img/scuttlebot/pi-rhwheel.png" alt="Screenshot of the motor config panel with the attributes set as described above.">
<br><br>

{{% expand "Click to view the raw JSON for the right motor" %}}
```json-viam
{
  "name": "right",
  "type": "motor",
  "model": "gpio",
  "attributes": {
    "pins": {
      "a": "16",
      "b": "15",
      "pwm": ""
    },
    "board": "local",
    "max_rpm": 100,
    "dir_flip": false
  },
  "depends_on": []
}
```
{{% /expand %}}

{{% alert title="Note" color="note" %}}  
If your wheel turns in reverse when it should turn forward, add the <code>dir_flip</code> attribute (found by clicking <strong>SHOW OPTIONAL</strong>) and set it to "true."
{{% /alert %}}

### Testing the motor configuration

Having configured a board and a motor component, you can now actuate your motor.
Save the config by clicking **SAVE CONFIG** at the bottom of the page, then click over to the **CONTROL** tab.

Here you'll see a panel for the right `motor`.
You'll use this panel to set the motor's `power` level.

<img src="../img/scuttlebot/pi-moverhmotor.png">

Be careful when activating your robot!
Start with the power level set to 10% and increase it incrementally until the wheel rotates at a reasonable speed, clicking **Run** at each increment.

{{% alert title="Note" color="note" %}}  
A "whining" sound emitted from the motor indicates that the power level is not high enough to turn the armature.
If this happens, increase the power level by 10% increments until it starts to turn.
{{% /alert %}}
At this point, the right-side wheel should be working.

### Adding the left motor

Now, you're ready to add the left-side motor.
This will be very similar to adding the right motor.

<ol>
<li class="spacing">Name the component "left".</li>
<li class="spacing">Select "motor" from the <strong>Type</strong> drop-down.</li>
<li class="spacing">Select "gpio" from the <strong>Model</strong> drop-down.</li>
<li class="spacing">Click <strong>Create Component</strong>.</li>
<li class="spacing">Select <code>local</code> from the <strong>Board</strong> drop-down.</li>
<li class="spacing">Set the <strong>Max RPM</strong> attribute to <code>100</code>.
<li class="spacing">Configure the motor's pins:</li>
<ol type="a">
<li class="spacing">Switch the Component Pin Assignment Type to <strong>In1/In2</strong>.</li>
  <li class="spacing">Set <strong>A/In1</strong> to <code>12</code>.</li>
  <li class="spacing">Set <strong>B/In2</strong> to <code>11</code>.</li>
</ol>
</ol>

{{% expand "Click to view the raw JSON for the left motor" %}}
```json-viam
{
  "name": "left",
  "type": "motor",
  "model": "gpio",
  "attributes": {
    "pins": {
      "a": "12",
      "b": "11",
      "pwm": ""
    },
    "board": "local",
    "max_rpm": 100,
    "dir_flip": false
  },
  "depends_on": []
}
```
{{% /expand %}}
<br>

With both motors configured, the **CONTROL** tab now display panels for both motors:

<img src="../img/scuttlebot/scuttle-bothmotors.png">

Viam ([https://app.viam.com](https://app.viam.com)) displays component panels in order of their creation.
Don't worry if your motor panels are not adjacent.

## Configuring the base

It's time to configure a [base component](/components/base/), which describes the geometry of your chassis and wheels so that the software can calculate how to steer the rover in a coordinated way.
Configuring a base component will give you a nice UI for moving the rover around.

From the **CONFIG** tab:
1. Give your base a name.
1. Enter "base" in **Type**.
1. Enter "wheeled" in **Model**.
1. In the **Right Motors** drop-down select "right."
1. In the **Left Motors** drop-down select "left."
1. From **Depends On**, select "local."
1. Enter "400" in <code>width_mm</code> (measured between the midpoints of the wheels).
1. Enter "250" in <code>wheel_circumference_mm</code>.

    The <code>left</code> and <code>right</code> attributes represent the motors corresponding to the left and right sides of the rover.
    Since we named the motors "left" and "right", you can simply add “left” and “right” between the brackets for your set of motors, respectively.

The attributes of your base component's config should look something like this:

```json-viam
{
 "width_mm": 400,
 "wheel_circumference_mm": 250,
 "left": ["left"],
 "right": ["right"]
}
```

When you save the config and switch to the **CONTROL** tab, you'll see new control buttons for the base.
In the **Keyboard** tab, toggle your keyboard control to active.
Use **W** and **S** to go forward and back, and **A** and **D** to arc and spin.

<img src="../img/scuttlebot/pi-kybrd-control.png" width="300px">

If you click the **Discrete** tab, then you'll see different movement modes such as <code>Straight</code> and <code>Spin</code>; and different movement types such as <code>Continuous</code> and <code>Discrete</code> and directions such as <code>Forwards</code> and <code>Backwards</code>.

<img src="../img/scuttlebot/pi-discrete.png"><br>

Now you have a rover that you can drive using Viam's UI!
Awesome!

Try driving your SCUTTLE Robot around using the WASD keyboard controls described above.

{{% alert title="Caution" color="caution" %}}  
Ensure that your robot has sufficient space to drive around without hitting anyone or anything.
{{% /alert %}}

## Configuring the camera 

Finally, we'll add a camera to your SCUTTLE Robot.

1. Enter a name of your choice in **Name**.
2. Enter "camera" in **Model**.
4. Click <strong>Create Component</strong>.

Now, you'll see the config panel for the camera component:
<img src="../img/scuttlebot/pi-cam-control.png">

On the camera config panel, set the <code>video_path</code>.
This is often "video0," but please see our [camera configuration tutorial](/tutorials/configure-a-camera/#connect-and-configure-a-webcam) for more information on choosing the correct video path.

Once you save the config, you'll be able to see your camera's stream in the **CONTROL** tab.

## On completion

After successfully completing this tutorial, you have a fully configured SCUTTLE robot.
You can drive it around and view its camera stream.

To take things to the next level, check out our [Color Detection with SCUTTLE Robot](../color-detection-scuttle/) tutorial or create your own camera-related tutorial.
Alternatively, you can  check out our [Bluetooth Gamepad For SCUTTLE](../scuttle-gamepad/) tutorial or our [Line Follower Robot tutorial](../webcam-line-follower-robot/).

## Documents referenced

* [Installing Raspberry Pi OS on the Raspberry Pi](/installation/rpi-setup/#installing-raspberry-pi-os)

* [Color Detection with SCUTTLE Robot on Viam](../color-detection-scuttle/)

* [Controlling a SCUTTLE Robot on Viam with a Bluetooth Gamepad](../scuttle-gamepad/)

* [Line Following with SCUTTLE Robot on Viam](../webcam-line-follower-robot/)
