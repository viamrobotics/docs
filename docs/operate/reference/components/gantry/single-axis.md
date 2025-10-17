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
component_description: "Supports a gantry with a singular linear rail."
toc_hide: true
# SME: Rand, Martha
---

Configure a `single-axis` gantry to integrate a single-axis gantry into your machine.
First, be sure to physically assemble the gantry and connect it to your machine's computer.
Power both on.
Also, configure any [motor components](/operate/reference/components/motor/) that are part of the gantry.
Then, configure the gantry:

{{< tabs >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `gantry` type, then select the `single-axis` model.
Enter a name or use the suggested name for your sensor and click **Create**.

![Creation of a single-axis gantry component.](/components/gantry/single-axis-ui-config.png)

Fill in the attributes as applicable to your gantry, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    // < Your motor config >
    {
      "name": "<your-single-axis-gantry-name>",
      "model": "single-axis",
      "api": "rdk:component:gantry",
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
| Attribute | Type | Required? | Description |
| --------- | ---- | --------- | ----------  |
| `length_mm` | int | **Required** | Length of the axis of the gantry in millimeters. |
| `motor` | string | **Required** | `name` of the [motor](/operate/reference/components/motor/) that moves the gantry's actuator. |
| `board`  |  string | Optional | `name` of the [board](/operate/reference/components/board/) containing the limit switches and pins. If `limit_pins` exist, `board` is required. |
| `limit_pins`  | object | Optional | The `boards`'s pins attached to the limit switches on either end. If the [motor](/operate/reference/components/motor/) used does not include an [encoder](/operate/reference/components/motor/encoded-motor/), `limit_pins` are required to be set. |
| `limit_pin_enabled_high` | boolean | Optional | Whether the limit pins are enabled. <br> Default: `false` |
| `mm_per_rev` | int | **Required** | How far the gantry moves (linear, distance in mm) per one revolution of the motor’s output shaft. This typically corresponds to Distance = PulleyDiameter * pi, or the pitch of a linear screw. |
| `gantry_mm_per_sec` | int | Optional | The speed at which the gantry moves in millimeters per second. Used to calculate the gantry `motor`'s revolutions per minute (RPM). <br> Default: `100` RPM |

{{< readfile "/static/include/components/test-control/gantry-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/gantry.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/gantry/" customTitle="Gantry API" noimage="true" %}}
{{% card link="/operate/modules/configure-modules/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
