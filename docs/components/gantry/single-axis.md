---
title: "Configure a Single-Axis Gantry"
linkTitle: "single-axis"
weight: 70
type: "docs"
description: "Configure a single-axis gantry."
images: ["/components/img/components/gantry.svg"]
tags: ["gantry", "components"]
aliases:
    - "/components/gantry/oneaxis/"
# SME: Rand
---

Configure a `single-axis` gantry to integrate a one-axis gantry into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `gantry`, and select the `single-axis` model.

Click **Create component**.

![Creation of a single-axis gantry component in the Viam app config builder.](../img/single-axis-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    // < Your motor config >
    {
      "name": "<your-single-axis-gantry-name>",
      "type": "gantry",
      "model": "single-axis",
      "attributes": {
        "motor": "<your-motor-name>",
        "length_mm": <int>,
        "axis": {
          "X": <int>,
          "Y": <int>,
          "Z": <int>
        }
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

The following attributes are available for `single-axis` gantries:

| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------  |
| `length_mm` | int | **Required** | The length of the axis of the gantry in millimeters. |
| `motor` | string | **Required** | The `name` of the [motor](/components/motor/) that moves the gantry's actuator. |
| `axis` | object | **Required** | The translational axis for the gantry. Must be exactly one of `x`, `y`, or `z`. |
| `board`  |  string | Optional | The `name` of the [board](/components/board/) containing the limit switches and pins. If `limit_pins` exist, `board` is required. |
| `limit_pins`  | object | Optional | The `boards`'s pins attached to the limit switches on either end. If the [motor](/components/motor/) used does not include an [encoder](/components/motor/gpio/encoded-motor/), you must set `limit_pins`. The order of these pins is important. If the pins are in the wrong order, the gantry may try to travel beyond the limit switch (or switches). The switch representing the home (`0`) position must be first in the list. See [Configure `limit_pins`](#configure-limit_pins) for more information. |
| `limit_pin_enabled_high` | boolean | Optional | Whether the limit pin must be “high” or “low” to be considered “hit”, with a value of `true` representing "high". This attribute is **Required** if `limit_pins` is set.<br> Default: `false` |
| `mm_per_rev` | int | Optional | How far the gantry moves (linear, distance in mm) per one revolution of the motor’s output shaft. This typically corresponds to Distance = PulleyDiameter * pi, or the pitch of a linear screw. |
| `gantry_rpm` | int | Optional | The gantry `motor`'s default revolutions per minute (RPM). |

## Configure `limit_pins`

When `viam-server` starts, a `single-axis` gantry component will perform a homing routine if its `limit_pins` attribute is set. The axis will move towards one limit switch, then the other, before stopping at 80% of the travel of the axis.

If there are multiple `single-axis` gantries configured (for example, when using a [`multi-axis` gantry](/components/gantry/multi-axis/)), the order of homing may be important.

In this case, you must specify the axes that must be homed first in a `depends_on` array to each `single-axis` gantry. For example, if there is a tool mounted to the z axis that could be damaged during homing of the x or y axes, you must add the z axis as a dependency to the x and y axes. This will ensure the z axis completes its homing routine first, and that the tool head is in a safe location to begin the homing process on the other axes.

{{% alert="Note" color="note" %}}
The order of axes in the `subaxes_list` for a `multi-axis` gantry does not influence the order of homing. A `multi-axis` gantry component is not constructed until all the `single-axis` gantry components are constructed and finish homing. Thus to ensure that homing occurs in a proscribed order, you must explicitly add dependencies to each axis for axes that must be homed first.
{{% /alert %}}

The following shows an example of adding an explicit dependency, where the `mySecondGantry`, along the y axis, is configured to always be homed before the `myFirstGantry`, along the x axis:

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    // < Your motor config >
    {
      "name": "myFirstGantry",
      "type": "gantry",
      "model": "single-axis",
      "attributes": {
        "motor": "xmotor",
        "length_mm": 1000,
        "axis": {
          "X": 1,
          "Y": 0,
          "Z": 0
        },
        "limit_pin_enabled_high": false,
        "limit_pins": [
            "32",
            "36"
        ]
      },
      "depends_on": [
        "mySecondGantry"
      ],
    }
    {
      "name": "mySecondGantry",
      "type": "gantry",
      "model": "single-axis",
      "attributes": {
        "motor": "ymotor",
        "length_mm": 1000,
        "axis": {
          "X": 0,
          "Y": 1,
          "Z": 0
        },
        "limit_pin_enabled_high": false,
        "limit_pins": [
            "37",
            "38"
        ]
      }
    }
  ]
}
```
