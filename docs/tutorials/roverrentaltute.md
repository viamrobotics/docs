---
title: "Try Viam: Using Try Viam to Remotely Control A Rover"
linkTitle: "Try Viam Rover Tutorial"
weight: 39
type: "docs"
description: "Instructions for renting and remotely configuring and controlling a Viam Rover located on-site at Viam in NYC."
---

## Introduction

_Try Viam_ is a way to try out the platform without setting up any hardware yourself. You can take over a Viam Rover in our robotics lab for 15 minutes to play around!

This tutorial will guide you through configuring and controlling the Viam Rover that you’ll use in the Rover Rink. The Viam Rover is pre-assembled with a Raspberry Pi microcontroller, two motors, a base, encoders, and a camera. It also has a remote overhead camera to provide a view of your Rental Rover in its Rover Rink, allowing you to view its movements in the rink in real-time.

## Access and use the reservation system

#### Access the system

You must be logged in and have a Viam account to make a reservation. 

If you are not logged in, navigate to [https://app.viam.com/try](https://app.viam.com/try) to access the login dialog. New users can easily create an account from this dialog by providing a valid email address and a password to use with the Viam system.

Once you login to the Viam App, you can click **Try Now** to reserve a time slot.

#### Create a reservation

The Try Viam landing page displays the **Next time slot** or **Estimated Time to Start** and other status information.

If a Viam Rover is available, you'll take over immediately. Otherwise, the Try App displays an estimate of the next available start time and will later send you a “Time to Play” email (below) when it’s your turn. 

The “Time to Play” notification email appears similar to this example:

![alt_text](../img/roverrentaltute/image35.png)<br><br>

#### Access your Rover Rental 

From the confirmation email, click **Rover **to open Try Viam with your Robot in the **CONTROL** tab, or click **TRY NOW** if you were queued and awaiting your Robot to begin your reservation. 

Try Viam steps through various screens as the system readies your robot:

Initial display (available now)<br>

![alt_text](../img/roverrentaltute/image2.png)<br><br>

Display when a time slot isn’t immediately available

![alt_text](../img/roverrentaltute/image23.png)<br><br>

Your reservation is in the queue <br><br>

![alt_text](../img/roverrentaltute/image2.png)<br><br>

Viam has begun preparing your rover <br><br>

![alt_text](../img/roverrentaltute/image15.png)<br><br>

Almost ready <br><br>

![alt_text](../img/roverrentaltute/image20.png)<br><br>

Scrolling on the **SETTING UP ROBOT** “status capsule” displays a popup announcing that the wait time could take 30 seconds.

![alt_text](../img/roverrentaltute/image16.png)<br><br>

After the system establishes a connection and configures your robot, the status capsule displays **RUNNING**, and new buttons: 

1. Click **TRY YOUR ROBOT** to open your robot in a new Try Viam tab.
2. Click **CANCEL RESERVATION** to immediately end the rental session.
3. Click **EXTEND RESERVATION** to extend the current session if there is time remaining and the next available rental slot in this Rover Rink is open.

![alt_text](../img/roverrentaltute/image27.png)<br><br>

You can always return to the generic rental page by clicking on the **TRY** tab.  Clicking the timer in the top banner redirects you to the specific robot control page for _this_ session. 

![alt_text](../img/roverrentaltute/image12.png)<br><br>

## The CONTROL tab

Viam first displays your robot page and the **CONTROL** **panel. The header contains the name of the rover (“solitary-host”), the host (octagon-rover-1), and trhe remote address (10.1.7.141). Viam randomly generates this information for each rental session: 

![alt_text](../img/roverrentaltute/bannerinfo.png)<br><br>

On the** **CONTROL** **tab, you find the base, the left and right motors, the web game pad, the board, and two cameras. The components are not displayed in any order and that order may vary between rovers and rentals. 

![alt_text](../img/roverrentaltute/image28.png)<br><br>

### Component Controls in the UI

#### Movement Control

To move your rover using the interface, click on **viam_base** and toggle **Keyboard disabled** to off (grey). 

By default, Viam provides movement control using the **W**, **A**, **S**, and **D** buttons, which correspond to using the **W**, **A**, **S**, and **D**  keys on the keyboard to move forward, backward, arc, or spin, respectively. 

You can also use the keyboard’s arrow keys to control the movement if desired. 

Note that keyboard control is only enabled when the **Keyboard Disabled** switch is greyed-out.

#### Camera Control

Selecting a camera allows you to view your Rental Rover as you move it around. You can choose “cam” for the front-facing camera or “overhead-cam:cam” for an overhead view of your Rover.

![alt_text](../img/roverrentaltute/image10.png)<br><br>

![alt_text](../img/roverrentaltute/image5.png)<br><br>

The camera selection panel looks like this when expanded:

![alt_text](../img/roverrentaltute/image25.png)<br><br>


Selecting both cams stacks the displays:<br><br>


![alt_text](../img/roverrentaltute/image9.png)<br><br>


Each time you show or hide a camera,  **Keyboard Enabled** automatically toggles to **Keyboard Disabled**.

{{% alert title="Tip" color="tip" %}}

If you change your camera configurations, don’t forget to re-enable your keyboard control, if necessary. This automation is for safety purposes. 

{{% /alert %}}


#### Base Control

If you toggle to **DISCRETE** **tab, then you’ll see different movement modes such as “Straight” and “Spin”; and different movement types such as “Continuous” and “Discrete” and directions such as “Forwards” and “Backwards.” You will also be able to tinker with speed. 

![alt_text](../img/roverrentaltute/image29.png)<br><br>


## Changing the Camera Configuration

Click a camera configuration panel to view its individual configuration. Click to expand, and toggle **Show Camera**. In these panels, you can refresh your camera at a certain frequency (always live, refresh every minute, etc.) and you export screenshots from your camera streams. 

**cam Stream**:

![alt_text](../img/roverrentaltute/image21.png)

**overhead-cam:cam Stream**:

![alt_text](../img/roverrentaltute/image18.png)

### Changing the Motor Configuration 

Some other preconfigured components in your robot config are the motors (which allow you to move the base). We named these motors “left” and “right” corresponding to their location on the rover base. Their initial state is **Idle**.** You can click on the each panel and make your motor **RUN** **or **STOP**.  **

![alt_text](../img/roverrentaltute/image6.png)<br><br>


A running left motor state would look like this: <br><br>


![alt_text](../img/roverrentaltute/image24.png)
<br><br>

Both motors running at the same time would look like this:<br><br>


![alt_text](../img/roverrentaltute/image7.png)<br><br>

In these panels, you can change the motors’ direction of rotation (which will allow them to go forward or backwards), and their power levels (which will allow them to go faster or slower). You can also see their current positions in real time. 


#### Board Control

The remaining pre-configured component in your robot config is the board. The Viam Rover uses the Raspberry Pi. 

![alt_text](../img/roverrentaltute/image11.png)


#### WebGamepad Control

Finally, you will see your web gamepad. It is default to disabled, but you can enable it by toggling the button. 

  

Disabled:<br><br>

![alt_text](../img/roverrentaltute/image26.png)<br><br>

Enabled:<br><br>

![alt_text](../img/roverrentaltute/image8.png)<br><br>

## Learning about robot configuration

Now that you learned how to drive your rover with the UI, let’s go a bit further. One other thing you can do within your experience is see your configuration. 

On the Viam App, navigate to the **COMPONENTS** section, under **CONFIG**. There you can view each component in the robot and obtain more information about their configuration such as their attributes, board/component dependencies, pin assignments, etc.:

![alt_text](../img/roverrentaltute/image26.png)

### Motor Configuration

The Motor panel also provides attributes, board/component dependencies, pin assignments, etc., 

The Attributes section lists the Motor model (which is “gpio” for both motors), whether the motor is encoded, the **Encoder** name,  its **Ticks Per Rotation**, **Ramp Rate Rpm Per Sec**, **Tick Per Rotation**, and **Max RPM**. 

#### Right Motor

In your config, the right motor will appear similar to this:

![alt_text](../img/roverrentaltute/image30.png)

**Attributes**:

* **Board**: local (i.e., the name of the Raspberry Pi)
* **Encoder** type: Encoded
* **Encoder** name: Renc
* **Ticks per Rotation**: 996
* **Ramp Rate Rpm Per Sec**: No assignment

**Component Pin Assignments**:

* **Type**: In1/In2
* **Enable Pins**: Neither
* **A/In1**: 16 GPIO 23
* **B/In2**: 18 GPIO 24
* **PWM**:  22 GPIO 25. 

**Data Capture Configuration**: No assignment

**Frame**: No assignment

**Depends On**: local (i.e., the Raspberry Pi SBC), and the Renc (i.e., the Right Encoder)

You can click **go to Advanced** to toggle to the full configuration for this component. The **Attributes** pane contains the current JSON configuration for this component. Beside it, the **Attribute Guide** contains a complete list of valid, available attributes for this component. 


#### Left Motor

The left motor component appears almost identical to the right motor, the differences being pin assignments and **Encoder** name: 

![alt_text](../img/roverrentaltute/image19.png)

**Attributes**:

* **Board**: local (i.e., the name of the Raspberry Pi)
* **Encoder** type: Encoded
* **Encoder** name: Lenc
* **Ticks per Rotation**: 996
* **Ramp Rate Rpm Per Sec**: No assignment

**Component Pin Assignments**:

* **Type**: In1/In2
* **Enable Pins**: Neither
* **A/In1**: 11 GPIO 17
* **B/In2**: 13 GPIO 27
* **PWM**:  15 GPIO 22. 

**Data Capture Configuration**: No assignment

**Frame**: No assignment

**Depends On**: local (i.e., the Raspberry Pi SBC), and the Renc (i.e., the Right Encoder)

As with the right motor, you can click **go to Advanced** to toggle to the full configuration for this component. The **Attributes** pane contains the current JSON configuration for this component. Beside it, the **Attribute Guide** contains a complete list of valid, available attributes for this component. 

### Base Configuration

Its type is “base” and its model is “wheeled”. The “wheel_circumference_mm” is 217. The “width_mm” is distance between wheel centerlines, 260mm in this case. The Left and right attributes represent the motors corresponding to the left and right sides of the rover. Since the motors are “left” and “right”, simply add “left” and “right”, respectively, between the brackets for the set of motors.

**Attributes**:

* **Right Motors**: right
* **Left Motors**: left
* **Wheel Circumference (mm)**: 217
* **Width**: 260
* **Depends On**: left, right, local

![alt_text](../img/roverrentaltute/image36.png)

### Camera Configuration

In the camera component, you will see the **type **as “camera” and the **model **“webcam”. The **Video Path **is  “video0”.

To learn more, refer to our [camera configuration tutorial](https://docs.viam.com/tutorials/configure-a-camera/#connect-and-configure-a-webcam) for more information on choosing the correct video path.

![alt_text](../img/roverrentaltute/image33.png)

### Encoder Configuration

The encoders are named, respectively, “Renc” and “Lenc”. They will depend on “local” which is our board, the Raspberry Pi SBC.

![alt_text](../img/roverrentaltute/image1.png)

![alt_text](../img/roverrentaltute/image4.png)

### Gamepad Configuration

The final component is the web gamepad. The gamepad is **type **is “input_controller” and the **model **is a webgamepad. 

If you connect a generic gamepad controller to your computer, you can use it to control your robot in the rover rink. The gamepad requires a service to function, though. Fortunately, we added one for you! 

![alt_text](../img/roverrentaltute/image14.png)

Navigate to the **SERVICES** section under the **CONFIG** tab. The **SERVICES** contains the “Base Remote Control” service which uses three attributes:

**Base Remote Control Attributes**:

* **base**: viam_base
* **control_mode**: joystickControl
* **input_controller**: WebGamepad

The names for **base** and **input_controller** correspond to the naming scheme from the **COMPONENTS** tab. 

![alt_text](../img/roverrentaltute/image3.png)

Now that you have learned about components and services, one more thing to try is, viewing the code that Viam generate for the rover as you added those components and services. 

On the **CONFIG** tab, toggle **Mode** from **Builder** to **RAW JSON**. The full configuration is displayed. Click anywhere in the JSON and press **CTRL+A** on Windows or Linux platforms, or **CMD+A** on macOS to copy the configuration.

![alt_text](../img/roverrentaltute/image13.png)

## Extending time!

If the Try Landing page shows the next time slot is open, you can click **EXTEND RESERVATION** to extend your session at any time before its end.

When you are done with your time, if you go back to your Try Viam page ([https://app.viam.com/try](https://app.viam.com/try)), you will see the button say **FINISHED**. **You can click **TRY NOW** **to rent the rover again if no one is in the queue. 

The system provides an alert when your session is over. 

![alt_text](../img/roverrentaltute/image12.png)

Your Rover Rental Location now contains your robot with the final configuration from the now ended session.

## Connecting to a Viam rover with the Viam SDK

You can write your own code to control the Viam robot. Before you get started, you will need to install an SDK locally. 

### How to install a Viam SDK

In this step, you are going to install either the [Viam Python SDK](https://python.viam.dev/) (Software Development Kit) or the [Viam Golang SDK](https://pkg.go.dev/go.viam.com/rdk). Use which ever programming language you are most comfortable with.

{{% alert title="Note" color="note" %}}
Refer to the appropriate SDK documentation for SDK installation instructions.
{{% /alert %}}

