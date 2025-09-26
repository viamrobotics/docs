---
title: "Configure a GPIO-Controlled Stepper Motor"
linkTitle: "gpiostepper"
weight: 20
type: "docs"
description: "Configure a bipolar stepper motor with current regulation and 1/32 microstepping driven by a basic driver."
images: ["/icons/components/motor.svg"]
aliases:
  - "/components/motor/gpiostepper/"
component_description: "Supports stepper motors driven by basic GPIO-controlled stepper driver chips."
usage: 900000
toc_hide: true
# SMEs: Rand, James
---

The `gpiostepper` model of the motor component supports bipolar [stepper motors](https://en.wikipedia.org/wiki/Stepper_motor) controlled by basic stepper driver chips (such as [DRV8825](https://www.ti.com/product/DRV8825), [A4988](https://www.pololu.com/product/1182), or [TMC2209](https://www.trinamic.com/support/eval-kits/details/tmc2209-bob/)) that take step and direction input through GPIO and move the motor one step per pulse.

{{< alert title="Tip" color="tip" >}}
Viam also supports some more advanced stepper driver chips like the [TMC5072](https://github.com/viam-modules/analog-devices/) that have their own microcontrollers that handle things like speed and acceleration control.
{{< /alert >}}

To use a `gpiostepper` motor as a component of your machine, first wire your motor to a suitable stepper motor driver, which is in turn wired to a board.
Configure the [board](/operate/reference/components/board/) to which the motor driver is wired.
Then configure the motor:

{{< tabs name="gpiostepper-config">}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `motor` type, then select the `gpiostepper` model.
Enter a name or use the suggested name for your motor and click **Create**.

![Screenshot of a gpiostepper motor config with the step and dir pins configured to pins 13 and 15.](/components/motor/gpiostepper-config-ui.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json
{
  "components": [
    {
      "name": "<your-board-name>",
      "model": "<your-board-model>",
      "api": "rdk:component:board",
      "attributes": {},
      "depends_on": [],
    },
    {
      "name": "<your-motor-name>",
      "model": "gpiostepper",
      "api": "rdk:component:motor",
      "attributes": {
        "board": "<your-board-name>",
        "pins": {
          "step": "<pin-number>",
          "dir": "<pin-number>"
        },
        "ticks_per_rotation": <int>,
        "stepper_delay_usec": <int>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

Here’s an example of a basic stepper driver config:

```json
{
  "components": [
    {
      "name": "example-board",
      "model": "pi",
      "api": "rdk:component:board"
    },
    {
      "name": "example-motor",
      "model": "gpiostepper",
      "api": "rdk:component:motor",
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

![motor-gpiostepper-json.](/components/motor/motor-gpiostepper-json.png)

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gpiostepper` motors:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ---------- |
| `board` | string | **Required** | `name` of the [board](/operate/reference/components/board/) the motor driver is wired to. |
| `pins` | object | **Required** |  A struct containing the [board](/operate/reference/components/board/) {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}} that the `step` and `dir` pins of the motor driver are wired to. |
| `ticks_per_rotation` | int | **Required** | Number of full steps in a rotation. 200 (equivalent to 1.8 degrees per step) is very common. If your data sheet specifies this in terms of degrees per step, divide 360 by that number to get ticks per rotation. |
| `stepper_delay_usec` | int | Optional | Time in microseconds to remain high for each step. Required when using the SetPower API. |

Refer to your motor and motor driver data sheets for specifics.

## Wiring example

Typically, a stepper motor will have an even number of wires.
Each pair of wires forms a loop through a coil of the motor.
In the case of a four wire (bi-polar) stepper, one pair of wires may be labeled A1 and A2 and the other B1 and B2.
Refer to your motor data sheet and motor driver data sheet for correct wiring.

The following example uses a Big Tree Tech breakout board with a [TMC2209 integrated circuit](https://www.trinamic.com/products/integrated-circuits/details/tmc2209-la/) to drive a two phase stepper motor.

![An example wiring diagram for a four wire Nema 17 stepper motor driven by a Big Tree Tech TMC2209 stepper driver. The driver is connected to a Raspberry Pi with step and dir pins, as well as logic power wires. A separate 12V power supply is attached to the motor driver to power the motor.](/components/motor/motor-gpiostepper-wiring.png)

In this particular example the enable pin on the upper left corner of the driver is connected to ground to pull it low.
See the data sheet of your stepper motor and stepper motor driver for information on how to wire your specific hardware.

## Test the motor

{{< readfile "/static/include/components/test-control/motor-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/motor.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/motor/" customTitle="Motor API" noimage="true" %}}
{{% card link="/operate/modules/supported-hardware/" noimage="true" %}}
{{< /cards >}}
