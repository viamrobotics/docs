---
title: "Configure a Single-Axis Gantry"
linkTitle: "single-axis"
weight: 70
type: "docs"
description: "Configure a single-axis gantry."
images: ["/icons/components/gantry.svg"]
tags: ["gantry", "components"]
aliases:
    - "/components/gantry/oneaxis/"
# SME: Rand, Martha
---

Configure a `single-axis` gantry to integrate a single-axis gantry into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `gantry`, and select the `single-axis` model.

Click **Create component**.

![Creation of a single-axis gantry component in the Viam app config builder.](/components/gantry/single-axis-ui-config.png)

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
        "mm_per_rev": <int>
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
| `length_mm` | int | **Required** | Length of the axis of the gantry in millimeters. |
| `motor` | string | **Required** | `name` of the [motor](/components/motor/) that moves the gantry's actuator. |
| `board`  |  string | Optional | `name` of the [board](/components/board/) containing the limit switches and pins. If `limit_pins` exist, `board` is required. |
| `limit_pins`  | object | Optional | The pins on the `board` which are attached to the limit switches on either end. If the [motor](/components/motor/) used does not include an [encoder](/components/motor/gpio/encoded-motor/), you must set `limit_pins`.The order of these pins is important, as the gantry may try to travel beyond the limit switch (or switches) if the pins are specified in the wrong order. The switch representing the home (`0`) position must be first in the list. In addition, if you are configuring multiple `single-axis` gantries with `limit_pins`, you can [specify the order of homing routines](#specify-the-order-of-homing-routines) if needed. |
| `limit_pin_enabled_high` | boolean | Optional | Whether the limit pin must be “high” or “low” to be considered “hit”, with a value of `true` representing "high". This attribute is **required** if `limit_pins` is set.<br> Default: `false` |
| `mm_per_rev` | int | **Required** | How far the gantry moves (linear, distance in mm) per one revolution of the motor’s output shaft. This typically corresponds to Distance = PulleyDiameter * pi, or the pitch of a linear screw. |
| `gantry_mm_per_sec` | int | Optional | The speed at which the gantry moves in millimeters per second. Used to calculate the gantry `motor`'s revolutions per minute (RPM). <br> Default: `100` RPM |

## Specify the order of homing routines

When `limit_pins` is set, a `single-axis` gantry component performs a homing routine when `viam-server` starts.
The axis moves towards one limit switch, then the other, before stopping at 80% of the travel of the axis.

If you configure multiple `single-axis` gantries (for example, when using a [`multi-axis` gantry](/components/gantry/multi-axis/)), the order in which these homing routines are executed may be important.
For example, if there is a tool mounted to the z axis gantry that could be damaged during homing of the x or y axes gantries, you would want to ensure that the z axis gantry completes its homing routine first, so that the tool head returns to a safe location before the homing process begins on the other axes.

In this case, you can specify the axes that must be homed first in a `depends_on` array to each `single-axis` gantry.
The example below configures `myFirstGantry` to wait until the homing process for `mySecondGantry` has completed before starting its own:

```json {class="line-numbers linkable-line-numbers"}
{
    "components": [
        // < Your motor config >
        {
            "name": "myFirstGantry",
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
                "depends_on": [
                    "mySecondGantry"
                ]
            }
        },
        // < mySecondGantry config >
    ]
}
```

{{% alert="Note" color="note" %}}
The order of axes in the `subaxes_list` for a [`multi-axis` gantry](/components/gantry/multi-axis/) does not influence the order of homing.
To ensure that homing occurs in a set order, you must add a `depends_on` array specifying the axis or axes to be homed first for each `single-axis` gantry.
{{% /alert %}}
