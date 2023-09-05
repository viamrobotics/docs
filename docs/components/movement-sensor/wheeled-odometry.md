---
title: "Configure a wheeled-odometry movement sensor"
linkTitle: "wheeled-odometry"
type: "docs"
description: "Configure a wheeled-odometry movement sensor."
images: ["/icons/components/imu.svg"]
tags: ["movement sensor", "components", "movement sensor"]
# SMEs: Rand, Martha
---

Configure a `wheeled-odometry` movement sensor to implement _wheeled odometry_ on your robot.

_Wheeled odometry_ is the estimation of the rate of change of position, orientation, linear velocity, and angular velocity using the dimensions of a base, calculated by measuring the movement of the motors through encoders.
This model uses [encoders](/components/encoder/) from [position reporting motors](/components/motor/) to get an odometry estimate of a wheeled base as it moves.

With a configured `wheeled-odometry` movement sensor, after every time `time_interval_msec` elapses during a [session](/program/apis/sessions/), your robot calculates an estimation of the position, orientation, linear velocity, and angular velocity of the wheeled base.
You can access these readings through the [movement sensor API](/components/movement-sensor/#api).
For the best accuracy with odometry calculations, it is recommended you configure a time interval less of than `1000` milliseconds.

After configuring a `wheeled-odometry` movement sensor, you can operate your base with Viam's built-in services like the [navigation service](/services/navigation/).

## Set-up requirements

To prepare your robot, attach [encoders](/components/encoder/) to each of the position-reporting motors on your base to measure their rotation.

- Pick out motors that can report their own position, like an encoded [`roboclaw`](/components/motor/roboclaw/) or [`gpio` motors](/components/motor/gpio/) with [encoders](/components/encoder/#configuration), or the [`odrive`](/extend/modular-resources/examples/odrive/) module.
You can access this property of a configured motor through the [motor API's `GetProperties()`](/components/motor/#getproperties).
- Configure your rover as a [wheeled base component](/components/base/wheeled/).
- Configure each of the position-reporting motors [as motor components](/components/motor/).
- Then, proceed to [configure](#configuration) a `wheeledodometry` movement sensor with the name of each of the motor components.

{{% alert title="Tip" color="tip" %}}

The `roboclaw` motor does not require you to configure [encoder components](/components/encoder/#configuration) for use with the `wheeled-odometry` movement sensor.
It reports its own position with a built-in encoded motor.

{{% /alert %}}

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
| `left_motors` | object | **Required** | A list holding the name of each of the bases' left [position-reporting motors](/components/motor/gpio/). |
| `right_motors` | object | **Required** | A list holding the name of each of the bases' right [position-reporting motors](/components/motor/gpio/). |
| `time_interval_msec` | number | Optional | The time in between each wheeled odometry calculation. <br> Default: `500.0` </br> |
