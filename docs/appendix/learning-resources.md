---
title: "Learning Resources"
linkTitle: "Learning Resources"
description: "A collection of links to external sources discussing robotics topics and basic information that we believe users may find helpful."
type: "docs"
draft: true
---

## Overview

The following sections contain links that we think you will find useful during your journey into robotics.

## Basic Electronics

### Hobby Servos

Hobby servos are a type of actuator comprising a small motor with built-in closed-loop control.
They are useful for precise positioning, usually limited to a 180 degree range of angles.
Continuous rotation servos are also available that maintain a speed rather than a position.

#### Mechanism

Hobby servos contain a small electric motor, a series of gears, and a potentiometer attached to the shaft to act as an encoder.
It also contains a closed-loop position control circuit that takes a [Pulse Width Modulation (PWM)](https://en.wikipedia.org/wiki/Pulse-width_modulation) signal input and holds the shaft at a certain angle based on that input.

A typical servo will take PWM pulses ranging from 1ms to 2ms long, and map this range to a 180 degree range of possible positions.
A 1.5ms signal will hold the servo in the middle or "neutral" position, 1ms will move it to 90 degrees from there in one direction, and 2ms will move it 90 degrees from neutral in the opposite direction.
Note that some servos have a different PWM range, mapping to a different set of angles.

#### Hardware Requirements

Unlike [motors](/build/configure/components/motor/), servos do not require a motor driver chip.

A typical servo control setup comprises the following:

- A Raspberry Pi (or other [board](/build/configure/components/board/))
- A servo
- An appropriate power supply
  - If the servo will not be under any significant load and thus won’t draw much current, you may be able to get away with powering it off 5V (if that’s its required voltage) from the Pi pins.
    However it is advisable to power it directly from a power supply that can meet its peak current needs so as not to inadvertently power cycle the Pi or other components.

#### Wiring

{{% alert title="Caution" color="caution" %}}
Always disconnect devices from power before plugging, unplugging or moving wires or otherwise modifying electrical circuits.
{{% /alert %}}

Here's an example of how a servo might be wired to a Raspberry Pi:

![A diagram showing the signal wire of a servo connected to pin 16 on a Raspberry Pi. The servo's power wires are connected to a 4.8V power supply.](/build/configure/components/servo/servo-wiring.png)

### Resistors

[Online Resistor Color Code Calculator](https://goodcalculators.com/resistor-color-code-calculator/) - Enter the desired resistor value in Ohms, kOhms, or MOhms, and press enter and this site displays the color bands for that resistor value.

#### Resistor Value Chart

![Chart of standard colors to values for electronic components. An example resistor with green, red, and orange bands is shown. The value is 52 times 10 to the third power, or 52,000 Ohms.](/internals/vector/resistor.png)

You can easily learn resistor color markings without referring to a chart by remembering this jingle:

"Badly Burnt Resistors On Your Ground Bus Void General Warranty."

Now, equate the jingle to the colors in this order:
Black, Brown, Red, Orange, Yellow, Green, Blue, Violet, Gray, White

And their values on a resistor:
0, 1, 2, 3, 4, 5, 6, 7, 8, 9

- The bands 1 and 2 indicate the first two significant digits on a resistor.
- Band 3 is a multiplier on four-band resistors.
  For example, a resistor with brown, green, orange bands representing, 1, 5, and 3, respectively, which equates to 15 times ten to the third, or 15,000 Ohms, or 15 kOhms.
- On resistors with four bands, the band 4 indicates tolerance, with gold being +/- 5% and silver being +/- 10%.
- On five-band resistors, band 3 becomes an additional significant digit, band 4 becomes the multiplier, and band 5 becomes the tolerance band.
- Six-band resistors are read identically to five-band resistors, their difference being that the sixth band indicates the resistor's temperature coefficient.

### LEDs (Light-Emitting Diodes)

Light-emitting diodes come in a variety of form factors:
![Image of various Light Emitting Diode form factors.](/internals/vector/verschiedene-leds.jpg)
LEDs commonly have two leads, although specialty LEDs are available that are capable of simultaneously displaying two colors or of displaying a blended shade. These specialty LEDs have 4-6 leads and 2-4 LED junctions.

LEDs work by applying a voltage with a positive and negative polarity to the leads in such a manner that the positive voltage is attached to the anode of the LED and the negative voltage lead is attached to the LED's cathode. On a two-pin LED, the longer pin is the anode and the short pin is the cathode.

LEDs require current-limiting resistors to avoid destroying the LED junction during an over-current situation. Always include a current-limiting resistor in basic LED circuits. The following schematic illustrates this circuit:

![This image displays a schematic showing the arrangement of a DC voltage source with the positive lead to the LED's anode, the LED's cathode connected to a one end of a current-limiting resistor and the other end of the voltage drop resistor connected to the negative lead of the voltage source, completing the circuit.](/internals/vector/led-circuit2.png)
