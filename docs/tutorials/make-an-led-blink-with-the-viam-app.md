---
title: "How to Make an LED Blink with a Raspberry Pi Using the Viam App"
linkTitle: "Blink an LED with a Pi and the Viam App"
weight: 05
type: "docs"
description: "How to make an LED blink with a Raspberry Pi and the Viam app."
# SME: Joe Karlsson
---

In this post, we will show you how to use Viam to make an LED blink with a Raspberry Pi.
This tutorial is a great place to start if you have never built a robot or a circuit before.

<img src="../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image9.gif" alt ="A GIF of the completed project showing a blinking blue LED connected to a Raspberry Pi with jumper cables." width="50%"><br>

## What you'll need for this guide

You will need the following tools to complete the project:

### Hardware

<ol>
    <li><a href="https://a.co/d/5Tn67G3" target="_blank">Raspberry Pi 3 or 4</a></li>
<ol type="a">
<li>Refer to the <a href="https://docs.viam.com/getting-started/rpi-setup" target="_blank">Viam Raspberry Pi Setup Guide </a> to setup your Pi.</li>
</ol>
    <li><a href="https://amzn.to/2Q4Z5Ta" target="_blank">Solderless breadboard</a></li>
    <li><a href="http://amzn.to/2qVhd4y" target="_blank">Jumper wires for easy hookup</a></li>
    <li><a href="http://amzn.to/2Dmainw" target="_blank">Resistor pack </a>You will be using a 100 Ohm resistor, which is the resistor with brown-black-brown bands</li>
    <li><a href="http://amzn.to/2Ex2v5q" target="_blank">LED</a></li>
</ol>

[Click to view the Component URL Listing](#components-url-list)

### Software

- [viam-server](/getting-started/rpi-setup/)

## Project setup

Before you proceed with building your circuit, you are going to need to set up the operating system on your Raspberry Pi and install Viam Server on the Pi.
We recommend that you follow along with the [Installing Viam Server on Raspberry Pi](/getting-started/rpi-setup/) guide in the Viam documentation.
Be sure to follow all the steps including [adding your Pi on the Viam app.](/getting-started/rpi-setup/#adding-your-pi-on-the-viam-app)

{{% alert title="Tip" color="tip" %}}  
If you have any issues whatsoever setting up Viam on your Raspberry Pi, let us know on the <a href="http://viamrobotics.slack.com" target="_blank">Viam Community Slack</a>, and we will be happy to help you get up and running.
{{% /alert %}}

## Building the circuit

The first step in this project is to design a simple LED circuit.
Then you will make the LED circuit controllable from the Raspberry Pi by connecting the circuit to the **general purpose input/output** (GPIO) pins on the Raspberry Pi.

A simple LED circuit consists of a LED and resistor.
The resistor is used to limit the current that is being drawn and is called a *current-limiting resistor*.

### GPIO Pinout

**General-purpose input/output** (**GPIO**) is a digital signal <a href="https://en.wikipedia.org/wiki/Pin_(electronics)" target="_blank">pin</a>[^pin] on a circuit board, like a Raspberry Pi, which may be used as an input or output, or both, and is controllable by software.

<img src="../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image10.png" alt ="Photo showing a Raspberry Pi 4 with a white box around the GPIO pins on the Pi and big red letters that say, 'GPIO Pins.'" width="100%"><br>

As you may have guessed, **each pin has a specific role, and you can use it only for that role**. Some of them are input/output, power (3.3V or 5V), or ground.
As you can see in the diagram below, there are 40 output pins on the Pi. You can program 26 of the GPIO pins.

<img src="../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image4.jpg" alt ="Diagram showing all of the GPIO pins on a Raspberry Pi 4 and their corresponding pin number and function." width="100%"><br>

One thing to note that might be confusing with the pin numbering on Raspberry Pi's: There are 40 physical pins numbered from 1 to 40.
That is **board pin numbering,** corresponding to the pin's physical location on the board.
When working with the GPIO pins with Viam, you will use the board numbers.
e.g., Pin 1 can be located pretty easily, since Pin 1 is the always the pin whose corner is rounded.

Then there's numbering them by function or GPIO connection.
These are the big numbers, e.g. "GPIO 22". These numbers are helpful for understanding the function of each pin.

When in doubt, the website <a href="https://pinout.xyz/" target="_blank">pinout.xyz</a>[^pinout] is useful for identifying pins.
It gives you the exact layout and role of each pin.

### Circuit Explanation

Here's the circuit diagram used in this tutorial for making the LED blink.

<img src="../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image1.png" alt ="Circuit diagram showing a Raspberry Pi with a red connector running out of GPIO pin 8 to a 100-ohm resistor. The resistor is connected to the long lead of a red LED bulb. Finally, a blue connector connects the short lead of the LED to the ground connection on pin 6 of the Raspberry Pi GPIO pins." width="100%"><br>

You can now hook the LED and resistor up to GPIO 14 on pin 8 on your Raspberry Pi.
The resistor and LED need to be in series as in the diagram above. To find the right resistor use the resistor color code -- for a 100 ohm resistor, it needs to be brown-black-brown.
You can use your multimeter to double-check the resistor value or check yours using the photo below.

<img src="../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image3.jpg" alt ="Photo of a 100-ohm resistor with text overlaid that says, in order, brown-black-brown-gold." width="50%"><br>

When hooking up the circuit, note the *polarity* of the LED.
You will notice that the LED has long and short leads. The long lead is the positive side, which is known as the anode, the short lead is the negative side, which is known as the cathode.
The long anode should be connected to the resistor and the short cathode should be connected to the ground via the blue jumper wire and pin 6 on the Raspberry Pi as shown on the diagram.

## Configuring your bot using the Viam app

Before proceeding, be sure that you have added your Pi to the Viam app.
Steps on how to do this can be found in the [Adding your Pi on the Viam App](/getting-started/rpi-setup/#adding-your-pi-on-the-viam-app) section of the Viam Documentation.

Now that we have gotten that out of the way, let's get back to setting up your robot in the Viam app.
First, go to the Viam app at [app.viam.com](https://app.viam.com/) on your web browser, and select the robot's config.

<img src="../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image2.png" alt ="Screenshot of the Vam App showing the default board configuration on the 'components' tab." width="100%"><br>

The first component you will add is the **`board`** representing your your single board computer, which in this case is the Raspberry Pi.
This is where you will wire all other components. To create a new component, select **`Create a component`**. For the component **`Type`**, select **`board`**.
Then you can name the **`board`** whatever you like as long as you are consistent when referring to it later; we'll name this component **`local`** since it is the **`board`** we will communicate with directly.
For **`Model`**, select **`pi`**, then click **`new component`**.
Your board component's config will generate the following JSON attributes:

<img src="../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image6.png" alt ="Screenshot of the Viam app showing the board configuration on the 'config' tab. The board is named 'local' and the attributes are shown as empty braces." width="100%"><br>

As you add your board component to your robot in the Viam app, it generates a tab for your board in the Control tab.
Here, you can click on "**Get**" to get the current status of your pin.
The first time you click "**Get Pin State**", it should return "Pin: 8 is low."

<img src="../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image5.png" alt ="Screenshot of the Viam app showing the board configuration on the **CODE SAMPLE** tab. The 'Board Local' row is expanded, and under the 'Get' row, the pin is set to '8.' A red box is around the '**Get Pin State**' button and the output, which reads, 'Pin: 8 is low.'" width="100%"><br>

You can now select "**Set**" to control the status of your pin to "high."
It will look like this:

<img src="../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image8.png" alt ="Screenshot of the Viam app showing the board configuration on the 'Connect' tab. The 'Board Local' row is expanded, and under the 'Set' row, the pin is set to '8.' A red box is around the 'Set Pin State' field." width="100%"><br>

After setting your pin to "high" the LED should illuminate.
You can play around with values "**low**" and "**high**" by setting them differently, and you will see your LED toggle on and off.

<img src="../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image7.gif" alt ="A GIF of the completed project showing a blinking blue LED connected to a Raspberry Pi with jumper cables." width="35%"><br>

## Summary

Congratulations!
If you have followed along, you have just successfully used Viam to make an LED blink with a Raspberry Pi!
Hopefully, you have learned how the GPIO on a Raspberry Pi works, and how to build circuits for LED bulbs.

You are ready for your next robotics project.
We recommend that you check out the next part in this series, [How to Make an LED Blink with a Raspberry Pi and the Viam SDK](/make-an-led-blink-with-a-raspberry-pi-and-sdk/), where you will learn how to use the Viam SDK to control a Raspberry Pi robot with Go or Python.

If you are looking for some more projects that would be a great next step in your journey of learning about how to build robots, we would recommend that you check out one of following [Tutorial List](..).

If you want to connect with other developers learning how to build robots or if you have any issues whatsoever getting Viam set up, let us know on the <a href="http://viamrobotics.slack.com" target="_blank">Viam Community Slack</a>[^slack], and we will be happy to help you get up and running

## Components URL List

<ul>
    <li>Raspberry Pi 3 or 4: <a href="https://a.co/d/5Tn67G3" target="_blank">ht<span></span>tps://a.co/d/5Tn67G3</a></li>
    <li>Solderless breadboard: <a href="https://amzn.to/2Q4Z5Ta" target="_blank">ht<span></span>tps://amzn.to/2Q4Z5Ta</a></li>
    <li>Jumper wires for easy hookup: <a href="http://amzn.to/2qVhd4y" target="_blank">ht<span></span>tp://amzn.to/2qVhd4y</a></li>
    <li>Resistor pack: <a href="http://amzn.to/2Dmainw" target="_blank">ht<span></span>tp://amzn.to/2Dmainw</a></li>
    <li>Red LED: <a href="http://amzn.to/2Ex2v5q" target="_blank">ht<span></span>tp://amzn.to/2Ex2v5q</a></li>
    <li>Multimeter (optional): <a href="http://amzn.to/2qWurxS" target="_blank">ht<span></span>tp://amzn.to/2qWurxS</a></li>
</ul>

[^pin]: <a href="https://en.wikipedia.org/wiki/Pin_(electronics)" target="_blank">Wikipedia: htt<span></span>ps://en.wikipedia.org/wiki/Pin_electronics</a>
[^pinout]: <a href="https://pinout.xyz/" target="_blank">Pinout: pinout.xyz</a>
[^slack]: <a href="http://viamrobotics.slack.com" target="_blank">Viam Community Slack: ht<span></span>tp://viamrobotics.slack.com</a>
