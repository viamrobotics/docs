---
title: "Motor Component"
linkTitle: "Motor"
weight: 70
type: "docs"
description: "Explanation of motor configuration and usage in Viam."
tags: ["motor", "components"]
icon: "img/components/motor.png"
# no_list: true
aliases:
    - /components/motor/
# SME: Rand, Jessamy
---

Electric motors are the most common form of actuator in robotics.
Viam natively supports the following models of motor:

Model | Supported hardware
---------- | ------------------
[`gpio`](#gpio) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor)
[`gpiostepper`](#gpio-stepper) | [Stepper motor](https://en.wikipedia.org/wiki/Stepper_motor) driven by a basic stepper driver
[`TMC5072`](#tmc5072-stepper) | Stepper motor driven by [the TMC5072 chip](https://www.trinamic.com/support/eval-kits/details/tmc5072-bob/)
[`DMC4000`](#dmc4000-stepper) | Stepper motor driven by a [DMC-40x0 series motion controller](https://www.galil.com/motion-controllers/multi-axis/dmc-40x0)
[`fake`](#fake) | Used to test code without hardware

{{% alert title="Note" color="note" %}}
Information on hobby servos (i.e., servomotors) is located in the <a href="../servo">Servo Component Document</a>.
{{% /alert %}}

## GPIO

## GPIO Stepper

## TMC5072 Stepper

## DMC4000 Stepper

## Fake

## Next Steps
