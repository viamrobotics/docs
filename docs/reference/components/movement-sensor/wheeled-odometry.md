---
title: "wheeled-odometry"
linkTitle: "wheeled-odometry"
type: "docs"
description: "Reference for the wheeled-odometry movement-sensor model. Wheeled odometry movement sensor."
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
aliases:
  - "/components/movement-sensor/wheeled-odometry/"
  - "/operate/reference/components/movement-sensor/wheeled-odometry/"
component_description: "A model that uses encoders to get an odometry estimate from a wheeled base."
# SMEs: Rand, Martha
---

Configure a `wheeled-odometry` movement sensor to implement _wheeled odometry_ on your machine.

_Wheeled odometry_ is the estimation of the rate of change of position, orientation, linear velocity, and angular velocity using the dimensions of a base, calculated by measuring the movement of the motors through encoders.
Because of this method of estimation, you don't have to have a specific piece of movement sensor hardware to implement `wheeled-odometry` on your machine.
This model uses [encoders](/reference/components/encoder/) from [position reporting motors](/reference/components/motor/) to get an odometry estimate of a wheeled base as it moves.

With a configured `wheeled-odometry` movement sensor, your machine calculates an estimation of the position, orientation, linear velocity, and angular velocity of the wheeled base each time `time_interval_msec` elapses during a [session](/reference/apis/sessions/).
You can access these readings through the [movement sensor API](/reference/apis/components/movement-sensor/#api).
For the best accuracy with odometry calculations, it is recommended you configure a time interval of less than `1000` milliseconds.

After configuring a `wheeled-odometry` movement sensor, you can operate your base with Viam's built-in services like the [navigation service](/navigation/).

## Set-up requirements

To prepare your machine, attach [encoders](/reference/components/encoder/) to each of the position-reporting motors on your base to measure their rotation.

- Select and configure motors that can report their own position, like [`gpio` motors](/reference/components/motor/gpio/) with [encoders](/reference/components/encoder/), or the [`odrive` module](https://github.com/viam-modules/odrive).
  You can access this property of a configured motor through the [motor API's `GetProperties()`](/reference/apis/components/motor/#getproperties).
- Configure your rover as a [wheeled base component](/reference/components/base/wheeled/).
  Make sure to configure the base width and circumference, as these measurements as a property of the base are vital for accurate odometry estimations by your movement sensor.
  This movement sensor accesses these values through the base's `GetProperties()` API method.
- Then, proceed to [configure](#configuration) a `wheeled-odometry` movement sensor with the name of each of the motor components.

## Configuration

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "<your-wheeledodometry-movement-sensor-name>",
      "model": "wheeled-odometry",
      "api": "rdk:component:movement_sensor",
      "attributes": {
        "base": "<your-base-name>",
        "left_motors": ["<your-base-left-motor-name-1>", "<your-base-left-motor-name-2>"],
        "right_motors": ["<your-base-right-motor-name-1", "your-base-right-motor-name-2>"],
        "time-interval-msec": <number>
      }
    }
  ]
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "name": "my-wheeled-odometer",
      "model": "wheeled-odometry",
      "api": "rdk:component:movement_sensor",
      "attributes": {
        "base": "my_wheeled_base",
        "left_motors": ["leftm1", "leftm2"],
        "right_motors": ["rightm1", "rightm2"]
      }
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

## Attributes

The following attributes are available for `wheeled-odometry` movement sensors:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `base` | string | **Required** | The `name` of the [base](/reference/components/base/) to which the encoders making up this movement sensor are wired. |
| `left_motors` | object | **Required** | A list containing the name of each of the bases' left [position-reporting motors](/reference/components/motor/gpio/). |
| `right_motors` | object | **Required** | A list containing the name of each of the bases' right [position-reporting motors](/reference/components/motor/gpio/). |
| `time_interval_msec` | float | Optional | The time in milliseconds between each wheeled odometry calculation.<br>Default: `500.0`</br> |
