---
title: "Configure a wheeledodometry movement sensor"
linkTitle: "wheeledodometry"
type: "docs"
description: "Configure a wheeledodometry movement sensor."
images: ["/icons/components/imu.svg"]
tags: ["movement sensor", "components", "movement sensor"]
# SMEs: Rand, Martha
---

Configure a `wheeledodometry` movement sensor to implement _wheeled odometry_ on your robot.

_Wheeled odometry_ is the estimation of position, orientation, linear velocity, and angular velocity using the dimensions of a base.
This model uses [encoders](/components/encoder/) to get an odometry estimate from an encoder wheeled base.

## Set-up requirements

To prepare your robot, attach [encoders](/components/encoder/) to each the motors of your base to measure their rotation.

- Configure each of these encoded motors [as encoder components](/components/encoder/#configuration).
- Then, proceed to [configure](#configuration) a `wheeledodometry` movement sensor with the name of each of the encoder components.

## Configuration

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Select **Raw JSON** mode.
Copy and paste the following:

```json {class="line-numbers linkable-line-numbers"}
"name" : "<your-wheeledodometry-movement-sensor-name>",
"type" : "movement_sensor",
"model" : "wheeledodometry",
"attributes" : {
    "base" : "<your-base-name>",
    "left_motors" : ["<your-base-left-motor-name-1>", "<your-base-left-motor-name-2>"],
    "right_motors" : ["<your-base-right-motor-name-1", "your-base-right-motor-name-2>"],
    "time-interval-msec": <number>
}
```

Fill in and edit the attributes as applicable.

## Attributes

The following attributes are available for `wheeledodometry` movement sensors:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `base` | string | **Required** | The `name` of the [base](/components/base/) to which the encoders making up this movement sensor are wired. |
| `left_motors` | object | **Required** | A struct holding the name of each of the bases' left [encoded motors](/components/encoder/). |
| `right_motors` | object | **Required** | A struct holding the name of each of the bases' right [encoded motors](/components/encoder/). |
| `time_interval_msec` | number | Optional | The time in between each wheeled odometry calculation. <br> Default: `500.0` </br> |

With a configured `wheeledodometry` movement sensor, after every time `time_interval_msec` elapses during a [session](/program/apis/sessions), your robot calculates an estimation of the position, orientation, linear velocity, and angular velocity of the wheeled base.
You can access these readings through the [movement sensor API](/components/movement-sensor/#api).

After configuring a `wheeledodometry` movement sensor, you can operate your base with Viam's built-in services like the [navigation service](/services/navigation/).
