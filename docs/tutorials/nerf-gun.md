---
title: "Nerf Gun Robot Tutorial"
linkTitle: "Nerf Gun Robot"
weight: 160
type: "docs"
description: "Use Viam to configure a rover and to shoot a nerf gun activated by GPIO pins on a Raspberry Pi."
# SME: Kurt S. and Hazal M.
---

**Introduction**

This tutorial will show you how to build your very own Nerf gun robot using Viam, a Raspberry Pi, a generic Nerf gun with foam darts, a USB camera, a solenoid, a relay, and a motor controller. 
This robot will be able to move around, and shoot a Nerf dart at people and objects.

This project is a great place to start if you are new to building robots, have a love for Nerf guns, and an occasion to target something and shoot it while you troll your friends. 
Don’t forget to be careful and have fun! 

{{< figure src="../img/nerf-robot/init-image-nerf-robot.gif" width="400px" alt="Firing a Nerf gun taped to a rover having batteries and cables exposed." title="Nerf Robot firing a dart from a Nerf gun taped to a robot." >}}

## What you’ll need for this tutorial:

You will need the following hardware, software, tools, and materials to complete this project:

{{% alert="Note" color="note"%}} If you use a different rover and/or motor controller, ensure that the motor driver is compatible with the motors on your rover. 
For example, a brushed DC motor requires a brushed DC motor driver that is rated for the power requirements of the motor. 
Also, the configuration files shown in this tutorial *must* be modified if you use a different setup.
{{% /alert %}}

**Hardware and Software Requirements:**

* [Raspberry Pi with microSD card](https://a.co/d/bxEdcAT), with [viam-server](https://github.com/viamrobotics/rdk/tree/0c550c246739b87b4d5a9e8d96d2b6fdb3948e2b) installed according to: ["Installing Viam on Linux Systems"](https://docs.viam.com/getting-started/linux-install/).
* [A wheeled rover](https://www.amazon.com/Smart-Chassis-Motors-Encoder-Battery/dp/B01LXY7CM3/)[^wrvr]
* [A Nerf gun](https://www.amazon.com/Nerf-N-Strike-Elite-Jolt-Blaster/dp/B01HEQHXE8)[^ng]
* [A USB camera](https://www.amazon.com/gp/product/B0972KK7BC/)[^cam] (optional, to see where you are going and aiming)
* [A solenoid](https://www.amazon.com/0530-Frame-Solenoid-Electromagnet-Stroke/dp/B07K35L4TH/)[^sol]
* [A relay](https://www.amazon.com/HiLetgo-Channel-Isolation-Support-Trigger/dp/B00LW15D1M/)[^relay]
* [A dual motor controller](https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6/)[^dmc]. If you use a different motor controller, you may need to configure it differently from what is shown in this tutorial. Refer to the manufacturer’s data sheet and our [motor component documentation](https://docs.viam.com/components/motor) to see how to configure the pins.
* Jumper wires (breadboard wires)
[^wrvr]: A wheeled rover: <a href="https://www.amazon.com/Smart-Chassis-Motors-Encoder-Battery/dp/B01LXY7CM3/" target="_blank">ht<span></span>tps://www.amazon.com/Smart-Chassis-Motors-Encoder-Battery/dp/B01LXY7CM3/</a>
[^ng]: Nerf Gun: <a href="https://www.amazon.com/Nerf-N-Strike-Elite-Jolt-Blaster/dp/B01HEQHXE8/" target="_blank">ht<span></span>tps://www.amazon.com/Nerf-N-Strike-Elite-Jolt-Blaster/dp/B01HEQHXE8/</a>
[^cam]: Webcam: <a href="https://www.amazon.com/gp/product/B0972KK7BC/" target="_blank">ht<span></span>tps://www.amazon.com/gp/product/B0972KK7BC/</a>
[^sol]: Solenoid: <a href="https://www.amazon.com/0530-Frame-Solenoid-Electromagnet-Stroke/dp/B07K35L4TH/" target="_blank">ht<span></span>tps://www.amazon.com/0530-Frame-Solenoid-Electromagnet-Stroke/dp/B07K35L4TH/</a>
[^relay]: Relay: <a href="https://www.amazon.com/HiLetgo-Channel-Isolation-Support-Trigger/dp/B00LW15D1M/" target="_blank">ht<span></span>tps://www.amazon.com/HiLetgo-Channel-Isolation-Support-Trigger/dp/B00LW15D1M/</a>
[^dmc]:Dual H-bridge Moror Controller: <a href="https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6/" target="_blank">ht<span></span>tps://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6/</a>

**Other Materials:**

* Solder (optional)
* [Flathead screwdriver](https://www.amazon.com/Precision-Screwdriver-Flathead-Philips-Different/dp/B01N5W8MA3/)[^sd]
* [Cutting pliers](https://www.amazon.com/IGAN-P6-Precision-Clippers-Spring-loaded-Handmade/dp/B087P191LP/)[^pliers]
* Electrical Tape
* Elastic bands/Rubber Bands

[^sd]:Flathead screwdriver: <a href="https://www.amazon.com/Precision-Screwdriver-Flathead-Philips-Different/dp/B01N5W8MA3/" target="_blank">ht<span></span>tps://www.amazon.com/Precision-Screwdriver-Flathead-Philips-Different/dp/B01N5W8MA3/</a>
[^pliers]: 6-inch, flush cut, side-cutting pliers <a href="https://www.amazon.com/IGAN-P6-Precision-Clippers-Spring-loaded-Handmade/dp/B087P191LP/">ht<span></span>tps://www.amazon.com/IGAN-P6-Precision-Clippers-Spring-loaded-Handmade/dp/B087P191LP/</a>>

### How to Assemble Your Hardware

Hardware configuration includes how to attach your hardware to the Raspberry Pi.

#### Motor Controller Setup

The motor controller is a piece of hardware that takes digital signals from the Raspberry Pi and sends power to the motors accordingly. 
For this setup we just have one motor controller for the two motors.

{{% alert="Note" color="note"%}}
If you have more than two motors you will likely need two motor controllers. 
{{% /alert %}}

{{< figure src="../img/nerf-robot/dual-h-bridge-motor-controller.jpg" width="400px" alt="Dual H-bridge motor controller with four signal wires going in and two sets of motor power wires coming out." title="Dual H-bridge motor controller." >}}

We need only worry about <strong>Out1-4</strong>, <strong>In1-4</strong>, 12V, and ground

<ol>
<li>Attach left to the motor controller.
<ol type="a">
    <li>Use a small flathead screwdriver to loosen the screw terminals for <strong>Out1</strong> and <strong>Out2</strong>
<li>Place the red motor wire into <strong>Out1</strong>
<li>Place the black motor wire into <strong>Out2</strong>
<li>Use the flathead screwdriver to tighten the terminals to firmly hold the wires in place.
<strong>Note</strong>: Twisting the stripped wire ends and then tinning them makes it easier to insert and secure them in screw terminal connectors.
   </ol>
<li>Connect the control wires <strong>In1</strong> and <strong>In2</strong> to your Raspberry Pi.
<ol type="a">
<li>The example robot has <strong>In1</strong> -> pin 11, <strong>In2</strong> -> pin 13
       </ol>
<li>Repeat steps 1-2 for the right motor and using <strong>Out3</strong>, <strong>Out4</strong>, <strong>In3</strong>, <strong>In4</strong>
<ol type="a">
<li>The example robot has <strong>In3</strong> -> pin 16, <strong>In4</strong> -> pin 18
   </ol>
<li>Connect the external power that will supply power to the motors.
<ol type="a">
    <li>In the example we have 4 AA batteries connected to the motor driver giving us 6V of power for the motors.
</ol>
</ol>

#### Camera Setup

This is as easy as plugging the camera into a USB slot. 
We’ll configure the camera in the Viam App in later steps. 

#### Relay/Solenoid Setup

The solenoid is used to actuate the Nerf gun trigger. 
The relay works as a switch to turn on and off our solenoid. 
This allows us to activate the Nerf gun by using a GPIO pin on the board.

{{% alert="Note" color="note"%}}
We cannot directly power components from GPIO pins. 
This board limitation restricts GPIO pins to providing 3.3V and a very limited current supply (16mA). 
Even the 3V and 5.5V power pins on the Pi supply are limited to about 1A. 
If a component pulls more than that, you risk power cycling the Pi. 
That is why we use a relay instead to supply 5V and more current to the solenoid. 
This is standard practice for power control circuits in many situations. 
For example, using a common off-the-shelf (COTS) 15A light switch to actuate a relay bank that controls hundreds of amps of lighting for an entire office floor.
{{% /alert %}}

{{< figure src="../img/nerf-robot/power-relay.jpg" width="400px" alt="Power relay." title="Power Relay." >}}
<ol>
<li>Connect the solenoid to the relay.</li>
<ol type="a">
    <li>Connect a wire to the Normally Open (<strong>NO</strong>) terminal connector.</li>
    <li>Connect the other end to a ground pin on the Raspberry Pi. (Ground pins: 09, 25, 39, 06, 14, 23, 30, or 34)</li>
    </ol>
<li>Connect the Relay <strong>COM</strong>mon pin.</li>
<ol type="a">
<li>Connect the <strong>COM</strong> pin to the 3.3V power of the Raspberry Pi. (3.3V pins: 01 or 17)</li>
</ol>
<li>Connect <strong> VCC </strong>(<strong>DC+</strong>) and ground (<strong>DC-</strong>) .</li>
<ol type="a">
<li>Connect <strong>DC+</strong> to the 5V of the Raspberry Pi. (5V Pins: 02 or 04)</li>
<li>Connect <strong>DC-</strong> to ground on the Raspberry Pi. (Ground pins: 09, 25, 39, 06, 14, 20, 30, or 34)</li>
</ol>
<li>Connect <strong>IN</strong>. </li>
<ol type="a">
<li>Connect <strong>IN</strong> to a GPIO pin on the Raspberry Pi. (GPIO Pins: 03, 05, 07, 11, 13, 15, 19, 21 23, 29, 31, 35, 37, 08, 10, 12, 16, 18, 22, 24, 26, 32, 36, 38, or 40)</li>
<li>For this example, we've connected to pin 37.</li>
</ol>
</ol>

#### Assemble Solenoid/Nerf Gun

{{< figure src="../img/nerf-robot/assembled-nerf-gun.jpg" width="400px" alt="Solenoid attached to the orange nerf gun using rubber bands and electrical tape." title="Nerf Gun/Solenoid Assembly." >}}

1. Modify the Nerf gun to make room for the solenoid. 
   Using cutting pliers, we cut the trigger guard off of the front as seen in the picture above.
2. Test that the solenoid has enough power to press the trigger when the Nerf gun is loaded. 
3. If the solenoid is not strong enough we can:
    * Wrap the trigger with rubber bands to make the trigger easier to fire[^rb].
    * Increase the voltage to the solenoid. 
  Right now it receives 5 volts, but some solenoids can support up to 12 volts. 
  If necessary, you can connect the solenoid to another power supply such as a 9 volt battery. 
  Check the details of your solenoid[^solvolt]. 
4. Tape the solenoid so it will make good contact with the trigger when it is activated via the relay.
5. Put all of your components onto your base.

[^rb]: If you use the rubber band method, you may need to pull the rubber bands away from the trigger when reloading the Nerf gun so it can reset and load properly. 
Try activating the solenoid manually to ensure that it hits the nerf gun trigger in the right spot.
[^solvolt]:  If you choose to increase the voltage, you must connect **VCC** and ground (**DC+** and **DC-**) to the new voltage source rather than connecting them to the Raspberry Pi as described in Step 3 of [Assemble Solenoid/Nerf Gun](##assemble-solenoidnerf-gun).

{{< figure src="../img/nerf-robot/ng-taped-to-rover.jpg"  alt="Nerf gun taped to a rover base using electrical tape." title="Nerf Gun Taped to the Rover" width="400">}}

### **How to Configure Your Nerf Gun Robot with the Viam App**

Create a new robot in the Viam app and give it a name. 
Then in the robot’s **CONFIG** tab you will be able to create new components with the following attributes:

* **Name**: 
* **Type**: 
* **Model**: 

#### Configure the Pi (board)

Add your board with the name `board`, type `board` and model `pi`. Click **Create Component**.

{{< figure src="../img/nerf-robot/add-board.png"  alt="Viam App Board component attribute pane." title="Board Component Attribute Pane" width="800" >}}

You can name your board whatever you want, we picked `board` for simplicity. 
Just remember to use it consistently in the following steps. 

#### Configure the motors (left and right)

Add the left [motor](https://docs.viam.com/components/motor/) with the name “left”, type `motor`, and model `gpio`. 
Add the right motor with the name “right”, type `motor` and model `gpio`. 
After clicking **Create Component** you’ll see a pin assignment type toggle. 
Click **In1/In2** since that is compatible with the type of input our motor controller expects. 
In the drop downs for A/In1 and B/In2, choose `11 GPIO 17` and `13 GPIO 27`, respectively, for the left motor, and `16 GPIO 23` and `18 GPIO 24`, respectively, for the right motor. 
In the **Board** drop-down, choose the name of the board the motor controller is wired to (“board”). 
Make them depend on the board component by choosing the board’s name (“board”) from the **Depends On** drop-down at the bottom of the motor config. 
This ensures that the board initializes before the motor driver when the robot boots up, thereby reducing errors.

<table>
<tr><td style="background:white; border-right: 1px solid black; padding-right: 25px">
{{< figure src="../img/nerf-robot/left-motor.png"  alt="Motor Component Attribute Pane (left motor)." title="Left Motor Component Configuration Pane" width="400">}}  
</td><td style="background:white;">
{{< figure src="../img/nerf-robot/right-motor.png"  alt="Motor Component Attribute Pane (right motor)." title="Right Motor Component Configuration Pane" width="400">}} 
 </td></tr></table>

Click **SAVE CONFIG** at the bottom of the screen. 
Then go to the **CONTROL** tab where you will now see the buttons you can use to control the motors: 

{{< figure src="../img/nerf-robot/LR-motor-config-panes.png"  alt="Left and right motor configuration panes." title="Left and Right Motor Configuration Panes" width="800">}}

Now, you can move around your wheels separately. 
Let’s add a base to be able to control them together. 

#### Configure the base

Add your motors to the [base](https://docs.viam.com/components/base/) so you can move them around with your keyboard. 

Here we have to specify the wheel circumference and the width between the wheels. 
Depending on your rover, you can change these numbers. 
Don’t forget to make the base depend on the `left`, `right`, and the `board` components. 

{{< figure src="../img/nerf-robot/config-base.png"  alt="Base Component Attribute Pane." title="Base Component Attribute Pane" width="800">}}

Now let’s add a camera so we can see the stream on the control panel as you move your rover. 

#### Configure the camera

Add your usb camera as a webcam. 

{{< figure src="../img/nerf-robot/config-webcam.png"  alt="Camera Component Attribute Pane." title="Camera Component Attribute Pane" width="800" >}}

If you go back to the **CONTROL** tab, you will see your base and camera. 

{{< figure src="../img/nerf-robot/base-cam-view.png"  alt="Camera view from the Base component's keyboard tab." title="Camera View from the Base Component's Keyboard Tab." width="800">}}

Here you can click the toggle to enable keyboard control, and use A, W, S, and D to move your rover around. 
You can view the camera stream at the same time. 
If you scroll down, you will see your camera as a component and you will be able to change the refresh frequency and export screenshots from your camera. 

{{< figure src="../img/nerf-robot/camera-cam-view.png"  alt="Camera view from the Camera component pane." title="Camera View from the Camera Component Pane." width="800">}}

#### Toggle between your GPIO pin states

The board card in the **CONTROL** tab provides a way to change the state of the pin connected to the solenoid. 
If you click the board component, you will be able to see your GPIO pin and its current state. 
In the **Set** part of the GPIO section, select pin 37 (the pin we wired to control the solenoid). 
If you set the pin state to high, the solenoid will actuate. 
If you set it to low, it should deactivate the solenoid. 
Since we already assembled the robot, setting pin 37 to high will allow you to shoot your Nerf gun if its loaded. 

{{< figure src="../img/nerf-robot/board-low.png"  alt="Board component, G P I O section showing High selected on the Pin State drop-down." title="Board component, GPIO section showing High selected on the Pin State drop-down" width="800">}}

{{< figure src="../img/nerf-robot/board-displaying-high.png"  alt="Board component, G P I O section with High selected." title="Board component, GPIO section with High selected." width="800">}}

{{< figure src="../img/nerf-robot/board-high.png"  alt="Board component, G P I O section showing Low selected on the Pin State drop-down." title="Board component, GPIO section showing Low selected on the Pin State drop-down" width="800">}}

### Debug info

* If any components are not appearing when connecting to the robot in Viam App check the logs tab for any potential errors.

### Final Code

Raw JSON for entire config can be found here if you wish to copy it into your config: [https://gist.github.com/mestcihazal/7683fbdd0975579b44295b3208757b5a](https://gist.github.com/mestcihazal/7683fbdd0975579b44295b3208757b5a)


#### Control via Viam App

##### Controlling the Base

1. Navigate to Viam app -> base component
2. Enable keyboard controls
3. Drive your robot around!

##### Firing the Nerf dart

1. Make sure your Nerf gun is loaded and ready to go
2. When you are ready, navigate to the Viam app -> **CONTROL** tab -> board component and set the **IN** pin (pin 37 in our example) to high to fire. 

You can see the demo video of it in action here:

{{< video src="../videos/NerfGunRobotDemo.mp4" type="video/mp4">}}

## **Summary**

In this tutorial, you learned how to create a remote controllable Nerf gun robot activated by GPIO pins on a Raspberry Pi using Viam. 
You could use this same concept to build a security robot which shoots darts at people if they enter your room, a Nerf ball blaster dog toy, a kitten treat shooter for cats to fetch in excitement, you name it! 
You can even add object detection and machine learning, and only activate when your camera sees a specific object or person. 

If you are looking for some projects that would be a great next step in your journey of learning how to build robots, we recommend that you check out the following tutorials:



* [Tutorial List](https://docs.viam.com/#tutorials)

If you have any issues getting Viam set up or if you are stuck, let us know on the[ Viam Community Slack](http://viamrobotics.slack.com), and we will be happy to help you get up and running.
 It is also a great place if you want to connect with other developers learning how to build robots. 
