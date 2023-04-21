---
title: "Configure a Multi-Axis Gantry"
linkTitle: "multiaxis"
weight: 80
type: "docs"
description: "Configure a multiaxis gantry."
tags: ["gantry", "components"]
# SME: Rand
---

Configure a `multiaxis` gantry to integrate a multi-axis gantry into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your gantry, select the type `gantry`, and select the `multiaxis` model.

Click **Create component**.
Paste into the **Attributes** box:

``` json
"attributes": {
    "subaxes_list": [
        <"xaxis-name">,
        <"yaxis-name">,
        <"zaxis-name">
    ]
}
```

![Creation of a multi-axis gantry component in the Viam app config builder.](../img/multiaxis-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    // your motor & oneaxis gantry configs
    {
        "name": <"your-fake-gantry-name">,
        "type": "gantry",
        "model": "multiaxis",
        "attributes": {
            "subaxes_list": [
                <"xaxis-name">,
                <"yaxis-name">,
                <"zaxis-name">
            ]
        },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "components": [
        {
            "name": "local",
            "type": "board",
            "model": "pi"
        },
        {
            "name": "xmotor",
            "type": "motor",
            "model": "gpiostepper",
            "attributes": {
                "board": "local",
                "pins": {
                    "dir": "dirx",
                    "pwm": "pwmx",
                    "step": "stepx"
                },
                "stepperDelay": 50,
                "ticksPerRotation": 200
            }
        },
        {
            "name": "ymotor",
            "type": "motor",
            "model": "gpiostepper",
            "attributes": {
                "board": "local",
                "pins": {
                    "dir": "diry",
                    "pwm": "pwmy",
                    "step": "stepy"
                },
                "stepperDelay": 50,
                "ticksPerRotation": 200
            }
        },
        {
            "name": "zmotor",
            "type": "motor",
            "model": "gpiostepper",
            "attributes": {
                "board": "local",
                "pins": {
                    "dir": "dirz",
                    "pwm": "pwmz",
                    "step": "stepz"
                },
                "stepperDelay": 50,
                "ticksPerRotation": 200
            }
        },
        {
            "name": "xaxis",
            "type": "gantry",
            "model": "oneaxis",
            "attributes": {
                "length_mm": 1000,
                "board": "local",
                "limit_pin_enabled_high": false,
                "limit_pins": [
                    "xlim1",
                    "xlim2"
                ],
                "motor": "xmotor",
                "gantry_rpm": 500,
                "axis": {
                    "x": 1,
                    "y": 0,
                    "z": 0
                }
            }
        },
        {
            "name": "yaxis",
            "type": "gantry",
            "model": "oneaxis",
            "attributes": {
                "length_mm": 1000,
                "board": "local",
                "limit_pin_enabled_high": false,
                "limit_pins": [
                    "ylim1",
                    "ylim2"
                ],
                "motor": "ymotor",
                "gantry_rpm": 500,
                "axis": {
                    "x": 0,
                    "y": 1,
                    "z": 0
                }
            }
        },
        {
            "name": "zaxis",
            "type": "gantry",
            "model": "oneaxis",
            "attributes": {
                "length_mm": 1000,
                "board": "local",
                "limit_pin_enabled_high": false,
                "limit_pins": [
                    "zlim1",
                    "zlim2"
                ],
                "motor": "zmotor",
                "gantry_rpm": 500,
                "axis": {
                    "x": 0,
                    "y": 0,
                    "z": 1
                }
            },
            "frame": {
                "parent": "world",
                "orientation": {
                    "type": "euler_angles",
                    "value": {
                        "roll": 0,
                        "pitch": 40,
                        "yaw": 0
                    }
                },
                "translation": {
                    "x": 0,
                    "y": 3,
                    "z": 0
                }
            }
        },
        {
            "name": "test",
            "type": "gantry",
            "model": "multiaxis",
            "attributes": {
                "subaxes_list": [
                    "xaxis",
                    "yaxis",
                    "zaxis"
                ]
            }
        }
    ]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `multiaxis` gantries:

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `subaxes_list`  | **Required** | An array of the `name`s of the sub-axes, the [one-axis](/components/gantry/oneaxis) gantries that make up the multi-axis gantry. |
