---
title: "Configure a Multi-Axis Gantry"
linkTitle: "multi-axis"
weight: 80
type: "docs"
description: "Configure a multi-axis gantry."
images: ["/icons/components/gantry.svg"]
tags: ["gantry", "components"]
aliases:
    - "/components/gantry/multiaxis/"
# SME: Rand, Martha
---

Configure a `multi-axis` gantry to integrate a multi-axis gantry into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `gantry` type, then select the `multi-axis` model.
Enter a name for your gantry and click **Create**.

![Creation of a multi-axis gantry component in the Viam app config builder.](/components/gantry/multi-axis-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    ... // < INSERT YOUR MOTOR AND SINGLE-AXIS GANTRY CONFIGURATIONS >
    {
        "name": "<your-fake-gantry-name>",
        "type": "gantry",
        "model": "multi-axis",
        "attributes": {
            "subaxes_list": [
                "<xaxis-name>",
                "<yaxis-name>",
                "<zaxis-name>"
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
            "model": "single-axis",
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
            "model": "single-axis",
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
            "model": "single-axis",
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
            "name": "my_multi-axis_gantry",
            "type": "gantry",
            "model": "multi-axis",
            "attributes": {
                "subaxes_list": [
                    "xaxis",
                    "yaxis",
                    "zaxis"
                ],
                "move_simultaneously": "false"
            }
        }
    ]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `multi-axis` gantries:

| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------- |
| `subaxes_list` | array | **Required** | An array of the `name` of each of the sub-axes, the [`single-axis`](/components/gantry/single-axis/) gantries that make up the `multi-axis` gantry. |
| `move_simultaneously` | boolean | Optional | A boolean indicating if the sub-axes should move together, or one at a time when `MoveToPosition` is called. <br> Default:  `false` |
