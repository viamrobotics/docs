---
title: "Configure a wheeled-odometry movement sensor"
linkTitle: "wheeled-odometry"
type: "docs"
description: "Configure a wheeled-odometry movement sensor."
images: ["/icons/components/imu.svg"]
tags:
  [
    "movement sensor",
    "components",
    "encoder",
    "motor",
    "base",
    "wheeled",
    "odometry",
  ]
# SMEs: Rand, Martha
---

Configure a `wheeled-odometry` movement sensor to implement _wheeled odometry_ on your robot.

_Wheeled odometry_ is the estimation of the rate of change of position, orientation, linear velocity, and angular velocity using the dimensions of a base, calculated by measuring the movement of the motors through encoders.
Because of this method of estimation, you don't have to have a specific piece of movement sensor hardware to implement `wheeled-odometry` on your robot.
This model uses [encoders](/components/encoder/) from [position reporting motors](/components/motor/) to get an odometry estimate of a wheeled base as it moves.

With a configured `wheeled-odometry` movement sensor, your robot calculates an estimation of the position, orientation, linear velocity, and angular velocity of the wheeled base each time `time_interval_msec` elapses during a [session](/program/apis/sessions/).
You can access these readings through the [movement sensor API](/components/movement-sensor/#api).
For the best accuracy with odometry calculations, it is recommended you configure a time interval of less than `1000` milliseconds.

After configuring a `wheeled-odometry` movement sensor, you can operate your base with Viam's built-in services like the [navigation service](/services/navigation/).

## Set-up requirements

To prepare your robot, attach [encoders](/components/encoder/) to each of the position-reporting motors on your base to measure their rotation.

- Select motors that can report their own position, like an encoded [`roboclaw`](/components/motor/roboclaw/) or [`gpio` motors](/components/motor/gpio/) with [encoders](/components/encoder/#configuration), or the [`odrive`](/extend/modular-resources/examples/odrive/) module.
  You can access this property of a configured motor through the [motor API's `GetProperties()`](/components/motor/#getproperties).
- Configure your rover as a [wheeled base component](/components/base/wheeled/).
  Make sure to configure the base width and circumference, as these measurements as a property of the base are vital for accurate odometry estimations by your movement sensor.
  This movement sensor accesses these values through the base's `GetProperties()` API method.
- Configure each of the position-reporting motors [as motor components](/components/motor/).
- Then, proceed to [configure](#configuration) a `wheeled-odometry` movement sensor with the name of each of the motor components.

## Configuration

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Select **Raw JSON** mode.
Copy and paste the following:

```json {class="line-numbers linkable-line-numbers"}
"name" : "<your-wheeledodometry-movement-sensor-name>",
"type" : "movement_sensor",
"model" : "wheeled-odometry",
"attributes" : {
    "base" : "<your-base-name>",
    "left_motors" : ["<your-base-left-motor-name-1>", "<your-base-left-motor-name-2>"],
    "right_motors" : ["<your-base-right-motor-name-1", "your-base-right-motor-name-2>"],
    "time-interval-msec": <number>
}
```

Fill in and edit the attributes as applicable.

## Attributes

The following attributes are available for `wheeled-odometry` movement sensors:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `base` | string | **Required** | The `name` of the [base](/components/base/) to which the encoders making up this movement sensor are wired. |
| `left_motors` | object | **Required** | A list containing the name of each of the bases' left [position-reporting motors](/components/motor/gpio/). |
| `right_motors` | object | **Required** | A list containing the name of each of the bases' right [position-reporting motors](/components/motor/gpio/). |
| `time_interval_msec` | number | Optional | The time in milliseconds between each wheeled odometry calculation.<br>Default: `500.0`</br> |

{{< readfile "/static/include/components/movement-sensor-control.md" >}}
