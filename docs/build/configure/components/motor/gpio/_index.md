---
title: "Configure a gpio motor"
linkTitle: "gpio"
weight: 10
type: "docs"
description: "Configure brushed or brushless DC motors."
images: ["/icons/components/motor.svg"]
aliases:
  - "/components/motor/gpio/"
# SMEs: Rand, James
---

The `gpio` model supports [DC motors](https://en.wikipedia.org/wiki/DC_motor) (both brushed and brushless).

[Encoders](/build/configure/components/encoder/) can be configured to work with `gpio` motors.
Find more information in the [encoded motor documentation](/build/configure/components/motor/gpio/encoded-motor/).

To configure a DC motor as a component of your robot, first configure the [board](/build/configure/components/board/) to which the motor driver is wired.
Then add your motor:

{{< tabs name="gpio-config">}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `motor` type, then select the `gpio` model.
Enter a name for your motor and click **Create**.

![G P I O motor config in the builder UI with the In1 and In2 pins configured and the PWM pin field left blank.](/build/configure/components/motor/gpio-config-ui.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json
{
  "components": [
    {
      "name": "<your-board-name>",
      "model": "<your-board-model>",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": [],
    },
    {
      "name": "<your-motor-name>",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "pins": {
          <...>
        },
        "board": "<your-board-name>",
        "max_rpm": <int>,
        "min_power_pct": <float>,
        "max_power_pct": <float>,
        "pwm_freq": <float>,
        "dir_flip": <float>,
        "en_low": <float>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

An example configuration for a `gpio` motor:

```json
{
  "components": [
    {
      "name": "local",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "example-gpio",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "pins": {
          "dir": "36",
          "pwm": "32"
        },
        "board": "local",
        "max_rpm": 500
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Annotated JSON" %}}

![Same example JSON as on the JSON example tab, with notes alongside it. See attribute table below for all the same information.](/build/configure/components/motor/motor-gpio-json.png)

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `gpio` motors:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `board` | string | **Required** | `name` of the [board](/build/configure/components/board/) to which the motor driver is wired. |
| `max_rpm` | int | **Required** | This is an estimate of the maximum RPM the motor will run at with full power under no load. The [`GoFor`](/build/configure/components/motor/#gofor) method calculates how much power to send to the motor as a percentage of `max_rpm`. If unknown, you can set it to 100, which will mean that giving 40 as the `rpm` argument to `GoFor` or `GoTo` will set it to 40% speed. ***Not required** or available for [encoded](/build/configure/components/motor/gpio/encoded-motor/) `gpio` motors.* |
| `pins` | object | **Required** | A structure that holds pin configuration information; [see below](#pins). |
| `min_power_pct` | number | Optional | Sets a limit on minimum power percentage sent to the motor. <br> Default: `0.0` |
| `max_power_pct` | number | Optional | Range is 0.06 to 1.0; sets a limit on maximum power percentage sent to the motor. <br> Default: `1.0` |
| `pwm_freq` | int | Optional | Sets the PWM pulse frequency in Hz. Many motors operate optimally in the kHz range. <br> Default: `800` |
| `dir_flip` | bool | Optional | Flips the direction of "forward" versus "backward" rotation. Default: `false` |
| `en_high` / `en_low` | string | Optional | Some drivers have optional enable pins that enable or disable the driver chip. If your chip requires a high signal to be enabled, add `en_high` with the pin number to the pins section. If you need a low signal use `en_low`. |
| `encoder` | string | Optional | The name of an encoder attached to this motor. See [encoded motor](/build/configure/components/motor/gpio/encoded-motor/). |

Refer to your motor and motor driver data sheets for specifics.

## `pins`

There are three common ways for your computer to communicate with a brushed DC motor driver chip.
**Your motor driver data sheet will specify which one to use.**

- PWM/DIR: Use this if one of your motor driver's pins (labeled "PWM") takes a [pulse width modulation (PWM)](https://en.wikipedia.org/wiki/Pulse-width_modulation) signal to the driver to control speed while another pin labeled "DIR" takes a high or low signal to control the direction.
  - Configure `pwm` and `dir`.
- In1/In2: Use this if your motor driver has pins labeled "IN1" and "IN2" or "A" and "B," or similar.
  One digital signal set to a high voltage and another set to a low voltage turns the motor in one direction and vice versa.
  Speed is controlled with PWM through one or both pins.
  - Configure `a` and `b`.
- In1/In2 and PWM: Use this if your motor driver uses three pins: In1 (A) and In2 (B) to control direction and a separate PWM pin to control speed.
  - Configure `a`, `b`, and `pwm`.

Inside the `pins` struct you need to configure **two or three** of the following, depending on your motor driver:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `a` | string | **Required** for some drivers | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's "IN1" or "A" pin is wired to. |
| `b` | string | **Required** for some drivers | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's "IN2" or "B" pin is wired to. |
| `dir` | string | **Required** for some drivers | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's direction ("DIR") pin is wired to. |
| `pwm` | string | **Required** for some drivers | Board {{< glossary_tooltip term_id="pin-number" text="pin number" >}} this motor driver's "PWM" pin is wired to. |

{{% alert title="Important" color="note" %}}

Only two or three of these `pins` attributes are required, depending on your motor driver.

If your motor drivers uses only In1 and In2, and not a third PWM pin, **do not configure a `pwm` pin**.

{{% /alert %}}

## Wiring examples

{{% alert title="Tip" color="tip" %}}

The following are just examples and do not apply to all motor setups.
Refer to your motor and motor driver data sheets for information on power requirements and how to properly wire your motor.

{{% /alert %}}

### Brushed DC motor

Taking a 12V brushed DC motor controlled by a [DRV8256E Single Brushed DC Motor Driver Carrier](https://www.pololu.com/product/4038) wired to a Raspberry Pi as an example, the wiring diagram would look like this:

![An example wiring diagram showing a Raspberry Pi, 12V power supply, DRV8256E motor driver, and 12V brushed DC motor. The logic side of the driver is connected to the Pi's ground and 3.3V pins. The driver pin for PWM goes to pin 32 on the Pi and the direction pin goes to pin 36 on the Pi. The motor side of the motor driver is connected to the ground and 12V terminals of a power supply and the OUT1 and OUT2 pins go to the two terminals of the motor.](/build/configure/components/motor/motor-brushed-dc-wiring.png)

The signal wires in the diagram run from two GPIO pins on the Pi to the DIR and PWM pins on the motor driver.
Refer to a [Raspberry Pi pinout schematic](https://pinout.xyz/) to locate generic GPIO pins and determine their pin numbers for configuration.

### Brushless DC motor

Brushless DC motor drivers work in much the same way as brushed DC motor drivers.
They typically require a PWM/DIR input or an A/B (In1/In2) and PWM input to set the motor power and direction.
The key difference between a brushed and brushless motor driver is on the motor output side.
Brushless motors typically have three power connections (commonly referred to as A, B and C; or sometimes Phase 1, 2 and 3) and 3 sensor connections (commonly referred to as Hall A, Hall B, and Hall C) running between the motor and driver.

The configuration file of a BLDC motor with Viam is the same as that of a brushed motor.
Only the output side of the driver board is different in that more wires connect the driver to the motor.

![An example wiring diagram showing a Raspberry Pi, 12V power supply, RioRand 400W brushless DC motor controller, and 3 phase 12V brushless DC motor. The motor has three power wires (one for each phase) and five sensor wires (two to power the sensor and one for each of the three Hall effect sensors).](/build/configure/components/motor/motor-brushless-dc-wiring.png)

{{< readfile "/static/include/components/test-control/motor-control.md" >}}

## Next steps
