---
title: "Try Viam: Using Try Viam to Remotely Control A Viam Rover"
linkTitle: "Try Viam Rover Tutorial"
weight: 39
type: "docs"
description: "Instructions for renting and remotely configuring and controlling a Viam Rover located on-site at Viam in NYC."
tags: ["try viam", "app"]
---

_Try Viam_ is a way to try out the Viam platform without setting up any hardware yourself.
You can take over a Viam Rover in our robotics lab for 15 minutes to play around!

This tutorial will guide you through controlling a Viam Rover.
The rental rover is made up of a chassis with a Raspberry Pi 4B single board computer, two motors, encoders, and a camera.
The Try Viam area also has an overhead camera to provide a view of the rental rover, allowing you to view its movements in real time.

## Using the reservation system

### Access the system

While logged in with a Viam account, navigate to <a href="https://app.viam.com/try" target="_blank">TRY in the Viam app</a> to make a reservation.
(If you don’t have an account, it only takes a minute to sign up.)
From the **TRY** page, click **TRY NOW** to reserve a time slot.

### Create a reservation

The Try Viam landing page displays the **Next time slot** or **Estimated Time to Start** and other status information.

If a Viam Rover is available, you can click **TRY NOW** to start your 15 minutes.
Then click **TRY YOUR ROBOT** to access your rental.
Otherwise, you'll see an estimate of the next available start time.
Click **RESERVE ROVER** to get in the queue.
If the wait is longer than four minutes you will receive a “Time to Play” email when it’s your turn.

### Access your Rover Rental

From the confirmation email, click **Take Me to My Rover** to open Try Viam with your Robot in the **CONTROL** tab, or click **TRY NOW** from <a href="https://app.viam.com/try" target="_blank">the TRY page</a>.

Try Viam steps through various screens as the system readies your robot.

After the system establishes a connection and configures your robot, the status capsule displays **RUNNING**, and several buttons:

1. Click **TRY YOUR ROBOT** to access your rental robot page.
2. Click **CANCEL RESERVATION** to immediately end the rental session.
3. Click **EXTEND RESERVATION** to extend the current session if there is time remaining and the next available rental slot is open.

![Screenshot of the Try Viam reservation management page.](../img/try-viam/reservation-management.png)

You can always return to the reservation management page by clicking on the **TRY** tab.
Clicking the timer in the top banner redirects you to the **CONTROL** tab where you can drive the robot.

![Screenshot of the top navigation bar of the Viam app with the Viam Rover time remaining indicator/button.](../img/try-viam/timer.png)

## The **CONTROL** tab

Upon **TRY YOUR ROBOT** you will land on the robot page for the rental rover with the **CONTROL** tab selected.
The header contains the name of the rover, the host, and the IP address.
The rental system randomly generates this information for each rental session:

![Screenshot of the top banner of a Try Viam rover robot page. The randomly generated name for this rover is "solitary-voice".](../img/try-viam/bannerinfo.png)

The **CONTROL** tab contains panels for each component configured on the rover: the base, the left and right motors, the web game pad, the board, and two cameras.
The components are not displayed in any particular order and that order may vary between rovers and rentals.

![Screenshot of the component panels on the CONTROL tab of the Try Viam rover. None of them are expanded yet so they display as thin rectangles with component names and types shown.](../img/try-viam/control-panel-list.png)

### Base Control

Click the `viam_base` rectangle to expand the base control pane, revealing the camera feed and driving interfaces described below.

#### Camera Control (from the base panel)

Selecting a camera allows you to view your Rental Rover as you move it around.
You can choose “cam” for the front-facing camera or “overhead-cam:cam” for an overhead view of your rover.
We recommend enabling both cameras so you can have a better sense of what's happening in the space.

![Screenshot of the viam_base component panel on the CONTROL tab. The Keyboard Disabled toggle is grey and not yet enabled.](../img/try-viam/initial-base-control.png)

![Screenshot of the viam_base component panel with the keyboard enabled (allowing use of the WASD keys to drive the base) and with the "cam" camera feed enabled.](../img/try-viam/enabled-base-control.png)

The camera selection panel looks like this when expanded:

![Screenshot of the camera component panel of the CONTROL tab with the camera named "cam" selected and its feed displayed.](../img/try-viam/camera-expanded.png)

Selecting both cameras stacks the displays:

![Screenshot showing both camera feeds stacked one above the other.](../img/try-viam/two-cams.png)

Each time you show or hide a camera, **Keyboard Enabled** automatically toggles to **Keyboard Disabled**.

{{% alert title="Tip" color="tip" %}}

If you change your camera configurations, don’t forget to re-enable your keyboard control, if necessary.
This automation is for safety purposes.

{{% /alert %}}

#### Movement Control

To move your rover using the Viam app, click on **viam_base** and toggle **Keyboard disabled** to off (grey) to enable.

By default, Viam provides movement control using the **W**, **A**, **S**, and **D** buttons, which correspond to using the **W**, **A**, **S**, and **D** keys on your keyboard to move forward, left, backward, or right, respectively.

You can also use your keyboard’s arrow keys to control the movement.

Note that keyboard control is disabled when the **Keyboard Disabled** switch is greyed out.

##### Discrete Movement Control

If you toggle from **KEYBOARD** to the **DISCRETE** tab, then you’ll see different movement modes: “Straight” and “Spin,” different movement types: “Continuous” and “Discrete,” and directions: “Forwards” and “Backwards.”
In continuous movement mode you can set a speed at which the rover will move indefinitely in the specified direction.
In discrete movement mode you can set a speed at which to move and a distance to cover before stopping.

![Screenshot of the DISCRETE tab of the viam_base component panel. Movement mode, movement type, and direction mode toggles are shown as well as a speed (mm/sec) field and a distance field (the latter of which is greyed out because the movement type toggle is set to continuous instead of discrete movement).](../img/try-viam/discrete.png)

### Camera Control (from the camera panels)

Though the camera streams are accessible from the base component panel, you can also click either of the individual camera component panels in the **CONTROL** tab to view them individually and access more features.
In these panels, you can refresh your camera at a certain frequency (live, refresh every minute, etc.) and you can export screenshots from your camera streams.

**cam Stream**:

![Screenshot of the front-facing camera panel (for the component named "cam").](../img/try-viam/cam-panel.png)

**overhead-cam:cam Stream**:

![Screenshot of the overhead camera panel (for the component named "overhead-cam").](../img/try-viam/overhead-cam-panel.png)

### Motor Control

Some other preconfigured components in your robot config are the motors (which allow you to move the base).
We named these motors “left” and “right” corresponding to their location on the rover base.
Their initial state is **Idle**.
You can click on the each panel and make your motor **RUN** or **STOP**.

![Screenshot of the left and right motor panels on the CONTROL tab.](../img/try-viam/left-right-panels.png)

The left motor running at 45% power would look like this:

![Screenshot of the left motor control panel in Go mode with Direction of Rotation set to Forwards and Power Percent set to 45.](../img/try-viam/45-percent.png)

Both motors running at the same time would look like this:

![Screenshot of the left and right motor control panels. A green "Running" icon is displayed on the upper right of both motor panels, and a "Position" indicator displays non-zero positions for both motors.](../img/try-viam/motors-running.png)

In these panels, you can change the motors’ direction of rotation (which will cause them to go forward or backwards), and their power levels (which will cause them to go faster or slower).
You can also see their current positions (based on encoder readings) in real time.

#### Board Control

You will see a panel for a board component named "local".
The Viam Rover's board is a Raspberry Pi.
The board panel allows the user to get and set the states of individual GPIO pins on the board.

![Screenshot of the board panel in the CONTROL tab, including fields to get and set GPIO pin states.](../img/try-viam/board-panel.png)

#### Web Gamepad Control

Finally, you will see your web gamepad component panel.
This type of input is disabled by default, but if you have a compatible gamepad you'd like to use to drive the rover, you can enable it by toggling the **Enabled** switch.
You can find more information on the [WebGamepad in the Input Controller topic](/components/input-controller/#webgamepad).

**Disabled**:

<img src="/tutorials/img/try-viam/gamepad-disabled.png" alt="Screenshot of the input controller panel in the CONTROL tab with the switch in the controller disabled position." width="50%"><br>

**Enabled**:

<img src="/tutorials/img/try-viam/gamepad-enabled.png" alt="Screenshot of the input controller panel in the CONTROL tab with the switch in the controller enabled position." width="50%"><br>

## Learning about robot configuration

Now that you learned how to drive your rover with the UI, let’s go a bit further.
One other thing you can do within your experience is see your configuration.

On the Viam app, navigate to the **COMPONENTS** subtab, under **CONFIG**.
There you can view each component in the robot and obtain more information about their configuration such as their attributes, component dependencies, pin assignments, etc.:

![Screenshot of the CONFIG tab in Builder mode (as opposed to Raw JSON). The board component panel and right motor panel are visible.](../img/try-viam/config-builder.png)

### Board Configuration

The [board component](/components/board/) represents the Raspberry Pi on the rover.
We named it "local" and configured it with **Type** "board" and **Model** "pi" (the model for Raspberry Pis).

### Encoder Configuration

The encoders on the right and left motors are named, respectively, “Renc” and “Lenc”.
They must be configured before the motors because the motors will depend on the encoders.

![Screenshot of the right encoder config panel with the board attribute set to "local" and the pins struct containing "i" set to "re".](../img/try-viam/right-encoder.png)

![Screenshot of the left encoder config panel.](../img/try-viam/left-encoder.png)

### Motor Configuration

Both motors on this rover are of model "gpio" which is the model for basic DC motors.

The Attributes section lists the board to which the motor is wired, and since our motors are encoded the encoded motor attributes are shown: the encoder name, motor ramp rate limit, encoder ticks per rotation, and max RPM limit.

You can click **Go to Advanced** to view the attributes field in raw JSON format.
The **Attributes** pane contains the current JSON configuration for this component.
Beside it, the **Attribute Guide** contains a complete list of available attributes for this component type.
Click **Go to Fancy** to return to the GUI format.

### Base Configuration

The "left" and "right" attributes represent the motors corresponding to the left and right sides of the rover.
Since we named the motors "left" and "right", the lists of motors for the left and right sides are simply "left", and "right", respectively.
Its type is “base” and its model is “wheeled”.
The "wheel_circumference_mm" is 217.
The "width_mm" is the distance between wheel centerlines, 260mm in this case.
The "spin_slip_factor" of 1.76 is used in steering calculations to account for slippage of the wheels against the ground while turning.

**Attributes**:

* **Right Motors**: right
* **Left Motors**: left
* **Wheel Circumference (mm)**: 217
* **Width**: 260
* **Spin Slip Factor**: 1.76

![Screenshot of the base configuration panel, showing right and left motors, wheel circumference set to 217, width set to 260mm, and spin slip factor set to 1.76.](../img/try-viam/base-config.png)

### Camera Configuration

In the camera component, you will see the **Type** as “camera” and the **Model** as “webcam”.
The **Video Path** is “video0”.

For more information on choosing the correct video path, refer to our [camera configuration tutorial](/tutorials/configure-a-camera/#connect-and-configure-a-webcam).

![Screenshot of the webcam configuration panel. The video path is set to "video0".](../img/try-viam/camera-config.png)

### Gamepad Configuration

The final component is the web gamepad.
The gamepad has a **Type** of “input_controller” and the **Model** is "webgamepad".

![Screenshot of the gamepad configuration panel. No attributes are configured.](../img/try-viam/gamepad-config.png)

If you connect a generic gamepad controller to your computer, you can use it to control your robot.
The gamepad requires a service to function, though.
Fortunately, we added one for you!

Navigate to the **SERVICES** section under the **CONFIG** tab.
The **SERVICES** subtab contains the “Base Remote Control” service which uses three attributes:

**Base Remote Control Attributes**:

* **base**: viam_base
* **control_mode**: joystickControl
* **input_controller**: WebGamepad

The names for **base** and **input_controller** correspond to the naming scheme from the **COMPONENTS** tab.

![Screenshot of the base remote control service named "base_rc" on the Services sub-tab of the CONFIG tab.](../img/try-viam/base-rc.png)

### Raw JSON

So far we've been viewing our rover configuration in 'Builder' mode.
This interface provides a user-friendly, guided experience, but ultimately, Viam robot configuration is output as JSON.
You can view the complete JSON for your rover by clicking on **Raw JSON** at the top left of the **CONFIG** tab.

![Screenshot of the CONFIG tab with the mode toggled to Raw JSON. A section of the full raw JSON config is displayed but one would have to scroll to see all of it.](../img/try-viam/raw-json.png)

To copy the config, click anywhere in the JSON and press **Ctrl+A** and then **Ctrl+C** on Windows or Linux platforms, or **CMD+A** and then **CMD+C** on macOS.

## Extending time

If the Try landing page shows the next time slot is open, you can click **EXTEND RESERVATION** to extend your session at any time before its end.

If you're done using the rental rover and wish to free it up for the next person to use, click **CANCEL RESERVATION**.

When your time is up, if you go back to your Try Viam page ([https://app.viam.com/try](https://app.viam.com/try)), you will see the button say **FINISHED**.
You can click **TRY NOW** to rent the rover again if no one is in the queue.

The system provides an alert when your session is over.

![A screenshot from the Try Viam robot page that reads "Time is up! You can always request to play with the rover again."](../img/try-viam/end-of-session.png)

Your rover rental location now contains your robot with the final configuration from the now ended session.

## Connecting to a Viam Rover with the Viam SDK

You can write your own code to control the Viam robot using Viam's SDKs.
Learn how to use a Viam SDK to make the Viam Rover drive in a square in our [using the Viam SDK to control your Viam Rover tutorial](/tutorials/try-viam-sdk/).

## Next Steps

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, be sure that you head over to the [Viam Community Slack](http://viamrobotics.slack.com).

If you'd like to pre-order your own Viam Rover, you can do so at <a href="https://www.viam.com/resources/rover" target="_blank">this link</a>.
