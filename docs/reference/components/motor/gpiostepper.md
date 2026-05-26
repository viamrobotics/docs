---
title: "gpiostepper"
linkTitle: "gpiostepper"
weight: 20
type: "docs"
description: "Reference for the gpiostepper motor model. Bipolar stepper motor with current regulation and 1/32 microstepping driven by a basic driver."
images: ["/icons/components/motor.svg"]
aliases:
  - "/operate/reference/components/motor/gpiostepper/"
  - "/components/motor/gpiostepper/"
  - "/reference/components/motor/gpiostepper/"
component_description: "Supports stepper motors driven by basic GPIO-controlled stepper driver chips."
# SMEs: Rand, James
---

The `gpiostepper` model of the motor component supports bipolar [stepper motors](https://en.wikipedia.org/wiki/Stepper_motor) controlled by basic stepper driver chips (such as [DRV8825](https://www.ti.com/product/DRV8825), [A4988](https://www.pololu.com/product/1182), or [TMC2209](https://www.trinamic.com/support/eval-kits/details/tmc2209-bob/)) that take step and direction input through GPIO and move the motor one step per pulse.

{{< alert title="Tip" color="tip" >}}
Viam also supports some more advanced stepper driver chips like the [TMC5072](https://github.com/viam-modules/analog-devices/) that have their own microcontrollers that handle things like speed and acceleration control.
{{< /alert >}}

To use a `gpiostepper` motor as a component of your machine, first wire your motor to a suitable stepper motor driver, which is in turn wired to a board.
Configure the [board](/reference/components/board/) to which the motor driver is wired.

{{< tabs name="gpiostepper-config">}}
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
        "microsteps": <int>,
        "max_rpm": <number>
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
{{< /tabs >}}

The following attributes are available for `gpiostepper` motors:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ---------- |
| `board` | string | **Required** | `name` of the [board](/reference/components/board/) the motor driver is wired to. |
| `pins` | object | **Required** |  A struct containing the [board](/reference/components/board/) {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}} that the `step` and `dir` pins of the motor driver are wired to. |
| `ticks_per_rotation` | int | **Required** | Number of **full** motor steps in one shaft revolution. 200 (equivalent to 1.8 degrees per step) is very common. If your data sheet specifies this in terms of degrees per step, divide 360 by that number to get ticks per rotation. The effective pulses sent per revolution on the `step` pin is `ticks_per_rotation × microsteps`. |
| `microsteps` | int | Optional | Microstep divisor configured on the driver (typically `1`, `2`, `4`, `8`, `16`, or `32`) — should match whatever the driver's `MS1`/`MS2`/`MS3` pins are wired for. Defaults to `1` (full-step). Setting this lets you keep `ticks_per_rotation` at the motor's physical full-step count and have Viam compute the pulse-per-revolution math for you. |
| `max_rpm` | number | Optional | Maximum shaft speed in RPM. Used to cap the step-pin pulse frequency so it stays within what your driver and motor can handle. Required when using the `SetPower` API — a `SetPower(1.0)` runs the motor at `max_rpm`. The internal cap is `max_freq = max_rpm × ticks_per_rotation × microsteps / 60` Hz. |
| `stepper_delay_usec` | int | Optional | **Deprecated** — set `max_rpm` instead. Minimum time in microseconds between consecutive step pulses, which caps the maximum step frequency at `1 / stepper_delay_usec`. Still honored when `max_rpm` is not set, so existing configs keep working. If both `max_rpm` and `stepper_delay_usec` are set, `max_rpm` wins and a deprecation warning is logged. |

Refer to your motor and motor driver data sheets for specifics.

### Microstepping and speed math

The step-pin pulse frequency required to spin the motor at a given RPM is:

```text
freq_Hz = rpm × ticks_per_rotation × microsteps / 60
```

For example, a NEMA 17 (`ticks_per_rotation: 200`) driven in 1/8 microstep mode (`microsteps: 8`) at 60 RPM emits `60 × 200 × 8 / 60 = 1600` pulses per second on the step pin. Setting `max_rpm` caps that frequency: with `max_rpm: 300` on the same motor, the driver will be pulsed at no more than `300 × 200 × 8 / 60 = 8000` Hz, even if a caller requests a higher RPM.

If you are migrating an existing config that already folded microsteps into `ticks_per_rotation` (for example, `ticks_per_rotation: 1600` for a 200-step motor in 1/8 mode), you have two equivalent options:

1. Leave `ticks_per_rotation: 1600` and omit `microsteps` — behaviour is unchanged.
2. Set `ticks_per_rotation: 200` and `microsteps: 8` — clearer to read; identical at runtime.

Do **not** do both at once (`ticks_per_rotation: 1600` _and_ `microsteps: 8`) or you will get 8× the expected speed.

## Wiring example

Typically, a stepper motor will have an even number of wires.
Each pair of wires forms a loop through a coil of the motor.
In the case of a four wire (bi-polar) stepper, one pair of wires may be labeled A1 and A2 and the other B1 and B2.
Refer to your motor data sheet and motor driver data sheet for correct wiring.

The following example uses a Big Tree Tech breakout board with a [TMC2209 integrated circuit](https://www.trinamic.com/products/integrated-circuits/details/tmc2209-la/) to drive a two phase stepper motor.

![An example wiring diagram for a four wire Nema 17 stepper motor driven by a Big Tree Tech TMC2209 stepper driver. The driver is connected to a Raspberry Pi with step and dir pins, as well as logic power wires. A separate 12V power supply is attached to the motor driver to power the motor.](/components/motor/motor-gpiostepper-wiring.png)

In this particular example the enable pin on the upper left corner of the driver is connected to ground to pull it low.
See the data sheet of your stepper motor and stepper motor driver for information on how to wire your specific hardware.
