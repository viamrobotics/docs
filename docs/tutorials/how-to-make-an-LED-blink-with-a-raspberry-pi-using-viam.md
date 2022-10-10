---
title: "Making an LED Blink with a Raspberry Pi Using Viam"
linkTitle: "Make an LED Blink with a Pi and Viam"
weight: 87
type: "docs"
description: "How to make an LED blink with a Raspberry Pi and Viam."

---

## Intro

In this post, we will show you how to use Viam to make an LED blink with a Raspberry Pi. This tutorial is a great place to start if you have never built a robot or a circuit before.

![A GIF of the completed project showing a blinking blue LED connected to a Raspberry Pi with jumper cables.](../img/how-to-make-an-LED-blink-with-a-raspberry-pi-using-viam/image9.gif)

## What you'll need for this guide

You will need the following tools to complete the project:

[Click to view the Component URL Listing](#components-url-list)
<ol>
<li><a href="https://a.co/d/5Tn67G3" target="_blank">Raspberry Pi 3 or 4</a></li>
  
<ol type="a">

<li>Refer to the <a href="https://docs.viam.com/getting-started/installation" target="_blank">Viam Raspberry Pi Setup Guide </a> to setup your Pi.</li>

<li>Be sure that you have <a href="https://docs.viam.com/getting-started/installation/#installing-viam-server" target="_blank">set up Viam Server on your Raspberry Pi</a> as well.</li>
</ol>
<li><a href="https://amzn.to/2Q4Z5Ta" target="_blank">Solderless breadboard</a></li>
<li><a href="http://amzn.to/2qVhd4y" target="_blank">Jumper wires for easy hookup</a></li>
<li><a href="http://amzn.to/2Dmainw" target="_blank">Resistor pack </a></li>
<OL type="a">

<li>You will be using a 220Ω or a 1K Ω resistor, which are the resistors with brown-black-brown or brown-black-red colored bands, respectively.</li>
</OL>
<li><a href="http://amzn.to/2Ex2v5q" target="_blank">Red LED</a></li>
<li><a href="http://amzn.to/2qWurxS" target="_blank">Multimeter (optional)</a></li>
<li><a href="https://github.com/viamrobotics/rdk/tree/0c550c246739b87b4d5a9e8d96d2b6fdb3948e2b" target="_blank">Viam Server</a></li></ol>

## Project setup

Before you proceed with building your circuit, you are going to need to set up the operating system on your Raspberry Pi and install Viam Server on the Pi. We recommend that you follow along with the [Installing Viam Server on Raspberry Pi](../../getting-started/installation) guide in the Viam documentation. Be sure to follow all the steps including [adding your Pi to Viam.](../../getting-started/installation/#adding-your-pi-on-the-viam-app)

{{% alert title="Note" color="note" %}}  
If you have any issues whatsoever setting up Viam on your Raspberry Pi, let us know on the [Viam Community Slack](http://viamrobotics.slack.com), and we will be happy to help you get up and running.*
{{% /alert %}}

## Building the circuit

The first step in this project is to design a simple LED circuit. Then you will make the LED circuit controllable from the Raspberry Pi by connecting the circuit to the **general purpose input/output** (GPIO) pins on the Raspberry Pi.

A simple LED circuit consists of a LED and resistor. The resistor is used to limit the current that is being drawn and is called a *current-limiting resistor*.

### GPIO Pinoutccc

**General-purpose input/output** (**GPIO**) is a digital signal <a href="https://en.wikipedia.org/wiki/Pin_(electronics)" target="_blank">pin</a>[^pin] on a circuit board, like a Raspberry Pi, which may be used as an input or output, or both, and is controllable by software.

[^pin]: Pin (Electronics): <a href="https://en.wikipedia.org/wiki/Pin_(electronics)" target="_blank">https://en.wikipedia.org/wiki/Pin_(electronics)</a>

![Photo showing a Raspberry Pi 4 with a white box around the GPIO pins on the Pi and big red letters that say, "GPIO Pins."](../img/how-to-make-an-LED-blink-with-a-raspberry-pi-using-viam/image10.png)

As you may have guessed, **each pin has a specific role, and you can use it only for that role**. Some of them are input/output, power (3.3V or 5V), or ground. As you can see in the diagram below, there are 40 output pins on the Pi. You can program 26 of the GPIO pins.

![Diagram showing all of the GPIO pins on a Raspberry Pi 4 and their corresponding pin number and function.](../img/how-to-make-an-LED-blink-with-a-raspberry-pi-using-viam/image4.jpg)

One thing to note that might be confusing with the pin numbering on Raspberry Pi's: There are 40 physical pins numbered from 1 to 40. That is **board pin numbering,** corresponding to the pin's physical location on the board. When working with the GPIO pins with Viam, you will use the board numbers. Pin 1 can be located pretty easily, since Pin 1 is the always the pin whose corner is rounded.

Then there's numbering them by function or GPIO connection. These are the big numbers, e.g. "GPIO 22". These numbers are helpful for understanding the function of each pin.

When in doubt, the website [pinout.xyz](https://pinout.xyz/) is useful for identifying pins. It gives you the exact layout and role of each pin.

### Circuit Explanation

Here's the circuit diagram used in this tutorial for making the LED blink.

![Circuit diagram showing a Raspberry Pi with a red connector running out of GPIO pin 8 to a 100-ohm* resistor*. The resistor is connected to the long lead of a red LED bulb. Finally, a blue connector connects the short lead of the LED to the ground connection on pin 6 of the Raspberry Pi GPIO pins.](../img/how-to-make-an-LED-blink-with-a-raspberry-pi-using-viam/image1.png)

You can now hook the LED and resistor up to GPIO 14 on pin 8 on your Raspberry Pi. The resistor and LED need to be in series as in the diagram above. To find the right resistor use the resistor color code -- for a 100 ohm resistor, it needs to be brown-black-brown. You can use your multimeter to double-check the resistor value or check yours using the photo below.

![Photo of a 100-ohm resistor with text overlaid that says, in order, brown-black-brown-gold.](../img/how-to-make-an-LED-blink-with-a-raspberry-pi-using-viam/image3.jpg)

When hooking up the circuit, note the *polarity* of the LED. You will notice that the LED has long and short leads. The long lead is the positive side, which is known as the anode, the short lead is the negative side, which is known as the cathode. The long anode should be connected to the resistor and the short cathode should be connected to the ground via the blue jumper wire and pin 6 on the Raspberry Pi as shown on the diagram.

## Configuring your Bot using Viam

Before proceeding, be sure that you have added your Pi to the Viam. Steps on how to do this can be found in the [Adding your Pi to Viam](../../getting-started/installation/#adding-your-pi-on-the-viam-app) section of the Viam Documentation.

Now that we have got that out of the way, let's get back to setting up your robot in Viam. First, go to Viam at [app.viam.com](https://app.viam.com/) on your web browser, and select the robot's config.

![Screenshot of Viam showing the default board configuration on the "components" tab.](../img/how-to-make-an-LED-blink-with-a-raspberry-pi-using-viam/image2.png)

The first component you will add is the **`board`**, which represents your single board computer, which in this case is the Raspberry Pi. This is where you will wire all other components. To create a new component, select **`Create a component`**. For the component **`Type`**, select **`board`**. Then you can name the **`board`** whatever you like as long as you are consistent when referring to it later; we'll name this component **`local`** since it is the **`board`** we will communicate with directly. For **`Model`**, select **`pi`**, then click **`new component`**. Your board component's config will generate the following JSON attributes:

![Screenshot of the Viam App showing the board configuration on the 'config' tab. The board is named "local" and the attributes are shown as empty braces.](../img/how-to-make-an-LED-blink-with-a-raspberry-pi-using-viam/image6.png)

As you add your board component to your robot in Viam, it generates a tab for your board in the Control tab. Here, you can click on "**Get**" to get the current status of your pin. The first time you click "**Get Pin State**", it should return "Pin: 8 is low."![Screenshot of Viam showing the board configuration on the "**Connect**" tab. The "Board Local" row is expanded, and under the "Get" row, the pin is set to "8." A red box is around the "**Get Pin State**" button and the output, which reads, "Pin: 8 is low."](../img/how-to-make-an-LED-blink-with-a-raspberry-pi-using-viam/image5.png)

You can now select "**Set**" to control the status of your pin to "high." It will look like this:

![Screenshot of Viam showing the board configuration on the "Connect" tab. The "Board Local" row is expanded, and under the "Set" row, the pin is set to "8." A red box is around the "Set Pin State" field.](../img/how-to-make-an-LED-blink-with-a-raspberry-pi-using-viam/image8.png)

After setting your pin to "high" the LED should illuminate. You can play around with values "**low**" and "**high**" by setting them differently, and you will see your LED toggle on and off.

![A GIF of the completed project showing a blinking blue LED connected to a Raspberry Pi with jumper cables.](../img/how-to-make-an-LED-blink-with-a-raspberry-pi-using-viam/image7.gif)

## Summary

Congratulations! If you have followed along, you have just successfully used Viam to make an LED blink with a Raspberry Pi! Hopefully, you have learned how the GPIO on a Raspberry PI works, and how to build circuits for LED bulbs. You are ready for your next robotics project. If you are looking for some projects that would be a great next step, we would recommend that you check out the following:

-   [Tutorial List](../../tutorials)

If you want to connect with other developers learning how to build robots, or if you have any issues whatsoever getting Viam set up, let us know on the [Viam Community Slack](http://viamrobotics.slack.com), and we will be happy to help you get up and running.

## Components URL List

<UL>
<li>Raspberry Pi 3 or 4: <a href="https://a.co/d/5Tn67G3" target="_blank">ht<span></span>tps://a.co/d/5Tn67G3</a></li>
<li>Solderless breadboard: <a href="https://amzn.to/2Q4Z5Ta" target="_blank">ht<span></span>tps://amzn.to/2Q4Z5Ta</a></li>
<li>Jumper wires for easy hookup: <a href="http://amzn.to/2qVhd4y" target="_blank">ht<span></span>tp://amzn.to/2qVhd4y</a></li>
<li>Resistor pack: <a href="http://amzn.to/2Dmainw" target="_blank">ht<span></span>tp://amzn.to/2Dmainw</a></li>
<li>Red LED: <a href="http://amzn.to/2Ex2v5q" target="_blank">ht<span></span>tp://amzn.to/2Ex2v5q</a></li>
<li>Multimeter (optional): <a href="http://amzn.to/2qWurxS" target="_blank">ht<span></span>tp://amzn.to/2qWurxS</a></li>
</UL>
