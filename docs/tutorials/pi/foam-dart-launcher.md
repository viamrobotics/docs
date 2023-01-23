---
title: "Foam Dart Launcher Robot Tutorial"
linkTitle: "Dart Launcher Robot"
weight: 160
type: "docs"
description: "Use Viam to configure a rover and launch a foam dart activated by GPIO pins on a Raspberry Pi."
tags: ["base", "motor", "camera", "raspberry pi"]
# SME: Kurt S. and Hazal M.
---

## Introduction

This tutorial will show you how to build your very own foam dart launcher robot using Viam, a Raspberry Pi, a generic foam dart launcher with foam darts, a USB camera, a solenoid, a relay, and a motor controller.
This robot will be able to move around and launch foam darts.

This project is a great place to start if you are new to building robots, have a love for Nerf toys, an occasion to target something and launch a dart at it, or if you just want to troll your friends.
Don’t forget to be careful and have fun!

{{< figure src="../../img/foam-dart-launcher/init-image-nerf-robot.gif" width="400px" alt="Robot launching a dart from a foam dart launcher taped to the robot." title="Robot launching a dart from a foam dart launcher taped to the robot." >}}

## What You’ll Need for This Tutorial

You will need the following hardware, software, tools, and consumables to complete this project:

{{% alert title="Note" color="note"%}}
If you use a different rover and/or motor controller, ensure that the motor driver is compatible with the motors on your rover.
For example, a brushed DC motor requires a brushed DC motor driver that is rated for the power requirements of the motor.
Also, the configuration files shown in this tutorial *must* be modified if you use a different setup.

You can find more information on configuring different motors in the [Motor Component](/components/motor) topic.
{{% /alert %}}

### Hardware and software requirements

* [Raspberry Pi with microSD card](https://a.co/d/bxEdcAT)[^rpi], with viam-server installed per [our Raspberry Pi setup guide](/installation/prepare/).
* [A wheeled rover](https://www.amazon.com/Smart-Chassis-Motors-Encoder-Battery/dp/B01LXY7CM3/)[^wrvr]
* [A foam dart launcher](https://www.amazon.com/Nerf-N-Strike-Elite-Jolt-Blaster/dp/B01HEQHXE8)[^ng]
* [A USB camera (webcam)](https://www.amazon.com/gp/product/B0972KK7BC/)[^cam] (optional, to see where you are going and aiming)
* [A solenoid](https://www.amazon.com/0530-Frame-Solenoid-Electromagnet-Stroke/dp/B07K35L4TH/)[^sol]
* [A relay](https://www.amazon.com/HiLetgo-Channel-Isolation-Support-Trigger/dp/B00LW15D1M/)[^relay]
* [A dual motor controller](https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6/)[^dmc].
If you use a different motor driver, refer to the manufacturer’s data sheet and our [motor component topic](/components/motor) to learn how to configure the pins.
* Jumper wires (breadboard wires)

[^rpi]: A Raspberry Pi 4 microSD card: <a href="https://a.co/d/bxEdcAT/">ht<span></span>tps://a.co/d/bxEdcAT/
[^wrvr]: A wheeled rover: <a href="https://www.amazon.com/Smart-Chassis-Motors-Encoder-Battery/dp/B01LXY7CM3/" target="_blank">ht<span></span>tps://www.amazon.com/Smart-Chassis-Motors-Encoder-Battery/dp/B01LXY7CM3/</a>
[^ng]: Foam dart launcher: <a href="https://www.amazon.com/Nerf-N-Strike-Elite-Jolt-Blaster/dp/B01HEQHXE8/" target="_blank">ht<span></span>tps://www.amazon.com/Nerf-N-Strike-Elite-Jolt-Blaster/dp/B01HEQHXE8/</a>
[^cam]: Webcam: <a href="https://www.amazon.com/gp/product/B0972KK7BC/" target="_blank">ht<span></span>tps://www.amazon.com/gp/product/B0972KK7BC/</a>
[^sol]: Solenoid: <a href="https://www.amazon.com/0530-Frame-Solenoid-Electromagnet-Stroke/dp/B07K35L4TH/" target="_blank">ht<span></span>tps://www.amazon.com/0530-Frame-Solenoid-Electromagnet-Stroke/dp/B07K35L4TH/</a>
[^relay]: Relay: <a href="https://www.amazon.com/HiLetgo-Channel-Isolation-Support-Trigger/dp/B00LW15D1M/" target="_blank">ht<span></span>tps://www.amazon.com/HiLetgo-Channel-Isolation-Support-Trigger/dp/B00LW15D1M/</a>
[^dmc]: Dual H-bridge Motor Controller: <a href="https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6/" target="_blank">ht<span></span>tps://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6/</a>

### Tools and Consumables

* Solder (optional)
* Small flathead screwdriver
* Cutting pliers (flush-cutting pliers preferred)
* Electrical tape
* Elastic/rubber bands

## How to Assemble Your Hardware

### Motor Controller Setup

A motor controller is a piece of hardware that takes digital signals from the Raspberry Pi and sends power to the motors accordingly.
For this setup we have one dual motor controller for the two motors.

{{% alert title="Note" color="note"%}}
If you have more than two motors you will likely need two motor controllers.
{{% /alert %}}

{{< figure src="../../img/foam-dart-launcher/dual-h-bridge-motor-controller.jpg" width="400px" alt="Dual H-bridge motor controller with four signal wires going in and two sets of motor power wires coming out." title="Dual H-bridge motor controller." >}}

We need only worry about <strong>OUT1</strong> through <strong>OUT4</strong>, <strong>IN1</strong> through <strong>IN4</strong>, 12V, and ground.

<ol>
<li>Attach left to the motor controller.
<ol type="a">
    <li>Use a small flathead screwdriver to loosen the <strong>Out1</strong> and <strong>OUT2</strong> screw terminals.
<li>Place the red motor wire into <strong>OUT1</strong>
<li>Place the black motor wire into <strong>OUT2</strong>
<li>Use the flathead screwdriver to tighten the terminals to firmly hold the wires in place.
<strong>Note</strong>: Tightly twisting each stripped wire end and then tinning it makes it easier to insert and secure the jumper in screw terminal connectors.
   </ol>
<li>Connect the control wires <strong>IN1</strong> and <strong>IN2</strong> to your Raspberry Pi.
<ol type="a">
<li>The example robot has <strong>IN1</strong> -> pin 11, <strong>IN2</strong> -> pin 13
       </ol>
<li>Repeat steps 1-2 for the right motor using <strong>OUT3</strong>, <strong>OUT4</strong>, <strong>IN3</strong>, <strong>IN4</strong>
<ol type="a">
<li>The example robot has <strong>IN3</strong> -> pin 16, <strong>IN4</strong> -> pin 18
   </ol>
<li>Connect the external power that will supply power to the motors.
<ol type="a">
    <li>In the example we have 4 AA batteries connected to the motor driver giving us 6V of power for the motors.
</ol>
</ol>

### Camera Setup

This is as easy as plugging the camera into a USB slot on your Pi.
We’ll configure the camera in the Viam app in later steps.

### Relay/Solenoid Setup

The solenoid component actuates the foam dart launcher trigger.
The relay works as a switch to turn on and off the solenoid.
This allows us to activate the foam dart launcher via a GPIO pin on the board.

{{% alert title="Note" color="note"%}}
We cannot directly power these components from GPIO pins, since there board limitation which restricts GPIO pins to providing 3.3V and a very limited current supply (16mA).
This board limitation restricts GPIO pins to providing 3.3V and a very limited current supply (16mA).
Even the 3V and 5.5V power pins on the Pi supply are limited to about 1A.

If a component attempts to pull more current than that, you risk power cycling the Pi.
That is why we use a relay to supply 5VDC with a higher current to actuate the solenoid.
This is standard practice for power control circuits in many situations.
For example, by using a common off-the-shelf (COTS) 15A light switch to actuate a relay bank, it is possible to control hundreds of amps of lighting for an entire office floor.
{{% /alert %}}

{{< figure src="../../img/foam-dart-launcher/power-relay.jpg" width="400px" alt="Power relay." title="Power relay." >}}

<ol>
<li>Connect the solenoid to the relay.</li>
<ol type="a">
    <li>Connect a wire to the Normally Open (<strong>NO</strong>) terminal connector.</li>
    <li>Connect the other end to a ground pin on the Raspberry Pi. </li>
    </ol>
<li>Connect the Relay <strong>COM</strong>mon pin.</li>
<ol type="a">
<li>Connect the <strong>COM</strong> pin to the 3.3V power of the Raspberry Pi. </li>
</ol>
<li>Connect <strong>VCC</strong> (<strong>DC+</strong>) and ground (<strong>DC-</strong>) .</li>
<ol type="a">
<li>Connect <strong>DC+</strong> to the 5V of the Raspberry Pi.</li>
<li>Connect <strong>DC-</strong> to ground on the Raspberry Pi. </li>
</ol>
<li>Connect <strong>IN</strong>. </li>
<ol type="a">
<li>Connect <strong>IN</strong> to a GPIO pin on the Raspberry Pi. </li>
<li>For this example, we've connected to pin 37.</li>
</ol>
</ol>

### Assemble Solenoid/Foam Dart Launcher

{{< figure src="../../img/foam-dart-launcher/assembled-foam-dart-launcher.jpg" width="400px" alt="Solenoid attached to the orange foam dart launcher using rubber bands and electrical tape." title="Foam dart launcher/Solenoid Assembly." >}}

1. Modify the foam dart launcher to make room for the solenoid.
   Using cutting pliers, we cut the trigger guard off of the front as seen in the picture above.
2. Test that the solenoid has enough power to press the trigger when the foam dart launcher is loaded.
3. If the solenoid is not strong enough we can:
    * Wrap the trigger with rubber bands to make the trigger easier to activate[^rb].
    * Increase the voltage to the solenoid.
  Right now it receives 5 volts, but some solenoids can support up to 12 volts.
  If necessary, you can connect the solenoid to another power supply such as a 9 volt battery.
  Check the details of your solenoid[^solvolt].
4. Tape the solenoid in such a manner that it makes good contact with the trigger when activated via the relay.
5. Attach all of your components to the base.

[^rb]: If you use the rubber band method, you may need to pull the rubber bands away from the trigger when reloading the foam dart launcher so it can reset and load properly.
Try activating the solenoid manually to ensure that it hits the foam dart launcher trigger in the right spot.
[^solvolt]:  If you choose to increase the voltage, you must connect **VCC** and ground (**DC+** and **DC-**) to the new voltage source rather than connecting them to the Raspberry Pi as described in Step 3 of [Assemble Solenoid/Foam Dart Launcher](#assemble-solenoidfoam-dart-launcher).

{{< figure src="../../img/foam-dart-launcher/ng-taped-to-rover.jpg"  alt="Foam dart launcher taped to a rover base using electrical tape." title="Foam dart launcher Taped to the Rover" width="400">}}

## Configure Your Foam Dart Launcher Robot with the Viam App

Create a new robot in the Viam app and give it a name.

### Pi Configuration (board)

Add your board with the name `board`, type `board`, and model `pi`.
Click **Create Component**.

{{< figure src="../../img/foam-dart-launcher/add-board.png"  alt="Viam App Board component attribute pane." title="Board Component Attribute Pane" width="800" >}}

You can name your board whatever you want, we picked `board` for simplicity.
Just remember to use that name consistently in the following steps.

### Motors Configuration (Left and Right)

Add the left [motor](/components/motor/) with the name `left`, type `motor`, and model `gpio`, then add the right motor with the name `right`, type `motor` and model `gpio`.
After clicking **Create Component** you’ll see the **Component Pin Assignment** toggle.
Select **In1/In2** since that is compatible with the input type our motor controller expects.
In the **A/In1** and **B/In2** drop-downs, choose `11 GPIO 17` and `13 GPIO 27`, respectively, for the left motor, and `16 GPIO 23` and `18 GPIO 24`, respectively, for the right motor.

Select the name of the board the motor controller is wired to (“board”) from the **Board** drop-down.

<table>
<tr><td style="background:white; border-right: 1px solid black; padding-right: 25px">
{{< figure src="../../img/foam-dart-launcher/left-motor.png"  alt="Motor Component Attribute Pane (left motor)." title="Left Motor Component Configuration Pane" width="400">}}  
</td><td style="background:white;">
{{< figure src="../../img/foam-dart-launcher/right-motor.png"  alt="Motor Component Attribute Pane (right motor)." title="Right Motor Component Configuration Pane" width="400">}}
</td></tr></table>

Click **SAVE CONFIG** at the bottom of the screen.
Then go to the **CONTROL** tab where you will now see the buttons you can use to control the motors:

{{< figure src="../../img/foam-dart-launcher/LR-motor-config-panes.png"  alt="Left and right motor configuration panes." title="Left and Right Motor Configuration Panes" width="800">}}

Now, you can move around your wheels separately.
Let’s add a base to be able to control them together.

### Base Configuration

Add your motors to the [base](/components/base/) so you can move them around with your keyboard.

Here we must specify the wheel circumference and the width between the wheels (measured centerline to centerline).
Depending on your rover, you can change these numbers.
Don’t forget to make the base depend on the `left`, `right`, and the `board` components.

{{< figure src="../../img/foam-dart-launcher/config-base.png"  alt="Base Component Attribute Pane." title="Base Component Attribute Pane" width="800">}}

Now let’s add a camera to watch the video stream on the control panel as you move your rover.

### Camera configuration

Add your USB camera as a webcam. Please refer to [How to Configure a Camera > Connect and Configure a Camera](/components/camera/configure-a-camera/#connect-and-configure-a-webcam) for complete instructions.

{{< figure src="../../img/foam-dart-launcher/config-webcam.png"  alt="Camera Component Attribute Pane." title="Camera Component Attribute Pane" width="800" >}}

If you go back to the **CONTROL** tab, you will see your base and camera.

{{< figure src="../../img/foam-dart-launcher/base-cam-view.png"  alt="Camera view from the Base component's keyboard tab." title="Camera View from the Base Component's Keyboard Tab." width="800">}}

Toggle the switch under **Keyboard Disabled** to enable keyboard control, then use the W, A, S, and D keys on your keyboard to move your rover around.
You can view the camera stream at the same time.
If you scroll down, you will see your camera as a component. From the camera component pane, you can change the camera's refresh frequency and also export screenshots from your camera.

{{< figure src="../../img/foam-dart-launcher/camera-cam-view.png"  alt="Camera view from the Camera component pane." title="Camera View from the Camera Component Pane." width="800">}}

## Toggling GPIO Pin States

The board card in the **CONTROL** tab provides a way to change the state of the pin connected to the solenoid.
If you click the board component, you will be able to see your GPIO pin and its current state.
In the **Set** part of the GPIO section, select pin 37 (the pin we wired to control the solenoid).
If you set the pin state to high, the solenoid will actuate.
If you set it to low, it should deactivate the solenoid.
Since we already assembled the robot, setting pin 37 to high launches your foam dart launcher if its loaded.

{{< figure src="../../img/foam-dart-launcher/board-low.png"  alt="Board component, G P I O section showing Low selected on the Pin State drop-down." title="Board component, GPIO section showing Low selected on the Pin State drop-down" width="800">}}

{{< figure src="../../img/foam-dart-launcher/board-displaying-high.png"  alt="Board component, G P I O section with pin 37 set to High." title="Board component, GPIO section with pin 37 set to High." width="800">}}

{{< figure src="../../img/foam-dart-launcher/board-high.png"  alt="Board component, G P I O section showing High selected on the Pin State drop-down." title="Board component, GPIO section showing High selected on the Pin State drop-down" width="800">}}

## Debug Information

If any component fails to appear when connecting to the robot in the Viam app, check the **LOGS** tab for potential errors.

## Final Code

The raw JSON for the entire configuration can be found here if you wish to copy it into your config: [https://gist.github.com/mestcihazal/7683fbdd0975579b44295b3208757b5a](https://gist.github.com/mestcihazal/7683fbdd0975579b44295b3208757b5a)

## Control via the Viam App

### Controlling the Base

1. Navigate to Viam app -> base component
2. Enable keyboard controls
3. Drive your robot around!

### Activating the Foam Dart Launcher

1. Make sure your foam dart launcher is loaded and ready to go.
2. When you are ready, navigate to the Viam app -> **CONTROL** tab -> board component and set the **IN** pin (pin 37 in our example) to high to activate.

You can see the demo video of it in action here:

{{< video src="../../videos/FoamDartLauncherRobotDemo.mp4" type="video/mp4">}}

## Summary

In this tutorial, you learned how to create a remotely-controlled foam dart launching robot activated by the GPIO pins on a Raspberry Pi using Viam.
You could use this same concept as the basis for a security robot that launches darts at people if they enter your room, a Nerf ball blaster dog toy, a kitten treat shooter for cats to fetch in excitement, you name it!
You could even add [object detection and machine learning](/services/vision/) and activate the launcher only when the camera sees a specific object or person.

If you are looking for projects that would be a great next step in your journey of robots creation, we recommend that you check out the following tutorials:

* [Tutorial List](/tutorials)

If you have any issues getting Viam set up or get stuck, let us know on the [Viam Community Slack](http://viamrobotics.slack.com) and we'll be happy to help you get up and running.
The Viam Community Slack is also a great place to connect with other developers learning how to build robots.
