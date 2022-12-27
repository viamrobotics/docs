---
title: "Base Component"
linkTitle: "Base"
weight: 10
type: "docs"
description: "Explanation of base configuration, and usage in Viam."
tags: ["base", "components"]
# SMEs: Steve B
---

Most robots with wheeled bases will comprise at least the following:

-   A [board component](/components/board/) that can run a viam-server instance. 
That is to say, a computing device with general purpose input/output (GPIO) pins such as a Raspberry Pi or other single-board computer with GPIO.

-   Two or more motors with wheels attached

-   A power supply for the board

-   A power supply for the motors

-   Some sort of chassis to hold everything together

For example:

<img src="../img/base/base-trk-rover-w-arm.png" alt="A robot comprised of a base (motors, wheels and chassis) as well as some other components. The wheels are highlighted to indicate that they are part of the concept of a 'base', while the non-base components are not highlighted. There are width and diameter labels on the diagram because width and circumference (pi times diameter) are required attributes when configuring a base component." />

An example of a wiring diagram for a base that has one motor on each side is shown below.
Note that this will vary greatly depending on choice of motors, motor drivers, power supply, and board.

<img src="../img/base/base-wiring-diagram.png" alt="Wiring diagram showing a Raspberry Pi, motor drivers, motors, power supply, and voltage regulator for the rover."/>


## Configuration

Configuring a base involves configuring the drive motors and ensuring the base attributes section contains the names of all motors that move the base right or left, respectively.
Configure each motor according to its type. 
You can find more information on wiring and configuring different types of motors in the [motor topic](../motor/).
The [board](/components/board/) controlling the base must also be configured.

An example configuration file, including the board, motors, and base:

{{< tabs name="Example Servo Config" >}}
{{% tab name="Raw JSON" %}}

```json-viam
{
  "components": [
    {
      "attributes": {},
      "model": "pi",
      "name": "follow-pi",
      "type": "board"
    },
    {
      "attributes": {
        "board": "follow-pi",
        "max_rpm": 300,
        "pins": {
          "dir": "16",
          "pwm": "15"
        }
      },
      "model": "gpio",
      "name": "rightm",
      "type": "motor"
    },
    {
      "attributes": {
        "board": "follow-pi",
        "max_rpm": 300,
        "pins": {
          "dir": "13",
          "pwm": "11"
        }
      },
      "model": "gpio",
      "name": "leftm",
      "type": "motor"
    },
    {
      "attributes": {
        "left": [
          "leftm"
        ],
        "right": [
          "rightm"
        ],
        "wheel_circumference_mm": 183,
        "width_mm": 195
      },
      "model": "wheeled",
      "name": "tread-base",
      "type": "base"
    }
  ]
}
```

{{% /tab %}}
{{< tab name="Annotated JSON" >}}

<img src="../img/base/base-json.png" alt="An image of the JSON configuration file with annotations explaining some of the attributes."/>

{{< /tab >}}
{{< /tabs >}}

### Required Attributes
<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><code>type</code></td>
    <td>string</td>
    <td>Use "base" for any base component</td>
  </tr>
  <tr>
    <td><code>model</code></td>
    <td>string</td>
    <td>Select "wheeled" unless you have a "boat".</td>
  </tr>
  <tr>
    <td><code>name</code></td>
    <td>string</td>
    <td>Name your base.</td>
  </tr>
  <tr>
    <td><code>left</code></td>
    <td>array of strings</td>
    <td>List with the names of all drive motors on the left side of the base. There may be one or more motors.</td>
  </tr>
  <tr>
    <td><code>right</code></td>
    <td>array of strings</td>
    <td>List with the names of all drive motors on the right side of the base. There may be one or more motors.</td>
  </tr>
  <tr>
    <td><code>wheel_circumference_mm</code></td>
    <td>int</td>
    <td>The outermost circumference (not diameter!) of the drive wheels in millimeters. Used for odometry, so try to enter your best approximation of the effective circumference.</td>
  </tr>
  <tr>
    <td><code>width_mm</code></td>
    <td>int</td>
    <td>Width of the base in millimeters. In other words, the distance between the approximate centers of the right and left wheels.</td>
  </tr>

</tbody>
</table>

### Optional Attributes

`spin_slip_factor` (float): Used in steering calculations to correct for slippage between the wheels and the floor.
To be calibrated by the user.

## Implementation

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/base/index.html)
