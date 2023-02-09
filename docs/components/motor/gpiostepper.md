---
title: "Configure a `gpiostepper` motor"
linkTitle: "gpiostepper"
weight: 20
type: "docs"
description: "How to configure a motor with model `gpiostepper`"
# SMEs: Rand, James
---

The Viam `gpiostepper` model of motor component supports [stepper motors](https://en.wikipedia.org/wiki/Stepper_motor) controlled by basic stepper driver chips that take step and direction input via GPIO and simply move the motor one step per pulse.

Viam also supports some more advanced stepper driver chips ([TMC5072](/components/motor/tmc5072/), [DMC4000](/components/motor/dmc4000/)) that have their own microcontrollers that handle things like speed and acceleration control.
Refer to those docs for more information.

Here’s an example of a basic stepper driver config:

{{< tabs name="gpiostepper-config">}}
{{% tab name="Builder UI" %}}

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
`ticks_per_rotation` | integer | Number of full steps in a rotation. 200 (equivalent to 1.8 degrees per step) is very common.

### Optional Attributes

Name | Type | Description
-------------- | ---- | ---------------
`stepper_delay` | uint | Time in microseconds to remain high for each step. Default is 20.

### Wiring Example

![motor-gpiostepper-wiring](../../img/motor/motor-gpiostepper-wiring.png)
