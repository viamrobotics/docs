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

![Creation of a multi-axis gantry component in the Viam app config builder.](../img/multiaxis-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    // < Your motor & oneaxis gantry configs >
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
                    "dir": "11",
                    "pwm": "13",
                    "step": "15"
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
                    "dir": "16",
                    "pwm": "18",
                    "step": "22"
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
                    "dir": "29",
                    "pwm": "31",
                    "step": "33"
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
                    "32",
                    "36"
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
                    "37",
                    "38"
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
                    "10",
                    "12"
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
            "name": "my_multiaxis_gantry",
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
