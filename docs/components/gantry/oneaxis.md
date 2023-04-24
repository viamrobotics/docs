---
title: "Configure a One-Axis Gantry"
linkTitle: "oneaxis"
weight: 70
type: "docs"
description: "Configure a oneaxis gantry."
tags: ["gantry", "components"]
# SME: Rand
---

Configure a `oneaxis` gantry to integrate a one-axis gantry into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `gantry`, and select the `oneaxis` model.

Click **Create component**.

![Creation of a one-axis gantry component in the Viam app config builder.](../img/oneaxis-ui-config.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    // < Your motor config >
    {
      "name": <"your-oneaxis-gantry-name">,
      "type": "gantry",
      "model": "oneaxis",
      "attributes": {
        "motor": <"your-motor-name">,
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

The following attributes are available for `oneaxis` gantries:

| Attribute | Inclusion | Description |
| ----------- | -------------- | --------------  |
| `length_mm` | **Required** | Length of the axis of the gantry in millimeters. |
| `motor` | **Required** | `name` of the [motor](/components/motor) that moves the gantry's actuator. |
| `axis` | **Required** | The translational axis for the gantry. Must be exactly one of x, y, or z. |
| `board`  |  Optional | `name` of the [board](/components/board) containing the limit switches and pins. If `limit_pins` exist, `board` is required. |
| `limit_pins`  | Optional | The `boards`'s pins attached to the limit switches on either end. If the [motor](/components/motor) used does not include an [encoder](/motor/gpio/encoded-motor), `limit_pins` are required to be set. |
| `limit_pin_enabled_high` | Optional | Whether the limit pins are enabled. <br> Default: `false` |
| `mm_per_rev` | Optional | How far the gantry moves (linear, distance in mm) per one revolution of the motor’s output shaft. This typically corresponds to Distance = PulleyDiameter*pi, or the pitch of a linear screw. |
| `gantry_rpm` | Optional | The gantry `motor`'s default revolutions per minute (RPM). |
