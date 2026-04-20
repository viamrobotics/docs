---
title: "sensor-controlled"
linkTitle: "sensor-controlled"
weight: 40
type: "docs"
description: "Reference for the sensor-controlled base model. Sensor-controlled base, a robotic base with feedback control from a movement sensor."
images: ["/icons/components/base.svg"]
tags: ["base", "components"]
aliases:
  - "/components/base/sensor-controlled/"
  - "/reference/components/base/sensor-controlled/"
component_description: "Wrap other base models and add feedback control using a movement sensor."
# SMEs: Rand H., Martha J.
---

A `sensor-controlled` base supports a robotic base with feedback control from a movement sensor.

{{% alert title="Requirements" color="note" %}}
In order to use feedback control, you must provide a movement sensor that implements [AngularVelocity()](/reference/apis/components/movement-sensor/#getangularvelocity) and [LinearVelocity()](/reference/apis/components/movement-sensor/#getlinearvelocity). This will enable feedback control for [SetVelocity()](/reference/apis/components/base/#setvelocity).

In order to use feedback control for [Spin()](/reference/apis/components/base/#spin), you must also provide a movement sensor that implements [Orientation()](/reference/apis/components/movement-sensor/#getorientation).

In order to use feedback control for [MoveStraight()](/reference/apis/components/base/#spin), you must also provide a movement sensor that implements [Position()](/reference/apis/components/movement-sensor/#getposition).
Additionally, heading feedback control while moving straight can be used by providing a movement sensor that implements [Orientation()](/reference/apis/components/movement-sensor/#getorientation) or [CompassHeading()](/reference/apis/components/movement-sensor/#getcompassheading).
{{% /alert %}}

To configure a `sensor-controlled` base as a component of your machine, first configure the [model of base](/reference/components/base/) you want to wrap with feedback control and each required [movement sensor](/reference/components/movement-sensor/).
To see what models of movement sensor report which feedback, reference the appropriate column in [Movement Sensor API](/reference/apis/components/movement-sensor/#api).

Configure a `sensor-controlled` base as follows:

{{< tabs name="Configure a Sensor-Controlled Base" >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    { ... INSERT MOVEMENT SENSOR CONFIGURATION },
    { ... INSERT BASE CONFIGURATION },
    {
      "name": "my-sensor-controlled-base",
      "model": "sensor-controlled",
      "api": "rdk:component:base",
      "attributes": {
        "movement_sensor": [
          "<your-orientation-or-velocity-movement-sensor-1>",
          "<your-orientation-or-velocity-movement-sensor-2>"
        ],
        "base": "<your-base>"
      },
      "depends_on": []
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `sensor-controlled` bases:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `movement_sensor` | array | **Required** | Array with the `name`s of any movement sensors on your base you want to gather feedback from. The driver will select the first movement sensor providing appropriate feedback for either the `SetVelocity()` or the `Spin()` endpoint. <br> If your sensor has an adjustable frequency or period, set the frequency to something greater than or equal to the `control_frequency_hz`. A higher frequency will generally result in more stable behavior because the base control loop that adjusts the machine's behavior runs more frequently. |
| `base` | string | **Required** | String with the `name` of the base you want to wrap with sensor control. |
| `control_parameters` | object | Optional | A JSON object containing the coefficients for the proportional, integral, and derivative terms for linear and angular velocity. If you want these values to be auto-tuned, you can set all values to 0: `[ { "type": "linear_velocity", "p": 0, "i": 0, "d": 0 }, { "type": "angular_velocity", "p": 0, "i": 0, "d": 0 } ]`, and `viam-server` will auto-tune and log the calculated values. Tuning takes several seconds and spins the motors. Copy the values from the logs and add them to the configuration once tuned for the values to take effect. If you need to auto-tune multiple controlled components that depend on the same hardware, such as a sensor controlled base and one of the motors on the base, run the auto-tuning process one component at a time. For more information see [Feedback control](#feedback-control). |
| `control_frequency_hz` | float | Optional | Adjusts the frequency that the base control loop runs at. A higher frequency will generally result in more stable behavior because the base control loop that adjusts the machine's behavior runs more frequently, provided the movement sensors can support the higher frequency. The default base control loop frequency is 10Hz. |

## Feedback control

### SetVelocity

{{< readfile "/static/include/components/base-sensor.md" >}}

### Spin

When the `control_parameters` attribute is set, `Spin` implements a form of feedback control that polls the provided movement sensor and corrects any error between the desired angular velocity and the actual angular velocity using a PID control loop. `Spin` also monitors the angular distance traveled and stops the base when the goal angle is reached.

### MoveStraight

When `control_parameters` is set, `MoveStraight` calculates the required velocity to reach the desired velocity and distance. It then polls the provided velocity movement sensor and corrects any error between this calculated velocity and the actual velocity using a PID control loop. `MoveStraight` also monitors the position and stops the base when the goal distance is reached. If a compass heading movement sensor is provided, `MoveStraight` will attempt to keep the heading of the base fixed in the original direction it was faced at the beginning of the `MoveStraight` call.
