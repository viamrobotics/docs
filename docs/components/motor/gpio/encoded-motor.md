---
title: "Configure a Motor with an Encoder"
linkTitle: "Encoded Motors"
weight: 90
type: "docs"
description: "How to configure an encoded motor."
images: ["/icons/components/motor.svg"]
aliases:
  - "/components/motor/gpio/encoded-motor/"
# SMEs: Rand, James
---

Use an [encoder](/components/encoder/) with a motor to create a closed feedback loop for better control of your machine.
Instead of sending speed or position commands without a way to verify the motor's behavior, the encoder lets the computer know how the motor is actually rotating in the real world, so adjustments can be made to achieve the desired motor movement.

Some motors come with encoders integrated with or attached to them.
You can also add an encoder to a motor.
See the [encoder component documentation](/components/encoder/) for more information on encoders.

Viam supports `gpio` model motors with encoders.
To configure an encoded motor, you must configure the encoder [per the encoder documentation](/components/encoder/) and then configure a `gpio` motor with an `encoder` attribute in addition to the [standard `gpio` model attributes](/components/motor/gpio/).

<a id="encoder-config">
{{< tabs >}}
{{% tab name="Config Builder" %}}

Here’s an example configuration:

![An encoded motor config in the Viam app UI.](/components/motor/encoded-config-ui.png)

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
      "depends_on": []
    },
    {
      "name": "<your-encoder-name>",
      "model": "<your-encoder-model>",
      "type": "encoder",
      "namespace": "rdk",
      "attributes": {
        ... // insert encoder model specific attributes
      },
      "depends_on": []
    },
    {
      "name": "<your-motor-name>",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "board": "<your-board-name>",
        "pins": {
          <...> // insert pins struct
        },
        "encoder": "<your-encoder-name>",
        "ticks_per_rotation": <#>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

Here’s an example configuration:

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
      "name": "myEncoder",
      "model": "incremental",
      "type": "encoder",
      "namespace": "rdk",
      "attributes": {
        "board": "local",
        "pins": {
          "a": "13",
          "b": "15"
        }
      },
      "depends_on": []
    },
    {
      "name": "myMotor1",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "board": "local",
        "pins": {
          "pwm": "16",
          "dir": "18"
        },
        "encoder": "myEncoder",
        "ticks_per_rotation": 9600
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}

{{% tab name="Annotated JSON" %}}

![Same example JSON as on the JSON example tab, with notes alongside it. See attribute table below for all the same information.](/components/motor/motor-encoded-dc-json.png)

{{% /tab %}}
{{< /tabs >}}

In addition to the [attributes for a non-encoded motor](/components/motor/gpio/), the following attributes are available for encoded DC motors:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `encoder` | string | **Required** | `name` of the encoder. |
| `ticks_per_rotation` | int | **Required** | Number of ticks in a full rotation of the encoder and motor shaft. |
| `ramp_rate` | float | Optional | Rate to increase the motor's input voltage (power supply) per second when increasing the speed the motor rotates (RPM). <br> Range = (`0.0`, `1.0`] <br> Default: `0.2` |

{{% alert title="Info" color="info" %}}

The attribute [`max_rpm`](/components/motor/gpio/) is not required or available for encoded `gpio` motors.

{{% /alert %}}

{{% alert title="Important" color="note" %}}

If `encoder` is model [`AM5-AS5048`](/components/encoder/ams-as5048/),`ticks_per_rotation` must be `1`, as `AM5-AS5048` is an absolute encoder which provides angular measurements directly.

{{% /alert %}}

## Wiring Example

Here's an example of an encoded DC motor wired with [the MAX14870 Single Brushed DC Motor Driver Carrier](https://www.pololu.com/product/2961).
This wiring example corresponds to the [example config above](#encoder-config).

![Example wiring diagram with a Raspberry Pi, brushed DC motor, 12V power supply, and Pololu MAX14870 motor driver. The DIR pin of the driver is wired to pin 18 on the Pi. PWM goes to pin 16. The motor's encoder signal wires (out a and out b) go to pins 11 and 13 on the Pi. The motor's main power wires are connected to the motor driver while its encoder logic power wires are connected to the Pi.](/components/motor/motor-encoded-dc-wiring.png)

## Test the motor

Once your motor is configured and connected, go to the [**Control** tab](/fleet/machines/#control) and click on the motor's dropdown panel.
Use the buttons to try turning your motor forwards or backwards at different power levels and check whether it moves as expected.

![Motor control panel.](/components/motor/control.png)

For example, a [Viam Rover](https://docs.viam.com/get-started/try-viam/rover-resources/) with encoded motors following both an [angular](/components/base/#spin) and [linear](/components/base/#movestraight) velocity command:

{{<gif webm_src="/components/encoded-motor/base_moving.webm" mp4_src="/components/encoded-motor/base-moving.mp4" alt="A Viam rover turning in a half circle" max-width="400px" >}}

The position, orientation, and linear and angular velocity of the rover changing as it moves, as measured by a [movement sensor](/components/movement-sensor/):

{{<gif webm_src="/components/encoded-motor/controls_change.webm" mp4_src="/components/encoded-motor/controls_change.mp4" alt="The control tab of a movement sensor on a base with encoded motors as it turns">}}

If the motor does not appear on the **Control** tab, or if you notice unexpected behavior, check your machine's [**Logs** tab](/fleet/machines/#logs) for errors, and review the configuration.
