---
title: "Configuring a SCUTTLE Robot with a Camera"
linkTitle: "Configuring a SCUTTLE Robot"
weight: 20
type: "docs"
description: "Instructions for configuring a SCUTTLE Robot on the Viam platform"
---
This tutorial will guide you through setting up a SCUTTLE Robot with a camera.

## Requirements

* A Raspberry Pi with Raspian OS 64-bit Lite and the viam-server installed.
Refer to [Installing Raspian on the Raspberry Pi](../../getting-started/installation/#installing-raspian-on-the-raspberry-pi), if necessary.
* A SCUTTLE Robot ([https://www.scuttlerobot.org/shop/]((https://www.scuttlerobot.org/shop/))
* A Camera

## Configuring the Board
Note: When naming components, remember to use consistent letter casing to avoid problems with "missing" components.

<ol type="D">
<li class="spacing">Begin by accessing <a href="https://app.viam.com"> Viam at https://app.viam.com</a>.</li>
<li class="spacing">If you are using an existing robot config, select your robot's config and skip to Step 5.</li>
<li class="spacing">Create an <strong>Organization</strong>.
If you already have an Organization, then this step is optional. </li>
<li class="spacing">Create a <strong>Location</strong>.
If you already have a Location, then this step is optional. </li>
<img src="../img/createcomponent.png">
<li class="spacing">Add your first component, the Raspberry Pi.</li>
<ol type="a">
    <li class="spacing">Enter a name for your robot in <strong>Name</strong>, then click <strong>Add</strong> to add your robot and access your robot's configuration page.
    In this tutorial, we've named the board "local."
    As long as you're consistent, you can name the <code>board</code> whatever you want.</li>
    <li class="spacing">Select the component <strong>Type</strong>, "board."</li>
    <li class="spacing">Select "pi" from the <strong>Model</strong> drop-down.</li>
    <li class="spacing">Click <strong>Save Config</strong> to save the new component, which will generate an empty JSON configuration:</li></ol></ol>
<img src="../img/board-empty-json.png" alt="This image is the component configuration panel for a board component.
The Depends On drop-down listbox has no selection.
Initially, the left-side Attributes panel for board component is empty.
The right-side panel contains a list of available board component Attributes.">

## Configuring the Motors and Wheels
### Adding the Right-Side Wheel

The next step is to add a wheel and make it spin.
The first step is to create a <strong>NEW COMPONENT</strong>.

<ol>
<li class="spacing">Begin by adding the Right-Side Wheel, naming the component <code>right</code>.</li>
<li class="spacing">Select "motor" from the <code>Type</code> drop-down.</li>
<li class="spacing">Select "gpio" from the <code>Model</code> drop-down.</li>
<li class="spacing">Click <strong>Create Component</strong>, which will bring you to the following screen:</li>
<img src="../img/pi-rhwheel-f.png"  alt="Fancy component config screen for a Motor."width="515px"><br>

This screen provides read-only displays of JSON configuration and allows you to select which board controls this motor, to toggle the <strong>Component Pin Assignment</strong> between Direction and Int1/Int2, and to <strong>Enable Pins</strong> (i.e., set them to High, Low, or Neither).
Also, you can add a <strong>Frame</strong> and a <strong>Data Capture Pathway</strong>, and set the <strong>Depends On</strong>.<br>


<li class="spacing">Next, you'll need to tell Viam how the motor is wired to the Pi:</li>
<ol type="a">
<li class="spacing">Click <strong>Go to Advanced</strong>. You'll now see the current JSON attributes for this motor component and a reference for the available attributes:</li>
<img src="../img/pi-rhwheel.png" alt="Advanced component config screen for a Motor.">
<li class="spacing">Then select <code>local</code> from the <strong>Depends On</strong> drop-down (since the motor is wired to the Raspberry Pi named "local."</li>

<li class="spacing">Make the following changes to the JSON:</li>
<OL type="i">
            <li class="spacing">Set <code>a</code> to <code>16</code></li>
            <li class="spacing">Set <code>b</code> to <code>15</code></li>
            <li class="spacing">Leave the <code>dir</code> and <code>pwm</code> (pulse-width modulation) pins blank, because this specific motor driver’s configuration does not require those settings.</li>
            <li class="spacing">Set <code >max_rpm</code> to <code>100</code></li>
            <li class="spacing">Set <code>board</code> to <code>local</code></li>
</ol>
</ol>
</OL>

Note: If your wheel turns in reverse when it should turn forward, add the <code>dir_flip</code> attribute and set it to "true."

<img src="../img/pi-rhwheel.png">

**Right-Wheel JSON**

```JSON
{
 "pins": {
   "a": "16",
   "b": "15",
   "dir": "",
   "pwm": ""
 },
 "board": "local",
 "max_rpm": 100
}
```

### Testing the Motor Configuration

Having entered a board and a motor component, you can now actuate your motor.
Save the config by clicking **SAVE CONFIG** at the bottom of the page, then click **CONTROL** at the top of the page to navigate to the Control Page.

On the Control page, you'll see a panel for the right `motor`.
You'll use this panel to set the motor's `power` level.

<img src="../img/pi-moverhmotor.png">

Be careful when activating your robot! Start with the power level (RPM) set to 10% and increase it incrementally until the wheel rotates at a satisfactory speed.

Note: A "whining" sound emitted from the motor indicates that the power level is not high enough to turn the armature. If this happens, increase the power level by 10%.

At this point, the right-side wheel should be working.

### Adding the Left-Side Wheel

Now, you're ready to add the left-side wheel to start driving this robot in a coordinated manner.
To do this, you’ll have to add the second <code>motor</code> controller and link them with a <code>base</code>.

Once again, you’ll select **NEW COMPONENT**. The config attributes for the <code>left motor</code> controller are very similar to that of the <code>right</code> motor component that you already configured (since the hardware is the same and connected to a single <code>board</code>).

<ol>
<li class="spacing">Add the Left Side Wheel, naming the component <code>left</code>.</li>
<li class="spacing">Select "motor" from the <code>Type</code> drop-down.</li>
<li class="spacing">Select "gpio" from the <code>Model</code> drop-down.</li>
<li class="spacing">Click <strong>Create Component</strong>.
Viam opens the component config panel for the wheel.</li>
<li class="spacing">Now, tell Viam how this motor is wired to the Pi:</li>
<ol type="a">
<li class="spacing" style="list-style-type:lower-alpha">First, select the board name from the <strong>Depends On</strong>, which is "local." 

<li class="spacing" style="list-style-type:lower-alpha">Now, make the following changes in the Left-Wheel's JSON:</li>
<OL type="a">
            <li class="spacing" style="list-style-type:lower-roman">Set <code>a</code> to <code>12</code></li>
            <li class="spacing" style="list-style-type:lower-roman">Set <code>b</code> to <code>11</code></li>
            <li class="spacing" style="list-style-type:lower-roman">Leave the <code>dir</code> and <code>pwm</code> (pulse-width modulation) pins blank, because this specific motor driver’s configuration does not require those settings.</li>
            <li class="spacing" style="list-style-type:lower-roman"><code >Set max_rpm</code> to <code>100</code></li>
            <li class="spacing" style="list-style-type:lower-roman"><code>Set board</code> to <code>local</code></li>
</ol>
</ol>
</OL>

**Left-Wheel JSON**:

```JSON
{
 "pins": {
   "a": "12",
   "b": "11",
   "dir": "",
   "pwm": ""
 },
 "board": "local",
 "max_rpm": 100
}
```

With both motors configured, the component page now display panels for both motors:

<img src="../img/scuttle-bothmotors.png">

Viam ([https://app.viam.com](https://app.viam.com)) displays component panels in order of their creation.
Therefore, it's normal if your motor panels are not adjacent.

## Configuring the Base

Unite your wheels with a <code>base</code> component, which describes the physical structure onto which your components are mounted.
Configuring a <code>base</code> component will give you a nice UI for moving the rover around.

From the Config screen:

1. Enter "base" in **Name**.
2. Enter "wheeled" in **Model**.
3. From **Depends On**, select three items: "left," "right," and "local."
4. Enter "400" in <code>width_mm</code> (measured between the midpoints of the wheels).
5. Enter "250" in <code>wheel_circumference_mm</code>.
6. Enter "left" in <code>"left"</code>
7. Enter "right" in <code>"right"</code>


    The <code>left</code> and <code>right</code> attributes are intended to be the motors corresponding to the left and right sides of the rover.
    You can simply add “left” and “right” between the brackets for your set of motors, respectively.

If you wish to copy and paste it, see below for the code for your base attributes.

```JSON
{
 "width_mm": 400,
 "wheel_circumference_mm": 250,
 "left": ["left"],
 "right": ["right"]
}
```

When you save the Config and switch to the **Control** view, you'll see new control buttons for the <code>base</code>.
In the **Keyboard** tab, toggle your keyboard control to active, and then use **W** and **S** to go back and forth, and **A** and **D** to arc and spin.

<img src="../img/pi-kybrd-control.png" width="300px">

If you click the **Discrete** tab, then you'll see different movement modes such as <code>Straight</code> and <code>Spin</code>; and different movement types such as <code>Continuous</code> and <code>Discrete</code> and directions such as <code>Forwards</code> and <code>Backwards</code>.

<img src="../img/pi-discrete.png">

Now you have a rover that you can drive via Viam's UI at [https://app.viam.com](https://app.viam.com).

Control the wheels using the keyboard controls described above.
When you feel ready, try driving your SCUTTLE Robot around.

{{< caution >}}
Ensure that your robot has sufficient space to drive around without hitting anyone or anything.
{{< /caution >}}

## Configuring the Camera 

Finally, we'll add a camera to your SCUTTLE Robot.
To begin, click <strong>NEW COMPONENT</strong> before proceeding to the steps below.

1. Enter "camera" in **Name**.
2. Enter "camera" in **Model**.
3. From **Depends On**, select "local."
4. Click <strong>Create Component</strong>.

Now, you'll see the config panel for the camera component:
<img src="../img/pi-cam-control.png">

On the Camera Config panel:

1. Enter "camera" in **Name**.
2. Enter "camera" in **Model**.
3. From **Depends On**, select "local."
4. In the JSON, set <code>video_path</code> to "video0."

If you wish to copy and paste code for your camera, use the below:

```JSON
{
 "intrinsic_parameters": {
   "width_px": 0,
   "height_px": 0,
   "fx": 0,
   "fy": 0,
   "ppx": 0,
   "ppy": 0
 },
 "distortion_parameters": {
   "rk1": 0,
   "rk2": 0,
   "rk3": 0,
   "tp1": 0,
   "tp2": 0
 },
 "stream": "",
 "width_px": 0,
 "height_px": 0,
 "debug": false,
 "format": "",
 "video_path": "video0",
 "video_path_pattern": ""
}
```

Once you save the config, you'll be able to see your camera's stream in the Control tab.

## On Completion
After successfully completing this tutorial, you should have a fully functional SCUTTLE Robot. You can drive it around and view its camera stream. To take things to the next level, check out our [Color Detection with SCUTTLE Robot](../color-detection-scuttle) tutorial or create your own camera-related tutorial.
Alternatively, you can  check out our [Bluetooth Gamepad For SCUTTLE](../scuttle-gamepad/) tutorial or our [Line-Follower Robot] tutorial (../webcam-line-follower-robot).

## Documents Referenced

  * **Installing Raspian on the Raspberry Pi**: [https://docs.viam.com/getting-started/installation/#installing-raspian-on-the-raspberry-pi](https://docs.viam.com/getting-started/installation/#installing-raspian-on-the-raspberry-pi)

  * **Color Detection with SCUTTLE Robot on Viam**: [https://docs.viam.com/tutorials/color-detection-scuttle/](https://docs.viam.com/tutorials/color-detection-scuttle/)

  * **Controlling a SCUTTLE Robot on Viam with a Bluetooth Gamepad**: [https://docs.viam.com/tutorials/scuttle-gamepad/](https://docs.viam.com/tutorials/scuttle-gamepad/)

  * **Line Following with SCUTTLE Robot on Viam**: [https://docs.viam.com/tutorials/webcam-line-follower-robot/](https://docs.viam.com/tutorials/webcam-line-follower-robot/)
