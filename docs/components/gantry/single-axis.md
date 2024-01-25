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
  - "/components/gantry/single-axis/"
# SME: Rand, Martha
---

Configure a `single-axis` gantry to integrate a single-axis gantry into your machine.
Before configuring the gantry, configure any [motor components](/components/motor/) that are part of the gantry.

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `gantry` type, then select the `single-axis` model.
Enter a name for your sensor and click **Create**.

![Creation of a single-axis gantry component in the Viam app config builder.](/components/gantry/single-axis-ui-config.png)

Copy and paste the following attribute template into your gantry's **Attributes** box.
Then remove and fill in the attributes as applicable to your gantry, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "motor": "<your-motor-name>",
  "length_mm": <int>,
  "mm_per_rev": <int>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "motor": "my-motor",
  "length_mm": 98,
  "mm_per_rev": 20
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    // < Your motor config >
    {
      "name": "<your-single-axis-gantry-name>",
      "model": "single-axis",
      "type": "gantry",
      "namespace": "rdk",
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

<!-- prettier-ignore -->
| Attribute | Type | Inclusion | Description |
| --------- | ---- | --------- | ----------  |
| `length_mm` | int | **Required** | Length of the axis of the gantry in millimeters. |
| `motor` | string | **Required** | `name` of the [motor](/components/motor/) that moves the gantry's actuator. |
| `board`  |  string | Optional | `name` of the [board](/components/board/) containing the limit switches and pins. If `limit_pins` exist, `board` is required. |
| `limit_pins`  | object | Optional | The `boards`'s pins attached to the limit switches on either end. If the [motor](/components/motor/) used does not include an [encoder](/components/motor/gpio/encoded-motor/), `limit_pins` are required to be set. |
| `limit_pin_enabled_high` | boolean | Optional | Whether the limit pins are enabled. <br> Default: `false` |
| `mm_per_rev` | int | **Required** | How far the gantry moves (linear, distance in mm) per one revolution of the motor’s output shaft. This typically corresponds to Distance = PulleyDiameter * pi, or the pitch of a linear screw. |
| `gantry_mm_per_sec` | int | Optional | The speed at which the gantry moves in millimeters per second. Used to calculate the gantry `motor`'s revolutions per minute (RPM). <br> Default: `100` RPM |

{{< readfile "/static/include/components/test-control/gantry-control.md" >}}
