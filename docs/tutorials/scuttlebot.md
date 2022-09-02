---
title: Setting up a Scuttle with Viam
summary: Instructions for using the Viam App to Configure Raspberry Pi board for a Camera-Equipped Scuttle Robot
authors:
- Hazal Mescti (HM:ma)
date: 2022-07-13, revised on 2022-08-01
---
# Configuring a Camera-Equipped Scuttle Bot Two-Wheel Drive Rover
This tutorial will guide you through setting up a Scuttle Bot and Raspberry Pi micro-controller to use a camera.

The Raspberry Pi is a single-board computer into which you will wire all other components.

## Prerequisites

* Raspberry Pi with Raspian OS 64-bit Lite and Viam server installed.
Refer to the <a href="/getting-started/installation/#installing-raspian-on-the-raspberry-pi">Installing Raspian on the Raspberry Pi</a>, if necessary.
* The Pi is able to connect to the Viam App ([https://app.viam.com](https://app.viam.com))
* Scuttle Bot

## Configuring the Board
!!! note
    When naming components, remember to use consistent letter casing to avoid problems with "missing" components.

<ol type="I">
<li class="spacing">Begin by accessing <a href="https://app.viam.com">the Viam App at https://app.viam.com</a>.</li>
<li class="spacing">If you are using an existing Robot configuration, select your Robot's config and continue with Step 5.
Otherwise, complete all steps.</li>
<li class="spacing">Create an <strong>Org</strong>.
This step is optional if you already have an Organization.</li>
<li class="spacing">Create a <strong>Location</strong>.
This step is optional if you already have an <strong>Location</strong>.</li>
<img src="../img/createcomponent.png">
<li class="spacing">The first component is the Raspberry Pi, which is a single-board computer into which you will wire all other components.</li>
<ol type="a">
    <li class="spacing" style="list-style-type:lower-alpha">Enter a name for your robot in <strong>Name</strong>, then click <strong>Add</strong> to add your robot and access your robot's configuration page.
    In this tutorial, the board name is "local".
    You can name the <code>board</code> whatever you like as long as you are consistent when referring to it later.</li>
    <li class="spacing" style="list-style-type:lower-alpha">Select the component <strong>Type</strong>, which is "board".</li>
    <li class="spacing" style="list-style-type:lower-alpha">Select "pi" from the <strong>Model</strong> drop-down.</li>
    <li class="spacing" style="list-style-type:lower-alpha">Click <strong>Save Config</strong> to Save the new component (i.e., your Board component) and generate an empty JSON configuration:</li></ol></ol>
<img src="../img/board-empty-json.png" alt="This image is the component configuration panel for a board component.
The Depends On drop-down listbox has no selection.
Initially, the left-side Attributes panel for board component is empty.
The right-side panel contains a list of available board component Attributes.">

## Configuring the Motors and Wheels
### Adding the Right Side Wheel

The next step is to add a wheel and make it spin.
As with all other components, the first step is clicking <strong>CREATE A COMPONENT</strong>.

<ol>
<li class="spacing">Begin by adding the Right Side Wheel, naming the component <code>right</code>.</li>
<li class="spacing">Select "motor" from the <code>Type</code> drop-down.</li>
<li class="spacing">Select "gpio" from the <code>Model</code> drop-down.</li>
<li class="spacing">Click <strong>Create Component</strong>.
The Viam App returns the following screen:</li>
<img src="../img/pi-rhwheel-f.png"  alt="Fancy component config screen for a Motor."width="515px"><br>

This screen provides read-only displays of JSON configuration information and allows you to select which board controls this motor, to toggle the <strong>Component Pin Assignment</strong> between Direction and Int1/Int2, and <strong>Enable Pins</strong> (i.e., set them to High, Low, or Neither). 
You can also add a <strong>Frame</strong>, a <strong>Data Capture Pathway</strong>, and set the <strong>Depends On</strong>.<br>
Note that you will not make modifications to the "fancy" screen during the tutorial.


<li class="spacing">Now, tell Viam how this motor is wired to the Pi:</li>
<ol type="a">
<li class="spacing" style="list-style-type:lower-alpha">Click <strong>Go to Advanced</strong>. The Viam App now displays the advanced screen where the app displays the current JSON attributes for this motor component and a reference for the available attributes</li>
<img src="../img/PI-rhWheel.png" alt="Advanced component config screen for a Motor.">
<li class="spacing" style="list-style-type:lower-alpha">First, select <code>local</code> from the <strong>Depends On</strong> drop-down as the motor is wired to the Raspberry Pi board named, "local".</li>

<li class="spacing" style="list-style-type:lower-alpha">Make the following changes in the JSON:</li>
<OL type="i">
            <li class="spacing" style="list-style-type:lower-roman">Set <code>a</code> to <code>16</code></li>
            <li class="spacing" style="list-style-type:lower-roman">Set <code>b</code> to <code>15</code></li>
            <li class="spacing" style="list-style-type:lower-roman">Leave the <code>dir</code> and <code>pwm</code> (pulse-width modulation) pins blank, because this specific motor driver’s configuration does not require those settings.</li>
            <li class="spacing" style="list-style-type:lower-roman">Set <code >max_rpm</code> to <code>100</code></li>
            <li class="spacing" style="list-style-type:lower-roman">Set <code>board</code> to <code>local</code></li>
</ol>
</ol>
</OL>

!!! note
    If your wheel turns in reverse when it should turn forward, add the <code>dir_flip</code> attribute and set it to "true".

The Viam App returns the following screen with empty JSON attributes for the motor component and a reference for the available attributes.

<img src="../img/PI-rhWheel.png">


**Right Wheel JSON**

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

On the Control Page, you will see a panel for the right `motor`.
You will use this panel to set the motor's `power` level.

<img src="../img/PI-moveRhMotor.png">

Please be careful when activating your robot! Start with the power level (RPM) set to 10% and increase it incrementally (about 10% per increase), activating the motor at each step until the wheel rotates at a speed you like when you press run.
You can also change the direction of the rotation.

!!! note
    A "whining" sound emitted from the motor indicates that the power level is not high enough to turn the armature which is normal.Increase the power level by 10%.

At this point, the wheel on one side of your robot should be working through the Viam App ([https://app.viam.com](https://app.viam.com)).

### Adding the Left Side Wheel

Now add the second wheel to see if you can get this bot driving in a coordinated manner.
To do this, you’ll have to add the other <code>motor</code> controller and link them together with a <code>base</code>.

To do this, you’ll once again select <code>CREATE A COMPONENT</code> The config attributes for the <code>left motor</code> controller are very similar to that of the <code>right</code> motor component that you have already configured, which makes sense as the hardware is the same and it is connected to the same <code>board</code>.

Some of the differences are the <code>Name</code> which is <code>left</code> and the pins that it connects to.

<ol>
<li class="spacing">Add the Left Side Wheel, naming the component <code>left</code>.</li>
<li class="spacing">Select "motor" from the <code>Type</code> drop-down.</li>
<li class="spacing">Select "gpio" from the <code>Model</code> drop-down.</li>
<li class="spacing">Click <strong>Create Component</strong>.
The Viam App opens the Component config Panel for the wheel.</li>
<li class="spacing">Now, tell Viam how this motor is wired to the Pi:</li>
<ol type="a">
<li class="spacing" style="list-style-type:lower-alpha">First, select the board name from the <strong>Depends On</strong>, which is "local" in this example, as the motor is wired to the Raspberry Pi board named, "local".</li>

<li class="spacing" style="list-style-type:lower-alpha">Now, make the following changes in the Left Wheel's JSON:</li>
<OL type="a">
            <li class="spacing" style="list-style-type:lower-roman">Set <code>a</code> to <code>12</code></li>
            <li class="spacing" style="list-style-type:lower-roman">Set <code>b</code> to <code>11</code></li>
            <li class="spacing" style="list-style-type:lower-roman">Leave the <code>dir</code> and <code>pwm</code> (pulse-width modulation) pins blank, because this specific motor driver’s configuration does not require those settings.</li>
            <li class="spacing" style="list-style-type:lower-roman"><code >Set max_rpm</code> to <code>100</code></li>
            <li class="spacing" style="list-style-type:lower-roman"><code>Set board</code> to <code>local</code></li>
</ol>
</ol>
</OL>

**Left Wheel JSON**:

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

<img src="../img/scuttle-bothMotors.png">

!!! note
    The Viam App ([https://app.viam.com](https://app.viam.com)) displays component panels in the order of their creation.
    If your motor panels are not adjacent, that is normal.

## Configuring the Base

Unite your wheelsets with a <code>base</code> component, which describes the physical structure onto which your components are mounted.
Configuring a <code>base</code> component will give you a nice UI for moving the rover around.

From the Config screen:

1. Enter "base" in **Name**.
2. Enter "wheeled" in **Model**.
3. From **Depends On**, select three items: "left," "right," and "local," are the components that comprise our <code>base</code>.
4. Enter "400" in <code>width_mm</code> (measured between the midpoints of the wheels).
5. Enter "250" in <code>wheel_circumference_mm</code>.
6. Enter "left" in <code>"left"</code>
7. Enter "right" in <code>"right"</code>

!!! note
    The <code>left</code> and <code>right</code> attributes are intended to be the motors corresponding to the left and right sides of the rover.
    You can simply add “left” and “right” between the brackets for your set of motors, respectively.

Here is the code of your base attributes if you wish to copy and paste it.

```JSON
{
 "width_mm": 400,
 "wheel_circumference_mm": 250,
 "left": ["left"],
 "right": ["right"]
}
```

When you save the Config and switch to the **Control** view, the Viam App displays new control buttons for the <code>base</code> functionality.
In the **Keyboard** tab, you can toggle your keyboard control to active, and then use **W** and **S** to go back and forth, and **A** and **D** to arc and spin.

<img src="../img/pi-kybrd-control.png" width="300px">

If you click the **Discrete** tab, you can see different movement modes just as <code>Straight</code> and <code>Spin</code>; and different movement types such as <code>Continuous</code> and <code>Discrete</code> and directions <code>Forwards</code> and <code>Backwards</code>.

<img src="../img/pi-discrete.png">

Now you have a rover that you can drive via the Viam App's WebUI at [https://app.viam.com](https://app.viam.com).

Control the scuttle's wheels using the WASD movement controls to gain a sense of how they operate.
When you feel ready, try driving your scuttle bot around, being careful of its surroundings and other people in the area.

!!! caution
    Ensure that the rover has sufficient space to drive around without hitting anyone or anything.
    Consider possibly holding your robot off the ground so it cannot run away or collide with anything unexpected.

## Configuring the Camera Component

Finally, we will add a camera.
Once again, click <strong>CREATE A COMPONENT</strong> to begin, then continue with the steps, below.

1. Enter "camera" in **Name**.
2. Enter "camera" in **Model**.
3. From **Depends On**, select "local," which is our Raspberry Pi.
4. Click <strong>Create Component</strong>.

The Viam App now displays the config panel for this camera component:
<img src="../img/pi-cam-control.png">

On the Camera Config panel:

1. Enter "camera" in **Name**.
2. Enter "camera" in **Model**.
3. From **Depends On**, select "local".
4. In the JSON, set <code>path_pattern</code> to "video0".

This is the code of your camera attributes if you wish to copy and paste it.

```JSON
{
 "camera_parameters": {
   "width": 0,
   "height": 0,
   "fx": 0,
   "fy": 0,
   "ppx": 0,
   "ppy": 0,
   "distortion": {
     "rk1": 0,
     "rk2": 0,
     "rk3": 0,
     "tp1": 0,
     "tp2": 0
   }
 },
 "source": "",
 "stream": "",
 "width": 0,
 "height": 0,
 "hide": false,
 "debug": false,
 "dump": false,
 "format": "",
 "path": "",
 "path_pattern": "video0"
}
```

If you save the config and click on your WebUI, you will be able to see your camera streaming.

## On Completion
After successfully completing this tutorial, you should have a fully functional Scuttle rover which you can drive around and view the rover's perspective via the Viam App [https://app.viam.com](https://app.viam.com).
Play around with it and try some creative ideas on how you can use the camera with your rover.
If you’d like, you can check out [Color Detection with Scuttle Robot on VIAM](https://docs.google.com/document/d/1FzWl6sJ78BnRsAFCjIBZuLWwzQPs_E99DQ8gI9HMJM0/edit), or create your own camera-related tutorials.
You can also check out our [GPIO Pins for Scuttle Robot](https://docs.google.com/document/d/12QdRVXmHKjnShPkfsBA7QbYGE_NEuAiboov76sHZ7lk/edit) on VIAM or our [Bluetooth Gamepad Tutorial For Scuttle with a Pi](https://docs.google.com/document/d/1jXI_bMYLUtKlrtPHrNMdpdK5NaD031NkBctrwdEA2Gw/edit) to learn more about different configurations possible with the Scuttle rover.

## Referenced Document URLs

  * **Installing Raspian on the Raspberry Pi**: [https://docs.viam.com/getting-started/installation/#installing-raspian-on-the-raspberry-pi](https://docs.viam.com/getting-started/installation/#installing-raspian-on-the-raspberry-pi)

  * **Color Detection with Scuttle Robot on VIAM**: [https://docs.google.com/document/d/1FzWl6sJ78BnRsAFCjIBZuLWwzQPs_E99DQ8gI9HMJM0/edit](https://docs.google.com/document/d/1FzWl6sJ78BnRsAFCjIBZuLWwzQPs_E99DQ8gI9HMJM0/edit)

  * **GPIO Pins for Scuttle Robot**: [https://docs.google.com/document/d/12QdRVXmHKjnShPkfsBA7QbYGE_NEuAiboov76sHZ7lk/edit](https://docs.google.com/document/d/12QdRVXmHKjnShPkfsBA7QbYGE_NEuAiboov76sHZ7lk/edit)

  * **Controlling a Scuttle Robot on VIAM with a Bluetooth Gamepad**: [https://docs.google.com/document/d/1jXI_bMYLUtKlrtPHrNMdpdK5NaD031NkBctrwdEA2Gw/edit](https://docs.google.com/document/d/1jXI_bMYLUtKlrtPHrNMdpdK5NaD031NkBctrwdEA2Gw/edit)
