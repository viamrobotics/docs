---
title: "Base Component"
linkTitle: "Base Component"
weight: 10
type: "docs"
description: "Explanation of base types, configuration, and usage in Viam."
---

Most robots with wheeled bases will comprise at least the following:

-   A `board` component that can run a Viam server instance. 
That is to say, a computing device with general purpose input/output (GPIO) pins such as a Raspberry Pi or other single-board computer with GPIO.

-   Two or more motors with wheels attached

-   A power supply for the board

-   A power supply for the motors

-   Some sort of chassis to hold everything together

For example:
<../img src="/components/img/base-trk-rover-w-arm.png" alt="A base consisting of a rover with motors and single board computer having GPIO pins" />

An example of a wiring diagram for a base that has one motor on each side is shown below.
Note that this will vary greatly depending on choice of motors, motor drivers, power supply, and board.

<i../mg src="/components/img/base-wiring-diagram.png" alt="Wiring diagram showing a Raspberry Pi's connections to the motor drivers, motors, power supply, and voltage regulator for the rover."/>


## Configuration

Configuring a base involves configuring the drive motors and ensuring the base attributes section contains the names of all motors that move the base right or left, respectively.
Configure each motor according to its type. 
You can find more information on wiring and configuring different types of motors under the [Motor Component](../motor/).
The board controlling the base must also be configured.

An example configuration file, including the board, motors, and base:

```json
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
      "depends_on": [
        "follow-pi"
      ],
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
      "depends_on": [
        "follow-pi"
      ],
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
      "depends_on": [
        "rightm",
        "leftm"
      ],
      "model": "wheeled",
      "name": "tread-base",
      "type": "base"
    }
  ]
}
```

An explanatory view of the same config file:
<img src="../img/base-json.png" alt="An image of the JSON configuration file with annotations explaining some of the attributes."/>

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
    <td>string</td>
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
    <td>The outermost circumference of the drive wheels in millimeters.Used for odometry, so try to enter your best approximation of the effective circumference.</td>
  </tr>
  <tr>
    <td><code>width_mm</code></td>
    <td>int</td>
    <td>Width of the base in millimeters. In other words, the distance between the approximate centers of the right and left wheels.</td>
  </tr>
  <tr>
    <td><code>depends_on</code></td>
    <td>array of strings</td>
    <td>List the names of the right and left motors again. This is so the code will find the motors before it attempts to register the base, avoiding errors.</td>
  </tr>

</tbody>
</table>

### Optional Attributes

`spin_slip_factor` (float): Used in steering calculations to correct for slippage between the wheels and the floor.
To be calibrated by the user.

## Implementation

[Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/base/index.html)
