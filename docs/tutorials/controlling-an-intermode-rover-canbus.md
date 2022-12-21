---
title: "Controlling an Intermode Rover with Canbus and Viam"
linkTitle: "Controlling an Intermode Rover with Canbus"
weight: 60
type: "docs"
description: "Integrate an Intermode rover as a modular resource base component via CAN bus"
# SME: Matt Vella, Matt Dannenberg, James Otting
---

## Introduction

The Viam platform comes with a component called [base](/components/base/), which adds some very useful abstractions for simplified control of mobile robots.
Instead of controlling individual motors, the base component allows you to [do things](https://python.viam.dev/autoapi/viam/components/base/index.html#package-contents”) like “drive straight”, “spin”, “set velocity” and “stop”.  

Many robotic rovers can be controlled out-of-the-box with the Viam **wheeled** base model - simply by specifying how your motorized wheels are configured.
But what if you want to control a rover or other mobile robot that does not expose direct motor control?
This tutorial will show you how to create a modular resource (custom component), which can then be controlled seamlessly with the rest of your robot (sensors, etc) through the [Viam SDK](/product-overviews/sdk-as-client/) of your choice.

<img src="../img/intermode/rover_outside.png"  style="float:left;margin-right:12px" alt="Intermode rover pictured outdoors." title="Intermode rover pictured outdoors." width="400" />

While the concepts covered here are applicable to other hardware, we’ll specifically be showing you how to use Viam to control the <a href="https://www.intermode.io/" target="_blank">Intermode rover</a>.
This is a powerful pairing: **Intermode** aims to make the hardware aspects of a mobile robot-based business simple and worry-free, while Viam simplifies the software aspects of any robotics business.

The Intermode rover uses the [Can bus](https://en.wikipedia.org/wiki/CAN_bus) protocol, a robust and prevalent vehicle communication standard (in fact, probably most vehicles you’ve ever been in use it!).
This tutorial will show how we can both leverage this protocol and abstract it into the Viam base interface so that the rover can then be controlled securely from anywhere with the programming language of your choice.

## What You’ll Need for This Tutorial

{{% alert title="Note" color="note"%}}
Even if you are not in possession of an Intermode rover, many of the other concepts presented here may be relevant to your robotic project(s).  
While this tutorial can be followed verbatim for the Intermode rover, much of it can be applied to other **base**, **Can bus**, or modular resource-based projects.
{{% /alert %}}

You will need the following hardware to complete this project:

* [Raspberry Pi with microSD card](https://a.co/d/bxEdcAT), with viam-server installed per [our Raspberry Pi setup guide](https://docs.viam.com/getting-started/rpi-setup/).
* [An Intermode rover](https://www.intermode.io/)
* [PiCAN 2 - Canbus interface for Raspberry Pi](https://copperhilltech.com/pican-2-can-bus-interface-for-raspberry-pi/)
* [12V to 5V Buck Converter](https://www.amazon.com/dp/B01M03288J)
* [USB-C Male Plug to  Pigtail Cable](https://www.amazon.com/Type-C-Cable-10inch-22AWG-Pigtail/dp/B09C7SLHFP)

## Initial Setup

### Raspberry Pi software setup

You'll want to first [follow these instructions](https://docs.viam.com/installation/rpi-setup/) to set up Viam Server on your Raspberry Pi and configure (for now) an empty robot configuration.

Next, you'll install the PiCAN 2 driver software [following these instructions](https://copperhilltech.com/blog/pican2-pican3-and-picanm-driver-installation-for-raspberry-pi/)

### Hardware

Now, power your Raspberry Pi off and attach the PiCAN 2 by aligning the 40 way connector and fitting to the top of the Pi using a spacer and screw as per the instructions [here](https://copperhilltech.com/pican2-controller-area-network-can-interface-for-raspberry-pi/).

<img src="../img/intermode/can_terminal_conn.png"  style="float:right;margin-right:12px" alt="PiCAN Terminal Wiring." title="PiCAN Terminal Wiring." width="400" />

Next, with the Intermode rover powered down, use the Intermode provided 6-wire amphenol connector to wire into 4 screw terminal on PiCAN bus.
Connect one of the 12v wires (red) to the +12V terminal, one of the ground wires (black) to the GND terminal, the CAN low wire (blue) to the CAN_L terminal, and the CAN high wire (white) to the CAN_H terminal.
You will have two remaining wires (12v and ground).

Now, connect the remaining two wires to the + (red) and - (black) **input** terminals on your buck converter.  Now, attach the USB-C adaptor to the **output** of your buck converter, and plug this into your Pi.  Powering up the Intermode should now power up your Pi and allow it to communicate with the rover via CAN bus!

<img src="../img/intermode/intermode_wiring.jpg"  style="margin-right:12px" alt="Intermode, Pi Wiring." title="Intermode, Pi Wiring." width="800" />


## Creating the base modular resource 

Viam includes API interfaces for a number of common components within Viam Server (otherwise known as the RDK - Robot Development Kit).
The Viam component that exposes the interfaces for controlling a mobile robot is the [base](/components/base) component.

For the Intermode rover , we'll want to conform to the base **API** interface, but create a new **model** with its own implementation of each method.
Both the **API** interface and **model** are namespaced as a triplet in Viam.
Since we are conforming to an existing Viam API for **base**, the **API** namespace we'll use is: 

_rdk:component:base_

Since we're creating this base model for tutorial purposes only, we'll use the following **model** namespace:

_viamlabs::tutorial::intermode_
