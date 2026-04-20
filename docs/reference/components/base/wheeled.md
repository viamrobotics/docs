---
title: "wheeled"
linkTitle: "wheeled"
weight: 30
type: "docs"
description: "Reference for the wheeled base model. And wire a wheeled base."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - "/components/base/wheeled/"
  - "/reference/components/base/wheeled/"
component_description: "Supports mobile wheeled robotic bases with motors on both sides for differential steering."
# SMEs: Steve B
---

A `wheeled` base supports mobile robotic bases with motors on both sides (differential steering).
To configure a `wheeled` base as a component of your machine, first configure the [board](/reference/components/board/) controlling the base and any [motors](/reference/components/motor/) attached to the base.

If you want to test your base as you configure it, physically assemble the base, connect it to your machine's computer, and turn it on.

{{< tabs name="Configure a Wheeled Base" >}}
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
      "api": "rdk:component:base",
      "attributes": {
        "left": [
          "<your-left-motor-name>" // <INSERT ANY ADDITIONAL LEFT MOTOR NAMES>
        ],
        "right": [
          "<your-right-motor-name>" // <INSERT ANY ADDITIONAL RIGHT MOTOR NAMES>
        ],
        "wheel_circumference_mm": <int>,
        "width_mm": <int>
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
      "api": "rdk:component:board",
      "attributes": {},
      "depends_on": []
    },
    {
      "name": "rightm",
      "model": "gpio",
      "api": "rdk:component:motor",
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
      "api": "rdk:component:motor",
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
      "api": "rdk:component:base",
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
{{< /tabs >}}

The following attributes are available for `wheeled` bases:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `left` | array | **Required** | Array with the `name` of any drive motors on the left side of the base. |
| `right` | array | **Required** | Array with the `name` of any drive motors on the right side of the base. |
| `wheel_circumference_mm` | int | **Required** | The outermost circumference of the drive wheels in millimeters. Used for odometry. Can be an approximation. |
| `width_mm` | int | **Required** | Width of the base in millimeters. In other words, the distance between the approximate centers of the right and left wheels. Can be an approximation. |
| `spin_slip_factor` | float | Optional | Can be used in steering calculations to correct for slippage between the wheels and the floor. If used, calibrated by the user. |

## Wire a `wheeled` base

An example wiring diagram for a base with one motor on each side:

![Wiring diagram showing a Raspberry Pi, motor drivers, motors, power supply, and voltage regulator for the rover](/components/base/base-wiring-diagram.png)

Note that your base's wiring will vary depending on your choice of board, motors, motor drivers, and power supply.
