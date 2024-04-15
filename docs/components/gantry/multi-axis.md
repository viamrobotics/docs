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
  - "/components/gantry/multi-axis/"
# SME: Rand, Martha
---

Configure a `multi-axis` gantry to integrate a gantry made up of multiple [`single-axis`](/components/gantry/single-axis/) gantries into your machine:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `gantry` type, then select the `multi-axis` model.
Enter a name or use the suggested name for your gantry and click **Create**.

![Creation of a multi-axis gantry component in the Viam app config builder.](/components/gantry/multi-axis-ui-config.png)

Fill in the attributes as applicable to your gantry, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    ... // < INSERT YOUR MOTOR AND SINGLE-AXIS GANTRY CONFIGURATIONS >
    {
      "name": "<your-fake-gantry-name>",
      "model": "multi-axis",
      "type": "gantry",
      "namespace": "rdk",
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
      "model": "pi",
      "type": "board",
      "namespace": "rdk"
    },
    {
      "name": "xmotor",
      "model": "gpiostepper",
      "type": "motor",
      "namespace": "rdk",
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
      "model": "gpiostepper",
      "type": "motor",
      "namespace": "rdk",
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
      "model": "gpiostepper",
      "type": "motor",
      "namespace": "rdk",
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
      "model": "single-axis",
      "type": "gantry",
      "namespace": "rdk",
      "attributes": {
        "length_mm": 1000,
        "board": "local",
        "limit_pin_enabled_high": false,
        "limit_pins": ["32", "36"],
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
      "model": "single-axis",
      "type": "gantry",
      "namespace": "rdk",
      "attributes": {
        "length_mm": 1000,
        "board": "local",
        "limit_pin_enabled_high": false,
        "limit_pins": ["37", "38"],
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
      "model": "single-axis",
      "type": "gantry",
      "namespace": "rdk",
      "attributes": {
        "length_mm": 1000,
        "board": "local",
        "limit_pin_enabled_high": false,
        "limit_pins": ["10", "12"],
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
      "model": "multi-axis",
      "type": "gantry",
      "namespace": "rdk",
      "attributes": {
        "subaxes_list": ["xaxis", "yaxis", "zaxis"],
        "move_simultaneously": "false"
      }
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `multi-axis` gantries:

<!-- prettier-ignore -->
| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------- |
| `subaxes_list` | array | **Required** | An array of the `name` of each of the sub-axes, the [`single-axis`](/components/gantry/single-axis/) gantries that make up the `multi-axis` gantry. |
| `move_simultaneously` | boolean | Optional | A boolean indicating if the sub-axes should move together, or one at a time when `MoveToPosition` is called. <br> Default:  `false` |

{{< readfile "/static/include/components/test-control/gantry-control.md" >}}
