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
# SME: Rand
---

Configure a `single-axis` gantry to integrate a one-axis gantry into your robot:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your sensor, select the type `gantry`, and select the `single-axis` model.

Click **Create component**.

{{< imgproc src="/components/gantry/single-axis-ui-config.png" alt="Creation of a single-axis gantry component in the Viam app config builder." resize="1000x" >}}

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
| `length_mm` | int | **Required** | Length of the axis of the gantry in millimeters. |
| `motor` | string | **Required** | `name` of the [motor](/components/motor/) that moves the gantry's actuator. |
| `axis` | object | **Required** | The translational axis for the gantry. Must be exactly one of `x`, `y`, or `z`. |
| `board`  |  Optional | string | `name` of the [board](/components/board/) containing the limit switches and pins. If `limit_pins` exist, `board` is required. |
| `limit_pins`  | Optional | object | The `boards`'s pins attached to the limit switches on either end. If the [motor](/components/motor/) used does not include an [encoder](/components/motor/gpio/encoded-motor/), `limit_pins` are required to be set. |
| `limit_pin_enabled_high` | boolean | Optional | Whether the limit pins are enabled. <br> Default: `false` |
| `mm_per_rev` | int | Optional | How far the gantry moves (linear, distance in mm) per one revolution of the motor’s output shaft. This typically corresponds to Distance = PulleyDiameter * pi, or the pitch of a linear screw. |
| `gantry_rpm` | int | Optional | The gantry `motor`'s default revolutions per minute (RPM). |
