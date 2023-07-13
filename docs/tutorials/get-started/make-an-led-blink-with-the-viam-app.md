---
title: "Control an LED with a Raspberry Pi Using the Viam App"
linkTitle: "Control an LED with the Viam App"
weight: 30
type: "docs"
description: "Intro to Hardware Programming Part 1: Use the Viam app to make an LED turn on and off with a Raspberry Pi."
webmSrc: "/img/blink.webm"
mp4Src: "/img/blink.mp4"
videoAlt: "A blinking L.E.D. connected to a Raspberry Pi"
images: ["/img/blink.gif"]
aliases:
    - /tutorials/make-an-led-blink-with-the-viam-app/
tags: ["board", "raspberry pi", "app"]
authors: []
languages: []
viamresources: [ "board" ]
level: "Beginner"
date: "4 October 2022"
cost: 70
---

In this post, we will show you how to use Viam to make an LED blink with a Raspberry Pi.
This tutorial is a great place to start if you have never built a robot or a circuit before.

{{<gif webm_src="/tutorials/img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image9.webm" mp4_src="/tutorials/img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image9.mp4" alt="A GIF of the completed project showing a blinking blue LED connected to a Raspberry Pi with jumper cables." max-width="300px">}}

## What you'll need for this guide

You will need the following to complete the project:

### Hardware

- [Raspberry Pi 3 or 4](https://a.co/d/5Tn67G3)
  - Refer to the [Viam Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/) to set up your Pi.
- [Solderless breadboard](https://amzn.to/2Q4Z5Ta)
- [Jumper wires](https://amzn.to/2qVhd4y)
- [Resistor pack](https://amzn.to/2Dmainw)
  - You will be using a 100 Ohm resistor, which is the resistor with brown-black-brown bands
- [LED](https://amzn.to/2Ex2v5q)

### Software

- [viam-server](/installation/#install-viam-server)

## Project setup

Before you proceed with building your circuit, you are going to need to set up the operating system on your Raspberry Pi and install `viam-server` on the Pi.
We recommend that you follow along with the [Installing `viam-server` on Raspberry Pi](/installation/prepare/rpi-setup/) guide in the Viam documentation.
Be sure to follow all the steps including [adding your Pi on the Viam app.](/installation/#install-viam-server).

{{< snippet "social.md" >}}

## Building the circuit

The first step in this project is to design a simple LED circuit.
Then you will make the LED circuit controllable from the Raspberry Pi by connecting the circuit to the *general purpose input/output* (GPIO) pins on the Raspberry Pi.

A simple LED circuit consists of a LED and resistor.
The resistor is used to limit the current that is being drawn and is called a *current-limiting resistor*.

### GPIO Pinout

*General-purpose input/output* (GPIO) is a digital signal [pin](https://en.wikipedia.org/wiki/Pin_(electronics)) on a circuit board, like a Raspberry Pi, which may be used as an input or output, or both, and is controllable by software.

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image10.png" alt="Photo showing a Raspberry Pi 4 with a white box around the GPIO pins on the Pi and big red letters that say, 'GPIO Pins.'" width="100%">

As you may have guessed, **each pin has a specific role, and you can use it only for that role**.
Some of them are input/output, power (3.3V or 5V), or ground.
As you can see in the diagram below, there are 40 output pins on the Pi.
You can program 26 of the GPIO pins.

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image4.jpg" alt="Diagram showing all of the GPIO pins on a Raspberry Pi 4 and their corresponding pin number and function." width="100%">

One thing to note that might be confusing with the pin numbering on Raspberry Pis: There are 40 physical pins numbered from 1 to 40.
That is *board pin numbering*, corresponding to the pin's physical location on the board.
When working with the GPIO pins with Viam, you will use the board numbers.
For example, Pin 1 can be located pretty easily, since Pin 1 is always the pin whose corner is rounded.

Then there's numbering them by function or GPIO connection.
These are the big numbers, like "GPIO 22".
These numbers are helpful for understanding the function of each pin.

When in doubt, the website [pinout.xyz](https://pinout.xyz/) is useful for identifying pins.
It gives you the exact layout and role of each pin.

### Circuit explanation

Here's the circuit diagram used in this tutorial for making the LED blink.

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image1.png" alt="Circuit diagram showing a Raspberry Pi with a red connector running out of GPIO pin 8 to a 100-ohm resistor. The resistor is connected to the long lead of a red LED bulb. Finally, a blue connector connects the short lead of the LED to the ground connection on pin 6 of the Raspberry Pi GPIO pins." width="100%">

You can now hook the LED and resistor up to GPIO 14 (or pin 8) on your Raspberry Pi.
The resistor and LED need to be in series as in the diagram above.
To find the right resistor use the resistor color code -- for a 100 ohm resistor, it needs to be brown-black-brown.
You can use your multimeter to double-check the resistor value or check yours using the photo below.

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image3.jpg" alt="Photo of a 100-ohm resistor with text overlaid that says, in order, brown-black-brown-gold." width="50%">

When hooking up the circuit, note the *polarity* of the LED.
You will notice that the LED has long and short leads.
The long lead is the positive side, which is known as the anode, the short lead is the negative side, which is known as the cathode.
The long anode should be connected to the resistor and the short cathode should be connected to the ground using the blue jumper wire and pin 6 on the Raspberry Pi as shown on the diagram.

## Configuring your bot using the Viam app

Before proceeding, be sure that you have connected your Pi to the Viam app.
Steps on how to do this can be found in the [Adding your Pi on the Viam App](/installation/#install-viam-server) section of the Viam Documentation.

Now that we have gotten that out of the way, let's get back to configuring your robot's components.
First, go to the Viam app at [app.viam.com](https://app.viam.com/) on your web browser, and select the robot's **Config** tab.

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image2.png" alt="Screenshot of the Viam app showing the Create Component field on the Components subtab of the Config tab." width="100%">

You will add a [*board component*](/components/board/) to represent your single board computer, which in this case is the Raspberry Pi.
You'll create the new component in the **Create Component** panel.
Name the board whatever you like as long as you are consistent when referring to it later; we'll name it "local" since it is the board we will communicate with directly.
For the component **Type**, select **`board`**.
For **Model**, select **`pi`**, then click **`Create Component`**.
Your board component pane will look like this:

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image6.png" alt="Screenshot of the Viam app showing the board configuration on the Config tab. The board is named 'local' and the attributes are shown as empty braces." width="100%">

Click **Save Config** at the bottom of the screen.

As you add your board component to your robot in the Viam app, it generates a panel for your board in the **Control** tab.
Here, you can click on **Get** to get the current status of your pin.
The first time you click **Get Pin State**, it should return "Pin: 8 is low."

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image5.png" alt="Screenshot of the Viam app showing the board configuration on the Control tab. The 'Board Local' row is expanded, and under the 'Get' row, the pin is set to '8.' A red box is around the 'Get Pin State' button and the output, which reads, 'Pin: 8 is low.'" width="100%">

You can now select **Set** to control the status of your pin to **high**.
It will look like this:

<img src="../../img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image8.png" alt="Screenshot of the Viam app showing the board configuration on the Control tab. The 'Board Local' row is expanded, and under the 'Set' row, the pin is set to '8.' A red box is around the 'Set Pin State' field." width="100%">

After setting your pin to **high** the LED should illuminate.
You can play around with values **low** and **high** by setting them differently, and you will see your LED toggle on and off depending on whether you have the value set to **low** or **high**.

{{<gif webm_src="/tutorials/img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image7.webm" mp4_src="/tutorials/img/make-an-led-blink-with-a-raspberry-pi-and-the-viam-app/image7.mp4" alt="A GIF of the completed project showing a blinking blue LED connected to a Raspberry Pi with jumper cables." max-width="300px">}}

{{< alert title="Tip" color="tip" >}}
The above image blinks at regular intervals, while yours will turn on and off when you set the values to **high** and **low** respectively.
To make your LED blink at regular intervals, see [How to Make an LED Blink with a Raspberry Pi and the Viam SDK](/tutorials/get-started/make-an-led-blink-with-a-raspberry-pi-and-sdk/).
{{< /alert >}}

## Summary

Congratulations!
If you have followed along, you have just successfully used Viam to make an LED blink with a Raspberry Pi!
You have learned how the GPIO on a Raspberry Pi works, and how to build circuits for LED bulbs.

## Next Steps

Check out the next part in this series to control your LED programmatically:

{{< cards >}}
  {{% card link="/tutorials/get-started/make-an-led-blink-with-a-raspberry-pi-and-sdk/" %}}
{{< /cards >}}
