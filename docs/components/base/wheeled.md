---
title: "Configure a Wheeled Base"
linkTitle: "wheeled"
weight: 30
type: "docs"
description: "Configure and wire a wheeled base."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - "/components/base/wheeled/"
# SMEs: Steve B
---

A `wheeled` base supports mobile robotic bases with drive motors on both sides (differential steering).
To configure a `wheeled` base as a component of your robot, first configure the [board](/components/board/) controlling the base and any [motors](/components/motor/) attached to the base.

Configure a `wheeled` base as follows:

{{< tabs name="Configure a Wheeled Base" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `base` type, then select the `wheeled` model.
Enter a name for your arm and click **Create**.

{{< imgproc src="/components/base/wheeled-base-ui-config.png" alt="An example configuration for a wheeled base in the Viam app config builder, with Attributes & Depends On dropdowns and the option to add a frame." resize="600x" >}}

Select the motors attached to the base as your **Right Motors** and **Left Motors**.
Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      ... <INSERT YOUR BOARD COMPONENT CONFIGURATION>
    },
    {
      ... <INSERT YOUR LEFT MOTOR COMPONENT CONFIGURATION>
    },
    {
      ... <INSERT YOUR RIGHT MOTOR COMPONENT CONFIGURATION>
    },
    {
      "name": "<your-base-name>",
      "model": "wheeled",
      "type": "base",
      "namespace": "rdk",
      "attributes": {
        "left": [
          "<your-left-motor-name>" // <INSERT ANY ADDITIONAL LEFT MOTOR NAMES>
        ],
        "right": [
          "<your-right-motor-name>" // <INSERT ANY ADDITIONAL RIGHT MOTOR NAMES>
        ],
        "wheel_circumference_mm": <#>,
        "width_mm": <#>
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json
{
  "components": [
    {
      "name": "my-pi",
      "model": "pi",
      "type": "board",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "rightm",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "pins": {
          "dir": "16",
          "pwm": "15"
        },
        "board": "my-pi"
      },
      "depends_on": []
    },
    {
      "name": "leftm",
      "model": "gpio",
      "type": "motor",
      "namespace": "rdk",
      "attributes": {
        "pins": {
          "dir": "13",
          "pwm": "11"
        },
        "board": "my-pi"
      },
      "depends_on": []
    },
    {
      "name": "my-wheeled-base",
      "model": "wheeled",
      "type": "base",
      "namespace": "rdk",
      "attributes": {
        "width_mm": 195,
        "wheel_circumference_mm": 183,
        "left": ["leftm"],
        "right": ["rightm"]
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{% tab name="Annotated JSON" %}}

{{< imgproc src="/components/base/base-json.png" alt="JSON configuration file for a wheeled base with annotations explaining some of the attributes." resize="600x" >}}

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `wheeled` bases:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `left` | array | **Required** | Array with the `name` of any drive motors on the left side of the base. |
| `right` | array | **Required** | Array with the `name` of any drive motors on the right side of the base. |
| `wheel_circumference_mm` | int | **Required** | The outermost circumference of the drive wheels in millimeters. Used for odometry. Can be an approximation. |
| `width_mm` | int | **Required** | Width of the base in millimeters. In other words, the distance between the approximate centers of the right and left wheels. Can be an approximation. |
| `spin_slip_factor` | float | Optional | Can be used in steering calculations to correct for slippage between the wheels and the floor. If utilized, calibrated by the user. |

## Wire a Wheeled Base

An example wiring diagram for a base with one motor on each side:

![Wiring diagram showing a Raspberry Pi, motor drivers, motors, power supply, and voltage regulator for the rover](/components/base/base-wiring-diagram.png)

Note that your base's wiring will vary depending on your choice of board, motors, motor drivers, and power supply.

## Test the base

{{< readfile "/static/include/components/test-control/base-control.md" >}}
