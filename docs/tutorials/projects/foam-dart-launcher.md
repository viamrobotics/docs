---
title: "Foam Dart Launcher Robot Tutorial"
linkTitle: "Dart Launcher Robot"
type: "docs"
description: "Build a foam dart launcher with a wheeled rover and a Raspberry Pi."
webmSrc: "/tutorials/videos/foam-dart.webm"
mp4Src: "/tutorials/videos/foam-dart.mp4"
videoAlt: "Robot launching a dart."
images: ["/tutorials/videos/foam-dart.gif"]
aliases:
  - /tutorials/foam-dart-launcher
tags: ["base", "motor", "camera", "raspberry pi"]
# SME: Kurt S. and Hazal M.
authors: ["Hazal Mestci"]
languages: ["python"]
viamresources: ["base", "camera", "motor", "board"]
level: "Intermediate"
date: "2022-11-29"
# updated: ""
cost: "145"
no_list: true
---

## Introduction

This tutorial will show you how to build your very own foam dart launcher robot using Viam, a Raspberry Pi, a generic foam dart launcher with foam darts, a USB camera, a solenoid, a relay, and a motor controller.
This robot will be able to move around and launch foam darts.

This project is a great place to start if you are new to building robots, have a love for Nerf toys, an occasion to target something and launch a dart at it, or if you just want to troll your friends.
Don’t forget to be careful and have fun!

{{<gif webm_src="/tutorials/foam-dart-launcher/init-image-nerf-robot.webm" mp4_src="/tutorials/foam-dart-launcher/init-image-nerf-robot.mp4" alt="Robot launching a dart from a foam dart launcher taped to the robot." max-width="400px">}}

## What You’ll Need for This Tutorial

You will need the following hardware, software, tools, and consumables to complete this project:

{{% alert title="Important" color="note"%}}
If you use a different rover and/or motor controller, ensure that the motor driver is compatible with the motors on your rover.
For example, a brushed DC motor requires a brushed DC motor driver that is rated for the power requirements of the motor.
Also, the configuration files shown in this tutorial _must_ be modified if you use a different setup.

You can find more information on configuring different motors in the [Motor Component](/build/configure/components/motor/) topic.
{{% /alert %}}

### Hardware and software requirements

- [Raspberry Pi with microSD card](https://a.co/d/bxEdcAT), with `viam-server` installed per [our Raspberry Pi setup guide](/get-started/installation/).
- [A wheeled rover](https://www.amazon.com/Smart-Chassis-Motors-Encoder-Battery/dp/B01LXY7CM3/)
- [A foam dart launcher](https://www.amazon.com/Nerf-N-Strike-Elite-Jolt-Blaster/dp/B01HEQHXE8)
- [A USB camera (webcam)](https://www.amazon.com/gp/product/B0972KK7BC/) (optional, to see where you are going and aiming)
- [A solenoid](https://www.amazon.com/0530-Frame-Solenoid-Electromagnet-Stroke/dp/B07K35L4TH/)
- [A relay](https://www.amazon.com/HiLetgo-Channel-Isolation-Support-Trigger/dp/B00LW15D1M/)
- [A dual motor controller](https://www.amazon.com/Qunqi-Controller-Module-Stepper-Arduino/dp/B014KMHSW6/)
  If you use a different motor driver, refer to the manufacturer’s data sheet and our [motor component topic](/build/configure/components/motor/) to learn how to configure the pins.
- Jumper wires (breadboard wires)

### Tools and Consumables

- Solder (optional)
- Small flathead screwdriver
- Cutting pliers (flush-cutting pliers preferred)
- Electrical tape
- Elastic/rubber bands

## How to Assemble Your Hardware

### Motor Controller Setup

A motor controller is a piece of hardware that takes digital signals from the Raspberry Pi and sends power to the motors accordingly.
For this setup we have one dual motor controller for the two motors.

{{% alert title="Info" color="info" %}}
If you have more than two motors you will likely need two motor controllers.
{{% /alert %}}

{{< figure src="/tutorials/foam-dart-launcher/dual-h-bridge-motor-controller.jpg" width="400px" alt="Dual H-bridge motor controller with four signal wires going in and two sets of motor power wires coming out." title="Dual H-bridge motor controller." >}}

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
This allows us to activate the foam dart launcher with a GPIO pin on the board.

{{% alert title="Info" color="info" %}}
We cannot directly power these components from GPIO pins, since there is a board limitation that restricts GPIO pins to providing 3.3V and a very limited current supply (16mA).
Even the 3.3V and 5V power pins on the Pi supply are limited to about 1A.

If a component attempts to pull more current than that, you risk power cycling the Pi.
That is why we use a relay to supply 5VDC with a higher current to actuate the solenoid.
This is standard practice for power control circuits in many situations.
For example, by using a common off-the-shelf 15A light switch to actuate a relay bank, it is possible to control hundreds of amps of lighting for an entire office floor.
{{% /alert %}}

{{< figure src="/tutorials/foam-dart-launcher/power-relay.jpg" width="400px" alt="Power relay." title="Power relay." >}}

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
<li>Connect <strong>DC+</strong> to the 6V of the external battery pack.</li>
<li>Connect <strong>DC-</strong> to ground on the Raspberry Pi. </li>
</ol>
<li>Connect <strong>IN</strong>. </li>
<ol type="a">
<li>Connect <strong>IN</strong> to a GPIO pin on the Raspberry Pi. </li>
<li>For this example, we've connected to pin 37.</li>
</ol>
</ol>

### Assemble Solenoid/Foam Dart Launcher

{{< figure src="/tutorials/foam-dart-launcher/assembled-foam-dart-launcher.jpg" width="400px" alt="Solenoid attached to the orange foam dart launcher using rubber bands and electrical tape." title="Foam dart launcher/Solenoid Assembly." >}}

1. Modify the foam dart launcher to make room for the solenoid.
   Using cutting pliers, we cut the trigger guard off of the front as seen in the picture above.
2. Test that the solenoid has enough power to press the trigger when the foam dart launcher is loaded.
3. If the solenoid is not strong enough we can:
   - Wrap the trigger with rubber bands to make the trigger easier to activate[^rb].
   - Increase the voltage to the solenoid.
     Right now it receives 5 volts, but some solenoids can support up to 12 volts.
     If necessary, you can connect the solenoid to another power supply such as a 9 volt battery.
     Check the details of your solenoid[^solvolt].
4. Tape the solenoid in such a manner that it makes good contact with the trigger when activated with the relay.
5. Attach all of your components to the base.

[^rb]:
    If you use the rubber band method, you may need to pull the rubber bands away from the trigger when reloading the foam dart launcher so it can reset and load properly.
    Try activating the solenoid manually to ensure that it hits the foam dart launcher trigger in the right spot.

[^solvolt]: If you choose to increase the voltage, you must connect **VCC** and ground (**DC+** and **DC-**) to the new voltage source rather than connecting them to the Raspberry Pi as described in Step 3 of [Assemble Solenoid/Foam Dart Launcher](#assemble-solenoidfoam-dart-launcher).

{{< figure src="/tutorials/foam-dart-launcher/ng-taped-to-rover.jpg"  alt="Foam dart launcher taped to a rover base using electrical tape." title="Foam dart launcher Taped to the Rover" width="400">}}

## Configure Your Foam Dart Launcher Robot with the Viam App

Create a new robot in the Viam app and give it a name.
Navigate to your new robot's **Config** tab and click the **Components** subtab.

### Board Configuration (Raspberry Pi)

Click **Create component** and add your [board](/build/configure/components/board/).
Choose type `board` and model `pi`.
Name it `local` and click **Create**.

{{<imgproc src="/tutorials/foam-dart-launcher/add-board.png" resize="800x" declaredimensions=true alt="Viam app board component attribute pane.">}}

You can name your board whatever you want, we picked `local`.
Just remember to use that name consistently in the following steps.

### Motor Configuration

#### Left Motor

Click **Create component** and add the left [motor](/build/configure/components/motor/) with type `motor` and model `gpio`.
Name it `left` and click **Create**.

Select the name of the board the motor controller is wired to (for example, "local") from the **Board** dropdown.

Toggle the **Component Pin Assignment Type** to **In1/In2** since that is compatible with the input type our motor controller expects.

In the **A/In1** and **B/In2** dropdowns, choose `11 GPIO 17` and `13 GPIO 27`, respectively.

Set **Max RPM** to `150`.

{{<imgproc src="/tutorials/foam-dart-launcher/left-motor.png" resize="800x" declaredimensions=true alt="Left motor component config UI.">}}

Click **Save config** at the bottom of the screen.

#### Right Motor

Click **Create component** and add the right [motor](/build/configure/components/motor/) with type `motor` and model `gpio`.
Name it `right` and click **Create**.

Select the name of the board the motor controller is wired to (for example, "local") from the **Board** dropdown.

Toggle the **Component Pin Assignment Type** to **In1/In2**.

For **A/In1** select `16 GPIO 23` and for **B/In2** select `18 GPIO 24`.

Set **Max RPM** to `150`.

{{<imgproc src="/tutorials/foam-dart-launcher/right-motor.png" resize="800x" declaredimensions=true alt="Right motor component config UI.">}}

Click **Save config** at the bottom of the screen.
Then go to the **Control** tab where you will now see the buttons you can use to control the motors:

{{<imgproc src="/tutorials/foam-dart-launcher/LR-motor-config-panes.png" resize="800x" declaredimensions=true alt="Left and right motor configuration panes.">}}

Now you can drive your left and right wheels separately.
Let’s add a base to be able to control them together.

### Base Configuration

Configure a [base component](/build/configure/components/base/) to coordinate your motors so you can move the base around with your keyboard.

Click **Create component** and add the base with type `base` and model `wheeled`.
Give it a name (you can call it `base`) and click **Create**.

From the **Right Motors** and **Left Motors** dropdowns, select `right` and `left`, respectively (the motors you configured in the previous step).

Set the **Wheel Circumference** to `200` and the **Width** to `130` if you used [the same rover we did](https://www.amazon.com/Smart-Chassis-Motors-Encoder-Battery/dp/B01LXY7CM3/).
If you used different hardware, measure the diameter of your wheels and multiply by pi for the circumference.
Measure the distance between the centers of the right and left wheels to find the width.

{{<imgproc src="/tutorials/foam-dart-launcher/config-base.png" resize="800x" declaredimensions=true alt="Base Component Attribute Pane.">}}

Now let’s add a camera to watch the video stream on the control panel as you move your rover.

### Camera Configuration

Add your USB camera as a webcam.
Please refer to [our webcam documentation](/build/configure/components/camera/webcam/) for complete instructions.

{{<imgproc src="/tutorials/foam-dart-launcher/config-webcam.png" resize="800x" declaredimensions=true alt="Camera Component Attribute Pane.">}}

If you go back to the **Control** tab and click to expand the base panel, you will see your base and camera:

{{<imgproc src="/tutorials/foam-dart-launcher/base-cam-view.png" resize="800x" declaredimensions=true alt="Camera view from the Base component's keyboard tab.">}}

Toggle the switch under **Keyboard Disabled** to enable keyboard control, then use the W, A, S, and D keys on your keyboard to move your rover around.
You can view the camera stream at the same time.

### Final Config

The full raw JSON config file generated by the configuration steps you just completed will look like this:

{{% expand "Click to view the raw JSON for the dart launcher robot" %}}

```json
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "left",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "pins": {
          "a": "11",
          "b": "13",
          "pwm": ""
        },
        "board": "local",
        "max_rpm": 150
      },
      "depends_on": []
    },
    {
      "name": "right",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "pins": {
          "a": "16",
          "b": "18",
          "pwm": ""
        },
        "board": "local",
        "max_rpm": 150
      },
      "depends_on": []
    },
    {
      "name": "base",
      "model": "wheeled",
      "type": "base",
      "namespace": "rdk",
      "attributes": {
        "width_mm": 130,
        "wheel_circumference_mm": 200,
        "left": ["left"],
        "right": ["right"]
      },
      "depends_on": []
    },
    {
      "name": "camera",
      "model": "webcam",
      "type": "camera",
      "namespace": "rdk",
      "attributes": {
        "video_path": "video0"
      },
      "depends_on": []
    }
  ]
}
```

{{% /expand %}}

If you prefer you can copy paste it, replacing the **Raw JSON** field on your robot's **Config** tab instead of going through all the steps above.

## Toggling GPIO Pin States

The board card in the **Control** tab provides a way to change the state of the pin connected to the solenoid.
If you click the board component, you will be able to see your GPIO pin and its current state.
In the **Set** part of the GPIO section, select pin **37** (the pin we wired to control the solenoid).
If you set the pin state to high, the solenoid will actuate.
If you set it to low, it should deactivate the solenoid.
Since we already assembled the robot, setting pin 37 to **high** launches your foam dart launcher if its loaded.

{{< figure src="/tutorials/foam-dart-launcher/board-low.png"  alt="Board component, G P I O section showing Low selected on the Pin State dropdown." title="Board component, GPIO section showing Low selected on the Pin State dropdown" width="800">}}

{{< figure src="/tutorials/foam-dart-launcher/board-displaying-high.png"  alt="Board component, G P I O section with pin 37 set to High." title="Board component, GPIO section with pin 37 set to High." width="800">}}

{{< figure src="/tutorials/foam-dart-launcher/board-high.png"  alt="Board component, G P I O section showing High selected on the Pin State dropdown." title="Board component, GPIO section showing High selected on the Pin State dropdown" width="800">}}

## Control with the Viam App

### Controlling the Base

1. Navigate to Viam app -> base component
2. Enable keyboard controls
3. Drive your robot around!

### Activating the Foam Dart Launcher

1. Make sure your foam dart launcher is loaded and ready to go.
2. When you are ready, navigate to the Viam app -> **Control** tab -> board component and set the **IN** pin (pin 37 in our example) to high to activate.

You can see the demo video of it in action here:

{{<video webm_src="/tutorials/videos/FoamDartLauncherRobotDemo.webm" mp4_src="/tutorials/videos/FoamDartLauncherRobotDemo.mp4" poster="/tutorials/foam-dart-launcher/FoamDartLauncherRobotDemo.jpg" alt="Foam Dart Launcher Demo">}}

## Troubleshooting

If any component fails to appear when connecting to the robot in the Viam app, check the **Logs** tab for potential errors.

## Summary

In this tutorial, you learned how to create a remotely-controlled foam dart launching robot activated by the GPIO pins on a Raspberry Pi using Viam.
You could use this same concept as the basis for a security robot that launches darts at people if they enter your room, a Nerf ball blaster dog toy, a kitten treat shooter for cats to fetch in excitement, you name it!
You could even add [object detection and machine learning](/ml/vision/) and activate the launcher only when the camera sees a specific object or person.

If you are looking for a new robotics project, check out our other [tutorials](/tutorials/).

{{< snippet "social.md" >}}
