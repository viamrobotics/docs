---
title: "Configure a `fake` motor"
linkTitle: "fake"
weight: 70
type: "docs"
description: "How to configure a motor with model `fake`"
# SMEs: Rand, James
---

To configure a `fake` motor as a component of your robot, you don't need any hardware, and you don't need to configure any attributes.

Just configure your `fake` motor with the universal component fields:

Field | Description
----- | -----------
`name` | Choose a name to identify the motor.
`type` | `motor` is the type for all motor components.
`model` | Depends on the motor driver; see the list of models in the [table above](#model-table).

{{< tabs name="fake-config">}}
{{% tab name="Builder UI" %}}

<img src="/components/img/motor/fake-config-ui.png" alt="Screenshot of a gpio motor config with the In1 and In2 pins configured and the PWM pin field left blank." style="max-width:800px;width:100%" >

{{% /tab %}}
{{% tab name="Raw JSON" %}}

```json
{
  "components": [
    {
      "name": "fake-motor",
      "type": "motor",
      "model": "fake",
      "attributes": {
        "pins": {
          "dir": "",
          "pwm": ""
        },
        "board": "",
        "direction_flip": false
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}
