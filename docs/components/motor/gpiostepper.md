---
title: "Configure a gpiostepper motor"
linkTitle: "gpiostepper"
weight: 20
type: "docs"
description: "Configure a stepper motor with a basic driver."
# SMEs: Rand, James
---

The Viam `gpiostepper` model of motor component supports [stepper motors](https://en.wikipedia.org/wiki/Stepper_motor) controlled by basic stepper driver chips (such as [DRV8825](https://www.ti.com/product/DRV8825) or [TMC2209](https://www.trinamic.com/support/eval-kits/details/tmc2209-bob/)) that take step and direction input via GPIO and simply move the motor one step per pulse.

Viam also supports some more advanced stepper driver chips ([TMC5072](../tmc5072/), [DMC4000](../dmc4000/)) that have their own microcontrollers that handle things like speed and acceleration control.
Refer to those docs for more information.

## Configuration

To configure a `gpiostepper` as a component of your robot, first configure the [board](/components/board/) to which the motor driver is wired.

Then assign your motor a `name` (to identify the motor), `type` (`motor`) and `model` (`gpiostepper`), and fill in the [attributes](#required-attributes) that apply to your particular hardware.
Refer to your motor and motor driver data sheets for specifics.

Here’s an example of a basic stepper driver config:

{{< tabs name="gpiostepper-config">}}
{{% tab name="Config Builder" %}}

<img src="../../img/motor/gpiostepper-config-ui.png" alt="Screenshot of a gpiostepper motor config with the step and dir pins configured to pins 13 and 15, respectively." style="max-width:800px;width:100%" >

{{% /tab %}}
{{% tab name="Raw JSON" %}}

```json
{
  "components": [
    {
      "name": "example-board",
      "type": "board",
      "model": "pi"
    },
    {
      "name": "example-motor",
      "type": "motor",
      "model": "gpiostepper",
      "attributes": {
        "board": "example-board",
        "pins": {
          "step": "13",
          "dir": "15"
        },
        "ticks_per_rotation": 200
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Annotated JSON" %}}

![motor-gpiostepper-json](../../img/motor/motor-gpiostepper-json.png)

{{% /tab %}}
{{< /tabs >}}

### Required Attributes

Name | Type | Description
-------------- | ---- | ---------------
`board` | string | Should match name of board to which the motor driver is wired.
`pins` | object | A structure containing "step" and "dir" pin numbers; see example JSON above.
`ticks_per_rotation` | integer | Number of full steps in a rotation. 200 (equivalent to 1.8 degrees per step) is very common. If your data sheet specifies this in terms of degrees per step, divide 360 by that number to get ticks per rotation.

### Optional Attributes

Name | Type | Description
-------------- | ---- | ---------------
`stepper_delay` | uint | Time in microseconds to remain high for each step. Default is 20.

### Wiring Example

Typically, a stepper motor will have an even number of wires.
Each pair of wires forms a loop through a coil of the motor.
In the case of a four wire (bi-polar) stepper, one pair of wires may be labeled A1 and A2 and the other B1 and B2.
Refer to your motor data sheet and motor driver data sheet for correct wiring.

The following example uses a Big Tree Tech breakout board with a [TMC2209 integrated circuit](https://www.trinamic.com/products/integrated-circuits/details/tmc2209-la/) to drive a two phase stepper motor.

![An example wiring diagram for a four wire Nema 17 stepper motor driven by a Big Tree Tech TMC2209 stepper driver. The driver is connected to a Raspberry Pi with step and dir pins, as well as logic power wires. A separate 12V power supply is attached to the motor driver to power the motor.](../../img/motor/motor-gpiostepper-wiring.png)

In this particular example the enable pin on the upper left corner of the driver is connected to ground to pull it low.
See the data sheet of your stepper motor and stepper motor driver for information on how to wire your specific hardware.
