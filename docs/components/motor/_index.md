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

Electric motors are the most common form of [actuator](https://en.wikipedia.org/wiki/Actuator) in robotics.
The Viam *motor* component type natively supports the following models of motor:

Model | Supported hardware <a name="model-table"></a>
---------- | ------------------
[`gpio`](#gpio) | [Standard brushed or brushless DC motor](https://en.wikipedia.org/wiki/DC_motor)
[`gpiostepper`](#gpio-stepper) | [Stepper motor](https://en.wikipedia.org/wiki/Stepper_motor) driven by a basic stepper driver
[`TMC5072`](#tmc5072-stepper) | Stepper motor driven by [the TMC5072 chip](https://www.trinamic.com/support/eval-kits/details/tmc5072-bob/)
[`DMC4000`](#dmc4000-stepper) | Stepper motor driven by a [DMC-40x0 series motion controller](https://www.galil.com/motion-controllers/multi-axis/dmc-40x0)
[`fake`](#fake) | Used to test code without hardware

As is evident in the table above, how you configure your motor with Viam depends more on the [motor driver](https://www.wellpcb.com/what-is-motor-driver.html) than on the motor itself.

This document assumes you have motor, compatible motor driver, and power supply.
You'll also need a [board](/components/board/) to send signals to the motor driver[^dmcboard].

## Configuration

To configure a motor as a component of your robot, first configure the [board](/components/board/) to which the motor driver is wired[^dmcboard].

Configure your motor with the universal component fields:

Field | Description
----- | -----------
`name` | Choose a name to identify the motor.
`type` | `motor` is the type for all motor components.
`model` | Depends on the motor driver; see the list of models in the [table above](#model-table).

<br>

```json
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "<board model>",
      "attributes": {},
      "depends_on": [],
      
    },
    {
      "name": "example-gpio",
      "type": "motor",
      "model": "<model, e.g. 'gpio'>",
      "attributes": {
        "<ATTRIBUTES VARY DEPENDING ON MOTOR MODEL; SEE BELOW>"
        "board": "local"
      },
      "depends_on": []
    }
  ]
}
```

## GPIO

An example configuration for a `gpio` motor:

{{< tabs name="gpio-config">}}
{{% tab name="Builder UI" %}}

<img src="/components/img/motor/gpio-config.png" alt="Screenshot of a gpio motor config with the In1 and In2 pins configured and the PWM pin field left blank." max-width="100px" >

{{% /tab %}}
{{% tab name="Raw JSON" %}}

```json
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "pi",
      "attributes": {},
      "depends_on": [],
      
    },
    {
      "name": "example-gpio",
      "type": "motor",
      "model": "gpio",
      "attributes": {
        {
          "pins": {
            "a": "11",
            "b": "13",
            "pwm": "",
          },
        "board": "local",
        "max_rpm": 120
        }
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

### Pins

There are three common ways for the computing device to communicate with a brushed DC motor driver chip.
The driver data sheet will specify which one to use.

- PWM/DIR: One digital input (such as a GPIO pin) sends a [pulse width modulation (PWM)](https://en.wikipedia.org/wiki/Pulse-width_modulation) signal to the driver to control speed while another digital input sends a high or low signal to control the direction.
- In1/In2 (or A/B): One digital input is set to high and another set to low turns the motor in one direction and vice versa, while speed is controlled via PWM through one or both pins.
- In1/In2 + PWM: Three pins: an In1 (A) and In2 (B) to control direction and a separate PWM pin to control speed.

{{% alert title="Note" color="note" %}}

The PWM pin does not have to be configured for motor drivers that use only In1 and In2, and not a third PWM pin.

{{% /alert %}}

## GPIO Stepper

## TMC5072 Stepper

## DMC4000 Stepper

This is a highly featured motion controller that, unlike the other motor models listed, does not require a board component.

## Fake

## Next Steps

[^dmcboard]: The `DMC4000` model does not require a board.
