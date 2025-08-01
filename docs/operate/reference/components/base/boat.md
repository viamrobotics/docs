---
title: "Configure a Boat Base"
linkTitle: "boat"
weight: 35
type: "docs"
draft: "true"
description: "Configure a boat base."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - "/components/base/boat/"
toc_hide: true
# SMEs: Eliot
---

A `boat` base is a model for a mobile robotic boat.
To configure a `boat` base as a component of your machine, first configure the [board](/operate/reference/components/board/) controlling the base and any [motors](/operate/reference/components/motor/) attached to the base.

{{< tabs name="Configure a Boat Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `base` type, then select the `boat` model.
Enter a name or use the suggested name for your base and click **Create**.

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "base",
      "model": "boat",
      "api": "rdk:component:base",
      "attributes": {
        "drive_mode": "<a_drive_mode_option>",
        "serial_path": "</dev/ttyXXXX>"
      },
      "depends_on": []
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `boat` bases:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `length_mm` | int | **Required** | Length of the base in millimeters. In other words, the distance between the approximate centers of the right and left wheels. Can be an approximation. |
| `width_mm` | int | **Required** | Width of the base in millimeters. In other words, the distance between the approximate centers of the right and left motors. Can be an approximation. |
| `IMU` | string | **Required** | Name of the [Inertial Measurement Unit](/dev/reference/apis/components/movement-sensor/#imu-configuration) in the boat. |
| `Motors` | string[] | **Required** | JSON struct containing the configuration attributes for each motor attached to the boat. |

Each [motor](/operate/reference/components/motor/) inside of `Motors` has the following attributes available:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `Name` | string | **Required** | Name of the motor. |
| `x_offset_mm` | int | **Required** | |
| `y_offset_mm` | int | **Required** | |
| `angle_degs` | int | **Required** | |
| `Weight` | int | **Required** | |

## Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}

## Troubleshooting

{{< readfile "/static/include/components/troubleshoot/base.md" >}}

## Next steps

For more configuration and usage info, see:

{{< cards >}}
{{% card link="/dev/reference/apis/components/base/" customTitle="Base API" noimage="true" %}}
{{% card link="/tutorials/configure/configure-rover/" noimage="true" %}}
{{% card link="/tutorials/control/drive-rover/" noimage="true" %}}
{{< /cards >}}
