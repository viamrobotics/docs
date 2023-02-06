---
title: "Configure a motor with an encoder"
linkTitle: "Encoded Motors"
weight: 90
type: "docs"
description: "How to configure an encoded motor."
# SMEs: Rand, James
---

Some motors come with encoders integrated with or attached to them.
Other times, you may add an encoder to a motor.
See the [encoder component documentation](/components/encoder/) for more information on encoders.

Viam supports motors with encoders within model `gpio`.
Configuration of an encoder requires configuring the encoder [per the encoder documentation](/components/encoder) in addition to the [standard `gpio` model attributes](/components/motor/gpio/).

Here’s an example configuration:

{{< tabs name="encoder-config">}}
{{% tab name="Builder UI" %}}

<img src="../../img/motor/encoded-config-ui.png" alt="Screenshot of an encoded motor config in the Viam app UI." style="max-width:800px;width:100%" >

{{% /tab %}}
{{% tab name="Raw JSON" %}}

```json
{
  "components": [
    {
      "name": "local",
      "type": "board",
      "model": "pi",
      "attributes": {}
    },
    {
      "name": "myEncoder",
      "type": "encoder",
      "model": "incremental",
      "attributes": {
        "board": "local",
        "pins": {
          "a": "13",
          "b": "15"
        }
      }
    },
    {
      "name": "myMotor1",
      "type": "motor",
      "model": "gpio",
      "attributes": {
        "board": "local",
        "max_rpm": 500,
        "pins": {
          "pwm": "16",
          "dir": "18"
        },
        "encoder": "myEncoder",
        "ticks_per_rotation": 9600
      }
    }
  ]
}
```

{{% /tab %}}

{{% tab name="Annotated JSON" %}}

![motor-encoded-dc-json](../../img/motor/motor-encoded-dc-json.png)
{{% /tab %}}
{{< /tabs >}}

#### Required Attributes

In addition to the required [attributes for a non-encoded motor](/components/motor/gpio/#required-attributes), encoded DC motors require the following:

Name | Type | Description
-------------- | ---- | ---------------
`encoder` | string | Should match name of the encoder you configure as an `encoder` component.
`ticks_per_rotation` | string | Number of ticks in a full rotation of the encoder (and motor shaft).

`max_rpm` does *not* apply to encoded `gpio` motors.

#### Optional Attributes

In addition to the optional attributes listed in the [non-encoded DC motor section](/components/motor/gpio/#optional-attributes), encoded motors have the following additional options:

Name | Type | Description
-------------- | ---- | ---------------
`ramp_rate` | float | How fast to ramp power to motor when using RPM control. 0.01 ramps very slowly; 1 ramps instantaneously. Range is (0, 1]. Default is 0.2.

## Wiring Example

Here's an example of an encoded DC motor wired with [the MAX14870 Single Brushed DC Motor Driver Carrier](https://www.pololu.com/product/2961).
This wiring example corresponds to the [example config above](#encoder-config).

![motor-encoded-dc-wiring](../../img/motor/motor-encoded-dc-wiring.png)
