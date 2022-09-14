---
title: "Servo Component"
linkTitle: "Servo Component"
weight: 80
type: "docs"
description: "Explanation of servo wiring and configuration in Viam."
---

Hobby servos (sometimes called servomotors) are a type of actuator comprising a small motor with built-in closed-loop control.
They are useful for precise positioning, usually limited to a 180 degree range of angles.
Continuous rotation servos are also available that maintain a speed rather than a position.

## Hardware Requirements
A typical servo control setup comprises the following:

- A Raspberry Pi
- A servo
- An appropriate power supply
    - If the servo will not be under any significant load and thus won’t draw much current, you may be able to get away with powering it off 5V (if that’s its required voltage) from the Pi pins.
    However it is advisable to power it directly from a power supply that can meet its peak current needs so as not to inadvertently power cycle the Pi or other components.

!!! note
    Always disconnect devices from power before plugging, unplugging or moving wires or otherwise modifying electrical circuits.

## Mechanism
A servo contains a small electric motor, a series of gears, and a potentiometer attached to the shaft to act as an encoder.
It also contains a closed-loop position control circuit that takes a Pulse Width Modulation [(PWM)](https://en.wikipedia.org/wiki/Pulse-width_modulation)[^pwm] signal input and holds the shaft at a certain angle based on that input.

[^pwm]: Pulse Width Modulation (PWM): [https://en.wikipedia.org/wiki/Pulse-width_modulation](https://en.wikipedia.org/wiki/Pulse-width_modulation)

A typical servo will take PWM pulses ranging from 1ms to 2ms long, and map this range to a 180 degree range of possible positions.
A 1.5ms signal will hold the servo in the middle or “neutral” position, 1ms will move it to 90 degrees from there in one direction, and 2ms will move it 90 degrees from neutral in the opposite direction.

## Wiring
Here's an example of how a servo might be wired to a Raspberry Pi:  

![servo-wiring](../img/servo-wiring.png)

## Viam Configuration

### Required Attributes
In addition to the `name` (of your choosing), `model` ("pi") and `type` ("servo"), you'll need to configure a `pin` to control the servo.
The servo will depend on the board, which must also be configured.

An example configuration file containing the necessary attributes is as follows:  

![servo-JSON](../img/servo-json.png)
[Click here for the raw JSON.](../example-configs/servo-config.json)

### Optional Attributes
Attribute Name | Type | Meaning/Purpose
-------------- | ---- | ---------------
`min` | int | Specifies the minimum angle in degrees to which the servo can move  
`max` | int | Specifies the maximum angle in degrees to which the servo can move

## Implementation
[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/servo/index.html)